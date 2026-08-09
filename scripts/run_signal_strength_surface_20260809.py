"""Test whether the node--dyad crossover follows a signal-strength ratio."""

from __future__ import annotations

from math import atanh, exp, log, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_building_target_separation_20260808 import (
    _profile_statistics,
    mantel_test,
)
from scripts.run_node_dyad_mixture_20260808 import (
    _dyadic_components,
    _fast_within_block_indices,
    _node_components,
    _paired_difference_summary,
)


NODE_STRENGTHS = (0.35, 0.55, 0.75)
DYAD_STRENGTHS = (0.45, 0.65, 0.80)
COARSE_WEIGHTS = (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.65, 0.80, 1.0)


def _building_components(
    rng: np.random.Generator,
    node_strength: float,
    dyad_strength: float,
    *,
    n_blocks: int = 4,
    rooms_per_block: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    blocks = np.repeat(np.arange(n_blocks), rooms_per_block)
    scales = np.geomspace(1.0, 2.5, n_blocks)
    node_x = np.empty(blocks.size)
    node_y = np.empty(blocks.size)
    dyad_x = np.empty(blocks.size)
    dyad_y = np.empty(blocks.size)
    for block in range(n_blocks):
        members = np.flatnonzero(blocks == block)
        nx, ny = _node_components(
            rng, rooms_per_block, radius_rho=node_strength
        )
        dx, dy = _dyadic_components(
            rng, rooms_per_block, value_rho=dyad_strength
        )
        node_x[members], node_y[members] = scales[block] * nx, scales[block] * ny
        dyad_x[members], dyad_y[members] = scales[block] * dx, scales[block] * dy
    return node_x, node_y, dyad_x, dyad_y, blocks


def _mix_components(
    components: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    weight: float,
) -> tuple[np.ndarray, np.ndarray]:
    node_x, node_y, dyad_x, dyad_y = components
    return (
        sqrt(1.0 - weight) * node_x + sqrt(weight) * dyad_x,
        sqrt(1.0 - weight) * node_y + sqrt(weight) * dyad_y,
    )


def run_strength_surface(
    combinations: tuple[tuple[float, float], ...],
    weights_by_combination: dict[tuple[float, float], tuple[float, ...]],
    *,
    repetitions: int,
    n_perm: int,
    seed: int,
    phase: str,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for node_strength, dyad_strength in combinations:
        weights = weights_by_combination[(node_strength, dyad_strength)]
        summaries = {
            weight: {"huber": [], "mantel": [], "p_difference": 0.0}
            for weight in weights
        }
        for _ in range(repetitions):
            node_x, node_y, dyad_x, dyad_y, blocks = _building_components(
                rng, node_strength, dyad_strength
            )
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            components = (node_x, node_y, dyad_x, dyad_y)
            for weight in weights:
                x, y = _mix_components(components, weight)
                huber = _profile_statistics(
                    huber_reference_profile(x), huber_reference_profile(y), indices
                )
                _, huber_p = huber["ratio"]
                _, pearson_p = huber["correlation"]
                _, mantel_p = mantel_test(x, y, indices)
                summaries[weight]["huber"].append(huber_p < 0.05)
                summaries[weight]["mantel"].append(mantel_p < 0.05)
                summaries[weight]["p_difference"] = max(
                    summaries[weight]["p_difference"],
                    abs(huber_p - pearson_p),
                )
        for weight in weights:
            huber_reject = np.asarray(summaries[weight]["huber"], dtype=bool)
            mantel_reject = np.asarray(summaries[weight]["mantel"], dtype=bool)
            paired = _paired_difference_summary(huber_reject, mantel_reject)
            rows.append(
                {
                    "phase": phase,
                    "node_strength": node_strength,
                    "dyad_strength": dyad_strength,
                    "raw_strength_ratio": node_strength / dyad_strength,
                    "fisher_z_strength_ratio": atanh(node_strength) / atanh(dyad_strength),
                    "dyadic_weight": weight,
                    "node_weight": 1.0 - weight,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    **paired,
                    "maximum_huber_cdelta_pearson_p_difference": summaries[weight]["p_difference"],
                }
            )
    return rows


def estimate_crossovers(
    surface_rows: list[dict[str, float | int | str]],
    *,
    phase: str,
) -> list[dict[str, float | int | str]]:
    output = []
    combinations = sorted(
        {
            (float(row["node_strength"]), float(row["dyad_strength"]))
            for row in surface_rows
        }
    )
    for node_strength, dyad_strength in combinations:
        selected = sorted(
            (
                row
                for row in surface_rows
                if float(row["node_strength"]) == node_strength
                and float(row["dyad_strength"]) == dyad_strength
            ),
            key=lambda row: float(row["dyadic_weight"]),
        )
        bracket_low = bracket_high = estimate = np.nan
        for left, right in zip(selected[:-1], selected[1:]):
            dl = float(left["power_difference"])
            dr = float(right["power_difference"])
            if dl == 0.0 or dl * dr <= 0.0:
                wl = float(left["dyadic_weight"])
                wr = float(right["dyadic_weight"])
                bracket_low, bracket_high = wl, wr
                estimate = wl if dl == 0.0 else wl - dl * (wr - wl) / (dr - dl)
                break
        uncertain = [
            float(row["dyadic_weight"])
            for row in selected
            if float(row["paired_ci_low"]) <= 0.0 <= float(row["paired_ci_high"])
        ]
        output.append(
            {
                "phase": phase,
                "node_strength": node_strength,
                "dyad_strength": dyad_strength,
                "raw_strength_ratio": node_strength / dyad_strength,
                "fisher_z_strength_ratio": atanh(node_strength) / atanh(dyad_strength),
                "bracket_low": bracket_low,
                "bracket_high": bracket_high,
                "crossover_estimate": estimate,
                "zero_difference_band_low": min(uncertain) if uncertain else np.nan,
                "zero_difference_band_high": max(uncertain) if uncertain else np.nan,
                "grid_points": len(selected),
                "repetitions_per_point": int(selected[0]["repetitions"]),
                "n_perm": int(selected[0]["n_perm"]),
            }
        )
    return output


def local_weights(
    crossover_rows: list[dict[str, float | int | str]],
    *,
    step: float = 0.025,
    padding: float = 0.05,
) -> dict[tuple[float, float], tuple[float, ...]]:
    result = {}
    for row in crossover_rows:
        left = float(row["bracket_low"])
        right = float(row["bracket_high"])
        if not np.isfinite(left) or not np.isfinite(right):
            raise ValueError("coarse grid did not bracket a crossover")
        lower = max(0.0, left - padding)
        upper = min(1.0, right + padding)
        count = int(round((upper - lower) / step))
        weights = tuple(round(lower + step * index, 3) for index in range(count + 1))
        key = (float(row["node_strength"]), float(row["dyad_strength"]))
        result[key] = weights
    return result


def combine_surface_runs(
    runs: tuple[list[dict[str, float | int | str]], ...],
    *,
    phase: str = "combined",
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[float, float, float], dict[str, int]] = {}
    for rows in runs:
        for row in rows:
            key = (
                float(row["node_strength"]),
                float(row["dyad_strength"]),
                float(row["dyadic_weight"]),
            )
            cell = grouped.setdefault(
                key,
                {
                    "repetitions": 0,
                    "profile_only_rejections": 0,
                    "mantel_only_rejections": 0,
                    "both_reject": 0,
                    "neither_reject": 0,
                    "n_perm": int(row["n_perm"]),
                },
            )
            for field in (
                "repetitions",
                "profile_only_rejections",
                "mantel_only_rejections",
                "both_reject",
                "neither_reject",
            ):
                cell[field] += int(row[field])
    output = []
    for (node_strength, dyad_strength, weight), cell in sorted(grouped.items()):
        n = cell["repetitions"]
        po = cell["profile_only_rejections"]
        mo = cell["mantel_only_rejections"]
        both = cell["both_reject"]
        neither = cell["neither_reject"]
        difference = (po - mo) / n
        variance = (po + mo - n * difference**2) / (n - 1)
        standard_error = sqrt(variance / n)
        output.append(
            {
                "phase": phase,
                "node_strength": node_strength,
                "dyad_strength": dyad_strength,
                "raw_strength_ratio": node_strength / dyad_strength,
                "fisher_z_strength_ratio": atanh(node_strength) / atanh(dyad_strength),
                "dyadic_weight": weight,
                "node_weight": 1.0 - weight,
                "repetitions": n,
                "n_perm": cell["n_perm"],
                "profile_power": (po + both) / n,
                "mantel_power": (mo + both) / n,
                "power_difference": difference,
                "paired_standard_error": standard_error,
                "paired_ci_low": difference - 1.96 * standard_error,
                "paired_ci_high": difference + 1.96 * standard_error,
                "profile_only_rejections": po,
                "mantel_only_rejections": mo,
                "both_reject": both,
                "neither_reject": neither,
                "maximum_huber_cdelta_pearson_p_difference": 0.0,
            }
        )
    return output


def _fit_linear(y: np.ndarray, x: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    design = np.column_stack((np.ones(y.size), x))
    coefficients, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ coefficients
    residual = y - fitted
    total = float(np.sum((y - np.mean(y)) ** 2))
    r_squared = 1.0 - float(np.sum(residual**2)) / total
    rmse = float(np.sqrt(np.mean(residual**2)))
    maximum_error = float(np.max(np.abs(residual)))
    return coefficients, r_squared, rmse, maximum_error


def _leave_one_out_error(y: np.ndarray, x: np.ndarray) -> tuple[float, float]:
    residuals = []
    for omitted in range(y.size):
        keep = np.arange(y.size) != omitted
        coefficients, _, _, _ = _fit_linear(y[keep], x[keep])
        prediction = float(
            np.concatenate(([1.0], np.asarray(x[omitted]).reshape(-1)))
            @ coefficients
        )
        residuals.append(float(y[omitted] - prediction))
    residuals_array = np.asarray(residuals)
    return (
        float(np.sqrt(np.mean(residuals_array**2))),
        float(np.max(np.abs(residuals_array))),
    )


def fit_ratio_models(
    crossover_rows: list[dict[str, float | int | str]],
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    valid = [row for row in crossover_rows if np.isfinite(float(row["crossover_estimate"]))]
    weights = np.asarray([float(row["crossover_estimate"]) for row in valid])
    y = np.log(weights / (1.0 - weights))
    raw_log_ratio = np.log(
        np.asarray([float(row["raw_strength_ratio"]) for row in valid])
    )
    fisher_log_ratio = np.log(
        np.asarray([float(row["fisher_z_strength_ratio"]) for row in valid])
    )
    node_log = np.log(np.asarray([atanh(float(row["node_strength"])) for row in valid]))
    dyad_log = np.log(np.asarray([atanh(float(row["dyad_strength"])) for row in valid]))
    model_specs = {
        "raw_ratio": raw_log_ratio[:, None],
        "fisher_z_ratio": fisher_log_ratio[:, None],
        "separate_fisher_z": np.column_stack((node_log, dyad_log)),
    }
    model_rows = []
    prediction_rows = []
    for name, predictors in model_specs.items():
        coefficients, r_squared, rmse, maximum_error = _fit_linear(y, predictors)
        loocv_rmse, loocv_maximum_error = _leave_one_out_error(y, predictors)
        design = np.column_stack((np.ones(y.size), predictors))
        fitted_logit = design @ coefficients
        predicted = 1.0 / (1.0 + np.exp(-fitted_logit))
        model_rows.append(
            {
                "model": name,
                "n_combinations": len(valid),
                "intercept": float(coefficients[0]),
                "coefficient_1": float(coefficients[1]),
                "coefficient_2": float(coefficients[2]) if len(coefficients) > 2 else np.nan,
                "r_squared_logit_crossover": r_squared,
                "rmse_logit_crossover": rmse,
                "maximum_absolute_logit_residual": maximum_error,
                "loocv_rmse_logit_crossover": loocv_rmse,
                "loocv_maximum_absolute_logit_error": loocv_maximum_error,
                "separate_coefficient_sum": (
                    float(coefficients[1] + coefficients[2])
                    if len(coefficients) > 2
                    else np.nan
                ),
            }
        )
        for row, prediction, residual in zip(valid, predicted, y - fitted_logit):
            prediction_rows.append(
                {
                    "model": name,
                    "node_strength": float(row["node_strength"]),
                    "dyad_strength": float(row["dyad_strength"]),
                    "observed_crossover": float(row["crossover_estimate"]),
                    "predicted_crossover": float(prediction),
                    "crossover_error": float(row["crossover_estimate"]) - float(prediction),
                    "logit_residual": float(residual),
                }
            )
    return model_rows, prediction_rows


if __name__ == "__main__":
    combinations = tuple(
        (node, dyad) for node in NODE_STRENGTHS for dyad in DYAD_STRENGTHS
    )
    coarse_weights = {combination: COARSE_WEIGHTS for combination in combinations}
    coarse = run_strength_surface(
        combinations,
        coarse_weights,
        repetitions=300,
        n_perm=199,
        seed=20261030,
        phase="coarse",
    )
    coarse_crossovers = estimate_crossovers(coarse, phase="coarse")
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_surface_coarse_20260809.tsv", coarse)
    refined_weights = local_weights(coarse_crossovers)
    refined_runs = []
    for phase, seed in (("refined", 20261031), ("replication", 20261032)):
        rows = run_strength_surface(
            combinations,
            refined_weights,
            repetitions=400,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        refined_runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"signal_strength_surface_{phase}_20260809.tsv",
            rows,
        )
    combined = combine_surface_runs(tuple(refined_runs))
    crossovers = estimate_crossovers(combined, phase="combined")
    models, predictions = fit_ratio_models(crossovers)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_surface_combined_20260809.tsv", combined)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_surface_crossovers_20260809.tsv", crossovers)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_ratio_models_20260809.tsv", models)
    write_tsv(PROJECT_ROOT / "results" / "signal_strength_ratio_predictions_20260809.tsv", predictions)
