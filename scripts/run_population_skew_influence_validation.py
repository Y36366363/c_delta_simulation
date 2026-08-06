"""Validate the skew-lognormal influence formula at distribution level."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.optimize import brentq
from scipy.stats import norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


MAD_NORMAL_CONSTANT = 1.4826
HUBER_C = 1.345


def _normal_quadrature(order: int = 160) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = hermgauss(order)
    return np.sqrt(2.0) * nodes, weights / np.sqrt(np.pi)


def _lognormal_cdf(value: float, sigma: float) -> float:
    if value <= 0.0:
        return 0.0
    return float(norm.cdf(np.log(value) / sigma))


def _lognormal_pdf(value: float, sigma: float) -> float:
    if value <= 0.0:
        return 0.0
    return float(norm.pdf(np.log(value) / sigma) / (sigma * value))


def _mixture_quantile(
    base_cdf,
    point: float,
    epsilon: float,
    probability: float,
    lower: float,
    upper: float,
) -> float:
    below = (1.0 - epsilon) * base_cdf(point)
    if probability <= below:
        target = probability / (1.0 - epsilon)
        return float(brentq(lambda value: base_cdf(value) - target, lower, point))
    if probability <= below + epsilon:
        return point
    target = (probability - epsilon) / (1.0 - epsilon)
    return float(brentq(lambda value: base_cdf(value) - target, point, upper))


def _marginal_fit(
    sigma: float,
    nodes: np.ndarray,
    weights: np.ndarray,
    *,
    epsilon: float = 0.0,
    point: float = 1.0,
) -> tuple[float, float, float, float]:
    cdf = lambda value: _lognormal_cdf(value, sigma)
    if epsilon == 0.0:
        median = 1.0
    else:
        median = _mixture_quantile(cdf, point, epsilon, 0.5, 1e-10, 1e3)

    radius_cdf = lambda radius: (
        cdf(median + radius) - cdf(max(0.0, median - radius))
    )
    point_radius = abs(point - median)
    if epsilon == 0.0:
        mad = float(brentq(lambda radius: radius_cdf(radius) - 0.5, 0.0, 100.0))
    else:
        mad = _mixture_quantile(
            radius_cdf, point_radius, epsilon, 0.5, 0.0, 100.0
        )
    scale = MAD_NORMAL_CONSTANT * mad
    values = np.exp(sigma * nodes)

    def equation(location: float) -> float:
        base = float(
            np.sum(weights * np.clip((values - location) / scale, -HUBER_C, HUBER_C))
        )
        contamination = float(
            np.clip((point - location) / scale, -HUBER_C, HUBER_C)
        )
        return (1.0 - epsilon) * base + epsilon * contamination

    location = float(brentq(equation, 1e-10, 100.0))
    return median, mad, scale, location


def _population_components(
    sigma: float,
    rho: float,
    nodes: np.ndarray,
    weights: np.ndarray,
    tx: float,
    ty: float,
) -> dict[str, float]:
    u = nodes[:, None]
    v = rho * u + np.sqrt(1.0 - rho**2) * nodes[None, :]
    joint_weights = weights[:, None] * weights[None, :]
    x = np.exp(sigma * u)
    y = np.exp(sigma * v)
    ax, ay = np.abs(x - tx), np.abs(y - ty)
    sign_x, sign_y = np.sign(x - tx), np.sign(y - ty)
    return {
        "mean_x": float(np.sum(joint_weights * ax)),
        "mean_y": float(np.sum(joint_weights * ay)),
        "cross": float(np.sum(joint_weights * ax * ay)),
        "g_x": float(np.sum(joint_weights * sign_x)),
        "g_y": float(np.sum(joint_weights * sign_y)),
        "h_x": float(np.sum(joint_weights * sign_x * ay)),
        "h_y": float(np.sum(joint_weights * ax * sign_y)),
    }


def _location_influence(
    point: float,
    sigma: float,
    nodes: np.ndarray,
    weights: np.ndarray,
    median: float,
    mad: float,
    scale: float,
    location: float,
) -> tuple[float, float]:
    density_median = _lognormal_pdf(median, sigma)
    density_upper = _lognormal_pdf(median + mad, sigma)
    density_lower = _lognormal_pdf(median - mad, sigma)
    median_if = (0.5 - float(point <= median)) / density_median
    mad_if = (
        0.5
        - float(abs(point - median) <= mad)
        - (density_upper - density_lower) * median_if
    ) / (density_upper + density_lower)
    scale_if = MAD_NORMAL_CONSTANT * mad_if
    values = np.exp(sigma * nodes)
    residual = (values - location) / scale
    active = np.abs(residual) < HUBER_C
    sensitivity = float(np.sum(weights * active))
    scale_coupling = float(np.sum(weights * residual * active))
    location_if = (
        scale
        / sensitivity
        * float(np.clip((point - location) / scale, -HUBER_C, HUBER_C))
        - scale_coupling / sensitivity * scale_if
    )
    fixed_scale_if = (
        scale
        / sensitivity
        * float(np.clip((point - location) / scale, -HUBER_C, HUBER_C))
    )
    return location_if, fixed_scale_if


def population_truth(
    *, sigma: float = 0.60, rho: float = 0.40, order: int = 160
) -> dict[str, float]:
    """Return quadrature population c_delta and complete IF variance."""
    nodes, weights = _normal_quadrature(order)
    median, mad, scale, location = _marginal_fit(sigma, nodes, weights)
    components = _population_components(
        sigma, rho, nodes, weights, location, location
    )
    mean_x, mean_y, cross = (
        components["mean_x"], components["mean_y"], components["cross"]
    )
    coefficient = cross / (mean_x * mean_y)
    gamma_x = (
        coefficient * components["g_x"] / mean_x
        - components["h_x"] / (mean_x * mean_y)
    )
    gamma_y = (
        coefficient * components["g_y"] / mean_y
        - components["h_y"] / (mean_x * mean_y)
    )

    u = nodes[:, None]
    v = rho * u + np.sqrt(1.0 - rho**2) * nodes[None, :]
    joint_weights = weights[:, None] * weights[None, :]
    x, y = np.exp(sigma * u), np.exp(sigma * v)

    def location_if(values: np.ndarray) -> np.ndarray:
        density_median = _lognormal_pdf(median, sigma)
        density_upper = _lognormal_pdf(median + mad, sigma)
        density_lower = _lognormal_pdf(median - mad, sigma)
        median_if = (0.5 - (values <= median).astype(float)) / density_median
        mad_if = (
            0.5
            - (np.abs(values - median) <= mad).astype(float)
            - (density_upper - density_lower) * median_if
        ) / (density_upper + density_lower)
        residual = (values - location) / scale
        base_values = np.exp(sigma * nodes)
        base_residual = (base_values - location) / scale
        active = np.abs(base_residual) < HUBER_C
        sensitivity = float(np.sum(weights * active))
        scale_coupling = float(np.sum(weights * base_residual * active))
        return (
            scale / sensitivity * np.clip(residual, -HUBER_C, HUBER_C)
            - scale_coupling / sensitivity * MAD_NORMAL_CONSTANT * mad_if
        )

    ax, ay = np.abs(x - location), np.abs(y - location)
    direct = (
        ax * ay / (mean_x * mean_y)
        - coefficient * ax / mean_x
        - coefficient * ay / mean_y
        + coefficient
    )
    influence = direct + gamma_x * location_if(x) + gamma_y * location_if(y)
    influence_mean = float(np.sum(joint_weights * influence))
    influence_variance = float(
        np.sum(joint_weights * (influence - influence_mean) ** 2)
    )
    return {
        "c_delta": coefficient,
        "influence_variance": influence_variance,
        "huber_location": location,
        "mad": mad,
    }


def run(
    *, sigma: float = 0.60, rho: float = 0.40, order: int = 160
) -> list[dict[str, float | str]]:
    nodes, weights = _normal_quadrature(order)
    fit = _marginal_fit(sigma, nodes, weights)
    median, mad, scale, location = fit
    components = _population_components(
        sigma, rho, nodes, weights, location, location
    )
    mean_x, mean_y, cross = (
        components["mean_x"],
        components["mean_y"],
        components["cross"],
    )
    coefficient = cross / (mean_x * mean_y)
    gamma_x = (
        coefficient * components["g_x"] / mean_x
        - components["h_x"] / (mean_x * mean_y)
    )
    gamma_y = (
        coefficient * components["g_y"] / mean_y
        - components["h_y"] / (mean_x * mean_y)
    )
    quantile = lambda probability: float(np.exp(sigma * norm.ppf(probability)))
    points = {
        "matched_high": (quantile(0.99), quantile(0.99)),
        "unmatched_x_high": (quantile(0.99), quantile(0.60)),
        "central_regular": (quantile(0.55), quantile(0.45)),
        "median_boundary": (1.0, 1.0),
        "low_high": (quantile(0.01), quantile(0.99)),
    }
    rows: list[dict[str, float | str]] = []
    for point_name, (point_x, point_y) in points.items():
        location_if_x, fixed_x = _location_influence(
            point_x, sigma, nodes, weights, *fit
        )
        location_if_y, fixed_y = _location_influence(
            point_y, sigma, nodes, weights, *fit
        )
        direct = (
            abs(point_x - location) * abs(point_y - location) / (mean_x * mean_y)
            - coefficient * abs(point_x - location) / mean_x
            - coefficient * abs(point_y - location) / mean_y
            + coefficient
        )
        analytic = direct + gamma_x * location_if_x + gamma_y * location_if_y
        fixed_scale_analytic = direct + gamma_x * fixed_x + gamma_y * fixed_y
        for epsilon in (1e-6, 1e-5, 1e-4, 5e-4):
            fit_x = _marginal_fit(
                sigma, nodes, weights, epsilon=epsilon, point=point_x
            )
            fit_y = _marginal_fit(
                sigma, nodes, weights, epsilon=epsilon, point=point_y
            )
            contaminated_components = _population_components(
                sigma, rho, nodes, weights, fit_x[3], fit_y[3]
            )
            contaminated_mean_x = (
                (1.0 - epsilon) * contaminated_components["mean_x"]
                + epsilon * abs(point_x - fit_x[3])
            )
            contaminated_mean_y = (
                (1.0 - epsilon) * contaminated_components["mean_y"]
                + epsilon * abs(point_y - fit_y[3])
            )
            contaminated_cross = (
                (1.0 - epsilon) * contaminated_components["cross"]
                + epsilon
                * abs(point_x - fit_x[3])
                * abs(point_y - fit_y[3])
            )
            contaminated_cdelta = contaminated_cross / (
                contaminated_mean_x * contaminated_mean_y
            )
            finite_difference = (contaminated_cdelta - coefficient) / epsilon
            rows.append(
                {
                    "point": point_name,
                    "epsilon": epsilon,
                    "population_cdelta": coefficient,
                    "analytic_influence": analytic,
                    "finite_difference": finite_difference,
                    "absolute_error": abs(finite_difference - analytic),
                    "scaled_error": abs(finite_difference - analytic)
                    / (1.0 + abs(analytic)),
                    "direct_component": direct,
                    "location_component": (
                        gamma_x * location_if_x + gamma_y * location_if_y
                    ),
                    "mad_indirect_component": analytic - fixed_scale_analytic,
                    "huber_location": location,
                    "mad": mad,
                }
            )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "population_skew_influence_validation_20260806.tsv",
        run(),
    )
