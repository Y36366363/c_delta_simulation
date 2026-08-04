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


if __name__ == "__main__":
    unittest.main()
