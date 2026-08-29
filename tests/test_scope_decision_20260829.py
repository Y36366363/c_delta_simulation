from pathlib import Path

from scripts.audit_scope_decision_20260829 import scope_decision_audit


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_scope_decision_audit_passes_without_new_simulation():
    rows = scope_decision_audit()
    assert len(rows) == 5
    assert all(int(row["passed"]) == 1 for row in rows)


def test_active_manuscript_documents_freeze_rho_as_primary():
    architecture = (
        PROJECT_ROOT / "docs" / "paper_architecture_and_conceptual_guide_20260818.md"
    ).read_text()
    ledger = (
        PROJECT_ROOT / "docs" / "manuscript_claim_ledger_20260826.md"
    ).read_text()
    scope = (
        PROJECT_ROOT / "docs" / "professor_scope_decision_20260829.md"
    ).read_text()

    assert "paper must explicitly decide whether" not in architecture
    assert "The construct decision is now closed" in architecture
    assert "Professor Hoorn's 2026-08-29 scope decision" in ledger
    assert "New Yao--Hoorn paper" in scope
    assert "No new distribution grid is needed" in scope

