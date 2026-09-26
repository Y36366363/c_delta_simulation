"""Negative controls for exact evidence joins and deterministic affine checks."""
import pytest
from scripts.audit_record_identity_20260925 import (
    AuditFailure, RESULT_FILES, affine_case, read_tsv, validate_records,
)


@pytest.fixture(scope="module")
def evidence():
    return tuple(read_tsv(path) for path in RESULT_FILES[:3])


def changed_row(rows, field, value):
    result = list(rows)
    result[0] = {**result[0], field: value}
    return result


def test_complete_frozen_record_grid_and_join(evidence):
    result = validate_records(*evidence)
    assert result["datasets"] == 6000
    assert result["method_rows"] == 18000
    assert result["exact_marginal_residuals"] == 12000


@pytest.mark.parametrize("table,field,value", [
    (1, "replication", "999999"),
    (1, "root_seed", "999999"),
    (1, "truth", "0.25"),
    (0, "replication", "999999"),
    (0, "root_seed", "999999"),
    (0, "truth", "0.25"),
    (0, "method", "unplanned_method"),
])
def test_invalid_identity_or_truth_is_rejected(evidence, table, field, value):
    rows = list(evidence)
    rows[table] = changed_row(rows[table], field, value)
    with pytest.raises(AuditFailure):
        validate_records(*rows)


@pytest.mark.parametrize("table", [0, 1])
def test_duplicate_replacing_a_missing_record_is_rejected(evidence, table):
    rows = list(evidence)
    rows[table] = list(rows[table])
    rows[table][1] = dict(rows[table][0])
    with pytest.raises(AuditFailure, match="duplicate"):
        validate_records(*rows)


@pytest.mark.parametrize("table", [0, 1])
def test_dropped_record_is_rejected(evidence, table):
    rows = list(evidence)
    rows[table] = rows[table][1:]
    with pytest.raises(AuditFailure, match="row count"):
        validate_records(*rows)


@pytest.mark.parametrize("table,error", [(0, "0"), (1, "False"), (1, " "), (0, None)])
def test_only_empty_error_string_means_success(evidence, table, error):
    rows = list(evidence)
    rows[table] = changed_row(rows[table], "error", error)
    with pytest.raises(AuditFailure, match="error field"):
        validate_records(*rows)


@pytest.mark.parametrize("field,value", [
    ("x_exact_residual_passed", "False"),
    ("x_score_exact_numerator", "999999999999999999999999999999999999999"),
    ("x_score_exact_denominator", "0"),
    ("x_tolerance", "0.1"),
    ("y_score_exact_float", "nan"),
])
def test_residual_flags_and_exact_inequality_are_rechecked(evidence, field, value):
    rows = list(evidence)
    rows[1] = changed_row(rows[1], field, value)
    with pytest.raises(AuditFailure):
        validate_records(*rows)


def test_population_anchor_cannot_drift_with_all_row_truths(evidence):
    rows = [[{**r, "truth": "0.25"} for r in evidence[0]],
            [{**r, "truth": "0.25"} for r in evidence[1]],
            [{**r, "rho_p": "0.25"} for r in evidence[2]]]
    with pytest.raises(AuditFailure, match="reference truth"):
        validate_records(*rows)


@pytest.mark.parametrize("n", [95, 96])
def test_score_checked_signed_affine_laws_and_exact_equality_qualification(n):
    cases = affine_case(n)
    positive, reflection = cases
    assert positive["max_if_gap"] < 2e-9
    assert reflection["max_equality_prediction_error"] < 2e-9
    if n % 2:
        assert reflection["equality_counts"]["x"]["median"] == 1
        assert reflection["equality_counts"]["x"]["mad_boundary"] == 1
        assert reflection["max_if_gap"] > 1e-4
        assert abs(reflection["standard_error_gap"]) > 1e-10
    else:
        assert reflection["equality_counts"]["x"]["median"] == 0
        assert reflection["max_if_gap"] < 2e-9
