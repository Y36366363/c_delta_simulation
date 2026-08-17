from pathlib import Path
import sys

import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.run_profile_bridge_calibration_20260817 import (
    generate_bridge_profile_null,
    run_cell,
)


def test_bridge_generator_rejects_invalid_probability():
    rng = np.random.default_rng(1)
    with pytest.raises(ValueError):
        generate_bridge_profile_null(
            rng, 40, radial_log_sd=0.1, bridge_probability=1.1
        )


def test_bridge_generator_preserves_population_profile_weak_null():
    rng = np.random.default_rng(2)
    x, y = generate_bridge_profile_null(
        rng, 6000, radial_log_sd=0.1, bridge_probability=0.2
    )
    profile_correlation = np.corrcoef(
        huber_reference_profile(x), huber_reference_profile(y)
    )[0, 1]
    assert abs(profile_correlation) < 0.05
    assert np.corrcoef(x, y)[0, 1] > 0.5


def test_positive_bridge_adds_observations_near_zero():
    rng = np.random.default_rng(3)
    without_x, _ = generate_bridge_profile_null(
        rng, 2000, radial_log_sd=0.1, bridge_probability=0.0
    )
    with_x, _ = generate_bridge_profile_null(
        rng, 2000, radial_log_sd=0.1, bridge_probability=0.2
    )
    assert np.mean(np.abs(with_x) < 0.2) > 0.02
    assert np.mean(np.abs(without_x) < 0.2) == 0.0


def test_calibration_smoke_reports_warning_decomposition():
    row = run_cell(
        repetitions=4,
        n=40,
        n_perm=9,
        n_bootstrap=9,
        seed=4,
        phase="test",
        design="bridge",
        radial_log_sd=0.1,
        bridge_probability=0.05,
    )
    assert row["scenario"] == "sigma_0.1_bridge_0.05"
    assert 0.0 <= row["bootstrap_warning_rate"] <= 1.0
    assert 0.0 <= row["structural_warning_rate"] <= 1.0
    assert row["median_sqrt_n_bootstrap_spread"] >= 0.0
