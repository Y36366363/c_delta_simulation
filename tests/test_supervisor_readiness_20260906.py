import csv
from pathlib import Path

from scripts.audit_supervisor_readiness_20260906 import supervisor_readiness_audit


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_supervisor_readiness_audit_passes():
    rows = supervisor_readiness_audit()
    assert len(rows) == 12
    assert all(int(row["passed"]) for row in rows)


def test_readiness_audit_preserves_mixed_evidence_statuses():
    rows = {row["check"]: row for row in supervisor_readiness_audit()}
    assert rows["regular_iid_theorem_matches_appendix"]["status"] == "ready"
    assert (
        rows["claim2_switching_mechanism_has_triangulated_support"]["status"]
        == "ready_as_mixed_theory_empirical_claim"
    )
    assert (
        rows["claim3_first_order_transport_and_residual_are_both_visible"]["status"]
        == "ready_as_explanatory_diagnostic"
    )
    assert (
        rows["application_and_scope_expansions_are_explicitly_open"]["status"]
        == "supervisor_decision_required"
    )


def test_stored_readiness_table_matches_live_audit():
    path = PROJECT_ROOT / "results" / "supervisor_readiness_audit_20260906.tsv"
    with path.open(newline="") as stream:
        stored = list(csv.DictReader(stream, delimiter="\t"))
    expected = supervisor_readiness_audit()
    assert len(stored) == len(expected)
    for observed, regenerated in zip(stored, expected, strict=True):
        assert observed == {key: str(value) for key, value in regenerated.items()}


def test_readiness_script_is_audit_only():
    text = (
        PROJECT_ROOT / "scripts" / "audit_supervisor_readiness_20260906.py"
    ).read_text()
    for forbidden in (
        "default_rng",
        "np.random",
        "profile_weak_null_test",
        "profile_studentized_permutation_test",
    ):
        assert forbidden not in text
