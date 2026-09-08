import csv
from pathlib import Path

import numpy as np

from scripts.audit_referee_readiness_20260908 import coverage_diagnostics, root_replay
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_frozen_tail_diagnostics_rebuild_with_exhaustive_accounting():
    stored = read("referee_coverage_diagnostics_20260908.tsv")
    rebuilt = coverage_diagnostics()
    assert len(stored) == len(rebuilt) == 12
    for a, b in zip(stored, rebuilt, strict=True):
        assert (
            int(a["n"]) == b["n"]
            and a["method"] == b["method"]
            and a["scale"] == b["scale"]
        )
        assert (
            b["coverage_count"]
            + b["below_truth_miss_count"]
            + b["above_truth_miss_count"]
            == b["valid"]
        )
        assert b["valid"] + b["failures"] == 2000
        for key in (
            "coverage",
            "wilson_low",
            "wilson_high",
            "error_se_correlation",
            "z_q025",
            "z_q975",
            "mean_interval_width",
            "paired_difference_mcse",
            "identity_mean_minus_u_delta",
            "identity_mean_remainder",
        ):
            assert np.isclose(float(a[key]), b[key], rtol=1e-12, atol=1e-12)
        assert b["wilson_low"] <= b["coverage"] <= b["wilson_high"]
        assert "not an interval recommendation" in b["scope"]
        assert b["identity_max_error"] < 1e-12
        assert (
            abs(
                b["z_mean"]
                - b["identity_mean_u"]
                - b["identity_mean_minus_u_delta"]
                - b["identity_mean_remainder"]
            )
            < 1e-12
        )


def test_root_replays_are_fixed_regular_samples_not_a_new_grid():
    rows = root_replay()
    assert len(rows) == 18
    assert {r["replication"] for r in rows} == {0, 1, 2}
    assert all(r["passed"] for r in rows)
    assert max(r["sqrt_n_score_residual"] for r in rows) < 1e-7
    stored = read("referee_root_replay_20260908.tsv")
    for a, b in zip(stored, rows, strict=True):
        assert (
            abs(
                float(a["root_difference_in_scale_units"])
                - b["root_difference_in_scale_units"]
            )
            < 1e-12
        )


def test_referee_diagnostic_manifest_is_current():
    for row in read("referee_diagnostics_manifest_20260908.tsv"):
        assert normalized_text_sha256(ROOT / row["path"]) == row["sha256_lf"]


def test_discussion_separates_infeasible_diagnosis_from_validated_methods():
    text = (ROOT / "docs/manuscript_draft_section_8_20260908.md").read_text()
    normalized = " ".join(text.split())
    for phrase in (
        "pointwise, not uniform",
        "can cause, not always causes",
        "first-order organizer, not a universal cutoff",
        "robust reference, not a globally robust correlation",
        "infeasible diagnostic, not a",
        "post hoc",
        "not a substitute",
        "independent mathematical peer review",
    ):
        assert phrase in normalized
    for left, right in ((r"\(", r"\)"), (r"\[", r"\]")):
        assert text.count(left) == text.count(right)


def test_readiness_is_not_reduced_to_typesetting_or_passed_unit_tests():
    skeleton = (ROOT / "docs/manuscript_skeleton_and_readiness_20260829.md").read_text()
    assert "Theory gate — independent review open" in skeleton
    assert "Theory gate — nearly passed" not in skeleton
    assert "Evidence gate — passed" not in skeleton
    review = (ROOT / "docs/referee_readiness_review_20260908.md").read_text()
    for phrase in (
        "not independent peer",
        "not submission-ready",
        "total variation",
        "AI assistance",
        "not an arbitrary-distribution",
    ):
        assert phrase in " ".join(review.split())


def test_appendix_requires_negligible_huber_equation_residual():
    text = (ROOT / "docs/appendix_asymptotic_theory_20260819.md").read_text()
    assert "approximate-root condition" in text
    assert "fixed iteration cap does not by itself" in text
    assert r"P_n\psi_c\{(W-\widehat T)/(k\widehat d)\}=o_P(n^{-1/2})" in text
