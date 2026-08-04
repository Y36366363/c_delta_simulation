"""Shared utilities for routine robust-definition extension pilots."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


def common_permutation_pvalues(
    profiles_x: dict[str, np.ndarray],
    profiles_y: dict[str, np.ndarray],
    permutation_indices: np.ndarray,
) -> dict[str, tuple[float, float, float]]:
    """Return upper-tail p-value, raw ratio, and correlation by method."""
    results: dict[str, tuple[float, float, float]] = {}
    n_perm, n = permutation_indices.shape
    for method in profiles_x:
        sx, sy = profiles_x[method], profiles_y[method]
        denominator = float(sx.mean() * sy.mean())
        observed = float(np.mean(sx * sy) / denominator)
        statistics = (sy[permutation_indices] @ sx) / n / denominator
        p_value = (int(np.sum(statistics >= observed)) + 1) / (n_perm + 1)
        correlation = float(np.corrcoef(sx, sy)[0, 1])
        results[method] = (p_value, observed, correlation)
    return results


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
