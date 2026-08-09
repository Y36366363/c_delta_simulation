"""Targeted extension for the one surface cell whose refined grid missed zero."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_signal_strength_surface_20260809 import (
    combine_surface_runs,
    run_strength_surface,
)


if __name__ == "__main__":
    combination = ((0.35, 0.65),)
    weights = {(0.35, 0.65): tuple(round(0.025 * index, 3) for index in range(8))}
    runs = []
    for phase, seed in (("extension", 20261034), ("extension_replication", 20261035)):
        rows = run_strength_surface(
            combination,
            weights,
            repetitions=600,
            n_perm=199,
            seed=seed,
            phase=phase,
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"signal_strength_surface_{phase}_20260809.tsv",
            rows,
        )
    combined = combine_surface_runs(tuple(runs), phase="extension_combined")
    write_tsv(
        PROJECT_ROOT / "results" / "signal_strength_surface_extension_combined_20260809.tsv",
        combined,
    )
