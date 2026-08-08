from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import within_block_permutation_indices
from scripts.run_building_target_separation_20260808 import (
    _profile_statistics,
    fixed_correlation_cv_grid,
    make_building_pair,
    mantel_statistic,
)


class BuildingTargetSeparationTests(unittest.TestCase):
    def test_block_restricted_cdelta_and_pearson_pvalues_are_identical(self):
        rng = np.random.default_rng(20261010)
        x, y, blocks = make_building_pair(rng, "node_salience_sign_rewired")
        indices = within_block_permutation_indices(blocks, 199, rng)
        outcomes = _profile_statistics(
            huber_reference_profile(x), huber_reference_profile(y), indices
        )
        self.assertEqual(outcomes["ratio"][1], outcomes["correlation"][1])

    def test_mantel_is_invariant_to_common_label_permutation(self):
        rng = np.random.default_rng(20261011)
        x, y, _ = make_building_pair(rng, "shared_dyadic_geometry")
        order = rng.permutation(x.size)
        self.assertAlmostEqual(
            mantel_statistic(x, y), mantel_statistic(x[order], y[order])
        )

    def test_building_generator_has_balanced_blocks(self):
        rng = np.random.default_rng(20261012)
        for scenario in (
            "conditional_null",
            "node_salience_sign_rewired",
            "shared_dyadic_geometry",
            "matched_structural_extreme",
            "unmatched_extreme_negative_control",
        ):
            x, y, blocks = make_building_pair(rng, scenario)
            self.assertEqual(x.shape, (48,))
            self.assertEqual(y.shape, (48,))
            np.testing.assert_array_equal(np.bincount(blocks), np.repeat(12, 4))

    def test_fixed_pearson_target_changes_cdelta_through_cv_weighting(self):
        rows = fixed_correlation_cv_grid(
            sample_sizes=(4000,), repetitions=1, seed=20261013
        )
        self.assertAlmostEqual(rows[0]["target_profile_correlation"], 0.30)
        self.assertLess(rows[0]["population_cdelta_star"], 1.03)
        self.assertGreater(rows[3]["population_cdelta_star"], 3.0)
        for row in rows:
            expected = 1.0 + 0.30 * row["population_cv_product"]
            self.assertAlmostEqual(row["population_cdelta_star"], expected)


if __name__ == "__main__":
    unittest.main()
