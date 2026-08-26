from pathlib import Path

from scripts.audit_claim_theory_20260826 import audit_claim_theory


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_all_deterministic_claim_theory_audits_pass():
    rows = audit_claim_theory()
    assert len(rows) == 12
    assert all(int(row["passed"]) == 1 for row in rows)


def test_appendix_claim_additions_are_well_formed_and_mad_formula_not_duplicated():
    path = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"
    text = path.read_text()
    assert "Corollary A.3 (reference orthogonality under independence)" in text
    assert "Proposition A.3 (positive affine invariance)" in text
    assert "\r" not in text

    derivative = text.split("\\dot d[h]=-", maxsplit=1)[1].split("\\]", maxsplit=1)[0]
    assert derivative.count("H(m+d)-H(m-d)") == 1

