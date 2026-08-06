"""Compare density estimators and HC-style sandwich corrections."""

from __future__ import annotations

from pathlib import Path
from statistics import NormalDist
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_cdelta_influence_inference
from scripts.robust_extension_utils import write_tsv
from scripts.run_population_skew_influence_validation import (
    _lognormal_pdf,
    population_truth,
)
from scripts.run_robust_cdelta_grid import wilson


METHODS = (
    "oracle",
    "kde_hc0",
    "kde_sample",
    "kde_hc1",
    "kde_hc3",
    "crossfit_sample",
    "analytic_sample",
    "analytic_hc1",
)


def run(
    *,
    repetitions: int = 2500,
    seed: int = 20260921,
    sample_sizes: tuple[int, ...] = (40, 80, 160),
    sigma: float = 0.60,
    rho: float = 0.40,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    truth = population_truth(sigma=sigma, rho=rho)
    target = truth["c_delta"]
    z = NormalDist().inv_cdf(0.975)
    analytic_density = lambda value: _lognormal_pdf(value, sigma)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        summaries = {
            method: {"cover": 0, "se": [], "estimate": [], "width": []}
            for method in METHODS
        }
        oracle_se = float(np.sqrt(truth["influence_variance"] / n))
        for repetition in range(repetitions):
            u = rng.normal(size=n)
            v = rho * u + np.sqrt(1.0 - rho**2) * rng.normal(size=n)
            x, y = np.exp(sigma * u), np.exp(sigma * v)
            fits = {
                "kde_hc0": huber_cdelta_influence_inference(
                    x, y, small_sample_correction="hc0"
                ),
                "kde_sample": huber_cdelta_influence_inference(
                    x, y, small_sample_correction="sample"
                ),
                "kde_hc1": huber_cdelta_influence_inference(
                    x, y, small_sample_correction="hc1"
                ),
                "kde_hc3": huber_cdelta_influence_inference(
                    x, y, small_sample_correction="hc3"
                ),
                "crossfit_sample": huber_cdelta_influence_inference(
                    x,
                    y,
                    density_method="crossfit_kde",
                    density_seed=seed + repetition,
                    small_sample_correction="sample",
                ),
                "analytic_sample": huber_cdelta_influence_inference(
                    x,
                    y,
                    density_method="analytic",
                    analytic_density_x=analytic_density,
                    analytic_density_y=analytic_density,
                    small_sample_correction="sample",
                ),
                "analytic_hc1": huber_cdelta_influence_inference(
                    x,
                    y,
                    density_method="analytic",
                    analytic_density_x=analytic_density,
                    analytic_density_y=analytic_density,
                    small_sample_correction="hc1",
                ),
            }
            estimate = float(fits["kde_sample"]["estimate"])
            specifications = {"oracle": oracle_se}
            specifications.update(
                {method: float(fitted["standard_error"]) for method, fitted in fits.items()}
            )
            for method, standard_error in specifications.items():
                log_se = standard_error / estimate
                lower = float(np.exp(np.log(estimate) - z * log_se))
                upper = float(np.exp(np.log(estimate) + z * log_se))
                cell = summaries[method]
                cell["cover"] += int(lower <= target <= upper)
                cell["se"].append(standard_error)
                cell["estimate"].append(estimate)
                cell["width"].append(upper - lower)
        empirical_sd = float(np.std(summaries["oracle"]["estimate"], ddof=1))
        for method, summary in summaries.items():
            coverage = int(summary["cover"])
            lower, upper = wilson(coverage, repetitions)
            mean_se = float(np.mean(summary["se"]))
            rows.append(
                {
                    "n": n,
                    "sigma": sigma,
                    "latent_correlation": rho,
                    "population_cdelta": target,
                    "method": method,
                    "repetitions": repetitions,
                    "coverage_rate": coverage / repetitions,
                    "coverage_wilson_low": lower,
                    "coverage_wilson_high": upper,
                    "mean_standard_error": mean_se,
                    "empirical_estimate_sd": empirical_sd,
                    "se_over_empirical_sd": mean_se / empirical_sd,
                    "mean_interval_width": float(np.mean(summary["width"])),
                    "mean_estimate_bias": float(
                        np.mean(summary["estimate"]) - target
                    ),
                }
            )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "density_hc_studentization_20260806.tsv",
        run(),
    )
