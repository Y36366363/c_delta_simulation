from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta_from_profiles,
    huber_reference_profile,
    permutation_test_profiles,
)


class RobustDefinitionTests(unittest.TestCase):
    def test_profile_is_shift_and_nonzero_scale_invariant(self):
        x = np.array([-4.0, -1.0, 0.5, 2.0, 8.0, 12.0])
        base = huber_reference_profile(x, radial_floor=1.0)
        transformed = huber_reference_profile(-7.0 * x + 11.0, radial_floor=1.0)
        np.testing.assert_allclose(base, transformed, rtol=1e-9, atol=1e-9)

    def test_radius_profile_matches_existing_huber_ratio(self):
        from cdelta import center_salience_vector

        x = np.array([-3.0, -1.0, 0.0, 2.0, 7.0, 20.0])
        y = np.array([-2.0, -0.5, 1.0, 3.0, 8.0, 18.0])
        old = c_delta_from_profiles(
            center_salience_vector(x, center="huber"),
            center_salience_vector(y, center="huber"),
        )["raw"]
        new = c_delta_from_profiles(
            huber_reference_profile(x), huber_reference_profile(y)
        )["raw"]
        self.assertAlmostEqual(old, new, places=9)

    def test_regularized_profile_has_positive_floor(self):
        x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
        scores = huber_reference_profile(x, radial_floor=1.0)
        self.assertTrue(np.all(scores >= 1.0))

    def test_hard_cap_bounds_final_profile(self):
        x = np.array([-2.0, -1.0, 0.0, 1.0, 1e12])
        scores = huber_reference_profile(x, cap=6.0)
        self.assertLessEqual(float(np.max(scores)), 6.0)

    def test_profile_permutation_test_is_reproducible(self):
        x = np.array([-3.0, -1.0, 0.0, 2.0, 8.0, 12.0])
        y = np.array([-2.0, -0.5, 1.0, 3.0, 7.0, 11.0])
        sx = huber_reference_profile(x)
        sy = huber_reference_profile(y)
        first = permutation_test_profiles(sx, sy, n_perm=199, seed=123)
        second = permutation_test_profiles(sx, sy, n_perm=199, seed=123)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
