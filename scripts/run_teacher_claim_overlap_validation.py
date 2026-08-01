from __future__ import annotations

import csv
import sys
from math import comb
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import c_delta  # noqa: E402
from scripts.run_paired_salience_validation import distance_matrix_correlation  # noqa: E402


def background_sample(rng, n, background):
    if background == "normal":
        return rng.normal(size=n)
    if background == "t3":
        return rng.standard_t(3, size=n)
    if background == "t2":
        return rng.standard_t(2, size=n)
    raise ValueError(background)


def mad_standardize(values):
    centered = values - np.median(values)
    mad = np.median(np.abs(centered))
    return centered / mad


def make_overlap_scenario(n, background, overlap_fraction, seed):
    rng = np.random.default_rng(seed)
    x = mad_standardize(background_sample(rng, n, background))
    y = mad_standardize(background_sample(rng, n, background))
    k = max(2, int(round(0.05 * n)))
    indices = rng.permutation(n)
    x_indices = indices[:k]
    overlap = int(round(k * overlap_fraction))
    shared = x_indices[:overlap]
    available = np.setdiff1d(np.arange(n), x_indices, assume_unique=False)
    y_only = rng.choice(available, size=k - overlap, replace=False)
    y_indices = np.concatenate([shared, y_only])
    signs_x = rng.choice([-1.0, 1.0], size=k)
    signs_y = rng.choice([-1.0, 1.0], size=k)
    x[x_indices] = 8.0 * signs_x
    y[y_indices] = 8.0 * signs_y
    return x, y, k, overlap


def permutation_p_value(dx, dy, n_perm, seed):
    rng = np.random.default_rng(seed)
    zx = (dx - np.mean(dx)) / np.std(dx)
    zy = (dy - np.mean(dy)) / np.std(dy)
    observed = float(np.mean(zx * zy))
    exceed = 0
    for _ in range(n_perm):
        exceed += float(np.mean(zx * rng.permutation(zy))) >= observed
    return (exceed + 1) / (n_perm + 1)


def wilson(successes, total, z=1.959963984540054):
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return center - half, center + half


def run_overlap_grid():
    repetitions = 300
    n_perm = 199
    overlap_fractions = [0.0, 0.25, 0.5, 0.75, 1.0]
    rows = []
    condition = 0
    for kind in ["l2", "l1"]:
        for n in [40, 80, 160]:
            for background in ["normal", "t3", "t2"]:
                for fraction in overlap_fractions:
                    rejected = 0
                    correlations = []
                    observed_overlaps = []
                    for rep in range(repetitions):
                        seed = 20260731 + condition * 1_000_000 + rep
                        x, y, k, overlap = make_overlap_scenario(
                            n, background, fraction, seed
                        )
                        result = c_delta(x, y, kind=kind)
                        p_value = permutation_p_value(
                            result.dx, result.dy, n_perm, seed + 500_000
                        )
                        rejected += p_value < 0.05
                        correlations.append(result.direction_correlation)
                        observed_overlaps.append(overlap / k)
                    low, high = wilson(rejected, repetitions)
                    rows.append({
                        "kind": kind,
                        "n": n,
                        "background": background,
                        "k": k,
                        "target_overlap_fraction": fraction,
                        "observed_overlap_fraction": round(float(np.mean(observed_overlaps)), 4),
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": round(rejected / repetitions, 4),
                        "wilson_low": round(float(low), 4),
                        "wilson_high": round(float(high), 4),
                        "mean_divergence_correlation": round(float(np.mean(correlations)), 4),
                    })
                    condition += 1
    return rows


def run_null_calibration():
    repetitions = 1000
    n_perm = 499
    rows = []
    condition = 0
    for kind in ["l2", "l1"]:
        for background in ["normal", "t3", "t2"]:
            rejected = 0
            correlations = []
            for rep in range(repetitions):
                seed = 20310731 + condition * 1_000_000 + rep
                rng = np.random.default_rng(seed)
                x = mad_standardize(background_sample(rng, 80, background))
                y = mad_standardize(background_sample(rng, 80, background))
                result = c_delta(x, y, kind=kind)
                p_value = permutation_p_value(
                    result.dx, result.dy, n_perm, seed + 500_000
                )
                rejected += p_value < 0.05
                correlations.append(result.direction_correlation)
            low, high = wilson(rejected, repetitions)
            rows.append({
                "kind": kind,
                "n": 80,
                "background": background,
                "repetitions": repetitions,
                "n_perm": n_perm,
                "rejection_rate": round(rejected / repetitions, 4),
                "wilson_low": round(float(low), 4),
                "wilson_high": round(float(high), 4),
                "mean_divergence_correlation": round(float(np.mean(correlations)), 4),
            })
            condition += 1
    return rows


def run_focused_normal_null():
    repetitions = 5000
    n_perm = 499
    rows = []
    for kind_index, kind in enumerate(["l2", "l1"]):
        rejected = 0
        for rep in range(repetitions):
            seed = 20510731 + kind_index * 10_000_000 + rep
            rng = np.random.default_rng(seed)
            x = mad_standardize(background_sample(rng, 80, "normal"))
            y = mad_standardize(background_sample(rng, 80, "normal"))
            result = c_delta(x, y, kind=kind)
            p_value = permutation_p_value(
                result.dx, result.dy, n_perm, seed + 700_000
            )
            rejected += p_value < 0.05
        low, high = wilson(rejected, repetitions)
        rows.append({
            "kind": kind,
            "n": 80,
            "background": "normal",
            "repetitions": repetitions,
            "n_perm": n_perm,
            "rejection_rate": round(rejected / repetitions, 4),
            "wilson_low": round(float(low), 4),
            "wilson_high": round(float(high), 4),
        })
    return rows


def run_geometry_loss():
    rng = np.random.default_rng(20410731)
    rows = []
    for n in [40, 80, 160]:
        correlations = []
        for _ in range(1000):
            half = n // 2
            magnitudes = rng.uniform(0.25, 2.0, size=half)
            x = np.concatenate([magnitudes, -magnitudes])
            flips = rng.choice([-1.0, 1.0], size=half)
            y = np.concatenate([flips * magnitudes, -flips * magnitudes])
            order = rng.permutation(n)
            x = x[order]
            y = y[order]
            result = c_delta(x, y, kind="l2")
            correlations.append(distance_matrix_correlation(x, y))
            if abs(result.direction_correlation - 1.0) > 1e-10:
                raise AssertionError("salience vectors should match exactly")
        values = np.asarray(correlations)
        rows.append({
            "n": n,
            "repetitions": 1000,
            "divergence_correlation": 1.0,
            "mean_distance_matrix_correlation": round(float(np.mean(values)), 4),
            "q025_distance_matrix_correlation": round(float(np.quantile(values, 0.025)), 4),
            "q50_distance_matrix_correlation": round(float(np.quantile(values, 0.5)), 4),
            "q975_distance_matrix_correlation": round(float(np.quantile(values, 0.975)), 4),
        })
    return rows


def binary_overlap_correlation(n, k, overlap):
    """Pearson correlation of two binary salience labels with equal k."""
    return (n * overlap - k * k) / (k * (n - k))


def binary_overlap_pmf(n, k, overlap):
    """Exact chance-overlap probability for two independent size-k sets."""
    if not 0 <= overlap <= k <= n:
        raise ValueError("require 0 <= overlap <= k <= n")
    if k - overlap > n - k:
        return 0.0
    return comb(k, overlap) * comb(n - k, k - overlap) / comb(n, k)


def run_binary_overlap_bridge():
    """Compare the binary-overlap theory with continuous divergence scores."""
    repetitions = 200
    n_perm = 199
    n = 80
    k = 4
    rows = []
    condition = 0
    for kind in ["l2", "l1"]:
        for background in ["normal", "t3", "t2"]:
            for magnitude in [4.0, 6.0, 8.0, 12.0]:
                for overlap in range(k + 1):
                    correlations = []
                    rejected = 0
                    for rep in range(repetitions):
                        seed = 20610801 + condition * 1_000_000 + rep
                        x, y, _, observed_overlap = make_overlap_scenario(
                            n, background, overlap / k, seed
                        )
                        x[np.abs(x) == 8.0] *= magnitude / 8.0
                        y[np.abs(y) == 8.0] *= magnitude / 8.0
                        result = c_delta(x, y, kind=kind)
                        correlations.append(result.direction_correlation)
                        p_value = permutation_p_value(
                            result.dx, result.dy, n_perm, seed + 800_000
                        )
                        rejected += p_value < 0.05
                    low, high = wilson(rejected, repetitions)
                    theory = binary_overlap_correlation(n, k, observed_overlap)
                    mean_corr = float(np.mean(correlations))
                    rows.append({
                        "kind": kind,
                        "n": n,
                        "background": background,
                        "k": k,
                        "magnitude_mad": magnitude,
                        "overlap": observed_overlap,
                        "overlap_fraction": observed_overlap / k,
                        "binary_theory_correlation": round(theory, 4),
                        "mean_divergence_correlation": round(mean_corr, 4),
                        "attenuation_from_binary_theory": round(mean_corr - theory, 4),
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": round(rejected / repetitions, 4),
                        "wilson_low": round(float(low), 4),
                        "wilson_high": round(float(high), 4),
                    })
                    condition += 1
    return rows


def write_tsv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    output = PROJECT_ROOT / "results"
    output.mkdir(exist_ok=True)
    write_tsv(output / "teacher_claim_overlap_grid_20260731.tsv", run_overlap_grid())
    write_tsv(output / "teacher_claim_null_validation_20260731.tsv", run_null_calibration())
    write_tsv(output / "teacher_claim_focused_normal_null_20260731.tsv", run_focused_normal_null())
    write_tsv(output / "row_aggregation_geometry_loss_20260731.tsv", run_geometry_loss())
    write_tsv(output / "binary_overlap_bridge_20260801.tsv", run_binary_overlap_bridge())
