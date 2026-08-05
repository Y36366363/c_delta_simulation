"""Validate influence-function and jackknife studentized c_delta intervals."""

from __future__ import annotations

from pathlib import Path
from statistics import NormalDist
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    direct_profile_influence_standard_error,
    huber_cdelta_influence_inference,
    huber_cdelta_jackknife_inference,
    huber_reference_profile,
    symmetric_lognormal_cdelta_moments,
)
from scripts.robust_extension_utils import write_tsv
from scripts.run_huber_bootstrap_coverage import analytic_pair
from scripts.run_robust_cdelta_grid import wilson


METHODS = (
    "oracle_normal",
    "oracle_log",
    "direct_normal",
    "direct_log",
    "sandwich_normal",
    "sandwich_log",
    "jackknife_normal",
    "jackknife_log",
)


def _interval(
    estimate: float, standard_error: float, z: float, log_scale: bool
) -> tuple[float, float]:
    if log_scale:
        log_se = standard_error / estimate
        return (
            float(np.exp(np.log(estimate) - z * log_se)),
            float(np.exp(np.log(estimate) + z * log_se)),
        )
    return estimate - z * standard_error, estimate + z * standard_error


def run(
    *,
    repetitions: int = 1200,
    seed: int = 20260914,
    sample_sizes: tuple[int, ...] = (40, 80, 160),
    latent_correlations: tuple[float, ...] = (0.0, 0.2, 0.5),
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    z = NormalDist().inv_cdf(0.975)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for rho in latent_correlations:
            population = symmetric_lognormal_cdelta_moments(rho)
            truth = population["c_delta"]
            oracle_se = np.sqrt(population["influence_variance"] / n)
            summaries = {
                method: {"cover": 0, "width": [], "se": [], "estimate": []}
                for method in METHODS
            }
            for _ in range(repetitions):
                x, y = analytic_pair(rng, n, rho)
                sx, sy = huber_reference_profile(x), huber_reference_profile(y)
                direct = direct_profile_influence_standard_error(sx, sy)
                sandwich = huber_cdelta_influence_inference(x, y)
                jackknife = huber_cdelta_jackknife_inference(x, y)
                estimate = float(jackknife["estimate"])
                direct_se = float(direct["standard_error"])
                jackknife_se = float(jackknife["standard_error"])
                sandwich_se = float(sandwich["standard_error"])
                method_specs = {
                    "oracle_normal": (oracle_se, False),
                    "oracle_log": (oracle_se * estimate / truth, True),
                    "direct_normal": (direct_se, False),
                    "direct_log": (direct_se, True),
                    "sandwich_normal": (sandwich_se, False),
                    "sandwich_log": (sandwich_se, True),
                    "jackknife_normal": (jackknife_se, False),
                    "jackknife_log": (jackknife_se, True),
                }
                for method, (standard_error, use_log) in method_specs.items():
                    lower, upper = _interval(
                        estimate, standard_error, z, use_log
                    )
                    cell = summaries[method]
                    cell["cover"] += int(lower <= truth <= upper)
                    cell["width"].append(upper - lower)
                    cell["se"].append(
                        oracle_se if method.startswith("oracle") else standard_error
                    )
                    cell["estimate"].append(estimate)
            empirical_sd = float(
                np.std(summaries["jackknife_normal"]["estimate"], ddof=1)
            )
            for method, values in summaries.items():
                cover = int(values["cover"])
                low, high = wilson(cover, repetitions)
                mean_se = float(np.mean(values["se"]))
                rows.append(
                    {
                        "n": n,
                        "latent_correlation": rho,
                        "population_cdelta": truth,
                        "method": method,
                        "repetitions": repetitions,
                        "coverage_rate": cover / repetitions,
                        "coverage_wilson_low": low,
                        "coverage_wilson_high": high,
                        "mean_width": float(np.mean(values["width"])),
                        "mean_standard_error": mean_se,
                        "empirical_estimate_sd": empirical_sd,
                        "se_over_empirical_sd": mean_se / empirical_sd,
                        "mean_estimate_bias": float(
                            np.mean(values["estimate"]) - truth
                        ),
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "studentized_inference_validation_20260805.tsv",
        run(),
    )
