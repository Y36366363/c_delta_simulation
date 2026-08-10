import numpy as np

from scripts.run_mixed_path_local_slopes_20260810 import (
    correlation_and_derivative,
    mixture_value_and_tangent,
    run_population_slopes,
)


def test_mixture_tangent_matches_central_difference():
    node = np.asarray([-1.0, 0.5, 2.0])
    dyad = np.asarray([0.2, -0.7, 1.2])
    weight = 0.37
    value, tangent = mixture_value_and_tangent(node, dyad, weight)
    epsilon = 1e-6
    plus, _ = mixture_value_and_tangent(node, dyad, weight + epsilon)
    minus, _ = mixture_value_and_tangent(node, dyad, weight - epsilon)
    assert np.allclose(value, np.sqrt(1.0 - weight) * node + np.sqrt(weight) * dyad)
    assert np.allclose(tangent, (plus - minus) / (2.0 * epsilon), atol=1e-8)


def test_correlation_derivative_matches_linear_path_difference():
    rng = np.random.default_rng(20261059)
    x = rng.normal(size=20_000)
    y = 0.4 * x + rng.normal(size=x.size)
    x_dot = rng.normal(size=x.size)
    y_dot = rng.normal(size=x.size)
    correlation, derivative = correlation_and_derivative(x, y, x_dot, y_dot)
    epsilon = 1e-5
    plus = np.corrcoef(x + epsilon * x_dot, y + epsilon * y_dot)[0, 1]
    minus = np.corrcoef(x - epsilon * x_dot, y - epsilon * y_dot)[0, 1]
    assert abs(correlation - np.corrcoef(x, y)[0, 1]) < 1e-12
    assert abs(derivative - (plus - minus) / (2.0 * epsilon)) < 1e-8


def test_small_population_run_validates_pathwise_derivative():
    rows = run_population_slopes(
        n_batches=3, batch_size=20_000, epsilon=0.002, seed=20261063
    )
    assert len(rows) == 8
    assert max(row["absolute_derivative_check_error"] for row in rows) < 0.01
