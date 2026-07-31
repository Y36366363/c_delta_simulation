from pathlib import Path
import sys
import unittest

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta,
    c_delta_identity_from_divergences,
    calibrated_subgroup_simulation,
    divergence_vector,
    independent_null_size_simulation,
    large_scale_simulation,
    l2_divergence_closed_form,
    make_scenario,
    multi_extreme_power_simulation,
    near_zero_divergence_simulation,
    overlap_layer_diagnostic,
    outlier_influence_summary,
    permutation_test,
    permutation_mean_check,
    permutation_statistics_from_divergences,
    power_curve_simulation,
    repeated_outlier_simulation,
    variant_comparison_simulation,
)
from scripts.run_background_masking_diagnostics import masking_metrics


class CDeltaTests(unittest.TestCase):
    def test_l2_divergence_closed_form(self):
        x = np.array([-3.0, -1.0, 0.5, 2.0, 7.0])
        direct = divergence_vector(x, kind="l2")
        closed = l2_divergence_closed_form(x)
        np.testing.assert_allclose(direct, closed, rtol=0.0, atol=1e-12)

    def test_l2_divergence_ranks_absolute_centered_values(self):
        x = np.array([-4.0, -1.0, 0.0, 2.0, 6.0, 8.0])
        divergence_order = np.argsort(divergence_vector(x, kind="l2"))
        centered_order = np.argsort(np.abs(x - x.mean()))
        np.testing.assert_array_equal(divergence_order, centered_order)

    def test_background_masking_metrics_detect_unmatched_maximum(self):
        dx = np.array([10.0, 1.0, 1.0, 4.0, 4.0])
        dy = np.array([1.0, 9.0, 1.0, 4.0, 4.0])
        metrics = masking_metrics(dx, dy, k=2)
        self.assertEqual(metrics["both_max_are_background"], 1.0)
        self.assertEqual(metrics["background_topk_index_overlap"], 0.5)
        self.assertEqual(
            metrics["background_max_product_exceeds_planted_mean_product"], 0.0
        )

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

    def test_exact_permutation_mean_equals_one(self):
        x, y = make_scenario("aligned_normal", 6, seed=111)
        check = permutation_mean_check(x, y, exact=True)
        self.assertAlmostEqual(check["mean_permuted_raw"], 1.0, places=6)

    def test_c_delta_correlation_identity(self):
        x, y = make_scenario("aligned_normal", 30, seed=121)
        result = c_delta(x, y)
        identity = c_delta_identity_from_divergences(result.dx, result.dy)
        self.assertEqual(identity["status"], "ok")
        self.assertAlmostEqual(
            identity["c_delta"], identity["identity_value"], places=12
        )

    def test_c_delta_and_divergence_correlation_rank_permutations_identically(self):
        x, y = make_scenario("aligned_normal", 18, seed=122)
        result = c_delta(x, y)
        rng = np.random.default_rng(123)
        c_values = []
        r_values = []
        for _ in range(99):
            permuted_dy = rng.permutation(result.dy)
            identity = c_delta_identity_from_divergences(result.dx, permuted_dy)
            c_values.append(identity["c_delta"])
            r_values.append(identity["correlation"])
        self.assertTrue(
            np.array_equal(np.argsort(c_values), np.argsort(r_values))
        )

    def test_corrected_raw_is_old_raw_divided_by_n(self):
        x, y = make_scenario("aligned_normal", 20, seed=118)
        result = c_delta(x, y)
        old_raw = float(np.dot(result.dx, result.dy) / (result.dx.mean() * result.dy.mean()))
        self.assertAlmostEqual(result.raw, old_raw / result.dx.size, places=12)

    def test_permutation_order_is_unchanged_by_n_factor(self):
        x, y = make_scenario("aligned_normal", 18, seed=119)
        result = c_delta(x, y)
        corrected_stats = permutation_statistics_from_divergences(
            result.dx, result.dy, n_perm=49, seed=120
        )
        rng = np.random.default_rng(120)
        old_observed = float(np.dot(result.dx, result.dy) / (result.dx.mean() * result.dy.mean()))
        old_stats = np.asarray(
            [
                np.dot(result.dx, rng.permutation(result.dy))
                / (result.dx.mean() * result.dy.mean())
                for _ in range(49)
            ],
            dtype=float,
        )
        old_p = (float(np.sum(old_stats >= old_observed)) + 1) / 50
        corrected_p = (float(np.sum(corrected_stats >= result.raw)) + 1) / 50
        self.assertAlmostEqual(corrected_p, old_p, places=12)

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

    def test_variant_comparison_smoke(self):
        rows = variant_comparison_simulation(
            n=20,
            k=1,
            backgrounds=["normal"],
            kinds=["l2", "l1"],
            scenarios=["matched", "independent_null"],
            repetitions=3,
            n_perm=9,
            seed=114,
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["kind"] for row in rows}, {"l2", "l1"})

    def test_calibrated_subgroup_simulation_smoke(self):
        rows = calibrated_subgroup_simulation(
            n=20,
            k_values=[1, 2],
            magnitude_grid=[4.0, 8.0],
            reference_k=1,
            reference_magnitude=8.0,
            calibration_repetitions=3,
            evaluation_repetitions=3,
            n_perm=9,
            seed=115,
            scenarios=["matched", "independent_null"],
        )
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["k_extremes"] for row in rows}, {1, 2})

    def test_explicit_target_calibration_smoke(self):
        rows = calibrated_subgroup_simulation(
            n=20,
            k_values=[1, 2],
            magnitude_grid=[2.0, 4.0, 8.0],
            target_corr=0.55,
            calibration_repetitions=3,
            evaluation_repetitions=3,
            n_perm=9,
            seed=116,
            scenarios=["matched"],
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["target_corr"] for row in rows}, {0.55})

    def test_calibrated_sample_size_smoke(self):
        rows = []
        for n in [15, 20]:
            rows.extend(
                calibrated_subgroup_simulation(
                    n=n,
                    k_values=[1],
                    magnitude_grid=[2.0, 4.0, 8.0],
                    target_corr=0.35,
                    calibration_repetitions=2,
                    evaluation_repetitions=2,
                    n_perm=9,
                    seed=117 + n,
                    scenarios=["matched", "independent_null"],
                )
            )
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["n"] for row in rows}, {15, 20})


if __name__ == "__main__":
    unittest.main()
