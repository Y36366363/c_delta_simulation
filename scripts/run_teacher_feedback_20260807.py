"""Focused validation of Professor Hoorn's 2026-08-07 questions."""

from __future__ import annotations

from pathlib import Path
import csv
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta_from_profiles,
    center_salience_vector,
    divergence_vector,
    huber_reference_profile,
)
from scripts.robust_extension_utils import write_tsv


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def _profile_cdelta(x: np.ndarray, y: np.ndarray) -> float:
    return float(c_delta_from_profiles(x, y)["raw"])


def _permutation_pvalues(
    sx: np.ndarray,
    sy: np.ndarray,
    indices: np.ndarray,
) -> tuple[float, float, float]:
    observed_c = _profile_cdelta(sx, sy)
    observed_r = _pearson(sx, sy)
    denominator = float(np.mean(sx) * np.mean(sy))
    c_values = (sy[indices] @ sx) / sx.size / denominator
    centered_x = sx - np.mean(sx)
    centered_y = sy - np.mean(sy)
    r_values = (
        centered_y[indices] @ centered_x
        / np.sqrt(np.sum(centered_x**2) * np.sum(centered_y**2))
    )
    p_c = (1 + int(np.sum(c_values >= observed_c))) / (indices.shape[0] + 1)
    p_r = (1 + int(np.sum(r_values >= observed_r))) / (indices.shape[0] + 1)
    rank_disagreement = float(np.max(np.abs(np.argsort(np.argsort(c_values)) - np.argsort(np.argsort(r_values)))))
    return p_c, p_r, rank_disagreement


def _feedback_pair(
    rng: np.random.Generator, scenario: str, n: int
) -> tuple[np.ndarray, np.ndarray]:
    if scenario == "normal_correlated":
        x = rng.normal(size=n)
        return x, 0.45 * x + np.sqrt(1.0 - 0.45**2) * rng.normal(size=n)
    if scenario == "t3_correlated":
        common = rng.standard_t(3, size=n)
        return common + rng.standard_t(3, size=n), common + rng.standard_t(3, size=n)
    if scenario == "skew_correlated":
        u = rng.normal(size=n)
        v = 0.45 * u + np.sqrt(1.0 - 0.45**2) * rng.normal(size=n)
        return np.exp(0.7 * u), np.exp(0.7 * v)
    x, y = rng.normal(size=n), rng.normal(size=n)
    if scenario == "matched_outlier":
        x[0] = 15.0
        y[0] = 15.0
    elif scenario == "unmatched_outlier":
        x[0] = 15.0
        y[1] = 15.0
    else:
        raise ValueError(scenario)
    return x, y


def profile_pearson_validation(
    *, seed: int = 20260927, n: int = 80, n_perm: int = 4999
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for scenario in (
        "normal_correlated",
        "t3_correlated",
        "skew_correlated",
        "matched_outlier",
        "unmatched_outlier",
    ):
        x, y = _feedback_pair(rng, scenario, n)
        standardized_x = huber_reference_profile(x)
        standardized_y = huber_reference_profile(y)
        unscaled_x = center_salience_vector(x, center="huber")
        unscaled_y = center_salience_vector(y, center="huber")
        coefficient = _profile_cdelta(standardized_x, standardized_y)
        correlation = _pearson(standardized_x, standardized_y)
        cv_product = (
            np.std(standardized_x) / np.mean(standardized_x)
            * np.std(standardized_y) / np.mean(standardized_y)
        )
        indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
        p_c, p_r, rank_disagreement = _permutation_pvalues(
            standardized_x, standardized_y, indices
        )
        rows.append(
            {
                "scenario": scenario,
                "n": n,
                "n_perm": n_perm,
                "c_delta_star": coefficient,
                "pearson_robust_absolute_residuals": correlation,
                "cv_product": float(cv_product),
                "identity_value": float(1.0 + correlation * cv_product),
                "identity_absolute_error": abs(
                    coefficient - (1.0 + correlation * cv_product)
                ),
                "unscaled_residual_cdelta": _profile_cdelta(unscaled_x, unscaled_y),
                "scale_normalisation_absolute_difference": abs(
                    coefficient - _profile_cdelta(unscaled_x, unscaled_y)
                ),
                "permutation_p_cdelta": p_c,
                "permutation_p_pearson": p_r,
                "permutation_p_absolute_difference": abs(p_c - p_r),
                "maximum_permutation_rank_disagreement": rank_disagreement,
            }
        )
    return rows


def _distance_matrix(values: np.ndarray) -> np.ndarray:
    return np.abs(values[:, None] - values[None, :])


def _mantel_correlation(x: np.ndarray, y: np.ndarray) -> float:
    upper = np.triu_indices(x.size, k=1)
    return _pearson(_distance_matrix(x)[upper], _distance_matrix(y)[upper])


def mantel_information_validation(
    *, repetitions: int = 2000, seed: int = 20260928
) -> list[dict[str, float | int]]:
    rng = np.random.default_rng(seed)
    radii = np.repeat(np.linspace(0.5, 5.0, 20), 2)
    signs_x = np.tile(np.array([1.0, -1.0]), 20)
    x = radii * signs_x
    dx = divergence_vector(x, kind="l2")
    variance = float(np.mean((x - np.mean(x)) ** 2))
    closed_form = np.sqrt(
        x.size
        / (x.size - 1.0)
        * ((x - np.mean(x)) ** 2 + variance)
    )
    identity_error = float(np.max(np.abs(dx - closed_form)))
    rows: list[dict[str, float | int]] = []
    for flip_probability in (0.0, 0.25, 0.50, 0.75, 1.0):
        c_values, profile_correlations, mantel_correlations = [], [], []
        for _ in range(repetitions):
            pair_flips = rng.random(20) < flip_probability
            signs_y = signs_x.copy()
            for pair, flip in enumerate(pair_flips):
                if flip:
                    signs_y[2 * pair : 2 * pair + 2] *= -1.0
            y = radii * signs_y
            dy = divergence_vector(y, kind="l2")
            c_values.append(_profile_cdelta(dx, dy))
            profile_correlations.append(_pearson(dx, dy))
            mantel_correlations.append(_mantel_correlation(x, y))
        rows.append(
            {
                "n": x.size,
                "flip_probability": flip_probability,
                "repetitions": repetitions,
                "mean_c_delta": float(np.mean(c_values)),
                "sd_c_delta": float(np.std(c_values)),
                "mean_profile_correlation": float(np.mean(profile_correlations)),
                "minimum_profile_correlation": float(np.min(profile_correlations)),
                "mean_mantel_correlation": float(np.mean(mantel_correlations)),
                "sd_mantel_correlation": float(np.std(mantel_correlations)),
                "minimum_mantel_correlation": float(np.min(mantel_correlations)),
                "maximum_mantel_correlation": float(np.max(mantel_correlations)),
                "l2_row_profile_identity_max_error": identity_error,
            }
        )
    return rows


METHODS = {
    "original_l2": lambda values: divergence_vector(values, kind="l2"),
    "huber_uncapped_cdelta_star": lambda values: huber_reference_profile(values),
    "huber_cap6_sensitivity": lambda values: huber_reference_profile(values, cap=6.0),
}


def outlier_estimand_validation(
    *, repetitions: int = 1000, seed: int = 20260929, n: int = 60
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    summaries: dict[tuple[str, str, float], dict[str, list[float]]] = {}
    for condition in ("matched", "unmatched"):
        for magnitude in (2.0, 4.0, 8.0, 16.0, 32.0):
            for method in METHODS:
                summaries[(condition, method, magnitude)] = {
                    "cdelta": [],
                    "correlation": [],
                    "top_share": [],
                    "ordinary_shift_x": [],
                    "ordinary_shift_y": [],
                }
    for _ in range(repetitions):
        base_x, base_y = rng.normal(size=n), rng.normal(size=n)
        base_profiles = {
            method: (profile(base_x), profile(base_y))
            for method, profile in METHODS.items()
        }
        for condition in ("matched", "unmatched"):
            for magnitude in (2.0, 4.0, 8.0, 16.0, 32.0):
                x, y = base_x.copy(), base_y.copy()
                x[0] = magnitude
                if condition == "matched":
                    y[0] = magnitude
                    ordinary = np.arange(n) != 0
                else:
                    y[1] = magnitude
                    ordinary = (np.arange(n) != 0) & (np.arange(n) != 1)
                for method, profile in METHODS.items():
                    sx, sy = profile(x), profile(y)
                    base_sx, base_sy = base_profiles[method]
                    products = sx * sy
                    cell = summaries[(condition, method, magnitude)]
                    cell["cdelta"].append(_profile_cdelta(sx, sy))
                    cell["correlation"].append(_pearson(sx, sy))
                    cell["top_share"].append(
                        float(np.max(products) / np.sum(products))
                    )
                    cell["ordinary_shift_x"].append(
                        float(
                            np.mean(np.abs(sx[ordinary] - base_sx[ordinary]))
                            / np.mean(base_sx[ordinary])
                        )
                    )
                    cell["ordinary_shift_y"].append(
                        float(
                            np.mean(np.abs(sy[ordinary] - base_sy[ordinary]))
                            / np.mean(base_sy[ordinary])
                        )
                    )
    rows: list[dict[str, float | int | str]] = []
    for (condition, method, magnitude), values in summaries.items():
        rows.append(
            {
                "condition": condition,
                "method": method,
                "magnitude": magnitude,
                "n": n,
                "repetitions": repetitions,
                "mean_cdelta": float(np.mean(values["cdelta"])),
                "mean_profile_correlation": float(np.mean(values["correlation"])),
                "median_largest_numerator_share": float(
                    np.median(values["top_share"])
                ),
                "mean_ordinary_profile_shift_x": float(
                    np.mean(values["ordinary_shift_x"])
                ),
                "mean_ordinary_profile_shift_y": float(
                    np.mean(values["ordinary_shift_y"])
                ),
            }
        )
    return rows


def cross_building_reanalysis() -> list[dict[str, float | int | str]]:
    """Summarise the existing high-replication block-null experiment."""
    source = PROJECT_ROOT / "results" / "design_respecting_permutation_20260805.tsv"
    with source.open() as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    grouped: dict[tuple[str, str], list[float]] = {}
    for row in rows:
        if row["family"] != "conditional_null":
            continue
        key = (row["method"], row["permutation_scheme"])
        grouped.setdefault(key, []).append(float(row["rejection_rate"]))
    output: list[dict[str, float | int | str]] = []
    for (method, scheme), rates in sorted(grouped.items()):
        output.append(
            {
                "method": method,
                "permutation_scheme": scheme,
                "conditions": len(rates),
                "repetitions_per_condition": 1500,
                "mean_rejection_rate": float(np.mean(rates)),
                "minimum_rejection_rate": float(np.min(rates)),
                "maximum_rejection_rate": float(np.max(rates)),
            }
        )
    return output


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "teacher_profile_pearson_20260807.tsv",
        profile_pearson_validation(),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "teacher_mantel_information_20260807.tsv",
        mantel_information_validation(),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "teacher_outlier_estimand_20260807.tsv",
        outlier_estimand_validation(),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "teacher_cross_building_reanalysis_20260807.tsv",
        cross_building_reanalysis(),
    )
