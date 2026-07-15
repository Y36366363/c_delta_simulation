from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import calibrated_subgroup_simulation


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    rows = []
    for target_corr in [0.35, 0.55, 0.65]:
        for background in ["normal", "t3", "lognormal"]:
            rows.extend(
                calibrated_subgroup_simulation(
                    n=40,
                    k_values=[1, 2, 3],
                    magnitude_grid=[
                        1.0,
                        1.5,
                        2.0,
                        2.5,
                        3.0,
                        3.5,
                        4.0,
                        4.5,
                        5.0,
                        5.5,
                        6.0,
                        7.0,
                        8.0,
                    ],
                    target_corr=target_corr,
                    reference_k=1,
                    reference_magnitude=8.0,
                    calibration_repetitions=180,
                    evaluation_repetitions=500,
                    n_perm=499,
                    seed=20260715 + int(target_corr * 1000),
                    background=background,
                    kind="l2",
                    scenarios=["matched", "negative_control", "independent_null"],
                    alpha=0.05,
                )
            )
    print_table(
        rows,
        [
            "background",
            "kind",
            "n",
            "k_extremes",
            "scenario",
            "target_reference",
            "target_corr",
            "selected_magnitude",
            "calibrated_mean_corr",
            "calibrated_mean_norm",
            "alpha",
            "calibration_repetitions",
            "evaluation_repetitions",
            "n_perm",
            "reject_count",
            "rejection_rate",
            "wilson_low",
            "wilson_high",
            "mean_raw",
            "mean_norm",
            "mean_corr",
            "mean_p",
            "p05",
            "p50",
            "p95",
            "mean_index_overlap",
        ],
    )


if __name__ == "__main__":
    main()
