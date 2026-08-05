"""Validate robust c_delta on tied, discrete, and degenerate margins."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "huber_primary": lambda z: huber_reference_profile(z),
    "huber_cap6": lambda z: huber_reference_profile(z, cap=6.0),
}


FAMILY_ROLES = {
    "null_bernoulli_50": "null",
    "null_bernoulli_20": "null",
    "null_ordinal3": "null",
    "null_poisson_05": "null",
    "null_poisson_2": "null",
    "null_zero_inflated_80": "null",
    "null_quantized_normal": "null",
    "null_near_constant_1e12": "null",
    "degenerate_constant_x": "degenerate",
    "alternative_shared_rare_binary": "alternative",
    "alternative_shared_ordinal": "alternative",
    "alternative_shared_zero_pattern": "alternative",
}


def _zero_inflated(
    rng: np.random.Generator, n: int, zero_probability: float
) -> np.ndarray:
    active = rng.random(n) >= zero_probability
    return active * rng.normal(2.0, 0.5, n)


def make_boundary_pair(
    rng: np.random.Generator, n: int, family: str
) -> tuple[np.ndarray, np.ndarray]:
    if family == "null_bernoulli_50":
        return rng.binomial(1, 0.5, n), rng.binomial(1, 0.5, n)
    if family == "null_bernoulli_20":
        return rng.binomial(1, 0.2, n), rng.binomial(1, 0.2, n)
    if family == "null_ordinal3":
        return (
            rng.choice(3, n, p=(0.6, 0.3, 0.1)),
            rng.choice(3, n, p=(0.6, 0.3, 0.1)),
        )
    if family == "null_poisson_05":
        return rng.poisson(0.5, n), rng.poisson(0.5, n)
    if family == "null_poisson_2":
        return rng.poisson(2.0, n), rng.poisson(2.0, n)
    if family == "null_zero_inflated_80":
        return _zero_inflated(rng, n, 0.8), _zero_inflated(rng, n, 0.8)
    if family == "null_quantized_normal":
        return np.round(rng.normal(size=n)), np.round(rng.normal(size=n))
    if family == "null_near_constant_1e12":
        return 3.0 + 1e-12 * rng.normal(size=n), -2.0 + 1e-12 * rng.normal(size=n)
    if family == "degenerate_constant_x":
        return np.full(n, 3.0), rng.normal(size=n)
    if family == "alternative_shared_rare_binary":
        x = rng.binomial(1, 0.12, n)
        return x, x.copy()
    if family == "alternative_shared_ordinal":
        x = rng.choice(3, n, p=(0.6, 0.3, 0.1))
        y = x.copy()
        replace = rng.random(n) < 0.25
        y[replace] = rng.choice(3, int(np.sum(replace)), p=(0.6, 0.3, 0.1))
        return x, y
    if family == "alternative_shared_zero_pattern":
        active = rng.random(n) >= 0.8
        x = active * rng.normal(2.0, 0.5, n)
        y = active * rng.normal(2.0, 0.5, n)
        return x, y
    raise ValueError(family)


def run(
    *, repetitions: int = 1500, n_perm: int = 499, seed: int = 20260904
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (20, 40, 80):
        for family, role in FAMILY_ROLES.items():
            summaries = {
                method: {
                    "reject": 0,
                    "determined": 0,
                    "constant": 0,
                    "p_values": [],
                }
                for method in METHODS
            }
            for _ in range(repetitions):
                x, y = make_boundary_pair(rng, n, family)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                for method, profile in METHODS.items():
                    sx, sy = profile(x), profile(y)
                    mean_x, mean_y = float(sx.mean()), float(sy.mean())
                    cell = summaries[method]
                    if mean_x == 0.0 or mean_y == 0.0:
                        continue
                    cell["determined"] += 1
                    cell["constant"] += int(sx.std() == 0.0 or sy.std() == 0.0)
                    denominator = mean_x * mean_y
                    observed = float(np.mean(sx * sy) / denominator)
                    statistics = (sy[indices] @ sx) / n / denominator
                    p_value = (int(np.sum(statistics >= observed)) + 1) / (
                        n_perm + 1
                    )
                    cell["p_values"].append(p_value)
                    cell["reject"] += int(p_value < 0.05)
            for method, values in summaries.items():
                reject = int(values["reject"])
                low, high = wilson(reject, repetitions)
                determined = int(values["determined"])
                rows.append(
                    {
                        "family": family,
                        "family_role": role,
                        "n": n,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate_all": reject / repetitions,
                        "wilson_low_all": low,
                        "wilson_high_all": high,
                        "determined_rate": determined / repetitions,
                        "constant_profile_rate": int(values["constant"])
                        / repetitions,
                        "mean_p_value_determined": (
                            float(np.mean(values["p_values"]))
                            if values["p_values"]
                            else np.nan
                        ),
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "discrete_degeneracy_validation_20260805.tsv",
        run(),
    )
