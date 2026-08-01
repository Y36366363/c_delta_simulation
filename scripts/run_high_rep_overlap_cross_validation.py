from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_teacher_claim_overlap_validation import (
    background_sample,
    binary_overlap_correlation,
    mad_standardize,
    make_overlap_scenario,
    permutation_p_value,
    wilson,
)

sys.path.insert(0, str(PROJECT_ROOT / "src"))
from cdelta import c_delta  # noqa: E402


def make_random_set_null(n, background, magnitude, seed):
    rng = np.random.default_rng(seed)
    x = mad_standardize(background_sample(rng, n, background))
    y = mad_standardize(background_sample(rng, n, background))
    k = max(2, int(round(0.05 * n)))
    x_indices = rng.choice(n, size=k, replace=False)
    y_indices = rng.choice(n, size=k, replace=False)
    x[x_indices] = magnitude * rng.choice([-1.0, 1.0], size=k)
    y[y_indices] = magnitude * rng.choice([-1.0, 1.0], size=k)
    overlap = int(np.intersect1d(x_indices, y_indices).size)
    return x, y, k, overlap


def run_forced_overlap_cross_validation():
    repetitions = 1000
    n_perm = 199
    n = 80
    k = 4
    rows = []
    condition = 0
    for kind in ["l2", "l1"]:
        for background in ["normal", "t3", "t2"]:
            for overlap in range(k + 1):
                rejected = 0
                correlations = []
                for rep in range(repetitions):
                    seed = 20710801 + condition * 2_000_000 + rep
                    x, y, _, observed = make_overlap_scenario(
                        n, background, overlap / k, seed
                    )
                    result = c_delta(x, y, kind=kind)
                    correlations.append(result.direction_correlation)
                    p_value = permutation_p_value(
                        result.dx, result.dy, n_perm, seed + 900_000
                    )
                    rejected += p_value < 0.05
                low, high = wilson(rejected, repetitions)
                values = np.asarray(correlations)
                rows.append({
                    "kind": kind,
                    "n": n,
                    "background": background,
                    "k": k,
                    "magnitude_mad": 8.0,
                    "overlap": observed,
                    "overlap_fraction": observed / k,
                    "binary_theory_correlation": round(
                        binary_overlap_correlation(n, k, observed), 4
                    ),
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "mean_divergence_correlation": round(float(values.mean()), 4),
                    "q025_divergence_correlation": round(float(np.quantile(values, 0.025)), 4),
                    "q975_divergence_correlation": round(float(np.quantile(values, 0.975)), 4),
                    "rejection_rate": round(rejected / repetitions, 4),
                    "wilson_low": round(float(low), 4),
                    "wilson_high": round(float(high), 4),
                })
                condition += 1
    return rows


def run_random_set_null():
    repetitions = 3000
    n_perm = 199
    n = 80
    rows = []
    overlap_rows = []
    condition = 0
    for kind in ["l2", "l1"]:
        for background in ["normal", "t3", "t2"]:
            rejected = 0
            overlap_counts = {m: 0 for m in range(5)}
            overlap_rejections = {m: 0 for m in range(5)}
            correlations = []
            for rep in range(repetitions):
                seed = 20810801 + condition * 5_000_000 + rep
                x, y, k, overlap = make_random_set_null(
                    n, background, 8.0, seed
                )
                result = c_delta(x, y, kind=kind)
                correlations.append(result.direction_correlation)
                p_value = permutation_p_value(
                    result.dx, result.dy, n_perm, seed + 1_100_000
                )
                decision = p_value < 0.05
                rejected += decision
                overlap_counts[overlap] += 1
                overlap_rejections[overlap] += decision
            low, high = wilson(rejected, repetitions)
            rows.append({
                "kind": kind,
                "n": n,
                "background": background,
                "k": k,
                "magnitude_mad": 8.0,
                "repetitions": repetitions,
                "n_perm": n_perm,
                "expected_overlap": k * k / n,
                "mean_observed_overlap": round(
                    sum(m * count for m, count in overlap_counts.items())
                    / repetitions,
                    4,
                ),
                "mean_divergence_correlation": round(
                    float(np.mean(correlations)), 4
                ),
                "rejection_rate": round(rejected / repetitions, 4),
                "wilson_low": round(float(low), 4),
                "wilson_high": round(float(high), 4),
            })
            for overlap, count in overlap_counts.items():
                if count:
                    overlap_rows.append({
                        "kind": kind,
                        "background": background,
                        "overlap": overlap,
                        "count": count,
                        "frequency": round(count / repetitions, 4),
                        "conditional_rejection_rate": round(
                            overlap_rejections[overlap] / count, 4
                        ),
                    })
            condition += 1
    return rows, overlap_rows


def write_tsv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    output = PROJECT_ROOT / "results"
    output.mkdir(exist_ok=True)
    forced = run_forced_overlap_cross_validation()
    random_null, overlap_layers = run_random_set_null()
    write_tsv(output / "forced_overlap_high_rep_20260801.tsv", forced)
    write_tsv(output / "random_set_null_high_rep_20260801.tsv", random_null)
    write_tsv(output / "random_set_null_overlap_layers_20260801.tsv", overlap_layers)
