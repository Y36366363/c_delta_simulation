"""Broad comparison of original and robust c_delta profile definitions."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import wilson


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "original_l1": lambda z: divergence_vector(z, kind="l1"),
    "huber_primary": lambda z: huber_reference_profile(z, huber_c=1.345),
    "huber_cap6": lambda z: huber_reference_profile(z, huber_c=1.345, cap=6.0),
}


SCENARIO_ROLES = {
    "null_normal": "exchangeable_null",
    "null_t3": "exchangeable_null",
    "null_t2": "exchangeable_null",
    "null_lognormal": "exchangeable_null",
    "null_bimodal_independent": "exchangeable_null",
    "null_contam5_m20": "exchangeable_null",
    "sparse_matched_1_m8": "core_alternative",
    "sparse_matched_5_m6": "core_alternative",
    "partial_overlap_5_half_m8": "partial_alternative",
    "diffuse_low_noise": "core_alternative",
    "diffuse_high_noise": "core_alternative",
    "t2_matched_5_m8": "core_alternative",
    "lognormal_shared": "core_alternative",
    "bimodal_balanced_shared": "core_alternative",
    "bimodal_unequal_shared": "core_alternative",
    "unmatched_masking": "contaminated_alternative",
    "reverse_salience": "directional_diagnostic",
    "nonexchangeable_shared_scale": "design_violation_diagnostic",
}


def _standardise(z: np.ndarray) -> np.ndarray:
    return (z - float(z.mean())) / float(z.std())


def make_scenario(
    name: str, n: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    if name == "null_normal":
        return rng.normal(size=n), rng.normal(size=n)
    if name == "null_t3":
        return rng.standard_t(3, n), rng.standard_t(3, n)
    if name == "null_t2":
        return rng.standard_t(2, n), rng.standard_t(2, n)
    if name == "null_lognormal":
        return (
            _standardise(rng.lognormal(0.0, 0.8, n)),
            _standardise(rng.lognormal(0.0, 0.8, n)),
        )
    if name == "null_bimodal_independent":
        lx = rng.choice((-1.0, 1.0), size=n)
        ly = rng.choice((-1.0, 1.0), size=n)
        return 3.0 * lx + rng.normal(0, 0.5, n), 4.0 * ly + rng.normal(0, 0.5, n)
    if name == "null_contam5_m20":
        x, y = rng.normal(size=n), rng.normal(size=n)
        k = max(1, round(0.05 * n))
        x[rng.choice(n, k, replace=False)] += 20.0
        y[rng.choice(n, k, replace=False)] += 20.0
        return x, y
    if name in {"sparse_matched_1_m8", "sparse_matched_5_m6"}:
        fraction, magnitude = ((0.01, 8.0) if "_1_" in name else (0.05, 6.0))
        x, y = rng.normal(size=n), rng.normal(size=n)
        indices = rng.choice(n, max(1, round(fraction * n)), replace=False)
        x[indices] += magnitude
        y[indices] += magnitude
        return x, y
    if name == "partial_overlap_5_half_m8":
        x, y = rng.normal(size=n), rng.normal(size=n)
        k = max(2, round(0.05 * n))
        overlap = max(1, k // 2)
        shared = rng.choice(n, overlap, replace=False)
        remaining = np.setdiff1d(np.arange(n), shared)
        x_only = rng.choice(remaining, k - overlap, replace=False)
        remaining = np.setdiff1d(remaining, x_only)
        y_only = rng.choice(remaining, k - overlap, replace=False)
        x[np.concatenate((shared, x_only))] += 8.0
        y[np.concatenate((shared, y_only))] += 8.0
        return x, y
    if name in {"diffuse_low_noise", "diffuse_high_noise", "reverse_salience"}:
        magnitude = rng.uniform(0.7, 1.8, size=n)
        x = rng.choice((-1.0, 1.0), size=n) * magnitude
        if name == "reverse_salience":
            y_magnitude = np.maximum(0.05, 2.5 - magnitude + rng.normal(0, 0.15, n))
        else:
            noise = 0.15 if name == "diffuse_low_noise" else 0.50
            y_magnitude = np.maximum(0.05, magnitude + rng.normal(0, noise, n))
        y = rng.choice((-1.0, 1.0), size=n) * y_magnitude
        return x, y
    if name == "t2_matched_5_m8":
        x, y = rng.standard_t(2, n), rng.standard_t(2, n)
        indices = rng.choice(n, max(1, round(0.05 * n)), replace=False)
        x[indices] += 8.0
        y[indices] += 8.0
        return x, y
    if name == "lognormal_shared":
        latent = rng.lognormal(0.0, 0.8, n)
        return _standardise(latent), _standardise(latent + rng.normal(0, 0.25, n))
    if name in {"bimodal_balanced_shared", "bimodal_unequal_shared"}:
        probability = 0.50 if name == "bimodal_balanced_shared" else 0.20
        labels = np.where(rng.random(n) < probability, 1.0, -1.0)
        return (
            3.0 * labels + rng.normal(0, 0.45, n),
            4.0 * labels + rng.normal(0, 0.45, n),
        )
    if name == "unmatched_masking":
        x, y = rng.standard_t(3, n), rng.standard_t(3, n)
        indices = rng.choice(n, max(4, round(0.05 * n)), replace=False)
        x[indices[:2]] += 6.0
        y[indices[:2]] += 6.0
        x[indices[2]] += 20.0
        y[indices[3]] += 20.0
        return x, y
    if name == "nonexchangeable_shared_scale":
        scales = np.ones(n)
        scales[: n // 3] = 3.0
        rng.shuffle(scales)
        return rng.normal(size=n) * scales, rng.normal(size=n) * scales
    raise ValueError(f"unknown scenario: {name}")


def run(
    *, repetitions: int = 1500, n_perm: int = 499, seed: int = 20260826
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (20, 40, 80, 160):
        for scenario, role in SCENARIO_ROLES.items():
            summary = {
                method: {"reject": 0, "corr": []} for method in METHODS
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(
                    {method: fn(x) for method, fn in METHODS.items()},
                    {method: fn(y) for method, fn in METHODS.items()},
                    indices,
                )
                for method, (p_value, _, correlation) in outcomes.items():
                    summary[method]["reject"] += int(p_value < 0.05)
                    summary[method]["corr"].append(correlation)
            for method, values in summary.items():
                reject = int(values["reject"])
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "scenario": scenario,
                        "scenario_role": role,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                        "mean_profile_correlation": float(np.mean(values["corr"])),
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "comprehensive_scope_benchmark_20260805.tsv",
        run(),
    )
