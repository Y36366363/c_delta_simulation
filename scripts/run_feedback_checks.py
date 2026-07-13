from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import (
    independent_null_size_simulation,
    make_multi_extreme_scenario,
    overlap_layer_diagnostic,
    permutation_mean_check,
)


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    print("Permutation mean check")
    x, y, _ = make_multi_extreme_scenario(
        n=8,
        k=2,
        seed=20260713,
        magnitude=8.0,
        matched=True,
    )
    rows = [
        permutation_mean_check(x, y, exact=True),
        permutation_mean_check(x, y, n_perm=5000, seed=20260713, exact=False),
    ]
    print_table(
        rows,
        ["n", "method", "n_statistics", "mean_permuted_raw", "expected_mean", "absolute_error"],
    )

    print()
    print("Overlap-layer diagnostic")
    overlap_rows = overlap_layer_diagnostic(
        n=15,
        k=3,
        magnitude=8.0,
        n_perm=10000,
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

    print()
    print("Independent-null size check")
    null_rows = []
    for background in ["normal", "t3", "lognormal"]:
        null_rows.extend(
            independent_null_size_simulation(
                n=40,
                k=2,
                magnitude=8.0,
                repetitions=200,
                n_perm=499,
                seed=20260713,
                background=background,
                alphas=[0.05, 0.01],
            )
        )
    print_table(
        null_rows,
        [
            "background",
            "n",
            "k_extremes",
            "magnitude",
            "alpha",
            "repetitions",
            "n_perm",
            "empirical_size",
            "mean_p",
            "mean_index_overlap",
        ],
    )


if __name__ == "__main__":
    main()
