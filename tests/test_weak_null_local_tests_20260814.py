import numpy as np

from scripts.run_weak_null_local_tests_20260814 import (
    _correlation_delta,
    holm_adjust,
    mantel_jackknife_test,
    mantel_weak_null_test,
    profile_jackknife_test,
    profile_weak_null_test,
)


def test_correlation_moment_gradient_matches_finite_difference():
    moments = np.asarray((2.1, 1.2, 1.5, 2.0, 2.8))  # ab, a, b, a2, b2
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    numerical = []
    epsilon = 1e-6
    for index in range(5):
        changed = moments.copy()
        changed[index] += epsilon
        value, _ = _correlation_delta(
            changed[1], changed[2], changed[0], changed[3], changed[4]
        )
        numerical.append((value - estimate) / epsilon)
    assert np.allclose(gradient, numerical, atol=2e-5)


def test_local_influence_functions_are_centered_and_finite():
    rng = np.random.default_rng(14)
    x = rng.normal(size=80)
    y = 0.2 * x + rng.normal(size=80)
    profile = profile_weak_null_test(x, y)
    mantel = mantel_weak_null_test(x, y)
    for result in (profile, mantel):
        assert np.isfinite(result["estimate"])
        assert result["standard_error"] > 0.0
        assert abs(np.mean(result["influence"])) < 1e-12
        assert 0.0 <= result["p_value"] <= 1.0


def test_full_refit_and_delete_node_jackknife_return_valid_tests():
    rng = np.random.default_rng(15)
    x = rng.standard_t(5, size=60)
    y = rng.standard_t(5, size=60)
    profile = profile_jackknife_test(x, y)
    mantel = mantel_jackknife_test(x, y)
    for result in (profile, mantel):
        assert result["leave_one_out"].shape == (60,)
        assert result["standard_error"] > 0.0
        assert 0.0 <= result["p_value"] <= 1.0


def test_holm_equals_two_hypothesis_closed_bonferroni_adjustment():
    profile, mantel = holm_adjust(0.01, 0.04)
    assert profile == 0.02
    assert mantel == 0.04
    profile, mantel = holm_adjust(0.20, 0.03)
    assert mantel == 0.06
    assert profile == 0.20
