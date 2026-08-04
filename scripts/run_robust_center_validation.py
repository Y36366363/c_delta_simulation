"""Compare centre-based and h-star-inspired c_delta profile definitions."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import center_salience_vector, divergence_vector, h_star_profile


METHODS = {
    "original_pairwise_l2": lambda z: divergence_vector(z, kind="l2"),
    "centroid_radius": lambda z: center_salience_vector(z, center="mean"),
    "median_radius": lambda z: center_salience_vector(z, center="median"),
    "iqr_fit_all_radius": lambda z: center_salience_vector(
        z, center="iqr_inlier_mean"
    ),
    "iqr_fit_all_capped3": lambda z: center_salience_vector(
        z, center="iqr_inlier_mean", cap=3.0
    ),
    "hstar_profile_l2": lambda z: h_star_profile(z, eta=2.0),
    "hstar_profile_l1": lambda z: h_star_profile(z, eta=1.0),
}


def _scenario(
    name: str, rng: np.random.Generator, n: int
) -> tuple[np.ndarray, np.ndarray]:
    if name == "clean_null":
        return rng.normal(size=n), rng.normal(size=n)

    if name == "random_outlier_null":
        x, y = rng.normal(size=n), rng.normal(size=n)
        x[rng.integers(n)] += 10.0
        y[rng.integers(n)] += 10.0
        return x, y

    if name == "matched_outlier":
        x, y = rng.normal(size=n), rng.normal(size=n)
        index = int(rng.integers(n))
        x[index] += 8.0
        y[index] += 8.0
        return x, y

    if name == "diffuse_salience":
        magnitude = rng.uniform(0.7, 1.8, size=n)
        x = rng.choice([-1.0, 1.0], size=n) * magnitude
        y_magnitude = magnitude + rng.normal(scale=0.18, size=n)
        y = rng.choice([-1.0, 1.0], size=n) * y_magnitude
        return x, y

    if name == "t2_matched_pair":
        x, y = rng.standard_t(2, size=n), rng.standard_t(2, size=n)
        indices = rng.choice(n, size=2, replace=False)
        x[indices] += 8.0
        y[indices] += 8.0
        return x, y

    if name == "unmatched_masking":
        x, y = rng.standard_t(3, size=n), rng.standard_t(3, size=n)
        indices = rng.choice(n, size=4, replace=False)
        planted = indices[:2]
        x[planted] += 6.0
        y[planted] += 6.0
        x[indices[2]] += 20.0
        y[indices[3]] += 20.0
        return x, y

    raise ValueError(f"unknown scenario: {name}")


def _profile_test(
    sx: np.ndarray,
    sy: np.ndarray,
    rng: np.random.Generator,
    n_perm: int,
) -> tuple[float, float]:
    mean_x, mean_y = float(np.mean(sx)), float(np.mean(sy))
    observed = float(np.mean(sx * sy) / (mean_x * mean_y))
    exceed = sum(
        float(np.mean(sx * rng.permutation(sy)) / (mean_x * mean_y)) >= observed
        for _ in range(n_perm)
    )
    p_value = (exceed + 1) / (n_perm + 1)
    correlation = float(np.corrcoef(sx, sy)[0, 1])
    return p_value, correlation


def _wilson(count: int, total: int) -> tuple[float, float]:
    z = 1.959963984540054
    p = count / total
    denominator = 1.0 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total**2))
    return float(centre - half / denominator), float(centre + half / denominator)


def run_validation(
    *,
    n: int = 80,
    repetitions: int = 500,
    n_perm: int = 199,
    seed: int = 20260804,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    scenarios = [
        "clean_null",
        "random_outlier_null",
        "matched_outlier",
        "diffuse_salience",
        "t2_matched_pair",
        "unmatched_masking",
    ]
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios:
        summaries = {
            method: {"reject": 0, "p": [], "corr": []} for method in METHODS
        }
        for _ in range(repetitions):
            x, y = _scenario(scenario, rng, n)
            for method, profile_fn in METHODS.items():
                sx, sy = profile_fn(x), profile_fn(y)
                p_value, correlation = _profile_test(sx, sy, rng, n_perm)
                summaries[method]["reject"] += p_value < 0.05
                summaries[method]["p"].append(p_value)
                summaries[method]["corr"].append(correlation)
        for method, summary in summaries.items():
            reject = int(summary["reject"])
            low, high = _wilson(reject, repetitions)
            rows.append(
                {
                    "scenario": scenario,
                    "method": method,
                    "n": n,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejections": reject,
                    "rejection_rate": reject / repetitions,
                    "wilson_low": low,
                    "wilson_high": high,
                    "mean_profile_correlation": float(np.mean(summary["corr"])),
                    "median_p_value": float(np.median(summary["p"])),
                }
            )
    return rows


def influence_path() -> list[dict[str, float | str]]:
    ordinary = np.linspace(-2.0, 2.0, 81)
    rows: list[dict[str, float | str]] = []
    for magnitude in [4.0, 8.0, 16.0, 64.0, 256.0, 1024.0]:
        values = np.append(ordinary, magnitude)
        for method, profile_fn in METHODS.items():
            scores = profile_fn(values)
            rows.append(
                {
                    "magnitude": magnitude,
                    "method": method,
                    "outlier_score": float(scores[-1]),
                    "ordinary_mean_score": float(np.mean(scores[:-1])),
                    "outlier_to_ordinary_ratio": float(
                        scores[-1] / np.mean(scores[:-1])
                    ),
                }
            )
    return rows


def _write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    validation_path = PROJECT_ROOT / "results" / "robust_center_validation_20260804.tsv"
    influence_path_out = PROJECT_ROOT / "results" / "robust_center_influence_20260804.tsv"
    _write_tsv(validation_path, run_validation())
    _write_tsv(influence_path_out, influence_path())
    print(validation_path)
    print(influence_path_out)


if __name__ == "__main__":
    main()
