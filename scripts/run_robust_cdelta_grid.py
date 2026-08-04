"""Systematic contamination and background validation for robust c_delta."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import center_salience_vector, divergence_vector


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "iqr_fit_all": lambda z: center_salience_vector(z, center="iqr_inlier_mean"),
    "trim10_fit_all": lambda z: center_salience_vector(z, center="trimmed_mean"),
    "huber_fit_all": lambda z: center_salience_vector(z, center="huber"),
    "iqr_capped3": lambda z: center_salience_vector(
        z, center="iqr_inlier_mean", cap=3.0
    ),
    "huber_capped3": lambda z: center_salience_vector(z, center="huber", cap=3.0),
}


def _standardise(z: np.ndarray) -> np.ndarray:
    return (z - float(z.mean())) / float(z.std())


def make_scenario(
    name: str, n: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    if name == "null_clean":
        return rng.normal(size=n), rng.normal(size=n)

    if name.startswith("null_contam_p"):
        fraction = int(name.split("p")[1]) / 100
        x, y = rng.normal(size=n), rng.normal(size=n)
        k = max(1, int(round(fraction * n)))
        x[rng.choice(n, size=k, replace=False)] += 20.0
        y[rng.choice(n, size=k, replace=False)] += 20.0
        return x, y

    if name.startswith("matched_p"):
        fraction = int(name.split("p")[1].split("_")[0]) / 100
        x, y = rng.normal(size=n), rng.normal(size=n)
        k = max(1, int(round(fraction * n)))
        indices = rng.choice(n, size=k, replace=False)
        x[indices] += 8.0
        y[indices] += 8.0
        return x, y

    if name == "diffuse_aligned":
        magnitude = rng.uniform(0.7, 1.8, size=n)
        x = rng.choice([-1.0, 1.0], size=n) * magnitude
        y = rng.choice([-1.0, 1.0], size=n) * (magnitude + rng.normal(0, 0.18, n))
        return x, y

    if name == "t2_matched":
        x, y = rng.standard_t(2, n), rng.standard_t(2, n)
        indices = rng.choice(n, size=max(1, round(0.05 * n)), replace=False)
        x[indices] += 8.0
        y[indices] += 8.0
        return x, y

    if name == "skewed_aligned":
        latent = rng.lognormal(0.0, 0.8, n)
        x = _standardise(latent)
        y = _standardise(latent + rng.normal(0, 0.20, n))
        return x, y

    if name == "bimodal_aligned":
        labels = rng.choice([-1.0, 1.0], size=n)
        x = 3.0 * labels + rng.normal(0, 0.35, n)
        y = 4.0 * labels + rng.normal(0, 0.35, n)
        return x, y

    if name == "unmatched_masking":
        x, y = rng.standard_t(3, n), rng.standard_t(3, n)
        indices = rng.choice(n, size=max(4, round(0.05 * n)), replace=False)
        x[indices[:2]] += 6.0
        y[indices[:2]] += 6.0
        x[indices[2]] += 20.0
        y[indices[3]] += 20.0
        return x, y

    raise ValueError(f"unknown scenario: {name}")


def profile_test(
    sx: np.ndarray,
    sy: np.ndarray,
    rng: np.random.Generator,
    n_perm: int,
) -> tuple[float, float]:
    denominator = float(sx.mean() * sy.mean())
    observed = float(np.mean(sx * sy) / denominator)
    permuted = np.asarray([rng.permutation(sy) for _ in range(n_perm)])
    statistics = (permuted @ sx) / sx.size / denominator
    p_value = (int(np.sum(statistics >= observed)) + 1) / (n_perm + 1)
    return p_value, float(np.corrcoef(sx, sy)[0, 1])


def wilson(count: int, total: int) -> tuple[float, float]:
    z = 1.959963984540054
    p = count / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total**2))
    return float(centre - half / denominator), float(centre + half / denominator)


def run_grid(
    *,
    sample_sizes: tuple[int, ...] = (40, 80, 160),
    repetitions: int = 300,
    n_perm: int = 199,
    seed: int = 20260805,
) -> list[dict[str, float | int | str]]:
    scenarios = [
        "null_clean",
        "null_contam_p01",
        "null_contam_p05",
        "null_contam_p10",
        "matched_p01_m8",
        "matched_p05_m8",
        "diffuse_aligned",
        "t2_matched",
        "skewed_aligned",
        "bimodal_aligned",
        "unmatched_masking",
    ]
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for scenario in scenarios:
            summary = {
                method: {"reject": 0, "corr": [], "p": []}
                for method in METHODS
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                for method, profile_fn in METHODS.items():
                    sx, sy = profile_fn(x), profile_fn(y)
                    p_value, correlation = profile_test(sx, sy, rng, n_perm)
                    summary[method]["reject"] += int(p_value < 0.05)
                    summary[method]["corr"].append(correlation)
                    summary[method]["p"].append(p_value)
            for method, values in summary.items():
                reject = int(values["reject"])
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "scenario": scenario,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejections": reject,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                        "mean_profile_correlation": float(np.mean(values["corr"])),
                        "median_p_value": float(np.median(values["p"])),
                    }
                )
    return rows


def run_high_rep_null(
    *,
    sample_sizes: tuple[int, ...] = (80, 160),
    repetitions: int = 2000,
    n_perm: int = 199,
    seed: int = 20260806,
) -> list[dict[str, float | int | str]]:
    """Higher-replication calibration check for clean and contaminated nulls."""
    scenarios = ["null_clean", "null_contam_p05", "null_contam_p10"]
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for scenario in scenarios:
            summary = {method: 0 for method in METHODS}
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                for method, profile_fn in METHODS.items():
                    sx, sy = profile_fn(x), profile_fn(y)
                    p_value, _ = profile_test(sx, sy, rng, n_perm)
                    summary[method] += int(p_value < 0.05)
            for method, reject in summary.items():
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "scenario": scenario,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejections": reject,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
    return rows


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    output = PROJECT_ROOT / "results" / "robust_cdelta_grid_20260804.tsv"
    write_tsv(output, run_grid())
    null_output = PROJECT_ROOT / "results" / "robust_cdelta_null_high_rep_20260804.tsv"
    write_tsv(null_output, run_high_rep_null())
    print(output)
    print(null_output)
