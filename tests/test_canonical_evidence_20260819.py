from pathlib import Path

import numpy as np

from scripts.freeze_canonical_evidence_20260819 import (
    PROJECT_ROOT,
    estimand_audit,
    freeze_bridge_recovery,
    freeze_family_residual,
    freeze_near_degenerate_failure,
    freeze_regular_calibration,
    wilson,
)


def test_wilson_interval_contains_observed_rate():
    low, high = wilson(15, 300)
    assert low < 0.05 < high


def test_four_canonical_groups_have_expected_fixed_rows_and_uncertainty():
    groups = {
        "regular": freeze_regular_calibration(),
        "failure": freeze_near_degenerate_failure(),
        "recovery": freeze_bridge_recovery(),
        "residual": freeze_family_residual(),
    }
    assert {name: len(rows) for name, rows in groups.items()} == {
        "regular": 3,
        "failure": 3,
        "recovery": 24,
        "residual": 4,
    }
    for rows in groups.values():
        for row in rows:
            assert Path(PROJECT_ROOT / row["source_file"]).exists()
            assert row["wilson_95_low"] <= row["rejection_rate"]
            assert row["rejection_rate"] <= row["wilson_95_high"]
            assert row["monte_carlo_se"] >= 0.0
            assert len(row["source_sha256"]) == 64


def test_conditioning_index_orders_severe_and_recovered_bridge_cells():
    rows = freeze_bridge_recovery()
    severe = [row for row in rows if np.isclose(row["sqrt_n_sigma_min_j"], 0.22, atol=0.01)]
    recovered = [row for row in rows if row["sqrt_n_sigma_min_j"] > 1.7]
    assert min(row["rejection_rate"] for row in severe) >= 0.50
    assert max(row["rejection_rate"] for row in recovered) <= 0.055


def test_estimand_audit_supports_profile_correlation_as_primary():
    rows = {row["criterion"]: row for row in estimand_audit()}
    assert rows["algebraic_identity"]["value"] < 2e-15
    assert rows["permutation_p_equivalence"]["value"] == 0.0
    assert rows["fixed_rho_population_C_range"]["value"] > 2.5
    assert rows["estimand_decision"]["value"] == "rho_P primary; C secondary"
