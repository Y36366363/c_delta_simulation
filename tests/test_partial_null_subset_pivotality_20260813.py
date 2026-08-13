import numpy as np

from scripts.run_partial_null_subset_pivotality_20260813 import (
    _max_t_outcomes,
    _raw_components,
    calibrate_mantel_null,
    make_mantel_null_profile_alt,
    make_profile_null_mantel_alt,
)


def test_partial_null_generators_have_declared_shapes_and_signals():
    rng = np.random.default_rng(13)
    x, y, blocks = make_profile_null_mantel_alt(rng, size=24)
    assert x.shape == y.shape == blocks.shape == (24,)
    assert np.unique(blocks).tolist() == [0]

    x, y, blocks = make_mantel_null_profile_alt(rng, mixing=0.0528)
    profile, _ = _raw_components(x, y)
    assert x.shape == y.shape == blocks.shape == (60,)
    assert profile > 0.7


def test_mantel_zero_effect_calibration_brackets_target():
    result = calibrate_mantel_null(seed=14, repetitions=1_000)
    assert 0.04 < result["mixing"] < 0.07
    assert abs(result["mean_mantel_effect"]) < 1e-4
    assert result["mean_profile_effect"] > 0.75


def test_max_t_outcomes_preserve_component_adjustment_identities():
    observed = np.asarray((0.50, 0.25))
    permuted = np.asarray(
        ((0.10, 0.20), (0.30, -0.10), (-0.20, 0.40), (0.05, 0.00))
    )
    result = _max_t_outcomes(observed, permuted)
    assert result["adjusted_profile_p"] >= result["profile_p"]
    assert result["adjusted_mantel_p"] >= result["mantel_p"]
    assert result["standardized_max_p"] == min(
        result["adjusted_profile_p"], result["adjusted_mantel_p"]
    )
