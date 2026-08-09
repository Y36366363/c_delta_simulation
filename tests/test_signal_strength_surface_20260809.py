from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.run_signal_strength_surface_20260809 import (
    _building_components,
    _fit_linear,
    _leave_one_out_error,
    _mix_components,
    estimate_crossovers,
    fit_ratio_models,
    local_weights,
)


class SignalStrengthSurfaceTests(unittest.TestCase):
    def test_components_and_mixture_are_finite(self):
        rng = np.random.default_rng(20261033)
        node_x, node_y, dyad_x, dyad_y, blocks = _building_components(
            rng, 0.55, 0.70
        )
        x, y = _mix_components((node_x, node_y, dyad_x, dyad_y), 0.25)
        self.assertEqual(x.shape, (48,))
        self.assertEqual(y.shape, (48,))
        self.assertTrue(np.all(np.isfinite(x)))
        self.assertTrue(np.all(np.isfinite(y)))
        np.testing.assert_array_equal(np.bincount(blocks), np.repeat(12, 4))

    def test_crossover_and_local_grid(self):
        rows = [
            {"node_strength": 0.55, "dyad_strength": 0.70, "dyadic_weight": 0.2, "power_difference": 0.02, "paired_ci_low": -0.01, "paired_ci_high": 0.05, "repetitions": 100, "n_perm": 99},
            {"node_strength": 0.55, "dyad_strength": 0.70, "dyadic_weight": 0.3, "power_difference": -0.03, "paired_ci_low": -0.06, "paired_ci_high": 0.00, "repetitions": 100, "n_perm": 99},
        ]
        crossover = estimate_crossovers(rows, phase="test")[0]
        self.assertAlmostEqual(crossover["crossover_estimate"], 0.24)
        weights = local_weights([crossover])[(0.55, 0.70)]
        self.assertEqual(weights[0], 0.15)
        self.assertEqual(weights[-1], 0.35)

    def test_linear_fit_recovers_exact_relation(self):
        x = np.arange(5.0)[:, None]
        y = 1.5 + 0.75 * x[:, 0]
        coefficients, r_squared, rmse, maximum_error = _fit_linear(y, x)
        np.testing.assert_allclose(coefficients, (1.5, 0.75))
        self.assertAlmostEqual(r_squared, 1.0)
        self.assertAlmostEqual(rmse, 0.0)
        self.assertAlmostEqual(maximum_error, 0.0)

    def test_leave_one_out_recovers_exact_linear_relation(self):
        x = np.arange(6.0)[:, None]
        y = -0.5 + 1.25 * x[:, 0]
        rmse, maximum_error = _leave_one_out_error(y, x)
        self.assertAlmostEqual(rmse, 0.0)
        self.assertAlmostEqual(maximum_error, 0.0)

    def test_ratio_models_accept_complete_surface(self):
        rows = []
        for node in (0.35, 0.55, 0.75):
            for dyad in (0.45, 0.65, 0.80):
                ratio = np.arctanh(node) / np.arctanh(dyad)
                weight = ratio / (1.0 + ratio)
                rows.append(
                    {
                        "node_strength": node,
                        "dyad_strength": dyad,
                        "raw_strength_ratio": node / dyad,
                        "fisher_z_strength_ratio": ratio,
                        "crossover_estimate": weight,
                    }
                )
        models, predictions = fit_ratio_models(rows)
        fisher = next(row for row in models if row["model"] == "fisher_z_ratio")
        self.assertAlmostEqual(fisher["r_squared_logit_crossover"], 1.0)
        self.assertEqual(len(predictions), 27)


if __name__ == "__main__":
    unittest.main()
