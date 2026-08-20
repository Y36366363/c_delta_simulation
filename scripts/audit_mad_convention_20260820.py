"""Audit the finite-sample median/MAD convention used by the project."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "results" / "mad_convention_audit_20260820.tsv"
DEFAULT_SEED = 20260820


def lower_empirical_median(values: np.ndarray, axis: int = -1) -> np.ndarray:
    """Return inf{x: F_n(x) >= 1/2}, i.e. the lower middle value for even n."""
    values = np.asarray(values, dtype=float)
    n = values.shape[axis]
    kth = (n - 1) // 2
    return np.partition(values, kth, axis=axis).take(kth, axis=axis)


def numpy_median_mad(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centres = np.median(samples, axis=1)
    deviations = np.abs(samples - centres[:, None])
    return centres, np.median(deviations, axis=1)


def lower_quantile_median_mad(samples: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centres = lower_empirical_median(samples, axis=1)
    deviations = np.abs(samples - centres[:, None])
    return centres, lower_empirical_median(deviations, axis=1)


def _summarize_difference(
    *,
    distribution: str,
    n: int,
    quantity: str,
    difference: np.ndarray,
    seed: int,
) -> dict[str, float | int | str]:
    absolute = np.abs(difference)
    repetitions = absolute.size
    mean_absolute = float(np.mean(absolute))
    mcse_mean_absolute = float(np.std(absolute, ddof=1) / np.sqrt(repetitions))
    median_absolute = float(np.median(absolute))
    q95_absolute = float(np.quantile(absolute, 0.95))
    return {
        "seed": seed,
        "distribution": distribution,
        "n": n,
        "repetitions": repetitions,
        "quantity": quantity,
        "mean_abs_difference": mean_absolute,
        "mcse_mean_abs_difference": mcse_mean_absolute,
        "median_abs_difference": median_absolute,
        "q95_abs_difference": q95_absolute,
        "sqrt_n_times_median_abs_difference": np.sqrt(n) * median_absolute,
        "sqrt_n_times_q95_abs_difference": np.sqrt(n) * q95_absolute,
        "n_times_median_abs_difference": n * median_absolute,
    }


def run_audit(
    *,
    seed: int = DEFAULT_SEED,
    repetitions: int = 6000,
    sample_sizes: tuple[int, ...] = (40, 80, 160, 320, 640),
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for distribution in ("normal", "lognormal_logsd_1p1"):
        for n in sample_sizes:
            if distribution == "normal":
                samples = rng.normal(size=(repetitions, n))
            else:
                samples = rng.lognormal(mean=0.0, sigma=1.1, size=(repetitions, n))
            numpy_median, numpy_mad = numpy_median_mad(samples)
            lower_median, lower_mad = lower_quantile_median_mad(samples)
            rows.append(
                _summarize_difference(
                    distribution=distribution,
                    n=n,
                    quantity="median",
                    difference=numpy_median - lower_median,
                    seed=seed,
                )
            )
            rows.append(
                _summarize_difference(
                    distribution=distribution,
                    n=n,
                    quantity="mad",
                    difference=numpy_mad - lower_mad,
                    seed=seed,
                )
            )
    return rows


def write_rows(rows: list[dict[str, float | int | str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--repetitions", type=int, default=6000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = run_audit(seed=args.seed, repetitions=args.repetitions)
    write_rows(rows, args.output)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
