from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import large_scale_simulation


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    rows = large_scale_simulation(
        sample_sizes=[100, 250, 500],
        extreme_counts=[1, 2, 3],
        scenarios=["matched", "mismatched"],
        backgrounds=["normal", "t3", "lognormal"],
        repetitions=80,
        n_perm=499,
        seed=20260712,
        magnitude=8.0,
        alpha=0.05,
    )
    print("Large-scale multi-extreme simulation")
    print_table(
        rows,
        [
            "background",
            "n",
            "k_extremes",
            "alignment",
            "magnitude",
            "alpha",
            "repetitions",
            "n_perm",
            "resolution_floor_approx",
            "mean_raw",
            "mean_corr",
            "rejection_rate",
        ],
    )


if __name__ == "__main__":
    main()
