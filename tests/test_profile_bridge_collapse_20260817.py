import numpy as np

from scripts.summarize_profile_bridge_calibration_20260817 import (
    fit_collapse_models,
)


def test_free_collapse_recovers_probability_exponent_two():
    n = np.array([50, 50, 200, 200, 800, 800], dtype=float)
    probability = np.array([0.05, 0.10, 0.025, 0.05, 0.0125, 0.025])
    linear_predictor = 0.5 - 0.8 * np.log(n * probability**2)
    rejection = 1.0 / (1.0 + np.exp(-linear_predictor))
    rows = fit_collapse_models(n, probability, rejection, repetitions=100_000)
    free = rows[-1]
    assert abs(free["implied_probability_exponent"] - 2.0) < 0.01
    assert free["r_squared"] > 0.999
