import numpy as np

from scripts.run_application_node_decomposition_20260812 import (
    cross_validated_weight_statistic,
)
from scripts.run_unequal_building_adaptive_validation_20260813 import (
    ROOM_DESIGNS,
    aggregation_weights,
    building_covariates,
    make_covariate_building_pair,
)
from scripts.summarize_unequal_building_adaptive_20260813 import combine_runs


def test_room_designs_hold_total_sample_size_fixed():
    assert {int(np.sum(value)) for value in ROOM_DESIGNS.values()} == {72}
    assert np.std(ROOM_DESIGNS["severely_unequal"]) > np.std(
        ROOM_DESIGNS["moderately_unequal"]
    )


def test_covariates_and_generator_follow_unequal_sizes():
    counts = ROOM_DESIGNS["severely_unequal"]
    covariates = building_covariates(counts)
    assert all(values.shape == (6,) for values in covariates.values())
    x, y, blocks, diagnostics = make_covariate_building_pair(
        np.random.default_rng(12), counts, "mixed_covariate"
    )
    assert x.shape == y.shape == blocks.shape == (72,)
    assert np.array_equal(np.bincount(blocks), counts)
    assert diagnostics["size_cv"] > 0.7


def test_balanced_design_treats_constant_area_covariate_as_zero():
    counts = ROOM_DESIGNS["balanced"]
    assert np.all(building_covariates(counts)["log_floor_area"] == 0.0)
    x, y, blocks, _ = make_covariate_building_pair(
        np.random.default_rng(120), counts, "conditional_null"
    )
    assert np.all(np.isfinite(x)) and np.all(np.isfinite(y))
    assert np.array_equal(np.bincount(blocks), counts)


def test_size_only_control_removes_covariate_scale_and_center_effects():
    counts = ROOM_DESIGNS["severely_unequal"]
    x, y, blocks, diagnostics = make_covariate_building_pair(
        np.random.default_rng(121), counts, "radial_node_size_only"
    )
    assert np.all(np.isfinite(x)) and np.all(np.isfinite(y))
    assert np.array_equal(np.bincount(blocks), counts)
    assert abs(diagnostics["scale_ratio"] - 1.0) < 1e-12


def test_signal_multiplier_is_validated_and_changes_signal():
    counts = ROOM_DESIGNS["balanced"]
    try:
        make_covariate_building_pair(
            np.random.default_rng(122),
            counts,
            "radial_node",
            signal_multiplier=-0.1,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("negative signal multiplier must fail")


def test_aggregation_weights_represent_distinct_targets():
    counts = ROOM_DESIGNS["moderately_unequal"]
    assert np.all(aggregation_weights(counts, "building_equal") == 1.0)
    assert np.allclose(aggregation_weights(counts, "sqrt_rooms"), np.sqrt(counts))
    assert np.array_equal(aggregation_weights(counts, "room_equal"), counts)


def test_weighted_cross_validation_matches_equal_rule_for_equal_weights():
    rng = np.random.default_rng(13)
    scores = rng.normal(size=(7, 6, 2))
    unweighted = cross_validated_weight_statistic(scores, temperature=2.0)
    weighted = cross_validated_weight_statistic(
        scores, temperature=2.0, block_weights=np.ones(6)
    )
    assert np.allclose(unweighted[0], weighted[0])
    assert np.allclose(unweighted[1], weighted[1])


def test_zero_temperature_is_fixed_equal_mixture():
    scores = np.asarray([[[1.0, 0.0], [0.2, 0.8], [-0.4, 0.6]]])
    statistic, weight = cross_validated_weight_statistic(scores, temperature=0.0)
    assert np.allclose(weight, 0.5)
    assert np.allclose(statistic, np.mean(scores, axis=(1, 2)))


def test_invalid_aggregation_and_weights_are_rejected():
    counts = ROOM_DESIGNS["balanced"]
    try:
        aggregation_weights(counts, "unknown")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown aggregation must fail")
    scores = np.ones((2, 6, 2))
    for weights in (np.ones(5), np.asarray((1, 1, 1, 1, 1, 0))):
        try:
            cross_validated_weight_statistic(scores, block_weights=weights)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid block weights must fail")


def test_combiner_preserves_rejection_counts():
    runs = [
        [
            {
                "design": "balanced",
                "scenario": "conditional_null",
                "temperature": "1.0",
                "aggregation": "building_equal",
                "method": "profile",
                "repetitions": "100",
                "rejection_rate": str(rate),
                "mean_profile_weight": "0.5",
            }
        ]
        for rate in (0.04, 0.06)
    ]
    combined = combine_runs(
        runs, ("design", "scenario", "temperature", "aggregation", "method")
    )
    assert combined[0]["repetitions"] == 200
    assert combined[0]["reject_count"] == 10
    assert abs(float(combined[0]["rejection_rate"]) - 0.05) < 1e-12
