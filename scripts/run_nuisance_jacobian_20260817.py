"""Numerically evaluate the complete median/MAD/Huber nuisance Jacobian."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import lognorm, norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_bridge_family_validation_20260817 import BRIDGE_FAMILIES


RESULTS_DIR = PROJECT_ROOT / "results"
HUBER_C = 1.345
MAD_NORMAL_CONSTANT = 1.4826


def bridge_pdf(radius: float, family: str) -> float:
    if radius < 0.0:
        return 0.0
    if family == "uniform":
        return 1.0 if radius <= 1.0 else 0.0
    if family == "exponential":
        return float(np.exp(-radius))
    if family == "half_normal":
        scale = np.sqrt(2.0 / np.pi)
        return float(2.0 * norm.pdf(radius / scale) / scale)
    if family == "scaled_beta12":
        return float(1.0 - radius / 2.0) if radius <= 2.0 else 0.0
    raise ValueError(f"unknown bridge family: {family}")


def bridge_cdf(radius: float, family: str) -> float:
    if radius <= 0.0:
        return 0.0
    if family == "uniform":
        return min(radius, 1.0)
    if family == "exponential":
        return float(1.0 - np.exp(-radius))
    if family == "half_normal":
        scale = np.sqrt(2.0 / np.pi)
        return float(2.0 * norm.cdf(radius / scale) - 1.0)
    if family == "scaled_beta12":
        if radius >= 2.0:
            return 1.0
        return float(1.0 - (1.0 - radius / 2.0) ** 2)
    raise ValueError(f"unknown bridge family: {family}")


@dataclass(frozen=True)
class PopulationDistribution:
    name: str
    pdf: object
    cdf: object
    lower: float
    upper: float


def symmetric_bridge_distribution(
    bridge_probability: float, family: str, radial_log_sd: float = 0.10
) -> PopulationDistribution:
    radial = lognorm(s=radial_log_sd, scale=1.0)

    def radius_pdf(radius: float) -> float:
        return float(
            (1.0 - bridge_probability) * radial.pdf(radius)
            + bridge_probability * bridge_pdf(radius, family)
        )

    def radius_cdf(radius: float) -> float:
        return float(
            (1.0 - bridge_probability) * radial.cdf(radius)
            + bridge_probability * bridge_cdf(radius, family)
        )

    def pdf(value: float) -> float:
        if value == 0.0:
            return bridge_probability / 2.0
        return 0.5 * radius_pdf(abs(value))

    def cdf(value: float) -> float:
        if value < 0.0:
            return 0.5 * (1.0 - radius_cdf(-value))
        return 0.5 + 0.5 * radius_cdf(value)

    return PopulationDistribution(
        name=f"{family}_epsilon_{bridge_probability:g}",
        pdf=pdf,
        cdf=cdf,
        lower=-np.inf,
        upper=np.inf,
    )


def skew_lognormal_distribution(sigma: float = 1.10) -> PopulationDistribution:
    distribution = lognorm(s=sigma, scale=1.0)
    return PopulationDistribution(
        name=f"skew_lognormal_{sigma:g}",
        pdf=lambda value: float(distribution.pdf(value)),
        cdf=lambda value: float(distribution.cdf(value)),
        lower=0.0,
        upper=np.inf,
    )


def expectation(
    distribution: PopulationDistribution, function: object
) -> float:
    value, _ = quad(
        lambda x: float(function(x)) * float(distribution.pdf(x)),
        distribution.lower,
        distribution.upper,
        epsabs=2e-10,
        epsrel=2e-10,
        limit=300,
        points=None,
    )
    return float(value)


def population_nuisance(
    distribution: PopulationDistribution,
    *,
    huber_c: float = HUBER_C,
    mad_constant: float = MAD_NORMAL_CONSTANT,
) -> dict[str, float | str | np.ndarray]:
    """Return nuisance solution, analytic Jacobian, and finite-difference check."""
    median = brentq(lambda x: float(distribution.cdf(x)) - 0.5, -20.0, 20.0)

    def mad_equation(distance: float) -> float:
        return (
            float(distribution.cdf(median + distance))
            - float(distribution.cdf(median - distance))
            - 0.5
        )

    mad = brentq(mad_equation, 1e-10, 50.0)
    scale = mad_constant * mad

    def huber_equation(location: float, scale_value: float = scale) -> float:
        return expectation(
            distribution,
            lambda x: np.clip((x - location) / scale_value, -huber_c, huber_c),
        )

    location = brentq(lambda value: huber_equation(value), -20.0, 50.0)
    lower_knot = location - huber_c * scale
    upper_knot = location + huber_c * scale
    active_probability = float(
        distribution.cdf(upper_knot) - distribution.cdf(lower_knot)
    )
    scale_coupling = expectation(
        distribution,
        lambda x: (
            (x - location) / scale
            if lower_knot < x < upper_knot
            else 0.0
        ),
    )
    density_median = float(distribution.pdf(median))
    density_lower = float(distribution.pdf(median - mad))
    density_upper = float(distribution.pdf(median + mad))

    jacobian = np.array(
        [
            [mad * density_median, 0.0, 0.0],
            [
                mad * (density_upper - density_lower),
                mad * (density_upper + density_lower),
                0.0,
            ],
            [0.0, -scale_coupling, -active_probability / mad_constant],
        ]
    )

    def equations(normalized: np.ndarray) -> np.ndarray:
        candidate_median = median + mad * normalized[0]
        candidate_mad = mad * normalized[1]
        candidate_location = location + mad * normalized[2]
        candidate_scale = mad_constant * candidate_mad
        return np.array(
            [
                float(distribution.cdf(candidate_median)) - 0.5,
                float(distribution.cdf(candidate_median + candidate_mad))
                - float(distribution.cdf(candidate_median - candidate_mad))
                - 0.5,
                huber_equation(candidate_location, candidate_scale),
            ]
        )

    point = np.array([0.0, 1.0, 0.0])
    # A 1e-4 standardized step balances quadrature noise against O(h^2)
    # central-difference error near the clipped-score knots.
    step = 1e-4
    numerical = np.column_stack(
        [
            (equations(point + step * np.eye(3)[index])
             - equations(point - step * np.eye(3)[index]))
            / (2.0 * step)
            for index in range(3)
        ]
    )
    singular_values = np.linalg.svd(jacobian, compute_uv=False)
    inverse_jacobian = np.linalg.inv(jacobian)
    return {
        "scenario": distribution.name,
        "median": median,
        "mad": mad,
        "scale": scale,
        "huber_location": location,
        "density_median": density_median,
        "density_lower_mad": density_lower,
        "density_upper_mad": density_upper,
        "standardized_median_density": mad * density_median,
        "standardized_mad_density_sum": mad * (density_upper + density_lower),
        "standardized_mad_density_difference": mad * (density_upper - density_lower),
        "huber_active_probability": active_probability,
        "huber_scale_coupling": scale_coupling,
        "huber_location_curvature": active_probability / mad_constant,
        "minimum_singular_value": float(np.min(singular_values)),
        "maximum_singular_value": float(np.max(singular_values)),
        "jacobian_condition_number": float(np.max(singular_values) / np.min(singular_values)),
        "inverse_jacobian_norm": float(1.0 / np.min(singular_values)),
        "jacobian_determinant": float(np.linalg.det(jacobian)),
        "sqrt80_minimum_singular_value": float(np.sqrt(80.0) * np.min(singular_values)),
        "sqrt320_minimum_singular_value": float(np.sqrt(320.0) * np.min(singular_values)),
        "finite_difference_max_error": float(np.max(np.abs(jacobian - numerical))),
        "jacobian": jacobian,
        "inverse_jacobian": inverse_jacobian,
        "numerical_jacobian": numerical,
    }


def flatten_result(result: dict[str, float | str | np.ndarray]) -> dict[str, float | str]:
    row = {
        key: value
        for key, value in result.items()
        if key not in {"jacobian", "inverse_jacobian", "numerical_jacobian"}
    }
    jacobian = np.asarray(result["jacobian"])
    for row_index, label_row in enumerate(("median", "mad", "huber")):
        for column_index, label_column in enumerate(("median", "mad", "huber")):
            row[f"jacobian_{label_row}_{label_column}"] = float(
                jacobian[row_index, column_index]
            )
    inverse = np.asarray(result["inverse_jacobian"])
    for row_index, label_row in enumerate(("median", "mad", "huber")):
        for column_index, label_column in enumerate(("median", "mad", "huber")):
            row[f"inverse_{label_row}_{label_column}"] = float(
                inverse[row_index, column_index]
            )
    return row  # type: ignore[return-value]


def main() -> None:
    rows = []
    for bridge_probability in (0.05, 0.10, 0.20):
        for family in BRIDGE_FAMILIES:
            rows.append(
                flatten_result(
                    population_nuisance(
                        symmetric_bridge_distribution(bridge_probability, family)
                    )
                )
            )
    rows.append(flatten_result(population_nuisance(skew_lognormal_distribution())))
    output = RESULTS_DIR / "nuisance_jacobian_population_20260817.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
