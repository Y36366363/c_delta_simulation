from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from cdelta import (
    c_delta_from_profiles,
    center_salience_vector,
    divergence_vector,
    huber_reference_profile,
)
from scripts.run_teacher_feedback_20260807 import _mantel_correlation


class TeacherFeedbackTests(unittest.TestCase):
    def test_cdelta_star_has_exact_pearson_cv_decomposition(self):
        rng = np.random.default_rng(20260930)
        x = rng.lognormal(0.0, 0.7, 100)
        y = np.exp(0.4 * np.log(x) + rng.normal(0.0, 0.6, 100))
        sx, sy = huber_reference_profile(x), huber_reference_profile(y)
        coefficient = c_delta_from_profiles(sx, sy)["raw"]
        correlation = np.corrcoef(sx, sy)[0, 1]
        cv_product = sx.std() / sx.mean() * sy.std() / sy.mean()
        self.assertAlmostEqual(coefficient, 1.0 + correlation * cv_product)

    def test_mad_scale_normalisation_cancels_from_cdelta_star(self):
        rng = np.random.default_rng(20261001)
        x, y = rng.standard_t(3, 80), rng.standard_t(3, 80)
        scaled = c_delta_from_profiles(
            huber_reference_profile(x), huber_reference_profile(y)
        )["raw"]
        unscaled = c_delta_from_profiles(
            center_salience_vector(x, center="huber"),
            center_salience_vector(y, center="huber"),
        )["raw"]
        self.assertAlmostEqual(scaled, unscaled, places=10)

    def test_l2_row_profile_discards_sign_rewiring_retained_by_mantel(self):
        radii = np.repeat(np.linspace(0.5, 5.0, 20), 2)
        signs = np.tile(np.array([1.0, -1.0]), 20)
        x = radii * signs
        y_signs = signs.copy()
        y_signs.reshape(-1, 2)[::2] *= -1.0
        y = radii * y_signs
        dx, dy = divergence_vector(x, kind="l2"), divergence_vector(y, kind="l2")
        np.testing.assert_allclose(dx, dy)
        self.assertAlmostEqual(np.corrcoef(dx, dy)[0, 1], 1.0)
        self.assertLess(_mantel_correlation(x, y), 0.5)

    def test_l2_row_profile_closed_form(self):
        rng = np.random.default_rng(20261002)
        x = rng.normal(size=50)
        variance = np.mean((x - x.mean()) ** 2)
        expected = np.sqrt(
            x.size / (x.size - 1.0) * ((x - x.mean()) ** 2 + variance)
        )
        np.testing.assert_allclose(divergence_vector(x, kind="l2"), expected)


if __name__ == "__main__":
    unittest.main()
