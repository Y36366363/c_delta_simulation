"""Summarise the n * bridge_probability^2 recovery scaling."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def fit_collapse_models(
    n: np.ndarray, probability: np.ndarray, rejection: np.ndarray, repetitions: int
) -> list[dict[str, float | str]]:
    """Compare n*epsilon and n*epsilon^2 on the empirical logit scale."""
    n = np.asarray(n, dtype=float)
    probability = np.asarray(probability, dtype=float)
    rejection = np.asarray(rejection, dtype=float)
    if np.any(probability <= 0.0):
        raise ValueError("collapse fitting requires positive bridge probabilities")
    smoothed = (rejection * repetitions + 0.5) / (repetitions + 1.0)
    response = np.log(smoothed / (1.0 - smoothed))

    def fit(name: str, design: np.ndarray) -> dict[str, float | str]:
        coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
        fitted = design @ coefficients
        residual = float(np.sum((response - fitted) ** 2))
        total = float(np.sum((response - np.mean(response)) ** 2))
        return {
            "model": name,
            "r_squared": 1.0 - residual / total,
            "intercept": float(coefficients[0]),
            "slope_1": float(coefficients[1]),
            "slope_2": (
                float(coefficients[2]) if coefficients.size > 2 else float("nan")
            ),
            "implied_probability_exponent": (
                float(coefficients[2] / coefficients[1])
                if name == "free_log_n_log_probability"
                else (1.0 if name == "log_n_probability" else 2.0)
            ),
        }

    ones = np.ones(n.size)
    return [
        fit(
            "log_n_probability",
            np.column_stack((ones, np.log(n * probability))),
        ),
        fit(
            "log_n_probability_squared",
            np.column_stack((ones, np.log(n * probability**2))),
        ),
        fit(
            "free_log_n_log_probability",
            np.column_stack((ones, np.log(n), np.log(probability))),
        ),
    ]


def main() -> None:
    source = RESULTS_DIR / "profile_bridge_calibration_pilot_20260817.tsv"
    with source.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    positive = []
    for row in rows:
        probability = float(row["scenario"].rsplit("_", 1)[1])
        if probability > 0.0:
            positive.append((row, probability))
    repetitions = int(positive[0][0]["repetitions"])
    models = fit_collapse_models(
        np.asarray([int(row["n"]) for row, _ in positive]),
        np.asarray([probability for _, probability in positive]),
        np.asarray([float(row["studentized_rejection"]) for row, _ in positive]),
        repetitions,
    )
    write_tsv(RESULTS_DIR / "profile_bridge_collapse_models_20260817.tsv", models)

    lookup = {
        (int(row["n"]), probability): float(row["studentized_rejection"])
        for row, probability in positive
    }
    matched = []
    for probability_80 in (0.05, 0.10, 0.20):
        probability_320 = probability_80 / 2.0
        rejection_80 = lookup[(80, probability_80)]
        rejection_320 = lookup[(320, probability_320)]
        matched.append(
            {
                "n_epsilon_squared": 80 * probability_80**2,
                "epsilon_n80": probability_80,
                "rejection_n80": rejection_80,
                "epsilon_n320": probability_320,
                "rejection_n320": rejection_320,
                "absolute_rejection_difference": abs(rejection_80 - rejection_320),
            }
        )
    write_tsv(RESULTS_DIR / "profile_bridge_matched_kappa_20260817.tsv", matched)
    for row in models + matched:
        print(row)


if __name__ == "__main__":
    main()
