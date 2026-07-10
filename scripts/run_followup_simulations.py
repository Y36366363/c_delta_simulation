from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    background_extreme_simulation,
    nominal_size_simulation,
    power_curve_simulation,
)


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    print("Power curve: matched extreme under normal background")
    power_rows = power_curve_simulation(
        sample_sizes=[15, 20, 40],
        magnitudes=[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
        repetitions=120,
        n_perm=199,
        seed=20260710,
        background="normal",
        alpha=0.05,
    )
    print_table(
        power_rows,
        [
            "n",
            "magnitude",
            "background",
            "alpha",
            "repetitions",
            "mean_raw",
            "mean_corr",
            "rejection_rate",
            "mean_raw_change",
        ],
    )

    print()
    print("Background check: extreme-value alignment under non-normal data")
    background_rows = background_extreme_simulation(
        backgrounds=["normal", "t3", "lognormal"],
        n=40,
        magnitude=8.0,
        repetitions=120,
        n_perm=199,
        seed=20260710,
        alpha=0.05,
    )
    print_table(
        background_rows,
        [
            "background",
            "scenario",
            "n",
            "magnitude",
            "alpha",
            "repetitions",
            "mean_raw",
            "mean_corr",
            "rejection_rate",
            "mean_raw_change",
        ],
    )

    print()
    print("Nominal size check: null and mismatched controls")
    size_rows = nominal_size_simulation(
        backgrounds=["normal", "t3", "lognormal"],
        scenarios=["null_normal", "mismatched_extreme"],
        n=40,
        magnitude=8.0,
        repetitions=200,
        n_perm=499,
        seed=20260710,
        alphas=[0.05, 0.01],
    )
    print_table(
        size_rows,
        [
            "background",
            "scenario",
            "n",
            "magnitude",
            "alpha",
            "repetitions",
            "n_perm",
            "empirical_size",
            "mean_p",
        ],
    )


if __name__ == "__main__":
    main()
