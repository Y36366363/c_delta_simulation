"""Cross-validate fixed-MAD/IQR identification ratios without resampling."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_bridge_family_nuisance_20260817 import fixed_mad_scale
from scripts.run_profile_bridge_family_validation_20260817 import (
    generate_family_bridge_profile_null,
)
from scripts.run_profile_regularity_comparison_20260816 import GATE_CV_SCENARIOS
from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
)


RESULTS_DIR = PROJECT_ROOT / "results"
THRESHOLDS = (0.25, 0.40, 0.50, 0.60)


def margin_scale_iqr_ratio(values: np.ndarray) -> float:
    iqr = float(np.quantile(values, 0.75) - np.quantile(values, 0.25))
    return fixed_mad_scale(values) / iqr


def run_ratio_cell(
    *,
    repetitions: int,
    n: int,
    seed: int,
    design: str,
    scenario: str,
    radial_log_sd: float = 0.10,
    bridge_probability: float = 0.0,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    ratios = np.empty(repetitions)
    for index in range(repetitions):
        if design == "external":
            if scenario == "independent_affine_near_constant":
                x = 3.0 + 1e-12 * rng.normal(size=n)
                y = -2.0 + 1e-12 * rng.normal(size=n)
            else:
                x, y = generate_stress_scenario(rng, scenario, n, 0.65)
        else:
            x, y = generate_family_bridge_profile_null(
                rng,
                n,
                radial_log_sd=radial_log_sd,
                bridge_probability=bridge_probability,
                bridge_family="uniform",
            )
        ratios[index] = min(
            margin_scale_iqr_ratio(x), margin_scale_iqr_ratio(y)
        )
    row: dict[str, float | int | str] = {
        "design": design,
        "scenario": scenario,
        "n": n,
        "repetitions": repetitions,
        "median_minimum_mad_iqr_ratio": float(np.median(ratios)),
        "q01_minimum_mad_iqr_ratio": float(np.quantile(ratios, 0.01)),
        "q05_minimum_mad_iqr_ratio": float(np.quantile(ratios, 0.05)),
        "q10_minimum_mad_iqr_ratio": float(np.quantile(ratios, 0.10)),
    }
    for threshold in THRESHOLDS:
        suffix = str(threshold).replace(".", "p")
        row[f"ratio_below_{suffix}_rate"] = float(np.mean(ratios < threshold))
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", choices=("external", "sigma", "bridge"), default="external")
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--scenario", choices=GATE_CV_SCENARIOS, default="independent_t5")
    parser.add_argument("--radial-log-sd", type=float, default=0.10)
    parser.add_argument("--bridge-probability", type=float, default=0.05)
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    if args.combine:
        rows = []
        for path in sorted(
            RESULTS_DIR.glob("mad_ratio_crossvalidation_*_n*_20260817.tsv")
        ):
            with path.open(newline="") as stream:
                rows.extend(csv.DictReader(stream, delimiter="\t"))
        rows.sort(key=lambda row: (str(row["design"]), int(row["n"]), str(row["scenario"])))
        output = RESULTS_DIR / "mad_ratio_crossvalidation_20260817.tsv"
        write_tsv(output, rows)
        print(f"combined {len(rows)} rows in {output}")
        return
    if args.design == "external":
        scenario = args.scenario
        label = args.scenario
    elif args.design == "sigma":
        scenario = f"sigma_{args.radial_log_sd:g}"
        label = scenario
    else:
        scenario = f"sigma_{args.radial_log_sd:g}_bridge_{args.bridge_probability:g}"
        label = scenario
    row = run_ratio_cell(
        repetitions=2000,
        n=args.n,
        seed=2026081790 + args.n + sum(ord(char) for char in label),
        design=args.design,
        scenario=scenario,
        radial_log_sd=args.radial_log_sd,
        bridge_probability=(
            args.bridge_probability if args.design == "bridge" else 0.0
        ),
    )
    output = RESULTS_DIR / (
        f"mad_ratio_crossvalidation_{args.design}_n{args.n}_"
        f"{label.replace('.', 'p')}_20260817.tsv"
    )
    write_tsv(output, [row])
    print(row)


if __name__ == "__main__":
    main()
