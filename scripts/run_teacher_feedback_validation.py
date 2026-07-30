from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
from scipy.stats import norm, t

from cdelta import (
    _wilson_interval,
    c_delta,
    c_delta_identity_from_divergences,
    permutation_statistics_from_divergences,
)
from scripts.run_tail_factor_comparison import background_sample, write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"
TAILS = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]


def scale_factor(df_label: str, design: str) -> float:
    if design == "common_scale_parameter" or df_label == "normal":
        return 1.0
    df = float(df_label[1:])
    if design == "common_mad":
        return float(norm.ppf(0.75) / t.ppf(0.75, df))
    if design == "common_variance":
        if df <= 2:
            raise ValueError("same-variance scaling requires df > 2")
        return float(np.sqrt((df - 2) / df))
    raise ValueError(f"unknown scale design: {design}")


def make_scaled_scenario(
    *,
    n: int,
    k: int,
    magnitude: float,
    df_label: str,
    scenario: str,
    design: str,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    factor = scale_factor(df_label, design)
    x = factor * background_sample(rng, n, df_label)
    y = factor * background_sample(rng, n, df_label)
    x_idx = np.arange(n - k, n)
    if scenario == "matched":
        y_idx = x_idx
    elif scenario == "independent_null":
        y_idx = np.sort(rng.choice(n, size=k, replace=False))
    else:
        raise ValueError(f"unknown scenario: {scenario}")
    x[x_idx] = magnitude
    y[y_idx] = magnitude
    return x, y


def summarize(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    median = float(np.median(arr))
    mad = float(np.median(np.abs(arr - median)))
    return {
        "mean": float(np.mean(arr)),
        "sd": float(np.std(arr, ddof=1)),
        "median": median,
        "mad": mad,
        "q05": float(np.quantile(arr, 0.05)),
        "q95": float(np.quantile(arr, 0.95)),
    }


def run_validation() -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    distribution_rows = []
    summary_rows = []
    identity_rows = []
    power_rows = []
    repetitions = 300
    n_perm = 299
    n = 80
    k = 2
    magnitude = 8.0

    designs = ["common_scale_parameter", "common_mad", "common_variance"]
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for design_offset, design in enumerate(designs):
            labels = [label for label in TAILS if not (
                design == "common_variance" and label == "t2"
            )]
            for tail_offset, df_label in enumerate(labels):
                matched_stats = []
                null_stats = []
                matched_corrs = []
                null_corrs = []
                permutation_q95s = []
                identity_errors = []
                p_value_mismatches = 0
                matched_p_values = []
                null_p_values = []
                for rep in range(repetitions):
                    seed = (
                        20260730
                        + kind_offset * 100_000_000
                        + design_offset * 10_000_000
                        + tail_offset * 100_000
                        + rep
                    )
                    row_values = {}
                    for scenario in ["matched", "independent_null"]:
                        x, y = make_scaled_scenario(
                            n=n,
                            k=k,
                            magnitude=magnitude,
                            df_label=df_label,
                            scenario=scenario,
                            design=design,
                            seed=seed + (0 if scenario == "matched" else 50_000),
                        )
                        result = c_delta(x, y, kind=kind)
                        identity = c_delta_identity_from_divergences(
                            result.dx, result.dy
                        )
                        perm_stats = permutation_statistics_from_divergences(
                            result.dx,
                            result.dy,
                            n_perm=n_perm,
                            seed=seed + (20_000 if scenario == "matched" else 70_000),
                        )
                        cv_factor = identity["cv_product"]
                        perm_corrs = (perm_stats - 1.0) / cv_factor
                        p_c = (np.sum(perm_stats >= result.raw) + 1) / (n_perm + 1)
                        p_r = (
                            np.sum(perm_corrs >= result.direction_correlation) + 1
                        ) / (n_perm + 1)
                        p_value_mismatches += int(p_c != p_r)
                        identity_errors.append(identity["absolute_error"])
                        row_values[f"{scenario}_c_delta"] = result.raw
                        row_values[f"{scenario}_correlation"] = (
                            result.direction_correlation
                        )
                        row_values[f"{scenario}_p_value"] = p_c
                        if scenario == "matched":
                            matched_stats.append(result.raw)
                            matched_corrs.append(result.direction_correlation)
                            matched_p_values.append(p_c)
                            permutation_q95s.append(
                                float(np.quantile(perm_stats, 0.95))
                            )
                        else:
                            null_stats.append(result.raw)
                            null_corrs.append(result.direction_correlation)
                            null_p_values.append(p_c)
                    distribution_rows.append(
                        {
                            "kind": kind,
                            "scale_design": design,
                            "df_label": df_label,
                            "n": n,
                            "k_extremes": k,
                            "magnitude": magnitude,
                            "repetition": rep,
                            **{key: round(value, 8) for key, value in row_values.items()},
                        }
                    )

                for statistic, matched, null in [
                    ("c_delta", matched_stats, null_stats),
                    ("divergence_correlation", matched_corrs, null_corrs),
                ]:
                    matched_summary = summarize(matched)
                    null_summary = summarize(null)
                    robust_separation = (
                        (matched_summary["median"] - null_summary["median"])
                        / null_summary["mad"]
                        if null_summary["mad"] > 0
                        else np.nan
                    )
                    classical_separation = (
                        (matched_summary["mean"] - null_summary["mean"])
                        / null_summary["sd"]
                        if null_summary["sd"] > 0
                        else np.nan
                    )
                    summary_rows.append(
                        {
                            "kind": kind,
                            "scale_design": design,
                            "df_label": df_label,
                            "statistic": statistic,
                            "n": n,
                            "k_extremes": k,
                            "magnitude": magnitude,
                            "repetitions": repetitions,
                            "matched_median": round(matched_summary["median"], 6),
                            "matched_mean": round(matched_summary["mean"], 6),
                            "null_median": round(null_summary["median"], 6),
                            "null_mad": round(null_summary["mad"], 6),
                            "null_mean": round(null_summary["mean"], 6),
                            "null_sd": round(null_summary["sd"], 6),
                            "null_q95": round(null_summary["q95"], 6),
                            "robust_separation": round(robust_separation, 4),
                            "classical_separation": round(classical_separation, 4),
                            "matched_median_minus_null_q95": round(
                                matched_summary["median"] - null_summary["q95"], 6
                            ),
                            "median_conditional_permutation_q95": (
                                round(float(np.median(permutation_q95s)), 6)
                                if statistic == "c_delta"
                                else "NA"
                            ),
                            "matched_median_minus_median_permutation_q95": (
                                round(
                                    matched_summary["median"]
                                    - float(np.median(permutation_q95s)),
                                    6,
                                )
                                if statistic == "c_delta"
                                else "NA"
                            ),
                        }
                    )
                for scenario, p_values in [
                    ("matched", matched_p_values),
                    ("independent_null", null_p_values),
                ]:
                    reject_count = int(np.sum(np.asarray(p_values) < 0.05))
                    low, high = _wilson_interval(reject_count, repetitions)
                    power_rows.append(
                        {
                            "kind": kind,
                            "scale_design": design,
                            "df_label": df_label,
                            "scenario": scenario,
                            "n": n,
                            "k_extremes": k,
                            "magnitude": magnitude,
                            "repetitions": repetitions,
                            "n_perm": n_perm,
                            "reject_count": reject_count,
                            "rejection_rate": round(reject_count / repetitions, 4),
                            "wilson_low": round(float(low), 4),
                            "wilson_high": round(float(high), 4),
                        }
                    )
                identity_rows.append(
                    {
                        "kind": kind,
                        "scale_design": design,
                        "df_label": df_label,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "maximum_identity_error": round(
                            float(np.max(identity_errors)), 14
                        ),
                        "p_value_mismatch_count": p_value_mismatches,
                    }
                )
    return distribution_rows, summary_rows, identity_rows, power_rows


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    distribution_rows, summary_rows, identity_rows, power_rows = run_validation()
    write_tsv(
        RESULTS_DIR / "teacher_feedback_statistic_distributions_20260730.tsv",
        distribution_rows,
    )
    write_tsv(
        RESULTS_DIR / "teacher_feedback_separation_summary_20260730.tsv",
        summary_rows,
    )
    write_tsv(
        RESULTS_DIR / "teacher_feedback_identity_checks_20260730.tsv",
        identity_rows,
    )
    write_tsv(
        RESULTS_DIR / "teacher_feedback_power_summary_20260730.tsv",
        power_rows,
    )


if __name__ == "__main__":
    main()
