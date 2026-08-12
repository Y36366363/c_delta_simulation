"""Validate adaptive profile/Mantel weighting under unequal buildings."""

from __future__ import annotations

import argparse
from math import exp, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_application_node_decomposition_20260812 import (
    _component_statistics,
    _correlated_normals,
    adaptive_permutation_outcomes,
)
from scripts.run_node_dyad_mixture_20260808 import _fast_within_block_indices
from scripts.run_robust_cdelta_grid import wilson


ROOM_DESIGNS = {
    "balanced": np.asarray((12, 12, 12, 12, 12, 12)),
    "moderately_unequal": np.asarray((6, 8, 10, 12, 16, 20)),
    "severely_unequal": np.asarray((5, 5, 6, 8, 16, 32)),
}
TEMPERATURES = (0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
AGGREGATIONS = ("building_equal", "sqrt_rooms", "room_equal")
SCENARIOS = (
    "conditional_null",
    "radial_node_size_only",
    "radial_node",
    "dyadic",
    "mixed_covariate",
)


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    scale = float(np.std(values))
    if scale == 0.0:
        return np.zeros_like(values)
    return (values - np.mean(values)) / scale


def building_covariates(room_counts: np.ndarray) -> dict[str, np.ndarray]:
    """Return fixed stylized covariates resembling a heterogeneous portfolio."""
    if room_counts.shape != (6,) or np.any(room_counts < 5):
        raise ValueError("room_counts must contain six building sizes of at least five")
    return {
        "log_floor_area": _standardize(np.log(room_counts.astype(float))),
        "age": _standardize(np.asarray((8, 22, 37, 55, 73, 96), dtype=float)),
        "centrality": _standardize(np.asarray((0.2, 0.9, -0.4, 0.5, -1.0, 0.1))),
        "retrofit": np.asarray((1.0, 1.0, 0.0, 1.0, 0.0, 0.0)),
    }


def aggregation_weights(room_counts: np.ndarray, rule: str) -> np.ndarray:
    if rule == "building_equal":
        return np.ones(room_counts.size)
    if rule == "sqrt_rooms":
        return np.sqrt(room_counts.astype(float))
    if rule == "room_equal":
        return room_counts.astype(float)
    raise ValueError(f"unknown aggregation rule: {rule}")


def make_covariate_building_pair(
    rng: np.random.Generator,
    room_counts: np.ndarray,
    scenario: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    """Generate a stylized portfolio with covariate-driven nuisance structure."""
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    covariates = building_covariates(room_counts)
    age = covariates["age"]
    area = covariates["log_floor_area"]
    centrality = covariates["centrality"]
    retrofit = covariates["retrofit"]
    blocks = np.repeat(np.arange(room_counts.size), room_counts)
    x = np.empty(blocks.size)
    y = np.empty(blocks.size)

    residual_center_x, residual_center_y = _correlated_normals(
        rng, room_counts.size, 0.75
    )
    center_x = 0.55 * age + 0.30 * centrality + 0.45 * residual_center_x
    center_y = 0.55 * age + 0.30 * centrality + 0.45 * residual_center_y
    building_scale = np.exp(0.16 * age + 0.12 * area - 0.12 * retrofit)
    prevalence = 1.0 / (1.0 + np.exp(-0.35 * age + 0.15 * centrality))
    magnitude_sigma = 0.60 + 0.12 * age - 0.07 * retrofit
    if scenario == "radial_node_size_only":
        center_x = np.zeros(room_counts.size)
        center_y = np.zeros(room_counts.size)
        building_scale = np.ones(room_counts.size)
        prevalence = np.full(room_counts.size, 0.50)
        magnitude_sigma = np.full(room_counts.size, 0.65)

    realized = {"sign_x": [], "sign_y": [], "radius_product": [], "dyad_product": []}
    for block, count in enumerate(room_counts):
        members = np.flatnonzero(blocks == block)
        signs_x = np.where(rng.random(count) < prevalence[block], 1.0, -1.0)
        signs_y = np.where(rng.random(count) < prevalence[block], 1.0, -1.0)

        if scenario in ("radial_node", "radial_node_size_only"):
            radius_rho, dyad_rho = 0.65, 0.0
        elif scenario == "dyadic":
            radius_rho, dyad_rho = 0.0, 0.65
        elif scenario == "mixed_covariate":
            radius_rho = float(0.30 + 0.25 / (1.0 + exp(-age[block])))
            dyad_rho = float(0.30 + 0.25 / (1.0 + exp(centrality[block])))
        else:
            radius_rho, dyad_rho = 0.0, 0.0

        radius_x, radius_y = _correlated_normals(rng, int(count), radius_rho)
        dyad_x, dyad_y = _correlated_normals(rng, int(count), dyad_rho)
        sigma = float(max(0.25, magnitude_sigma[block]))
        node_x = signs_x * np.exp(sigma * radius_x) / exp(sigma**2)
        node_y = signs_y * np.exp(sigma * radius_y) / exp(sigma**2)
        within_x = sqrt(0.75) * node_x + sqrt(0.25) * dyad_x
        within_y = sqrt(0.75) * node_y + sqrt(0.25) * dyad_y
        x[members] = center_x[block] + building_scale[block] * within_x
        y[members] = center_y[block] + building_scale[block] * within_y
        realized["sign_x"].extend((signs_x > 0.0).tolist())
        realized["sign_y"].extend((signs_y > 0.0).tolist())
        realized["radius_product"].extend((radius_x * radius_y).tolist())
        realized["dyad_product"].extend((dyad_x * dyad_y).tolist())
    return x, y, blocks, {
        "total_rooms": int(np.sum(room_counts)),
        "minimum_rooms": int(np.min(room_counts)),
        "maximum_rooms": int(np.max(room_counts)),
        "size_cv": float(np.std(room_counts) / np.mean(room_counts)),
        "mean_positive_probability": float(
            (np.mean(realized["sign_x"]) + np.mean(realized["sign_y"])) / 2.0
        ),
        "mean_radius_product": float(np.mean(realized["radius_product"])),
        "mean_dyad_product": float(np.mean(realized["dyad_product"])),
        "covariate_center_correlation": (
            float(np.corrcoef(center_x, center_y)[0, 1])
            if np.std(center_x) > 0.0 and np.std(center_y) > 0.0
            else 0.0
        ),
        "scale_ratio": float(np.max(building_scale) / np.min(building_scale)),
    }


def _summaries() -> dict[tuple[float, str, str], dict[str, list[float] | int]]:
    return {
        (temperature, aggregation, method): {"reject": 0, "p": [], "weight": []}
        for temperature in TEMPERATURES
        for aggregation in AGGREGATIONS
        for method in (
            "profile",
            "mantel",
            "nested_max",
            "standardized_max",
            "cv_retrained",
            "cv_standardized",
        )
    }


def run_validation(
    *, repetitions: int, n_perm: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for design, room_counts in ROOM_DESIGNS.items():
        for scenario in SCENARIOS:
            summaries = _summaries()
            diagnostics = []
            for _ in range(repetitions):
                x, y, blocks, diagnostic = make_covariate_building_pair(
                    rng, room_counts, scenario
                )
                diagnostics.append(diagnostic)
                indices = _fast_within_block_indices(blocks, n_perm, rng)
                components = _component_statistics(x, y, blocks, indices)
                for aggregation in AGGREGATIONS:
                    weights = aggregation_weights(room_counts, aggregation)
                    for temperature in TEMPERATURES:
                        outcomes = adaptive_permutation_outcomes(
                            *components,
                            temperature=temperature,
                            block_weights=weights,
                        )
                        for method in (
                            "profile",
                            "mantel",
                            "nested_max",
                            "standardized_max",
                            "cv_retrained",
                            "cv_standardized",
                        ):
                            cell = summaries[(temperature, aggregation, method)]
                            p_value = float(outcomes[f"{method}_p"])
                            cell["reject"] = int(cell["reject"]) + int(p_value < 0.05)
                            cell["p"].append(p_value)
                            weight_key = (
                                "observed_standardized_profile_weight"
                                if method == "cv_standardized"
                                else "observed_profile_weight"
                            )
                            cell["weight"].append(outcomes[weight_key])
            for (temperature, aggregation, method), cell in summaries.items():
                reject = int(cell["reject"])
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "phase": phase,
                        "design": design,
                        "scenario": scenario,
                        "temperature": temperature,
                        "aggregation": aggregation,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                        "median_p_value": float(np.median(cell["p"])),
                        "mean_profile_weight": float(np.mean(cell["weight"])),
                        "sd_profile_weight": float(np.std(cell["weight"])),
                        **{key: float(np.mean([d[key] for d in diagnostics])) for key in diagnostics[0]},
                    }
                )
    return rows


def run_restriction_check(
    *, repetitions: int, n_perm: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    """Compare unrestricted and within-building null calibration."""
    rng = np.random.default_rng(seed)
    room_counts = ROOM_DESIGNS["severely_unequal"]
    summaries = {
        (scheme, method): 0
        for scheme in ("unrestricted", "within_building")
        for method in (
            "profile",
            "mantel",
            "nested_max",
            "standardized_max",
            "cv_retrained",
            "cv_standardized",
        )
    }
    for _ in range(repetitions):
        x, y, blocks, _ = make_covariate_building_pair(
            rng, room_counts, "conditional_null"
        )
        permutation_sets = {
            "unrestricted": np.asarray(
                [rng.permutation(blocks.size) for _ in range(n_perm)]
            ),
            "within_building": _fast_within_block_indices(blocks, n_perm, rng),
        }
        weights = aggregation_weights(room_counts, "building_equal")
        for scheme, indices in permutation_sets.items():
            outcomes = adaptive_permutation_outcomes(
                *_component_statistics(x, y, blocks, indices),
                temperature=4.0,
                block_weights=weights,
            )
            for method in (
                "profile",
                "mantel",
                "nested_max",
                "standardized_max",
                "cv_retrained",
                "cv_standardized",
            ):
                summaries[(scheme, method)] += int(outcomes[f"{method}_p"] < 0.05)
    rows = []
    for (scheme, method), reject in summaries.items():
        low, high = wilson(reject, repetitions)
        rows.append(
            {
                "phase": phase,
                "design": "severely_unequal",
                "scenario": "conditional_null_covariate_confounding",
                "permutation_scheme": scheme,
                "temperature": 4.0,
                "aggregation": "building_equal",
                "method": method,
                "repetitions": repetitions,
                "n_perm": n_perm,
                "rejection_rate": reject / repetitions,
                "wilson_low": low,
                "wilson_high": high,
            }
        )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=("all", "grid", "restriction"), default="all")
    args = parser.parse_args()
    if args.section in ("all", "grid"):
        for phase, seed in (("seed1", 20261301), ("seed2", 20261302)):
            write_tsv(
                PROJECT_ROOT / "results" / f"unequal_building_adaptive_{phase}_20260813.tsv",
                run_validation(repetitions=300, n_perm=199, seed=seed, phase=phase),
            )
    if args.section in ("all", "restriction"):
        for phase, seed in (("seed1", 20261311), ("seed2", 20261312)):
            write_tsv(
                PROJECT_ROOT / "results" / f"unequal_building_restriction_{phase}_20260813.tsv",
                run_restriction_check(
                    repetitions=800, n_perm=199, seed=seed, phase=phase
                ),
            )
