from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import multi_extreme_power_simulation


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    rows = multi_extreme_power_simulation(
        sample_sizes=[15, 20, 40, 100],
        extreme_counts=[1, 2, 3],
        magnitudes=[4.0, 6.0, 8.0, 10.0],
        repetitions=100,
        n_perm=199,
        seed=20260711,
        background="normal",
        alpha=0.05,
    )
    print("Multi-extreme power simulation")
    print_table(
        rows,
        [
            "n",
            "k_extremes",
            "alignment",
            "magnitude",
            "background",
            "alpha",
            "repetitions",
            "n_perm",
            "resolution_floor_approx",
            "mean_raw",
            "mean_corr",
            "rejection_rate",
            "mean_raw_change",
        ],
    )


if __name__ == "__main__":
    main()
