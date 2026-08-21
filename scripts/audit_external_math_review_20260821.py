"""Numerical safeguards for the external appendix mathematics review."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.stats import norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.audit_mad_convention_20260820 import lower_empirical_median
from scripts.robust_extension_utils import write_tsv
from scripts.run_population_skew_influence_validation import (
    _lognormal_pdf,
    _marginal_fit,
    _normal_quadrature,
)


OUTPUT = PROJECT_ROOT / "results" / "external_math_review_checks_20260821.tsv"
SEED = 20260821


def midpoint_mad_bound_max_violation(
    *, seed: int = SEED, repetitions: int = 2000, n: int = 80
) -> float:
    """Check the exact deterministic decomposition behind convention comparison."""
    rng = np.random.default_rng(seed)
    samples = rng.lognormal(mean=0.0, sigma=1.1, size=(repetitions, n))
    midpoint_centres = np.median(samples, axis=1)
    lower_centres = lower_empirical_median(samples, axis=1)
    midpoint_mads = np.median(
        np.abs(samples - midpoint_centres[:, None]), axis=1
    )
    lower_deviations = np.abs(samples - lower_centres[:, None])
    lower_mads = lower_empirical_median(lower_deviations, axis=1)
    ordered_lower_deviations = np.sort(lower_deviations, axis=1)
    r = n // 2
    central_deviation_half_spacing = 0.5 * (
        ordered_lower_deviations[:, r] - ordered_lower_deviations[:, r - 1]
    )
    bound = (
        np.abs(midpoint_centres - lower_centres)
        + central_deviation_half_spacing
    )
    return float(np.max(np.abs(midpoint_mads - lower_mads) - bound))


def skew_mad_influence_check(
    *, sigma: float = 0.6, epsilon: float = 1e-6, order: int = 160
) -> tuple[float, float, float, float]:
    """Compare the asymmetric-density sign with a population contamination path."""
    nodes, weights = _normal_quadrature(order)
    point = float(np.exp(sigma * norm.ppf(0.99)))
    median, mad, _, _ = _marginal_fit(sigma, nodes, weights)
    density_median = _lognormal_pdf(median, sigma)
    density_upper = _lognormal_pdf(median + mad, sigma)
    density_lower = _lognormal_pdf(median - mad, sigma)
    median_if = (0.5 - float(point <= median)) / density_median
    direct = 0.5 - float(abs(point - median) <= mad)
    analytic = (
        direct - (density_upper - density_lower) * median_if
    ) / (density_upper + density_lower)
    reversed_sign = (
        direct + (density_upper - density_lower) * median_if
    ) / (density_upper + density_lower)
    contaminated_mad = _marginal_fit(
        sigma, nodes, weights, epsilon=epsilon, point=point
    )[1]
    finite_difference = (contaminated_mad - mad) / epsilon
    return (
        analytic,
        finite_difference,
        abs(analytic - finite_difference),
        abs(reversed_sign - finite_difference),
    )


def sign_radius_piecewise_max_error(
    *, seed: int = SEED, repetitions: int = 10000
) -> float:
    """Verify the four affine pieces used in the VC-subgraph decomposition."""
    rng = np.random.default_rng(seed)
    x = rng.normal(size=repetitions)
    y = rng.normal(size=repetitions)
    tx, ty = 0.3, -0.4
    direct = np.sign(x - tx) * np.abs(y - ty)
    piecewise = np.empty_like(direct)
    right = x >= tx
    above = y >= ty
    piecewise[right & above] = y[right & above] - ty
    piecewise[right & ~above] = ty - y[right & ~above]
    piecewise[~right & above] = ty - y[~right & above]
    piecewise[~right & ~above] = y[~right & ~above] - ty
    return float(np.max(np.abs(direct - piecewise)))


def run() -> list[dict[str, float | str | bool]]:
    analytic, finite_difference, sign_error, reversed_error = (
        skew_mad_influence_check()
    )
    bound_violation = midpoint_mad_bound_max_violation()
    piecewise_error = sign_radius_piecewise_max_error()
    return [
        {
            "check": "midpoint_mad_deterministic_bound",
            "value": bound_violation,
            "reference": 1e-12,
            "passed": bound_violation <= 1e-12,
        },
        {
            "check": "skew_mad_if_finite_difference_error",
            "value": sign_error,
            "reference": 1e-4,
            "passed": sign_error < 1e-4,
        },
        {
            "check": "skew_mad_reversed_sign_error",
            "value": reversed_error,
            "reference": 0.1,
            "passed": reversed_error > 0.1,
        },
        {
            "check": "sign_radius_piecewise_error",
            "value": piecewise_error,
            "reference": 1e-12,
            "passed": piecewise_error <= 1e-12,
        },
        {
            "check": "skew_mad_if_analytic_value",
            "value": analytic,
            "reference": finite_difference,
            "passed": sign_error < 1e-4,
        },
    ]


if __name__ == "__main__":
    rows = run()
    write_tsv(OUTPUT, rows)
    print(f"wrote {len(rows)} checks to {OUTPUT}")
