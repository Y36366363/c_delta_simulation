"""First-stage pilot for the Huber robust-reference c_delta definition."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    bootstrap_ci,
    c_delta,
    center_salience_vector,
    make_scenario,
    permutation_test,
    permutation_test_profiles,
    robust_profile_bootstrap_ci,
)


SCENARIOS = [
    "null_normal",
    "aligned_normal",
    "inverted_divergence",
    "heavy_tailed",
    "skewed",
    "contaminated_aligned",
]


def profiles(x: np.ndarray, y: np.ndarray, method: str) -> tuple[np.ndarray, np.ndarray]:
    if method == "original_l2":
        from cdelta import divergence_vector

        return divergence_vector(x, kind="l2"), divergence_vector(y, kind="l2")
    if method == "huber_reference":
        return (
            center_salience_vector(x, center="huber"),
            center_salience_vector(y, center="huber"),
        )
    if method == "huber_reference_cap6":
        return (
            center_salience_vector(x, center="huber", cap=6.0),
            center_salience_vector(y, center="huber", cap=6.0),
        )
    if method == "iqr_reference":
        return (
            center_salience_vector(x, center="iqr_inlier_mean"),
            center_salience_vector(y, center="iqr_inlier_mean"),
        )
    raise ValueError(f"unknown method: {method}")


METHODS = [
    "original_l2",
    "huber_reference",
    "huber_reference_cap6",
    "iqr_reference",
]


def pilot(
    *, n: int = 60, n_perm: int = 499, n_boot: int = 500, seed: int = 20260804
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for scenario_offset, scenario in enumerate(SCENARIOS):
        x, y = make_scenario(scenario, n, seed=seed + scenario_offset)
        for method in METHODS:
            sx, sy = profiles(x, y, method)
            perm = permutation_test_profiles(sx, sy, n_perm=n_perm, seed=seed + 1000 + scenario_offset)
            if method == "original_l2":
                legacy = c_delta(x, y)
                ci = bootstrap_ci(x, y, n_boot=n_boot, seed=seed + 2000 + scenario_offset)
                raw, corr, normalized = legacy.raw, legacy.direction_correlation, legacy.normalized_pairing
                ci_lower, ci_upper = ci["lower"], ci["upper"]
            else:
                ci = robust_profile_bootstrap_ci(
                    x,
                    y,
                    center="huber" if "huber" in method else "iqr_inlier_mean",
                    cap=6.0 if method.endswith("cap6") else None,
                    n_boot=n_boot,
                    seed=seed + 2000 + scenario_offset,
                )
                raw = float(perm["observed"])
                corr = float(np.corrcoef(sx, sy)[0, 1])
                normalized = np.nan
                ci_lower, ci_upper = ci["lower"], ci["upper"]
            rows.append(
                {
                    "scenario": scenario,
                    "method": method,
                    "n": n,
                    "n_perm": n_perm,
                    "n_boot": n_boot,
                    "raw": round(float(raw), 6),
                    "profile_correlation": round(float(corr), 6),
                    "pairing_normalized": round(float(normalized), 6) if np.isfinite(normalized) else "",
                    "perm_p": round(float(perm["p_value"]), 6),
                    "bootstrap_lower": round(float(ci_lower), 6),
                    "bootstrap_upper": round(float(ci_upper), 6),
                }
            )
    return rows


def repeated(
    *, n: int = 60, repetitions: int = 300, n_perm: int = 199, seed: int = 20260804
) -> list[dict[str, float | int | str]]:
    accum = {
        (scenario, method): {"reject": 0, "corr": [], "raw": [], "p": []}
        for scenario in SCENARIOS
        for method in METHODS
    }
    for rep in range(repetitions):
        for scenario_offset, scenario in enumerate(SCENARIOS):
            x, y = make_scenario(scenario, n, seed=seed + rep * 100 + scenario_offset)
            for method in METHODS:
                sx, sy = profiles(x, y, method)
                perm = permutation_test_profiles(
                    sx, sy, n_perm=n_perm, seed=seed + 1_000_000 + rep * 100 + scenario_offset
                )
                entry = accum[(scenario, method)]
                entry["reject"] += int(perm["p_value"] < 0.05)
                entry["corr"].append(float(np.corrcoef(sx, sy)[0, 1]))
                entry["raw"].append(float(perm["observed"]))
                entry["p"].append(float(perm["p_value"]))
    rows = []
    for scenario in SCENARIOS:
        for method in METHODS:
            entry = accum[(scenario, method)]
            rows.append(
                {
                    "scenario": scenario,
                    "method": method,
                    "n": n,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejection_rate": round(entry["reject"] / repetitions, 6),
                    "mean_profile_correlation": round(float(np.mean(entry["corr"])), 6),
                    "mean_raw": round(float(np.mean(entry["raw"])), 6),
                    "median_p_value": round(float(np.median(entry["p"])), 6),
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
    pilot_path = PROJECT_ROOT / "results" / "robust_initial_pilot_20260804.tsv"
    repeated_path = PROJECT_ROOT / "results" / "robust_initial_repeated_20260804.tsv"
    write_tsv(pilot_path, pilot())
    write_tsv(repeated_path, repeated())
    print(pilot_path)
    print(repeated_path)
