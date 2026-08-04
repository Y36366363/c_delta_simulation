"""Independent validation of Huber c=2 and cap=6 as a joint candidate."""

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


METHODS = {
    "huber_c1.345": {"huber_c": 1.345, "cap": None},
    "huber_c2": {"huber_c": 2.0, "cap": None},
    "huber_c1.345_cap6": {"huber_c": 1.345, "cap": 6.0},
    "huber_c2_cap6": {"huber_c": 2.0, "cap": 6.0},
}


def _profiles(z: np.ndarray) -> dict[str, np.ndarray]:
    return {
        method: huber_reference_profile(z, **parameters)
        for method, parameters in METHODS.items()
    }


def _scenario(
    name: str, n: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    if name.startswith("diffuse_noise_"):
        return diffuse_scenario(n, float(name.rsplit("_", 1)[1]), rng)
    return make_scenario(name, n, rng)


def run(
    *, repetitions: int = 4000, n_perm: int = 999, seed: int = 20260825
) -> list[dict[str, float | int | str]]:
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
    rows: list[dict[str, float | int | str]] = []
    for n in (20, 40, 80, 160):
        for scenario in scenarios:
            counts = {method: 0 for method in METHODS}
            for _ in range(repetitions):
                x, y = _scenario(scenario, n, rng)
                indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                outcomes = common_permutation_pvalues(_profiles(x), _profiles(y), indices)
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
                        "rejections": reject,
                        "rejection_rate": reject / repetitions,
                        "wilson_low": low,
                        "wilson_high": high,
                    }
                )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "joint_candidate_validation_20260805.tsv",
        run(),
    )
