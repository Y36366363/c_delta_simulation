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
from scripts.run_cap6_expanded_cross_validation import (
    masked_signal,
    matched_signal,
)
from scripts.run_comprehensive_scope_benchmark import SCENARIO_ROLES, make_scenario
from scripts.run_diffuse_boundary_expansion import make_diffuse
from scripts.robust_extension_utils import within_block_permutation_indices


class RobustExtensionTests(unittest.TestCase):
    def test_within_block_permutations_preserve_labels_and_all_indices(self):
        blocks = np.repeat(np.arange(4), 5)
        indices = within_block_permutation_indices(
            blocks, 50, np.random.default_rng(20260901)
        )
        expected = np.arange(blocks.size)
        for row in indices:
            np.testing.assert_array_equal(np.sort(row), expected)
            np.testing.assert_array_equal(blocks[row], blocks)

    def test_within_block_permutations_reject_invalid_arguments(self):
        rng = np.random.default_rng(20260902)
        with self.assertRaises(ValueError):
            within_block_permutation_indices([[0, 0], [1, 1]], 10, rng)
        with self.assertRaises(ValueError):
            within_block_permutation_indices([0, 0, 1], 0, rng)

    def test_comprehensive_scenarios_return_finite_paired_samples(self):
        rng = np.random.default_rng(20260829)
        for scenario in SCENARIO_ROLES:
            x, y = make_scenario(scenario, 20, rng)
            self.assertEqual(x.shape, (20,))
            self.assertEqual(y.shape, (20,))
            self.assertTrue(np.all(np.isfinite(x)))
            self.assertTrue(np.all(np.isfinite(y)))

    def test_diffuse_contamination_adds_declared_number_of_remote_values(self):
        clean_rng = np.random.default_rng(20260830)
        dirty_rng = np.random.default_rng(20260830)
        clean_x, clean_y = make_diffuse(
            clean_rng, 40, 0.15, 0.50, 0.0, "uniform"
        )
        dirty_x, dirty_y = make_diffuse(
            dirty_rng, 40, 0.15, 0.50, 0.05, "uniform"
        )
        self.assertEqual(np.count_nonzero(dirty_x - clean_x), 2)
        self.assertEqual(np.count_nonzero(dirty_y - clean_y), 2)
        np.testing.assert_allclose(
            np.sort((dirty_x - clean_x)[dirty_x != clean_x]), [20.0, 20.0]
        )
        np.testing.assert_allclose(
            np.sort((dirty_y - clean_y)[dirty_y != clean_y]), [20.0, 20.0]
        )

    def test_masking_generator_adds_one_unmatched_contaminant_per_margin(self):
        clean_rng = np.random.default_rng(20260831)
        dirty_rng = np.random.default_rng(20260831)
        clean_x, clean_y = matched_signal(clean_rng, 40, "fixed1", 6.0, "normal")
        dirty_x, dirty_y = masked_signal(
            dirty_rng, 40, "fixed1", 6.0, 20.0, "normal"
        )
        self.assertEqual(np.count_nonzero(dirty_x - clean_x), 1)
        self.assertEqual(np.count_nonzero(dirty_y - clean_y), 1)
        self.assertNotEqual(
            int(np.flatnonzero(dirty_x != clean_x)[0]),
            int(np.flatnonzero(dirty_y != clean_y)[0]),
        )

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
