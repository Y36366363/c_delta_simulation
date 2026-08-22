import csv

import numpy as np

from scripts.audit_pipeline_integrity_20260822 import PROJECT_ROOT, audit_pipeline
from scripts.audit_wald_convergence_20260822 import generate_regular_scenario


def test_current_pipeline_integrity_checks_pass():
    rows = audit_pipeline()
    assert all(int(row["passed"]) == 1 for row in rows)


def test_regular_dependent_weak_null_has_normal_margins_and_independent_radii():
    rng = np.random.default_rng(2026082202)
    x, y = generate_regular_scenario(rng, "profile_null_normal_sign_link", 100_000)
    assert np.mean(np.sign(x) == np.sign(y)) == 1.0
    assert abs(np.mean(x)) < 0.015
    assert abs(np.std(x) - 1.0) < 0.015
    assert abs(np.corrcoef(np.abs(x), np.abs(y))[0, 1]) < 0.015


def test_stored_wald_audit_has_fixed_complete_grid_and_uncertainty():
    path = PROJECT_ROOT / "results" / "wald_convergence_audit_20260822.tsv"
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == 18
    assert {row["inference_track"] for row in rows} == {"iid_full_if_wald"}
    assert all(int(row["repetitions"]) == 600 for row in rows)
    assert all(int(row["valid_repetitions"]) + int(row["failures"]) == 600 for row in rows)
    assert all(
        float(row["wilson_95_low"])
        <= float(row["rejection_rate"])
        <= float(row["wilson_95_high"])
        for row in rows
    )
