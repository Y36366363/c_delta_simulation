"""Training/evaluation split pilot for pre-calibrating a robust-score cap."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import make_scenario, wilson


CAPS = (3.0, 4.0, 5.0, 6.0, 8.0)
SCENARIOS = (
    "null_clean",
    "null_contam_p10",
    "matched_p01_m8",
    "t2_matched",
    "unmatched_masking",
)


def _methods(z: np.ndarray) -> dict[str, np.ndarray]:
    profiles = {"huber_uncapped": huber_reference_profile(z)}
    profiles.update(
        {f"huber_cap{cap:g}": huber_reference_profile(z, cap=cap) for cap in CAPS}
    )
    return profiles


def run_grid(
    *,
    sample_sizes: tuple[int, ...],
    repetitions: int,
    n_perm: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for scenario in SCENARIOS:
            summary = {
                method: {"reject": 0, "corr": []}
                for method in ("huber_uncapped", *(f"huber_cap{c:g}" for c in CAPS))
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(_methods(x), _methods(y), indices)
                for method, (p_value, _, correlation) in outcomes.items():
                    summary[method]["reject"] += int(p_value < 0.05)
                    summary[method]["corr"].append(correlation)
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
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                        "mean_profile_correlation": float(np.mean(values["corr"])),
                    }
                )
    return rows


def select_cap(training: list[dict[str, object]]) -> tuple[float, list[dict[str, object]]]:
    lookup = {
        (int(row["n"]), str(row["scenario"]), str(row["method"])): float(
            row["rejection_rate"]
        )
        for row in training
    }
    sample_sizes = sorted({int(row["n"]) for row in training})
    diagnostics: list[dict[str, object]] = []
    for cap in CAPS:
        method = f"huber_cap{cap:g}"
        null_max = max(
            lookup[(n, scenario, method)]
            for n in sample_sizes
            for scenario in ("null_clean", "null_contam_p10")
        )
        sparse_retentions = [
            lookup[(n, "matched_p01_m8", method)]
            / max(lookup[(n, "matched_p01_m8", "huber_uncapped")], 1e-12)
            for n in sample_sizes
        ]
        masking_mean = float(
            np.mean([lookup[(n, "unmatched_masking", method)] for n in sample_sizes])
        )
        t2_mean = float(np.mean([lookup[(n, "t2_matched", method)] for n in sample_sizes]))
        feasible = null_max <= 0.065 and min(sparse_retentions) >= 0.95
        diagnostics.append(
            {
                "cap": cap,
                "null_max": null_max,
                "minimum_sparse_power_retention": min(sparse_retentions),
                "mean_t2_power": t2_mean,
                "mean_masking_power": masking_mean,
                "feasible": int(feasible),
            }
        )
    feasible_rows = [row for row in diagnostics if row["feasible"]]
    if not feasible_rows:
        raise RuntimeError("no cap satisfies the pre-specified training constraints")
    selected = max(feasible_rows, key=lambda row: float(row["mean_masking_power"]))
    for row in diagnostics:
        row["selected"] = int(row is selected)
    return float(selected["cap"]), diagnostics


if __name__ == "__main__":
    training = run_grid(
        sample_sizes=(40, 80), repetitions=1500, n_perm=499, seed=20260811
    )
    selected_cap, diagnostics = select_cap(training)
    evaluation = run_grid(
        sample_sizes=(20, 40, 80, 160),
        repetitions=5000,
        n_perm=999,
        seed=20260812,
    )
    evaluation = [
        row
        for row in evaluation
        if row["method"] in {"huber_uncapped", f"huber_cap{selected_cap:g}"}
    ]
    write_tsv(
        PROJECT_ROOT / "results" / "cap_precalibration_training_20260804.tsv",
        training,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_precalibration_selection_20260804.tsv",
        diagnostics,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_precalibration_evaluation_20260804.tsv",
        evaluation,
    )
    print(f"selected_cap={selected_cap:g}")
