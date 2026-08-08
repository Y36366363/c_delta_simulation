from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.run_node_dyad_mixture_20260808 import (
    _fast_within_block_indices,
    _paired_difference_summary,
    _refined_weights,
    combine_comparison_runs,
    crossing_interval,
    make_mixed_building_pair,
    run_mixture_grid,
)


class NodeDyadMixtureTests(unittest.TestCase):
    def test_vectorized_permutations_preserve_every_block(self):
        rng = np.random.default_rng(20261026)
        blocks = np.repeat(np.arange(4), 12)
        indices = _fast_within_block_indices(blocks, 200, rng)
        np.testing.assert_array_equal(blocks[indices], np.tile(blocks, (200, 1)))
        for row in indices:
            np.testing.assert_array_equal(np.sort(row), np.arange(48))

    def test_mixture_generator_endpoints_and_blocks(self):
        rng = np.random.default_rng(20261023)
        for weight in (0.0, 0.35, 1.0):
            x, y, blocks = make_mixed_building_pair(rng, weight)
            self.assertEqual(x.shape, (48,))
            self.assertEqual(y.shape, (48,))
            np.testing.assert_array_equal(np.bincount(blocks), np.repeat(12, 4))
            self.assertTrue(np.all(np.isfinite(x)))
            self.assertTrue(np.all(np.isfinite(y)))

    def test_mixture_weight_must_be_in_unit_interval(self):
        rng = np.random.default_rng(20261024)
        with self.assertRaises(ValueError):
            make_mixed_building_pair(rng, -0.01)
        with self.assertRaises(ValueError):
            make_mixed_building_pair(rng, 1.01)

    def test_paired_difference_counts_match_power_difference(self):
        profile = np.array([True, True, False, False, True])
        mantel = np.array([True, False, True, False, False])
        result = _paired_difference_summary(profile, mantel)
        self.assertEqual(result["profile_only_rejections"], 2)
        self.assertEqual(result["mantel_only_rejections"], 1)
        self.assertAlmostEqual(result["power_difference"], 0.2)

    def test_combined_comparison_preserves_paired_counts(self):
        base = {
            "dyadic_weight": 0.2,
            "node_weight": 0.8,
            "profile_method": "huber_cdelta_star",
            "repetitions": 10,
            "n_perm": 99,
            "profile_only_rejections": 3,
            "mantel_only_rejections": 1,
            "both_reject": 2,
            "neither_reject": 4,
        }
        combined = combine_comparison_runs(([base], [base]))[0]
        self.assertEqual(combined["repetitions"], 20)
        self.assertEqual(combined["profile_only_rejections"], 6)
        self.assertEqual(combined["mantel_only_rejections"], 2)
        self.assertAlmostEqual(combined["profile_power"], 0.5)
        self.assertAlmostEqual(combined["mantel_power"], 0.3)

    def test_crossing_and_refinement_are_interpolated(self):
        rows = [
            {"profile_method": "huber_cdelta_star", "dyadic_weight": 0.4, "power_difference": 0.1},
            {"profile_method": "huber_cdelta_star", "dyadic_weight": 0.5, "power_difference": -0.1},
        ]
        left, right, estimate = crossing_interval(rows)
        self.assertEqual((left, right), (0.4, 0.5))
        self.assertAlmostEqual(estimate, 0.45)
        refined = _refined_weights(rows)
        self.assertEqual(refined[0], 0.3)
        self.assertEqual(refined[-1], 0.6)

    def test_small_grid_preserves_huber_pearson_permutation_equivalence(self):
        methods, _ = run_mixture_grid(
            (0.0, 1.0), repetitions=4, n_perm=19, seed=20261025, phase="test"
        )
        huber = {
            row["dyadic_weight"]: row
            for row in methods
            if row["method"] == "huber_cdelta_star"
        }
        pearson = {
            row["dyadic_weight"]: row
            for row in methods
            if row["method"] == "huber_profile_pearson"
        }
        for weight in huber:
            self.assertEqual(
                huber[weight]["rejection_rate"], pearson[weight]["rejection_rate"]
            )
            self.assertEqual(
                huber[weight]["maximum_huber_cdelta_pearson_p_difference"], 0.0
            )


if __name__ == "__main__":
    unittest.main()
