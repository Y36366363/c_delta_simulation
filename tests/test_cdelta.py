from pathlib import Path
import sys
import unittest

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta,
    divergence_vector,
    make_scenario,
    outlier_influence_summary,
    permutation_test,
)


class CDeltaTests(unittest.TestCase):
    def test_divergence_vector_length(self):
        dx = divergence_vector([1.0, 2.0, 4.0, 8.0])
        self.assertEqual(dx.shape, (4,))
        self.assertTrue(np.all(dx > 0))

    def test_scale_and_shift_invariance(self):
        x = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
        y = np.array([2.0, 3.0, 5.0, 9.0, 17.0])
        base = c_delta(x, y).raw
        transformed = c_delta(10 * x + 7, -3 * y + 2).raw
        self.assertAlmostEqual(base, transformed, places=10)

    def test_zero_divergence_is_undetermined(self):
        result = c_delta([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])
        self.assertTrue(np.isnan(result.raw))
        self.assertEqual(result.status, "undetermined due to data limitations")

    def test_pairing_normalization_in_unit_interval(self):
        x, y = make_scenario("aligned_normal", 40, seed=11)
        result = c_delta(x, y)
        self.assertGreaterEqual(result.normalized_pairing, 0.0)
        self.assertLessEqual(result.normalized_pairing, 1.0 + 1e-12)

    def test_permutation_test_detects_aligned_signal(self):
        x, y = make_scenario("aligned_normal", 45, seed=22)
        result = permutation_test(x, y, n_perm=99, seed=33)
        self.assertLess(result["p_value"], 0.10)

    def test_matched_extreme_has_stronger_divergence_alignment(self):
        rows = outlier_influence_summary(n=40, seed=44, n_perm=49)
        by_name = {row["scenario"]: row for row in rows}
        self.assertGreater(
            by_name["matched_extreme"]["main_corr"],
            by_name["x_only_extreme"]["main_corr"],
        )


if __name__ == "__main__":
    unittest.main()
