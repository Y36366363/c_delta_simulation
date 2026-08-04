"""Locate the diffuse-power versus robust-centre tradeoff."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_diffuse_and_decision_rule_pilot import diffuse_scenario
from scripts.run_robust_cdelta_grid import make_scenario, wilson


HUBER_CS = (1.345, 2.0, 3.0, 4.0)


def _tail_trigger(z: np.ndarray, threshold: float = 6.0) -> bool:
    median = float(np.median(z))
    scale = 1.4826 * float(np.median(np.abs(z - median)))
    if scale == 0.0:
        scale = float(np.mean(np.abs(z - median)))
    if scale == 0.0:
        return False
    return bool(np.max(np.abs(z - median) / scale) > threshold)


def adaptive_profile(z: np.ndarray) -> tuple[np.ndarray, bool]:
    triggered = _tail_trigger(z)
    huber_c = 1.345 if triggered else 4.0
    return huber_reference_profile(z, huber_c=huber_c), triggered


def _profiles(z: np.ndarray) -> tuple[dict[str, np.ndarray], bool]:
    adaptive, triggered = adaptive_profile(z)
    profiles = {
        f"huber_c{c:g}": huber_reference_profile(z, huber_c=c) for c in HUBER_CS
    }
    profiles["adaptive_c1.345_or_4"] = adaptive
    return profiles, triggered


def _scenario(
    name: str, n: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    if name.startswith("diffuse_noise_"):
        noise = float(name.rsplit("_", 1)[1])
        return diffuse_scenario(n, noise, rng)
    return make_scenario(name, n, rng)


def run(
    *, repetitions: int = 2500, n_perm: int = 499, seed: int = 20260824
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    rng = np.random.default_rng(seed)
    scenarios = (
        "null_clean",
        "null_contam_p10",
        "matched_p01_m8",
        "t2_matched",
        "bimodal_aligned",
        "unmatched_masking",
        "diffuse_noise_0.15",
        "diffuse_noise_0.30",
        "diffuse_noise_0.50",
    )
    methods = (*(f"huber_c{c:g}" for c in HUBER_CS), "adaptive_c1.345_or_4")
    rows: list[dict[str, float | int | str]] = []
    trigger_rows: list[dict[str, float | int | str]] = []
    for n in (12, 20, 40, 80):
        for scenario in scenarios:
            counts = {method: 0 for method in methods}
            x_triggers = 0
            y_triggers = 0
            for _ in range(repetitions):
                x, y = _scenario(scenario, n, rng)
                px, x_triggered = _profiles(x)
                py, y_triggered = _profiles(y)
                x_triggers += int(x_triggered)
                y_triggers += int(y_triggered)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(px, py, indices)
                for method, (p_value, _, _) in outcomes.items():
                    counts[method] += int(p_value < 0.05)
            for method, reject in counts.items():
                low, high = wilson(reject, repetitions)
                rows.append(
                    {
                        "n": n,
                        "scenario": scenario,
                        "method": method,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
            trigger_rows.append(
                {
                    "n": n,
                    "scenario": scenario,
                    "repetitions": repetitions,
                    "x_trigger_rate": x_triggers / repetitions,
                    "y_trigger_rate": y_triggers / repetitions,
                    "either_margin_trigger_rate_upper_bound": min(
                        1.0, (x_triggers + y_triggers) / repetitions
                    ),
                }
            )
    return rows, trigger_rows


def influence_path() -> list[dict[str, float | str]]:
    ordinary = np.linspace(-2.0, 2.0, 41)
    rows: list[dict[str, float | str]] = []
    for magnitude in (4.0, 8.0, 16.0, 64.0, 256.0, 1024.0):
        sample = np.append(ordinary, magnitude)
        methods, triggered = _profiles(sample)
        for method, scores in methods.items():
            rows.append(
                {
                    "magnitude": magnitude,
                    "method": method,
                    "adaptive_triggered": int(triggered) if method.startswith("adaptive") else "",
                    "ordinary_mean_score": float(np.mean(scores[:-1])),
                    "remote_score": float(scores[-1]),
                }
            )
    return rows


if __name__ == "__main__":
    simulation, triggers = run()
    write_tsv(
        PROJECT_ROOT / "results" / "center_diffuse_tradeoff_20260805.tsv",
        simulation,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "center_adaptive_trigger_20260805.tsv",
        triggers,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "center_influence_path_20260805.tsv",
        influence_path(),
    )
