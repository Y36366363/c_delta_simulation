from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import outlier_influence_summary


def main() -> None:
    rows = outlier_influence_summary(n=40, seed=20260709, n_perm=499)
    headers = [
        "scenario",
        "main_raw",
        "main_norm",
        "main_corr",
        "main_perm_p",
        "sensitivity_raw_without_extreme_indices",
        "raw_change",
    ]
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


if __name__ == "__main__":
    main()
