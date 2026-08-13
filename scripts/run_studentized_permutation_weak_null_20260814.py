"""Fully recomputed studentized permutation tests for profile/Mantel weak nulls."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import _huber_location_influence
from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_weak_null_local_tests_20260814 import (
    _correlation_delta,
    calibrate_mantel_partial_mixture,
    generate_scenario,
    holm_adjust,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def _profile_studentized_score(
    x: np.ndarray,
    y: np.ndarray,
    location_if_x: np.ndarray,
    location_if_y: np.ndarray,
    tx: float,
    ty: float,
) -> tuple[float, float]:
    """Return effect and full-IF z score for one declared pairing."""
    a = np.abs(x - tx)
    b = np.abs(y - ty)
    moments = np.asarray(
        (np.mean(a * b), np.mean(a), np.mean(b), np.mean(a**2), np.mean(b**2))
    )
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    direct = (
        np.column_stack((a * b, a, b, a**2, b**2)) - moments
    ) @ gradient
    mean_a, mean_b = moments[1], moments[2]
    variance_a = moments[3] - mean_a**2
    variance_b = moments[4] - mean_b**2
    denominator = np.sqrt(variance_a * variance_b)
    sign_x = np.sign(x - tx)
    sign_y = np.sign(y - ty)
    covariance_tx = -np.mean(sign_x * b) + np.mean(sign_x) * mean_b
    covariance_ty = -np.mean(a * sign_y) + mean_a * np.mean(sign_y)
    variance_tx = -2.0 * np.mean(x - tx) + 2.0 * mean_a * np.mean(sign_x)
    variance_ty = -2.0 * np.mean(y - ty) + 2.0 * mean_b * np.mean(sign_y)
    coefficient_x = (
        covariance_tx / denominator - 0.5 * estimate * variance_tx / variance_a
    )
    coefficient_y = (
        covariance_ty / denominator - 0.5 * estimate * variance_ty / variance_b
    )
    influence = direct + coefficient_x * location_if_x + coefficient_y * location_if_y
    influence -= np.mean(influence)
    standard_error = np.std(influence, ddof=1) / np.sqrt(x.size)
    if standard_error <= 0.0:
        raise ValueError("profile studentizer is degenerate")
    return float(estimate), float(estimate / standard_error)


def profile_studentized_permutation_test(
    x: np.ndarray,
    y: np.ndarray,
    indices: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """Recompute the complete profile influence variance on every orbit member."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    tx, _, location_if_x = _huber_location_influence(
        x,
        huber_c=1.345,
        density_method="kde",
        analytic_density=None,
        density_folds=5,
        density_seed=2026081411,
    )
    ty, _, location_if_y = _huber_location_influence(
        y,
        huber_c=1.345,
        density_method="kde",
        analytic_density=None,
        density_folds=5,
        density_seed=2026081412,
    )
    observed, observed_z = _profile_studentized_score(
        x, y, location_if_x, location_if_y, tx, ty
    )
    permuted_z = np.empty(indices.shape[0])
    for orbit, index in enumerate(indices):
        _, permuted_z[orbit] = _profile_studentized_score(
            x,
            y[index],
            location_if_x,
            location_if_y[index],
            tx,
            ty,
        )
    p_value = (1.0 + np.sum(np.abs(permuted_z) >= abs(observed_z))) / (
        indices.shape[0] + 1.0
    )
    return {
        "estimate": observed,
        "z_statistic": observed_z,
        "p_value": float(p_value),
        "permuted_z": permuted_z,
    }


def _mantel_studentized_score(
    dx: np.ndarray, dy: np.ndarray
) -> tuple[float, float]:
    """Return Mantel effect and node-Hájek studentized score."""
    n = dx.shape[0]
    upper = np.triu_indices(n, 1)
    a = dx[upper]
    b = dy[upper]
    moments = np.mean(
        np.column_stack((a * b, a, b, a**2, b**2)), axis=0
    )
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    conditional = np.column_stack(
        (
            np.sum(dx * dy, axis=1),
            np.sum(dx, axis=1),
            np.sum(dy, axis=1),
            np.sum(dx**2, axis=1),
            np.sum(dy**2, axis=1),
        )
    ) / (n - 1.0)
    influence = 2.0 * (conditional - moments) @ gradient
    influence -= np.mean(influence)
    standard_error = np.std(influence, ddof=1) / np.sqrt(n)
    if standard_error <= 0.0:
        raise ValueError("Mantel studentizer is degenerate")
    return float(estimate), float(estimate / standard_error)


def mantel_studentized_permutation_test(
    x: np.ndarray,
    y: np.ndarray,
    indices: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """Recompute the node-Hájek variance on every Mantel orbit member."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    dx = np.abs(x[:, None] - x[None, :])
    dy = np.abs(y[:, None] - y[None, :])
    observed, observed_z = _mantel_studentized_score(dx, dy)
    permuted_z = np.empty(indices.shape[0])
    for orbit, index in enumerate(indices):
        permuted_dy = dy[index[:, None], index[None, :]]
        _, permuted_z[orbit] = _mantel_studentized_score(dx, permuted_dy)
    p_value = (1.0 + np.sum(np.abs(permuted_z) >= abs(observed_z))) / (
        indices.shape[0] + 1.0
    )
    return {
        "estimate": observed,
        "z_statistic": observed_z,
        "p_value": float(p_value),
        "permuted_z": permuted_z,
    }


def random_indices(
    rng: np.random.Generator, n: int, n_perm: int
) -> np.ndarray:
    return np.asarray([rng.permutation(n) for _ in range(n_perm)])


def run_validation(
    *, repetitions: int, n: int, n_perm: int, seed: int, phase: str
) -> tuple[list[dict[str, float | int | str]], dict[str, float]]:
    calibration = calibrate_mantel_partial_mixture(
        seed=seed + 100,
        draws=300_000 if phase == "confirmatory" else 100_000,
    )
    aligned_probability = calibration["aligned_probability"]
    rng = np.random.default_rng(seed)
    scenarios = (
        "global_null_profile_margins",
        "profile_null_mantel_alt",
        "global_null_mantel_margins",
        "mantel_null_profile_alt",
        "both_positive_alt",
    )
    rows = []
    for scenario in scenarios:
        records = []
        for _ in range(repetitions):
            x, y = generate_scenario(rng, scenario, n, aligned_probability)
            indices = random_indices(rng, n, n_perm)
            profile = profile_studentized_permutation_test(x, y, indices)
            mantel = mantel_studentized_permutation_test(x, y, indices)
            adjusted_profile, adjusted_mantel = holm_adjust(
                float(profile["p_value"]), float(mantel["p_value"])
            )
            records.append(
                (
                    float(profile["estimate"]),
                    float(profile["z_statistic"]),
                    float(profile["p_value"]),
                    float(mantel["estimate"]),
                    float(mantel["z_statistic"]),
                    float(mantel["p_value"]),
                    adjusted_profile,
                    adjusted_mantel,
                )
            )
        values = np.asarray(records)
        profile_true = scenario in {
            "global_null_profile_margins",
            "profile_null_mantel_alt",
            "global_null_mantel_margins",
        }
        mantel_true = scenario in {
            "global_null_profile_margins",
            "global_null_mantel_margins",
            "mantel_null_profile_alt",
        }
        true_raw = np.zeros(repetitions, dtype=bool)
        true_holm = np.zeros(repetitions, dtype=bool)
        if profile_true:
            true_raw |= values[:, 2] <= 0.05
            true_holm |= values[:, 6] <= 0.05
        if mantel_true:
            true_raw |= values[:, 5] <= 0.05
            true_holm |= values[:, 7] <= 0.05
        holm_count = int(np.sum(true_holm))
        interval = wilson(holm_count, repetitions)
        rows.append(
            {
                "phase": phase,
                "scenario": scenario,
                "n": n,
                "repetitions": repetitions,
                "n_perm": n_perm,
                "mean_profile_effect": float(np.mean(values[:, 0])),
                "mean_profile_z": float(np.mean(values[:, 1])),
                "profile_studentized_permutation_rejection": float(
                    np.mean(values[:, 2] <= 0.05)
                ),
                "holm_profile_rejection": float(np.mean(values[:, 6] <= 0.05)),
                "mean_mantel_effect": float(np.mean(values[:, 3])),
                "mean_mantel_z": float(np.mean(values[:, 4])),
                "mantel_studentized_permutation_rejection": float(
                    np.mean(values[:, 5] <= 0.05)
                ),
                "holm_mantel_rejection": float(np.mean(values[:, 7] <= 0.05)),
                "raw_true_null_fwer": float(np.mean(true_raw)),
                "holm_true_null_fwer": holm_count / repetitions,
                "holm_fwer_wilson_low": interval[0],
                "holm_fwer_wilson_high": interval[1],
                "both_holm_rejection": float(
                    np.mean((values[:, 6] <= 0.05) & (values[:, 7] <= 0.05))
                ),
            }
        )
    return rows, calibration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase", choices=("pilot", "confirmatory", "n160_extension"), default="pilot"
    )
    args = parser.parse_args()
    if args.phase == "pilot":
        settings = dict(repetitions=120, n=80, n_perm=199, seed=2026081421)
    elif args.phase == "confirmatory":
        settings = dict(repetitions=600, n=80, n_perm=499, seed=2026081422)
    else:
        settings = dict(repetitions=400, n=160, n_perm=199, seed=2026081423)
    rows, calibration = run_validation(phase=args.phase, **settings)
    RESULTS_DIR.mkdir(exist_ok=True)
    write_tsv(
        RESULTS_DIR / f"studentized_permutation_weak_null_{args.phase}_20260814.tsv",
        rows,
    )
    write_tsv(
        RESULTS_DIR / f"studentized_permutation_calibration_{args.phase}_20260814.tsv",
        [{"phase": args.phase, **calibration}],
    )
    for row in rows:
        print(row)
    print({"calibration": calibration})


if __name__ == "__main__":
    main()
