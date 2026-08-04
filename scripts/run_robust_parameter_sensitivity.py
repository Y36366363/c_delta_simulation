"""Parameter sensitivity for the proposed robust-reference c_delta."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import center_salience_vector
from scripts.run_robust_cdelta_grid import make_scenario, profile_test, wilson


CONFIGS = {
    "huber_c1.0": lambda z: center_salience_vector(z, center="huber", huber_c=1.0),
    "huber_c1.345": lambda z: center_salience_vector(z, center="huber", huber_c=1.345),
    "huber_c2.0": lambda z: center_salience_vector(z, center="huber", huber_c=2.0),
    "huber_c3.0": lambda z: center_salience_vector(z, center="huber", huber_c=3.0),
    "huber_cap3": lambda z: center_salience_vector(z, center="huber", cap=3.0),
    "huber_cap4": lambda z: center_salience_vector(z, center="huber", cap=4.0),
    "huber_cap6": lambda z: center_salience_vector(z, center="huber", cap=6.0),
    "huber_cap8": lambda z: center_salience_vector(z, center="huber", cap=8.0),
    "huber_soft3": lambda z: center_salience_vector(
        z, center="huber", cap=3.0, soft_cap=True
    ),
    "huber_soft4": lambda z: center_salience_vector(
        z, center="huber", cap=4.0, soft_cap=True
    ),
    "huber_soft6": lambda z: center_salience_vector(
        z, center="huber", cap=6.0, soft_cap=True
    ),
    "huber_soft8": lambda z: center_salience_vector(
        z, center="huber", cap=8.0, soft_cap=True
    ),
    "trim5": lambda z: center_salience_vector(z, center="trimmed_mean", trim_fraction=0.05),
    "trim10": lambda z: center_salience_vector(z, center="trimmed_mean", trim_fraction=0.10),
    "trim20": lambda z: center_salience_vector(z, center="trimmed_mean", trim_fraction=0.20),
}


def run(
    *, n: int = 80, repetitions: int = 300, n_perm: int = 199, seed: int = 20260807
) -> list[dict[str, float | int | str]]:
    scenarios = [
        "null_clean",
        "null_contam_p05",
        "matched_p01_m8",
        "t2_matched",
        "bimodal_aligned",
        "unmatched_masking",
    ]
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios:
        summary = {name: {"reject": 0, "corr": []} for name in CONFIGS}
        for _ in range(repetitions):
            x, y = make_scenario(scenario, n, rng)
            for name, fn in CONFIGS.items():
                p_value, corr = profile_test(fn(x), fn(y), rng, n_perm)
                summary[name]["reject"] += int(p_value < 0.05)
                summary[name]["corr"].append(corr)
        for name, values in summary.items():
            reject = int(values["reject"])
            low, high = wilson(reject, repetitions)
            rows.append(
                {
                    "scenario": scenario,
                    "method": name,
                    "n": n,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejections": reject,
                    "rejection_rate": reject / repetitions,
                    "wilson_low": low,
                    "wilson_high": high,
                    "mean_profile_correlation": float(np.mean(values["corr"])),
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
    output = PROJECT_ROOT / "results" / "robust_parameter_sensitivity_20260804.tsv"
    write_tsv(output, run())
    print(output)
