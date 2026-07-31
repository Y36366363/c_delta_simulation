from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np

from cdelta import _wilson_interval, c_delta
from scripts.run_tail_factor_comparison import fast_permutation_p_value, write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def distance_matrix_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation of upper-triangular pairwise distances."""
    upper = np.triu_indices(x.size, k=1)
    x_distances = np.abs(x[:, None] - x[None, :])[upper]
    y_distances = np.abs(y[:, None] - y[None, :])[upper]
    return float(np.corrcoef(x_distances, y_distances)[0, 1])


def signed_centered_values(
    levels: np.ndarray,
    *,
    rng: np.random.Generator,
) -> np.ndarray:
    """Assign independent signs and center without changing pairwise distances."""
    signs = rng.choice([-1.0, 1.0], size=levels.size)
    values = signs * levels
    return values - float(np.mean(values))


def make_salience_scenario(
    scenario: str,
    *,
    n: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    m = n

    if scenario == "diffuse_aligned":
        x_levels = np.linspace(0.8, 1.2, m)
        y_levels = np.clip(x_levels + rng.normal(0.0, 0.035, m), 0.65, None)
    elif scenario == "diffuse_null":
        x_levels = np.linspace(0.8, 1.2, m)
        y_levels = rng.permutation(
            np.clip(x_levels + rng.normal(0.0, 0.035, m), 0.65, None)
        )
    elif scenario == "diffuse_reverse":
        x_levels = np.linspace(0.8, 1.2, m)
        y_levels = x_levels[::-1]
    elif scenario == "full_profile_aligned":
        x_levels = np.linspace(0.25, 2.0, m)
        y_levels = np.clip(x_levels + rng.normal(0.0, 0.08, m), 0.10, None)
    elif scenario == "top_pair_only":
        x_levels = np.linspace(0.25, 2.0, m)
        y_levels = (
            rng.permutation(x_levels[:-2]).tolist() + x_levels[-2:].tolist()
        )
        y_levels = np.asarray(y_levels, dtype=float)
    elif scenario == "profile_null":
        x_levels = np.linspace(0.25, 2.0, m)
        y_levels = rng.permutation(x_levels)
    elif scenario == "sparse_extreme_aligned":
        x_levels = np.linspace(0.8, 1.2, m)
        x_levels[-2:] = 4.0
        y_levels = np.clip(x_levels + rng.normal(0.0, 0.035, m), 0.65, None)
        y_levels[-2:] = 4.0
    else:
        raise ValueError(f"unknown scenario: {scenario}")

    pair_order = rng.permutation(m)
    x_levels = np.asarray(x_levels)[pair_order]
    y_levels = np.asarray(y_levels)[pair_order]
    x = signed_centered_values(x_levels, rng=rng)
    y = signed_centered_values(y_levels, rng=rng)
    return x, y


def run_validation() -> tuple[list[dict], list[dict]]:
    scenarios = [
        "diffuse_aligned",
        "diffuse_null",
        "diffuse_reverse",
        "full_profile_aligned",
        "top_pair_only",
        "profile_null",
        "sparse_extreme_aligned",
    ]
    n = 80
    repetitions = 500
    n_perm = 499
    rows = []

    for kind_offset, kind in enumerate(["l2", "l1"]):
        for scenario_offset, scenario in enumerate(scenarios):
            for rep in range(repetitions):
                seed = (
                    20260731
                    + kind_offset * 100_000_000
                    + scenario_offset * 1_000_000
                    + rep
                )
                x, y = make_salience_scenario(scenario, n=n, seed=seed)
                result = c_delta(x, y, kind=kind)
                p_value = fast_permutation_p_value(
                    result.dx,
                    result.dy,
                    result.raw,
                    n_perm=n_perm,
                    seed=seed + 50_000_000,
                )
                abs_x = np.abs(x - np.mean(x))
                abs_y = np.abs(y - np.mean(y))
                rows.append(
                    {
                        "kind": kind,
                        "scenario": scenario,
                        "n": n,
                        "repetition": rep,
                        "n_perm": n_perm,
                        "c_delta": round(result.raw, 8),
                        "divergence_correlation": round(
                            result.direction_correlation, 8
                        ),
                        "p_value": round(p_value, 8),
                        "rejected": int(p_value < 0.05),
                        "raw_pearson": round(float(np.corrcoef(x, y)[0, 1]), 8),
                        "absolute_deviation_pearson": round(
                            float(np.corrcoef(abs_x, abs_y)[0, 1]), 8
                        ),
                        "distance_matrix_correlation": round(
                            distance_matrix_correlation(x, y), 8
                        ),
                        "x_max_to_median_absolute_deviation": round(
                            float(np.max(abs_x) / np.median(abs_x)), 8
                        ),
                        "y_max_to_median_absolute_deviation": round(
                            float(np.max(abs_y) / np.median(abs_y)), 8
                        ),
                    }
                )

    summaries = []
    for kind in ["l2", "l1"]:
        for scenario in scenarios:
            subset = [
                row
                for row in rows
                if row["kind"] == kind and row["scenario"] == scenario
            ]
            reject_count = int(sum(row["rejected"] for row in subset))
            low, high = _wilson_interval(reject_count, len(subset))
            summaries.append(
                {
                    "kind": kind,
                    "scenario": scenario,
                    "n": n,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejection_rate": round(reject_count / repetitions, 4),
                    "wilson_low": round(float(low), 4),
                    "wilson_high": round(float(high), 4),
                    "mean_c_delta": round(
                        float(np.mean([row["c_delta"] for row in subset])), 4
                    ),
                    "mean_divergence_correlation": round(
                        float(
                            np.mean(
                                [row["divergence_correlation"] for row in subset]
                            )
                        ),
                        4,
                    ),
                    "mean_raw_pearson": round(
                        float(np.mean([row["raw_pearson"] for row in subset])), 4
                    ),
                    "mean_absolute_deviation_pearson": round(
                        float(
                            np.mean(
                                [
                                    row["absolute_deviation_pearson"]
                                    for row in subset
                                ]
                            )
                        ),
                        4,
                    ),
                    "mean_distance_matrix_correlation": round(
                        float(
                            np.mean(
                                [
                                    row["distance_matrix_correlation"]
                                    for row in subset
                                ]
                            )
                        ),
                        4,
                    ),
                    "median_max_to_median_absolute_deviation": round(
                        float(
                            np.median(
                                [
                                    (
                                        row[
                                            "x_max_to_median_absolute_deviation"
                                        ]
                                        + row[
                                            "y_max_to_median_absolute_deviation"
                                        ]
                                    )
                                    / 2
                                    for row in subset
                                ]
                            )
                        ),
                        4,
                    ),
                }
            )
    return rows, summaries


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows, summaries = run_validation()
    write_tsv(RESULTS_DIR / "paired_salience_validation_20260731.tsv", rows)
    write_tsv(RESULTS_DIR / "paired_salience_summary_20260731.tsv", summaries)


if __name__ == "__main__":
    main()
