from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DRAFT = PROJECT_ROOT / "docs" / "manuscript_draft_sections_1_2_20260830.md"


def _text() -> str:
    return DRAFT.read_text()


def test_draft_has_complete_introduction_and_estimand_structure():
    text = _text()
    required_headings = (
        "## 1. Introduction",
        "## 2. Robust-reference divergence profiles",
        "### 2.1 Paired observations and marginal robust references",
        "### 2.2 Primary profile-correlation estimand",
        "### 2.3 Secondary normalized cross-moment scale",
        "### 2.4 Sample construction",
        "### 2.5 Relation to the original all-to-all profile",
        "### 2.6 Fixed-margin permutation ordering and inference boundary",
        "### 2.7 Interpretation carried forward",
    )
    for heading in required_headings:
        assert heading in text
    assert len(text.split()) > 2_100


def test_draft_matches_frozen_estimand_and_implementation_conventions():
    text = _text()
    assert "\\rho_P(P)" in text
    assert "C=1+\\rho_P\\,CV(" in text
    assert "CV(a_P)" in text and "CV(b_P)" in text
    assert "k=1.4826" in text
    assert "c=1.345" in text
    assert "midpoint convention" in text
    assert "\\widehat\\rho_P" in text
    assert "\\widehat C" in text
    assert "D_i^2" in text
    assert "\\frac{n}{n-1}\\{(X_i-\\bar X)^2+s_X^2\\}" in text


def test_draft_preserves_claim_and_inference_boundaries():
    text = _text()
    assert "It does not imply" in text
    assert "a universal cutoff or a data-driven accept/reject gate" in text
    assert "does not generally imply that invariance" in text
    assert "can* invalidate" in text
    assert "Neither construction is a uniformly" in text
    assert "A conditional weak-null" in text
    assert "arXiv:2510.16717" in text
    assert "final corrected arXiv citation to be inserted" not in text
    for forbidden in (
        "always invalidates",
        "universally valid",
        "proves weak-null permutation validity",
        "the new method is superior",
    ):
        assert forbidden not in text


def test_draft_latex_delimiters_and_control_characters_are_balanced():
    text = _text()
    assert "\r" not in text
    assert text.count("\\[") == text.count("\\]")
    assert text.count("\\(") == text.count("\\)")
