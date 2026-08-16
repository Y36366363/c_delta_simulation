import numpy as np

from scripts.run_profile_diagnostic_scaling_20260816 import (
    binary_auc,
    bootstrap_reference_diagnostics,
    centre_density_diagnostics,
    fit_huber_reference,
    run_path_cell,
)
from scripts.run_bootstrap_reference_precision_20260816 import (
    prefix_spreads,
    run_precision,
)


def test_huber_reference_is_affine_equivariant():
    values = np.array([-3.0, -1.0, 0.0, 0.4, 1.1, 8.0])
    fitted = fit_huber_reference(values)
    transformed = fit_huber_reference(4.0 - 2.5 * values)
    assert np.isclose(transformed, 4.0 - 2.5 * fitted)


def test_centre_density_diagnostics_are_affine_invariant():
    rng = np.random.default_rng(10)
    values = rng.standard_t(5.0, size=100)
    original = centre_density_diagnostics(values)
    transformed = centre_density_diagnostics(7.0 - 3.0 * values)
    assert np.allclose(original, transformed)


def test_central_valley_detects_separated_modes():
    rng = np.random.default_rng(20)
    regular = rng.normal(size=400)
    separated = np.r_[rng.normal(-3.0, 0.15, 200), rng.normal(3.0, 0.15, 200)]
    _, regular_valley = centre_density_diagnostics(regular)
    _, separated_valley = centre_density_diagnostics(separated)
    assert separated_valley < 0.25 * regular_valley


def test_bootstrap_reference_is_less_stable_for_separated_modes():
    rng = np.random.default_rng(30)
    regular = rng.normal(size=120)
    separated = np.r_[rng.normal(-2.0, 0.05, 60), rng.normal(2.0, 0.05, 60)]
    regular_spread, _ = bootstrap_reference_diagnostics(
        regular, n_bootstrap=199, rng=rng
    )
    separated_spread, separated_shift = bootstrap_reference_diagnostics(
        separated, n_bootstrap=199, rng=rng
    )
    assert separated_spread > regular_spread
    assert separated_shift > 0.10


def test_binary_auc_has_expected_orientation_and_ties():
    event = np.array([False, False, True, True])
    assert binary_auc(np.array([0.0, 1.0, 2.0, 3.0]), event) == 1.0
    assert binary_auc(np.ones(4), event) == 0.5


def test_path_smoke_returns_all_diagnostics():
    row = run_path_cell(
        repetitions=4,
        n=40,
        n_perm=9,
        n_bootstrap=9,
        seed=40,
        phase="test",
        radial_log_sd=0.2,
    )
    assert row["n"] == 40
    assert 0.0 <= row["studentized_rejection"] <= 1.0
    assert row["median_spacing_risk"] > 0.0
    assert row["median_valley_density_iqr"] >= 0.0
    assert row["median_bootstrap_reference_spread"] >= 0.0


def test_bootstrap_prefix_spreads_use_all_requested_prefixes():
    rng = np.random.default_rng(50)
    spreads = prefix_spreads(
        rng.normal(size=40), rng.normal(size=40), rng=rng
    )
    assert set(spreads) == {39, 79, 199, 399}
    assert all(value >= 0.0 for value in spreads.values())


def test_bootstrap_precision_reference_row_is_exact():
    rows = run_precision(
        repetitions=4,
        n=40,
        seed=60,
        phase="test",
        scenario="radial_0p1",
    )
    reference = rows[-1]
    assert reference["n_bootstrap"] == 399
    assert reference["correlation_with_b399"] == 1.0
    assert reference["median_absolute_error_vs_b399"] == 0.0
