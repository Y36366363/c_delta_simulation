from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np

from cdelta import c_delta, divergence_vector
from scripts.run_paired_salience_validation import (
    distance_matrix_correlation,
    make_salience_scenario,
)
from scripts.run_tail_factor_comparison import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def permutation_p_values(dx, dy, *, n_perm, seed):
    """Compute all three correlation-equivalent permutation p-values."""
    rng = np.random.default_rng(seed)
    zx = (dx - np.mean(dx)) / np.std(dx)
    zy = (dy - np.mean(dy)) / np.std(dy)
    observed = float(np.mean(zx * zy))
    permuted = np.asarray(
        [float(np.mean(zx * rng.permutation(zy))) for _ in range(n_perm)]
    )
    return {
        "greater": (np.count_nonzero(permuted >= observed) + 1) / (n_perm + 1),
        "less": (np.count_nonzero(permuted <= observed) + 1) / (n_perm + 1),
        "two-sided": (
            np.count_nonzero(np.abs(permuted) >= abs(observed)) + 1
        )
        / (n_perm + 1),
    }


def exact_information_loss_example():
    """Return a same-salience, different-geometry L2 counterexample."""
    magnitudes = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 5.0])
    x = magnitudes * np.array([-1.0, -1.0, -1.0, -1.0, 1.0, 1.0])
    y = magnitudes * np.array([1.0, -1.0, -1.0, 1.0, 1.0, -1.0])
    dx = divergence_vector(x, kind="l2")
    dy = divergence_vector(y, kind="l2")
    return [{
        "example": "same_l2_salience_different_geometry",
        "max_divergence_difference": round(float(np.max(np.abs(dx - dy))), 8),
        "divergence_correlation": round(float(np.corrcoef(dx, dy)[0, 1]), 8),
        "distance_matrix_correlation": round(distance_matrix_correlation(x, y), 8),
        "raw_pearson": round(float(np.corrcoef(x, y)[0, 1]), 8),
        "c_delta": round(c_delta(x, y, kind="l2").raw, 8),
    }]


def run_alternative_validation():
    scenario_map = {
        "positive": "diffuse_aligned",
        "null": "diffuse_null",
        "negative": "diffuse_reverse",
    }
    repetitions = 400
    n_perm = 399
    rows = []
    for kind_index, kind in enumerate(["l2", "l1"]):
        for scenario_index, (signal, scenario) in enumerate(scenario_map.items()):
            rejected = {name: 0 for name in ["greater", "less", "two-sided"]}
            correlations = []
            for rep in range(repetitions):
                seed = (
                    20260731
                    + kind_index * 10_000_000
                    + scenario_index * 100_000
                    + rep
                )
                x, y = make_salience_scenario(scenario, n=80, seed=seed)
                result = c_delta(x, y, kind=kind)
                correlations.append(result.direction_correlation)
                p_values = permutation_p_values(
                    result.dx, result.dy, n_perm=n_perm, seed=seed + 20_000_000
                )
                for alternative, p_value in p_values.items():
                    rejected[alternative] += p_value < 0.05
            for alternative in ["greater", "less", "two-sided"]:
                rows.append({
                    "kind": kind,
                    "signal": signal,
                    "alternative": alternative,
                    "n": 80,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "mean_divergence_correlation": round(
                        float(np.mean(correlations)), 4
                    ),
                    "rejection_rate": round(
                        rejected[alternative] / repetitions, 4
                    ),
                })
    return rows


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    write_tsv(
        RESULTS_DIR / "row_aggregation_exact_example_20260731.tsv",
        exact_information_loss_example(),
    )
    write_tsv(
        RESULTS_DIR / "salience_alternative_summary_20260731.tsv",
        run_alternative_validation(),
    )


if __name__ == "__main__":
    main()
