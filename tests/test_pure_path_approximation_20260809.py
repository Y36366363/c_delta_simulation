from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_pure_path_approximation_20260809 import (
    absolute_normal_correlation,
    dyad_path_cdelta_star,
    node_path_cdelta_star,
    node_radius_correlation,
    run,
)


class PurePathApproximationTests(unittest.TestCase):
    def test_zero_correlation_boundaries(self):
        self.assertAlmostEqual(absolute_normal_correlation(0.0), 0.0)
        self.assertAlmostEqual(dyad_path_cdelta_star(0.0), 1.0)
        self.assertAlmostEqual(node_radius_correlation(0.0), 0.0)
        self.assertAlmostEqual(node_path_cdelta_star(0.0), 1.0)

    def test_perfect_correlation_boundaries(self):
        self.assertAlmostEqual(absolute_normal_correlation(1.0), 1.0)
        self.assertAlmostEqual(node_radius_correlation(1.0), 1.0)

    def test_small_population_run_matches_formulas(self):
        rows = run(n_batches=4, batch_size=20_000, seed=20261041)
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertLess(row["cdelta_absolute_formula_error"], 0.03)
            self.assertLess(row["profile_absolute_formula_error"], 0.04)
            if row["path"] == "dyad":
                self.assertLess(row["mantel_absolute_formula_error"], 0.04)


if __name__ == "__main__":
    unittest.main()
