import numpy as np

from scripts.run_profile_regularity_comparison_20260816 import (
    distance_correlation,
    generate_sign_link_profile_null,
    largest_interior_spacing_ratio,
    run_comparison,
    run_gate_cross_validation,
)


def test_gap_diagnostic_is_location_and_scale_invariant():
    rng = np.random.default_rng(161)
    values = rng.normal(size=80)
    original = largest_interior_spacing_ratio(values)
    transformed = largest_interior_spacing_ratio(7.0 - 3.5 * values)
    assert np.isclose(original, transformed)


def test_gap_diagnostic_separates_two_tight_modes_from_normal():
    rng = np.random.default_rng(162)
    normal = rng.normal(size=100)
    signs = np.repeat((-1.0, 1.0), 50)
    separated = signs * np.exp(0.03 * rng.normal(size=100))
    assert largest_interior_spacing_ratio(separated) > 0.85
    assert largest_interior_spacing_ratio(normal) < 0.50


def test_distance_correlation_detects_shared_sign_dependence():
    rng = np.random.default_rng(163)
    x, y = generate_sign_link_profile_null(rng, 400, 0.20)
    independent = rng.normal(size=400)
    assert distance_correlation(x, y) > distance_correlation(x, independent)


def test_regularity_comparison_smoke_has_valid_rank_p_values():
    rows = run_comparison(
        repetitions=3,
        n=40,
        n_perm=9,
        seed=2026081614,
        phase="unit",
        radial_log_sds=(0.03, 0.80),
    )
    assert len(rows) == 2
    for row in rows:
        assert 0.0 <= row["studentized_rejection"] <= 1.0
        assert 0.0 <= row["naive_rejection"] <= 1.0
        assert 0.0 <= row["gap_0p75_pass_rate"] <= 1.0


def test_gate_cross_validation_smoke_returns_requested_scenarios():
    rows = run_gate_cross_validation(
        repetitions=3,
        n=40,
        n_perm=9,
        seed=2026081615,
        phase="unit",
        scenarios=("independent_t5", "independent_affine_near_constant"),
    )
    assert [row["scenario"] for row in rows] == [
        "independent_t5",
        "independent_affine_near_constant",
    ]
    for row in rows:
        assert 0.0 <= row["gap_0p5_pass_rate"] <= 1.0
