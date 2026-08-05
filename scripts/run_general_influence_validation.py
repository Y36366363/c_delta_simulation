"""Numerically validate the general Huber c_delta influence-function path."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


MAD_NORMAL_CONSTANT = 1.4826
HUBER_C = 1.345


def _weighted_quantile(
    values: np.ndarray, weights: np.ndarray, probability: float
) -> float:
    order = np.argsort(values)
    ordered_values, ordered_weights = values[order], weights[order]
    cumulative = np.cumsum(ordered_weights)
    return float(ordered_values[np.searchsorted(cumulative, probability)])


def _weighted_huber_location(
    values: np.ndarray, weights: np.ndarray, scale: float
) -> float:
    location = _weighted_quantile(values, weights, 0.5)
    for _ in range(200):
        residual = (values - location) / scale
        huber_weights = np.minimum(
            1.0, HUBER_C / np.maximum(np.abs(residual), 1e-15)
        )
        updated = float(
            np.sum(weights * huber_weights * values)
            / np.sum(weights * huber_weights)
        )
        if abs(updated - location) < 1e-12 * max(1.0, scale):
            return updated
        location = updated
    return location


def _marginal_fit(
    values: np.ndarray, weights: np.ndarray
) -> dict[str, float | np.ndarray]:
    median = _weighted_quantile(values, weights, 0.5)
    mad = _weighted_quantile(np.abs(values - median), weights, 0.5)
    scale = MAD_NORMAL_CONSTANT * mad
    location = _weighted_huber_location(values, weights, scale)
    return {
        "median": median,
        "mad": mad,
        "scale": scale,
        "location": location,
        "radius": np.abs(values - location),
    }


def _functional(
    x: np.ndarray, y: np.ndarray, weights: np.ndarray
) -> tuple[float, dict[str, float | np.ndarray], dict[str, float | np.ndarray]]:
    fit_x, fit_y = _marginal_fit(x, weights), _marginal_fit(y, weights)
    ax, ay = fit_x["radius"], fit_y["radius"]
    mean_x = float(np.sum(weights * ax))
    mean_y = float(np.sum(weights * ay))
    cross = float(np.sum(weights * ax * ay))
    return cross / (mean_x * mean_y), fit_x, fit_y


def _density_at(values: np.ndarray, point: float) -> float:
    bandwidth = 1.06 * float(np.std(values, ddof=1)) * values.size ** (-0.2)
    standardized = (values - point) / bandwidth
    return float(
        np.mean(np.exp(-0.5 * standardized**2))
        / (np.sqrt(2.0 * np.pi) * bandwidth)
    )


def _location_influence(
    values: np.ndarray,
    fit: dict[str, float | np.ndarray],
    contamination: float,
) -> float:
    median = float(fit["median"])
    mad = float(fit["mad"])
    scale = float(fit["scale"])
    location = float(fit["location"])
    density_median = _density_at(values, median)
    density_upper = _density_at(values, median + mad)
    density_lower = _density_at(values, median - mad)
    median_if = (0.5 - float(contamination <= median)) / density_median
    mad_if = (
        0.5
        - float(abs(contamination - median) <= mad)
        - (density_upper - density_lower) * median_if
    ) / (density_upper + density_lower)
    scale_if = MAD_NORMAL_CONSTANT * mad_if
    residual = (values - location) / scale
    active = np.abs(residual) < HUBER_C
    a_term = float(np.mean(active))
    b_term = float(np.mean(residual * active))
    contamination_residual = (contamination - location) / scale
    psi = float(np.clip(contamination_residual, -HUBER_C, HUBER_C))
    return scale / a_term * psi - b_term / a_term * scale_if


def analytic_influence(
    x: np.ndarray,
    y: np.ndarray,
    fit_x: dict[str, float | np.ndarray],
    fit_y: dict[str, float | np.ndarray],
    contamination_x: float,
    contamination_y: float,
) -> dict[str, float]:
    tx, ty = float(fit_x["location"]), float(fit_y["location"])
    ax, ay = np.abs(x - tx), np.abs(y - ty)
    mean_x, mean_y = float(np.mean(ax)), float(np.mean(ay))
    cross = float(np.mean(ax * ay))
    coefficient = cross / (mean_x * mean_y)
    sign_x, sign_y = np.sign(x - tx), np.sign(y - ty)
    location_if_x = _location_influence(x, fit_x, contamination_x)
    location_if_y = _location_influence(y, fit_y, contamination_y)
    direct = (
        abs(contamination_x - tx) * abs(contamination_y - ty)
        / (mean_x * mean_y)
        - coefficient * abs(contamination_x - tx) / mean_x
        - coefficient * abs(contamination_y - ty) / mean_y
        + coefficient
    )
    gamma_x = (
        coefficient * float(np.mean(sign_x)) / mean_x
        - float(np.mean(sign_x * ay)) / (mean_x * mean_y)
    )
    gamma_y = (
        coefficient * float(np.mean(sign_y)) / mean_y
        - float(np.mean(ax * sign_y)) / (mean_x * mean_y)
    )
    return {
        "analytic_influence": direct
        + gamma_x * location_if_x
        + gamma_y * location_if_y,
        "direct_component": direct,
        "location_component_x": gamma_x * location_if_x,
        "location_component_y": gamma_y * location_if_y,
        "location_if_x": location_if_x,
        "location_if_y": location_if_y,
    }


def _sample(
    rng: np.random.Generator, n: int, scenario: str
) -> tuple[np.ndarray, np.ndarray]:
    rho = 0.4
    u = rng.normal(size=n)
    v = rho * u + np.sqrt(1.0 - rho**2) * rng.normal(size=n)
    if scenario == "symmetric_signed_lognormal":
        return (
            rng.choice((-1.0, 1.0), n) * np.exp(0.45 * u),
            rng.choice((-1.0, 1.0), n) * np.exp(0.45 * v),
        )
    if scenario == "skew_lognormal":
        return np.exp(0.60 * u), np.exp(0.60 * v)
    raise ValueError(scenario)


def run(*, n: int = 300_000, seed: int = 20260916) -> list[dict[str, float | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | str]] = []
    for scenario in ("symmetric_signed_lognormal", "skew_lognormal"):
        x, y = _sample(rng, n, scenario)
        base_weights = np.full(n, 1.0 / n)
        base, fit_x, fit_y = _functional(x, y, base_weights)
        points = {
            "matched_high": (float(np.quantile(x, 0.99)), float(np.quantile(y, 0.99))),
            "unmatched_x_high": (float(np.quantile(x, 0.99)), float(np.median(y))),
            "central": (float(np.median(x)), float(np.median(y))),
            "low_high": (float(np.quantile(x, 0.01)), float(np.quantile(y, 0.99))),
        }
        for point_name, (point_x, point_y) in points.items():
            influence = analytic_influence(
                x, y, fit_x, fit_y, point_x, point_y
            )
            for epsilon in (0.0001, 0.0005, 0.001):
                contaminated_x = np.append(x, point_x)
                contaminated_y = np.append(y, point_y)
                weights = np.append(
                    np.full(n, (1.0 - epsilon) / n), epsilon
                )
                contaminated, _, _ = _functional(
                    contaminated_x, contaminated_y, weights
                )
                finite_difference = (contaminated - base) / epsilon
                analytic = influence["analytic_influence"]
                rows.append(
                    {
                        "scenario": scenario,
                        "point": point_name,
                        "epsilon": epsilon,
                        "base_cdelta": base,
                        "analytic_influence": analytic,
                        "finite_difference": finite_difference,
                        "absolute_error": abs(finite_difference - analytic),
                        "scaled_error": abs(finite_difference - analytic)
                        / (1.0 + abs(analytic)),
                        "direct_component": influence["direct_component"],
                        "location_component_x": influence["location_component_x"],
                        "location_component_y": influence["location_component_y"],
                        "location_if_x": influence["location_if_x"],
                        "location_if_y": influence["location_if_y"],
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "general_influence_validation_20260805.tsv",
        run(),
    )
