import numpy as np

from scripts.run_nuisance_jacobian_20260817 import (
    BRIDGE_FAMILIES,
    bridge_cdf,
    bridge_pdf,
    population_nuisance,
    skew_lognormal_distribution,
    symmetric_bridge_distribution,
)


def test_all_bridge_families_have_unit_right_density_at_zero():
    for family in BRIDGE_FAMILIES:
        assert bridge_pdf(0.0, family) == 1.0
        assert bridge_cdf(0.0, family) == 0.0


def test_symmetric_jacobian_matches_finite_difference_and_decouples_scale():
    result = population_nuisance(symmetric_bridge_distribution(0.1, "uniform"))
    assert result["finite_difference_max_error"] < 2e-5
    assert abs(result["huber_scale_coupling"]) < 1e-8
    jacobian = result["jacobian"]
    assert np.allclose(jacobian, np.diag(np.diag(jacobian)), atol=1e-8)
    assert np.allclose(jacobian @ result["inverse_jacobian"], np.eye(3))


def test_skew_jacobian_restores_mad_asymmetry_and_huber_scale_coupling():
    result = population_nuisance(skew_lognormal_distribution())
    assert result["finite_difference_max_error"] < 2e-5
    assert abs(result["standardized_mad_density_difference"]) > 0.01
    assert abs(result["huber_scale_coupling"]) > 0.01
    assert np.isfinite(result["jacobian_condition_number"])
