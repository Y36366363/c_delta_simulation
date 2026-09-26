"""Deterministic Gaussian target comparison; no simulated data or inference tests.

The absolute-product moment is computed by adaptive integration of the
conditional normal absolute first moment.  The comparison formula is
evaluated separately, so the integration does not reuse the closed form.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform

import scipy
from scipy.integrate import quad


CORRELATIONS = (-0.8, -0.4, 0.0, 0.4, 0.8)
TOLERANCE = 2e-11
SQRT_TWO_OVER_PI = math.sqrt(2.0 / math.pi)
SQRT_TWO_PI = math.sqrt(2.0 * math.pi)


def conditional_absolute_mean(x, correlation):
    """E[|Y| | X=x] for a standard bivariate Gaussian pair."""
    mean = correlation * x
    sd = math.sqrt(1.0 - correlation * correlation)
    return (
        sd * SQRT_TWO_OVER_PI * math.exp(-0.5 * (mean / sd) ** 2)
        + mean * math.erf(mean / (sd * math.sqrt(2.0)))
    )


def absolute_product_quadrature(correlation):
    def integrand(x):
        density = math.exp(-0.5 * x * x) / SQRT_TWO_PI
        return 2.0 * x * density * conditional_absolute_mean(x, correlation)

    return quad(integrand, 0.0, math.inf, epsabs=2e-13, epsrel=2e-13)


def squared_product_quadrature(correlation):
    def integrand(x):
        density = math.exp(-0.5 * x * x) / SQRT_TWO_PI
        conditional_second = 1.0 - correlation**2 + correlation**2 * x * x
        return 2.0 * x * x * density * conditional_second

    return quad(integrand, 0.0, math.inf, epsabs=2e-13, epsrel=2e-13)


def run():
    rows = []
    for correlation in CORRELATIONS:
        cross, error = absolute_product_quadrature(correlation)
        rho_quad = (cross - 2.0 / math.pi) / (1.0 - 2.0 / math.pi)
        rho_formula = (
            math.sqrt(1.0 - correlation**2)
            + correlation * math.asin(correlation)
            - 1.0
        ) / (math.pi / 2.0 - 1.0)
        square_cross, square_error = squared_product_quadrature(correlation)
        squared_corr_quad = (square_cross - 1.0) / 2.0
        assert abs(rho_quad - rho_formula) < TOLERANCE
        assert abs(squared_corr_quad - correlation**2) < TOLERANCE
        assert error < TOLERANCE
        assert square_error < TOLERANCE
        rows.append({
            "raw_gaussian_correlation": correlation,
            "pearson": correlation,
            "rho_profile_formula": rho_formula,
            "rho_profile_quadrature": rho_quad,
            "absolute_product_moment_quadrature": cross,
            "absolute_product_quadrature_error_estimate": error,
            "rho_formula_quadrature_absolute_gap": abs(rho_quad - rho_formula),
            "squared_variable_correlation": correlation**2,
            "squared_variable_correlation_quadrature": squared_corr_quad,
            "squared_product_quadrature_error_estimate": square_error,
            "linear_lancaster": max(abs(correlation), correlation**2),
            "rank_gaussian_lancaster": abs(correlation),
        })

    by_correlation = {row["raw_gaussian_correlation"]: row for row in rows}
    for correlation in (0.4, 0.8):
        positive = by_correlation[correlation]
        negative = by_correlation[-correlation]
        assert positive["pearson"] == -negative["pearson"]
        for field in ("rho_profile_formula", "rho_profile_quadrature",
                      "squared_variable_correlation", "linear_lancaster",
                      "rank_gaussian_lancaster"):
            assert abs(positive[field] - negative[field]) < TOLERANCE
        assert 0.0 < positive["rho_profile_formula"] < correlation**2 < correlation
        assert abs(positive["linear_lancaster"] - positive["rho_profile_formula"]) > 0.1
    assert abs(by_correlation[0.0]["rho_profile_quadrature"]) < TOLERANCE

    return {
        "all_passed": True,
        "date": "2026-09-25",
        "check_type": "deterministic population identities and target separation",
        "monte_carlo_datasets": 0,
        "new_simulation_cells": 0,
        "absolute_tolerance": TOLERANCE,
        "model": {
            "law": "Centered bivariate normal with unit marginal variances",
            "raw_correlations": list(CORRELATIONS),
            "population_robust_references": [0.0, 0.0],
            "reason_for_references": "Unique Huber roots are zero by marginal symmetry",
            "nuisance_contribution": (
                "Target reference derivatives vanish by joint central symmetry; "
                "this is not an active-nuisance validation."
            ),
        },
        "derivation": {
            "absolute_product": (
                "Integrate 2*x*phi(x)*E[abs(Y)|X=x] from zero to infinity, "
                "where Y|X=x is N(r*x,1-r^2)."
            ),
            "profile_correlation": (
                "(E[abs(X*Y)]-2/pi)/(1-2/pi), compared with "
                "(sqrt(1-r^2)+r*asin(r)-1)/(pi/2-1)."
            ),
            "squared_correlation": (
                "Integrate x^2*E[Y^2|X=x]; E[X^2]=1 and Var(X^2)=2 "
                "give Corr(X^2,Y^2)=r^2."
            ),
            "linear_lancaster": "max(abs(r), r^2)=abs(r) for abs(r)<=1",
            "rank_gaussian_lancaster": (
                "Phi^{-1}(F_X(X))=X and Phi^{-1}(F_Y(Y))=Y under "
                "standard normal margins; hence the same abs(r)."
            ),
        },
        "sources": [
            {
                "authors": "Afuecheta, E.; Nadarajah, S.; Chan, S.",
                "year": 2023,
                "title": "Folded Bivariate Distributions as Models for Magnitude Correlation",
                "journal": "REVSTAT--Statistical Journal",
                "volume_issue_pages": "21(1), 21-38",
                "doi": "10.57805/revstat.v21i1.395",
                "url": "https://revstat.ine.pt/index.php/REVSTAT/article/view/395",
                "relevance": (
                    "Page 22 defines Corr(abs(X),abs(Y)); page 24 equation (2.1) "
                    "gives the folded density. The Gaussian expression in this "
                    "audit is independently checked by conditional integration, "
                    "not attributed to this paper as a new identity."
                ),
            },
            {
                "authors": "Holzmann, H.; Klar, B.",
                "year": 2025,
                "title": "Lancaster correlation",
                "journal": "Scandinavian Journal of Statistics",
                "volume_issue_pages": "52(1), 145-169",
                "doi": "10.1111/sjos.12733",
                "url": "https://publikationen.bibliothek.kit.edu/1000172416/153641019",
                "relevance": (
                    "Linear and rank-Gaussian Lancaster targets differ from "
                    "correlation of unsigned marginal reference distances."
                ),
            },
        ],
        "rows": rows,
        "maximum_formula_quadrature_absolute_gap": max(
            row["rho_formula_quadrature_absolute_gap"] for row in rows
        ),
        "scope": [
            "No confidence intervals, rejection rates or calibration claims.",
            "No finite-sample reference-estimation comparison.",
            "No evidence that one target or test is generally superior.",
            "A formula check is not independent mathematical peer review.",
        ],
        "environment": {
            "python": platform.python_version(),
            "scipy": scipy.__version__,
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError("Use a fresh report path; do not overwrite frozen results")
    report = run()
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "all_passed": report["all_passed"],
        "population_points": len(report["rows"]),
        "maximum_formula_quadrature_absolute_gap": report[
            "maximum_formula_quadrature_absolute_gap"
        ],
        "new_simulation_cells": 0,
    }, indent=2))
