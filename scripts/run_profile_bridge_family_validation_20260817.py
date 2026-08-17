"""Validate profile diagnostics across bridge families with matched f(0)."""

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
from scripts.run_profile_bridge_calibration_20260817 import summarise_records
from scripts.run_profile_diagnostic_scaling_20260816 import pair_diagnostics
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)


RESULTS_DIR = PROJECT_ROOT / "results"
BRIDGE_FAMILIES = ("uniform", "exponential", "half_normal", "scaled_beta12")


def sample_unit_origin_density_radius(
    rng: np.random.Generator, size: int, family: str
) -> np.ndarray:
    """Sample a positive radius whose right density at zero equals one."""
    if family == "uniform":
        return rng.uniform(0.0, 1.0, size=size)
    if family == "exponential":
        return rng.exponential(1.0, size=size)
    if family == "half_normal":
        scale = np.sqrt(2.0 / np.pi)
        return np.abs(rng.normal(0.0, scale, size=size))
    if family == "scaled_beta12":
        return 2.0 * rng.beta(1.0, 2.0, size=size)
    raise ValueError(f"unknown bridge family: {family}")


def generate_family_bridge_profile_null(
    rng: np.random.Generator,
    n: int,
    *,
    radial_log_sd: float,
    bridge_probability: float,
    bridge_family: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate a true profile weak null with matched centre density."""
    if radial_log_sd <= 0.0:
        raise ValueError("radial_log_sd must be positive")
    if not 0.0 <= bridge_probability <= 1.0:
        raise ValueError("bridge_probability must be in [0, 1]")
    if bridge_family not in BRIDGE_FAMILIES:
        raise ValueError(f"bridge_family must be one of {BRIDGE_FAMILIES}")
    signs = rng.choice((-1.0, 1.0), size=n)

    def radius() -> np.ndarray:
        values = np.exp(radial_log_sd * rng.normal(size=n))
        bridge = rng.random(n) < bridge_probability
        values[bridge] = sample_unit_origin_density_radius(
            rng, int(np.sum(bridge)), bridge_family
        )
        return values

    return signs * radius(), signs * radius()


def run_family_cell(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    n_bootstrap: int,
    seed: int,
    phase: str,
    bridge_probability: float,
    bridge_family: str,
    radial_log_sd: float = 0.10,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    for _ in range(repetitions):
        x, y = generate_family_bridge_profile_null(
            rng,
            n,
            radial_log_sd=radial_log_sd,
            bridge_probability=bridge_probability,
            bridge_family=bridge_family,
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
    result = summarise_records(
        records,
        phase=phase,
        design="bridge_family",
        scenario=f"{bridge_family}_epsilon_{bridge_probability:g}",
        n=n,
        repetitions=repetitions,
        n_perm=n_perm,
        n_bootstrap=n_bootstrap,
    )
    result["bridge_family"] = bridge_family
    result["bridge_probability"] = bridge_probability
    result["origin_radius_density"] = 1.0
    result["marginal_origin_density"] = bridge_probability / 2.0
    result["n_epsilon_squared"] = n * bridge_probability**2
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase", choices=("smoke", "pilot", "confirmatory"), default="smoke"
    )
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--bridge-probability", type=float, default=0.10)
    parser.add_argument("--bridge-family", choices=BRIDGE_FAMILIES, default="uniform")
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    stem = "profile_bridge_family_validation"
    if args.combine:
        paths = sorted(
            RESULTS_DIR.glob(f"{stem}_{args.phase}_n*_cell_20260817.tsv")
        )
        rows: list[dict[str, object]] = []
        for path in paths:
            with path.open(newline="") as stream:
                rows.extend(csv.DictReader(stream, delimiter="\t"))
        if not rows:
            raise FileNotFoundError("no bridge-family cell results found")
        rows.sort(
            key=lambda row: (
                int(row["n"]),
                float(row["bridge_probability"]),
                str(row["bridge_family"]),
            )
        )
        output = RESULTS_DIR / f"{stem}_{args.phase}_20260817.tsv"
        write_tsv(output, rows)
        print(f"combined {len(rows)} rows in {output}")
        return
    if args.phase == "smoke":
        settings = dict(repetitions=10, n_perm=19, n_bootstrap=19)
    elif args.phase == "pilot":
        settings = dict(repetitions=150, n_perm=99, n_bootstrap=199)
    else:
        settings = dict(repetitions=500, n_perm=99, n_bootstrap=199)
    seed = (
        2026081750
        + args.n
        + int(round(10000 * args.bridge_probability))
        + 100000 * BRIDGE_FAMILIES.index(args.bridge_family)
    )
    row = run_family_cell(
        n=args.n,
        seed=seed,
        phase=args.phase,
        bridge_probability=args.bridge_probability,
        bridge_family=args.bridge_family,
        **settings,
    )
    probability_label = str(args.bridge_probability).replace(".", "p")
    output = RESULTS_DIR / (
        f"{stem}_{args.phase}_n{args.n}_{args.bridge_family}_"
        f"epsilon{probability_label}_cell_20260817.tsv"
    )
    write_tsv(output, [row])
    print(row)


if __name__ == "__main__":
    main()
