import csv
from pathlib import Path

import numpy as np

from scripts.freeze_canonical_evidence_20260819 import (
    PROJECT_ROOT,
    estimand_audit,
    freeze_bridge_recovery,
    freeze_family_residual,
    freeze_near_degenerate_failure,
    freeze_regular_calibration,
    normalized_text_sha256,
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
            source = Path(PROJECT_ROOT / row["source_file"])
            assert source.exists()
            assert row["wilson_95_low"] <= row["rejection_rate"]
            assert row["rejection_rate"] <= row["wilson_95_high"]
            assert row["monte_carlo_se"] >= 0.0
            assert row["source_sha256"] == normalized_text_sha256(source)
            assert row["inference_track"] == "fully_recomputed_studentized_permutation_empirical"
            assert "not direct validation of iid Wald theorem" in row["theorem_alignment"]


def test_stored_canonical_table_matches_regenerated_rows():
    regenerated = (
        freeze_regular_calibration()
        + freeze_near_degenerate_failure()
        + freeze_bridge_recovery()
        + freeze_family_residual()
    )
    path = PROJECT_ROOT / "results" / "canonical_evidence_20260819.tsv"
    with path.open(newline="") as stream:
        stored = list(csv.DictReader(stream, delimiter="\t"))
    assert len(stored) == len(regenerated) == 34
    for observed, expected in zip(stored, regenerated, strict=True):
        for key in (
            "evidence_group",
            "inference_track",
            "theorem_alignment",
            "source_file",
            "source_sha256",
            "scenario",
            "notes",
        ):
            assert observed[key] == str(expected[key])
        for key in (
            "n",
            "repetitions",
            "n_perm",
            "root_seed",
            "rejections",
            "rejection_rate",
            "monte_carlo_se",
            "wilson_95_low",
            "wilson_95_high",
        ):
            assert np.isclose(float(observed[key]), float(expected[key]), atol=1e-14)


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


def test_canonical_hash_is_invariant_to_lf_and_crlf(tmp_path):
    lf = tmp_path / "lf.tsv"
    crlf = tmp_path / "crlf.tsv"
    lf.write_bytes(b"a\tb\n1\t2\n")
    crlf.write_bytes(b"a\tb\r\n1\t2\r\n")
    assert normalized_text_sha256(lf) == normalized_text_sha256(crlf)
