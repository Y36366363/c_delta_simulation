"""Externally validate signal-strength crossover models on seven new cells."""

from __future__ import annotations

import csv
from math import atanh, exp, log, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_signal_strength_surface_20260809 import (
    COARSE_WEIGHTS,
    combine_surface_runs,
    estimate_crossovers,
    fit_ratio_models,
    local_weights,
    run_strength_surface,
)


EXTERNAL_COMBINATIONS = (
    (0.35, 0.30),
    (0.55, 0.30),
    (0.75, 0.30),
    (0.65, 0.30),
    (0.65, 0.45),
    (0.65, 0.65),
    (0.65, 0.80),
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _predictor(row: dict[str, object], model: str) -> np.ndarray:
    node = float(row["node_strength"])
    dyad = float(row["dyad_strength"])
    if model == "raw_ratio":
        return np.asarray([log(node / dyad)])
    if model == "fisher_z_ratio":
        return np.asarray([log(atanh(node) / atanh(dyad))])
    if model == "separate_fisher_z":
        return np.asarray([log(atanh(node)), log(atanh(dyad))])
    raise ValueError(model)


def validate_models(
    crossover_rows: list[dict[str, object]],
    model_rows: list[dict[str, object]],
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    valid_crossovers = [
        row
        for row in crossover_rows
        if np.isfinite(float(row["crossover_estimate"]))
    ]
    predictions = []
    metrics = []
    for model_row in model_rows:
        name = str(model_row["model"])
        coefficients = [
            float(model_row["intercept"]),
            float(model_row["coefficient_1"]),
        ]
        if name == "separate_fisher_z":
            coefficients.append(float(model_row["coefficient_2"]))
        errors = []
        logit_errors = []
        for row in valid_crossovers:
            observed = float(row["crossover_estimate"])
            predictor = _predictor(row, name)
            fitted_logit = float(np.r_[1.0, predictor] @ np.asarray(coefficients))
            predicted = 1.0 / (1.0 + exp(-fitted_logit))
            observed_logit = log(observed / (1.0 - observed))
            error = observed - predicted
            logit_error = observed_logit - fitted_logit
            errors.append(error)
            logit_errors.append(logit_error)
            predictions.append(
                {
                    "model": name,
                    "node_strength": float(row["node_strength"]),
                    "dyad_strength": float(row["dyad_strength"]),
                    "observed_crossover": observed,
                    "predicted_crossover": predicted,
                    "crossover_error": error,
                    "logit_residual": logit_error,
                }
            )
        error_array = np.asarray(errors)
        logit_array = np.asarray(logit_errors)
        metrics.append(
            {
                "model": name,
                "training_combinations": int(model_row["n_combinations"]),
                "external_combinations": len(valid_crossovers),
                "external_rmse_crossover": float(sqrt(np.mean(error_array**2))),
                "external_maximum_absolute_crossover_error": float(np.max(np.abs(error_array))),
                "external_bias_crossover": float(np.mean(error_array)),
                "external_rmse_logit_crossover": float(sqrt(np.mean(logit_array**2))),
                "external_maximum_absolute_logit_error": float(np.max(np.abs(logit_array))),
                "external_bias_logit_crossover": float(np.mean(logit_array)),
            }
        )
    return metrics, predictions


def write_model_outputs(crossovers: list[dict[str, object]]) -> None:
    original_crossovers = read_tsv(
        PROJECT_ROOT / "results" / "signal_strength_surface_crossovers_20260809.tsv"
    )
    original_models = read_tsv(
        PROJECT_ROOT / "results" / "signal_strength_ratio_models_20260809.tsv"
    )
    validation, predictions = validate_models(crossovers, original_models)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_model_validation_20260809.tsv", validation)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_predictions_20260809.tsv", predictions)

    expanded = [*original_crossovers, *crossovers]
    expanded_models, expanded_predictions = fit_ratio_models(expanded)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_expanded_crossovers_20260809.tsv", expanded)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_expanded_models_20260809.tsv", expanded_models)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_expanded_predictions_20260809.tsv", expanded_predictions)


def run_boundary_checks() -> list[list[dict[str, object]]]:
    """Increase precision where both weak signals make the crossing nearly flat."""
    combination = ((0.35, 0.30),)
    weights = {
        combination[0]: (0.0, 0.05, 0.10, 0.125, 0.15, 0.175, 0.20, 0.25)
    }
    runs = []
    for phase, seed in (
        ("external_boundary_check", 20261047),
        ("external_boundary_replication", 20261048),
    ):
        rows = run_strength_surface(
            combination,
            weights,
            repetitions=800,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"signal_strength_{phase}_20260809.tsv",
            rows,
        )
    return runs


def continue_boundary_check() -> None:
    """Resume after the extension and add high-precision weak-signal checks."""
    names = (
        "external_refined",
        "external_replication",
        "external_extension",
        "external_extension_replication",
    )
    runs: list[list[dict[str, object]]] = [
        read_tsv(PROJECT_ROOT / "results" / f"signal_strength_{name}_20260809.tsv")
        for name in names
    ]
    runs.extend(run_boundary_checks())
    combined = combine_surface_runs(tuple(runs), phase="external_combined")
    crossovers = estimate_crossovers(combined, phase="external_combined")
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_combined_20260809.tsv", combined)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_crossovers_20260809.tsv", crossovers)
    write_model_outputs(crossovers)


def continue_extension() -> None:
    """Resume from existing local runs and extend the one unbracketed cell."""
    runs: list[list[dict[str, object]]] = [
        read_tsv(PROJECT_ROOT / "results" / "signal_strength_external_refined_20260809.tsv"),
        read_tsv(PROJECT_ROOT / "results" / "signal_strength_external_replication_20260809.tsv"),
    ]
    missing = ((0.65, 0.30),)
    weights = {missing[0]: (0.30, 0.325, 0.35, 0.375, 0.40, 0.425, 0.45)}
    for phase, seed in (
        ("external_extension", 20261045),
        ("external_extension_replication", 20261046),
    ):
        rows = run_strength_surface(
            missing,
            weights,
            repetitions=400,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"signal_strength_{phase}_20260809.tsv",
            rows,
        )
    combined = combine_surface_runs(tuple(runs), phase="external_combined")
    crossovers = estimate_crossovers(combined, phase="external_combined")
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_combined_20260809.tsv", combined)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_crossovers_20260809.tsv", crossovers)
    write_model_outputs(crossovers)


def run() -> None:
    coarse = run_strength_surface(
        EXTERNAL_COMBINATIONS,
        {combination: COARSE_WEIGHTS for combination in EXTERNAL_COMBINATIONS},
        repetitions=250,
        n_perm=199,
        seed=20261042,
        phase="external_coarse",
    )
    coarse_crossovers = estimate_crossovers(coarse, phase="external_coarse")
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_coarse_20260809.tsv", coarse)
    write_tsv(
        PROJECT_ROOT / "results" / "signal_strength_external_coarse_crossovers_20260809.tsv",
        coarse_crossovers,
    )

    refined_weights = local_weights(coarse_crossovers)
    runs = []
    for phase, seed in (("external_refined", 20261043), ("external_replication", 20261044)):
        rows = run_strength_surface(
            EXTERNAL_COMBINATIONS,
            refined_weights,
            repetitions=400,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        runs.append(rows)
        write_tsv(PROJECT_ROOT / "results" / f"signal_strength_{phase}_20260809.tsv", rows)

    provisional = combine_surface_runs(tuple(runs), phase="external_provisional")
    provisional_crossovers = estimate_crossovers(
        provisional, phase="external_provisional"
    )
    missing = tuple(
        (float(row["node_strength"]), float(row["dyad_strength"]))
        for row in provisional_crossovers
        if not np.isfinite(float(row["crossover_estimate"]))
    )
    if missing:
        extension_weights = {
            combination: (0.30, 0.325, 0.35, 0.375, 0.40, 0.425, 0.45)
            for combination in missing
        }
        for phase, seed in (
            ("external_extension", 20261045),
            ("external_extension_replication", 20261046),
        ):
            rows = run_strength_surface(
                missing,
                extension_weights,
                repetitions=400,
                n_perm=199,
                seed=seed,
                phase=phase,
            )
            runs.append(rows)
            write_tsv(
                PROJECT_ROOT / "results" / f"signal_strength_{phase}_20260809.tsv",
                rows,
            )

    runs.extend(run_boundary_checks())

    combined = combine_surface_runs(tuple(runs), phase="external_combined")
    crossovers = estimate_crossovers(combined, phase="external_combined")
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_combined_20260809.tsv", combined)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_external_crossovers_20260809.tsv", crossovers)

    write_model_outputs(crossovers)


if __name__ == "__main__":
    run()
