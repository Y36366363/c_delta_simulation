"""Stricter stress validation of the three frozen manuscript claims."""

from __future__ import annotations

import argparse
from math import log, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.audit_wald_convergence_20260822 import generate_regular_scenario
from scripts.robust_extension_utils import write_tsv
from scripts.run_claim_validation_20260823 import (
    RESULTS_DIR,
    _binomial_log_loss,
    _expit,
    fit_binomial_logit,
    read_tsv,
)
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


def claim1_studentization_diagnostics(
    repetitions: int,
) -> list[dict[str, float | int | str]]:
    """Compare actual estimator spread with the reported sandwich scale."""
    designs = (
        ("profile_null_normal_sign_link", 160),
        ("profile_null_normal_sign_link", 640),
        ("independent_t5", 320),
        ("independent_t5", 640),
        ("independent_strong_skew", 640),
        ("independent_strong_skew", 2560),
    )
    rows = []
    for index, (scenario, n) in enumerate(designs, start=1):
        seed = 2026082401 + 100_000 * index + n
        rng = np.random.default_rng(seed)
        estimates, standard_errors, z_statistics = [], [], []
        failures = 0
        for _ in range(repetitions):
            x, y = generate_regular_scenario(rng, scenario, n)
            try:
                result = profile_weak_null_test(x, y)
            except (FloatingPointError, ValueError, np.linalg.LinAlgError):
                failures += 1
                continue
            estimates.append(float(result["estimate"]))
            standard_errors.append(float(result["standard_error"]))
            z_statistics.append(float(result["z_statistic"]))
        estimates_array = np.asarray(estimates)
        se_array = np.asarray(standard_errors)
        z_array = np.asarray(z_statistics)
        valid = z_array.size
        rejection_count = int(np.sum(np.abs(z_array) >= 1.959963984540054))
        interval = wilson(rejection_count, valid)
        empirical_sd = float(np.std(estimates_array, ddof=1))
        rms_se = float(np.sqrt(np.mean(se_array**2)))
        rows.append(
            {
                "claim": "claim1_studentization_diagnostic",
                "scenario": scenario,
                "n": n,
                "repetitions": repetitions,
                "valid_repetitions": valid,
                "failures": failures,
                "root_cell_seed": seed,
                "mean_estimate": float(np.mean(estimates_array)),
                "empirical_sd_estimate": empirical_sd,
                "root_mean_squared_reported_se": rms_se,
                "reported_se_to_empirical_sd": rms_se / empirical_sd,
                "mean_studentized_z": float(np.mean(z_array)),
                "sd_studentized_z": float(np.std(z_array, ddof=1)),
                "q025_studentized_z": float(np.quantile(z_array, 0.025)),
                "q975_studentized_z": float(np.quantile(z_array, 0.975)),
                "rejection_rate": rejection_count / valid,
                "wilson_95_low": interval[0],
                "wilson_95_high": interval[1],
            }
        )
    return rows


def _huber_center(values: np.ndarray, huber_c: float = 1.345) -> float:
    """Match the project's fixed-MAD Huber location fit."""
    median = float(np.median(values))
    scale = 1.4826 * float(np.median(np.abs(values - median)))
    if scale <= 0.0:
        raise ValueError("positive MAD required")
    location = median
    for _ in range(100):
        residual = (values - location) / scale
        weights = np.minimum(1.0, huber_c / np.maximum(np.abs(residual), 1e-15))
        updated = float(np.sum(weights * values) / np.sum(weights))
        if abs(updated - location) < 1e-10 * max(1.0, scale):
            return updated
        location = updated
    return location


def claim2_sign_balance_intervention(
    repetitions: int,
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    """Intervene on sign-count imbalance in the separated-mode null."""
    rows = []
    iid_records: list[dict[str, float | int]] = []
    for n_index, n in enumerate((80, 640), start=1):
        for design_index, sign_design in enumerate(("iid_signs", "exactly_balanced_signs"), start=1):
            seed = 2026082451 + 100_000 * n_index + 10_000 * design_index + n
            rng = np.random.default_rng(seed)
            records = []
            for _ in range(repetitions):
                if sign_design == "iid_signs":
                    signs = rng.choice((-1.0, 1.0), size=n)
                else:
                    signs = np.concatenate((np.ones(n // 2), -np.ones(n - n // 2)))
                    rng.shuffle(signs)
                x = signs * np.exp(0.10 * rng.normal(size=n))
                y = signs * np.exp(0.10 * rng.normal(size=n))
                result = profile_weak_null_test(x, y)
                center_x, center_y = _huber_center(x), _huber_center(y)
                record = {
                    "rejected": int(float(result["p_value"]) <= 0.05),
                    "effect": float(result["estimate"]),
                    "absolute_sign_imbalance": abs(float(np.mean(signs))),
                    "maximum_absolute_huber_center": max(abs(center_x), abs(center_y)),
                }
                records.append(record)
                if sign_design == "iid_signs":
                    iid_records.append({"n": n, **record})
            rejection_count = int(sum(record["rejected"] for record in records))
            interval = wilson(rejection_count, repetitions)
            rows.append(
                {
                    "claim": "claim2_sign_balance_mechanism",
                    "radial_log_sd": 0.10,
                    "n": n,
                    "sign_design": sign_design,
                    "repetitions": repetitions,
                    "root_cell_seed": seed,
                    "mean_absolute_sign_imbalance": float(
                        np.mean([record["absolute_sign_imbalance"] for record in records])
                    ),
                    "mean_maximum_absolute_huber_center": float(
                        np.mean([record["maximum_absolute_huber_center"] for record in records])
                    ),
                    "mean_profile_effect": float(np.mean([record["effect"] for record in records])),
                    "rejections": rejection_count,
                    "rejection_rate": rejection_count / repetitions,
                    "wilson_95_low": interval[0],
                    "wilson_95_high": interval[1],
                }
            )

    bins = []
    for n in (80, 640):
        subset = [record for record in iid_records if record["n"] == n]
        imbalance = np.asarray([record["absolute_sign_imbalance"] for record in subset])
        # Discrete sign counts create tied quantiles, so equal-frequency ranks
        # give stable diagnostic strata without pretending to be fixed cutoffs.
        order = np.argsort(imbalance, kind="stable")
        strata = np.empty(len(subset), dtype=int)
        strata[order] = np.minimum(3, 4 * np.arange(len(subset)) // len(subset))
        for stratum in range(4):
            selected = [record for index, record in enumerate(subset) if strata[index] == stratum]
            count = int(sum(record["rejected"] for record in selected))
            interval = wilson(count, len(selected))
            bins.append(
                {
                    "claim": "claim2_sign_imbalance_gradient",
                    "n": n,
                    "imbalance_rank_quartile": stratum + 1,
                    "cells": len(selected),
                    "mean_absolute_sign_imbalance": float(
                        np.mean([record["absolute_sign_imbalance"] for record in selected])
                    ),
                    "mean_maximum_absolute_huber_center": float(
                        np.mean([record["maximum_absolute_huber_center"] for record in selected])
                    ),
                    "rejection_rate": count / len(selected),
                    "wilson_95_low": interval[0],
                    "wilson_95_high": interval[1],
                }
            )
    return rows, bins


def _bridge_records() -> list[dict[str, float | int | str]]:
    bridge = read_tsv(RESULTS_DIR / "profile_bridge_family_validation_pilot_20260817.tsv")
    jacobian = {
        (row["scenario"], int(row["n"])): float(row["sqrt_n_minimum_singular_value"])
        for row in read_tsv(RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv")
    }
    records = []
    for row in bridge:
        trials = int(row["repetitions"])
        observed = float(row["studentized_rejection"])
        records.append(
            {
                "family": row["bridge_family"],
                "scenario": row["scenario"],
                "n": int(row["n"]),
                "epsilon": float(row["bridge_probability"]),
                "trials": trials,
                "successes": int(round(trials * observed)),
                "observed": observed,
                "index": jacobian[(row["scenario"], int(row["n"]))],
            }
        )
    return records


def _cross_validation_fold(
    records: list[dict[str, float | int | str]],
    training: list[dict[str, float | int | str]],
    held_out: list[dict[str, float | int | str]],
    scheme: str,
    fold: str,
) -> list[dict[str, float | int | str]]:
    x = np.asarray([[1.0, log(float(row["index"]))] for row in training])
    successes = np.asarray([row["successes"] for row in training], dtype=float)
    trials = np.asarray([row["trials"] for row in training], dtype=float)
    beta = fit_binomial_logit(x, successes, trials)
    baseline = float(np.sum(successes) / np.sum(trials))
    output = []
    for row in held_out:
        predicted = float(_expit(np.asarray([1.0, log(float(row["index"]))]) @ beta))
        observed = float(row["observed"])
        output.append(
            {
                "claim": "claim3_stricter_conditioning_validation",
                "cv_scheme": scheme,
                "fold": fold,
                "held_out_family": row["family"],
                "scenario": row["scenario"],
                "n": row["n"],
                "epsilon": row["epsilon"],
                "conditioning_index": row["index"],
                "observed_rejection": observed,
                "predicted_rejection": predicted,
                "baseline_prediction": baseline,
                "absolute_error": abs(observed - predicted),
                "baseline_absolute_error": abs(observed - baseline),
                "log_loss": _binomial_log_loss(observed, predicted),
                "baseline_log_loss": _binomial_log_loss(observed, baseline),
                "training_log_index_slope": float(beta[1]),
            }
        )
    return output


def claim3_stricter_cross_validation() -> tuple[
    list[dict[str, float | int | str]], list[dict[str, float | int | str]]
]:
    records = _bridge_records()
    predictions = []
    for held_n in (80, 320):
        training = [row for row in records if row["n"] != held_n]
        held_out = [row for row in records if row["n"] == held_n]
        predictions.extend(
            _cross_validation_fold(records, training, held_out, "cross_sample_size", f"hold_n_{held_n}")
        )
    levels = sorted({(int(row["n"]), float(row["epsilon"])) for row in records})
    for held_n, held_epsilon in levels:
        training = [
            row for row in records
            if not (row["n"] == held_n and row["epsilon"] == held_epsilon)
        ]
        held_out = [
            row for row in records
            if row["n"] == held_n and row["epsilon"] == held_epsilon
        ]
        predictions.extend(
            _cross_validation_fold(
                records,
                training,
                held_out,
                "leave_conditioning_level_out",
                f"hold_n_{held_n}_epsilon_{held_epsilon:g}",
            )
        )
    summaries = []
    schemes = sorted({str(row["cv_scheme"]) for row in predictions})
    for scheme in schemes:
        subset = [row for row in predictions if row["cv_scheme"] == scheme]
        observed = np.asarray([row["observed_rejection"] for row in subset])
        predicted = np.asarray([row["predicted_rejection"] for row in subset])
        baseline = np.asarray([row["baseline_prediction"] for row in subset])
        mae = float(np.mean(np.abs(observed - predicted)))
        baseline_mae = float(np.mean(np.abs(observed - baseline)))
        loss = float(np.mean([row["log_loss"] for row in subset]))
        baseline_loss = float(np.mean([row["baseline_log_loss"] for row in subset]))
        summaries.append(
            {
                "claim": "claim3_stricter_conditioning_validation",
                "cv_scheme": scheme,
                "held_out_cells": len(subset),
                "mean_absolute_error": mae,
                "baseline_mean_absolute_error": baseline_mae,
                "mae_improvement_fraction": 1.0 - mae / baseline_mae,
                "mean_log_loss": loss,
                "baseline_mean_log_loss": baseline_loss,
                "log_loss_improvement_fraction": 1.0 - loss / baseline_loss,
                "minimum_training_log_index_slope": min(
                    float(row["training_log_index_slope"]) for row in subset
                ),
                "maximum_training_log_index_slope": max(
                    float(row["training_log_index_slope"]) for row in subset
                ),
            }
        )
    return predictions, summaries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "validation"), default="smoke")
    parser.add_argument("--claim", choices=("all", "claim1", "claim2", "claim3"), default="all")
    args = parser.parse_args()
    repetitions = 20 if args.phase == "smoke" else 800
    suffix = args.phase
    outputs: list[tuple[str, list[dict[str, float | int | str]]]] = []
    if args.claim in {"all", "claim1"}:
        outputs.append(("claim1_studentization_diagnostics", claim1_studentization_diagnostics(repetitions)))
    if args.claim in {"all", "claim2"}:
        claim2, claim2_gradient = claim2_sign_balance_intervention(repetitions)
        outputs.extend(
            (
                ("claim2_sign_balance_intervention", claim2),
                ("claim2_sign_imbalance_gradient", claim2_gradient),
            )
        )
    if args.claim in {"all", "claim3"}:
        claim3, claim3_summary = claim3_stricter_cross_validation()
        outputs.extend(
            (
                ("claim3_stricter_cv_predictions", claim3),
                ("claim3_stricter_cv_summary", claim3_summary),
            )
        )
    for name, rows in outputs:
        write_tsv(RESULTS_DIR / f"{name}_{suffix}_20260824.tsv", rows)
        print(name)
        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
