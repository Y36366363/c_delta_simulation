"""Independently calibrate profile warnings near a low-density centre."""

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
from scripts.run_profile_diagnostic_scaling_20260816 import pair_diagnostics
from scripts.run_profile_regularity_comparison_20260816 import GATE_CV_SCENARIOS
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
)
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)


RESULTS_DIR = PROJECT_ROOT / "results"
SIGMA_GRID = (0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.25, 0.30)
BRIDGE_GRID = (0.00, 0.01, 0.025, 0.05, 0.10, 0.20)
BOOTSTRAP_WARNING = 2.0
SPACING_WARNING = 0.50
VALLEY_DENSITY_WARNING = 0.25


def generate_bridge_profile_null(
    rng: np.random.Generator,
    n: int,
    *,
    radial_log_sd: float,
    bridge_probability: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a true profile weak null with optional density at zero.

    The common sign creates dependence in the raw margins, while the two
    radii are independent.  With positive bridge probability, a Uniform(0,1)
    component gives each symmetric margin positive one-sided density at zero.
    """
    if radial_log_sd <= 0.0:
        raise ValueError("radial_log_sd must be positive")
    if not 0.0 <= bridge_probability <= 1.0:
        raise ValueError("bridge_probability must be in [0, 1]")
    signs = rng.choice((-1.0, 1.0), size=n)

    def radius() -> np.ndarray:
        values = np.exp(radial_log_sd * rng.normal(size=n))
        bridge = rng.random(n) < bridge_probability
        values[bridge] = rng.uniform(0.0, 1.0, size=int(np.sum(bridge)))
        return values

    return signs * radius(), signs * radius()


def _safe_rate(mask: np.ndarray, event: np.ndarray) -> float:
    return float(np.mean(event[mask])) if np.any(mask) else float("nan")


def summarise_records(
    records: list[dict[str, float]],
    *,
    phase: str,
    design: str,
    scenario: str,
    n: int,
    repetitions: int,
    n_perm: int,
    n_bootstrap: int,
) -> dict[str, float | int | str]:
    rejected = np.asarray([row["p_value"] <= 0.05 for row in records])
    spacing = np.asarray([row["spacing_risk"] for row in records])
    valley = np.asarray([row["valley_density_iqr"] for row in records])
    bootstrap = np.sqrt(n) * np.asarray(
        [row["bootstrap_reference_spread"] for row in records]
    )
    spacing_warning = spacing > SPACING_WARNING
    valley_warning = valley < VALLEY_DENSITY_WARNING
    bootstrap_warning = bootstrap > BOOTSTRAP_WARNING
    structural_warning = spacing_warning | valley_warning
    rejection_count = int(np.sum(rejected))
    low, high = wilson(rejection_count, repetitions)
    result: dict[str, float | int | str] = {
        "phase": phase,
        "design": design,
        "scenario": scenario,
        "n": n,
        "repetitions": repetitions,
        "n_perm": n_perm,
        "n_bootstrap": n_bootstrap,
        "studentized_rejection": rejection_count / repetitions,
        "studentized_wilson_low": low,
        "studentized_wilson_high": high,
        "mean_profile_effect": float(np.mean([row["estimate"] for row in records])),
    }
    for name, values in (
        ("spacing_risk", spacing),
        ("valley_density_iqr", valley),
        ("sqrt_n_bootstrap_spread", bootstrap),
    ):
        result[f"median_{name}"] = float(np.median(values))
        result[f"q10_{name}"] = float(np.quantile(values, 0.10))
        result[f"q90_{name}"] = float(np.quantile(values, 0.90))
    for name, warning in (
        ("spacing", spacing_warning),
        ("valley_density", valley_warning),
        ("structural", structural_warning),
        ("bootstrap", bootstrap_warning),
    ):
        passed = ~warning
        result[f"{name}_warning_rate"] = float(np.mean(warning))
        result[f"{name}_rejection_among_pass"] = _safe_rate(passed, rejected)
        result[f"{name}_rejection_retained_per_all"] = float(
            np.mean(passed & rejected)
        )
        result[f"{name}_warning_among_rejections"] = _safe_rate(rejected, warning)
    return result


def run_cell(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    n_bootstrap: int,
    seed: int,
    phase: str,
    design: str,
    radial_log_sd: float = 0.10,
    bridge_probability: float = 0.0,
    external_scenario: str = "independent_t5",
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    for _ in range(repetitions):
        if design == "external":
            if external_scenario == "independent_affine_near_constant":
                x = 3.0 + 1e-12 * rng.normal(size=n)
                y = -2.0 + 1e-12 * rng.normal(size=n)
            else:
                x, y = generate_stress_scenario(rng, external_scenario, n, 0.65)
            scenario = external_scenario
        else:
            x, y = generate_bridge_profile_null(
                rng,
                n,
                radial_log_sd=radial_log_sd,
                bridge_probability=bridge_probability,
            )
            scenario = (
                f"sigma_{radial_log_sd:g}"
                if design == "sigma"
                else f"sigma_{radial_log_sd:g}_bridge_{bridge_probability:g}"
            )
        test = profile_studentized_permutation_test(
            x, y, random_indices(rng, n, n_perm)
        )
        records.append(
            {
                "estimate": float(test["estimate"]),
                "p_value": float(test["p_value"]),
                **pair_diagnostics(x, y, n_bootstrap=n_bootstrap, rng=rng),
            }
        )
    return summarise_records(
        records,
        phase=phase,
        design=design,
        scenario=scenario,
        n=n,
        repetitions=repetitions,
        n_perm=n_perm,
        n_bootstrap=n_bootstrap,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "pilot"), default="smoke")
    parser.add_argument(
        "--design", choices=("sigma", "bridge", "external"), default="sigma"
    )
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--radial-log-sd", type=float, default=0.10)
    parser.add_argument("--bridge-probability", type=float, default=0.0)
    parser.add_argument(
        "--scenario", choices=GATE_CV_SCENARIOS, default="independent_t5"
    )
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    stem = f"profile_{args.design}_calibration"
    if args.combine:
        paths = sorted(
            RESULTS_DIR.glob(f"{stem}_{args.phase}_n*_cell_20260817.tsv")
        )
        rows: list[dict[str, object]] = []
        for path in paths:
            with path.open(newline="") as stream:
                rows.extend(csv.DictReader(stream, delimiter="\t"))
        if not rows:
            raise FileNotFoundError(f"no cell results found for {stem}")
        rows.sort(key=lambda row: (int(row["n"]), str(row["scenario"])))
        output = RESULTS_DIR / f"{stem}_{args.phase}_20260817.tsv"
        write_tsv(output, rows)
        print(f"combined {len(rows)} rows in {output}")
        return

    if args.phase == "smoke":
        settings = dict(repetitions=10, n_perm=19, n_bootstrap=19)
    else:
        settings = dict(repetitions=150, n_perm=99, n_bootstrap=199)
    seed = (
        2026081700
        + 1000 * ("sigma", "bridge", "external").index(args.design)
        + args.n
        + int(round(1000 * args.radial_log_sd))
        + int(round(10000 * args.bridge_probability))
        + GATE_CV_SCENARIOS.index(args.scenario)
    )
    row = run_cell(
        n=args.n,
        seed=seed,
        phase=args.phase,
        design=args.design,
        radial_log_sd=args.radial_log_sd,
        bridge_probability=args.bridge_probability,
        external_scenario=args.scenario,
        **settings,
    )
    if args.design == "sigma":
        label = f"sigma{args.radial_log_sd:g}".replace(".", "p")
    elif args.design == "bridge":
        label = (
            f"sigma{args.radial_log_sd:g}_bridge{args.bridge_probability:g}"
            .replace(".", "p")
        )
    else:
        label = args.scenario
    output = RESULTS_DIR / (
        f"{stem}_{args.phase}_n{args.n}_{label}_cell_20260817.tsv"
    )
    write_tsv(output, [row])
    print(row)


if __name__ == "__main__":
    main()
