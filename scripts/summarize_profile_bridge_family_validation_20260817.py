"""Summarise matched-density bridge-family validation."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np
from scipy.stats import chi2_contingency, spearmanr


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def holm_adjust(p_values: np.ndarray) -> np.ndarray:
    """Return general Holm-adjusted p-values."""
    p_values = np.asarray(p_values, dtype=float)
    order = np.argsort(p_values)
    adjusted = np.empty_like(p_values)
    running = 0.0
    m = p_values.size
    for rank, index in enumerate(order):
        running = max(running, (m - rank) * p_values[index])
        adjusted[index] = min(1.0, running)
    return adjusted


def fit_family_models(rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    """Measure improvement after adding family terms to log-kappa scaling."""
    repetitions = int(rows[0]["repetitions"])
    rejection = np.asarray([float(row["studentized_rejection"]) for row in rows])
    smoothed = (rejection * repetitions + 0.5) / (repetitions + 1.0)
    response = np.log(smoothed / (1.0 - smoothed))
    log_kappa = np.log([float(row["n_epsilon_squared"]) for row in rows])
    families = [row["bridge_family"] for row in rows]
    levels = ("exponential", "half_normal", "scaled_beta12")
    dummies = np.column_stack(
        [np.asarray([family == level for family in families], dtype=float) for level in levels]
    )
    designs = {
        "log_kappa_only": np.column_stack((np.ones(len(rows)), log_kappa)),
        "log_kappa_plus_family": np.column_stack(
            (np.ones(len(rows)), log_kappa, dummies)
        ),
        "log_kappa_family_interaction": np.column_stack(
            (np.ones(len(rows)), log_kappa, dummies, dummies * log_kappa[:, None])
        ),
    }
    outputs = []
    for name, design in designs.items():
        fitted = design @ np.linalg.lstsq(design, response, rcond=None)[0]
        residual = float(np.sum((response - fitted) ** 2))
        total = float(np.sum((response - np.mean(response)) ** 2))
        outputs.append(
            {
                "model": name,
                "parameters": design.shape[1],
                "r_squared": 1.0 - residual / total,
                "rmse_logit": float(np.sqrt(np.mean((response - fitted) ** 2))),
            }
        )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "confirmatory"), default="pilot")
    args = parser.parse_args()
    source = RESULTS_DIR / (
        f"profile_bridge_family_validation_{args.phase}_20260817.tsv"
    )
    with source.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))

    grouped: dict[tuple[int, float], list[dict[str, str]]] = {}
    for row in rows:
        key = (int(row["n"]), float(row["bridge_probability"]))
        grouped.setdefault(key, []).append(row)
    contrasts = []
    raw_p_values = []
    for (n, probability), group in sorted(grouped.items()):
        repetitions = int(group[0]["repetitions"])
        rejection = np.asarray(
            [float(row["studentized_rejection"]) for row in group]
        )
        counts = np.rint(rejection * repetitions).astype(int)
        table = np.column_stack((counts, repetitions - counts))
        chi_square, p_value, _, _ = chi2_contingency(table, correction=False)
        raw_p_values.append(p_value)
        bootstrap = np.asarray(
            [float(row["median_sqrt_n_bootstrap_spread"]) for row in group]
        )
        contrasts.append(
            {
                "n": n,
                "bridge_probability": probability,
                "n_epsilon_squared": n * probability**2,
                "min_rejection": float(np.min(rejection)),
                "max_rejection": float(np.max(rejection)),
                "rejection_range": float(np.ptp(rejection)),
                "min_median_bootstrap_spread": float(np.min(bootstrap)),
                "max_median_bootstrap_spread": float(np.max(bootstrap)),
                "bootstrap_spread_range": float(np.ptp(bootstrap)),
                "family_homogeneity_chi_square": float(chi_square),
                "family_homogeneity_p": float(p_value),
                "family_cramers_v": float(np.sqrt(chi_square / (4 * repetitions))),
            }
        )
    adjusted = holm_adjust(np.asarray(raw_p_values))
    for row, adjusted_p in zip(contrasts, adjusted):
        row["family_homogeneity_holm_p"] = float(adjusted_p)
    contrast_name = (
        "profile_bridge_family_group_contrasts_20260817.tsv"
        if args.phase == "pilot"
        else "profile_bridge_family_confirmatory_contrast_20260817.tsv"
    )
    write_tsv(RESULTS_DIR / contrast_name, contrasts)

    models: list[dict[str, float | str]] = []
    correlations: list[dict[str, float | str]] = []
    if len({row["n_epsilon_squared"] for row in rows}) > 1:
        models = fit_family_models(rows)
        write_tsv(RESULTS_DIR / "profile_bridge_family_models_20260817.tsv", models)

        rejection = np.asarray([float(row["studentized_rejection"]) for row in rows])
        diagnostic_specs = (
            ("median_spacing_risk", 1.0),
            ("median_valley_density_iqr", -1.0),
            ("median_sqrt_n_bootstrap_spread", 1.0),
            ("spacing_warning_rate", 1.0),
            ("valley_density_warning_rate", 1.0),
            ("bootstrap_warning_rate", 1.0),
        )
        for name, orientation in diagnostic_specs:
            values = orientation * np.asarray([float(row[name]) for row in rows])
            correlation, p_value = spearmanr(values, rejection)
            correlations.append(
                {
                    "diagnostic_risk_score": name,
                    "orientation": "high_risk" if orientation > 0 else "low_is_risk",
                    "spearman_rejection": float(correlation),
                    "spearman_p": float(p_value),
                }
            )
        write_tsv(
            RESULTS_DIR / "profile_bridge_family_diagnostic_correlations_20260817.tsv",
            correlations,
        )
    for row in contrasts + models + correlations:
        print(row)


if __name__ == "__main__":
    main()
