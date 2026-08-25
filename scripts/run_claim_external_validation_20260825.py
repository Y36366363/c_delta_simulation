"""Externalized checks for the three frozen c_delta manuscript claims."""

from __future__ import annotations

import argparse
from math import log, sqrt
from pathlib import Path
import sys

import numpy as np
from scipy.stats import gamma


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_claim_stress_validation_20260824 import _huber_center
from scripts.run_claim_validation_20260823 import (
    _binomial_log_loss,
    _expit,
    fit_binomial_logit,
    fixed_center_profile_test,
    read_tsv,
)
from scripts.run_nuisance_jacobian_20260817 import (
    PopulationDistribution,
    population_nuisance,
    skew_lognormal_distribution,
    symmetric_bridge_distribution,
)
from scripts.run_profile_bridge_family_validation_20260817 import (
    generate_family_bridge_profile_null,
)
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


RESULTS_DIR = PROJECT_ROOT / "results"


def _gamma_distribution() -> PopulationDistribution:
    distribution = gamma(a=0.7, scale=1.0)
    return PopulationDistribution(
        name="gamma_0.7",
        pdf=lambda value: float(distribution.pdf(value)),
        cdf=lambda value: float(distribution.cdf(value)),
        lower=0.0,
        upper=np.inf,
    )


def claim1_oracle_reference_decomposition(
    repetitions: int,
) -> list[dict[str, float | int | str]]:
    """Separate fixed-profile skew from estimated-reference effects."""
    centre_x = float(population_nuisance(skew_lognormal_distribution())["huber_location"])
    centre_y = float(population_nuisance(_gamma_distribution())["huber_location"])
    rows = []
    for n_index, n in enumerate((640, 2560), start=1):
        seed = 2026082501 + 100_000 * n_index + n
        rng = np.random.default_rng(seed)
        records: dict[str, list[float]] = {
            "refitted_estimate": [],
            "refitted_z": [],
            "oracle_estimate": [],
            "oracle_z": [],
        }
        for _ in range(repetitions):
            x = np.exp(1.1 * rng.normal(size=n))
            y = rng.gamma(0.7, 1.0, size=n)
            refitted = profile_weak_null_test(x, y)
            oracle = fixed_center_profile_test(x - centre_x, y - centre_y)
            records["refitted_estimate"].append(float(refitted["estimate"]))
            records["refitted_z"].append(float(refitted["z_statistic"]))
            records["oracle_estimate"].append(float(oracle["estimate"]))
            records["oracle_z"].append(float(oracle["z_statistic"]))
        for reference in ("refitted", "oracle_fixed_population"):
            prefix = "refitted" if reference == "refitted" else "oracle"
            estimates = np.asarray(records[f"{prefix}_estimate"])
            z = np.asarray(records[f"{prefix}_z"])
            count = int(np.sum(np.abs(z) >= 1.959963984540054))
            interval = wilson(count, repetitions)
            rows.append(
                {
                    "claim": "claim1_oracle_reference_decomposition",
                    "scenario": "independent_lognormal_gamma_strong_skew",
                    "reference_fit": reference,
                    "n": n,
                    "repetitions": repetitions,
                    "root_cell_seed": seed,
                    "population_huber_center_x": centre_x,
                    "population_huber_center_y": centre_y,
                    "mean_estimate": float(np.mean(estimates)),
                    "empirical_sd_estimate": float(np.std(estimates, ddof=1)),
                    "mean_z": float(np.mean(z)),
                    "sd_z": float(np.std(z, ddof=1)),
                    "q025_z": float(np.quantile(z, 0.025)),
                    "q975_z": float(np.quantile(z, 0.975)),
                    "rejections": count,
                    "rejection_rate": count / repetitions,
                    "wilson_95_low": interval[0],
                    "wilson_95_high": interval[1],
                }
            )
    return rows


def claim2_sign_coupling_dose_response(
    repetitions: int,
) -> list[dict[str, float | int | str]]:
    """Vary shared mode-selection coupling while fixed profiles stay uncorrelated."""
    rows = []
    for n_index, n in enumerate((80, 640), start=1):
        for coupling_index, coupling in enumerate((0.0, 0.25, 0.50, 0.75, 1.0), start=1):
            seed = 2026082551 + 100_000 * n_index + 10_000 * coupling_index + n
            rng = np.random.default_rng(seed)
            fitted_rejection, fixed_rejection = [], []
            fitted_effect, fixed_effect = [], []
            centre_product = []
            for _ in range(repetitions):
                sign_x = rng.choice((-1.0, 1.0), size=n)
                independent_sign_y = rng.choice((-1.0, 1.0), size=n)
                linked = rng.random(n) < coupling
                sign_y = np.where(linked, sign_x, independent_sign_y)
                x = sign_x * np.exp(0.10 * rng.normal(size=n))
                y = sign_y * np.exp(0.10 * rng.normal(size=n))
                fitted = profile_weak_null_test(x, y)
                fixed = fixed_center_profile_test(x, y)
                fitted_rejection.append(float(fitted["p_value"]) <= 0.05)
                fixed_rejection.append(bool(fixed["reject"]))
                fitted_effect.append(float(fitted["estimate"]))
                fixed_effect.append(float(fixed["estimate"]))
                centre_product.append(_huber_center(x) * _huber_center(y))
            fitted_count = int(np.sum(fitted_rejection))
            fixed_count = int(np.sum(fixed_rejection))
            fitted_interval = wilson(fitted_count, repetitions)
            fixed_interval = wilson(fixed_count, repetitions)
            rows.append(
                {
                    "claim": "claim2_sign_coupling_dose_response",
                    "n": n,
                    "shared_sign_coupling": coupling,
                    "population_fixed_profile_correlation": 0.0,
                    "repetitions": repetitions,
                    "root_cell_seed": seed,
                    "mean_huber_center_product": float(np.mean(centre_product)),
                    "mean_refitted_profile_effect": float(np.mean(fitted_effect)),
                    "refitted_rejection_rate": fitted_count / repetitions,
                    "refitted_wilson_95_low": fitted_interval[0],
                    "refitted_wilson_95_high": fitted_interval[1],
                    "mean_fixed_zero_profile_effect": float(np.mean(fixed_effect)),
                    "fixed_zero_rejection_rate": fixed_count / repetitions,
                    "fixed_zero_wilson_95_low": fixed_interval[0],
                    "fixed_zero_wilson_95_high": fixed_interval[1],
                }
            )
    return rows


def _old_bridge_training() -> tuple[np.ndarray, float]:
    bridge = read_tsv(RESULTS_DIR / "profile_bridge_family_validation_pilot_20260817.tsv")
    jacobian = {
        (row["scenario"], int(row["n"])): float(row["sqrt_n_minimum_singular_value"])
        for row in read_tsv(RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv")
    }
    x, successes, trials = [], [], []
    for row in bridge:
        n = int(row["n"])
        rejection = float(row["studentized_rejection"])
        repetitions = int(row["repetitions"])
        x.append((1.0, log(jacobian[(row["scenario"], n)])))
        successes.append(int(round(rejection * repetitions)))
        trials.append(repetitions)
    beta = fit_binomial_logit(
        np.asarray(x), np.asarray(successes, dtype=float), np.asarray(trials, dtype=float)
    )
    return beta, float(np.sum(successes) / np.sum(trials))


def claim3_prospective_family_validation(
    repetitions: int, n_perm: int
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    """Predict and then evaluate a fifth matched-density bridge family."""
    beta, baseline = _old_bridge_training()
    rows = []
    for n_index, n in enumerate((80, 320), start=1):
        for epsilon_index, epsilon in enumerate((0.05, 0.10, 0.20), start=1):
            nuisance = population_nuisance(
                symmetric_bridge_distribution(epsilon, "hyperexponential")
            )
            index = sqrt(n) * float(nuisance["minimum_singular_value"])
            predicted = float(_expit(np.asarray((1.0, log(index))) @ beta))
            seed = 2026082581 + 100_000 * n_index + 10_000 * epsilon_index + n
            rng = np.random.default_rng(seed)
            rejections = 0
            effects = []
            for _ in range(repetitions):
                x, y = generate_family_bridge_profile_null(
                    rng,
                    n,
                    radial_log_sd=0.10,
                    bridge_probability=epsilon,
                    bridge_family="hyperexponential",
                )
                test = profile_studentized_permutation_test(
                    x, y, random_indices(rng, n, n_perm)
                )
                rejections += int(float(test["p_value"]) <= 0.05)
                effects.append(float(test["estimate"]))
            observed = rejections / repetitions
            interval = wilson(rejections, repetitions)
            rows.append(
                {
                    "claim": "claim3_prospective_family_validation",
                    "family": "hyperexponential",
                    "origin_radius_density": 1.0,
                    "n": n,
                    "bridge_probability": epsilon,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "root_cell_seed": seed,
                    "conditioning_index": index,
                    "old_family_model_prediction": predicted,
                    "old_family_intercept_baseline": baseline,
                    "observed_rejections": rejections,
                    "observed_rejection_rate": observed,
                    "wilson_95_low": interval[0],
                    "wilson_95_high": interval[1],
                    "mean_profile_effect": float(np.mean(effects)),
                    "absolute_prediction_error": abs(observed - predicted),
                    "baseline_absolute_error": abs(observed - baseline),
                    "prediction_log_loss": _binomial_log_loss(observed, predicted),
                    "baseline_log_loss": _binomial_log_loss(observed, baseline),
                }
            )
    observed = np.asarray([row["observed_rejection_rate"] for row in rows], dtype=float)
    predicted = np.asarray([row["old_family_model_prediction"] for row in rows], dtype=float)
    baseline_values = np.asarray([row["old_family_intercept_baseline"] for row in rows], dtype=float)
    mae = float(np.mean(np.abs(observed - predicted)))
    baseline_mae = float(np.mean(np.abs(observed - baseline_values)))
    loss = float(np.mean([row["prediction_log_loss"] for row in rows]))
    baseline_loss = float(np.mean([row["baseline_log_loss"] for row in rows]))
    summary = [
        {
            "claim": "claim3_prospective_family_validation",
            "family": "hyperexponential",
            "cells": len(rows),
            "mean_absolute_error": mae,
            "baseline_mean_absolute_error": baseline_mae,
            "mae_improvement_fraction": 1.0 - mae / baseline_mae,
            "mean_log_loss": loss,
            "baseline_mean_log_loss": baseline_loss,
            "log_loss_improvement_fraction": 1.0 - loss / baseline_loss,
            "old_family_log_index_slope": float(beta[1]),
        }
    ]
    return rows, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "validation"), default="smoke")
    parser.add_argument("--claim", choices=("all", "claim1", "claim2", "claim3"), default="all")
    args = parser.parse_args()
    repetitions = 20 if args.phase == "smoke" else 600
    outputs: list[tuple[str, list[dict[str, float | int | str]]]] = []
    if args.claim in {"all", "claim1"}:
        outputs.append(("claim1_oracle_reference", claim1_oracle_reference_decomposition(repetitions)))
    if args.claim in {"all", "claim2"}:
        outputs.append(("claim2_sign_coupling", claim2_sign_coupling_dose_response(repetitions)))
    if args.claim in {"all", "claim3"}:
        claim3_repetitions = 10 if args.phase == "smoke" else 200
        n_perm = 19 if args.phase == "smoke" else 99
        rows, summary = claim3_prospective_family_validation(claim3_repetitions, n_perm)
        outputs.extend((("claim3_prospective_family", rows), ("claim3_prospective_family_summary", summary)))
    for name, rows in outputs:
        write_tsv(RESULTS_DIR / f"{name}_{args.phase}_20260825.tsv", rows)
        print(name)
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
