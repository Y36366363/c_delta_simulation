from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import magnitude_grid_simulation, repeated_outlier_simulation


def print_table(rows, headers):
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


def main() -> None:
    repeated = repeated_outlier_simulation(
        n=40,
        repetitions=300,
        n_perm=99,
        seed=20260709,
        magnitude=8.0,
    )
    repeated_headers = [
        "scenario",
        "repetitions",
        "magnitude",
        "mean_raw",
        "sd_raw",
        "mean_norm",
        "mean_corr",
        "rejection_rate",
        "mean_raw_change",
    ]
    print("Repeated outlier-alignment simulation")
    print_table(repeated, repeated_headers)

    print()
    grid = magnitude_grid_simulation(
        n=40,
        repetitions=200,
        n_perm=99,
        seed=20260709,
        magnitudes=[0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
    )
    grid_headers = [
        "scenario",
        "magnitude",
        "repetitions",
        "mean_raw",
        "mean_corr",
        "rejection_rate",
        "mean_raw_change",
    ]
    print("Matched-extreme magnitude grid")
    print_table(grid, grid_headers)


if __name__ == "__main__":
    main()
