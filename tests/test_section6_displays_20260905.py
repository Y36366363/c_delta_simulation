import csv
from pathlib import Path

from scripts.audit_section6_displays_20260905 import section6_display_audit
from scripts.build_section6_displays_20260905 import (
    MECHANISM_TRACK,
    PERMUTATION_TRACK,
    WALD_TRACK,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


def _rows(filename):
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_section6_display_audit_passes():
    rows = section6_display_audit()
    assert len(rows) == 10
    assert all(int(row["passed"]) for row in rows)


def test_wald_table_has_only_regular_theorem_aligned_evidence():
    rows = _rows("section6_display_table2_wald_20260905.tsv")
    assert len(rows) == 6
    assert {row["evidence_track"] for row in rows} == {WALD_TRACK}
    assert {int(row["n"]) for row in rows} == {160, 320, 640, 2560}
    assert all("Theorem 1" in row["theorem_relation"] for row in rows)


def test_mechanism_display_is_not_labeled_as_wald_calibration():
    rows = _rows("section6_display_figure1_mechanism_20260905.tsv")
    assert len(rows) == 22
    assert {row["evidence_track"] for row in rows} == {MECHANISM_TRACK}
    assert all("not" in row["theorem_relation"] for row in rows)


def test_permutation_displays_are_separate_and_complete():
    bridge = _rows("section6_display_figure2_bridge_20260905.tsv")
    residual = _rows("section6_display_figure3_residual_20260905.tsv")
    assert len(bridge) == 24
    assert len(residual) == 10
    assert {row["evidence_track"] for row in bridge + residual} == {PERMUTATION_TRACK}
    assert {row["family"] for row in bridge} == {
        "exponential",
        "half_normal",
        "scaled_beta12",
        "uniform",
    }
    assert sum(row["evidence_component"] == "prospective_fifth_family_prediction" for row in residual) == 6


def test_figure_assets_and_section6_draft_are_present():
    for stem in (
        "manuscript_figure1_reference_switching_20260905",
        "manuscript_figure2_conditioning_bridge_20260905",
        "manuscript_figure3_family_residual_20260905",
    ):
        for extension in ("png", "pdf"):
            path = PROJECT_ROOT / "figures" / f"{stem}.{extension}"
            assert path.exists()
            assert path.stat().st_size > 10_000
    draft = (PROJECT_ROOT / "docs" / "manuscript_draft_section_6_20260905.md").read_text()
    assert "No main display combines the two tracks." in draft
    assert "not a weak-null permutation theorem" in draft
