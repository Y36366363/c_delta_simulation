import numpy as np

from scripts.run_studentized_permutation_weak_null_20260814 import (
    mantel_studentized_permutation_test,
    profile_studentized_permutation_test,
    random_indices,
)
from scripts.run_weak_null_local_tests_20260814 import holm_adjust


def test_fully_recomputed_studentized_permutation_returns_rank_p_values():
    rng = np.random.default_rng(141)
    x = rng.normal(size=30)
    y = rng.normal(size=30)
    indices = random_indices(rng, 30, 99)
    for result in (
        profile_studentized_permutation_test(x, y, indices),
        mantel_studentized_permutation_test(x, y, indices),
    ):
        assert result["permuted_z"].shape == (99,)
        assert np.all(np.isfinite(result["permuted_z"]))
        assert 0.0 < result["p_value"] <= 1.0
        assert abs(result["p_value"] * 100 - round(result["p_value"] * 100)) < 1e-10


def test_studentized_permutation_is_invariant_to_common_reordering():
    rng = np.random.default_rng(142)
    x = rng.normal(size=24)
    y = 0.3 * x + rng.normal(size=24)
    indices = random_indices(rng, 24, 49)
    order = rng.permutation(24)
    inverse = np.empty(24, dtype=int)
    inverse[order] = np.arange(24)
    reordered_indices = inverse[indices[:, order]]
    original = mantel_studentized_permutation_test(x, y, indices)
    reordered = mantel_studentized_permutation_test(
        x[order], y[order], reordered_indices
    )
    assert np.isclose(original["estimate"], reordered["estimate"])
    assert np.isclose(original["p_value"], reordered["p_value"])


def test_holm_adjustment_does_not_decrease_studentized_p_values():
    adjusted = holm_adjust(0.031, 0.12)
    assert adjusted[0] >= 0.031
    assert adjusted[1] >= 0.12
