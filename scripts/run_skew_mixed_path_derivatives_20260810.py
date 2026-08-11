"""Validate Huber/MAD nuisance derivatives on skew mixed-signal paths."""

from __future__ import annotations

import csv
from math import exp, sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_mixed_path_local_slopes_20260810 import (
    correlation_and_derivative,
    mixture_value_and_tangent,
)
from scripts.run_building_target_separation_20260808 import (
    _profile_statistics,
    mantel_test,
)
from scripts.run_node_dyad_mixture_20260808 import (
    _fast_within_block_indices,
    _paired_difference_summary,
)
from scripts.run_signal_strength_surface_20260809 import COARSE_WEIGHTS


MAD_NORMAL_CONSTANT = 1.4826
HUBER_C = 1.345
CONFIGURATIONS = (
    {
        "name": "moderate_skew",
        "node_rho": 0.55,
        "dyad_rho": 0.70,
        "weight": 0.216,
        "positive_sign_probability": 0.70,
        "node_sigma": 0.55,
        "dyad_sigma": 0.55,
    },
    {
        "name": "strong_skew",
        "node_rho": 0.55,
        "dyad_rho": 0.70,
        "weight": 0.216,
        "positive_sign_probability": 0.80,
        "node_sigma": 0.70,
        "dyad_sigma": 0.80,
    },
)
EPSILONS = (0.0002, 0.0005, 0.001)


def order_statistic_value_derivative(
    values: np.ndarray, derivatives: np.ndarray
) -> tuple[float, float]:
    """Return numpy-median value and its local derivative without ties."""
    order = np.argsort(values)
    n = values.size
    if n % 2:
        index = int(order[n // 2])
        return float(values[index]), float(derivatives[index])
    left, right = int(order[n // 2 - 1]), int(order[n // 2])
    return (
        float((values[left] + values[right]) / 2.0),
        float((derivatives[left] + derivatives[right]) / 2.0),
    )


def huber_transport_fit(
    values: np.ndarray,
    velocities: np.ndarray,
    *,
    huber_c: float = HUBER_C,
) -> dict[str, float]:
    """Return the exact fixed-sample derivative while orderings remain stable."""
    median, median_dot = order_statistic_value_derivative(values, velocities)
    deviations = np.abs(values - median)
    deviation_dots = np.sign(values - median) * (velocities - median_dot)
    mad, mad_dot = order_statistic_value_derivative(deviations, deviation_dots)
    scale = MAD_NORMAL_CONSTANT * mad
    scale_dot = MAD_NORMAL_CONSTANT * mad_dot
    if scale <= 0.0:
        raise ValueError("positive MAD is required")

    location = median
    for _ in range(100):
        residual = (values - location) / scale
        weights = np.minimum(
            1.0, huber_c / np.maximum(np.abs(residual), 1e-15)
        )
        updated = float(np.sum(weights * values) / np.sum(weights))
        if abs(updated - location) < 1e-12 * max(1.0, scale):
            location = updated
            break
        location = updated
    residual = (values - location) / scale
    active = (np.abs(residual) < huber_c).astype(float)
    sensitivity = float(np.mean(active))
    scale_coupling = float(np.mean(residual * active))
    if sensitivity <= 0.0:
        raise ValueError("Huber derivative is undetermined")
    direct_location_dot = float(np.mean(active * velocities) / sensitivity)
    mad_indirect_location_dot = float(
        -scale_coupling / sensitivity * scale_dot
    )
    location_dot = direct_location_dot + mad_indirect_location_dot
    return {
        "median": median,
        "median_dot": median_dot,
        "mad": mad,
        "mad_dot": mad_dot,
        "scale": scale,
        "scale_dot": scale_dot,
        "location": location,
        "location_dot": location_dot,
        "direct_location_dot": direct_location_dot,
        "mad_indirect_location_dot": mad_indirect_location_dot,
        "sensitivity": sensitivity,
        "scale_coupling": scale_coupling,
        "boundary_bandwidth": np.nan,
    }


def _boundary_density_velocity(
    values: np.ndarray,
    velocities: np.ndarray,
    point: float,
    bandwidth: float,
) -> tuple[float, float]:
    standardized = (values - point) / bandwidth
    kernel = np.exp(-0.5 * standardized**2)
    kernel_sum = float(np.sum(kernel))
    if kernel_sum <= 0.0:
        raise ValueError("boundary kernel has zero effective mass")
    density = kernel_sum / (values.size * bandwidth * sqrt(2.0 * np.pi))
    conditional_velocity = float(np.sum(kernel * velocities) / kernel_sum)
    return density, conditional_velocity


def huber_population_transport_fit(
    values: np.ndarray,
    velocities: np.ndarray,
    *,
    huber_c: float = HUBER_C,
    bandwidth_multiplier: float = 1.0,
) -> dict[str, float]:
    """Estimate population transport derivatives at median/MAD boundaries."""
    if bandwidth_multiplier <= 0.0:
        raise ValueError("bandwidth_multiplier must be positive")
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scale = MAD_NORMAL_CONSTANT * mad
    if scale <= 0.0:
        raise ValueError("positive MAD is required")
    bandwidth = float(
        bandwidth_multiplier
        * 1.06
        * np.std(values, ddof=1)
        * values.size ** (-1.0 / 5.0)
    )
    _, median_dot = _boundary_density_velocity(
        values, velocities, median, bandwidth
    )
    density_upper, velocity_upper = _boundary_density_velocity(
        values, velocities, median + mad, bandwidth
    )
    density_lower, velocity_lower = _boundary_density_velocity(
        values, velocities, median - mad, bandwidth
    )
    mad_dot = (
        density_upper * (velocity_upper - median_dot)
        - density_lower * (velocity_lower - median_dot)
    ) / (density_upper + density_lower)
    scale_dot = MAD_NORMAL_CONSTANT * mad_dot

    location = median
    for _ in range(100):
        residual = (values - location) / scale
        weights = np.minimum(
            1.0, huber_c / np.maximum(np.abs(residual), 1e-15)
        )
        updated = float(np.sum(weights * values) / np.sum(weights))
        if abs(updated - location) < 1e-12 * max(1.0, scale):
            location = updated
            break
        location = updated
    residual = (values - location) / scale
    active = (np.abs(residual) < huber_c).astype(float)
    sensitivity = float(np.mean(active))
    scale_coupling = float(np.mean(residual * active))
    direct_location_dot = float(np.mean(active * velocities) / sensitivity)
    mad_indirect_location_dot = float(
        -scale_coupling / sensitivity * scale_dot
    )
    return {
        "median": median,
        "median_dot": median_dot,
        "mad": mad,
        "mad_dot": mad_dot,
        "scale": scale,
        "scale_dot": scale_dot,
        "location": location,
        "location_dot": direct_location_dot + mad_indirect_location_dot,
        "direct_location_dot": direct_location_dot,
        "mad_indirect_location_dot": mad_indirect_location_dot,
        "sensitivity": sensitivity,
        "scale_coupling": scale_coupling,
        "boundary_bandwidth": bandwidth,
    }


def _standardize_signed_lognormal(
    latent: np.ndarray,
    signs: np.ndarray,
    sigma: float,
    positive_probability: float,
    positive_multiplier: float = 1.0,
    negative_multiplier: float = 1.0,
) -> np.ndarray:
    signed_multiplier_mean = (
        positive_probability * positive_multiplier
        - (1.0 - positive_probability) * negative_multiplier
    )
    mean = signed_multiplier_mean * exp(0.5 * sigma**2)
    second_moment = exp(2.0 * sigma**2) * (
        positive_probability * positive_multiplier**2
        + (1.0 - positive_probability) * negative_multiplier**2
    )
    standard_deviation = sqrt(second_moment - mean**2)
    multipliers = np.where(
        signs > 0.0, positive_multiplier, negative_multiplier
    )
    return (signs * multipliers * np.exp(sigma * latent) - mean) / standard_deviation


def _standardize_lognormal(latent: np.ndarray, sigma: float) -> np.ndarray:
    mean = exp(0.5 * sigma**2)
    variance = exp(2.0 * sigma**2) - exp(sigma**2)
    return (np.exp(sigma * latent) - mean) / sqrt(variance)


def skew_components(
    rng: np.random.Generator, size: int, configuration: dict[str, float | str]
) -> tuple[np.ndarray, ...]:
    node_rho = float(configuration["node_rho"])
    dyad_rho = float(configuration["dyad_rho"])
    positive_probability = float(configuration["positive_sign_probability"])
    node_sigma = float(configuration["node_sigma"])
    positive_multiplier = float(configuration.get("positive_radius_multiplier", 1.0))
    negative_multiplier = float(configuration.get("negative_radius_multiplier", 1.0))
    dyad_sigma = float(configuration["dyad_sigma"])
    dyad_distribution = str(configuration.get("dyad_distribution", "lognormal"))

    node_x_latent = rng.normal(size=size)
    node_y_latent = (
        node_rho * node_x_latent
        + sqrt(1.0 - node_rho**2) * rng.normal(size=size)
    )
    sign_x = np.where(rng.random(size) < positive_probability, 1.0, -1.0)
    sign_y = np.where(rng.random(size) < positive_probability, 1.0, -1.0)
    node_x = _standardize_signed_lognormal(
        node_x_latent,
        sign_x,
        node_sigma,
        positive_probability,
        positive_multiplier,
        negative_multiplier,
    )
    node_y = _standardize_signed_lognormal(
        node_y_latent,
        sign_y,
        node_sigma,
        positive_probability,
        positive_multiplier,
        negative_multiplier,
    )

    dyad_x_latent = rng.normal(size=size)
    dyad_y_latent = (
        dyad_rho * dyad_x_latent
        + sqrt(1.0 - dyad_rho**2) * rng.normal(size=size)
    )
    if dyad_distribution == "lognormal":
        dyad_x = _standardize_lognormal(dyad_x_latent, dyad_sigma)
        dyad_y = _standardize_lognormal(dyad_y_latent, dyad_sigma)
    elif dyad_distribution == "gaussian":
        dyad_x, dyad_y = dyad_x_latent, dyad_y_latent
    else:
        raise ValueError("dyad_distribution must be 'gaussian' or 'lognormal'")
    return node_x, node_y, dyad_x, dyad_y


def _sample_standardize(values: np.ndarray) -> np.ndarray:
    centered = values - np.mean(values)
    scale = float(np.std(centered))
    if scale <= 0.0:
        raise ValueError("component is degenerate")
    return centered / scale


def _mix_value(node: np.ndarray, dyad: np.ndarray, weight: float) -> np.ndarray:
    if not 0.0 <= weight <= 1.0:
        raise ValueError("weight must lie in [0, 1]")
    return sqrt(1.0 - weight) * node + sqrt(weight) * dyad


def skew_building_components(
    rng: np.random.Generator,
    configuration: dict[str, float | str],
    *,
    n_blocks: int = 4,
    rooms_per_block: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    blocks = np.repeat(np.arange(n_blocks), rooms_per_block)
    scales = np.geomspace(1.0, 2.5, n_blocks)
    output = [np.empty(blocks.size) for _ in range(4)]
    for block in range(n_blocks):
        members = np.flatnonzero(blocks == block)
        components = skew_components(rng, rooms_per_block, configuration)
        for target, component in zip(output, components):
            target[members] = scales[block] * _sample_standardize(component)
    return output[0], output[1], output[2], output[3], blocks


def run_skew_power_grid(
    weights: tuple[float, ...],
    *,
    repetitions: int,
    n_perm: int,
    seed: int,
    phase: str,
    configurations: tuple[dict[str, float | str], ...] = CONFIGURATIONS,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for configuration in configurations:
        summaries = {
            weight: {"profile": [], "mantel": [], "p_difference": 0.0}
            for weight in weights
        }
        for _ in range(repetitions):
            node_x, node_y, dyad_x, dyad_y, blocks = skew_building_components(
                rng, configuration
            )
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            for weight in weights:
                x = _mix_value(node_x, dyad_x, weight)
                y = _mix_value(node_y, dyad_y, weight)
                profile = _profile_statistics(
                    huber_reference_profile(x), huber_reference_profile(y), indices
                )
                _, profile_p = profile["correlation"]
                _, ratio_p = profile["ratio"]
                _, mantel_p = mantel_test(x, y, indices)
                summaries[weight]["profile"].append(profile_p < 0.05)
                summaries[weight]["mantel"].append(mantel_p < 0.05)
                summaries[weight]["p_difference"] = max(
                    summaries[weight]["p_difference"], abs(profile_p - ratio_p)
                )
        for weight in weights:
            paired = _paired_difference_summary(
                np.asarray(summaries[weight]["profile"], dtype=bool),
                np.asarray(summaries[weight]["mantel"], dtype=bool),
            )
            rows.append(
                {
                    "phase": phase,
                    "configuration": str(configuration["name"]),
                    "node_strength": float(configuration["node_rho"]),
                    "dyad_strength": float(configuration["dyad_rho"]),
                    "dyadic_weight": weight,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    **paired,
                    "maximum_huber_cdelta_pearson_p_difference": summaries[weight]["p_difference"],
                }
            )
    return rows


def combine_skew_power_runs(
    runs: tuple[list[dict[str, float | int | str]], ...],
    *,
    phase: str = "combined",
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, float], dict[str, int]] = {}
    for rows in runs:
        for row in rows:
            key = (str(row["configuration"]), float(row["dyadic_weight"]))
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
    for (configuration, weight), cell in sorted(grouped.items()):
        n = cell["repetitions"]
        profile_only = cell["profile_only_rejections"]
        mantel_only = cell["mantel_only_rejections"]
        both = cell["both_reject"]
        difference = (profile_only - mantel_only) / n
        variance = (profile_only + mantel_only - n * difference**2) / (n - 1)
        standard_error = sqrt(variance / n)
        output.append(
            {
                "phase": phase,
                "configuration": configuration,
                "dyadic_weight": weight,
                "repetitions": n,
                "n_perm": cell["n_perm"],
                "profile_power": (profile_only + both) / n,
                "mantel_power": (mantel_only + both) / n,
                "power_difference": difference,
                "paired_standard_error": standard_error,
                "paired_ci_low": difference - 1.96 * standard_error,
                "paired_ci_high": difference + 1.96 * standard_error,
                **{field: cell[field] for field in (
                    "profile_only_rejections",
                    "mantel_only_rejections",
                    "both_reject",
                    "neither_reject",
                )},
                "maximum_huber_cdelta_pearson_p_difference": 0.0,
            }
        )
    return output


def estimate_skew_crossovers(
    rows: list[dict[str, float | int | str]], phase: str
) -> list[dict[str, float | int | str]]:
    output = []
    for configuration in sorted({str(row["configuration"]) for row in rows}):
        selected = sorted(
            (row for row in rows if str(row["configuration"]) == configuration),
            key=lambda row: float(row["dyadic_weight"]),
        )
        low = high = estimate = np.nan
        for left, right in zip(selected[:-1], selected[1:]):
            dl = float(left["power_difference"])
            dr = float(right["power_difference"])
            if dl == 0.0 or dl * dr <= 0.0:
                low = float(left["dyadic_weight"])
                high = float(right["dyadic_weight"])
                estimate = low if dl == 0.0 else low - dl * (high - low) / (dr - dl)
                break
        uncertain = [
            float(row["dyadic_weight"])
            for row in selected
            if float(row["paired_ci_low"]) <= 0.0 <= float(row["paired_ci_high"])
        ]
        output.append(
            {
                "phase": phase,
                "configuration": configuration,
                "bracket_low": low,
                "bracket_high": high,
                "crossover_estimate": estimate,
                "zero_difference_band_low": min(uncertain) if uncertain else np.nan,
                "zero_difference_band_high": max(uncertain) if uncertain else np.nan,
                "grid_points": len(selected),
                "repetitions_per_point": int(selected[0]["repetitions"]),
                "n_perm": int(selected[0]["n_perm"]),
            }
        )
    return output


def run_skew_power_validation() -> None:
    coarse = run_skew_power_grid(
        COARSE_WEIGHTS,
        repetitions=300,
        n_perm=199,
        seed=20261090,
        phase="coarse",
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_power_coarse_20260810.tsv",
        coarse,
    )
    local_weights = tuple(np.round(np.arange(0.10, 0.301, 0.025), 3))
    local_runs = []
    for phase, seed in (("local_seed1", 20261091), ("local_seed2", 20261092)):
        rows = run_skew_power_grid(
            local_weights,
            repetitions=800,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        local_runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mixed_path_power_{phase}_20260810.tsv",
            rows,
        )
    extension_weights = (0.0, 0.025, 0.05, 0.075, 0.10, 0.125)
    for phase, seed in (
        ("low_weight_seed1", 20261093),
        ("low_weight_seed2", 20261094),
    ):
        rows = run_skew_power_grid(
            extension_weights,
            repetitions=800,
            n_perm=199,
            seed=seed,
            phase=phase,
            configurations=(CONFIGURATIONS[1],),
        )
        local_runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mixed_path_power_{phase}_20260810.tsv",
            rows,
        )
    combined = combine_skew_power_runs(tuple(local_runs))
    crossovers = estimate_skew_crossovers(combined, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_power_combined_20260810.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_power_crossovers_20260810.tsv",
        crossovers,
    )


def continue_skew_power_extension() -> None:
    def read_rows(name: str) -> list[dict[str, str]]:
        with (PROJECT_ROOT / "results" / name).open(
            newline="", encoding="utf-8"
        ) as handle:
            return list(csv.DictReader(handle, delimiter="\t"))

    runs: list[list[dict[str, float | int | str]]] = [
        read_rows(f"skew_mixed_path_power_{phase}_20260810.tsv")  # type: ignore[list-item]
        for phase in ("local_seed1", "local_seed2")
    ]
    extension_weights = (0.0, 0.025, 0.05, 0.075, 0.10, 0.125)
    for phase, seed in (
        ("low_weight_seed1", 20261093),
        ("low_weight_seed2", 20261094),
    ):
        rows = run_skew_power_grid(
            extension_weights,
            repetitions=800,
            n_perm=199,
            seed=seed,
            phase=phase,
            configurations=(CONFIGURATIONS[1],),
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mixed_path_power_{phase}_20260810.tsv",
            rows,
        )
    combined = combine_skew_power_runs(tuple(runs))
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_power_combined_20260810.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_power_crossovers_20260810.tsv",
        estimate_skew_crossovers(combined, "combined"),
    )


def _cdelta_and_derivative(
    radius_x: np.ndarray,
    radius_y: np.ndarray,
    radius_x_dot: np.ndarray,
    radius_y_dot: np.ndarray,
) -> tuple[float, float]:
    mean_x = float(np.mean(radius_x))
    mean_y = float(np.mean(radius_y))
    cross = float(np.mean(radius_x * radius_y))
    mean_x_dot = float(np.mean(radius_x_dot))
    mean_y_dot = float(np.mean(radius_y_dot))
    cross_dot = float(
        np.mean(radius_x_dot * radius_y + radius_x * radius_y_dot)
    )
    coefficient = cross / (mean_x * mean_y)
    derivative = (
        cross_dot / (mean_x * mean_y)
        - coefficient * mean_x_dot / mean_x
        - coefficient * mean_y_dot / mean_y
    )
    return coefficient, derivative


def _profile_effects(
    x: np.ndarray,
    y: np.ndarray,
    x_dot: np.ndarray,
    y_dot: np.ndarray,
    fit_x: dict[str, float],
    fit_y: dict[str, float],
    location_mode: str,
) -> dict[str, tuple[float, float]]:
    if location_mode == "full":
        tx_dot = fit_x["location_dot"]
        ty_dot = fit_y["location_dot"]
    elif location_mode == "no_mad_indirect":
        tx_dot = fit_x["direct_location_dot"]
        ty_dot = fit_y["direct_location_dot"]
    elif location_mode == "fixed_location":
        tx_dot = ty_dot = 0.0
    else:
        raise ValueError(location_mode)
    radius_x = np.abs(x - fit_x["location"])
    radius_y = np.abs(y - fit_y["location"])
    radius_x_dot = np.sign(x - fit_x["location"]) * (x_dot - tx_dot)
    radius_y_dot = np.sign(y - fit_y["location"]) * (y_dot - ty_dot)
    return {
        "profile_correlation": correlation_and_derivative(
            radius_x, radius_y, radius_x_dot, radius_y_dot
        ),
        "cdelta_star": _cdelta_and_derivative(
            radius_x, radius_y, radius_x_dot, radius_y_dot
        ),
    }


def _refit_profile_effects(x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    radius_x = huber_reference_profile(x)
    radius_y = huber_reference_profile(y)
    return {
        "profile_correlation": float(np.corrcoef(radius_x, radius_y)[0, 1]),
        "cdelta_star": float(
            np.mean(radius_x * radius_y)
            / (np.mean(radius_x) * np.mean(radius_y))
        ),
    }


def derivative_batch(
    rng: np.random.Generator,
    size: int,
    configuration: dict[str, float | str],
    epsilons: tuple[float, ...] = EPSILONS,
    bandwidth_multiplier: float = 1.0,
) -> list[dict[str, float | str]]:
    components_1 = skew_components(rng, size, configuration)
    components_2 = skew_components(rng, size, configuration)
    nx, ny, dx, dy = components_1
    nx2, ny2, dx2, dy2 = components_2
    weight = float(configuration["weight"])
    x, x_dot = mixture_value_and_tangent(nx, dx, weight)
    y, y_dot = mixture_value_and_tangent(ny, dy, weight)
    x2, x2_dot = mixture_value_and_tangent(nx2, dx2, weight)
    y2, y2_dot = mixture_value_and_tangent(ny2, dy2, weight)
    fit_x = huber_population_transport_fit(
        x, x_dot, bandwidth_multiplier=bandwidth_multiplier
    )
    fit_y = huber_population_transport_fit(
        y, y_dot, bandwidth_multiplier=bandwidth_multiplier
    )
    effects = {
        mode: _profile_effects(x, y, x_dot, y_dot, fit_x, fit_y, mode)
        for mode in ("full", "no_mad_indirect", "fixed_location")
    }

    delta_x = x - x2
    delta_y = y - y2
    distance_x = np.abs(delta_x)
    distance_y = np.abs(delta_y)
    distance_x_dot = np.sign(delta_x) * (x_dot - x2_dot)
    distance_y_dot = np.sign(delta_y) * (y_dot - y2_dot)
    mantel = correlation_and_derivative(
        distance_x, distance_y, distance_x_dot, distance_y_dot
    )

    rows = []
    for epsilon in epsilons:
        finite = {"profile_correlation": [], "cdelta_star": [], "mantel": []}
        for candidate in (weight - epsilon, weight + epsilon):
            xa, _ = mixture_value_and_tangent(nx, dx, candidate)
            ya, _ = mixture_value_and_tangent(ny, dy, candidate)
            profile = _refit_profile_effects(xa, ya)
            finite["profile_correlation"].append(profile["profile_correlation"])
            finite["cdelta_star"].append(profile["cdelta_star"])
            xb, _ = mixture_value_and_tangent(nx2, dx2, candidate)
            yb, _ = mixture_value_and_tangent(ny2, dy2, candidate)
            finite["mantel"].append(
                float(np.corrcoef(np.abs(xa - xb), np.abs(ya - yb))[0, 1])
            )
        finite_slopes = {
            method: (values[1] - values[0]) / (2.0 * epsilon)
            for method, values in finite.items()
        }
        for method in ("profile_correlation", "cdelta_star"):
            full_effect, full_slope = effects["full"][method]
            no_mad_slope = effects["no_mad_indirect"][method][1]
            fixed_location_slope = effects["fixed_location"][method][1]
            rows.append(
                {
                    "configuration": str(configuration["name"]),
                    "method": method,
                    "epsilon": epsilon,
                    "effect": full_effect,
                    "full_pathwise_slope": full_slope,
                    "complete_refit_finite_slope": finite_slopes[method],
                    "no_mad_indirect_slope": no_mad_slope,
                    "fixed_location_slope": fixed_location_slope,
                    "mad_indirect_effect_component": full_slope - no_mad_slope,
                    "total_location_effect_component": full_slope - fixed_location_slope,
                    "derivative_check_error": finite_slopes[method] - full_slope,
                    "median_dot_x": fit_x["median_dot"],
                    "mad_dot_x": fit_x["mad_dot"],
                    "scale_dot_x": fit_x["scale_dot"],
                    "location_dot_x": fit_x["location_dot"],
                    "direct_location_dot_x": fit_x["direct_location_dot"],
                    "mad_indirect_location_dot_x": fit_x["mad_indirect_location_dot"],
                    "scale_coupling_x": fit_x["scale_coupling"],
                    "boundary_bandwidth_x": fit_x["boundary_bandwidth"],
                    "bandwidth_multiplier": bandwidth_multiplier,
                    "median_dot_y": fit_y["median_dot"],
                    "mad_dot_y": fit_y["mad_dot"],
                    "location_dot_y": fit_y["location_dot"],
                    "mad_indirect_location_dot_y": fit_y["mad_indirect_location_dot"],
                    "sample_size": size,
                }
            )
        rows.append(
            {
                "configuration": str(configuration["name"]),
                "method": "mantel",
                "epsilon": epsilon,
                "effect": mantel[0],
                "full_pathwise_slope": mantel[1],
                "complete_refit_finite_slope": finite_slopes["mantel"],
                "no_mad_indirect_slope": mantel[1],
                "fixed_location_slope": mantel[1],
                "mad_indirect_effect_component": 0.0,
                "total_location_effect_component": 0.0,
                "derivative_check_error": finite_slopes["mantel"] - mantel[1],
                "median_dot_x": fit_x["median_dot"],
                "mad_dot_x": fit_x["mad_dot"],
                "scale_dot_x": fit_x["scale_dot"],
                "location_dot_x": fit_x["location_dot"],
                "direct_location_dot_x": fit_x["direct_location_dot"],
                "mad_indirect_location_dot_x": fit_x["mad_indirect_location_dot"],
                "scale_coupling_x": fit_x["scale_coupling"],
                "boundary_bandwidth_x": fit_x["boundary_bandwidth"],
                "bandwidth_multiplier": bandwidth_multiplier,
                "median_dot_y": fit_y["median_dot"],
                "mad_dot_y": fit_y["mad_dot"],
                "location_dot_y": fit_y["location_dot"],
                "mad_indirect_location_dot_y": fit_y["mad_indirect_location_dot"],
                "sample_size": size,
            }
        )
    return rows


def run_seed(
    *, seed: int, n_batches: int = 10, batch_size: int = 100_000
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for configuration in CONFIGURATIONS:
        for batch in range(n_batches):
            for row in derivative_batch(rng, batch_size, configuration):
                rows.append({"seed": seed, "batch": batch, **row})
    return rows


def summarize(
    raw_rows: list[dict[str, float | int | str]], phase: str
) -> list[dict[str, float | int | str]]:
    output = []
    keys = sorted(
        {
            (
                str(row["configuration"]),
                str(row["method"]),
                float(row["epsilon"]),
                float(row["bandwidth_multiplier"]),
                int(row["sample_size"]),
            )
            for row in raw_rows
        }
    )
    numeric_fields = (
        "effect",
        "full_pathwise_slope",
        "complete_refit_finite_slope",
        "no_mad_indirect_slope",
        "fixed_location_slope",
        "mad_indirect_effect_component",
        "total_location_effect_component",
        "derivative_check_error",
        "median_dot_x",
        "mad_dot_x",
        "scale_dot_x",
        "location_dot_x",
        "direct_location_dot_x",
        "mad_indirect_location_dot_x",
        "scale_coupling_x",
        "boundary_bandwidth_x",
        "median_dot_y",
        "mad_dot_y",
        "location_dot_y",
        "mad_indirect_location_dot_y",
    )
    for configuration, method, epsilon, bandwidth_multiplier, sample_size in keys:
        selected = [
            row
            for row in raw_rows
            if str(row["configuration"]) == configuration
            and str(row["method"]) == method
            and float(row["epsilon"]) == epsilon
            and float(row["bandwidth_multiplier"]) == bandwidth_multiplier
            and int(row["sample_size"]) == sample_size
        ]
        result: dict[str, float | int | str] = {
            "phase": phase,
            "configuration": configuration,
            "method": method,
            "epsilon": epsilon,
            "bandwidth_multiplier": bandwidth_multiplier,
            "batches": len(selected),
            "batch_size": sample_size,
            "total_observations": len(selected) * sample_size,
        }
        for field in numeric_fields:
            values = np.asarray([float(row[field]) for row in selected])
            result[field] = float(np.mean(values))
            result[f"{field}_se"] = float(
                np.std(values, ddof=1) / sqrt(values.size)
            )
        result["absolute_mean_derivative_check_error"] = abs(
            float(result["derivative_check_error"])
        )
        output.append(result)
    return output


def run_sensitivity() -> list[dict[str, float | int | str]]:
    rows = []
    for configuration_index, configuration in enumerate(CONFIGURATIONS):
        for sample_size in (100_000, 400_000):
            for batch in range(6):
                seed = (
                    20261100
                    + 10_000 * configuration_index
                    + sample_size
                    + batch
                )
                for bandwidth_multiplier in (0.75, 1.0, 1.25):
                    batch_rows = derivative_batch(
                        np.random.default_rng(seed),
                        sample_size,
                        configuration,
                        epsilons=(0.0005,),
                        bandwidth_multiplier=bandwidth_multiplier,
                    )
                    for row in batch_rows:
                        rows.append({"seed": seed, "batch": batch, **row})
    return summarize(rows, "sensitivity")


def run() -> None:
    all_rows = []
    for label, seed in (("seed1", 20261070), ("seed2", 20261071)):
        rows = run_seed(seed=seed)
        all_rows.extend(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mixed_path_derivatives_{label}_20260810.tsv",
            summarize(rows, label),
        )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_derivatives_combined_20260810.tsv",
        summarize(all_rows, "combined"),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_derivative_sensitivity_20260810.tsv",
        run_sensitivity(),
    )
    high_precision = run_seed(
        seed=20261080, n_batches=8, batch_size=500_000
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mixed_path_derivatives_high_precision_20260810.tsv",
        summarize(high_precision, "high_precision"),
    )
    run_skew_power_validation()


if __name__ == "__main__":
    run()
