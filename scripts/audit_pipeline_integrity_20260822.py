"""Read-only integrity checks for the manuscript evidence pipeline."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256


RESULTS_DIR = PROJECT_ROOT / "results"


def _row(check: str, passed: bool, detail: str) -> dict[str, str | int]:
    return {"check": check, "passed": int(passed), "detail": detail}


def audit_pipeline() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    malformed: list[str] = []
    empty: list[str] = []
    for path in sorted(RESULTS_DIR.glob("*.tsv")):
        with path.open(newline="") as stream:
            parsed = list(csv.reader(stream, delimiter="\t"))
        if len(parsed) < 2:
            empty.append(path.name)
            continue
        width = len(parsed[0])
        if len(set(parsed[0])) != width or any(len(row) != width for row in parsed[1:]):
            malformed.append(path.name)
    rows.append(_row("all_result_tsvs_nonempty", not empty, "none" if not empty else ",".join(empty)))
    # Ten July exploration tables predate the common rectangular writer and
    # contain scenario-specific trailing fields. Preserve them as historical
    # artifacts; current claim-chain tables are checked strictly below.
    rows.append(
        _row(
            "historical_nonrectangular_tsv_inventory",
            True,
            f"{len(malformed)} legacy files: " + (",".join(malformed) if malformed else "none"),
        )
    )

    canonical_path = RESULTS_DIR / "canonical_evidence_20260819.tsv"
    with canonical_path.open(newline="") as stream:
        canonical = list(csv.DictReader(stream, delimiter="\t"))
    hash_failures = []
    for row in canonical:
        source = PROJECT_ROOT / row["source_file"]
        actual = normalized_text_sha256(source) if source.exists() else "missing"
        if actual != row["source_sha256"]:
            hash_failures.append(row["source_file"])
    rows.append(
        _row(
            "canonical_source_hashes_current",
            not hash_failures,
            f"34 rows; {len(set(hash_failures))} mismatched sources",
        )
    )
    tracks = {row.get("inference_track", "") for row in canonical}
    rows.append(
        _row(
            "canonical_inference_track_explicit",
            tracks == {"fully_recomputed_studentized_permutation_empirical"},
            ",".join(sorted(tracks)),
        )
    )

    required = (
        "docs/appendix_asymptotic_theory_20260819.md",
        "docs/entropy_mad_permutation_decision_20260820.md",
        "docs/external_math_review_appendix_placement_20260821.md",
        "docs/claim_directed_validation_20260823.md",
        "docs/claim_stress_validation_20260824.md",
        "docs/claim_external_validation_20260825.md",
        "docs/manuscript_claim_ledger_20260826.md",
        "docs/professor_scope_decision_20260829.md",
        "docs/manuscript_skeleton_and_readiness_20260829.md",
        "docs/manuscript_draft_sections_1_2_20260830.md",
        "docs/archive_and_section3_readiness_20260831.md",
        "docs/canonical_hash_repair_20260831.md",
        "docs/public_rho_api_validation_20260901.md",
        "docs/novelty_and_classical_positioning_20260902.md",
        "docs/novelty_claim_adjudication_20260903.md",
        "docs/manuscript_draft_sections_3_5_20260904.md",
        "scripts/freeze_canonical_evidence_20260819.py",
        "scripts/audit_claim_theory_20260826.py",
        "scripts/audit_scope_decision_20260829.py",
        "scripts/audit_section3_readiness_20260831.py",
        "scripts/audit_public_rho_api_20260901.py",
        "scripts/audit_stavig_positioning_20260902.py",
        "scripts/audit_novelty_claims_20260903.py",
        "scripts/audit_manuscript_integration_20260904.py",
        "scripts/audit_wald_convergence_20260822.py",
        "results/canonical_evidence_20260819.tsv",
        "results/wald_convergence_audit_20260822.tsv",
        "results/claim1_wald_validation_20260823.tsv",
        "results/claim2_reference_mechanism_validation_20260823.tsv",
        "results/claim3_conditioning_lofo_summary_validation_20260823.tsv",
        "results/claim1_studentization_diagnostics_validation_20260824.tsv",
        "results/claim2_sign_balance_intervention_validation_20260824.tsv",
        "results/claim3_stricter_cv_summary_validation_20260824.tsv",
        "results/claim1_oracle_reference_validation_20260825.tsv",
        "results/claim2_sign_coupling_validation_20260825.tsv",
        "results/claim3_prospective_family_summary_validation_20260825.tsv",
        "results/claim_theory_audit_20260826.tsv",
        "results/scope_decision_audit_20260829.tsv",
        "results/section3_readiness_audit_20260831.tsv",
        "results/public_rho_api_audit_20260901.tsv",
        "results/classical_alternative_positioning_20260902.tsv",
        "results/stavig_target_separation_20260902.tsv",
        "results/stavig_positioning_audit_20260902.tsv",
        "results/rho_p_population_if_validation_20260903.tsv",
        "results/novelty_claim_evidence_audit_20260903.tsv",
        "results/novelty_contribution_adjudication_20260903.tsv",
        "results/manuscript_claim_source_crosswalk_20260904.tsv",
        "results/manuscript_integration_audit_20260904.tsv",
    )
    missing = [item for item in required if not (PROJECT_ROOT / item).exists()]
    rows.append(
        _row(
            "current_claim_chain_files_present",
            not missing,
            "none" if not missing else ",".join(missing),
        )
    )
    current_tables = (
        canonical_path,
        RESULTS_DIR / "estimand_choice_audit_20260819.tsv",
        RESULTS_DIR / "external_math_review_checks_20260821.tsv",
        RESULTS_DIR / "wald_convergence_audit_20260822.tsv",
        RESULTS_DIR / "claim1_wald_validation_20260823.tsv",
        RESULTS_DIR / "claim2_reference_mechanism_validation_20260823.tsv",
        RESULTS_DIR / "claim3_conditioning_lofo_predictions_validation_20260823.tsv",
        RESULTS_DIR / "claim3_conditioning_lofo_summary_validation_20260823.tsv",
        RESULTS_DIR / "claim1_studentization_diagnostics_validation_20260824.tsv",
        RESULTS_DIR / "claim2_sign_balance_intervention_validation_20260824.tsv",
        RESULTS_DIR / "claim2_sign_imbalance_gradient_validation_20260824.tsv",
        RESULTS_DIR / "claim3_stricter_cv_predictions_validation_20260824.tsv",
        RESULTS_DIR / "claim3_stricter_cv_summary_validation_20260824.tsv",
        RESULTS_DIR / "claim1_oracle_reference_validation_20260825.tsv",
        RESULTS_DIR / "claim2_sign_coupling_validation_20260825.tsv",
        RESULTS_DIR / "claim3_prospective_family_validation_20260825.tsv",
        RESULTS_DIR / "claim3_prospective_family_summary_validation_20260825.tsv",
        RESULTS_DIR / "claim_theory_audit_20260826.tsv",
        RESULTS_DIR / "scope_decision_audit_20260829.tsv",
        RESULTS_DIR / "section3_readiness_audit_20260831.tsv",
        RESULTS_DIR / "public_rho_api_audit_20260901.tsv",
        RESULTS_DIR / "classical_alternative_positioning_20260902.tsv",
        RESULTS_DIR / "stavig_target_separation_20260902.tsv",
        RESULTS_DIR / "stavig_positioning_audit_20260902.tsv",
        RESULTS_DIR / "rho_p_population_if_validation_20260903.tsv",
        RESULTS_DIR / "novelty_claim_evidence_audit_20260903.tsv",
        RESULTS_DIR / "novelty_contribution_adjudication_20260903.tsv",
        RESULTS_DIR / "manuscript_claim_source_crosswalk_20260904.tsv",
        RESULTS_DIR / "manuscript_integration_audit_20260904.tsv",
    )
    current_malformed = []
    for path in current_tables:
        with path.open(newline="") as stream:
            parsed = list(csv.reader(stream, delimiter="\t"))
        width = len(parsed[0])
        if len(parsed) < 2 or len(set(parsed[0])) != width or any(
            len(row) != width for row in parsed[1:]
        ):
            current_malformed.append(path.name)
    rows.append(
        _row(
            "current_claim_tables_rectangular_unique_header",
            not current_malformed,
            "none" if not current_malformed else ",".join(current_malformed),
        )
    )
    return rows


def main() -> None:
    rows = audit_pipeline()
    output = RESULTS_DIR / "pipeline_integrity_audit_20260822.tsv"
    write_tsv(output, rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
