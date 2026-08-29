from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKELETON = PROJECT_ROOT / "docs" / "manuscript_skeleton_and_readiness_20260829.md"


def test_manuscript_skeleton_maps_every_primary_evidence_source_to_existing_file():
    text = SKELETON.read_text()
    required = (
        "results/estimand_choice_audit_20260819.tsv",
        "results/scope_decision_audit_20260829.tsv",
        "results/claim1_wald_validation_20260823.tsv",
        "results/claim1_oracle_reference_validation_20260825.tsv",
        "results/claim2_reference_mechanism_validation_20260823.tsv",
        "results/claim2_sign_balance_intervention_validation_20260824.tsv",
        "results/claim2_sign_coupling_validation_20260825.tsv",
        "results/claim3_conditioning_lofo_summary_validation_20260823.tsv",
        "results/claim3_stricter_cv_summary_validation_20260824.tsv",
        "results/claim3_prospective_family_summary_validation_20260825.tsv",
        "results/claim3_prospective_family_validation_20260825.tsv",
        "results/claim_theory_audit_20260826.tsv",
        "results/canonical_evidence_20260819.tsv",
    )
    for relative in required:
        assert f"`{relative}`" in text
        assert (PROJECT_ROOT / relative).exists()


def test_skeleton_preserves_inference_and_diagnostic_boundaries():
    text = SKELETON.read_text()
    assert "not yet a data-driven accept/reject gate" in text
    assert "empirical fully recomputed studentized-permutation evidence" in text
    assert "Lead with Wald evidence" in text
    assert "Applied illustration | Unresolved" in text
    assert "No sentence should claim uniform validity" in text

