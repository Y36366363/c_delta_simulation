from pathlib import Path

from scripts.audit_external_math_review_20260821 import run


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPENDIX = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"
REVIEW = PROJECT_ROOT / "docs" / "external_math_review_appendix_placement_20260821.md"


def test_external_math_numerical_safeguards_pass():
    rows = run()
    assert all(row["passed"] for row in rows)
    indexed = {row["check"]: row for row in rows}
    assert indexed["skew_mad_if_finite_difference_error"]["value"] < 1e-4
    assert indexed["skew_mad_reversed_sign_error"]["value"] > 0.1


def test_appendix_records_exact_literature_convention_and_placement():
    appendix = APPENDIX.read_text()
    review = REVIEW.read_text()
    assert "sample convention defined by Mazumder and Serfling" in appendix
    assert "Mazumder and Serfling (2009)" in appendix
    assert "Main manuscript Appendix A" in review
    assert "Online Supplement S1" in review
    assert "No conditional weak-null permutation CLT" in review
