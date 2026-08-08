"""Combine completed node/dyad mixture runs without rerunning simulations."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_node_dyad_mixture_20260808 import (
    combine_comparison_runs,
    crossover_summary,
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


if __name__ == "__main__":
    results = PROJECT_ROOT / "results"
    coarse = read_tsv(results / "node_dyad_mixture_coarse_comparison_20260808.tsv")
    refined = read_tsv(results / "node_dyad_mixture_refined_comparison_20260808.tsv")
    replication = read_tsv(
        results / "node_dyad_mixture_replication_comparison_20260808.tsv"
    )
    combined = combine_comparison_runs((refined, replication))
    write_tsv(
        results / "node_dyad_mixture_combined_comparison_20260808.tsv",
        combined,
    )
    summaries = []
    for phase, rows in (
        ("coarse", coarse),
        ("refined", refined),
        ("replication", replication),
        ("combined", combined),
    ):
        summaries.extend(crossover_summary(rows, phase=phase))
    write_tsv(
        results / "node_dyad_mixture_crossover_20260808.tsv",
        summaries,
    )
