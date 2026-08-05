"""Coverage pilot for Huber c_delta under an analytic population target."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_cdelta_bootstrap_intervals
from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson


INTERVAL_METHODS = ("percentile", "basic", "bca", "normal")


def analytic_pair(
    rng: np.random.Generator,
    n: int,
    latent_correlation: float,
    log_scale: float = 0.45,
) -> tuple[np.ndarray, np.ndarray]:
    u = rng.normal(size=n)
    v = latent_correlation * u + np.sqrt(1.0 - latent_correlation**2) * rng.normal(
        size=n
    )
    x = rng.choice((-1.0, 1.0), n) * np.exp(log_scale * u)
    y = rng.choice((-1.0, 1.0), n) * np.exp(log_scale * v)
    return x, y


def population_cdelta(
    latent_correlation: float, log_scale: float = 0.45
) -> float:
    """Population c_delta for symmetric correlated lognormal magnitudes."""
    return float(np.exp(log_scale**2 * latent_correlation))


def run(
    *,
    repetitions: int = 300,
    n_boot: int = 399,
    seed: int = 20260909,
    sample_sizes: tuple[int, ...] = (20, 40, 80, 160),
    latent_correlations: tuple[float, ...] = (0.0, 0.2, 0.5),
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for latent_correlation in latent_correlations:
            truth = population_cdelta(latent_correlation)
            summaries = {
                method: {"cover": 0, "width": [], "estimates": [], "fail": 0}
                for method in INTERVAL_METHODS
            }
            for _ in range(repetitions):
                x, y = analytic_pair(rng, n, latent_correlation)
                try:
                    intervals = huber_cdelta_bootstrap_intervals(
                        x,
                        y,
                        n_boot=n_boot,
                        seed=int(rng.integers(0, 2**32 - 1)),
                    )
                except ValueError:
                    for method in INTERVAL_METHODS:
                        summaries[method]["fail"] += 1
                    continue
                estimate = float(intervals["estimate"])
                for method in INTERVAL_METHODS:
                    lower = float(intervals[method]["lower"])
                    upper = float(intervals[method]["upper"])
                    cell = summaries[method]
                    cell["cover"] += int(lower <= truth <= upper)
                    cell["width"].append(upper - lower)
                    cell["estimates"].append(estimate)
            for method, values in summaries.items():
                used = repetitions - int(values["fail"])
                cover = int(values["cover"])
                low, high = wilson(cover, used)
                rows.append(
                    {
                        "n": n,
                        "latent_correlation": latent_correlation,
                        "population_cdelta": truth,
                        "interval_method": method,
                        "repetitions": repetitions,
                        "n_boot": n_boot,
                        "successful_rate": used / repetitions,
                        "coverage_rate": cover / used,
                        "coverage_wilson_low": low,
                        "coverage_wilson_high": high,
                        "mean_width": float(np.mean(values["width"])),
                        "mean_estimate_bias": float(
                            np.mean(values["estimates"]) - truth
                        ),
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "huber_bootstrap_coverage_20260805.tsv",
        run(),
    )
