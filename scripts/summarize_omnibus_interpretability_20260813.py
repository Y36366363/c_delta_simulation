"""Combine omnibus interpretability and focused attribution seed summaries."""

from __future__ import annotations

import csv
import math
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _finite(row: dict[str, str], field: str) -> float | None:
    try:
        value = float(row[field])
    except (KeyError, ValueError):
        return None
    return value if math.isfinite(value) else None


def combine_summary_rows(
    rows: list[dict[str, str]], key_fields: tuple[str, ...]
) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(tuple(row[field] for field in key_fields), []).append(row)
    output = []
    rate_fields = (
        "profile_rejection_rate",
        "mantel_rejection_rate",
        "best_component_power",
        "omnibus_regret",
        "adjusted_profile_rejection_rate",
        "adjusted_mantel_rejection_rate",
        "winner_profile_rate",
        "winner_expected_rate",
        "mean_profile_z",
        "mean_mantel_z",
        "profile_only_rate",
        "mantel_only_rate",
        "both_rate",
        "unresolved_rate",
        "winner_agreement_with_999",
        "decision_agreement_with_999",
        "attribution_agreement_with_999",
    )
    for key, group in sorted(grouped.items()):
        repetitions = sum(int(row["repetitions"]) for row in group)
        reject = sum(
            round(float(row["omnibus_rejection_rate"]) * int(row["repetitions"]))
            for row in group
        )
        low, high = wilson(reject, repetitions)
        combined: dict[str, float | int | str] = {
            **dict(zip(key_fields, key)),
            "repetitions": repetitions,
            "omnibus_reject_count": reject,
            "omnibus_rejection_rate": reject / repetitions,
            "wilson_low": low,
            "wilson_high": high,
        }
        for field in rate_fields:
            pairs = [
                (_finite(row, field), int(row["repetitions"])) for row in group
            ]
            valid = [(value, n) for value, n in pairs if value is not None]
            combined[field] = (
                sum(float(value) * n for value, n in valid) / sum(n for _, n in valid)
                if valid
                else math.nan
            )
        for label in ("profile_only", "mantel_only", "both", "unresolved"):
            numerator = sum(
                (
                    0.0
                    if _finite(row, f"{label}_share_given_reject") is None
                    else float(row[f"{label}_share_given_reject"])
                    * round(
                        float(row["omnibus_rejection_rate"])
                        * int(row["repetitions"])
                    )
                )
                for row in group
            )
            combined[f"{label}_share_given_reject"] = (
                numerator / reject if reject else math.nan
            )
        output.append(combined)
    return output


if __name__ == "__main__":
    stability = []
    for phase in ("seed1", "seed2"):
        stability.extend(
            read_tsv(
                PROJECT_ROOT / "results" / f"omnibus_interpretability_{phase}_20260813.tsv"
            )
        )
    write_tsv(
        PROJECT_ROOT / "results" / "omnibus_interpretability_combined_20260813.tsv",
        combine_summary_rows(
            stability, ("design", "scenario", "strength", "n_perm")
        ),
    )

    target = []
    for phase in ("seed1", "seed2"):
        target.extend(
            read_tsv(
                PROJECT_ROOT / "results" / f"omnibus_target_attribution_{phase}_20260813.tsv"
            )
        )
    combined_target = combine_summary_rows(
        target, ("design", "scenario", "strength", "n_perm")
    )
    for row in combined_target:
        if row["scenario"] == "node_salience_sign_rewired":
            row["expected_component"] = "profile"
            row["winner_expected_rate"] = row["winner_profile_rate"]
        elif row["scenario"] == "shared_dyadic_geometry":
            row["expected_component"] = "mantel"
            row["winner_expected_rate"] = 1.0 - float(row["winner_profile_rate"])
        else:
            row["expected_component"] = "none"
    write_tsv(
        PROJECT_ROOT / "results" / "omnibus_target_attribution_combined_20260813.tsv",
        combined_target,
    )
