from pathlib import Path
import csv
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.audit_manuscript_integration_20260904 import (
    manuscript_claim_crosswalk,
    manuscript_integration_audit,
)


def test_manuscript_integration_audit_passes():
    rows = manuscript_integration_audit()
    assert len(rows) == 11
    assert all(int(row["passed"]) for row in rows)


def test_crosswalk_has_one_frozen_source_for_every_statement():
    rows = manuscript_claim_crosswalk()
    assert len(rows) == 16
    assert all((PROJECT_ROOT / row["source_file"]).exists() for row in rows)
    assert all(row["source_metric"] for row in rows)
    assert all(row["uncertainty_or_boundary"] for row in rows)


def test_crosswalk_keeps_evidence_types_and_claim_sections_separate():
    rows = manuscript_claim_crosswalk()
    assert {row["manuscript_location"] for row in rows} == {
        "3.4",
        "4.2",
        "5.2",
        "5.3",
    }
    assert len({row["evidence_type"] for row in rows}) >= 8
    assert any(row["evidence_type"] == "higher-order residual" for row in rows)


def test_generated_manuscript_tables_match_live_audits():
    expected = {
        "manuscript_claim_source_crosswalk_20260904.tsv": len(
            manuscript_claim_crosswalk()
        ),
        "manuscript_integration_audit_20260904.tsv": len(
            manuscript_integration_audit()
        ),
    }
    for filename, row_count in expected.items():
        with (PROJECT_ROOT / "results" / filename).open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        assert len(rows) == row_count


def test_manuscript_does_not_promote_population_index_to_a_gate():
    text = (
        PROJECT_ROOT / "docs" / "manuscript_draft_sections_3_5_20260904.md"
    ).read_text()
    assert "population quantities" in text
    assert "do not calibrate a threshold" in text
    assert "not a universal cutoff" in text
    assert "No further general distribution grid" not in text
