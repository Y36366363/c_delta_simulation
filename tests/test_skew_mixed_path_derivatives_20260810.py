import numpy as np

from scripts.run_skew_mixed_path_derivatives_20260810 import (
    CONFIGURATIONS,
    combine_skew_power_runs,
    derivative_batch,
    estimate_skew_crossovers,
    huber_transport_fit,
    huber_population_transport_fit,
    order_statistic_value_derivative,
    skew_components,
)
from scripts.run_mixed_path_local_slopes_20260810 import mixture_value_and_tangent


def test_order_statistic_derivative_matches_stable_central_difference():
    values = np.asarray([-2.0, -0.4, 0.2, 1.1, 3.0])
    velocities = np.asarray([0.3, -0.1, 0.7, 0.2, -0.4])
    median, derivative = order_statistic_value_derivative(values, velocities)
    epsilon = 1e-6
    finite = (
        np.median(values + epsilon * velocities)
        - np.median(values - epsilon * velocities)
    ) / (2.0 * epsilon)
    assert median == 0.2
    assert abs(derivative - finite) < 1e-9


def test_huber_transport_location_derivative_matches_complete_refit():
    rng = np.random.default_rng(20261069)
    configuration = CONFIGURATIONS[0]
    node_x, _, dyad_x, _ = skew_components(rng, 100_000, configuration)
    weight = float(configuration["weight"])
    values, velocities = mixture_value_and_tangent(node_x, dyad_x, weight)
    fit = huber_transport_fit(values, velocities)
    epsilon = 1e-5
    plus, _ = mixture_value_and_tangent(node_x, dyad_x, weight + epsilon)
    minus, _ = mixture_value_and_tangent(node_x, dyad_x, weight - epsilon)
    plus_fit = huber_transport_fit(plus, np.zeros_like(plus))
    minus_fit = huber_transport_fit(minus, np.zeros_like(minus))
    finite = (plus_fit["location"] - minus_fit["location"]) / (2.0 * epsilon)
    assert abs(fit["location_dot"] - finite) < 2e-4


def test_small_skew_batch_full_derivatives_match_refits():
    rng = np.random.default_rng(20261072)
    rows = derivative_batch(
        rng, 80_000, CONFIGURATIONS[0], epsilons=(0.0005,)
    )
    assert len(rows) == 3
    assert max(abs(float(row["derivative_check_error"])) for row in rows) < 0.01
    profile_rows = [row for row in rows if row["method"] != "mantel"]
    assert any(abs(float(row["mad_indirect_effect_component"])) > 1e-5 for row in profile_rows)


def test_population_transport_fit_respects_pure_translation():
    rng = np.random.default_rng(20261073)
    values = rng.lognormal(mean=0.0, sigma=0.7, size=150_000)
    velocity = np.full(values.size, 0.37)
    fit = huber_population_transport_fit(values, velocity)
    assert abs(fit["median_dot"] - 0.37) < 1e-10
    assert abs(fit["mad_dot"]) < 1e-10
    assert abs(fit["location_dot"] - 0.37) < 1e-10
    assert abs(fit["mad_indirect_location_dot"]) < 1e-10


def test_skew_power_combination_and_crossover_interpolation():
    base = {
        "configuration": "synthetic",
        "repetitions": 100,
        "n_perm": 199,
        "both_reject": 20,
        "neither_reject": 60,
        "maximum_huber_cdelta_pearson_p_difference": 0.0,
    }
    first = [
        {
            **base,
            "dyadic_weight": 0.1,
            "profile_only_rejections": 15,
            "mantel_only_rejections": 5,
        },
        {
            **base,
            "dyadic_weight": 0.2,
            "profile_only_rejections": 5,
            "mantel_only_rejections": 15,
        },
    ]
    combined = combine_skew_power_runs((first, first))
    crossover = estimate_skew_crossovers(combined, "test")[0]
    assert len(combined) == 2
    assert combined[0]["repetitions"] == 200
    assert abs(crossover["crossover_estimate"] - 0.15) < 1e-12
