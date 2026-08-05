"""Map local diffuse-salience power and effect stability by sample size."""

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
    "huber_primary": lambda z: huber_reference_profile(z),
    "huber_cap6": lambda z: huber_reference_profile(z, cap=6.0),
}


def make_local_salience_pair(
    rng: np.random.Generator,
    n: int,
    latent_correlation: float,
    contamination_fraction: float,
) -> tuple[np.ndarray, np.ndarray]:
    u = rng.normal(size=n)
    v = latent_correlation * u + np.sqrt(1.0 - latent_correlation**2) * rng.normal(
        size=n
    )
    x_magnitude = np.exp(0.45 * u)
    y_magnitude = np.exp(0.45 * v)
    x = rng.choice((-1.0, 1.0), n) * x_magnitude
    y = rng.choice((-1.0, 1.0), n) * y_magnitude
    if contamination_fraction > 0.0:
        k = max(1, round(contamination_fraction * n))
        x[rng.choice(n, k, replace=False)] += 20.0
        y[rng.choice(n, k, replace=False)] += 20.0
    return x, y


def run(
    *, repetitions: int = 1200, n_perm: int = 499, seed: int = 20260905
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (20, 40, 80, 160, 320):
        for latent_correlation in (0.0, 0.1, 0.2, 0.3, 0.5, 0.7):
            for contamination_fraction in (0.0, 0.05):
                summaries = {
                    method: {"reject": 0, "raw": [], "correlation": []}
                    for method in METHODS
                }
                for _ in range(repetitions):
                    x, y = make_local_salience_pair(
                        rng, n, latent_correlation, contamination_fraction
                    )
                    indices = np.asarray(
                        [rng.permutation(n) for _ in range(n_perm)]
                    )
                    outcomes = common_permutation_pvalues(
                        {method: fn(x) for method, fn in METHODS.items()},
                        {method: fn(y) for method, fn in METHODS.items()},
                        indices,
                    )
                    for method, (p_value, raw, correlation) in outcomes.items():
                        summaries[method]["reject"] += int(p_value < 0.05)
                        summaries[method]["raw"].append(raw)
                        summaries[method]["correlation"].append(correlation)
                for method, values in summaries.items():
                    reject = int(values["reject"])
                    low, high = wilson(reject, repetitions)
                    rows.append(
                        {
                            "n": n,
                            "latent_correlation": latent_correlation,
                            "contamination_fraction": contamination_fraction,
                            "method": method,
                            "repetitions": repetitions,
                            "n_perm": n_perm,
                            "rejection_rate": reject / repetitions,
                            "wilson_low": low,
                            "wilson_high": high,
                            "mean_cdelta_minus_one": float(
                                np.mean(values["raw"]) - 1.0
                            ),
                            "mean_profile_correlation": float(
                                np.mean(values["correlation"])
                            ),
                        }
                    )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "local_salience_power_20260805.tsv",
        run(),
    )
