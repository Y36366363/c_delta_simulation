"""Derive and simulate local effect and power slopes on mixed signal paths."""

from __future__ import annotations

from math import exp, pi, sqrt
from pathlib import Path
from statistics import NormalDist
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
    _fast_within_block_indices,
)
from scripts.run_signal_strength_surface_20260809 import (
    _building_components,
    _mix_components,
)
from scripts.run_pure_path_approximation_20260809 import run as run_pure_paths


LOG_RADIUS_SIGMA = 0.55
CONFIGURATIONS = (
    ("default", 0.55, 0.70, 0.216),
    ("weak_both", 0.35, 0.30, 0.225),
    ("strong_node_low_dyad", 0.65, 0.30, 0.362),
    ("balanced_strong", 0.65, 0.65, 0.258),
)
LOCAL_OFFSETS = (-0.05, -0.025, 0.0, 0.025, 0.05)


def mixture_value_and_tangent(
    node: np.ndarray, dyad: np.ndarray, weight: float
) -> tuple[np.ndarray, np.ndarray]:
    """Return sqrt-variance mixture and its pathwise derivative in weight."""
    if not 0.0 < weight < 1.0:
        raise ValueError("local tangent requires weight strictly between zero and one")
    node_scale = sqrt(1.0 - weight)
    dyad_scale = sqrt(weight)
    value = node_scale * node + dyad_scale * dyad
    tangent = -node / (2.0 * node_scale) + dyad / (2.0 * dyad_scale)
    return value, tangent


def correlation_and_derivative(
    x: np.ndarray,
    y: np.ndarray,
    x_dot: np.ndarray,
    y_dot: np.ndarray,
) -> tuple[float, float]:
    """Correlation and its derivative for differentiable paired paths."""
    xc = x - np.mean(x)
    yc = y - np.mean(y)
    xdc = x_dot - np.mean(x_dot)
    ydc = y_dot - np.mean(y_dot)
    covariance = float(np.mean(xc * yc))
    variance_x = float(np.mean(xc**2))
    variance_y = float(np.mean(yc**2))
    covariance_dot = float(np.mean(xdc * yc + xc * ydc))
    variance_x_dot = float(2.0 * np.mean(xc * xdc))
    variance_y_dot = float(2.0 * np.mean(yc * ydc))
    correlation = covariance / sqrt(variance_x * variance_y)
    derivative = correlation * (
        covariance_dot / covariance
        - 0.5 * variance_x_dot / variance_x
        - 0.5 * variance_y_dot / variance_y
    ) if covariance != 0.0 else covariance_dot / sqrt(variance_x * variance_y)
    return float(correlation), float(derivative)


def _population_components(
    rng: np.random.Generator,
    size: int,
    node_rho: float,
    dyad_rho: float,
) -> tuple[np.ndarray, ...]:
    u = rng.normal(size=size)
    v = rng.normal(size=size)
    radius_x = np.exp(LOG_RADIUS_SIGMA * u)
    radius_y = np.exp(
        LOG_RADIUS_SIGMA
        * (node_rho * u + sqrt(1.0 - node_rho**2) * v)
    )
    node_sd = exp(LOG_RADIUS_SIGMA**2)
    node_x = rng.choice((-1.0, 1.0), size=size) * radius_x / node_sd
    node_y = rng.choice((-1.0, 1.0), size=size) * radius_y / node_sd
    dyad_x = rng.normal(size=size)
    dyad_y = (
        dyad_rho * dyad_x
        + sqrt(1.0 - dyad_rho**2) * rng.normal(size=size)
    )
    return node_x, node_y, dyad_x, dyad_y


def _population_batch(
    rng: np.random.Generator,
    size: int,
    node_rho: float,
    dyad_rho: float,
    weight: float,
    epsilon: float,
) -> dict[str, tuple[float, float, float]]:
    first = _population_components(rng, size, node_rho, dyad_rho)
    second = _population_components(rng, size, node_rho, dyad_rho)
    nx1, ny1, dx1, dy1 = first
    nx2, ny2, dx2, dy2 = second
    x1, x1_dot = mixture_value_and_tangent(nx1, dx1, weight)
    y1, y1_dot = mixture_value_and_tangent(ny1, dy1, weight)
    x2, x2_dot = mixture_value_and_tangent(nx2, dx2, weight)
    y2, y2_dot = mixture_value_and_tangent(ny2, dy2, weight)

    radius_x = np.abs(x1)
    radius_y = np.abs(y1)
    radius_x_dot = np.sign(x1) * x1_dot
    radius_y_dot = np.sign(y1) * y1_dot
    profile, profile_dot = correlation_and_derivative(
        radius_x, radius_y, radius_x_dot, radius_y_dot
    )

    delta_x = x1 - x2
    delta_y = y1 - y2
    distance_x = np.abs(delta_x)
    distance_y = np.abs(delta_y)
    distance_x_dot = np.sign(delta_x) * (x1_dot - x2_dot)
    distance_y_dot = np.sign(delta_y) * (y1_dot - y2_dot)
    mantel, mantel_dot = correlation_and_derivative(
        distance_x, distance_y, distance_x_dot, distance_y_dot
    )

    finite = {}
    for method in ("profile", "mantel"):
        values = []
        for candidate in (weight - epsilon, weight + epsilon):
            xa, _ = mixture_value_and_tangent(nx1, dx1, candidate)
            ya, _ = mixture_value_and_tangent(ny1, dy1, candidate)
            if method == "profile":
                left, right = np.abs(xa), np.abs(ya)
            else:
                xb, _ = mixture_value_and_tangent(nx2, dx2, candidate)
                yb, _ = mixture_value_and_tangent(ny2, dy2, candidate)
                left, right = np.abs(xa - xb), np.abs(ya - yb)
            values.append(float(np.corrcoef(left, right)[0, 1]))
        finite[method] = (values[1] - values[0]) / (2.0 * epsilon)
    return {
        "profile": (profile, profile_dot, finite["profile"]),
        "mantel": (mantel, mantel_dot, finite["mantel"]),
    }


def run_population_slopes(
    *,
    n_batches: int = 20,
    batch_size: int = 50_000,
    epsilon: float = 0.001,
    seed: int = 20261060,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for name, node_rho, dyad_rho, center in CONFIGURATIONS:
        estimates = {"profile": [], "mantel": []}
        for _ in range(n_batches):
            batch = _population_batch(
                rng, batch_size, node_rho, dyad_rho, center, epsilon
            )
            for method in estimates:
                estimates[method].append(batch[method])
        for method, values in estimates.items():
            array = np.asarray(values)
            mean = np.mean(array, axis=0)
            se = np.std(array, axis=0, ddof=1) / sqrt(n_batches)
            rows.append(
                {
                    "configuration": name,
                    "node_strength": node_rho,
                    "dyad_strength": dyad_rho,
                    "center_weight": center,
                    "method": method,
                    "population_effect": float(mean[0]),
                    "pathwise_effect_slope": float(mean[1]),
                    "pathwise_effect_slope_se": float(se[1]),
                    "finite_difference_effect_slope": float(mean[2]),
                    "finite_difference_effect_slope_se": float(se[2]),
                    "absolute_derivative_check_error": abs(float(mean[1] - mean[2])),
                    "finite_difference_epsilon": epsilon,
                    "n_batches": n_batches,
                    "batch_size": batch_size,
                    "total_dyads": n_batches * batch_size,
                }
            )
    return rows


def simulate_power_phase(
    *, repetitions: int, n_perm: int, seed: int
) -> dict[str, dict[str, np.ndarray]]:
    rng = np.random.default_rng(seed)
    output = {}
    for name, node_rho, dyad_rho, center in CONFIGURATIONS:
        weights = np.asarray([center + offset for offset in LOCAL_OFFSETS])
        statistics = {
            "profile": np.empty((repetitions, weights.size)),
            "mantel": np.empty((repetitions, weights.size)),
        }
        rejections = {
            "profile": np.empty((repetitions, weights.size), dtype=bool),
            "mantel": np.empty((repetitions, weights.size), dtype=bool),
        }
        for repetition in range(repetitions):
            node_x, node_y, dyad_x, dyad_y, blocks = _building_components(
                rng, node_rho, dyad_rho
            )
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            components = (node_x, node_y, dyad_x, dyad_y)
            for column, weight in enumerate(weights):
                x, y = _mix_components(components, float(weight))
                profile = _profile_statistics(
                    huber_reference_profile(x), huber_reference_profile(y), indices
                )
                profile_statistic, profile_p = profile["correlation"]
                _, ratio_p = profile["ratio"]
                if abs(profile_p - ratio_p) > 1e-12:
                    raise AssertionError("profile ratio and correlation p-values differ")
                mantel_statistic, mantel_p = mantel_test(x, y, indices)
                statistics["profile"][repetition, column] = profile_statistic
                statistics["mantel"][repetition, column] = mantel_statistic
                rejections["profile"][repetition, column] = profile_p < 0.05
                rejections["mantel"][repetition, column] = mantel_p < 0.05
        output[name] = {
            "weights": weights,
            "profile_statistics": statistics["profile"],
            "mantel_statistics": statistics["mantel"],
            "profile_rejections": rejections["profile"],
            "mantel_rejections": rejections["mantel"],
        }
    return output


def _probit_power_slope(power: np.ndarray, minus: int, center: int, plus: int, h: float, n: int) -> float:
    adjusted = np.clip(power, 0.5 / n, 1.0 - 0.5 / n)
    normal = NormalDist()
    q_minus = normal.inv_cdf(float(adjusted[minus]))
    q_center = normal.inv_cdf(float(adjusted[center]))
    q_plus = normal.inv_cdf(float(adjusted[plus]))
    q_slope = (q_plus - q_minus) / (2.0 * h)
    return exp(-0.5 * q_center**2) / sqrt(2.0 * pi) * q_slope


def summarize_power_slopes(
    phases: tuple[dict[str, dict[str, np.ndarray]], ...], phase: str
) -> list[dict[str, float | int | str]]:
    rows = []
    for name, node_rho, dyad_rho, center_weight in CONFIGURATIONS:
        weights = phases[0][name]["weights"]
        combined = {}
        for method in ("profile", "mantel"):
            combined[f"{method}_statistics"] = np.concatenate(
                tuple(run[name][f"{method}_statistics"] for run in phases), axis=0
            )
            combined[f"{method}_rejections"] = np.concatenate(
                tuple(run[name][f"{method}_rejections"] for run in phases), axis=0
            )
        methods = {
            "profile": (
                combined["profile_statistics"],
                combined["profile_rejections"].astype(float),
            ),
            "mantel": (
                combined["mantel_statistics"],
                combined["mantel_rejections"].astype(float),
            ),
            "profile_minus_mantel": (
                combined["profile_statistics"] - combined["mantel_statistics"],
                combined["profile_rejections"].astype(float)
                - combined["mantel_rejections"].astype(float),
            ),
        }
        repetitions = methods["profile"][0].shape[0]
        for h, minus, plus in ((0.025, 1, 3), (0.05, 0, 4)):
            for method, (statistics, rejection) in methods.items():
                statistic_slopes = (statistics[:, plus] - statistics[:, minus]) / (2.0 * h)
                power_slopes = (rejection[:, plus] - rejection[:, minus]) / (2.0 * h)
                powers = np.mean(rejection, axis=0)
                rows.append(
                    {
                        "phase": phase,
                        "configuration": name,
                        "node_strength": node_rho,
                        "dyad_strength": dyad_rho,
                        "center_weight": center_weight,
                        "method": method,
                        "half_width": h,
                        "repetitions": repetitions,
                        "n_perm": 199,
                        "mean_statistic_at_center": float(np.mean(statistics[:, 2])),
                        "statistic_slope": float(np.mean(statistic_slopes)),
                        "statistic_slope_se": float(np.std(statistic_slopes, ddof=1) / sqrt(repetitions)),
                        "power_minus": float(powers[minus]),
                        "power_center": float(powers[2]),
                        "power_plus": float(powers[plus]),
                        "power_slope": float(np.mean(power_slopes)),
                        "power_slope_se": float(np.std(power_slopes, ddof=1) / sqrt(repetitions)),
                        "probit_power_slope": (
                            _probit_power_slope(powers, minus, 2, plus, h, repetitions)
                            if method != "profile_minus_mantel"
                            else np.nan
                        ),
                    }
                )
    return rows


def run() -> None:
    write_tsv(
        PROJECT_ROOT / "results" / "pure_path_population_replication_20260810.tsv",
        run_pure_paths(seed=20261064),
    )
    population = run_population_slopes()
    write_tsv(
        PROJECT_ROOT / "results" / "mixed_path_population_slopes_20260810.tsv",
        population,
    )
    phase_specs = (("slope_seed1", 20261061), ("slope_seed2", 20261062))
    simulated = []
    for phase, seed in phase_specs:
        result = simulate_power_phase(repetitions=800, n_perm=199, seed=seed)
        simulated.append(result)
        write_tsv(
            PROJECT_ROOT / "results" / f"mixed_path_power_slopes_{phase}_20260810.tsv",
            summarize_power_slopes((result,), phase),
        )
    write_tsv(
        PROJECT_ROOT / "results" / "mixed_path_power_slopes_combined_20260810.tsv",
        summarize_power_slopes(tuple(simulated), "combined"),
    )


if __name__ == "__main__":
    run()
