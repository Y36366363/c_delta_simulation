from pathlib import Path
import csv
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.audit_novelty_claims_20260903 import (
    contribution_adjudication,
    novelty_evidence_audit,
    rho_complete_if_validation,
)


def test_primary_rho_complete_if_converges_in_every_smooth_direction():
    rows = rho_complete_if_validation()
    assert len(rows) == 12
    by_point: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_point.setdefault(str(row["point"]), []).append(row)
    assert len(by_point) == 4
    for point_rows in by_point.values():
        ordered = sorted(point_rows, key=lambda row: float(row["epsilon"]))
        errors = [float(row["scaled_error"]) for row in ordered]
        assert errors[0] < errors[1] < errors[2]
        assert errors[0] < 5e-4


def test_primary_rho_validation_exercises_reference_and_mad_paths():
    rows = [row for row in rho_complete_if_validation() if row["epsilon"] == 1e-6]
    assert max(abs(float(row["reference_location_component"])) for row in rows) > 0.1
    assert max(abs(float(row["mad_indirect_component"])) for row in rows) > 0.01


def test_three_component_evidence_audit_passes_and_keeps_residual_visible():
    rows = novelty_evidence_audit()
    assert len(rows) == 13
    assert all(int(row["passed"]) for row in rows)
    components = {row["novelty_component"] for row in rows}
    assert components == {
        "complete_generated_profile_inference",
        "reference_switching_distortion",
        "conditioning_diagnostic",
    }
    residual = next(
        row for row in rows if row["check"] == "prospective_family_systematic_residual"
    )
    assert float(residual["observed"]) > 0.0


def test_adjudication_separates_general_precedent_from_specific_advance():
    rows = contribution_adjudication()
    assert len(rows) == 3
    assert all(row["general_precedent"] for row in rows)
    assert all(row["project_specific_advance"] for row in rows)
    assert all(row["prohibited_overclaim"] for row in rows)


def test_generated_tables_match_current_audit_objects():
    expected = {
        "rho_p_population_if_validation_20260903.tsv": 12,
        "novelty_claim_evidence_audit_20260903.tsv": 13,
        "novelty_contribution_adjudication_20260903.tsv": 3,
    }
    for filename, row_count in expected.items():
        with (PROJECT_ROOT / "results" / filename).open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        assert len(rows) == row_count


def test_novelty_note_preserves_all_frozen_claim_boundaries():
    text = (
        PROJECT_ROOT / "docs" / "novelty_claim_adjudication_20260903.md"
    ).read_text()
    normalized = " ".join(text.split()).lower()
    for required in (
        "pointwise, not uniform",
        "can cause, not always causes",
        "first-order organizer, not a universal cutoff",
        "robust reference, not a globally robust correlation",
        "no further general distribution grid",
    ):
        assert required in normalized
    for forbidden in ("first-ever", "universally valid", "necessary and sufficient for failure"):
        assert forbidden not in normalized
