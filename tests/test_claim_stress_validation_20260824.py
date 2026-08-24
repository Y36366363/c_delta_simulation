import csv

from scripts.run_claim_stress_validation_20260824 import PROJECT_ROOT


def _read(name: str) -> list[dict[str, str]]:
    with (PROJECT_ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_claim1_studentization_diagnostic_separates_regular_and_skew_tails():
    rows = _read("claim1_studentization_diagnostics_validation_20260824.tsv")
    assert len(rows) == 6
    normal = [row for row in rows if row["scenario"] == "profile_null_normal_sign_link"]
    assert all(abs(float(row["reported_se_to_empirical_sd"]) - 1.0) < 0.02 for row in normal)
    assert all(float(row["wilson_95_low"]) <= 0.05 <= float(row["wilson_95_high"]) for row in normal)
    skew = [row for row in rows if row["scenario"] == "independent_strong_skew"]
    assert all(float(row["q025_studentized_z"]) < -2.7 for row in skew)
    assert all(float(row["q975_studentized_z"]) < 1.75 for row in skew)


def test_claim2_exact_balance_removes_switching_in_mechanism_intervention():
    rows = _read("claim2_sign_balance_intervention_validation_20260824.tsv")
    iid = [row for row in rows if row["sign_design"] == "iid_signs"]
    balanced = [row for row in rows if row["sign_design"] == "exactly_balanced_signs"]
    assert min(float(row["rejection_rate"]) for row in iid) > 0.50
    assert max(float(row["rejection_rate"]) for row in balanced) <= 0.06
    assert min(float(row["mean_maximum_absolute_huber_center"]) for row in iid) > 0.20
    assert max(float(row["mean_maximum_absolute_huber_center"]) for row in balanced) < 0.015


def test_claim2_sign_imbalance_gradient_is_monotone_descriptive_evidence():
    rows = _read("claim2_sign_imbalance_gradient_validation_20260824.tsv")
    for n in (80, 640):
        subset = sorted(
            (row for row in rows if int(row["n"]) == n),
            key=lambda row: int(row["imbalance_rank_quartile"]),
        )
        rejection = [float(row["rejection_rate"]) for row in subset]
        centres = [float(row["mean_maximum_absolute_huber_center"]) for row in subset]
        assert rejection == sorted(rejection)
        assert centres == sorted(centres)


def test_claim3_stricter_cross_validation_retains_large_baseline_gain():
    rows = _read("claim3_stricter_cv_summary_validation_20260824.tsv")
    assert {row["cv_scheme"] for row in rows} == {
        "cross_sample_size",
        "leave_conditioning_level_out",
    }
    assert all(float(row["mae_improvement_fraction"]) > 0.70 for row in rows)
    assert all(float(row["log_loss_improvement_fraction"]) > 0.17 for row in rows)
    assert all(float(row["maximum_training_log_index_slope"]) < 0.0 for row in rows)
