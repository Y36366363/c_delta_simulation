"""Small-building diagnostics for weak-null profile and Mantel inference."""

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import sys

import numpy as np
from scipy.stats import t as student_t


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_weak_null_local_tests_20260814 import (
    holm_adjust,
    mantel_weak_null_test,
    profile_weak_null_test,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def make_clustered_pair(
    rng: np.random.Generator,
    *,
    n_buildings: int,
    rooms_per_building: int,
    scenario: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Independent-building model with Gaussian or skew cluster heterogeneity."""
    blocks = np.repeat(np.arange(n_buildings), rooms_per_building)
    x = np.empty(blocks.size)
    y = np.empty(blocks.size)
    for building in range(n_buildings):
        members = blocks == building
        if scenario == "gaussian_cluster_null":
            center_x, center_y = rng.normal(scale=1.2, size=2)
            scale_x, scale_y = 1.0, 1.0
            correlation = 0.0
        elif scenario == "skew_scale_cluster_null":
            center_x, center_y = rng.normal(scale=0.6, size=2)
            scale_x, scale_y = np.exp(0.8 * rng.normal(size=2) - 0.32)
            correlation = 0.0
        elif scenario == "correlated_cluster_alt":
            center_x = rng.normal(scale=0.8)
            center_y = 0.7 * center_x + np.sqrt(1.0 - 0.7**2) * rng.normal(scale=0.8)
            latent_scale = rng.normal()
            scale_x = np.exp(0.55 * latent_scale - 0.15125)
            scale_y = np.exp(
                0.55 * (0.7 * latent_scale + np.sqrt(1.0 - 0.7**2) * rng.normal())
                - 0.15125
            )
            correlation = 0.45
        else:
            raise ValueError(f"unknown scenario: {scenario}")
        noise_x = rng.normal(size=rooms_per_building)
        noise_y = (
            correlation * noise_x
            + np.sqrt(1.0 - correlation**2) * rng.normal(size=rooms_per_building)
        )
        x[members] = center_x + scale_x * noise_x
        y[members] = center_y + scale_y * noise_y
    return x, y, blocks


def cluster_inference(
    estimate: float,
    influence: np.ndarray,
    blocks: np.ndarray,
) -> dict[str, float]:
    """Cluster-summed t and linearized wild sign-flip p-values."""
    labels = np.unique(blocks)
    cluster_scores = np.asarray(
        [np.sum(influence[blocks == label]) for label in labels]
    )
    n = influence.size
    b = labels.size
    standard_error = np.sqrt(
        b / (b - 1.0) * np.sum(cluster_scores**2)
    ) / n
    if standard_error <= 0.0:
        raise ValueError("cluster standard error is degenerate")
    statistic = estimate / standard_error
    t_p = float(2.0 * student_t.sf(abs(statistic), df=b - 1))
    if b <= 12:
        signs = np.asarray(list(product((-1.0, 1.0), repeat=b)))
    else:
        # Sign-flip is already a rejected diagnostic at B=6.  Avoid the
        # exponential 2^B orbit in the building-count extension.
        sign_rng = np.random.default_rng(2026081400 + b)
        signs = sign_rng.choice((-1.0, 1.0), size=(4096, b))
    reference = signs @ cluster_scores / n / standard_error
    signflip_p = float(np.mean(np.abs(reference) >= abs(statistic)))
    return {
        "cluster_standard_error": float(standard_error),
        "cluster_t": float(statistic),
        "cluster_t_p": t_p,
        "signflip_p": signflip_p,
        "max_cluster_score_share": float(
            np.max(np.abs(cluster_scores)) / np.sum(np.abs(cluster_scores))
        ),
    }


def run_validation(
    *, repetitions: int, n_buildings: int, rooms_per_building: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for scenario in (
        "gaussian_cluster_null",
        "skew_scale_cluster_null",
        "correlated_cluster_alt",
    ):
        records = []
        for _ in range(repetitions):
            x, y, blocks = make_clustered_pair(
                rng,
                n_buildings=n_buildings,
                rooms_per_building=rooms_per_building,
                scenario=scenario,
            )
            profile = profile_weak_null_test(x, y)
            mantel = mantel_weak_null_test(x, y)
            profile_cluster = cluster_inference(
                float(profile["estimate"]), np.asarray(profile["influence"]), blocks
            )
            mantel_cluster = cluster_inference(
                float(mantel["estimate"]), np.asarray(mantel["influence"]), blocks
            )
            holm_t = holm_adjust(
                profile_cluster["cluster_t_p"], mantel_cluster["cluster_t_p"]
            )
            holm_sign = holm_adjust(
                profile_cluster["signflip_p"], mantel_cluster["signflip_p"]
            )
            records.append(
                (
                    float(profile["p_value"]), profile_cluster["cluster_t_p"], profile_cluster["signflip_p"],
                    float(mantel["p_value"]), mantel_cluster["cluster_t_p"], mantel_cluster["signflip_p"],
                    holm_t[0], holm_t[1], holm_sign[0], holm_sign[1],
                    profile_cluster["max_cluster_score_share"], mantel_cluster["max_cluster_score_share"],
                    float(profile["estimate"]), float(mantel["estimate"]),
                )
            )
        values = np.asarray(records)
        null = scenario != "correlated_cluster_alt"
        room_fwer = np.mean((values[:, 0] <= 0.05) | (values[:, 3] <= 0.05)) if null else np.nan
        t_fwer = np.mean((values[:, 6] <= 0.05) | (values[:, 7] <= 0.05)) if null else np.nan
        sign_fwer = np.mean((values[:, 8] <= 0.05) | (values[:, 9] <= 0.05)) if null else np.nan
        count = int(round(t_fwer * repetitions)) if null else 0
        interval = wilson(count, repetitions) if null else (np.nan, np.nan)
        rows.append(
            {
                "phase": phase,
                "scenario": scenario,
                "n_buildings": n_buildings,
                "rooms_per_building": rooms_per_building,
                "repetitions": repetitions,
                "room_iid_profile_rejection": float(np.mean(values[:, 0] <= 0.05)),
                "cluster_t_profile_rejection": float(np.mean(values[:, 1] <= 0.05)),
                "signflip_profile_rejection": float(np.mean(values[:, 2] <= 0.05)),
                "room_iid_mantel_rejection": float(np.mean(values[:, 3] <= 0.05)),
                "cluster_t_mantel_rejection": float(np.mean(values[:, 4] <= 0.05)),
                "signflip_mantel_rejection": float(np.mean(values[:, 5] <= 0.05)),
                "room_iid_raw_fwer": float(room_fwer),
                "cluster_t_holm_fwer": float(t_fwer),
                "cluster_t_holm_wilson_low": interval[0],
                "cluster_t_holm_wilson_high": interval[1],
                "signflip_holm_fwer": float(sign_fwer),
                "mean_profile_max_cluster_score_share": float(np.mean(values[:, 10])),
                "mean_mantel_max_cluster_score_share": float(np.mean(values[:, 11])),
                "mean_profile_effect": float(np.mean(values[:, 12])),
                "mean_mantel_effect": float(np.mean(values[:, 13])),
                "cluster_t_both_rejection": float(np.mean((values[:, 6] <= 0.05) & (values[:, 7] <= 0.05))),
                "signflip_both_rejection": float(np.mean((values[:, 8] <= 0.05) & (values[:, 9] <= 0.05))),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase", choices=("pilot", "confirmatory", "count_extension"), default="pilot"
    )
    args = parser.parse_args()
    if args.phase == "pilot":
        rows = run_validation(
            phase=args.phase,
            repetitions=500,
            n_buildings=6,
            rooms_per_building=20,
            seed=2026081431,
        )
    elif args.phase == "confirmatory":
        rows = run_validation(
            phase=args.phase,
            repetitions=2_000,
            n_buildings=6,
            rooms_per_building=20,
            seed=2026081432,
        )
    else:
        rows = []
        for offset, n_buildings in enumerate((12, 24)):
            rows.extend(
                run_validation(
                    phase=args.phase,
                    repetitions=300,
                    n_buildings=n_buildings,
                    rooms_per_building=20,
                    seed=2026081433 + offset,
                )
            )
    RESULTS_DIR.mkdir(exist_ok=True)
    write_tsv(
        RESULTS_DIR / f"small_building_weak_null_{args.phase}_20260814.tsv",
        rows,
    )
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
