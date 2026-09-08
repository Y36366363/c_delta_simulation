"""Audit the Yao--Hoorn manuscript package before a supervisor discussion.

This script performs no simulation.  It checks the already drafted Sections
1--6, Appendix A, the public estimator audit, and the frozen evidence tables.
Its purpose is to distinguish results that are ready to report from decisions
that still require supervisor input.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.audit_section6_displays_20260905 import section6_display_audit
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"
SECTION12 = PROJECT_ROOT / "docs" / "manuscript_draft_sections_1_2_20260830.md"
SECTION35 = PROJECT_ROOT / "docs" / "manuscript_draft_sections_3_5_20260904.md"
SECTION6 = PROJECT_ROOT / "docs" / "manuscript_draft_section_6_20260905.md"
APPENDIX = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"
SKELETON = PROJECT_ROOT / "docs" / "manuscript_skeleton_and_readiness_20260829.md"


def _read_tsv(filename: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _find_one(rows: list[dict[str, str]], **criteria: object) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(str(row[key]) == str(value) for key, value in criteria.items())
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {criteria}, found {len(matches)}")
    return matches[0]


def _passed(value: str) -> bool:
    return value.strip().lower() in {"1", "true"}


def _check(
    check: str, passed: bool, status: str, detail: str, implication: str
) -> dict[str, object]:
    return {
        "check": check,
        "passed": int(passed),
        "status": status,
        "detail": detail,
        "supervisor_implication": implication,
    }


def supervisor_readiness_audit() -> list[dict[str, object]]:
    section12 = SECTION12.read_text()
    section35 = SECTION35.read_text()
    section6 = SECTION6.read_text()
    appendix = APPENDIX.read_text()
    skeleton = SKELETON.read_text()
    combined = "\n".join((section12, section35, section6))

    wald = _read_tsv("claim1_wald_validation_20260823.tsv")
    mechanism = _read_tsv("claim2_reference_mechanism_validation_20260823.tsv")
    balance = _read_tsv("claim2_sign_balance_intervention_validation_20260824.tsv")
    coupling = _read_tsv("claim2_sign_coupling_validation_20260825.tsv")
    lofo = _read_tsv("claim3_conditioning_lofo_summary_validation_20260823.tsv")
    strict = _read_tsv("claim3_stricter_cv_summary_validation_20260824.tsv")
    prospective = _read_tsv("claim3_prospective_family_validation_20260825.tsv")
    prospective_summary = _read_tsv(
        "claim3_prospective_family_summary_validation_20260825.tsv"
    )[0]

    normal640 = _find_one(wald, scenario="profile_null_normal_sign_link", n=640)
    t5640 = _find_one(wald, scenario="independent_t5", n=640)
    skew640 = _find_one(wald, scenario="independent_strong_skew", n=640)
    skew2560 = _find_one(wald, scenario="independent_strong_skew", n=2560)
    regular_wilson = all(
        float(row["wilson_95_low"]) <= 0.05 <= float(row["wilson_95_high"])
        for row in (normal640, t5640)
    )
    skew_declines = float(skew2560["rejection_rate"]) < float(
        skew640["rejection_rate"]
    )

    severe = [row for row in mechanism if float(row["radial_log_sd"]) == 0.1]
    diffuse = [row for row in mechanism if float(row["radial_log_sd"]) == 0.4]
    severe_minimum_reduction = min(
        float(row["paired_rejection_rate_difference"]) for row in severe
    )
    diffuse_maximum_difference = max(
        abs(float(row["paired_rejection_rate_difference"])) for row in diffuse
    )
    balance_reductions = []
    for n in (80, 640):
        iid = _find_one(balance, n=n, sign_design="iid_signs")
        exact = _find_one(balance, n=n, sign_design="exactly_balanced_signs")
        balance_reductions.append(
            float(iid["rejection_rate"]) - float(exact["rejection_rate"])
        )
    coupling_n640 = sorted(
        [row for row in coupling if int(row["n"]) == 640],
        key=lambda row: float(row["shared_sign_coupling"]),
    )
    coupling_gradient = (
        float(coupling_n640[-1]["mean_refitted_profile_effect"])
        - float(coupling_n640[0]["mean_refitted_profile_effect"])
    )
    fixed_coupling_maximum = max(
        abs(float(row["mean_fixed_zero_profile_effect"])) for row in coupling_n640
    )

    pooled = _find_one(lofo, held_out_family="pooled")
    cross_n = _find_one(strict, cv_scheme="cross_sample_size")
    held_level = _find_one(strict, cv_scheme="leave_conditioning_level_out")
    validation_improvements = (
        float(pooled["mae_improvement_fraction"]),
        float(cross_n["mae_improvement_fraction"]),
        float(held_level["mae_improvement_fraction"]),
        float(prospective_summary["mae_improvement_fraction"]),
    )
    prediction_residuals = [
        float(row["old_family_model_prediction"])
        - float(row["observed_rejection_rate"])
        for row in prospective
    ]

    proof_checks = _read_tsv("external_math_review_checks_20260821.tsv")
    api_checks = _read_tsv("public_rho_api_audit_20260901.tsv")
    section6_checks = section6_display_audit()
    manifest = _read_tsv("section6_display_manifest_20260905.tsv")
    manifest_current = all(
        (PROJECT_ROOT / row["source_file"]).exists()
        and normalized_text_sha256(PROJECT_ROOT / row["source_file"])
        == row["source_sha256"]
        for row in manifest
    )

    headings = (
        "## 1. Introduction",
        "## 2. Robust-reference divergence profiles",
        "## 3. Estimation and inference under regular identification",
        "## 4. A constructive failure from unstable robust references",
        "## 5. Nuisance conditioning as a first-order diagnostic",
        "## 6. Simulation design and consolidated evidence",
    )
    boundary_phrases = (
        "pointwise, not uniform",
        "can cause, not always causes",
        "first-order organizer, not a universal cutoff",
        "robust reference, not a globally robust correlation",
    )
    prohibited_positive_claims = (
        "the new method is superior",
        "proves weak-null permutation validity",
        "all multimodal laws fail",
        "necessary and sufficient for failure",
    )

    return [
        _check(
            "sections_1_to_6_are_structurally_complete",
            all(heading in combined for heading in headings),
            "ready",
            "all six planned main-text section headings are present",
            "A reportable backbone exists; active-nuisance calibration and independent mathematical review remain substantive boundaries.",
        ),
        _check(
            "primary_estimand_and_predecessor_are_separated",
            "Primary profile-correlation estimand" in section12
            and "arXiv:2510.16717" in section12
            and "changes the statistical functional" in section12
            and "not algebraically identical" in section12,
            "ready",
            "rho_P is primary and the original all-to-all c_d remains the predecessor",
            "Report a related but distinct paper, not a replacement coefficient.",
        ),
        _check(
            "regular_iid_theorem_matches_appendix",
            "Theorem 1 (regular robust-reference profile inference)" in section35
            and "Theorem A.1 (asymptotic linearity and normality)" in appendix
            and "Corollary A.1 (studentized Wald inference)" in appendix,
            "ready",
            "main theorem, appendix theorem, and Wald corollary are linked",
            "Claim 1 can be presented as theorem-level under declared assumptions.",
        ),
        _check(
            "external_proof_safeguards_pass",
            len(proof_checks) == 5 and all(_passed(row["passed"]) for row in proof_checks),
            "ready_with_publication_review",
            "MAD convention, endpoint-density sign, and piecewise algebra checks pass",
            "Source-level checks are not independent peer review; full mathematical review remains.",
        ),
        _check(
            "claim1_regular_calibration_and_boundary_are_preserved",
            regular_wilson and skew_declines,
            "ready_with_boundary",
            (
                f"n=640 regular Wilson intervals contain .05; strong-skew rejection "
                f"declines {float(skew640['rejection_rate']):.3f} to "
                f"{float(skew2560['rejection_rate']):.3f}"
            ),
            "Report pointwise validity and slow skew convergence together.",
        ),
        _check(
            "claim2_switching_mechanism_has_triangulated_support",
            severe_minimum_reduction >= 0.49
            and diffuse_maximum_difference <= 0.0180000001
            and min(balance_reductions) >= 0.475
            and coupling_gradient >= 0.62
            and fixed_coupling_maximum <= 0.0021,
            "ready_as_mixed_theory_empirical_claim",
            (
                f"minimum severe refit-fixed reduction={severe_minimum_reduction:.3f}; "
                f"diffuse maximum={diffuse_maximum_difference:.3f}; minimum balance "
                f"reduction={min(balance_reductions):.3f}; n=640 coupling effect "
                f"increase={coupling_gradient:.3f}"
            ),
            "Keep the imposed-offset identity separate from fitted-switching probabilities and finite-sample evidence.",
        ),
        _check(
            "claim3_first_order_transport_and_residual_are_both_visible",
            min(validation_improvements[:3]) >= 0.72
            and validation_improvements[3] >= 0.47
            and min(prediction_residuals) > 0.0,
            "ready_as_explanatory_diagnostic",
            (
                "LOFO/cross-size/held-level MAE improvements are at least "
                f"{min(validation_improvements[:3]):.3f}; prospective improvement="
                f"{validation_improvements[3]:.3f}; all six residuals are positive"
            ),
            "Report I_n as a first-order organizer, never as an operational gate.",
        ),
        _check(
            "public_rho_p_api_is_implementation_consistent",
            len(api_checks) == 8 and all(_passed(row["passed"]) for row in api_checks),
            "ready",
            "all eight API equivalence, invariance, and influence checks pass",
            "The implementation supports the primary estimand used in the manuscript.",
        ),
        _check(
            "section6_evidence_tracks_remain_separate",
            len(section6_checks) == 10
            and all(int(row["passed"]) for row in section6_checks),
            "ready",
            "Wald, mechanism, and empirical permutation displays pass all ten checks",
            "The empirical permutation panels do not validate the IID Wald theorem.",
        ),
        _check(
            "display_sources_and_hashes_are_current",
            len(manifest) == 7 and manifest_current,
            "ready",
            "all seven Section 6 source-manifest entries match current normalized hashes",
            "Reported numbers are traceable to frozen fixed-seed sources.",
        ),
        _check(
            "claim_boundaries_are_present_and_overclaims_absent",
            all(phrase in combined for phrase in boundary_phrases)
            and not any(phrase in combined.lower() for phrase in prohibited_positive_claims),
            "ready",
            "all four permanent boundaries are explicit; prohibited positive claims absent",
            "Use the same bounded wording in the abstract, cover letter, and meeting.",
        ),
        _check(
            "application_and_scope_expansions_are_explicitly_open",
            "Application gate — open" in skeleton
            and "Applied illustration" in skeleton
            and "operational warning rule" in skeleton,
            "supervisor_decision_required",
            "application choice and any operational diagnostic remain outside the frozen package",
            "Ask whether to add a real application and whether stronger local theory is desired.",
        ),
    ]


def main() -> None:
    rows = supervisor_readiness_audit()
    write_tsv(RESULTS_DIR / "supervisor_readiness_audit_20260906.tsv", rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
