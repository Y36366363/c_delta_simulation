"""Targeted audit of the theorem-aligned iid Wald inference track.

The frozen 2026-08-19 panels use fully recomputed studentized permutation.
This script deliberately studies a different object: the plug-in influence-
function Wald test proved in Appendix Theorem A.1/Corollary A.1.  Regular
models satisfy the stated marginal identification conditions; separated-mode
models are included only as out-of-regularity comparators.
"""

from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_regularity_comparison_20260816 import (
    generate_sign_link_profile_null,
)
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


RESULTS_DIR = PROJECT_ROOT / "results"
REGULAR_SCENARIOS = (
    "independent_t5",
    "independent_strong_skew",
    "profile_null_normal_sign_link",
)


def generate_regular_scenario(
    rng: np.random.Generator, scenario: str, n: int
) -> tuple[np.ndarray, np.ndarray]:
    """Generate rho_P=0 laws with regular continuous marginal references."""
    if scenario == "independent_t5":
        return rng.standard_t(5.0, n), rng.standard_t(5.0, n)
    if scenario == "independent_strong_skew":
        return np.exp(1.1 * rng.normal(size=n)), rng.gamma(0.7, 1.0, size=n)
    if scenario == "profile_null_normal_sign_link":
        # Margins are standard normal, hence have positive centre density and
        # unique regular median/MAD/Huber references.  The shared sign creates
        # dependence while the two absolute radii remain independent.
        signs = rng.choice((-1.0, 1.0), size=n)
        return signs * np.abs(rng.normal(size=n)), signs * np.abs(rng.normal(size=n))
    raise ValueError(f"unknown regular scenario: {scenario}")


def _cell_seed(root_seed: int, scenario_index: int, n: int) -> int:
    return root_seed + 100_000 * scenario_index + n


def audit_cell(
    *,
    scenario: str,
    n: int,
    repetitions: int,
    seed: int,
    regularity_class: str,
    radial_log_sd: float | None = None,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    estimates: list[float] = []
    standard_errors: list[float] = []
    z_statistics: list[float] = []
    rejections = 0
    failures = 0
    for _ in range(repetitions):
        if radial_log_sd is None:
            x, y = generate_regular_scenario(rng, scenario, n)
        else:
            x, y = generate_sign_link_profile_null(rng, n, radial_log_sd)
        try:
            result = profile_weak_null_test(x, y)
        except (FloatingPointError, ValueError, np.linalg.LinAlgError):
            failures += 1
            continue
        estimates.append(float(result["estimate"]))
        standard_errors.append(float(result["standard_error"]))
        z_statistics.append(float(result["z_statistic"]))
        rejections += int(float(result["p_value"]) <= 0.05)

    valid = len(z_statistics)
    if valid == 0:
        raise RuntimeError(f"all fits failed for {scenario}, n={n}")
    rejection_rate = rejections / valid
    low, high = wilson(rejections, valid)
    z = np.asarray(z_statistics)
    return {
        "inference_track": "iid_full_if_wald",
        "scenario": scenario,
        "regularity_class": regularity_class,
        "n": n,
        "repetitions": repetitions,
        "valid_repetitions": valid,
        "failures": failures,
        "failure_rate": failures / repetitions,
        "root_cell_seed": seed,
        "radial_log_sd": "" if radial_log_sd is None else radial_log_sd,
        "mean_estimate": float(np.mean(estimates)),
        "mean_standard_error": float(np.mean(standard_errors)),
        "mean_z": float(np.mean(z)),
        "sd_z": float(np.std(z, ddof=1)),
        "rejections": rejections,
        "rejection_rate": rejection_rate,
        "monte_carlo_se": sqrt(rejection_rate * (1.0 - rejection_rate) / valid),
        "wilson_95_low": low,
        "wilson_95_high": high,
    }


def run_audit(
    *, repetitions: int, sample_sizes: tuple[int, ...], root_seed: int
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for scenario_index, scenario in enumerate(REGULAR_SCENARIOS, start=1):
        for n in sample_sizes:
            rows.append(
                audit_cell(
                    scenario=scenario,
                    n=n,
                    repetitions=repetitions,
                    seed=_cell_seed(root_seed, scenario_index, n),
                    regularity_class="inside_appendix_conditions",
                )
            )
    # Two separated-mode paths document that the Wald theorem is not a rescue
    # outside its identification assumptions.  They are diagnostics, not part
    # of the regular convergence claim.
    for scenario_index, radial_log_sd in enumerate((0.10, 0.40), start=10):
        for n in (sample_sizes[0], sample_sizes[-1]):
            rows.append(
                audit_cell(
                    scenario=f"separated_mode_sd_{radial_log_sd:g}",
                    n=n,
                    repetitions=repetitions,
                    seed=_cell_seed(root_seed, scenario_index, n),
                    regularity_class="outside_positive_center_density_condition",
                    radial_log_sd=radial_log_sd,
                )
            )
    # The skew model is deliberately extended beyond the main n-grid because
    # its unbounded profiles produce visibly slow second-order convergence.
    for n in (1280, 2560):
        if n > sample_sizes[-1] and repetitions >= 100:
            rows.append(
                audit_cell(
                    scenario="independent_strong_skew",
                    n=n,
                    repetitions=repetitions,
                    seed=_cell_seed(root_seed, 2, n),
                    regularity_class="inside_appendix_conditions_slow_convergence_extension",
                )
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "audit"), default="smoke")
    args = parser.parse_args()
    if args.phase == "smoke":
        repetitions, sample_sizes = 20, (80, 160)
    else:
        repetitions, sample_sizes = 600, (80, 160, 320, 640)
    rows = run_audit(
        repetitions=repetitions,
        sample_sizes=sample_sizes,
        root_seed=2026082201,
    )
    RESULTS_DIR.mkdir(exist_ok=True)
    output = RESULTS_DIR / f"wald_convergence_{args.phase}_20260822.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
