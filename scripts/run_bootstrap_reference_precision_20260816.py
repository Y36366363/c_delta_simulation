"""Check Monte Carlo precision of the bootstrap reference-stability metric."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_diagnostic_scaling_20260816 import fit_huber_reference
from scripts.run_profile_regularity_comparison_20260816 import (
    generate_sign_link_profile_null,
)
from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
)


RESULTS_DIR = PROJECT_ROOT / "results"
BOOTSTRAP_PREFIXES = (39, 79, 199, 399)
SCENARIOS = ("radial_0p1", "radial_0p2", "independent_strong_skew")


def bootstrap_centres(
    values: np.ndarray, *, n_bootstrap: int, rng: np.random.Generator
) -> np.ndarray:
    n = values.size
    centres = np.empty(n_bootstrap)
    for index in range(n_bootstrap):
        centres[index] = fit_huber_reference(
            values[rng.integers(0, n, size=n)]
        )
    return centres


def prefix_spreads(
    x: np.ndarray, y: np.ndarray, *, rng: np.random.Generator
) -> dict[int, float]:
    centres_x = bootstrap_centres(x, n_bootstrap=max(BOOTSTRAP_PREFIXES), rng=rng)
    centres_y = bootstrap_centres(y, n_bootstrap=max(BOOTSTRAP_PREFIXES), rng=rng)
    iqr_x = float(np.quantile(x, 0.75) - np.quantile(x, 0.25))
    iqr_y = float(np.quantile(y, 0.75) - np.quantile(y, 0.25))
    outputs = {}
    for count in BOOTSTRAP_PREFIXES:
        spread_x = (
            np.quantile(centres_x[:count], 0.75)
            - np.quantile(centres_x[:count], 0.25)
        ) / iqr_x
        spread_y = (
            np.quantile(centres_y[:count], 0.75)
            - np.quantile(centres_y[:count], 0.25)
        ) / iqr_y
        outputs[count] = float(max(spread_x, spread_y))
    return outputs


def generate_scenario(
    rng: np.random.Generator, scenario: str, n: int
) -> tuple[np.ndarray, np.ndarray]:
    if scenario.startswith("radial_"):
        radial_log_sd = float(scenario.removeprefix("radial_").replace("p", "."))
        return generate_sign_link_profile_null(rng, n, radial_log_sd)
    return generate_stress_scenario(rng, scenario, n, 0.65)


def run_precision(
    *, repetitions: int, n: int, seed: int, phase: str, scenario: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    values = {count: [] for count in BOOTSTRAP_PREFIXES}
    for _ in range(repetitions):
        x, y = generate_scenario(rng, scenario, n)
        spreads = prefix_spreads(x, y, rng=rng)
        for count, spread in spreads.items():
            values[count].append(np.sqrt(n) * spread)
    reference = np.asarray(values[max(BOOTSTRAP_PREFIXES)])
    rows = []
    for count in BOOTSTRAP_PREFIXES:
        candidate = np.asarray(values[count])
        absolute_error = np.abs(candidate - reference)
        rows.append(
            {
                "phase": phase,
                "scenario": scenario,
                "n": n,
                "repetitions": repetitions,
                "n_bootstrap": count,
                "median_scaled_spread": float(np.median(candidate)),
                "correlation_with_b399": (
                    1.0
                    if count == max(BOOTSTRAP_PREFIXES)
                    else float(np.corrcoef(candidate, reference)[0, 1])
                ),
                "median_absolute_error_vs_b399": float(np.median(absolute_error)),
                "q90_absolute_error_vs_b399": float(np.quantile(absolute_error, 0.90)),
                "warning_agreement_at_2": float(
                    np.mean((candidate > 2.0) == (reference > 2.0))
                ),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "pilot"), default="smoke")
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--scenario", choices=SCENARIOS, default="radial_0p1")
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    if args.combine:
        paths = sorted(
            RESULTS_DIR.glob(
                f"bootstrap_reference_precision_{args.phase}_n*_20260816.tsv"
            )
        )
        combined: list[dict[str, object]] = []
        for path in paths:
            with path.open(newline="") as stream:
                combined.extend(csv.DictReader(stream, delimiter="\t"))
        if not combined:
            raise FileNotFoundError("no bootstrap-precision cell results found")
        combined.sort(
            key=lambda row: (
                int(row["n"]), str(row["scenario"]), int(row["n_bootstrap"])
            )
        )
        output = RESULTS_DIR / (
            f"bootstrap_reference_precision_{args.phase}_20260816.tsv"
        )
        write_tsv(output, combined)
        print(f"combined {len(combined)} rows in {output}")
        return
    repetitions = 12 if args.phase == "smoke" else 100
    rows = run_precision(
        repetitions=repetitions,
        n=args.n,
        seed=2026081700 + args.n + SCENARIOS.index(args.scenario),
        phase=args.phase,
        scenario=args.scenario,
    )
    output = RESULTS_DIR / (
        f"bootstrap_reference_precision_{args.phase}_n{args.n}_"
        f"{args.scenario}_20260816.tsv"
    )
    write_tsv(output, rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
