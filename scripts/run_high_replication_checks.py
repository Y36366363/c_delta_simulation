from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import independent_null_size_simulation, overlap_layer_diagnostic


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    print("High-replication independent-null size check")
    rows = []
    for background in ["normal", "t3", "lognormal"]:
        rows.extend(
            independent_null_size_simulation(
                n=40,
                k=2,
                magnitude=8.0,
                repetitions=1000,
                n_perm=999,
                seed=20260713,
                background=background,
                alphas=[0.05, 0.01],
            )
        )
    print_table(
        rows,
        [
            "background",
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
            "p25",
            "p50",
            "p75",
            "p95",
            "mean_index_overlap",
        ],
    )

    print()
    print("High-replication overlap-layer diagnostic")
    overlap_rows = overlap_layer_diagnostic(
        n=15,
        k=3,
        magnitude=8.0,
        n_perm=100000,
        seed=20260713,
    )
    print_table(
        overlap_rows,
        [
            "n",
            "k_extremes",
            "magnitude",
            "overlap_count",
            "n_permutations",
            "layer_probability",
            "mean_stat",
            "p95_stat",
            "max_stat",
            "observed_stat",
            "share_ge_observed",
        ],
    )


if __name__ == "__main__":
    main()
