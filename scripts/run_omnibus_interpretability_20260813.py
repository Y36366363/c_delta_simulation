"""Test component attribution and permutation stability of standardized max."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_application_node_decomposition_20260812 import (
    _component_statistics,
    adaptive_permutation_outcomes,
)
from scripts.run_node_dyad_mixture_20260808 import _fast_within_block_indices
from scripts.run_robust_cdelta_grid import wilson
from scripts.run_building_target_separation_20260808 import make_building_pair
from scripts.run_unequal_building_adaptive_validation_20260813 import (
    ROOM_DESIGNS,
    aggregation_weights,
    make_covariate_building_pair,
)


PERMUTATION_COUNTS = (199, 499, 999)
DESIGNS = ("moderately_unequal", "severely_unequal")
ALTERNATIVES = ("radial_node", "dyadic", "mixed_covariate")
STRENGTHS = (0.6, 1.0, 1.4)


def attribution_label(outcomes: dict[str, float | str], alpha: float = 0.05) -> str:
    profile = float(outcomes["adjusted_profile_p"]) < alpha
    mantel = float(outcomes["adjusted_mantel_p"]) < alpha
    if profile and mantel:
        return "both"
    if profile:
        return "profile_only"
    if mantel:
        return "mantel_only"
    return "unresolved"


def summarize_cell(
    records: list[dict[str, float | str]],
    *,
    phase: str,
    design: str,
    scenario: str,
    strength: float,
    n_perm: int,
) -> dict[str, float | int | str]:
    repetitions = len(records)
    reject = sum(float(row["standardized_max_p"]) < 0.05 for row in records)
    profile_reject = sum(float(row["profile_p"]) < 0.05 for row in records)
    mantel_reject = sum(float(row["mantel_p"]) < 0.05 for row in records)
    adjusted_profile = sum(float(row["adjusted_profile_p"]) < 0.05 for row in records)
    adjusted_mantel = sum(float(row["adjusted_mantel_p"]) < 0.05 for row in records)
    labels = [attribution_label(row) for row in records]
    rejected_labels = [
        label
        for row, label in zip(records, labels)
        if float(row["standardized_max_p"]) < 0.05
    ]
    low, high = wilson(int(reject), repetitions)
    expected = (
        "profile" if scenario == "radial_node" else "mantel" if scenario == "dyadic" else "none"
    )
    return {
        "phase": phase,
        "design": design,
        "scenario": scenario,
        "strength": strength,
        "n_perm": n_perm,
        "repetitions": repetitions,
        "omnibus_rejection_rate": reject / repetitions,
        "wilson_low": low,
        "wilson_high": high,
        "profile_rejection_rate": profile_reject / repetitions,
        "mantel_rejection_rate": mantel_reject / repetitions,
        "best_component_power": max(profile_reject, mantel_reject) / repetitions,
        "omnibus_regret": max(profile_reject, mantel_reject) / repetitions
        - reject / repetitions,
        "adjusted_profile_rejection_rate": adjusted_profile / repetitions,
        "adjusted_mantel_rejection_rate": adjusted_mantel / repetitions,
        "winner_profile_rate": sum(row["standardized_winner"] == "profile" for row in records)
        / repetitions,
        "winner_expected_rate": (
            sum(row["standardized_winner"] == expected for row in records) / repetitions
            if expected != "none"
            else np.nan
        ),
        "mean_profile_z": float(np.mean([float(row["standardized_profile_z"]) for row in records])),
        "mean_mantel_z": float(np.mean([float(row["standardized_mantel_z"]) for row in records])),
        "profile_only_rate": labels.count("profile_only") / repetitions,
        "mantel_only_rate": labels.count("mantel_only") / repetitions,
        "both_rate": labels.count("both") / repetitions,
        "unresolved_rate": labels.count("unresolved") / repetitions,
        "profile_only_share_given_reject": rejected_labels.count("profile_only") / reject if reject else np.nan,
        "mantel_only_share_given_reject": rejected_labels.count("mantel_only") / reject if reject else np.nan,
        "both_share_given_reject": rejected_labels.count("both") / reject if reject else np.nan,
        "unresolved_share_given_reject": rejected_labels.count("unresolved") / reject if reject else np.nan,
        "winner_agreement_with_999": float(
            np.mean([float(row["winner_agreement_with_999"]) for row in records])
        ),
        "decision_agreement_with_999": float(
            np.mean([float(row["decision_agreement_with_999"]) for row in records])
        ),
        "attribution_agreement_with_999": float(
            np.mean([float(row["attribution_agreement_with_999"]) for row in records])
        ),
    }


def run_interpretability(
    *, repetitions: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    output = []
    cells = [("conditional_null", 0.0)] + [
        (scenario, strength) for scenario in ALTERNATIVES for strength in STRENGTHS
    ]
    for design in DESIGNS:
        room_counts = ROOM_DESIGNS[design]
        weights = aggregation_weights(room_counts, "building_equal")
        for scenario, strength in cells:
            by_count = {n_perm: [] for n_perm in PERMUTATION_COUNTS}
            for _ in range(repetitions):
                x, y, blocks, _ = make_covariate_building_pair(
                    rng,
                    room_counts,
                    scenario,
                    signal_multiplier=(1.0 if scenario == "conditional_null" else strength),
                )
                indices = _fast_within_block_indices(blocks, max(PERMUTATION_COUNTS), rng)
                (
                    global_observed,
                    global_permuted,
                    block_observed,
                    block_permuted,
                ) = _component_statistics(x, y, blocks, indices)
                outcomes = {}
                for n_perm in PERMUTATION_COUNTS:
                    outcomes[n_perm] = adaptive_permutation_outcomes(
                        global_observed,
                        global_permuted[:n_perm],
                        block_observed,
                        block_permuted[:n_perm],
                        temperature=0.0,
                        block_weights=weights,
                    )
                reference = outcomes[max(PERMUTATION_COUNTS)]
                reference_decision = float(reference["standardized_max_p"]) < 0.05
                reference_attribution = attribution_label(reference)
                for n_perm, result in outcomes.items():
                    result = dict(result)
                    result["winner_agreement_with_999"] = float(
                        result["standardized_winner"] == reference["standardized_winner"]
                    )
                    result["decision_agreement_with_999"] = float(
                        (float(result["standardized_max_p"]) < 0.05) == reference_decision
                    )
                    result["attribution_agreement_with_999"] = float(
                        attribution_label(result) == reference_attribution
                    )
                    by_count[n_perm].append(result)
            for n_perm, records in by_count.items():
                output.append(
                    summarize_cell(
                        records,
                        phase=phase,
                        design=design,
                        scenario=scenario,
                        strength=strength,
                        n_perm=n_perm,
                    )
                )
    return output


def run_target_attribution(
    *, repetitions: int, n_perm: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    """Focused attribution on the original construct-separating alternatives."""
    rng = np.random.default_rng(seed)
    rows = []
    for scenario in (
        "conditional_null",
        "node_salience_sign_rewired",
        "shared_dyadic_geometry",
    ):
        records = []
        for _ in range(repetitions):
            x, y, blocks = make_building_pair(rng, scenario)
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            outcomes = adaptive_permutation_outcomes(
                *_component_statistics(x, y, blocks, indices), temperature=0.0
            )
            outcomes = dict(outcomes)
            outcomes["winner_agreement_with_999"] = 1.0
            outcomes["decision_agreement_with_999"] = 1.0
            outcomes["attribution_agreement_with_999"] = 1.0
            records.append(outcomes)
        row = summarize_cell(
            records,
            phase=phase,
            design="four_building_target_separation",
            scenario=scenario,
            strength=1.0,
            n_perm=n_perm,
        )
        row["expected_component"] = (
            "profile"
            if scenario == "node_salience_sign_rewired"
            else "mantel" if scenario == "shared_dyadic_geometry" else "none"
        )
        if scenario == "node_salience_sign_rewired":
            row["winner_expected_rate"] = row["winner_profile_rate"]
        elif scenario == "shared_dyadic_geometry":
            row["winner_expected_rate"] = 1.0 - float(row["winner_profile_rate"])
        rows.append(row)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--section", choices=("all", "stability", "target"), default="all"
    )
    args = parser.parse_args()
    if args.section in ("all", "stability"):
        for phase, seed in (("seed1", 20261321), ("seed2", 20261322)):
            write_tsv(
                PROJECT_ROOT / "results" / f"omnibus_interpretability_{phase}_20260813.tsv",
                run_interpretability(repetitions=50, seed=seed, phase=phase),
            )
    if args.section in ("all", "target"):
        for phase, seed in (("seed1", 20261331), ("seed2", 20261332)):
            write_tsv(
                PROJECT_ROOT / "results" / f"omnibus_target_attribution_{phase}_20260813.tsv",
                run_target_attribution(
                    repetitions=300, n_perm=499, seed=seed, phase=phase
                ),
            )
