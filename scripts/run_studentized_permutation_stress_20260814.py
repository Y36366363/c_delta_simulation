"""Focused stress tests for the iid studentized-permutation candidate."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_weak_null_20260814 import (
    mantel_studentized_permutation_test,
    profile_studentized_permutation_test,
    random_indices,
)
from scripts.run_weak_null_local_tests_20260814 import (
    calibrate_mantel_partial_mixture,
    generate_scenario,
    holm_adjust,
)


RESULTS_DIR = PROJECT_ROOT / "results"
SCENARIOS = (
    "independent_t5",
    "independent_t3_infinite_fourth",
    "independent_strong_skew",
    "profile_null_t5_sign_link",
    "profile_null_near_constant",
    "mantel_null_profile_alt",
)


def generate_stress_scenario(
    rng: np.random.Generator,
    scenario: str,
    n: int,
    aligned_probability: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate global and partial weak-null stress models."""
    if scenario == "independent_t5":
        return rng.standard_t(5.0, n), rng.standard_t(5.0, n)
    if scenario == "independent_t3_infinite_fourth":
        return rng.standard_t(3.0, n), rng.standard_t(3.0, n)
    if scenario == "independent_strong_skew":
        return np.exp(1.1 * rng.normal(size=n)), rng.gamma(0.7, 1.0, size=n)
    if scenario in {"profile_null_t5_sign_link", "profile_null_near_constant"}:
        signs = rng.choice((-1.0, 1.0), size=n)
        if scenario == "profile_null_t5_sign_link":
            radius_x = 0.25 + np.abs(rng.standard_t(5.0, n))
            radius_y = 0.25 + np.abs(rng.standard_t(5.0, n))
        else:
            radius_x = np.maximum(0.80, 1.0 + 0.03 * rng.normal(size=n))
            radius_y = np.maximum(0.80, 1.0 + 0.03 * rng.normal(size=n))
        return signs * radius_x, signs * radius_y
    if scenario == "mantel_null_profile_alt":
        return generate_scenario(rng, scenario, n, aligned_probability)
    raise ValueError(f"unknown stress scenario: {scenario}")


def run_stress(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    seed: int,
    phase: str,
    scenarios: tuple[str, ...] = SCENARIOS,
) -> list[dict[str, float | int | str]]:
    calibration = calibrate_mantel_partial_mixture(seed=seed + 100, draws=150_000)
    aligned_probability = calibration["aligned_probability"]
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios:
        profile_true = scenario != "mantel_null_profile_alt"
        mantel_true = scenario in {
            "independent_t5",
            "independent_t3_infinite_fourth",
            "independent_strong_skew",
            "mantel_null_profile_alt",
        }
        records = []
        failures = 0
        for _ in range(repetitions):
            x, y = generate_stress_scenario(
                rng, scenario, n, float(aligned_probability)
            )
            indices = random_indices(rng, n, n_perm)
            try:
                profile = profile_studentized_permutation_test(x, y, indices)
                mantel = mantel_studentized_permutation_test(x, y, indices)
            except (FloatingPointError, ValueError):
                failures += 1
                continue
            adjusted_profile, adjusted_mantel = holm_adjust(
                float(profile["p_value"]), float(mantel["p_value"])
            )
            records.append(
                (
                    float(profile["estimate"]),
                    float(profile["p_value"]),
                    float(mantel["estimate"]),
                    float(mantel["p_value"]),
                    adjusted_profile,
                    adjusted_mantel,
                )
            )
        values = np.asarray(records)
        valid = values.shape[0]
        if valid == 0:
            raise RuntimeError(f"all {scenario} stress datasets failed")
        true_holm = np.zeros(valid, dtype=bool)
        if profile_true:
            true_holm |= values[:, 4] <= 0.05
        if mantel_true:
            true_holm |= values[:, 5] <= 0.05
        count = int(np.sum(true_holm))
        interval = wilson(count, valid)
        rows.append(
            {
                "phase": phase,
                "scenario": scenario,
                "n": n,
                "repetitions": repetitions,
                "valid_repetitions": valid,
                "failure_rate": failures / repetitions,
                "n_perm": n_perm,
                "profile_null_true": int(profile_true),
                "mantel_null_true": int(mantel_true),
                "mean_profile_effect": float(np.mean(values[:, 0])),
                "profile_local_rejection": float(np.mean(values[:, 1] <= 0.05)),
                "profile_holm_rejection": float(np.mean(values[:, 4] <= 0.05)),
                "mean_mantel_effect": float(np.mean(values[:, 2])),
                "mantel_local_rejection": float(np.mean(values[:, 3] <= 0.05)),
                "mantel_holm_rejection": float(np.mean(values[:, 5] <= 0.05)),
                "holm_true_null_fwer": count / valid,
                "holm_fwer_wilson_low": interval[0],
                "holm_fwer_wilson_high": interval[1],
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "pilot"), default="smoke")
    parser.add_argument("--scenario", choices=("all", *SCENARIOS), default="all")
    args = parser.parse_args()
    if args.phase == "smoke":
        settings = dict(repetitions=20, n=60, n_perm=49, seed=2026081451)
    else:
        settings = dict(repetitions=300, n=80, n_perm=199, seed=2026081452)
    scenarios = SCENARIOS if args.scenario == "all" else (args.scenario,)
    rows = run_stress(phase=args.phase, scenarios=scenarios, **settings)
    RESULTS_DIR.mkdir(exist_ok=True)
    suffix = args.phase if args.scenario == "all" else f"{args.phase}_{args.scenario}"
    output = RESULTS_DIR / f"studentized_permutation_stress_{suffix}_20260814.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
