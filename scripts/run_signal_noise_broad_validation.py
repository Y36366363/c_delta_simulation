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


def rankdata(values: list[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    order = np.argsort(arr)
    ranks = np.empty(arr.size, dtype=float)
    i = 0
    while i < arr.size:
        j = i + 1
        while j < arr.size and arr[order[j]] == arr[order[i]]:
            j += 1
        ranks[order[i:j]] = (i + j - 1) / 2 + 1
        i = j
    return ranks


def corr(x: list[float], y: list[float], *, method: str) -> float:
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if method == "spearman":
        x_arr = rankdata(x_arr.tolist())
        y_arr = rankdata(y_arr.tolist())
    if np.std(x_arr) == 0.0 or np.std(y_arr) == 0.0:
        return float("nan")
    return float(np.corrcoef(x_arr, y_arr)[0, 1])


def bootstrap_ci(
    x: list[float],
    y: list[float],
    *,
    method: str,
    seed: int,
    n_boot: int = 1000,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    values = []
    for _ in range(n_boot):
        idx = rng.integers(0, x_arr.size, size=x_arr.size)
        values.append(corr(x_arr[idx].tolist(), y_arr[idx].tolist(), method=method))
    lo, hi = np.nanquantile(values, [0.025, 0.975])
    return float(lo), float(hi)


def load_matched_power_rows() -> list[dict[str, str]]:
    path = RESULTS_DIR / "tail_df_factor_grid_20260719.tsv"
    with path.open() as f:
        return [
            row
            for row in csv.DictReader(f, delimiter="\t")
            if row["scenario"] == "matched"
        ]


def background_noise_cache(
    matched_rows: list[dict[str, str]],
    *,
    repetitions: int,
) -> dict[tuple[str, str, int], dict[str, float]]:
    keys = sorted(
        {
            (row["kind"], row["df_label"], int(row["n"]))
            for row in matched_rows
        }
    )
    out = {}
    for key_offset, (kind, df_label, n) in enumerate(keys):
        cv_values = []
        q90_values = []
        q95_values = []
        topk_values = {1: [], 2: [], 3: [], 4: [], 8: []}
        max_values = []
        for rep in range(repetitions):
            rng = np.random.default_rng(20260726 + key_offset * 100_000 + rep)
            x = background_sample(rng, n, df_label)
            dx = divergence_vector(x, kind=kind)
            mean_dx = float(dx.mean())
            cv_values.append(float(dx.std() / mean_dx))
            q90_values.append(float(np.quantile(dx, 0.90) / mean_dx))
            q95_values.append(float(np.quantile(dx, 0.95) / mean_dx))
            max_values.append(float(dx.max() / mean_dx))
            sorted_dx = np.sort(dx)
            for k in topk_values:
                k_eff = min(k, dx.size)
                topk_values[k].append(float(np.mean(sorted_dx[-k_eff:]) / mean_dx))
        out[(kind, df_label, n)] = {
            "background_cv": mean_float(cv_values),
            "background_q90_to_mean": mean_float(q90_values),
            "background_q95_to_mean": mean_float(q95_values),
            "background_max_to_mean": mean_float(max_values),
            **{
                f"background_top{k}_to_mean": mean_float(values)
                for k, values in topk_values.items()
            },
        }
    return out


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
        "mean_corr_from_signal_runs": mean_float(corr_values),
        "mean_norm_from_signal_runs": mean_float(norm_values),
    }


def run_broad_validation() -> list[dict[str, float | str]]:
    matched_rows = load_matched_power_rows()
    background_repetitions = 700
    matched_repetitions = 220
    noise = background_noise_cache(matched_rows, repetitions=background_repetitions)
    out = []
    for row_offset, row in enumerate(matched_rows):
        kind = row["kind"]
        df_label = row["df_label"]
        n = int(row["n"])
        k = int(row["k_extremes"])
        magnitude = float(row["magnitude"])
        signal = matched_signal_summary(
            kind=kind,
            df_label=df_label,
            n=n,
            k=k,
            magnitude=magnitude,
            repetitions=matched_repetitions,
            seed_base=20260726 + row_offset * 10_000,
        )
        background = noise[(kind, df_label, n)]
        extreme = signal["matched_extreme_to_mean"]
        topk_key = f"background_top{k}_to_mean"
        out.append(
            {
                "kind": kind,
                "df_label": df_label,
                "n": n,
                "k_extremes": k,
                "magnitude": magnitude,
                "scenario": "matched",
                "power_repetitions": row["repetitions"],
                "power_n_perm": row["n_perm"],
                "background_repetitions": background_repetitions,
                "matched_repetitions": matched_repetitions,
                "rejection_rate": float(row["rejection_rate"]),
                "wilson_low": float(row["wilson_low"]),
                "wilson_high": float(row["wilson_high"]),
                "matched_extreme_to_mean": round(extreme, 4),
                "matched_nonextreme_to_mean": round(
                    signal["matched_nonextreme_to_mean"], 4
                ),
                "mean_corr_from_signal_runs": round(
                    signal["mean_corr_from_signal_runs"], 4
                ),
                "mean_norm_from_signal_runs": round(
                    signal["mean_norm_from_signal_runs"], 4
                ),
                **{k_: round(v, 4) for k_, v in background.items()},
                "background_topk_to_mean": round(background[topk_key], 4),
                "signal_over_q90_noise": round(
                    extreme / background["background_q90_to_mean"], 4
                ),
                "signal_over_q95_noise": round(
                    extreme / background["background_q95_to_mean"], 4
                ),
                "signal_over_topk_noise": round(
                    extreme / background[topk_key], 4
                ),
                "signal_over_max_noise": round(
                    extreme / background["background_max_to_mean"], 4
                ),
            }
        )
    return out


def summarize_correlations(rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    metrics = [
        "matched_extreme_to_mean",
        "background_cv",
        "background_q90_to_mean",
        "background_q95_to_mean",
        "background_topk_to_mean",
        "background_max_to_mean",
        "signal_over_q90_noise",
        "signal_over_q95_noise",
        "signal_over_topk_noise",
        "signal_over_max_noise",
        "mean_corr_from_signal_runs",
        "mean_norm_from_signal_runs",
    ]
    groups = [("all", rows)]
    for kind in ["l2", "l1"]:
        groups.append((f"kind={kind}", [r for r in rows if r["kind"] == kind]))
    for n in [40, 80, 160]:
        groups.append((f"n={n}", [r for r in rows if int(r["n"]) == n]))
    for k in [1, 2, 3]:
        groups.append((f"k={k}", [r for r in rows if int(r["k_extremes"]) == k]))
    for magnitude in [4.0, 6.0, 8.0]:
        groups.append(
            (
                f"magnitude={magnitude:g}",
                [r for r in rows if float(r["magnitude"]) == magnitude],
            )
        )

    out = []
    for group_name, subset in groups:
        if len(subset) < 10:
            continue
        y = [float(r["rejection_rate"]) for r in subset]
        for metric in metrics:
            x = [float(r[metric]) for r in subset]
            for method in ["pearson", "spearman"]:
                value = corr(x, y, method=method)
                lo, hi = bootstrap_ci(
                    x,
                    y,
                    method=method,
                    seed=20260726 + len(out) * 1000,
                    n_boot=1000,
                )
                out.append(
                    {
                        "group": group_name,
                        "metric": metric,
                        "method": method,
                        "correlation_with_rejection_rate": round(value, 4),
                        "bootstrap_low": round(lo, 4),
                        "bootstrap_high": round(hi, 4),
                        "n_rows": len(subset),
                    }
                )
    return out


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = run_broad_validation()
    write_tsv(RESULTS_DIR / "signal_noise_broad_validation_20260726.tsv", rows)
    write_tsv(
        RESULTS_DIR / "signal_noise_broad_correlations_20260726.tsv",
        summarize_correlations(rows),
    )


if __name__ == "__main__":
    main()
