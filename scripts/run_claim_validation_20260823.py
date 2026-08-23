"""Independent, claim-directed validation for the frozen paper architecture.

Claim 1 is checked with new seeds under regular iid weak-null laws. Claim 2
compares the fitted robust reference with the known population reference on
the same near-degenerate samples. Claim 3 uses leave-one-family-out prediction
on the already frozen 24-cell bridge experiment.
"""

from __future__ import annotations

import argparse
import csv
from math import exp, log, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.audit_wald_convergence_20260822 import audit_cell
from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_regularity_comparison_20260816 import (
    generate_sign_link_profile_null,
)
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_weak_null_local_tests_20260814 import (
    _correlation_delta,
    profile_weak_null_test,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def run_claim1(repetitions: int) -> list[dict[str, float | int | str]]:
    """Independently replicate regular-Wald calibration and its skew boundary."""
    designs = (
        ("profile_null_normal_sign_link", 160, "regular_dependent_weak_null"),
        ("profile_null_normal_sign_link", 640, "regular_dependent_weak_null"),
        ("independent_t5", 320, "regular_global_null"),
        ("independent_t5", 640, "regular_global_null"),
        ("independent_strong_skew", 640, "regular_slow_convergence_stress"),
        ("independent_strong_skew", 2560, "regular_slow_convergence_stress"),
    )
    rows = []
    for index, (scenario, n, role) in enumerate(designs, start=1):
        row = audit_cell(
            scenario=scenario,
            n=n,
            repetitions=repetitions,
            seed=2026082301 + 100_000 * index + n,
            regularity_class="inside_appendix_conditions",
        )
        row["claim"] = "claim1_pointwise_iid_wald"
        row["design_role"] = role
        rows.append(row)
    return rows


def fixed_center_profile_test(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    """Wald test for Corr(|X|, |Y|)=0 at the symmetry-defined centre zero."""
    a, b = np.abs(x), np.abs(y)
    moments = np.asarray(
        (np.mean(a * b), np.mean(a), np.mean(b), np.mean(a**2), np.mean(b**2))
    )
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    moment_if = np.column_stack((a * b, a, b, a**2, b**2)) - moments
    influence = moment_if @ gradient
    influence -= np.mean(influence)
    standard_error = sqrt(float(np.sum(influence**2)) / (x.size - 1) / x.size)
    z_statistic = estimate / standard_error
    # 1.959963984540054 is the two-sided standard-normal .05 cutoff.
    return {
        "estimate": float(estimate),
        "standard_error": standard_error,
        "z_statistic": float(z_statistic),
        "reject": float(abs(z_statistic) >= 1.959963984540054),
    }


def run_claim2(repetitions: int) -> list[dict[str, float | int | str]]:
    """Isolate fitted-reference distortion using a paired oracle comparison."""
    rows = []
    for sd_index, radial_log_sd in enumerate((0.10, 0.40), start=1):
        for n_index, n in enumerate((80, 640), start=1):
            seed = 2026082351 + 100_000 * sd_index + 10_000 * n_index + n
            rng = np.random.default_rng(seed)
            fitted_reject, oracle_reject = [], []
            fitted_effect, oracle_effect = [], []
            failures = 0
            for _ in range(repetitions):
                x, y = generate_sign_link_profile_null(rng, n, radial_log_sd)
                try:
                    fitted = profile_weak_null_test(x, y)
                    oracle = fixed_center_profile_test(x, y)
                except (FloatingPointError, ValueError, np.linalg.LinAlgError):
                    failures += 1
                    continue
                fitted_reject.append(float(fitted["p_value"]) <= 0.05)
                oracle_reject.append(bool(oracle["reject"]))
                fitted_effect.append(float(fitted["estimate"]))
                oracle_effect.append(float(oracle["estimate"]))
            fitted_indicator = np.asarray(fitted_reject, dtype=float)
            oracle_indicator = np.asarray(oracle_reject, dtype=float)
            valid = fitted_indicator.size
            if valid == 0:
                raise RuntimeError("all claim-2 fits failed")
            fitted_count = int(np.sum(fitted_indicator))
            oracle_count = int(np.sum(oracle_indicator))
            fitted_interval = wilson(fitted_count, valid)
            oracle_interval = wilson(oracle_count, valid)
            paired = fitted_indicator - oracle_indicator
            rows.append(
                {
                    "claim": "claim2_reference_fitting_mechanism",
                    "scenario": f"shared_sign_independent_lognormal_radii_sd_{radial_log_sd:g}",
                    "radial_log_sd": radial_log_sd,
                    "n": n,
                    "repetitions": repetitions,
                    "valid_repetitions": valid,
                    "failures": failures,
                    "root_cell_seed": seed,
                    "symmetry_reference_center": 0.0,
                    "mean_fitted_reference_effect": float(np.mean(fitted_effect)),
                    "fitted_reference_rejections": fitted_count,
                    "fitted_reference_rejection_rate": fitted_count / valid,
                    "fitted_wilson_95_low": fitted_interval[0],
                    "fitted_wilson_95_high": fitted_interval[1],
                    "mean_fixed_center_effect": float(np.mean(oracle_effect)),
                    "fixed_center_rejections": oracle_count,
                    "fixed_center_rejection_rate": oracle_count / valid,
                    "fixed_center_wilson_95_low": oracle_interval[0],
                    "fixed_center_wilson_95_high": oracle_interval[1],
                    "paired_rejection_rate_difference": float(np.mean(paired)),
                    "paired_difference_mcse": float(np.std(paired, ddof=1) / sqrt(valid)),
                }
            )
    return rows


def _expit(value: np.ndarray) -> np.ndarray:
    return np.where(
        value >= 0,
        1.0 / (1.0 + np.exp(-value)),
        np.exp(value) / (1.0 + np.exp(value)),
    )


def fit_binomial_logit(
    x: np.ndarray, successes: np.ndarray, trials: np.ndarray
) -> np.ndarray:
    """Fit a two-parameter aggregate-binomial logit by stable Newton steps."""
    pooled = float(np.sum(successes) / np.sum(trials))
    beta = np.asarray((log(pooled / (1.0 - pooled)), 0.0))
    for _ in range(100):
        probability = np.clip(_expit(x @ beta), 1e-9, 1.0 - 1e-9)
        gradient = x.T @ (successes - trials * probability)
        information = x.T @ ((trials * probability * (1.0 - probability))[:, None] * x)
        update = np.linalg.solve(information, gradient)
        beta += update
        if float(np.max(np.abs(update))) < 1e-12:
            break
    return beta


def _binomial_log_loss(observed: float, predicted: float) -> float:
    predicted = min(max(predicted, 1e-12), 1.0 - 1e-12)
    return -(observed * log(predicted) + (1.0 - observed) * log(1.0 - predicted))


def run_claim3() -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    """Test gross conditioning-index prediction across held-out bridge families."""
    bridge = read_tsv(RESULTS_DIR / "profile_bridge_family_validation_pilot_20260817.tsv")
    jacobian = {
        (row["scenario"], int(row["n"])): float(row["sqrt_n_minimum_singular_value"])
        for row in read_tsv(RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv")
    }
    records = []
    for row in bridge:
        repetitions = int(row["repetitions"])
        rejection = float(row["studentized_rejection"])
        records.append(
            {
                "family": row["bridge_family"],
                "scenario": row["scenario"],
                "n": int(row["n"]),
                "trials": repetitions,
                "successes": int(round(repetitions * rejection)),
                "observed": rejection,
                "conditioning_index": jacobian[(row["scenario"], int(row["n"]))],
            }
        )

    predictions = []
    families = sorted({str(row["family"]) for row in records})
    for family in families:
        training = [row for row in records if row["family"] != family]
        held_out = [row for row in records if row["family"] == family]
        x_train = np.asarray(
            [[1.0, log(float(row["conditioning_index"]))] for row in training]
        )
        successes = np.asarray([row["successes"] for row in training], dtype=float)
        trials = np.asarray([row["trials"] for row in training], dtype=float)
        beta = fit_binomial_logit(x_train, successes, trials)
        baseline = float(np.sum(successes) / np.sum(trials))
        for row in held_out:
            predicted = float(
                _expit(np.asarray([1.0, log(float(row["conditioning_index"]))]) @ beta)
            )
            observed = float(row["observed"])
            predictions.append(
                {
                    "claim": "claim3_conditioning_generalization",
                    "held_out_family": family,
                    "scenario": row["scenario"],
                    "n": row["n"],
                    "trials": row["trials"],
                    "conditioning_index": row["conditioning_index"],
                    "observed_rejection": observed,
                    "lofo_predicted_rejection": predicted,
                    "training_intercept_only_prediction": baseline,
                    "lofo_absolute_error": abs(observed - predicted),
                    "baseline_absolute_error": abs(observed - baseline),
                    "lofo_log_loss": _binomial_log_loss(observed, predicted),
                    "baseline_log_loss": _binomial_log_loss(observed, baseline),
                    "training_logit_intercept": float(beta[0]),
                    "training_logit_log_index_slope": float(beta[1]),
                }
            )

    summaries = []
    for family in (*families, "pooled"):
        subset = predictions if family == "pooled" else [
            row for row in predictions if row["held_out_family"] == family
        ]
        weights = np.asarray([row["trials"] for row in subset], dtype=float)
        observed = np.asarray([row["observed_rejection"] for row in subset])
        predicted = np.asarray([row["lofo_predicted_rejection"] for row in subset])
        baseline = np.asarray([row["training_intercept_only_prediction"] for row in subset])
        summaries.append(
            {
                "claim": "claim3_conditioning_generalization",
                "held_out_family": family,
                "cells": len(subset),
                "weighted_lofo_mae": float(np.average(np.abs(observed - predicted), weights=weights)),
                "weighted_baseline_mae": float(np.average(np.abs(observed - baseline), weights=weights)),
                "weighted_lofo_log_loss": float(
                    np.average(
                        [_binomial_log_loss(o, p) for o, p in zip(observed, predicted, strict=True)],
                        weights=weights,
                    )
                ),
                "weighted_baseline_log_loss": float(
                    np.average(
                        [_binomial_log_loss(o, p) for o, p in zip(observed, baseline, strict=True)],
                        weights=weights,
                    )
                ),
                "mae_improvement_fraction": float(
                    1.0
                    - np.average(np.abs(observed - predicted), weights=weights)
                    / np.average(np.abs(observed - baseline), weights=weights)
                ),
                "log_loss_improvement_fraction": float(
                    1.0
                    - np.average(
                        [_binomial_log_loss(o, p) for o, p in zip(observed, predicted, strict=True)],
                        weights=weights,
                    )
                    / np.average(
                        [_binomial_log_loss(o, p) for o, p in zip(observed, baseline, strict=True)],
                        weights=weights,
                    )
                ),
            }
        )
    return predictions, summaries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "validation"), default="smoke")
    args = parser.parse_args()
    repetitions = 20 if args.phase == "smoke" else 1000
    claim1 = run_claim1(repetitions)
    claim2 = run_claim2(repetitions)
    claim3_predictions, claim3_summary = run_claim3()
    suffix = args.phase
    write_tsv(RESULTS_DIR / f"claim1_wald_{suffix}_20260823.tsv", claim1)
    write_tsv(RESULTS_DIR / f"claim2_reference_mechanism_{suffix}_20260823.tsv", claim2)
    write_tsv(
        RESULTS_DIR / f"claim3_conditioning_lofo_predictions_{suffix}_20260823.tsv",
        claim3_predictions,
    )
    write_tsv(
        RESULTS_DIR / f"claim3_conditioning_lofo_summary_{suffix}_20260823.tsv",
        claim3_summary,
    )
    for label, rows in (
        ("claim1", claim1),
        ("claim2", claim2),
        ("claim3_summary", claim3_summary),
    ):
        print(label)
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
