import json

import numpy as np
import pytest

from scripts.audit_manuscript_completion_20260910 import (
    ROOT,
    OUTPUT,
    SECTION6,
    build_audit,
    display_checks,
    one,
)


def test_completion_audit_passes_without_new_simulation():
    report = build_audit()
    assert report["all_passed"]
    assert report["new_simulation_cells"] == 0
    assert report["display_number_checks"] == 95
    assert "not independent mathematical peer review" in report["scope"]


def test_table_audit_detects_an_optimistic_coverage_edit():
    text = (ROOT / SECTION6).read_text()
    assert "| 2560 | .9270 |" in text
    changed = text.replace("| 2560 | .9270 |", "| 2560 | .9500 |")
    failed = [r for r in display_checks(changed) if not r["passed"]]
    assert len(failed) == 1
    assert failed[0]["check"].startswith("active:2560:")


def test_source_lookup_never_silently_selects_duplicate_rows():
    with pytest.raises(ValueError, match="expected one source row"):
        one([{"n": "80"}, {"n": "80"}], n=80)
    with pytest.raises(ValueError, match="expected one source row"):
        one([{"n": "80"}], n=640)


def test_secondary_C_gradient_uses_only_three_moments():
    # An algebra safeguard, not a simulated heavy-tail CLT verification.
    moments = np.array([3.2, 1.3, 2.1])
    fun = lambda m: m[0] / (m[1] * m[2])
    effect = fun(moments)
    analytic = np.array(
        [1 / (moments[1] * moments[2]), -effect / moments[1], -effect / moments[2]]
    )
    h = 1e-6
    numerical = [
        (fun(moments + h * d) - fun(moments - h * d)) / (2 * h) for d in np.eye(3)
    ]
    np.testing.assert_allclose(analytic, numerical, atol=1e-9)
    appendix = (ROOT / "docs/appendix_asymptotic_theory_20260819.md").read_text()
    assert "No root-n expansion" in appendix and "M_C=" in appendix


def test_paired_covariance_is_not_removed_by_block_diagonal_derivative():
    # Fixed arrays illustrate a matrix identity; they are not new evidence cells.
    scores = np.array([[1, 3], [2, 4], [-1, -3], [-2, -4]], dtype=float)
    inverse_j = np.diag([0.5, 2.0])
    omega = np.cov(scores, rowvar=False, ddof=1)
    covariance = inverse_j @ omega @ inverse_j.T
    transformed = scores @ inverse_j.T
    np.testing.assert_allclose(covariance, np.cov(transformed, rowvar=False, ddof=1))
    projected_variance = np.var(transformed.sum(axis=1), ddof=1)
    assert np.isclose(projected_variance, covariance.sum())
    assert not np.isclose(projected_variance, np.trace(covariance))


def test_stored_completion_audit_is_current():
    stored = json.loads((ROOT / OUTPUT).read_text())
    assert stored == build_audit()


def test_draft_entry_preserves_open_application_and_review_decisions():
    entry = (ROOT / "docs/manuscript_review_frontmatter_20260910.md").read_text()
    review = (ROOT / "docs/manuscript_completion_review_20260910.md").read_text()
    assert "Provisional abstract" in entry
    assert "not a submission-ready manuscript" in entry
    assert "No dataset has passed this gate" in review
    assert "pending supervisor confirmation" in review
    assert "total variation" in review
    assert "population L2 with infinite fourth moments" in review
