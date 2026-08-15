import numpy as np

from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
    run_stress,
)


def test_stress_generators_are_finite_and_reproducible():
    scenarios = (
        "independent_t5",
        "independent_t3_infinite_fourth",
        "independent_strong_skew",
        "profile_null_t5_sign_link",
        "profile_null_near_constant",
        "mantel_null_profile_alt",
    )
    for scenario in scenarios:
        first = generate_stress_scenario(
            np.random.default_rng(11), scenario, 40, 0.65
        )
        second = generate_stress_scenario(
            np.random.default_rng(11), scenario, 40, 0.65
        )
        assert np.all(np.isfinite(first[0]))
        assert np.all(np.isfinite(first[1]))
        assert np.array_equal(first[0], second[0])
        assert np.array_equal(first[1], second[1])


def test_stress_smoke_returns_all_scenarios_and_valid_rates():
    rows = run_stress(
        repetitions=3,
        n=40,
        n_perm=9,
        seed=2026081453,
        phase="unit",
    )
    assert len(rows) == 6
    for row in rows:
        assert row["valid_repetitions"] > 0
        assert 0.0 <= row["failure_rate"] <= 1.0
        assert 0.0 <= row["holm_true_null_fwer"] <= 1.0
