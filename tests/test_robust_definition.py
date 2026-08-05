from pathlib import Path
import sys
import unittest

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta_from_profiles,
    huber_cdelta_bootstrap_intervals,
    huber_reference_profile,
    permutation_test_profiles,
    profile_permutation_reference,
)


class RobustDefinitionTests(unittest.TestCase):
    def test_huber_bootstrap_intervals_are_reproducible_and_ordered(self):
        rng = np.random.default_rng(20260906)
        x = rng.normal(size=30)
        y = 0.4 * x + rng.normal(size=30)
        first = huber_cdelta_bootstrap_intervals(
            x, y, n_boot=59, seed=20260907
        )
        second = huber_cdelta_bootstrap_intervals(
            x, y, n_boot=59, seed=20260907
        )
        self.assertEqual(first, second)
        for method in ("percentile", "basic", "bca", "normal"):
            self.assertLess(first[method]["lower"], first[method]["upper"])

    def test_huber_bootstrap_intervals_are_affine_invariant(self):
        rng = np.random.default_rng(20260908)
        x = rng.normal(size=25)
        y = rng.normal(size=25)
        base = huber_cdelta_bootstrap_intervals(x, y, n_boot=39, seed=12)
        transformed = huber_cdelta_bootstrap_intervals(
            -3.0 * x + 7.0, 5.0 * y - 2.0, n_boot=39, seed=12
        )
        for key in (
            "estimate",
            "bias_correction",
            "acceleration",
            "bootstrap_standard_error",
        ):
            self.assertAlmostEqual(base[key], transformed[key], places=8)
        for method in ("percentile", "basic", "bca", "normal"):
            self.assertAlmostEqual(
                base[method]["lower"], transformed[method]["lower"], places=8
            )
            self.assertAlmostEqual(
                base[method]["upper"], transformed[method]["upper"], places=8
            )

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

    def test_blocked_profile_permutation_is_reproducible(self):
        sx = np.array([0.2, 0.8, 1.1, 1.9, 3.0, 4.0])
        sy = np.array([0.4, 0.6, 1.2, 1.8, 2.5, 4.5])
        blocks = np.repeat(np.arange(3), 2)
        first = permutation_test_profiles(
            sx, sy, n_perm=199, seed=321, blocks=blocks
        )
        second = permutation_test_profiles(
            sx, sy, n_perm=199, seed=321, blocks=blocks
        )
        self.assertEqual(first, second)
        self.assertNotAlmostEqual(first["permutation_reference_mean"], 1.0)
        self.assertAlmostEqual(
            first["permutation_reference_mean"],
            first["permutation_reference_exact"],
            delta=0.02,
        )

    def test_blocked_reference_matches_exact_enumeration(self):
        from itertools import product, permutations

        sx = np.array([0.2, 0.8, 1.1, 1.9, 3.0, 4.0])
        sy = np.array([0.4, 0.6, 1.2, 1.8, 2.5, 4.5])
        blocks = np.repeat(np.arange(3), 2)
        members = [np.flatnonzero(blocks == label) for label in np.unique(blocks)]
        statistics = []
        for choices in product(*(list(permutations(group)) for group in members)):
            indices = np.arange(sx.size)
            for group, choice in zip(members, choices):
                indices[group] = choice
            statistics.append(
                np.mean(sx * sy[indices]) / (float(sx.mean()) * float(sy.mean()))
            )
        self.assertAlmostEqual(
            profile_permutation_reference(sx, sy, blocks=blocks),
            float(np.mean(statistics)),
            places=12,
        )
        self.assertEqual(profile_permutation_reference(sx, sy), 1.0)

    def test_blocked_profile_permutation_rejects_mismatched_blocks(self):
        sx = np.array([0.2, 0.8, 1.1, 1.9])
        sy = np.array([0.4, 0.6, 1.2, 1.8])
        with self.assertRaises(ValueError):
            permutation_test_profiles(sx, sy, blocks=[0, 0, 1])
        with self.assertRaises(ValueError):
            permutation_test_profiles(sx, sy, n_perm=0)

    def test_blocked_two_sided_test_centres_on_restricted_reference(self):
        sx = np.array([0.2, 0.8, 1.1, 1.9, 3.0, 4.0])
        sy = np.array([0.4, 0.6, 1.2, 1.8, 2.5, 4.5])
        blocks = np.repeat(np.arange(3), 2)
        result = permutation_test_profiles(
            sx,
            sy,
            n_perm=999,
            seed=654,
            blocks=blocks,
            alternative="two-sided",
        )
        reference = profile_permutation_reference(sx, sy, blocks=blocks)
        observed = c_delta_from_profiles(sx, sy)["raw"]
        rng = np.random.default_rng(654)
        statistics = []
        for _ in range(999):
            permuted = sy.copy()
            for label in np.unique(blocks):
                members = np.flatnonzero(blocks == label)
                permuted[members] = sy[rng.permutation(members)]
            statistics.append(
                np.mean(sx * permuted) / (float(sx.mean()) * float(sy.mean()))
            )
        expected = (
            sum(
                abs(stat - reference) >= abs(observed - reference)
                for stat in statistics
            )
            + 1
        ) / 1000
        self.assertNotAlmostEqual(reference, 1.0)
        self.assertAlmostEqual(result["p_value"], expected, places=12)

    def test_constant_margin_is_reported_as_undetermined(self):
        sx = huber_reference_profile(np.ones(10))
        sy = huber_reference_profile(np.arange(10.0))
        result = permutation_test_profiles(sx, sy, n_perm=19, seed=11)
        self.assertEqual(result["status"], "undetermined due to data limitations")
        self.assertTrue(np.isnan(result["p_value"]))


if __name__ == "__main__":
    unittest.main()
