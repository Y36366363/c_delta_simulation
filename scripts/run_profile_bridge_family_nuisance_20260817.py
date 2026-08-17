"""Audit Huber-location and MAD-scale instability across bridge families."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np
from scipy.stats import spearmanr


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.robust_extension_utils import write_tsv
from scripts.run_profile_bridge_family_validation_20260817 import (
    BRIDGE_FAMILIES,
    generate_family_bridge_profile_null,
)
from scripts.run_profile_diagnostic_scaling_20260816 import fit_huber_reference
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_studentized_permutation_weak_null_20260814 import (
    profile_studentized_permutation_test,
    random_indices,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def fixed_mad_scale(values: np.ndarray) -> float:
    median = float(np.median(values))
    return 1.4826 * float(np.median(np.abs(values - median)))


def margin_joint_bootstrap_instability(
    values: np.ndarray, *, n_bootstrap: int, rng: np.random.Generator
) -> tuple[float, float, float]:
    """Return scaled location spread, scaled log-MAD spread, and scale/IQR."""
    n = values.size
    iqr = float(np.quantile(values, 0.75) - np.quantile(values, 0.25))
    full_scale = fixed_mad_scale(values)
    locations = np.empty(n_bootstrap)
    log_scales = np.empty(n_bootstrap)
    for index in range(n_bootstrap):
        sample = values[rng.integers(0, n, size=n)]
        locations[index] = fit_huber_reference(sample)
        scale = fixed_mad_scale(sample)
        log_scales[index] = np.log(max(scale, np.finfo(float).tiny))
    root_n = np.sqrt(n)
    location_spread = root_n * (
        np.quantile(locations, 0.75) - np.quantile(locations, 0.25)
    ) / iqr
    scale_spread = root_n * (
        np.quantile(log_scales, 0.75) - np.quantile(log_scales, 0.25)
    )
    return float(location_spread), float(scale_spread), float(full_scale / iqr)


def run_family_nuisance(
    *,
    repetitions: int,
    n: int,
    n_perm: int,
    n_bootstrap: int,
    seed: int,
    bridge_probability: float,
    bridge_family: str,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    records = []
    for _ in range(repetitions):
        x, y = generate_family_bridge_profile_null(
            rng,
            n,
            radial_log_sd=0.10,
            bridge_probability=bridge_probability,
            bridge_family=bridge_family,
        )
        test = profile_studentized_permutation_test(
            x, y, random_indices(rng, n, n_perm)
        )
        location_x, scale_x, ratio_x = margin_joint_bootstrap_instability(
            x, n_bootstrap=n_bootstrap, rng=rng
        )
        location_y, scale_y, ratio_y = margin_joint_bootstrap_instability(
            y, n_bootstrap=n_bootstrap, rng=rng
        )
        records.append(
            (
                float(test["p_value"]) <= 0.05,
                max(location_x, location_y),
                max(scale_x, scale_y),
                min(ratio_x, ratio_y),
            )
        )
    values = np.asarray(records)
    rejected = values[:, 0].astype(bool)
    count = int(np.sum(rejected))
    low, high = wilson(count, repetitions)
    row: dict[str, float | int | str] = {
        "bridge_family": bridge_family,
        "n": n,
        "bridge_probability": bridge_probability,
        "repetitions": repetitions,
        "n_perm": n_perm,
        "n_bootstrap": n_bootstrap,
        "studentized_rejection": count / repetitions,
        "studentized_wilson_low": low,
        "studentized_wilson_high": high,
    }
    for name, data, orientation in (
        ("location_spread", values[:, 1], 1.0),
        ("log_mad_scale_spread", values[:, 2], 1.0),
        ("minimum_scale_iqr_ratio", values[:, 3], -1.0),
    ):
        row[f"median_{name}"] = float(np.median(data))
        row[f"q10_{name}"] = float(np.quantile(data, 0.10))
        row[f"q90_{name}"] = float(np.quantile(data, 0.90))
        if np.unique(data).size < 2 or np.unique(rejected).size < 2:
            correlation, p_value = float("nan"), float("nan")
        else:
            correlation, p_value = spearmanr(orientation * data, rejected)
        row[f"rejection_spearman_{name}"] = float(correlation)
        row[f"rejection_spearman_p_{name}"] = float(p_value)
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("smoke", "confirmatory"), default="smoke")
    parser.add_argument("--bridge-family", choices=BRIDGE_FAMILIES, default="uniform")
    parser.add_argument("--combine", action="store_true")
    args = parser.parse_args()
    if args.combine:
        rows = []
        for family in BRIDGE_FAMILIES:
            path = RESULTS_DIR / (
                f"profile_bridge_family_nuisance_{args.phase}_{family}_20260817.tsv"
            )
            with path.open(newline="") as stream:
                rows.extend(csv.DictReader(stream, delimiter="\t"))
        output = RESULTS_DIR / (
            f"profile_bridge_family_nuisance_{args.phase}_20260817.tsv"
        )
        write_tsv(output, rows)
        print(f"combined {len(rows)} rows in {output}")
        return
    if args.phase == "smoke":
        settings = dict(repetitions=8, n=80, n_perm=19, n_bootstrap=19)
    else:
        settings = dict(repetitions=300, n=320, n_perm=99, n_bootstrap=199)
    row = run_family_nuisance(
        seed=2026081780 + 10000 * BRIDGE_FAMILIES.index(args.bridge_family),
        bridge_probability=0.05,
        bridge_family=args.bridge_family,
        **settings,
    )
    output = RESULTS_DIR / (
        f"profile_bridge_family_nuisance_{args.phase}_{args.bridge_family}_"
        "20260817.tsv"
    )
    write_tsv(output, [row])
    print(row)


if __name__ == "__main__":
    main()
