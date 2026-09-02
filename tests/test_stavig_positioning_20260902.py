from pathlib import Path
import csv
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.audit_stavig_positioning_20260902 import (
    positioning_audit,
    positioning_rows,
    target_separation_rows,
)


def test_constructive_stavig_positioning_audit_passes_without_a_grid():
    rows = positioning_audit()
    assert len(rows) == 7
    assert all(int(row["passed"]) for row in rows)


def test_witnesses_separate_signed_agreement_from_radial_profile_agreement():
    rows = {row["scenario"]: row for row in target_separation_rows()}
    reversal = rows["global_sign_reversal"]
    rewired = rows["within_radius_sign_rewiring"]
    assert float(reversal["rho_p"]) > 1.0 - 1e-14
    assert float(reversal["stavig_interval_r_ad"]) < 0.0
    assert float(rewired["rho_p"]) > 1.0 - 1e-14
    assert abs(float(rewired["stavig_interval_r_ad"]) - 1.0) > 0.20


def test_positioning_table_contains_two_stavig_definitions_and_core_alternatives():
    rows = positioning_rows()
    methods = {row["method"] for row in rows}
    assert len(rows) == 10
    assert {"Stavig ranked r_ad", "Stavig interval r_AD"} <= methods
    assert {"Hoorn c_d", "distance correlation", "Mantel statistic/test"} <= methods
    assert all(row["primary_source"] for row in rows)


def test_generated_tables_match_the_audited_objects():
    paths_and_lengths = {
        "stavig_target_separation_20260902.tsv": len(target_separation_rows()),
        "classical_alternative_positioning_20260902.tsv": len(positioning_rows()),
        "stavig_positioning_audit_20260902.tsv": len(positioning_audit()),
    }
    for filename, expected_length in paths_and_lengths.items():
        with (PROJECT_ROOT / "results" / filename).open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        assert len(rows) == expected_length


def test_positioning_note_preserves_novelty_and_claim_boundaries():
    text = (
        PROJECT_ROOT / "docs" / "novelty_and_classical_positioning_20260902.md"
    ).read_text()
    normalized = " ".join(text.split()).lower()
    for required in (
        "pointwise, not uniform",
        "can cause, not always causes",
        "first-order organizer, not a universal cutoff",
        "robust reference, not a globally robust correlation",
        "not an exhaustive proof of absence",
    ):
        assert required in normalized
    for forbidden in ("first ever", "no previous method", "universally valid"):
        assert forbidden not in normalized
