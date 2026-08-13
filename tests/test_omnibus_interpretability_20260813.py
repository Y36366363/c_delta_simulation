from scripts.run_omnibus_interpretability_20260813 import (
    attribution_label,
    summarize_cell,
)
from scripts.summarize_omnibus_interpretability_20260813 import (
    combine_summary_rows,
)


def _outcome(profile_p, mantel_p, omnibus_p, winner="profile"):
    return {
        "profile_p": profile_p,
        "mantel_p": mantel_p,
        "standardized_max_p": omnibus_p,
        "adjusted_profile_p": profile_p,
        "adjusted_mantel_p": mantel_p,
        "standardized_winner": winner,
        "standardized_profile_z": 2.0,
        "standardized_mantel_z": 1.0,
        "winner_agreement_with_999": 1.0,
        "decision_agreement_with_999": 1.0,
        "attribution_agreement_with_999": 1.0,
    }


def test_attribution_labels_are_exhaustive():
    assert attribution_label(_outcome(0.01, 0.20, 0.01)) == "profile_only"
    assert attribution_label(_outcome(0.20, 0.01, 0.01)) == "mantel_only"
    assert attribution_label(_outcome(0.01, 0.01, 0.01)) == "both"
    assert attribution_label(_outcome(0.20, 0.20, 0.20)) == "unresolved"


def test_summary_rates_and_regret_are_coherent():
    records = [
        _outcome(0.01, 0.20, 0.01),
        _outcome(0.20, 0.01, 0.01, "mantel"),
        _outcome(0.01, 0.01, 0.01),
        _outcome(0.20, 0.20, 0.20),
    ]
    row = summarize_cell(
        records,
        phase="test",
        design="balanced",
        scenario="radial_node",
        strength=1.0,
        n_perm=999,
    )
    assert row["omnibus_rejection_rate"] == 0.75
    assert row["profile_only_rate"] == 0.25
    assert row["mantel_only_rate"] == 0.25
    assert row["both_rate"] == 0.25
    assert row["unresolved_rate"] == 0.25
    assert row["best_component_power"] == 0.5
    assert row["omnibus_regret"] == -0.25
    assert row["unresolved_share_given_reject"] == 0.0
    assert abs(
        row["profile_only_share_given_reject"]
        + row["mantel_only_share_given_reject"]
        + row["both_share_given_reject"]
        - 1.0
    ) < 1e-12


def test_seed_combiner_weights_rates_and_attribution_by_counts():
    base = summarize_cell(
        [_outcome(0.01, 0.20, 0.01), _outcome(0.20, 0.20, 0.20)],
        phase="seed1",
        design="balanced",
        scenario="radial_node",
        strength=1.0,
        n_perm=999,
    )
    rows = [{key: str(value) for key, value in base.items()} for _ in range(2)]
    combined = combine_summary_rows(
        rows, ("design", "scenario", "strength", "n_perm")
    )[0]
    assert combined["repetitions"] == 4
    assert combined["omnibus_reject_count"] == 2
    assert combined["omnibus_rejection_rate"] == 0.5
    assert combined["profile_only_share_given_reject"] == 1.0
    assert combined["unresolved_share_given_reject"] == 0.0
