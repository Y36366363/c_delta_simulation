"""Claim-directed novelty audit for the Yao--Hoorn manuscript.

The only new numerical calculation is a population finite-difference check of
the complete influence function for the primary estimand rho_P at one fixed
regular skew law.  All other checks recombine frozen claim evidence; no new
distribution grid is introduced.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np
from scipy.stats import norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_population_skew_influence_validation import (
    _location_influence,
    _marginal_fit,
    _normal_quadrature,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def _population_profile_moments(
    sigma: float,
    latent_correlation: float,
    nodes: np.ndarray,
    weights: np.ndarray,
    tx: float,
    ty: float,
) -> dict[str, float]:
    u = nodes[:, None]
    v = latent_correlation * u + np.sqrt(1.0 - latent_correlation**2) * nodes[None, :]
    joint_weights = weights[:, None] * weights[None, :]
    x = np.exp(sigma * u)
    y = np.exp(sigma * v)
    ax = np.abs(x - tx)
    ay = np.abs(y - ty)
    sign_x = np.sign(x - tx)
    sign_y = np.sign(y - ty)
    return {
        "cross": float(np.sum(joint_weights * ax * ay)),
        "mean_x": float(np.sum(joint_weights * ax)),
        "mean_y": float(np.sum(joint_weights * ay)),
        "square_x": float(np.sum(joint_weights * ax**2)),
        "square_y": float(np.sum(joint_weights * ay**2)),
        "mean_sign_x": float(np.sum(joint_weights * sign_x)),
        "mean_sign_y": float(np.sum(joint_weights * sign_y)),
        "sign_x_radius_y": float(np.sum(joint_weights * sign_x * ay)),
        "radius_x_sign_y": float(np.sum(joint_weights * ax * sign_y)),
        "centered_mean_x": float(np.sum(joint_weights * (x - tx))),
        "centered_mean_y": float(np.sum(joint_weights * (y - ty))),
    }


def _rho_from_moments(moment: dict[str, float]) -> float:
    variance_x = moment["square_x"] - moment["mean_x"] ** 2
    variance_y = moment["square_y"] - moment["mean_y"] ** 2
    covariance = moment["cross"] - moment["mean_x"] * moment["mean_y"]
    return float(covariance / np.sqrt(variance_x * variance_y))


def rho_complete_if_validation(
    *, sigma: float = 0.60, latent_correlation: float = 0.40, order: int = 160
) -> list[dict[str, object]]:
    """Validate the full rho_P IF by smooth-law contamination derivatives."""
    nodes, weights = _normal_quadrature(order)
    fit = _marginal_fit(sigma, nodes, weights)
    median, mad, scale, location = fit
    moment = _population_profile_moments(
        sigma, latent_correlation, nodes, weights, location, location
    )
    rho_p = _rho_from_moments(moment)
    variance_x = moment["square_x"] - moment["mean_x"] ** 2
    variance_y = moment["square_y"] - moment["mean_y"] ** 2
    denominator = float(np.sqrt(variance_x * variance_y))
    gradient = np.asarray(
        (
            1.0 / denominator,
            -moment["mean_y"] / denominator + rho_p * moment["mean_x"] / variance_x,
            -moment["mean_x"] / denominator + rho_p * moment["mean_y"] / variance_y,
            -0.5 * rho_p / variance_x,
            -0.5 * rho_p / variance_y,
        )
    )
    coefficient_x = (
        -moment["sign_x_radius_y"]
        + moment["mean_sign_x"] * moment["mean_y"]
    ) / denominator - 0.5 * rho_p * (
        -2.0 * moment["centered_mean_x"]
        + 2.0 * moment["mean_x"] * moment["mean_sign_x"]
    ) / variance_x
    coefficient_y = (
        -moment["radius_x_sign_y"]
        + moment["mean_x"] * moment["mean_sign_y"]
    ) / denominator - 0.5 * rho_p * (
        -2.0 * moment["centered_mean_y"]
        + 2.0 * moment["mean_y"] * moment["mean_sign_y"]
    ) / variance_y

    quantile = lambda probability: float(np.exp(sigma * norm.ppf(probability)))
    points = {
        "matched_high": (quantile(0.99), quantile(0.99)),
        "unmatched_x_high": (quantile(0.99), quantile(0.60)),
        "central_regular": (quantile(0.55), quantile(0.45)),
        "low_high": (quantile(0.01), quantile(0.99)),
    }
    base_vector = np.asarray(
        (
            moment["cross"],
            moment["mean_x"],
            moment["mean_y"],
            moment["square_x"],
            moment["square_y"],
        )
    )
    rows: list[dict[str, object]] = []
    for point_name, (point_x, point_y) in points.items():
        location_if_x, fixed_scale_if_x = _location_influence(
            point_x, sigma, nodes, weights, median, mad, scale, location
        )
        location_if_y, fixed_scale_if_y = _location_influence(
            point_y, sigma, nodes, weights, median, mad, scale, location
        )
        radius_x = abs(point_x - location)
        radius_y = abs(point_y - location)
        point_vector = np.asarray(
            (radius_x * radius_y, radius_x, radius_y, radius_x**2, radius_y**2)
        )
        direct = float((point_vector - base_vector) @ gradient)
        location_component = float(
            coefficient_x * location_if_x + coefficient_y * location_if_y
        )
        analytic = direct + location_component
        fixed_scale_analytic = float(
            direct
            + coefficient_x * fixed_scale_if_x
            + coefficient_y * fixed_scale_if_y
        )

        for epsilon in (1e-6, 1e-5, 1e-4):
            fit_x = _marginal_fit(
                sigma, nodes, weights, epsilon=epsilon, point=point_x
            )
            fit_y = _marginal_fit(
                sigma, nodes, weights, epsilon=epsilon, point=point_y
            )
            base_at_contaminated_fit = _population_profile_moments(
                sigma, latent_correlation, nodes, weights, fit_x[3], fit_y[3]
            )
            contaminated = {
                "cross": (1.0 - epsilon) * base_at_contaminated_fit["cross"]
                + epsilon * abs(point_x - fit_x[3]) * abs(point_y - fit_y[3]),
                "mean_x": (1.0 - epsilon) * base_at_contaminated_fit["mean_x"]
                + epsilon * abs(point_x - fit_x[3]),
                "mean_y": (1.0 - epsilon) * base_at_contaminated_fit["mean_y"]
                + epsilon * abs(point_y - fit_y[3]),
                "square_x": (1.0 - epsilon) * base_at_contaminated_fit["square_x"]
                + epsilon * (point_x - fit_x[3]) ** 2,
                "square_y": (1.0 - epsilon) * base_at_contaminated_fit["square_y"]
                + epsilon * (point_y - fit_y[3]) ** 2,
            }
            finite_difference = (_rho_from_moments(contaminated) - rho_p) / epsilon
            error = abs(finite_difference - analytic)
            rows.append(
                {
                    "point": point_name,
                    "epsilon": epsilon,
                    "population_rho_p": rho_p,
                    "analytic_influence": analytic,
                    "finite_difference": finite_difference,
                    "absolute_error": error,
                    "scaled_error": error / (1.0 + abs(analytic)),
                    "direct_five_moment_component": direct,
                    "reference_location_component": location_component,
                    "mad_indirect_component": analytic - fixed_scale_analytic,
                    "location_coefficient_x": coefficient_x,
                    "location_coefficient_y": coefficient_y,
                }
            )
    return rows


def _read_tsv(filename: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _audit_row(
    component: str,
    check: str,
    observed: float,
    criterion: str,
    threshold: float,
    passed: bool,
    interpretation: str,
) -> dict[str, object]:
    return {
        "novelty_component": component,
        "check": check,
        "observed": observed,
        "criterion": criterion,
        "threshold": threshold,
        "passed": int(passed),
        "interpretation": interpretation,
    }


def novelty_evidence_audit() -> list[dict[str, object]]:
    """Triangulate the three contributions from frozen evidence and the IF check."""
    if_rows = rho_complete_if_validation()
    smallest_epsilon = [row for row in if_rows if float(row["epsilon"]) == 1e-6]
    maximum_if_error = max(float(row["scaled_error"]) for row in smallest_epsilon)
    maximum_reference_component = max(
        abs(float(row["reference_location_component"])) for row in smallest_epsilon
    )
    maximum_mad_component = max(
        abs(float(row["mad_indirect_component"])) for row in smallest_epsilon
    )

    wald = _read_tsv("claim1_wald_validation_20260823.tsv")
    regular_large = {
        row["scenario"]: row
        for row in wald
        if row["scenario"] in {"profile_null_normal_sign_link", "independent_t5"}
        and int(row["n"]) == 640
    }
    regular_wilson_contains = all(
        float(row["wilson_95_low"]) <= 0.05 <= float(row["wilson_95_high"])
        for row in regular_large.values()
    )
    maximum_regular_z_sd_error = max(
        abs(float(row["sd_z"]) - 1.0) for row in regular_large.values()
    )
    skew_large = next(
        row
        for row in wald
        if row["scenario"] == "independent_strong_skew" and int(row["n"]) == 2560
    )

    mechanism = _read_tsv("claim2_reference_mechanism_validation_20260823.tsv")
    severe = [row for row in mechanism if float(row["radial_log_sd"]) == 0.1]
    diffuse = [row for row in mechanism if float(row["radial_log_sd"]) == 0.4]
    minimum_severe_reduction = min(
        float(row["paired_rejection_rate_difference"]) for row in severe
    )
    maximum_diffuse_difference = max(
        abs(float(row["paired_rejection_rate_difference"])) for row in diffuse
    )
    balanced = _read_tsv("claim2_sign_balance_intervention_validation_20260824.tsv")
    balance_by_n: dict[int, dict[str, float]] = {}
    for row in balanced:
        balance_by_n.setdefault(int(row["n"]), {})[row["sign_design"]] = float(
            row["rejection_rate"]
        )
    minimum_balance_reduction = min(
        cell["iid_signs"] - cell["exactly_balanced_signs"]
        for cell in balance_by_n.values()
    )

    lofo = _read_tsv("claim3_conditioning_lofo_summary_validation_20260823.tsv")
    pooled = next(row for row in lofo if row["held_out_family"] == "pooled")
    stricter = _read_tsv("claim3_stricter_cv_summary_validation_20260824.tsv")
    minimum_strict_mae_improvement = min(
        float(row["mae_improvement_fraction"]) for row in stricter
    )
    prospective = _read_tsv("claim3_prospective_family_validation_20260825.tsv")
    prospective_index = np.asarray(
        [float(row["conditioning_index"]) for row in prospective]
    )
    prospective_rate = np.asarray(
        [float(row["observed_rejection_rate"]) for row in prospective]
    )
    rank_index = np.argsort(np.argsort(prospective_index))
    rank_rate = np.argsort(np.argsort(prospective_rate))
    prospective_rank_correlation = float(np.corrcoef(rank_index, rank_rate)[0, 1])
    minimum_overprediction = min(
        float(row["old_family_model_prediction"])
        - float(row["observed_rejection_rate"])
        for row in prospective
    )

    return [
        _audit_row(
            "complete_generated_profile_inference",
            "rho_p_population_if_finite_difference",
            maximum_if_error,
            "less_than",
            5e-4,
            maximum_if_error < 5e-4,
            "the primary rho_P IF, not only C, matches a smooth-law contamination derivative",
        ),
        _audit_row(
            "complete_generated_profile_inference",
            "reference_path_is_numerically_active",
            maximum_reference_component,
            "greater_than",
            1e-3,
            maximum_reference_component > 1e-3,
            "the finite-difference agreement is not a vacuous fixed-reference case",
        ),
        _audit_row(
            "complete_generated_profile_inference",
            "mad_indirect_path_is_numerically_active",
            maximum_mad_component,
            "greater_than",
            1e-4,
            maximum_mad_component > 1e-4,
            "MAD scaling contributes through the fitted Huber location",
        ),
        _audit_row(
            "complete_generated_profile_inference",
            "regular_large_n_wilson_intervals_cover_nominal",
            float(regular_wilson_contains),
            "equal_to",
            1.0,
            regular_wilson_contains,
            "both fixed regular n=640 calibration designs remain compatible with 5 percent",
        ),
        _audit_row(
            "complete_generated_profile_inference",
            "regular_large_n_studentized_sd",
            maximum_regular_z_sd_error,
            "less_than",
            0.08,
            maximum_regular_z_sd_error < 0.08,
            "studentized spread is close to one in the two regular benchmark designs",
        ),
        _audit_row(
            "complete_generated_profile_inference",
            "strong_skew_slow_convergence_boundary_detected",
            float(skew_large["rejection_rate"]),
            "greater_than",
            0.07,
            float(skew_large["rejection_rate"]) > 0.07,
            "pointwise theory does not imply uniformly accurate moderate-sample calibration",
        ),
        _audit_row(
            "reference_switching_distortion",
            "paired_fixed_reference_removes_severe_failure",
            minimum_severe_reduction,
            "greater_than",
            0.45,
            minimum_severe_reduction > 0.45,
            "on identical samples, fixing the symmetry reference removes most severe distortion",
        ),
        _audit_row(
            "reference_switching_distortion",
            "fixed_reference_contrast_is_specific_to_near_degeneracy",
            maximum_diffuse_difference,
            "less_than",
            0.03,
            maximum_diffuse_difference < 0.03,
            "the same intervention is nearly neutral after radial variation recovers",
        ),
        _audit_row(
            "reference_switching_distortion",
            "exact_sign_balance_mechanism_intervention",
            minimum_balance_reduction,
            "greater_than",
            0.45,
            minimum_balance_reduction > 0.45,
            "removing sign-count fluctuations suppresses the fitted-reference switching path",
        ),
        _audit_row(
            "conditioning_diagnostic",
            "leave_one_family_out_mae_improvement",
            float(pooled["mae_improvement_fraction"]),
            "greater_than",
            0.65,
            float(pooled["mae_improvement_fraction"]) > 0.65,
            "I_n transports coarse transition information across the four bridge families",
        ),
        _audit_row(
            "conditioning_diagnostic",
            "stricter_grouped_cv_mae_improvement",
            minimum_strict_mae_improvement,
            "greater_than",
            0.65,
            minimum_strict_mae_improvement > 0.65,
            "the index retains signal under cross-size and held-conditioning-level checks",
        ),
        _audit_row(
            "conditioning_diagnostic",
            "prospective_family_rank_order",
            prospective_rank_correlation,
            "less_than",
            -0.80,
            prospective_rank_correlation < -0.80,
            "larger I_n prospectively corresponds to lower rejection in a fifth family",
        ),
        _audit_row(
            "conditioning_diagnostic",
            "prospective_family_systematic_residual",
            minimum_overprediction,
            "greater_than",
            0.0,
            minimum_overprediction > 0.0,
            "all prospective predictions are too high; the residual is unexplained by I_n, not proved purely higher order",
        ),
    ]


def contribution_adjudication() -> list[dict[str, str]]:
    """Separate general precedents from manuscript-specific contributions."""
    return [
        {
            "component": "complete generated-profile inference",
            "general_precedent": "functional delta methods and generated-regressor influence corrections are established",
            "project_specific_advance": "joint IF for five profile moments plus median/MAD-scaled Huber references for rho_P",
            "current_status": "formal pointwise theorem plus rho_P population finite-difference and calibration checks",
            "defensible_wording": "complete inference for this generated robust-reference profile estimand under fixed regular IID laws",
            "prohibited_overclaim": "a new general influence-function theory or uniform finite-sample validity",
            "remaining_requirement": "integrate proof and numerical audit into the manuscript appendix",
        },
        {
            "component": "reference-switching finite-sample distortion",
            "general_precedent": "M-estimator uniqueness and weak-identification failures are established general concerns",
            "project_specific_advance": "nonlocal robust-reference switching is isolated as a source of spurious profile correlation",
            "current_status": "idealized switching proposition plus paired fixed-reference, sign-balance, and coupling interventions",
            "defensible_wording": "near-degenerate reference fitting can cause severe finite-sample distortion in the studied construction",
            "prohibited_overclaim": "all multimodal or low-density laws fail, or the interventions are general corrections",
            "remaining_requirement": "state the construction and intervention logic compactly in the main text",
        },
        {
            "component": "I_n first-order diagnostic",
            "general_precedent": "Jacobian singularity as an identification diagnostic is established",
            "project_specific_advance": "sqrt(n) times the standardized nuisance Jacobian's minimum singular value organizes profile-inference failure",
            "current_status": "first-order derivation, affine-invariance proposition, grouped validation, and prospective family check",
            "defensible_wording": "a dimensionless first-order organizer with empirically demonstrated family residual",
            "prohibited_overclaim": "a universal cutoff, operational gate, or necessary-and-sufficient failure condition",
            "remaining_requirement": "decide whether to pursue local-to-degeneracy theory after supervisor feedback",
        },
    ]


def main() -> None:
    if_rows = rho_complete_if_validation()
    audit_rows = novelty_evidence_audit()
    write_tsv(RESULTS_DIR / "rho_p_population_if_validation_20260903.tsv", if_rows)
    write_tsv(RESULTS_DIR / "novelty_claim_evidence_audit_20260903.tsv", audit_rows)
    write_tsv(
        RESULTS_DIR / "novelty_contribution_adjudication_20260903.tsv",
        contribution_adjudication(),
    )
    for row in audit_rows:
        print(row)
    if not all(int(row["passed"]) for row in audit_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
