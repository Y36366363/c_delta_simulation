"""Refine the bounded-profile cap using a core-power constrained loss."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import make_scenario, wilson


CAPS = (4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0)
SCENARIOS = (
    "null_clean",
    "null_contam_p10",
    "matched_p01_m8",
    "t2_matched",
    "diffuse_aligned",
    "bimodal_aligned",
    "unmatched_masking",
)
CORE_SCENARIOS = (
    "matched_p01_m8",
    "t2_matched",
    "diffuse_aligned",
    "bimodal_aligned",
)


def _profiles(z: np.ndarray, caps: tuple[float, ...] = CAPS) -> dict[str, np.ndarray]:
    result = {"uncapped": huber_reference_profile(z)}
    result.update(
        {f"cap_{cap:g}": huber_reference_profile(z, cap=cap) for cap in caps}
    )
    return result


def run_grid(
    *,
    sample_sizes: tuple[int, ...],
    repetitions: int,
    n_perm: int,
    seed: int,
    caps: tuple[float, ...] = CAPS,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    methods = ("uncapped", *(f"cap_{cap:g}" for cap in caps))
    rows: list[dict[str, float | int | str]] = []
    for n in sample_sizes:
        for scenario in SCENARIOS:
            counts = {method: 0 for method in methods}
            for _ in range(repetitions):
                x, y = make_scenario(scenario, n, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(
                    _profiles(x, caps), _profiles(y, caps), indices
                )
                for method, (p_value, _, _) in outcomes.items():
                    counts[method] += int(p_value < 0.05)
            for method, reject in counts.items():
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "seed": seed,
                        "n": n,
                        "scenario": scenario,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejections": reject,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
    return rows


def loss_table(training: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[int, str, str], list[float]] = {}
    for row in training:
        key = (int(row["n"]), str(row["scenario"]), str(row["method"]))
        grouped.setdefault(key, []).append(float(row["rejection_rate"]))
    pooled = {key: float(np.mean(values)) for key, values in grouped.items()}
    sample_sizes = sorted({key[0] for key in pooled})
    rows: list[dict[str, object]] = []
    for cap in CAPS:
        method = f"cap_{cap:g}"
        null_rates = [
            pooled[(n, scenario, method)]
            for n in sample_sizes
            for scenario in ("null_clean", "null_contam_p10")
        ]
        core_losses = [
            max(0.0, pooled[(n, scenario, "uncapped")] - pooled[(n, scenario, method)])
            for n in sample_sizes
            for scenario in CORE_SCENARIOS
        ]
        masking_gains = [
            pooled[(n, "unmatched_masking", method)]
            - pooled[(n, "unmatched_masking", "uncapped")]
            for n in sample_sizes
        ]
        null_max = max(null_rates)
        worst_core_loss = max(core_losses)
        feasible = null_max <= 0.065 and worst_core_loss <= 0.03
        rows.append(
            {
                "cap": cap,
                "maximum_null_rejection": null_max,
                "worst_absolute_core_power_loss": worst_core_loss,
                "mean_core_power_loss": float(np.mean(core_losses)),
                "minimum_masking_gain": min(masking_gains),
                "mean_masking_gain": float(np.mean(masking_gains)),
                "feasible": int(feasible),
            }
        )
    feasible_rows = [row for row in rows if row["feasible"]]
    if not feasible_rows:
        raise RuntimeError("no cap satisfies the core-power constrained loss")
    selected = max(feasible_rows, key=lambda row: float(row["mean_masking_gain"]))
    for row in rows:
        row["selected"] = int(row is selected)
    return rows


def tolerance_map(losses: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for tolerance in (0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.10):
        feasible = [
            row
            for row in losses
            if float(row["maximum_null_rejection"]) <= 0.065
            and float(row["worst_absolute_core_power_loss"]) <= tolerance
        ]
        selected = (
            max(feasible, key=lambda row: float(row["mean_masking_gain"]))
            if feasible
            else None
        )
        rows.append(
            {
                "allowed_worst_core_power_loss": tolerance,
                "selected_cap": float(selected["cap"]) if selected else "",
                "selected_worst_core_power_loss": (
                    float(selected["worst_absolute_core_power_loss"])
                    if selected
                    else ""
                ),
                "selected_mean_masking_gain": (
                    float(selected["mean_masking_gain"]) if selected else ""
                ),
            }
        )
    return rows


if __name__ == "__main__":
    training: list[dict[str, object]] = []
    for seed in (20260820, 20260821, 20260822):
        training.extend(
            run_grid(
                sample_sizes=(20, 40, 80),
                repetitions=1200,
                n_perm=499,
                seed=seed,
            )
        )
    losses = loss_table(training)
    selected_cap = float(next(row["cap"] for row in losses if row["selected"]))
    evaluation_caps = tuple(sorted({selected_cap, 6.0}))
    evaluation = run_grid(
        sample_sizes=(20, 40, 80, 160),
        repetitions=5000,
        n_perm=999,
        seed=20260823,
        caps=evaluation_caps,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_loss_refinement_training_20260805.tsv",
        training,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_loss_refinement_pareto_20260805.tsv",
        losses,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_loss_tolerance_map_20260805.tsv",
        tolerance_map(losses),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "cap_loss_refinement_evaluation_20260805.tsv",
        evaluation,
    )
    print(f"selected_cap={selected_cap:g}")
