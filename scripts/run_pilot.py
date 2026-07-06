from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import summarize_scenarios


def main() -> None:
    scenarios = [
        "null_normal",
        "aligned_normal",
        "inverted_divergence",
        "heavy_tailed",
        "skewed",
        "contaminated_aligned",
    ]
    rows = summarize_scenarios(scenarios, n=60, seed=20260706)

    headers = [
        "scenario",
        "raw",
        "normalized_pairing",
        "direction_correlation",
        "perm_p",
        "ci_lower",
        "ci_upper",
    ]
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


if __name__ == "__main__":
    main()
