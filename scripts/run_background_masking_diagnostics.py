from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np

from cdelta import _wilson_interval, c_delta
from scripts.run_tail_factor_comparison import fast_permutation_p_value, write_tsv
from scripts.run_teacher_feedback_validation import make_scaled_scenario


RESULTS_DIR = PROJECT_ROOT / "results"
TAILS = ["normal", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]


def masking_metrics(dx: np.ndarray, dy: np.ndarray, k: int) -> dict[str, float]:
    n = dx.size
    planted = np.arange(n - k, n)
    background = np.arange(0, n - k)

    x_background_order = background[np.argsort(dx[background])]
    y_background_order = background[np.argsort(dy[background])]
    x_top_background = set(x_background_order[-k:].tolist())
    y_top_background = set(y_background_order[-k:].tolist())

    planted_products = dx[planted] * dy[planted]
    background_products = dx[background] * dy[background]
    mean_dx = float(np.mean(dx))
    mean_dy = float(np.mean(dy))
    random_pairing_planted_product = float(np.mean(dx[planted]) * mean_dy)

    return {
        "x_max_is_background": float(np.argmax(dx) < n - k),
        "y_max_is_background": float(np.argmax(dy) < n - k),
        "either_max_is_background": float(
            np.argmax(dx) < n - k or np.argmax(dy) < n - k
        ),
        "both_max_are_background": float(
            np.argmax(dx) < n - k and np.argmax(dy) < n - k
        ),
        "background_topk_index_overlap": float(
            len(x_top_background.intersection(y_top_background)) / k
        ),
        "background_max_over_planted_mean_x": float(
            np.max(dx[background]) / np.mean(dx[planted])
        ),
        "background_max_over_planted_mean_y": float(
            np.max(dy[background]) / np.mean(dy[planted])
        ),
        "either_background_max_exceeds_planted_mean": float(
            np.max(dx[background]) > np.mean(dx[planted])
            or np.max(dy[background]) > np.mean(dy[planted])
        ),
        "planted_product_to_background_product": float(
            np.mean(planted_products) / np.mean(background_products)
        ),
        "planted_product_to_random_pairing": float(
            np.mean(planted_products) / random_pairing_planted_product
        ),
        "mechanism_contrast": float(
            (
                np.mean(planted_products)
                - random_pairing_planted_product
            )
            / (mean_dx * mean_dy)
        ),
        "background_max_product_exceeds_planted_mean_product": float(
            np.max(background_products) > np.mean(planted_products)
        ),
    }


def summarize_rows(rows: list[dict]) -> list[dict]:
    groups = {}
    for row in rows:
        key = (row["kind"], row["scale_design"], row["df_label"])
        groups.setdefault(key, []).append(row)

    out = []
    for (kind, scale_design, df_label), subset in sorted(groups.items()):
        rejected = [row for row in subset if row["p_value"] < 0.05]
        not_rejected = [row for row in subset if row["p_value"] >= 0.05]
        masked = [
            row
            for row in subset
            if row["background_max_product_exceeds_planted_mean_product"] == 1.0
        ]
        not_masked = [
            row
            for row in subset
            if row["background_max_product_exceeds_planted_mean_product"] == 0.0
        ]
        reject_count = len(rejected)
        low, high = _wilson_interval(reject_count, len(subset))

        def mean(name: str, values: list[dict] = subset) -> float:
            if not values:
                return float("nan")
            return float(np.mean([float(row[name]) for row in values]))

        out.append(
            {
                "kind": kind,
                "scale_design": scale_design,
                "df_label": df_label,
                "n": subset[0]["n"],
                "k_extremes": subset[0]["k_extremes"],
                "magnitude": subset[0]["magnitude"],
                "repetitions": len(subset),
                "n_perm": subset[0]["n_perm"],
                "rejection_rate": round(reject_count / len(subset), 4),
                "wilson_low": round(float(low), 4),
                "wilson_high": round(float(high), 4),
                "prob_either_max_is_background": round(
                    mean("either_max_is_background"), 4
                ),
                "prob_both_max_are_background": round(
                    mean("both_max_are_background"), 4
                ),
                "mean_background_topk_index_overlap": round(
                    mean("background_topk_index_overlap"), 4
                ),
                "prob_background_max_exceeds_planted_mean": round(
                    mean("either_background_max_exceeds_planted_mean"), 4
                ),
                "prob_background_product_masks_planted_mean": round(
                    mean("background_max_product_exceeds_planted_mean_product"), 4
                ),
                "median_planted_to_background_product": round(
                    float(
                        np.median(
                            [
                                row["planted_product_to_background_product"]
                                for row in subset
                            ]
                        )
                    ),
                    4,
                ),
                "median_planted_to_random_pairing": round(
                    float(
                        np.median(
                            [
                                row["planted_product_to_random_pairing"]
                                for row in subset
                            ]
                        )
                    ),
                    4,
                ),
                "median_mechanism_contrast": round(
                    float(np.median([row["mechanism_contrast"] for row in subset])),
                    4,
                ),
                "masking_probability_when_rejected": round(
                    mean(
                        "background_max_product_exceeds_planted_mean_product",
                        rejected,
                    ),
                    4,
                ),
                "masking_probability_when_not_rejected": round(
                    mean(
                        "background_max_product_exceeds_planted_mean_product",
                        not_rejected,
                    ),
                    4,
                ),
                "rejection_rate_when_masking": round(
                    mean("rejected", masked), 4
                ),
                "rejection_rate_without_masking": round(
                    mean("rejected", not_masked), 4
                ),
            }
        )
    return out


def run_diagnostics() -> tuple[list[dict], list[dict]]:
    rows = []
    n = 80
    k = 2
    magnitude = 8.0
    repetitions = 500
    n_perm = 299

    for kind_offset, kind in enumerate(["l2", "l1"]):
        for design_offset, scale_design in enumerate(
            ["common_scale_parameter", "common_mad"]
        ):
            for tail_offset, df_label in enumerate(TAILS):
                for rep in range(repetitions):
                    seed = (
                        20260730
                        + kind_offset * 100_000_000
                        + design_offset * 10_000_000
                        + tail_offset * 100_000
                        + rep
                    )
                    x, y = make_scaled_scenario(
                        n=n,
                        k=k,
                        magnitude=magnitude,
                        df_label=df_label,
                        scenario="matched",
                        design=scale_design,
                        seed=seed,
                    )
                    result = c_delta(x, y, kind=kind)
                    p_value = fast_permutation_p_value(
                        result.dx,
                        result.dy,
                        result.raw,
                        n_perm=n_perm,
                        seed=seed + 50_000_000,
                    )
                    rows.append(
                        {
                            "kind": kind,
                            "scale_design": scale_design,
                            "df_label": df_label,
                            "n": n,
                            "k_extremes": k,
                            "magnitude": magnitude,
                            "repetition": rep,
                            "n_perm": n_perm,
                            "c_delta": round(result.raw, 8),
                            "divergence_correlation": round(
                                result.direction_correlation, 8
                            ),
                            "p_value": round(p_value, 8),
                            "rejected": float(p_value < 0.05),
                            **{
                                name: round(value, 8)
                                for name, value in masking_metrics(
                                    result.dx, result.dy, k
                                ).items()
                            },
                        }
                    )
    return rows, summarize_rows(rows)


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows, summaries = run_diagnostics()
    write_tsv(
        RESULTS_DIR / "background_masking_diagnostics_20260730.tsv",
        rows,
    )
    write_tsv(
        RESULTS_DIR / "background_masking_summary_20260730.tsv",
        summaries,
    )


if __name__ == "__main__":
    main()
