from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import variant_comparison_simulation


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    rows = variant_comparison_simulation(
        n=40,
        k=2,
        magnitude=8.0,
        repetitions=300,
        n_perm=499,
        seed=20260714,
        backgrounds=["normal", "t3", "lognormal"],
        kinds=["l2", "l1"],
        scenarios=["matched", "negative_control", "independent_null"],
        alpha=0.05,
    )
    print_table(
        rows,
        [
            "kind",
            "background",
            "scenario",
            "n",
            "k_extremes",
            "magnitude",
            "alpha",
            "repetitions",
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
