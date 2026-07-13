from pathlib import Path
import sys
import unittest

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta,
    divergence_vector,
    independent_null_size_simulation,
    large_scale_simulation,
    make_scenario,
    multi_extreme_power_simulation,
    near_zero_divergence_simulation,
    overlap_layer_diagnostic,
    outlier_influence_summary,
    permutation_test,
    permutation_mean_check,
    power_curve_simulation,
    repeated_outlier_simulation,
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

    def test_repeated_matched_extreme_has_stronger_mean_alignment(self):
        rows = repeated_outlier_simulation(
            n=35,
            repetitions=20,
            n_perm=19,
            seed=55,
            magnitude=8.0,
        )
        by_name = {row["scenario"]: row for row in rows}
        self.assertGreater(
            by_name["matched_extreme"]["mean_corr"],
            by_name["x_only_extreme"]["mean_corr"],
        )

    def test_power_curve_strengthens_with_magnitude(self):
        rows = power_curve_simulation(
            sample_sizes=[20],
            magnitudes=[2.0, 8.0],
            repetitions=10,
            n_perm=19,
            seed=66,
        )
        by_magnitude = {row["magnitude"]: row for row in rows}
        self.assertGreater(
            by_magnitude[8.0]["mean_corr"],
            by_magnitude[2.0]["mean_corr"],
        )

    def test_multi_extreme_matched_exceeds_mismatched_alignment(self):
        rows = multi_extreme_power_simulation(
            sample_sizes=[20],
            extreme_counts=[2],
            magnitudes=[8.0],
            repetitions=10,
            n_perm=19,
            seed=77,
        )
        by_alignment = {row["alignment"]: row for row in rows}
        self.assertGreater(
            by_alignment["matched"]["mean_corr"],
            by_alignment["mismatched"]["mean_corr"],
        )

    def test_near_zero_positive_scales_remain_stable(self):
        rows = near_zero_divergence_simulation(
            epsilons=[1.0, 1e-4, 0.0],
            n=20,
            seed=88,
        )
        self.assertEqual(rows[-1]["status"], "undetermined due to data limitations")
        self.assertAlmostEqual(rows[0]["raw"], rows[1]["raw"], places=6)

    def test_fast_permutation_matches_valid_output(self):
        x, y = make_scenario("aligned_normal", 30, seed=99)
        result = permutation_test(x, y, n_perm=19, seed=100)
        self.assertEqual(result["status"], "ok")
        self.assertGreaterEqual(result["p_value"], 0.0)
        self.assertLessEqual(result["p_value"], 1.0)

    def test_large_scale_simulation_smoke(self):
        rows = large_scale_simulation(
            sample_sizes=[50],
            extreme_counts=[1],
            backgrounds=["normal"],
            repetitions=3,
            n_perm=9,
            seed=101,
        )
        self.assertEqual(len(rows), 2)

    def test_exact_permutation_mean_equals_n(self):
        x, y = make_scenario("aligned_normal", 6, seed=111)
        check = permutation_mean_check(x, y, exact=True)
        self.assertAlmostEqual(check["mean_permuted_raw"], 6.0, places=6)

    def test_overlap_layer_diagnostic_counts_layers(self):
        rows = overlap_layer_diagnostic(n=12, k=2, n_perm=100, seed=112)
        self.assertEqual({row["overlap_count"] for row in rows}, {0, 1, 2})

    def test_independent_null_size_smoke(self):
        rows = independent_null_size_simulation(
            n=20,
            k=2,
            repetitions=5,
            n_perm=19,
            seed=113,
            alphas=[0.05],
        )
        self.assertEqual(len(rows), 1)
        self.assertIn("wilson_low", rows[0])
        self.assertIn("p50", rows[0])


if __name__ == "__main__":
    unittest.main()
