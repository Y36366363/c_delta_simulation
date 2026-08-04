"""Small-sample diffuse-power and dual-report decision-rule pilot."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import make_scenario, wilson


def diffuse_scenario(
    n: int, noise: float, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    magnitude = rng.uniform(0.7, 1.8, size=n)
    x = rng.choice((-1.0, 1.0), size=n) * magnitude
    y_magnitude = np.maximum(0.05, magnitude + rng.normal(0.0, noise, size=n))
    y = rng.choice((-1.0, 1.0), size=n) * y_magnitude
    return x, y


def diffuse_power(
    *, repetitions: int = 2500, n_perm: int = 499, seed: int = 20260815
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (12, 20, 30, 40, 60, 80):
        for noise in (0.15, 0.30, 0.50):
            summary = {"original_l2": 0, "huber_radius": 0}
            for _ in range(repetitions):
                x, y = diffuse_scenario(n, noise, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(
                    {
                        "original_l2": divergence_vector(x, kind="l2"),
                        "huber_radius": huber_reference_profile(x),
                    },
                    {
                        "original_l2": divergence_vector(y, kind="l2"),
                        "huber_radius": huber_reference_profile(y),
                    },
                    indices,
                )
                for method, (p_value, _, _) in outcomes.items():
                    summary[method] += int(p_value < 0.05)
            for method, reject in summary.items():
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "noise": noise,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
    return rows


def decision_rules(
    *, repetitions: int = 4000, n_perm: int = 999, seed: int = 20260816
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    scenarios = (
        "null_clean",
        "null_contam_p10",
        "matched_p01_m8",
        "t2_matched",
        "bimodal_aligned",
        "unmatched_masking",
    )
    rows: list[dict[str, float | int | str]] = []
    for n in (40, 80):
        for scenario in scenarios:
            counts = {
                "primary_only": 0,
                "cap6_only": 0,
                "unadjusted_union": 0,
                "bonferroni_union": 0,
                "intersection": 0,
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(
                    {
                        "primary": huber_reference_profile(x),
                        "cap6": huber_reference_profile(x, cap=6.0),
                    },
                    {
                        "primary": huber_reference_profile(y),
                        "cap6": huber_reference_profile(y, cap=6.0),
                    },
                    indices,
                )
                p_primary, p_cap = outcomes["primary"][0], outcomes["cap6"][0]
                counts["primary_only"] += int(p_primary < 0.05)
                counts["cap6_only"] += int(p_cap < 0.05)
                counts["unadjusted_union"] += int(p_primary < 0.05 or p_cap < 0.05)
                counts["bonferroni_union"] += int(p_primary < 0.025 or p_cap < 0.025)
                counts["intersection"] += int(p_primary < 0.05 and p_cap < 0.05)
            for rule, reject in counts.items():
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "scenario": scenario,
                        "rule": rule,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "diffuse_small_sample_power_20260804.tsv",
        diffuse_power(),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "dual_rule_pilot_20260804.tsv",
        decision_rules(),
    )
