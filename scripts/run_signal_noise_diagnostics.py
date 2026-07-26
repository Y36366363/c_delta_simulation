from pathlib import Path
import csv
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np

from cdelta import c_delta, divergence_vector
from scripts.run_tail_factor_comparison import (
    background_sample,
    make_tail_scenario,
    write_tsv,
)


RESULTS_DIR = PROJECT_ROOT / "results"


def mean_float(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def load_power_lookup() -> dict[tuple[str, str, float], dict[str, str]]:
    path = RESULTS_DIR / "tail_power_cross_validation_20260719.tsv"
    with path.open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    lookup = {}
    for row in rows:
        if row["n"] == "80" and row["k_extremes"] == "2":
            lookup[(row["kind"], row["df_label"], float(row["magnitude"]))] = row
    return lookup


def background_noise_summary(
    *,
    kind: str,
    df_label: str,
    n: int,
    repetitions: int,
    seed_base: int,
) -> dict[str, float]:
    cv_values = []
    q95_ratios = []
    max_ratios = []
    top2_ratios = []
    for rep in range(repetitions):
        rng = np.random.default_rng(seed_base + rep)
        x = background_sample(rng, n, df_label)
        dx = divergence_vector(x, kind=kind)
        mean_dx = float(dx.mean())
        cv_values.append(float(dx.std() / mean_dx))
        q95_ratios.append(float(np.quantile(dx, 0.95) / mean_dx))
        max_ratios.append(float(dx.max() / mean_dx))
        top2_ratios.append(float(np.mean(np.sort(dx)[-2:]) / mean_dx))

    return {
        "background_cv": mean_float(cv_values),
        "background_q95_to_mean": mean_float(q95_ratios),
        "background_top2_to_mean": mean_float(top2_ratios),
        "background_max_to_mean": mean_float(max_ratios),
    }


def matched_signal_summary(
    *,
    kind: str,
    df_label: str,
    n: int,
    k: int,
    magnitude: float,
    repetitions: int,
    seed_base: int,
) -> dict[str, float]:
    extreme_prominence_values = []
    nonextreme_prominence_values = []
    corr_values = []
    norm_values = []
    for rep in range(repetitions):
        x, y, _ = make_tail_scenario(
            n=n,
            k=k,
            magnitude=magnitude,
            df_label=df_label,
            scenario="matched",
            seed=seed_base + rep,
        )
        result = c_delta(x, y, kind=kind)
        idx = np.arange(n - k, n)
        rest = np.arange(0, n - k)
        x_extreme = float(np.mean(result.dx[idx]) / np.mean(result.dx))
        y_extreme = float(np.mean(result.dy[idx]) / np.mean(result.dy))
        x_rest = float(np.mean(result.dx[rest]) / np.mean(result.dx))
        y_rest = float(np.mean(result.dy[rest]) / np.mean(result.dy))
        extreme_prominence_values.append((x_extreme + y_extreme) / 2)
        nonextreme_prominence_values.append((x_rest + y_rest) / 2)
        corr_values.append(result.direction_correlation)
        norm_values.append(result.normalized_pairing)

    return {
        "matched_extreme_to_mean": mean_float(extreme_prominence_values),
        "matched_nonextreme_to_mean": mean_float(nonextreme_prominence_values),
        "mean_corr": mean_float(corr_values),
        "mean_norm": mean_float(norm_values),
    }


def run_signal_noise_diagnostics() -> list[dict[str, float | str]]:
    rows = []
    power_lookup = load_power_lookup()
    df_labels = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    magnitudes = [4.0, 6.0, 8.0]
    n = 80
    k = 2
    background_repetitions = 1000
    matched_repetitions = 600

    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(df_labels):
            noise = background_noise_summary(
                kind=kind,
                df_label=df_label,
                n=n,
                repetitions=background_repetitions,
                seed_base=20260726 + kind_offset * 10_000_000 + df_offset * 100_000,
            )
            for mag_offset, magnitude in enumerate(magnitudes):
                signal = matched_signal_summary(
                    kind=kind,
                    df_label=df_label,
                    n=n,
                    k=k,
                    magnitude=magnitude,
                    repetitions=matched_repetitions,
                    seed_base=(
                        20260726
                        + kind_offset * 100_000_000
                        + df_offset * 1_000_000
                        + mag_offset * 100_000
                    ),
                )
                power = power_lookup[(kind, df_label, magnitude)]
                extreme_prominence = signal["matched_extreme_to_mean"]
                rows.append(
                    {
                        "kind": kind,
                        "df_label": df_label,
                        "n": n,
                        "k_extremes": k,
                        "magnitude": magnitude,
                        "background_repetitions": background_repetitions,
                        "matched_repetitions": matched_repetitions,
                        "rejection_rate": float(power["rejection_rate"]),
                        "wilson_low": float(power["wilson_low"]),
                        "wilson_high": float(power["wilson_high"]),
                        "mean_corr": round(signal["mean_corr"], 4),
                        "mean_norm": round(signal["mean_norm"], 4),
                        "matched_extreme_to_mean": round(extreme_prominence, 4),
                        "matched_nonextreme_to_mean": round(
                            signal["matched_nonextreme_to_mean"], 4
                        ),
                        "background_cv": round(noise["background_cv"], 4),
                        "background_q95_to_mean": round(
                            noise["background_q95_to_mean"], 4
                        ),
                        "background_top2_to_mean": round(
                            noise["background_top2_to_mean"], 4
                        ),
                        "background_max_to_mean": round(
                            noise["background_max_to_mean"], 4
                        ),
                        "signal_over_q95_noise": round(
                            extreme_prominence / noise["background_q95_to_mean"], 4
                        ),
                        "signal_over_top2_noise": round(
                            extreme_prominence / noise["background_top2_to_mean"], 4
                        ),
                        "signal_over_max_noise": round(
                            extreme_prominence / noise["background_max_to_mean"], 4
                        ),
                    }
                )
    return rows


def summarize_by_metric(rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    out = []
    for kind in ["l2", "l1"]:
        subset = [r for r in rows if r["kind"] == kind]
        y = np.asarray([float(r["rejection_rate"]) for r in subset])
        for metric in [
            "matched_extreme_to_mean",
            "background_cv",
            "background_q95_to_mean",
            "background_top2_to_mean",
            "background_max_to_mean",
            "signal_over_q95_noise",
            "signal_over_top2_noise",
            "signal_over_max_noise",
            "mean_corr",
            "mean_norm",
        ]:
            x = np.asarray([float(r[metric]) for r in subset])
            corr = float(np.corrcoef(x, y)[0, 1])
            out.append(
                {
                    "kind": kind,
                    "metric": metric,
                    "correlation_with_rejection_rate": round(corr, 4),
                    "n_rows": len(subset),
                }
            )
    return out


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = run_signal_noise_diagnostics()
    write_tsv(RESULTS_DIR / "signal_noise_diagnostics_20260726.tsv", rows)
    write_tsv(
        RESULTS_DIR / "signal_noise_metric_correlations_20260726.tsv",
        summarize_by_metric(rows),
    )


if __name__ == "__main__":
    main()
