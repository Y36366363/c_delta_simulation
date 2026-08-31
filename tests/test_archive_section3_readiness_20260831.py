from pathlib import Path

from scripts.audit_section3_readiness_20260831 import section3_readiness_audit


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_section3_blocking_readiness_checks_pass_and_gap_is_explicit():
    rows = section3_readiness_audit()
    assert len(rows) == 7
    assert all(int(row["passed"]) for row in rows if int(row["blocking"]))
    open_gaps = [row for row in rows if not int(row["passed"])]
    assert [row["check"] for row in open_gaps] == [
        "primary_rho_inference_promoted_to_public_src_api"
    ]
    assert int(open_gaps[0]["blocking"]) == 0


def test_archive_audit_distinguishes_existing_v2_from_planned_correction():
    text = (
        PROJECT_ROOT / "docs" / "archive_and_section3_readiness_20260831.md"
    ).read_text()
    assert "arXiv:2510.16717" in text
    assert "current inspected version: v2" in text
    assert "the planned correction is not yet online" in text
    assert "c_\\delta^{\\mathrm{corrected}}" in text
    assert "c_\\delta^{(v2)}}{n}" in text


def test_active_draft_has_resolved_archive_identifier_and_no_false_status():
    draft = (
        PROJECT_ROOT / "docs" / "manuscript_draft_sections_1_2_20260830.md"
    ).read_text()
    assert "Hoorn (2025)" in draft
    assert "arXiv:2510.16717" in draft
    assert "final corrected arXiv citation to be inserted" not in draft
    assert "still lacks the planned \\(1/n\\) numerator correction" in draft


def test_section3_readiness_preserves_theorem_boundaries():
    text = (
        PROJECT_ROOT / "docs" / "archive_and_section3_readiness_20260831.md"
    ).read_text()
    assert "It should not attempt to prove finite-sample validity" in text
    assert "The theorem is pointwise" in text
    assert "weak-null permutation" in text
    assert "Section 3 is ready to draft" in text
