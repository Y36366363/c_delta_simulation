"""Map the transition between node-salience and dyadic-geometry power."""

from __future__ import annotations

from math import sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_building_target_separation_20260808 import (
    _profile_statistics,
    mantel_test,
)
from scripts.run_robust_cdelta_grid import wilson


PROFILE_METHODS = {
    "original_l2_cdelta": lambda z: divergence_vector(z),
    "huber_cdelta_star": lambda z: huber_reference_profile(z),
    "huber_cap6_cdelta_star": lambda z: huber_reference_profile(z, cap=6.0),
}


def _standardize(values: np.ndarray) -> np.ndarray:
    centered = values - np.mean(values)
    scale = float(np.std(centered))
    if scale == 0.0:
        raise ValueError("mixture component is degenerate")
    return centered / scale


def _fast_within_block_indices(
    blocks: np.ndarray,
    n_perm: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate uniform within-block permutations without Python row loops."""
    indices = np.tile(np.arange(blocks.size), (n_perm, 1))
    for label in np.unique(blocks):
        members = np.flatnonzero(blocks == label)
        orders = np.argsort(rng.random((n_perm, members.size)), axis=1)
        indices[:, members] = members[orders]
    return indices


def _node_components(
    rng: np.random.Generator,
    size: int,
    *,
    radius_rho: float = 0.55,
) -> tuple[np.ndarray, np.ndarray]:
    if size % 2:
        raise ValueError("node component requires an even block size")
    pair_count = size // 2
    common = rng.normal(size=pair_count)
    radius_x = np.repeat(np.exp(0.55 * common), 2)
    radius_y = np.repeat(
        np.exp(
            0.55
            * (
                radius_rho * common
                + sqrt(1.0 - radius_rho**2) * rng.normal(size=pair_count)
            )
        ),
        2,
    )
    signs_x = np.tile((1.0, -1.0), pair_count)
    pair_flips = rng.choice((-1.0, 1.0), size=pair_count)
    signs_y = signs_x * np.repeat(pair_flips, 2)
    return _standardize(signs_x * radius_x), _standardize(signs_y * radius_y)


def _dyadic_components(
    rng: np.random.Generator,
    size: int,
    *,
    value_rho: float = 0.70,
) -> tuple[np.ndarray, np.ndarray]:
    x = rng.normal(size=size)
    y = value_rho * x + sqrt(1.0 - value_rho**2) * rng.normal(size=size)
    return _standardize(x), _standardize(y)


def make_mixed_building_pair(
    rng: np.random.Generator,
    dyadic_weight: float,
    *,
    n_blocks: int = 4,
    rooms_per_block: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Mix standardized node and dyadic components by variance weight.

    ``dyadic_weight=0`` is a pure sign-rewired node-salience signal and
    ``dyadic_weight=1`` is a pure correlated-value dyadic signal. Independent
    standardized components are combined with square-root weights, so the
    parameter is interpretable as an approximate within-building variance
    share rather than an arbitrary amplitude interpolation.
    """
    if not 0.0 <= dyadic_weight <= 1.0:
        raise ValueError("dyadic_weight must lie in [0, 1]")
    blocks = np.repeat(np.arange(n_blocks), rooms_per_block)
    building_scales = np.geomspace(1.0, 2.5, n_blocks)
    x = np.empty(blocks.size)
    y = np.empty(blocks.size)
    node_weight = sqrt(1.0 - dyadic_weight)
    geometry_weight = sqrt(dyadic_weight)
    for block in range(n_blocks):
        members = np.flatnonzero(blocks == block)
        node_x, node_y = _node_components(rng, rooms_per_block)
        dyad_x, dyad_y = _dyadic_components(rng, rooms_per_block)
        x[members] = building_scales[block] * (
            node_weight * node_x + geometry_weight * dyad_x
        )
        y[members] = building_scales[block] * (
            node_weight * node_y + geometry_weight * dyad_y
        )
    return x, y, blocks


def _paired_difference_summary(
    profile_reject: np.ndarray,
    mantel_reject: np.ndarray,
) -> dict[str, float | int]:
    differences = profile_reject.astype(float) - mantel_reject.astype(float)
    repetitions = differences.size
    difference = float(np.mean(differences))
    standard_error = float(np.std(differences, ddof=1) / sqrt(repetitions))
    return {
        "profile_power": float(np.mean(profile_reject)),
        "mantel_power": float(np.mean(mantel_reject)),
        "power_difference": difference,
        "paired_standard_error": standard_error,
        "paired_ci_low": max(-1.0, difference - 1.96 * standard_error),
        "paired_ci_high": min(1.0, difference + 1.96 * standard_error),
        "profile_only_rejections": int(np.sum(profile_reject & ~mantel_reject)),
        "mantel_only_rejections": int(np.sum(~profile_reject & mantel_reject)),
        "both_reject": int(np.sum(profile_reject & mantel_reject)),
        "neither_reject": int(np.sum(~profile_reject & ~mantel_reject)),
    }


def run_mixture_grid(
    weights: tuple[float, ...],
    *,
    repetitions: int,
    n_perm: int,
    seed: int,
    phase: str,
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    rng = np.random.default_rng(seed)
    method_rows: list[dict[str, float | int | str]] = []
    comparison_rows: list[dict[str, float | int | str]] = []
    for weight in weights:
        statistics = {
            method: {"reject": [], "statistic": [], "p_value": []}
            for method in (
                "original_l2_cdelta",
                "huber_cdelta_star",
                "huber_profile_pearson",
                "huber_cap6_cdelta_star",
                "mantel",
            )
        }
        maximum_huber_p_difference = 0.0
        for _ in range(repetitions):
            x, y, blocks = make_mixed_building_pair(rng, weight)
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            for method, profile in PROFILE_METHODS.items():
                sx, sy = profile(x), profile(y)
                outcomes = _profile_statistics(sx, sy, indices)
                observed, p_value = outcomes["ratio"]
                statistics[method]["reject"].append(p_value < 0.05)
                statistics[method]["statistic"].append(observed)
                statistics[method]["p_value"].append(p_value)
                if method == "huber_cdelta_star":
                    correlation, correlation_p = outcomes["correlation"]
                    statistics["huber_profile_pearson"]["reject"].append(
                        correlation_p < 0.05
                    )
                    statistics["huber_profile_pearson"]["statistic"].append(
                        correlation
                    )
                    statistics["huber_profile_pearson"]["p_value"].append(
                        correlation_p
                    )
                    maximum_huber_p_difference = max(
                        maximum_huber_p_difference, abs(p_value - correlation_p)
                    )
            mantel_observed, mantel_p = mantel_test(x, y, indices)
            statistics["mantel"]["reject"].append(mantel_p < 0.05)
            statistics["mantel"]["statistic"].append(mantel_observed)
            statistics["mantel"]["p_value"].append(mantel_p)
        if maximum_huber_p_difference > 1e-12:
            raise AssertionError("Huber c_delta_star and Pearson p-values diverged")
        for method, values in statistics.items():
            rejection = np.asarray(values["reject"], dtype=bool)
            reject_count = int(np.sum(rejection))
            low, high = wilson(reject_count, repetitions)
            method_rows.append(
                {
                    "phase": phase,
                    "dyadic_weight": weight,
                    "node_weight": 1.0 - weight,
                    "method": method,
                    "n": 48,
                    "n_blocks": 4,
                    "rooms_per_block": 12,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejection_rate": reject_count / repetitions,
                    "wilson_low": low,
                    "wilson_high": high,
                    "mean_statistic": float(np.mean(values["statistic"])),
                    "median_p_value": float(np.median(values["p_value"])),
                    "maximum_huber_cdelta_pearson_p_difference": maximum_huber_p_difference,
                }
            )
        mantel_reject = np.asarray(statistics["mantel"]["reject"], dtype=bool)
        for profile_method in (
            "original_l2_cdelta",
            "huber_cdelta_star",
            "huber_cap6_cdelta_star",
        ):
            paired = _paired_difference_summary(
                np.asarray(statistics[profile_method]["reject"], dtype=bool),
                mantel_reject,
            )
            comparison_rows.append(
                {
                    "phase": phase,
                    "dyadic_weight": weight,
                    "node_weight": 1.0 - weight,
                    "profile_method": profile_method,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    **paired,
                }
            )
    return method_rows, comparison_rows


def crossing_interval(
    comparison_rows: list[dict[str, float | int | str]],
    *,
    profile_method: str = "huber_cdelta_star",
) -> tuple[float, float, float]:
    selected = sorted(
        (
            (float(row["dyadic_weight"]), float(row["power_difference"]))
            for row in comparison_rows
            if row["profile_method"] == profile_method
        ),
        key=lambda item: item[0],
    )
    for (left_weight, left_difference), (right_weight, right_difference) in zip(
        selected[:-1], selected[1:]
    ):
        if left_difference == 0.0:
            return left_weight, left_weight, left_weight
        if left_difference * right_difference <= 0.0:
            slope = (right_difference - left_difference) / (
                right_weight - left_weight
            )
            estimate = left_weight - left_difference / slope
            return left_weight, right_weight, float(estimate)
    closest = min(selected, key=lambda item: abs(item[1]))[0]
    return closest, closest, closest


def combine_comparison_runs(
    runs: tuple[list[dict[str, float | int | str]], ...],
    *,
    phase: str = "combined",
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[float, str], dict[str, int]] = {}
    for rows in runs:
        for row in rows:
            key = (float(row["dyadic_weight"]), str(row["profile_method"]))
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
            if cell["n_perm"] != int(row["n_perm"]):
                raise ValueError("cannot combine runs with different n_perm")
            for field in (
                "repetitions",
                "profile_only_rejections",
                "mantel_only_rejections",
                "both_reject",
                "neither_reject",
            ):
                cell[field] += int(row[field])
    output: list[dict[str, float | int | str]] = []
    for (weight, method), cell in sorted(grouped.items()):
        n = cell["repetitions"]
        profile_only = cell["profile_only_rejections"]
        mantel_only = cell["mantel_only_rejections"]
        both = cell["both_reject"]
        neither = cell["neither_reject"]
        difference = (profile_only - mantel_only) / n
        squared_sum = profile_only + mantel_only
        sample_variance = (squared_sum - n * difference**2) / (n - 1)
        standard_error = sqrt(sample_variance / n)
        output.append(
            {
                "phase": phase,
                "dyadic_weight": weight,
                "node_weight": 1.0 - weight,
                "profile_method": method,
                "repetitions": n,
                "n_perm": cell["n_perm"],
                "profile_power": (profile_only + both) / n,
                "mantel_power": (mantel_only + both) / n,
                "power_difference": difference,
                "paired_standard_error": standard_error,
                "paired_ci_low": max(-1.0, difference - 1.96 * standard_error),
                "paired_ci_high": min(1.0, difference + 1.96 * standard_error),
                "profile_only_rejections": profile_only,
                "mantel_only_rejections": mantel_only,
                "both_reject": both,
                "neither_reject": neither,
            }
        )
    return output


def crossover_summary(
    comparison_rows: list[dict[str, float | int | str]],
    *,
    phase: str,
) -> list[dict[str, float | int | str]]:
    rows = []
    for method in (
        "original_l2_cdelta",
        "huber_cdelta_star",
        "huber_cap6_cdelta_star",
    ):
        left, right, estimate = crossing_interval(
            comparison_rows, profile_method=method
        )
        selected = [
            row for row in comparison_rows if row["profile_method"] == method
        ]
        uncertain = [
            float(row["dyadic_weight"])
            for row in selected
            if float(row["paired_ci_low"]) <= 0.0 <= float(row["paired_ci_high"])
        ]
        rows.append(
            {
                "phase": phase,
                "profile_method": method,
                "bracket_low": left,
                "bracket_high": right,
                "linear_crossover_estimate": estimate,
                "zero_difference_ci_band_low": min(uncertain) if uncertain else np.nan,
                "zero_difference_ci_band_high": max(uncertain) if uncertain else np.nan,
                "grid_points": len(selected),
                "repetitions_per_point": int(selected[0]["repetitions"]),
                "n_perm": int(selected[0]["n_perm"]),
            }
        )
    return rows


def _refined_weights(
    comparison_rows: list[dict[str, float | int | str]],
) -> tuple[float, ...]:
    left, right, _ = crossing_interval(comparison_rows)
    lower = max(0.0, left - 0.10)
    upper = min(1.0, right + 0.10)
    count = int(round((upper - lower) / 0.025))
    return tuple(float(round(lower + 0.025 * index, 3)) for index in range(count + 1))


if __name__ == "__main__":
    coarse_weights = tuple(float(value) for value in np.linspace(0.0, 1.0, 11))
    coarse_methods, coarse_comparison = run_mixture_grid(
        coarse_weights,
        repetitions=500,
        n_perm=199,
        seed=20261020,
        phase="coarse",
    )
    write_tsv(
        PROJECT_ROOT / "results" / "node_dyad_mixture_coarse_20260808.tsv",
        coarse_methods,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "node_dyad_mixture_coarse_comparison_20260808.tsv",
        coarse_comparison,
    )
    refined_weights = _refined_weights(coarse_comparison)
    all_summaries = crossover_summary(coarse_comparison, phase="coarse")
    for phase, seed in (("refined", 20261021), ("replication", 20261022)):
        methods, comparison = run_mixture_grid(
            refined_weights,
            repetitions=1200,
            n_perm=399,
            seed=seed,
            phase=phase,
        )
        write_tsv(
            PROJECT_ROOT / "results" / f"node_dyad_mixture_{phase}_20260808.tsv",
            methods,
        )
        write_tsv(
            PROJECT_ROOT
            / "results"
            / f"node_dyad_mixture_{phase}_comparison_20260808.tsv",
            comparison,
        )
        all_summaries.extend(crossover_summary(comparison, phase=phase))
    write_tsv(
        PROJECT_ROOT / "results" / "node_dyad_mixture_crossover_20260808.tsv",
        all_summaries,
    )
