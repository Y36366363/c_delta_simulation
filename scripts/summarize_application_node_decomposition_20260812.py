"""Combine the independent application-model and adaptive-weight runs."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def combine_rates(
    runs: list[list[dict[str, str]]], key_fields: tuple[str, ...]
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, ...], dict[str, float]] = {}
    for rows in runs:
        for row in rows:
            key = tuple(row[field] for field in key_fields)
            cell = grouped.setdefault(key, {"repetitions": 0.0, "reject": 0.0})
            repetitions = int(row["repetitions"])
            cell["repetitions"] += repetitions
            cell["reject"] += round(float(row["rejection_rate"]) * repetitions)
    output = []
    for key, cell in sorted(grouped.items()):
        repetitions = int(cell["repetitions"])
        reject = int(cell["reject"])
        low, high = wilson(reject, repetitions)
        output.append(
            {
                **dict(zip(key_fields, key)),
                "repetitions": repetitions,
                "reject_count": reject,
                "rejection_rate": reject / repetitions,
                "wilson_low": low,
                "wilson_high": high,
            }
        )
    return output


def decomposition_effects(
    combined: list[dict[str, float | int | str]]
) -> list[dict[str, float | str]]:
    output = []
    for method in sorted({str(row["method"]) for row in combined}):
        selected = [row for row in combined if row["method"] == method]
        factors = (
            ("positive_probability", "0.5", "0.7"),
            ("sign_agreement", "0.5", "0.75"),
            ("magnitude_sigma", "0.35", "0.85"),
            ("center_sd", "0.0", "1.0"),
        )
        for factor, low_value, high_value in factors:
            low = [
                float(row["rejection_rate"])
                for row in selected
                if str(row[factor]) == low_value
            ]
            high = [
                float(row["rejection_rate"])
                for row in selected
                if str(row[factor]) == high_value
            ]
            output.append(
                {
                    "method": method,
                    "factor": factor,
                    "low_level": low_value,
                    "high_level": high_value,
                    "average_power_low": sum(low) / len(low),
                    "average_power_high": sum(high) / len(high),
                    "average_power_main_effect": sum(high) / len(high)
                    - sum(low) / len(low),
                }
            )
    return output


if __name__ == "__main__":
    decomposition_runs = [
        read_tsv(
            PROJECT_ROOT
            / "results"
            / f"application_node_decomposition_{phase}_20260812.tsv"
        )
        for phase in ("seed1", "seed2")
    ]
    decomposition = combine_rates(
        decomposition_runs,
        (
            "positive_probability",
            "sign_agreement",
            "magnitude_sigma",
            "center_sd",
            "method",
        ),
    )
    write_tsv(
        PROJECT_ROOT
        / "results"
        / "application_node_decomposition_combined_20260812.tsv",
        decomposition,
    )
    write_tsv(
        PROJECT_ROOT
        / "results"
        / "application_node_decomposition_effects_20260812.tsv",
        decomposition_effects(decomposition),
    )

    null_runs = [
        read_tsv(
            PROJECT_ROOT / "results" / f"adaptive_weight_null_{phase}_20260812.tsv"
        )
        for phase in ("seed1", "seed2")
    ]
    write_tsv(
        PROJECT_ROOT / "results" / "adaptive_weight_null_combined_20260812.tsv",
        combine_rates(null_runs, ("scenario", "method")),
    )
