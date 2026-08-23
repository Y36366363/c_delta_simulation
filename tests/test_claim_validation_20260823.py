import csv

import numpy as np

from scripts.run_claim_validation_20260823 import (
    PROJECT_ROOT,
    fixed_center_profile_test,
    run_claim3,
)


def _read(name: str) -> list[dict[str, str]]:
    with (PROJECT_ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_fixed_center_profile_uses_only_independent_radii():
    rng = np.random.default_rng(2026082302)
    signs = rng.choice((-1.0, 1.0), 500)
    radius_x = np.exp(0.2 * rng.normal(size=500))
    radius_y = np.exp(0.2 * rng.normal(size=500))
    result = fixed_center_profile_test(signs * radius_x, signs * radius_y)
    assert np.isclose(result["estimate"], np.corrcoef(radius_x, radius_y)[0, 1])


def test_claim1_regular_confirmation_and_skew_boundary_are_frozen():
    rows = _read("claim1_wald_validation_20260823.tsv")
    assert len(rows) == 6
    regular_dependent = [row for row in rows if row["design_role"] == "regular_dependent_weak_null"]
    assert all(
        float(row["wilson_95_low"]) <= 0.05 <= float(row["wilson_95_high"])
        for row in regular_dependent
    )
    skew = sorted(
        (row for row in rows if row["design_role"] == "regular_slow_convergence_stress"),
        key=lambda row: int(row["n"]),
    )
    assert float(skew[0]["rejection_rate"]) > 0.10
    assert float(skew[1]["rejection_rate"]) < float(skew[0]["rejection_rate"])


def test_claim2_paired_fixed_reference_isolates_severe_fitting_distortion():
    rows = _read("claim2_reference_mechanism_validation_20260823.tsv")
    severe = [row for row in rows if np.isclose(float(row["radial_log_sd"]), 0.10)]
    recovered = [row for row in rows if np.isclose(float(row["radial_log_sd"]), 0.40)]
    assert min(float(row["paired_rejection_rate_difference"]) for row in severe) > 0.45
    assert all(
        float(row["fixed_center_wilson_95_low"]) <= 0.05 <= float(row["fixed_center_wilson_95_high"])
        for row in severe
    )
    assert max(abs(float(row["paired_rejection_rate_difference"])) for row in recovered) < 0.025


def test_claim3_leave_one_family_out_gain_regenerates_and_preserves_limitation():
    predictions, summaries = run_claim3()
    pooled = next(row for row in summaries if row["held_out_family"] == "pooled")
    assert pooled["mae_improvement_fraction"] > 0.70
    assert pooled["log_loss_improvement_fraction"] > 0.10
    family_rows = [row for row in summaries if row["held_out_family"] != "pooled"]
    assert all(row["weighted_lofo_mae"] < row["weighted_baseline_mae"] for row in family_rows)
    assert all(float(row["training_logit_log_index_slope"]) < 0.0 for row in predictions)
    # Nonzero held-out error is retained: the index organizes but does not
    # completely explain family-specific finite-sample behavior.
    assert max(row["weighted_lofo_mae"] for row in family_rows) > 0.05
