"""Compare profile-regularity diagnostics across sample sizes.

This is a diagnostic study only: it does not alter the primary statistic or
turn any empirical threshold into a formal testing rule.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import _gaussian_kde_density
from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_regularity_comparison_20260816 import (
    GATE_CV_SCENARIOS,
    generate_sign_link_profile_null,
    largest_interior_spacing_ratio,
)
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_stress_20260814 import (
    generate_stress_scenario,
)
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)


RESULTS_DIR = PROJECT_ROOT / "results"
SAMPLE_SIZES = (40, 80, 160, 320)
RADIAL_LOG_SDS = (0.10, 0.20, 0.40, 0.80)


def fit_huber_reference(
    values: np.ndarray, *, huber_c: float = 1.345
) -> float:
    """Fit the fixed-MAD Huber location used by the profile definition."""
    values = np.asarray(values, dtype=float)
    median = float(np.median(values))
    scale = 1.4826 * float(np.median(np.abs(values - median)))
    if scale == 0.0:
        scale = float(np.mean(np.abs(values - median)))
    if scale == 0.0:
        scale = float(np.std(values))
    if scale == 0.0:
        return median
    location = median
    for _ in range(100):
        residual = (values - location) / scale
        weights = np.minimum(1.0, huber_c / np.maximum(np.abs(residual), 1e-15))
        updated = float(np.sum(weights * values) / np.sum(weights))
        if abs(updated - location) < 1e-10 * max(1.0, scale):
            return updated
        location = updated
    return location


def centre_density_diagnostics(values: np.ndarray) -> tuple[float, float]:
    """Return scale-free KDE density at the median and in its central valley.

    The valley quantity is the smallest density on a grid between the 40th
    and 60th percentiles.  It is included because an even-sample median can
    land close to either mode rather than in the low-density interval.
    """
    values = np.asarray(values, dtype=float)
    q25, q40, q60, q75 = np.quantile(values, [0.25, 0.40, 0.60, 0.75])
    iqr = float(q75 - q25)
    if iqr <= 0.0:
        return float("inf"), float("inf")
    median_density = _gaussian_kde_density(values, float(np.median(values))) * iqr
    grid = np.linspace(q40, q60, 21)
    valley_density = min(_gaussian_kde_density(values, float(z)) for z in grid) * iqr
    return float(median_density), float(valley_density)


def bootstrap_reference_diagnostics(
    values: np.ndarray,
    *,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Return relative bootstrap spread and large-shift frequency of T_H."""
    values = np.asarray(values, dtype=float)
    n = values.size
    q25, q75 = np.quantile(values, [0.25, 0.75])
    iqr = float(q75 - q25)
    if iqr <= 0.0:
        return float("inf"), 1.0
    fitted = fit_huber_reference(values)
    centres = np.empty(n_bootstrap)
    for bootstrap_index in range(n_bootstrap):
        sample = values[rng.integers(0, n, size=n)]
        centres[bootstrap_index] = fit_huber_reference(sample)
    spread = float(
        (np.quantile(centres, 0.75) - np.quantile(centres, 0.25)) / iqr
    )
    large_shift = float(np.mean(np.abs(centres - fitted) > 0.25 * iqr))
    return spread, large_shift


def pair_diagnostics(
    x: np.ndarray,
    y: np.ndarray,
    *,
    n_bootstrap: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Compute worst-margin diagnostics, oriented so larger means less regular."""
    median_dx, valley_dx = centre_density_diagnostics(x)
    median_dy, valley_dy = centre_density_diagnostics(y)
    spread_x, shift_x = bootstrap_reference_diagnostics(
        x, n_bootstrap=n_bootstrap, rng=rng
    )
    spread_y, shift_y = bootstrap_reference_diagnostics(
        y, n_bootstrap=n_bootstrap, rng=rng
    )
    return {
        "spacing_risk": max(
            largest_interior_spacing_ratio(x), largest_interior_spacing_ratio(y)
        ),
        "median_density_iqr": min(median_dx, median_dy),
        "valley_density_iqr": min(valley_dx, valley_dy),
        "bootstrap_reference_spread": max(spread_x, spread_y),
        "bootstrap_large_shift_rate": max(shift_x, shift_y),
    }


def binary_auc(risk: np.ndarray, event: np.ndarray) -> float:
    """AUC probability that an event observation has the larger risk score."""
    risk = np.asarray(risk, dtype=float)
    event = np.asarray(event, dtype=bool)
    positive = risk[event]
    negative = risk[~event]
    if positive.size == 0 or negative.size == 0:
        return float("nan")
    comparisons = positive[:, None] - negative[None, :]
    return float(np.mean(comparisons > 0.0) + 0.5 * np.mean(comparisons == 0.0))


def _summarise_records(
    records: list[dict[str, float]],
    *,
    phase: str,
    design: str,
    label: str,
    n: int,
    repetitions: int,
    n_perm: int,
    n_bootstrap: int,
) -> dict[str, float | int | str]:
    rejected = np.asarray([row["p_value"] <= 0.05 for row in records])
    rejection_count = int(np.sum(rejected))
    interval = wilson(rejection_count, repetitions)
    result: dict[str, float | int | str] = {
        "phase": phase,
        "design": design,
        "scenario": label,
        "n": n,
        "repetitions": repetitions,
        "n_perm": n_perm,
        "n_bootstrap": n_bootstrap,
        "studentized_rejection": rejection_count / repetitions,
        "studentized_wilson_low": interval[0],
        "studentized_wilson_high": interval[1],
        "mean_profile_effect": float(np.mean([row["estimate"] for row in records])),
    }
    diagnostic_orientations = {
        "spacing_risk": 1.0,
        "median_density_iqr": -1.0,
        "valley_density_iqr": -1.0,
        "bootstrap_reference_spread": 1.0,
        "bootstrap_large_shift_rate": 1.0,
    }
    for name, orientation in diagnostic_orientations.items():
        values = np.asarray([row[name] for row in records])
        result[f"median_{name}"] = float(np.median(values))
        result[f"q10_{name}"] = float(np.quantile(values, 0.10))
        result[f"q90_{name}"] = float(np.quantile(values, 0.90))
        result[f"rejection_auc_{name}"] = binary_auc(orientation * values, rejected)
    root_n = np.sqrt(n)
    for prefix in ("median", "q10", "q90"):
        result[f"{prefix}_sqrt_n_bootstrap_reference_spread"] = float(
            root_n * result[f"{prefix}_bootstrap_reference_spread"]
        )
    return result


def run_path_cell(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    n_bootstrap: int,
    seed: int,
    phase: str,
    radial_log_sd: float,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    for _ in range(repetitions):
        x, y = generate_sign_link_profile_null(rng, n, radial_log_sd)
        result = profile_studentized_permutation_test(
            x, y, random_indices(rng, n, n_perm)
        )
        record = {
            "estimate": float(result["estimate"]),
            "p_value": float(result["p_value"]),
            **pair_diagnostics(x, y, n_bootstrap=n_bootstrap, rng=rng),
        }
        records.append(record)
    return _summarise_records(
        records,
        phase=phase,
        design="radial_path",
        label=f"radial_log_sd_{radial_log_sd:g}",
        n=n,
        repetitions=repetitions,
        n_perm=n_perm,
        n_bootstrap=n_bootstrap,
    )


def run_external_cell(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    n_bootstrap: int,
    seed: int,
    phase: str,
    scenario: str,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    for _ in range(repetitions):
        if scenario == "independent_affine_near_constant":
            x = 3.0 + 1e-12 * rng.normal(size=n)
            y = -2.0 + 1e-12 * rng.normal(size=n)
        else:
            x, y = generate_stress_scenario(rng, scenario, n, 0.65)
        result = profile_studentized_permutation_test(
            x, y, random_indices(rng, n, n_perm)
        )
        records.append(
            {
                "estimate": float(result["estimate"]),
                "p_value": float(result["p_value"]),
                **pair_diagnostics(x, y, n_bootstrap=n_bootstrap, rng=rng),
            }
        )
    return _summarise_records(
        records,
        phase=phase,
        design="external_cv",
        label=scenario,
        n=n,
        repetitions=repetitions,
        n_perm=n_perm,
        n_bootstrap=n_bootstrap,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "pilot"), default="smoke")
    parser.add_argument("--design", choices=("path", "external"), default="path")
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--radial-log-sd", type=float, default=0.20)
    parser.add_argument(
        "--scenario", choices=GATE_CV_SCENARIOS, default="independent_t5"
    )
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    if args.combine:
        stem = (
            "profile_diagnostic_scaling_path"
            if args.design == "path"
            else "profile_diagnostic_external_cv"
        )
        paths = sorted(RESULTS_DIR.glob(f"{stem}_{args.phase}_n*_20260816.tsv"))
        rows: list[dict[str, object]] = []
        for path in paths:
            with path.open(newline="") as stream:
                rows.extend(csv.DictReader(stream, delimiter="\t"))
        if not rows:
            raise FileNotFoundError(f"no cell results found for {stem}")
        for row in rows:
            root_n = np.sqrt(int(row["n"]))
            for prefix in ("median", "q10", "q90"):
                source = f"{prefix}_bootstrap_reference_spread"
                row[f"{prefix}_sqrt_n_bootstrap_reference_spread"] = (
                    root_n * float(row[source])
                )
        rows.sort(key=lambda row: (int(row["n"]), str(row["scenario"])))
        output = RESULTS_DIR / f"{stem}_{args.phase}_20260816.tsv"
        write_tsv(output, rows)
        print(f"combined {len(rows)} rows in {output}")
        return
    if args.phase == "smoke":
        settings = dict(repetitions=12, n_perm=19, n_bootstrap=19)
    else:
        settings = dict(repetitions=150, n_perm=99, n_bootstrap=79)
    seed = 2026081620 + args.n + int(round(100 * args.radial_log_sd))
    if args.design == "path":
        row = run_path_cell(
            n=args.n,
            seed=seed,
            phase=args.phase,
            radial_log_sd=args.radial_log_sd,
            **settings,
        )
        label = f"n{args.n}_sd{args.radial_log_sd:g}".replace(".", "p")
        stem = "profile_diagnostic_scaling_path"
    else:
        row = run_external_cell(
            n=args.n,
            seed=seed + 1000,
            phase=args.phase,
            scenario=args.scenario,
            **settings,
        )
        label = f"n{args.n}_{args.scenario}"
        stem = "profile_diagnostic_external_cv"
    output = RESULTS_DIR / f"{stem}_{args.phase}_{label}_20260816.tsv"
    write_tsv(output, [row])
    print(row)


if __name__ == "__main__":
    main()
