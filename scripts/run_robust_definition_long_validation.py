"""Higher-replication validation for robust-reference c_delta candidates."""

from __future__ import annotations

import csv
from pathlib import Path
import sys
import time

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.run_robust_cdelta_grid import make_scenario, wilson
from scripts.run_robust_definition_stage2 import METHODS


SCENARIOS = (
    "null_clean",
    "null_contam_p05",
    "null_contam_p10",
    "matched_p01_m8",
    "matched_p05_m8",
    "diffuse_aligned",
    "t2_matched",
    "bimodal_aligned",
    "unmatched_masking",
)


def _write_checkpoint(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def run(
    *,
    sample_sizes: tuple[int, ...] = (20, 40, 80, 160),
    repetitions: int = 24000,
    n_perm: int = 999,
    seed: int = 20260810,
    output: Path,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    started = time.monotonic()
    total_conditions = len(sample_sizes) * len(SCENARIOS)
    completed = 0

    for n in sample_sizes:
        for scenario in SCENARIOS:
            summary = {
                method: {"reject": 0, "raw": [], "corr": []}
                for method in METHODS
            }
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                permutation_indices = np.asarray(
                    [rng.permutation(n) for _ in range(n_perm)], dtype=int
                )
                for method, profile_fn in METHODS.items():
                    sx, sy = profile_fn(x), profile_fn(y)
                    denominator = float(sx.mean() * sy.mean())
                    observed = float(np.mean(sx * sy) / denominator)
                    statistics = (sy[permutation_indices] @ sx) / n / denominator
                    p_value = (int(np.sum(statistics >= observed)) + 1) / (
                        n_perm + 1
                    )
                    values = summary[method]
                    values["reject"] += int(p_value < 0.05)
                    values["raw"].append(observed)
                    values["corr"].append(float(np.corrcoef(sx, sy)[0, 1]))

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

            _write_checkpoint(output, rows)
            completed += 1
            elapsed = time.monotonic() - started
            estimated_total = elapsed * total_conditions / completed
            print(
                f"completed={completed}/{total_conditions} n={n} "
                f"scenario={scenario} elapsed_minutes={elapsed / 60:.2f} "
                f"estimated_total_minutes={estimated_total / 60:.2f}",
                flush=True,
            )
    return rows


if __name__ == "__main__":
    output_path = (
        PROJECT_ROOT
        / "results"
        / "robust_definition_highrep_validation_20260804.tsv"
    )
    run(output=output_path)
    print(output_path)
