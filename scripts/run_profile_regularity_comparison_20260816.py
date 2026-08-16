"""Compare weak-null correlation tests along a profile-regularity path."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)
from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
)


RESULTS_DIR = PROJECT_ROOT / "results"
RADIAL_LOG_SDS = (0.03, 0.10, 0.20, 0.40, 0.80)
GAP_THRESHOLDS = (0.50, 0.75, 0.90)
GATE_CV_SCENARIOS = (
    "independent_t5",
    "independent_strong_skew",
    "profile_null_t5_sign_link",
    "independent_affine_near_constant",
)


def generate_sign_link_profile_null(
    rng: np.random.Generator, n: int, radial_log_sd: float
) -> tuple[np.ndarray, np.ndarray]:
    """Return dependent margins with independent population radius profiles."""
    signs = rng.choice((-1.0, 1.0), size=n)
    radius_x = np.exp(radial_log_sd * rng.normal(size=n))
    radius_y = np.exp(radial_log_sd * rng.normal(size=n))
    return signs * radius_x, signs * radius_y


def largest_interior_spacing_ratio(
    values: np.ndarray, *, trim_fraction: float = 0.10
) -> float:
    """Scale-free empirical warning for a low-density gap in a margin."""
    values = np.sort(np.asarray(values, dtype=float))
    if values.ndim != 1 or values.size < 20:
        raise ValueError("values must be one-dimensional with size >= 20")
    if not 0.0 <= trim_fraction < 0.25:
        raise ValueError("trim_fraction must be in [0, 0.25)")
    lower = int(np.floor(trim_fraction * values.size))
    upper = int(np.ceil((1.0 - trim_fraction) * values.size))
    interior = values[lower:upper]
    iqr = float(np.quantile(values, 0.75) - np.quantile(values, 0.25))
    if iqr <= 0.0:
        return float("inf")
    return float(np.max(np.diff(interior)) / iqr)


def distance_correlation(values_x: np.ndarray, values_y: np.ndarray) -> float:
    """Biased sample distance correlation, used only as a target comparator."""
    dx = np.abs(values_x[:, None] - values_x[None, :])
    dy = np.abs(values_y[:, None] - values_y[None, :])
    ax = dx - dx.mean(axis=0) - dx.mean(axis=1)[:, None] + dx.mean()
    ay = dy - dy.mean(axis=0) - dy.mean(axis=1)[:, None] + dy.mean()
    cross = float(np.mean(ax * ay))
    self_x = float(np.mean(ax**2))
    self_y = float(np.mean(ay**2))
    if self_x <= 0.0 or self_y <= 0.0:
        return 0.0
    squared = max(0.0, cross / np.sqrt(self_x * self_y))
    return float(np.sqrt(squared))


def run_comparison(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    seed: int,
    phase: str,
    radial_log_sds: tuple[float, ...] = RADIAL_LOG_SDS,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for radial_log_sd in radial_log_sds:
        records = []
        for _ in range(repetitions):
            x, y = generate_sign_link_profile_null(rng, n, radial_log_sd)
            indices = random_indices(rng, n, n_perm)
            result = profile_studentized_permutation_test(x, y, indices)
            observed = float(result["estimate"])
            permuted = np.asarray(result["permuted_estimates"])
            naive_p = (1.0 + np.sum(np.abs(permuted) >= abs(observed))) / (
                n_perm + 1.0
            )
            profile_x = huber_reference_profile(x)
            profile_y = huber_reference_profile(y)
            gap = max(
                largest_interior_spacing_ratio(x),
                largest_interior_spacing_ratio(y),
            )
            records.append(
                (
                    observed,
                    float(result["p_value"]),
                    float(naive_p),
                    gap,
                    float(np.std(profile_x, ddof=1) / np.mean(profile_x)),
                    float(np.std(profile_y, ddof=1) / np.mean(profile_y)),
                    distance_correlation(x, y),
                )
            )
        values = np.asarray(records)
        studentized_count = int(np.sum(values[:, 1] <= 0.05))
        naive_count = int(np.sum(values[:, 2] <= 0.05))
        studentized_interval = wilson(studentized_count, repetitions)
        naive_interval = wilson(naive_count, repetitions)
        row: dict[str, float | int | str] = {
            "phase": phase,
            "radial_log_sd": radial_log_sd,
            "n": n,
            "repetitions": repetitions,
            "n_perm": n_perm,
            "mean_profile_effect": float(np.mean(values[:, 0])),
            "studentized_rejection": studentized_count / repetitions,
            "studentized_wilson_low": studentized_interval[0],
            "studentized_wilson_high": studentized_interval[1],
            "naive_rejection": naive_count / repetitions,
            "naive_wilson_low": naive_interval[0],
            "naive_wilson_high": naive_interval[1],
            "median_max_gap_iqr": float(np.median(values[:, 3])),
            "q95_max_gap_iqr": float(np.quantile(values[:, 3], 0.95)),
            "median_profile_cv_x": float(np.median(values[:, 4])),
            "median_profile_cv_y": float(np.median(values[:, 5])),
            "mean_distance_correlation": float(np.mean(values[:, 6])),
        }
        for threshold in GAP_THRESHOLDS:
            passed = values[:, 3] <= threshold
            suffix = str(threshold).replace(".", "p")
            row[f"gap_{suffix}_pass_rate"] = float(np.mean(passed))
            row[f"gap_{suffix}_studentized_rejection_among_pass"] = (
                float(np.mean(values[passed, 1] <= 0.05))
                if np.any(passed)
                else float("nan")
            )
            row[f"gap_{suffix}_false_rejection_per_all"] = float(
                np.mean(passed & (values[:, 1] <= 0.05))
            )
        rows.append(row)
    return rows


def run_gate_cross_validation(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    seed: int,
    phase: str,
    scenarios: tuple[str, ...] = GATE_CV_SCENARIOS,
) -> list[dict[str, float | int | str]]:
    """Check warning-rate cost in regular heavy-tail and skew models."""
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios:
        records = []
        for _ in range(repetitions):
            if scenario == "independent_affine_near_constant":
                x = 3.0 + 1e-12 * rng.normal(size=n)
                y = -2.0 + 1e-12 * rng.normal(size=n)
            else:
                x, y = generate_stress_scenario(rng, scenario, n, 0.65)
            indices = random_indices(rng, n, n_perm)
            result = profile_studentized_permutation_test(x, y, indices)
            observed = float(result["estimate"])
            permuted = np.asarray(result["permuted_estimates"])
            naive_p = (1.0 + np.sum(np.abs(permuted) >= abs(observed))) / (
                n_perm + 1.0
            )
            gap = max(
                largest_interior_spacing_ratio(x),
                largest_interior_spacing_ratio(y),
            )
            records.append((float(result["p_value"]), float(naive_p), gap))
        values = np.asarray(records)
        row: dict[str, float | int | str] = {
            "phase": phase,
            "scenario": scenario,
            "n": n,
            "repetitions": repetitions,
            "n_perm": n_perm,
            "studentized_rejection": float(np.mean(values[:, 0] <= 0.05)),
            "naive_rejection": float(np.mean(values[:, 1] <= 0.05)),
            "median_max_gap_iqr": float(np.median(values[:, 2])),
            "q95_max_gap_iqr": float(np.quantile(values[:, 2], 0.95)),
        }
        for threshold in GAP_THRESHOLDS:
            passed = values[:, 2] <= threshold
            suffix = str(threshold).replace(".", "p")
            row[f"gap_{suffix}_pass_rate"] = float(np.mean(passed))
            row[f"gap_{suffix}_studentized_rejection_among_pass"] = (
                float(np.mean(values[passed, 0] <= 0.05))
                if np.any(passed)
                else float("nan")
            )
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "pilot"), default="smoke")
    parser.add_argument(
        "--design", choices=("radial_path", "gate_cv"), default="radial_path"
    )
    parser.add_argument("--radial-log-sd", type=float)
    parser.add_argument(
        "--scenario", choices=("all", *GATE_CV_SCENARIOS), default="all"
    )
    args = parser.parse_args()
    if args.phase == "smoke":
        settings = dict(repetitions=20, n=60, n_perm=49, seed=2026081611)
    else:
        settings = dict(repetitions=300, n=80, n_perm=199, seed=2026081612)
    if args.design == "radial_path":
        radial_log_sds = (
            RADIAL_LOG_SDS
            if args.radial_log_sd is None
            else (float(args.radial_log_sd),)
        )
        rows = run_comparison(
            phase=args.phase, radial_log_sds=radial_log_sds, **settings
        )
    else:
        scenarios = (
            GATE_CV_SCENARIOS if args.scenario == "all" else (args.scenario,)
        )
        rows = run_gate_cross_validation(
            phase=args.phase, scenarios=scenarios, **settings
        )
    RESULTS_DIR.mkdir(exist_ok=True)
    suffix = args.phase
    if args.design == "radial_path":
        if args.radial_log_sd is not None:
            suffix += f"_sd{args.radial_log_sd:g}".replace(".", "p")
        stem = "profile_regularity_comparison"
    else:
        if args.scenario != "all":
            suffix += f"_{args.scenario}"
        stem = "profile_regularity_gate_cv"
    output = RESULTS_DIR / f"{stem}_{suffix}_20260816.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
