"""Expanded boundary map for diffuse paired-salience alternatives."""

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
    "huber_primary": lambda z: huber_reference_profile(z),
    "huber_cap6": lambda z: huber_reference_profile(z, cap=6.0),
}


def _magnitudes(
    rng: np.random.Generator, n: int, family: str
) -> np.ndarray:
    if family == "uniform":
        return rng.uniform(0.7, 1.8, n)
    if family == "lognormal":
        values = rng.lognormal(0.0, 0.35, n)
        return values / float(np.mean(values)) * 1.25
    raise ValueError(family)


def make_diffuse(
    rng: np.random.Generator,
    n: int,
    noise: float,
    positive_probability: float,
    contamination_fraction: float,
    magnitude_family: str,
) -> tuple[np.ndarray, np.ndarray]:
    magnitude = _magnitudes(rng, n, magnitude_family)
    x_sign = np.where(rng.random(n) < positive_probability, 1.0, -1.0)
    y_sign = np.where(rng.random(n) < positive_probability, 1.0, -1.0)
    x = x_sign * magnitude
    y_magnitude = np.maximum(0.05, magnitude + rng.normal(0.0, noise, n))
    y = y_sign * y_magnitude
    if contamination_fraction > 0.0:
        k = max(1, round(contamination_fraction * n))
        x[rng.choice(n, k, replace=False)] += 20.0
        y[rng.choice(n, k, replace=False)] += 20.0
    return x, y


def run(
    *, repetitions: int = 1500, n_perm: int = 499, seed: int = 20260828
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (12, 20, 40, 80, 160):
        for noise in (0.15, 0.50):
            for positive_probability in (0.50, 0.65):
                for contamination_fraction in (0.0, 0.05):
                    for magnitude_family in ("uniform", "lognormal"):
                        counts = {method: 0 for method in METHODS}
                        for _ in range(repetitions):
                            x, y = make_diffuse(
                                rng,
                                n,
                                noise,
                                positive_probability,
                                contamination_fraction,
                                magnitude_family,
                            )
                            indices = np.asarray(
                                [rng.permutation(n) for _ in range(n_perm)]
                            )
                            outcomes = common_permutation_pvalues(
                                {method: fn(x) for method, fn in METHODS.items()},
                                {method: fn(y) for method, fn in METHODS.items()},
                                indices,
                            )
                            for method, (p_value, _, _) in outcomes.items():
                                counts[method] += int(p_value < 0.05)
                        for method, reject in counts.items():
                            low, high = wilson(reject, repetitions)
                            rows.append(
                                {
                                    "n": n,
                                    "noise": noise,
                                    "positive_probability": positive_probability,
                                    "contamination_fraction": contamination_fraction,
                                    "magnitude_family": magnitude_family,
                                    "method": method,
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
        PROJECT_ROOT / "results" / "diffuse_boundary_expansion_20260805.tsv",
        run(),
    )
