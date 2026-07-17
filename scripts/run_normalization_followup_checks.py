from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    calibrated_subgroup_simulation,
    independent_null_size_simulation,
    permutation_mean_check,
    make_scenario,
)


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    x, y = make_scenario("aligned_normal", 8, seed=20260716)
    print("Corrected permutation mean checks")
    print_table(
        [
            permutation_mean_check(x, y, exact=True),
            permutation_mean_check(x, y, n_perm=5000, seed=20260716),
        ],
        ["n", "method", "n_statistics", "mean_permuted_raw", "expected_mean", "absolute_error"],
    )

    print()
    print("Compact lower-target corrected-scale check")
    rows = []
    for kind in ["l2", "l1"]:
        rows.extend(
            calibrated_subgroup_simulation(
                n=40,
                k_values=[1, 2, 3],
                magnitude_grid=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0],
                target_corr=0.35,
                calibration_repetitions=80,
                evaluation_repetitions=150,
                n_perm=299,
                seed=20260716,
                background="normal",
                kind=kind,
                scenarios=["matched", "independent_null"],
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
            "target_corr",
            "selected_magnitude",
            "rejection_rate",
            "mean_raw",
            "mean_norm",
            "mean_corr",
            "mean_p",
        ],
    )

    print()
    print("Flagged large-n independent-null recheck")
    flagged = independent_null_size_simulation(
        n=160,
        k=1,
        magnitude=7.0,
        repetitions=1000,
        n_perm=999,
        seed=20260716,
        background="lognormal",
        kind="l1",
        alphas=[0.05, 0.01],
    )
    print_table(
        flagged,
        [
            "background",
            "kind",
            "n",
            "k_extremes",
            "magnitude",
            "alpha",
            "repetitions",
            "n_perm",
            "reject_count",
            "empirical_size",
            "wilson_low",
            "wilson_high",
            "mean_p",
            "p05",
            "p50",
            "p95",
            "mean_index_overlap",
        ],
    )


if __name__ == "__main__":
    main()
