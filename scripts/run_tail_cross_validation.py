from pathlib import Path
import csv
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np

from cdelta import _wilson_interval, c_delta
from scripts.run_tail_factor_comparison import (
    fast_permutation_p_value,
    make_tail_scenario,
    p_value_summary,
    write_tsv,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def summarize_runs(
    *,
    rowspec: dict,
    p_values: list[float],
    corr_values: list[float],
    norm_values: list[float],
    overlaps: list[int],
    alpha: float,
    repetitions: int,
    n_perm: int,
) -> dict:
    reject_count = int(sum(p < alpha for p in p_values))
    lo, hi = _wilson_interval(reject_count, repetitions)
    return {
        **rowspec,
        "alpha": alpha,
        "repetitions": repetitions,
        "n_perm": n_perm,
        "reject_count": reject_count,
        "rejection_rate": round(reject_count / repetitions, 4),
        "wilson_low": round(float(lo), 4),
        "wilson_high": round(float(hi), 4),
        "mean_norm": round(float(np.mean(norm_values)), 4),
        "mean_corr": round(float(np.mean(corr_values)), 4),
        "mean_index_overlap": round(float(np.mean(overlaps)), 4),
        **p_value_summary(p_values),
    }


def run_repeated_setting(
    *,
    rowspec: dict,
    repetitions: int,
    n_perm: int,
    seed_base: int,
    alpha: float = 0.05,
) -> dict:
    p_values = []
    corr_values = []
    norm_values = []
    overlaps = []
    for rep in range(repetitions):
        seed = seed_base + rep
        x, y, overlap = make_tail_scenario(
            n=rowspec["n"],
            k=rowspec["k_extremes"],
            magnitude=rowspec["magnitude"],
            df_label=rowspec["df_label"],
            scenario=rowspec["scenario"],
            seed=seed,
        )
        result = c_delta(x, y, kind=rowspec["kind"])
        p_values.append(
            fast_permutation_p_value(
                result.dx,
                result.dy,
                result.raw,
                n_perm=n_perm,
                seed=seed + 90_000_000,
            )
        )
        corr_values.append(result.direction_correlation)
        norm_values.append(result.normalized_pairing)
        overlaps.append(overlap)

    return summarize_runs(
        rowspec=rowspec,
        p_values=p_values,
        corr_values=corr_values,
        norm_values=norm_values,
        overlaps=overlaps,
        alpha=alpha,
        repetitions=repetitions,
        n_perm=n_perm,
    )


def run_matched_tail_power_validation() -> list[dict]:
    rows = []
    df_labels = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    repetitions = 500
    n_perm = 399
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(df_labels):
            for mag_offset, magnitude in enumerate([4.0, 6.0, 8.0]):
                rowspec = {
                    "validation": "matched_tail_power",
                    "kind": kind,
                    "df_label": df_label,
                    "n": 80,
                    "k_extremes": 2,
                    "magnitude": magnitude,
                    "scenario": "matched",
                }
                rows.append(
                    run_repeated_setting(
                        rowspec=rowspec,
                        repetitions=repetitions,
                        n_perm=n_perm,
                        seed_base=(
                            20260720
                            + kind_offset * 10_000_000
                            + df_offset * 1_000_000
                            + mag_offset * 100_000
                        ),
                    )
                )
    return rows


def run_independent_null_cross_validation() -> list[dict]:
    rows = []
    df_labels = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    repetitions = 1000
    n_perm = 499
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(df_labels):
            rowspec = {
                "validation": "independent_null_tail_size",
                "kind": kind,
                "df_label": df_label,
                "n": 80,
                "k_extremes": 2,
                "magnitude": 8.0,
                "scenario": "independent_null",
            }
            rows.append(
                run_repeated_setting(
                    rowspec=rowspec,
                    repetitions=repetitions,
                    n_perm=n_perm,
                    seed_base=20260720 + kind_offset * 10_000_000 + df_offset * 100_000,
                )
            )
    return rows


def run_fixed_k_vs_fixed_proportion_validation() -> list[dict]:
    rows = []
    repetitions = 250
    n_perm = 299
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(["normal", "t3", "t2"]):
            for mag_offset, magnitude in enumerate([6.0, 8.0]):
                for n_offset, n in enumerate([40, 80, 160]):
                    for design_offset, design in enumerate(["fixed_k", "fixed_proportion"]):
                        k = 2 if design == "fixed_k" else max(1, round(0.05 * n))
                        rowspec = {
                            "validation": "fixed_k_vs_fixed_proportion",
                            "design": design,
                            "kind": kind,
                            "df_label": df_label,
                            "n": n,
                            "k_extremes": k,
                            "k_fraction": round(k / n, 4),
                            "magnitude": magnitude,
                            "scenario": "matched",
                        }
                        rows.append(
                            run_repeated_setting(
                                rowspec=rowspec,
                                repetitions=repetitions,
                                n_perm=n_perm,
                                seed_base=(
                                    20260720
                                    + kind_offset * 100_000_000
                                    + df_offset * 10_000_000
                                    + mag_offset * 1_000_000
                                    + n_offset * 100_000
                                    + design_offset * 10_000
                                ),
                            )
                        )
    return rows


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    matched_rows = run_matched_tail_power_validation()
    null_rows = run_independent_null_cross_validation()
    proportion_rows = run_fixed_k_vs_fixed_proportion_validation()
    write_tsv(RESULTS_DIR / "tail_power_cross_validation_20260719.tsv", matched_rows)
    write_tsv(RESULTS_DIR / "tail_null_cross_validation_20260719.tsv", null_rows)
    write_tsv(
        RESULTS_DIR / "fixed_k_vs_fixed_proportion_20260719.tsv",
        proportion_rows,
    )


if __name__ == "__main__":
    main()
