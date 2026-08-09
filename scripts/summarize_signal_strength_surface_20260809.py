"""Create the final complete surface after the targeted grid extension."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_signal_strength_surface_20260809 import (
    estimate_crossovers,
    fit_ratio_models,
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


if __name__ == "__main__":
    results = PROJECT_ROOT / "results"
    base = read_tsv(results / "signal_strength_surface_combined_20260809.tsv")
    extension = read_tsv(
        results / "signal_strength_surface_extension_combined_20260809.tsv"
    )
    complete = [
        row
        for row in base
        if not (
            float(row["node_strength"]) == 0.35
            and float(row["dyad_strength"]) == 0.65
        )
    ] + extension
    crossovers = estimate_crossovers(complete, phase="final_combined")
    models, predictions = fit_ratio_models(crossovers)
    write_tsv(
        results / "signal_strength_surface_final_combined_20260809.tsv", complete
    )
    write_tsv(
        results / "signal_strength_surface_crossovers_20260809.tsv", crossovers
    )
    write_tsv(results / "signal_strength_ratio_models_20260809.tsv", models)
    write_tsv(
        results / "signal_strength_ratio_predictions_20260809.tsv", predictions
    )
