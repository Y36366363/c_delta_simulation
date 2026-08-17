import numpy as np

from scripts.run_profile_bridge_family_nuisance_20260817 import (
    fixed_mad_scale,
    margin_joint_bootstrap_instability,
    run_family_nuisance,
)


def test_mad_scale_is_scale_equivariant():
    values = np.array([-2.0, -1.0, 0.0, 0.5, 3.0])
    assert np.isclose(fixed_mad_scale(4.0 - 3.0 * values), 3.0 * fixed_mad_scale(values))


def test_joint_bootstrap_diagnostics_are_affine_invariant():
    rng = np.random.default_rng(1)
    values = rng.normal(size=100)
    first = margin_joint_bootstrap_instability(values, n_bootstrap=99, rng=rng)
    rng = np.random.default_rng(1)
    values = rng.normal(size=100)
    second = margin_joint_bootstrap_instability(
        5.0 - 2.0 * values, n_bootstrap=99, rng=rng
    )
    assert np.allclose(first, second)


def test_nuisance_smoke_returns_joint_metrics():
    row = run_family_nuisance(
        repetitions=4,
        n=40,
        n_perm=9,
        n_bootstrap=9,
        seed=2,
        bridge_probability=0.05,
        bridge_family="uniform",
    )
    assert row["median_location_spread"] >= 0.0
    assert row["median_log_mad_scale_spread"] >= 0.0
    assert row["median_minimum_scale_iqr_ratio"] >= 0.0
