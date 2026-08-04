"""Small-scale structural comparison for the robust c_delta definition."""

from __future__ import annotations

import csv
from itertools import permutations
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    c_delta_from_profiles,
    divergence_vector,
    huber_reference_profile,
)
from scripts.run_robust_cdelta_grid import make_scenario, wilson


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "huber_radius": lambda z: huber_reference_profile(z),
    "huber_l2_floor0.5": lambda z: huber_reference_profile(z, radial_floor=0.5),
    "huber_l2_floor1": lambda z: huber_reference_profile(z, radial_floor=1.0),
    "huber_radius_cap6": lambda z: huber_reference_profile(z, cap=6.0),
}


SCENARIOS = (
    "null_clean",
    "null_contam_p05",
    "matched_p01_m8",
    "diffuse_aligned",
    "t2_matched",
    "bimodal_aligned",
    "unmatched_masking",
)


def _profile_test(
    sx: np.ndarray,
    sy: np.ndarray,
    rng: np.random.Generator,
    n_perm: int,
) -> tuple[float, float, float]:
    result = c_delta_from_profiles(sx, sy)
    observed = float(result["raw"])
    denominator = float(sx.mean() * sy.mean())
    permuted = np.asarray([rng.permutation(sy) for _ in range(n_perm)])
    statistics = (permuted @ sx) / sx.size / denominator
    p_value = (int(np.sum(statistics >= observed)) + 1) / (n_perm + 1)
    correlation = float(np.corrcoef(sx, sy)[0, 1])
    return p_value, observed, correlation


def run_small_grid(
    *,
    sample_sizes: tuple[int, ...] = (40, 80),
    repetitions: int = 250,
    n_perm: int = 199,
    seed: int = 20260808,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for scenario in SCENARIOS:
            summary = {
                method: {"reject": 0, "raw": [], "corr": []}
                for method in METHODS
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                for method, profile_fn in METHODS.items():
                    p_value, raw, corr = _profile_test(
                        profile_fn(x), profile_fn(y), rng, n_perm
                    )
                    values = summary[method]
                    values["reject"] += int(p_value < 0.05)
                    values["raw"].append(raw)
                    values["corr"].append(corr)
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
                        "mean_raw": float(np.mean(values["raw"])),
                        "mean_profile_correlation": float(np.mean(values["corr"])),
                    }
                )
    return rows


def exact_reference_check() -> list[dict[str, float | int | str]]:
    x = np.array([-3.0, -1.0, 0.5, 2.0, 7.0, 11.0])
    y = np.array([-2.0, 0.0, 1.0, 3.0, 8.0, 13.0])
    rows: list[dict[str, float | int | str]] = []
    for method, profile_fn in METHODS.items():
        sx, sy = profile_fn(x), profile_fn(y)
        values = [
            float(c_delta_from_profiles(sx, sy[list(order)])["raw"])
            for order in permutations(range(y.size))
        ]
        rows.append(
            {
                "method": method,
                "n": x.size,
                "permutations": len(values),
                "permutation_mean": float(np.mean(values)),
                "absolute_error_from_one": abs(float(np.mean(values)) - 1.0),
            }
        )
    return rows


def influence_path() -> list[dict[str, float | str]]:
    ordinary = np.linspace(-2.0, 2.0, 41)
    rows: list[dict[str, float | str]] = []
    for magnitude in (4.0, 8.0, 16.0, 64.0, 256.0, 1024.0):
        sample = np.append(ordinary, magnitude)
        for method, profile_fn in METHODS.items():
            scores = profile_fn(sample)
            rows.append(
                {
                    "magnitude": magnitude,
                    "method": method,
                    "ordinary_mean_score": float(np.mean(scores[:-1])),
                    "remote_score": float(scores[-1]),
                    "remote_to_ordinary_ratio": float(scores[-1] / np.mean(scores[:-1])),
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
    outputs = {
        PROJECT_ROOT / "results" / "robust_definition_stage2_grid_20260804.tsv": run_small_grid(),
        PROJECT_ROOT / "results" / "robust_definition_exact_reference_20260804.tsv": exact_reference_check(),
        PROJECT_ROOT / "results" / "robust_definition_influence_path_20260804.tsv": influence_path(),
    }
    for path, rows in outputs.items():
        write_tsv(path, rows)
        print(path)
