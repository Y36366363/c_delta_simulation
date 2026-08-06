"""Focused coverage test for complete-influence bootstrap-t intervals."""

from __future__ import annotations

from pathlib import Path
from statistics import NormalDist
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    huber_cdelta_bootstrap_t_interval,
    huber_cdelta_influence_inference,
    symmetric_lognormal_cdelta_moments,
)
from scripts.robust_extension_utils import write_tsv
from scripts.run_huber_bootstrap_coverage import analytic_pair
from scripts.run_population_skew_influence_validation import population_truth
from scripts.run_robust_cdelta_grid import wilson


METHODS = ("sandwich_log", "hc3_log", "bootstrap_t_normal", "bootstrap_t_log")


def run(
    *,
    repetitions: int = 600,
    n_boot: int = 99,
    seed: int = 20260922,
    sample_sizes: tuple[int, ...] = (80, 160),
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    z = NormalDist().inv_cdf(0.975)
    rows: list[dict[str, float | int | str]] = []
    skew_truth = population_truth(sigma=0.60, rho=0.40)["c_delta"]
    for scenario in ("symmetric", "skew"):
        truth = (
            symmetric_lognormal_cdelta_moments(0.50)["c_delta"]
            if scenario == "symmetric"
            else skew_truth
        )
        for n in sample_sizes:
            summaries = {
                method: {"cover": 0, "width": [], "valid": 0}
                for method in METHODS
            }
            for repetition in range(repetitions):
                if scenario == "symmetric":
                    x, y = analytic_pair(rng, n, 0.50)
                else:
                    u = rng.normal(size=n)
                    v = 0.40 * u + np.sqrt(1.0 - 0.40**2) * rng.normal(size=n)
                    x, y = np.exp(0.60 * u), np.exp(0.60 * v)
                ordinary = huber_cdelta_influence_inference(x, y)
                hc3 = huber_cdelta_influence_inference(
                    x, y, small_sample_correction="hc3"
                )
                bootstrap = huber_cdelta_bootstrap_t_interval(
                    x,
                    y,
                    n_boot=n_boot,
                    seed=seed + repetition + 10_000 * n + (scenario == "skew"),
                )
                estimate = float(ordinary["estimate"])
                interval_map = {
                    "sandwich_log": (
                        float(np.exp(np.log(estimate) - z * float(ordinary["standard_error"]) / estimate)),
                        float(np.exp(np.log(estimate) + z * float(ordinary["standard_error"]) / estimate)),
                    ),
                    "hc3_log": (
                        float(np.exp(np.log(estimate) - z * float(hc3["standard_error"]) / estimate)),
                        float(np.exp(np.log(estimate) + z * float(hc3["standard_error"]) / estimate)),
                    ),
                    "bootstrap_t_normal": (
                        float(bootstrap["normal_scale"]["lower"]),
                        float(bootstrap["normal_scale"]["upper"]),
                    ),
                    "bootstrap_t_log": (
                        float(bootstrap["log_scale"]["lower"]),
                        float(bootstrap["log_scale"]["upper"]),
                    ),
                }
                for method, (lower, upper) in interval_map.items():
                    cell = summaries[method]
                    cell["valid"] += 1
                    cell["cover"] += int(lower <= truth <= upper)
                    cell["width"].append(upper - lower)
            for method, summary in summaries.items():
                valid = int(summary["valid"])
                coverage = int(summary["cover"])
                lower, upper = wilson(coverage, valid)
                rows.append(
                    {
                        "scenario": scenario,
                        "n": n,
                        "population_cdelta": truth,
                        "method": method,
                        "repetitions": repetitions,
                        "valid_repetitions": valid,
                        "bootstrap_repetitions": n_boot,
                        "coverage_rate": coverage / valid,
                        "coverage_wilson_low": lower,
                        "coverage_wilson_high": upper,
                        "mean_interval_width": float(np.mean(summary["width"])),
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "bootstrap_t_validation_20260806.tsv",
        run(),
    )
