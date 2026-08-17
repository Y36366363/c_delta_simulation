from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.run_profile_bridge_family_validation_20260817 import (
    BRIDGE_FAMILIES,
    generate_family_bridge_profile_null,
    run_family_cell,
    sample_unit_origin_density_radius,
)


def test_bridge_families_have_expected_support_and_finite_values():
    rng = np.random.default_rng(1)
    for family in BRIDGE_FAMILIES:
        values = sample_unit_origin_density_radius(rng, 1000, family)
        assert values.shape == (1000,)
        assert np.all(values >= 0.0)
        assert np.all(np.isfinite(values))


def test_matched_density_family_generator_preserves_profile_weak_null():
    rng = np.random.default_rng(2)
    for family in BRIDGE_FAMILIES:
        x, y = generate_family_bridge_profile_null(
            rng,
            5000,
            radial_log_sd=0.1,
            bridge_probability=0.2,
            bridge_family=family,
        )
        profile_correlation = np.corrcoef(
            huber_reference_profile(x), huber_reference_profile(y)
        )[0, 1]
        assert abs(profile_correlation) < 0.06


def test_family_cell_records_matched_identification_quantities():
    row = run_family_cell(
        repetitions=4,
        n=80,
        n_perm=9,
        n_bootstrap=9,
        seed=3,
        phase="test",
        bridge_probability=0.1,
        bridge_family="half_normal",
    )
    assert row["origin_radius_density"] == 1.0
    assert row["marginal_origin_density"] == 0.05
    assert np.isclose(row["n_epsilon_squared"], 0.8)
    assert 0.0 <= row["studentized_rejection"] <= 1.0
