"""Combine unequal-building adaptive validation runs and decision metrics."""

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


def combine_runs(
    runs: list[list[dict[str, str]]], key_fields: tuple[str, ...]
) -> list[dict[str, float | int | str]]:
    grouped = {}
    for rows in runs:
        for row in rows:
            key = tuple(row[field] for field in key_fields)
            cell = grouped.setdefault(
                key, {"repetitions": 0, "reject": 0, "weight_sum": 0.0}
            )
            repetitions = int(row["repetitions"])
            cell["repetitions"] += repetitions
            cell["reject"] += round(float(row["rejection_rate"]) * repetitions)
            cell["weight_sum"] += float(row.get("mean_profile_weight", 0.0)) * repetitions
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
                "mean_profile_weight": cell["weight_sum"] / repetitions,
            }
        )
    return output


def decision_summary(
    combined: list[dict[str, float | int | str]]
) -> list[dict[str, float | str]]:
    rows = []
    methods = sorted({str(row["method"]) for row in combined})
    for method in methods:
        selected = [row for row in combined if row["method"] == method]
        null = [
            float(row["rejection_rate"])
            for row in selected
            if row["scenario"] == "conditional_null"
        ]
        alternatives = [
            float(row["rejection_rate"])
            for row in selected
            if row["scenario"] != "conditional_null"
        ]
        rows.append(
            {
                "method": method,
                "aggregation": "all",
                "temperature": "all",
                "minimum_null_rejection": min(null),
                "maximum_null_rejection": max(null),
                "mean_alternative_power": sum(alternatives) / len(alternatives),
            }
        )
    # Temperature sensitivity for the two learned rules, averaging designs and alternatives.
    for method in ("cv_retrained", "cv_standardized"):
        for aggregation in ("building_equal", "sqrt_rooms", "room_equal"):
            subset = [
                row
                for row in combined
                if row["method"] == method and row["aggregation"] == aggregation
            ]
            for temperature in sorted({float(row["temperature"]) for row in subset}):
                cells = [
                    row
                    for row in subset
                    if float(row["temperature"]) == temperature
                    and row["scenario"] != "conditional_null"
                ]
                rows.append(
                    {
                        "method": method,
                        "aggregation": aggregation,
                        "temperature": temperature,
                        "minimum_null_rejection": "temperature_power",
                        "maximum_null_rejection": temperature,
                        "mean_alternative_power": sum(
                            float(row["rejection_rate"]) for row in cells
                        )
                        / len(cells),
                    }
                )
    return rows


if __name__ == "__main__":
    runs = [
        read_tsv(
            PROJECT_ROOT / "results" / f"unequal_building_adaptive_{phase}_20260813.tsv"
        )
        for phase in ("seed1", "seed2")
    ]
    combined = combine_runs(
        runs, ("design", "scenario", "temperature", "aggregation", "method")
    )
    write_tsv(
        PROJECT_ROOT / "results" / "unequal_building_adaptive_combined_20260813.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "unequal_building_adaptive_decision_20260813.tsv",
        decision_summary(combined),
    )

    restriction_runs = [
        read_tsv(
            PROJECT_ROOT / "results" / f"unequal_building_restriction_{phase}_20260813.tsv"
        )
        for phase in ("seed1", "seed2")
    ]
    write_tsv(
        PROJECT_ROOT / "results" / "unequal_building_restriction_combined_20260813.tsv",
        combine_runs(restriction_runs, ("permutation_scheme", "method")),
    )
