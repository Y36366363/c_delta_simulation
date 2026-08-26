"""Deterministic analytic audits for the three frozen manuscript claims."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_nuisance_jacobian_20260817 import (
    PopulationDistribution,
    population_nuisance,
    skew_lognormal_distribution,
    symmetric_bridge_distribution,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def independence_orthogonality_check() -> list[dict[str, object]]:
    """Verify the exact cancellation of reference terms under independence."""
    x = np.asarray((-2.0, -0.4, 0.3, 1.8, 4.0))
    px = np.asarray((0.08, 0.17, 0.31, 0.29, 0.15))
    y = np.asarray((-1.0, 0.2, 0.9, 3.2))
    py = np.asarray((0.14, 0.36, 0.28, 0.22))
    tx, ty = 0.35, 0.55

    a, b = np.abs(x - tx), np.abs(y - ty)
    sx, sy = np.sign(x - tx), np.sign(y - ty)
    joint = np.outer(px, py)
    mean_a, mean_b = float(px @ a), float(py @ b)
    var_a = float(px @ (a - mean_a) ** 2)
    var_b = float(py @ (b - mean_b) ** 2)
    denominator = np.sqrt(var_a * var_b)
    covariance = float(np.sum(joint * (a[:, None] - mean_a) * (b[None, :] - mean_b)))
    rho = covariance / denominator

    kappa_x = (
        -float(np.sum(joint * sx[:, None] * b[None, :]))
        + float(px @ sx) * mean_b
    ) / denominator
    kappa_x -= rho * (
        -2.0 * float(px @ (x - tx)) + 2.0 * mean_a * float(px @ sx)
    ) / (2.0 * var_a)
    kappa_y = (
        -float(np.sum(joint * a[:, None] * sy[None, :]))
        + mean_a * float(py @ sy)
    ) / denominator
    kappa_y -= rho * (
        -2.0 * float(py @ (y - ty)) + 2.0 * mean_b * float(py @ sy)
    ) / (2.0 * var_b)

    return [
        {
            "claim": "claim1",
            "audit": "independence_reference_orthogonality",
            "metric": metric,
            "value": value,
            "target": 0.0,
            "absolute_error": abs(value),
            "tolerance": 1e-14,
            "passed": int(abs(value) < 1e-14),
        }
        for metric, value in (("rho", rho), ("kappa_x", kappa_x), ("kappa_y", kappa_y))
    ]


def binary_switching_checks() -> list[dict[str, object]]:
    """Check the limiting profile correlations created by mode switching."""
    signs = np.asarray((-1.0, -1.0, 1.0, 1.0, 1.0))
    profiles = {
        "same_positive_mode": (np.abs(signs - 0.30), np.abs(signs - 0.55), 1.0),
        "same_negative_mode": (np.abs(signs + 0.30), np.abs(signs + 0.55), 1.0),
        "opposite_modes": (np.abs(signs - 0.30), np.abs(signs + 0.55), -1.0),
    }
    rows = []
    for name, (profile_x, profile_y, target) in profiles.items():
        correlation = float(np.corrcoef(profile_x, profile_y)[0, 1])
        error = abs(correlation - target)
        rows.append(
            {
                "claim": "claim2",
                "audit": "binary_mode_switching_limit",
                "metric": name,
                "value": correlation,
                "target": target,
                "absolute_error": error,
                "tolerance": 1e-14,
                "passed": int(error < 1e-14),
            }
        )
    return rows


def transformed_distribution(
    distribution: PopulationDistribution, *, shift: float, scale: float
) -> PopulationDistribution:
    """Return the law of shift + scale * W for a positive scale."""
    lower = shift + scale * distribution.lower
    upper = shift + scale * distribution.upper
    return PopulationDistribution(
        name=f"affine_{distribution.name}",
        pdf=lambda value: float(distribution.pdf((value - shift) / scale) / scale),
        cdf=lambda value: float(distribution.cdf((value - shift) / scale)),
        lower=lower,
        upper=upper,
    )


def affine_invariance_checks() -> list[dict[str, object]]:
    """Numerically verify invariance of standardized J and its index."""
    rows = []
    distributions = (
        symmetric_bridge_distribution(0.10, "hyperexponential"),
        skew_lognormal_distribution(),
    )
    for distribution in distributions:
        original = population_nuisance(distribution)
        transformed = population_nuisance(
            transformed_distribution(distribution, shift=3.25, scale=2.40)
        )
        jacobian_error = float(
            np.max(
                np.abs(
                    np.asarray(original["jacobian"])
                    - np.asarray(transformed["jacobian"])
                )
            )
        )
        singular_error = abs(
            float(original["minimum_singular_value"])
            - float(transformed["minimum_singular_value"])
        )
        inverse_identity_error = abs(
            float(original["inverse_jacobian_norm"])
            * float(original["minimum_singular_value"])
            - 1.0
        )
        for metric, value, tolerance in (
            ("max_abs_J_difference", jacobian_error, 2e-7),
            ("minimum_singular_value_difference", singular_error, 2e-7),
            ("inverse_norm_identity_error", inverse_identity_error, 1e-12),
        ):
            rows.append(
                {
                    "claim": "claim3",
                    "audit": "positive_affine_invariance",
                    "metric": f"{distribution.name}:{metric}",
                    "value": value,
                    "target": 0.0,
                    "absolute_error": value,
                    "tolerance": tolerance,
                    "passed": int(value < tolerance),
                }
            )
    return rows


def audit_claim_theory() -> list[dict[str, object]]:
    return (
        independence_orthogonality_check()
        + binary_switching_checks()
        + affine_invariance_checks()
    )


def main() -> None:
    rows = audit_claim_theory()
    output = RESULTS_DIR / "claim_theory_audit_20260826.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
