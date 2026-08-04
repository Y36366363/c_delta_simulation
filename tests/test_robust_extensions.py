from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_multivariate_robust_pilot import (
    coordinate_huber_profile,
    spatial_median_profile,
)
from scripts.run_cap_loss_refinement import tolerance_map


class RobustExtensionTests(unittest.TestCase):
    def test_spatial_profile_is_rotation_invariant(self):
        rng = np.random.default_rng(20260817)
        z = rng.normal(size=(60, 5))
        z[0] += np.array([9.0, -2.0, 1.0, 3.0, 4.0])
        q, _ = np.linalg.qr(rng.normal(size=(5, 5)))
        np.testing.assert_allclose(
            spatial_median_profile(z),
            spatial_median_profile(z @ q),
            rtol=1e-8,
            atol=1e-8,
        )

    def test_coordinate_huber_is_not_rotation_invariant(self):
        rng = np.random.default_rng(20260818)
        z = rng.normal(size=(60, 4))
        z[0] += np.array([12.0, 0.0, 0.0, 0.0])
        q, _ = np.linalg.qr(rng.normal(size=(4, 4)))
        error = np.max(
            np.abs(coordinate_huber_profile(z) - coordinate_huber_profile(z @ q))
        )
        self.assertGreater(error, 1e-3)

    def test_cap_tolerance_map_selects_highest_masking_gain_feasible_cap(self):
        losses = [
            {
                "cap": 5.0,
                "maximum_null_rejection": 0.05,
                "worst_absolute_core_power_loss": 0.04,
                "mean_masking_gain": 0.50,
            },
            {
                "cap": 6.0,
                "maximum_null_rejection": 0.05,
                "worst_absolute_core_power_loss": 0.02,
                "mean_masking_gain": 0.40,
            },
            {
                "cap": 7.0,
                "maximum_null_rejection": 0.05,
                "worst_absolute_core_power_loss": 0.005,
                "mean_masking_gain": 0.30,
            },
        ]
        by_tolerance = {
            row["allowed_worst_core_power_loss"]: row["selected_cap"]
            for row in tolerance_map(losses)
        }
        self.assertEqual(by_tolerance[0.01], 7.0)
        self.assertEqual(by_tolerance[0.03], 6.0)
        self.assertEqual(by_tolerance[0.05], 5.0)


if __name__ == "__main__":
    unittest.main()
