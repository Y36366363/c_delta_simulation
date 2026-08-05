"""Shared utilities for routine robust-definition extension pilots."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


def within_block_permutation_indices(
    blocks: np.ndarray | list[object],
    n_perm: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate index permutations that only rearrange units within blocks.

    The returned rows can be used anywhere ordinary permutation indices are
    accepted.  Every row is a full permutation of ``range(n)`` and preserves
    each observation's block label.
    """
    labels = np.asarray(blocks)
    if labels.ndim != 1:
        raise ValueError("blocks must be one-dimensional")
    if labels.size < 3:
        raise ValueError("blocks must contain at least three observations")
    if n_perm < 1:
        raise ValueError("n_perm must be positive")

    indices = np.tile(np.arange(labels.size), (n_perm, 1))
    for label in np.unique(labels):
        members = np.flatnonzero(labels == label)
        if members.size < 2:
            continue
        for row in range(n_perm):
            indices[row, members] = rng.permutation(members)
    return indices


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
