from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import near_zero_divergence_simulation


def main() -> None:
    rows = near_zero_divergence_simulation(
        epsilons=[1.0, 1e-2, 1e-4, 1e-6, 1e-8, 0.0],
        n=40,
        seed=20260712,
    )
    headers = [
        "epsilon",
        "divergence_scale",
        "raw",
        "normalized_pairing",
        "direction_correlation",
        "status",
    ]
    print("Near-zero empirical divergence boundary")
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(row[h]) for h in headers))


if __name__ == "__main__":
    main()
