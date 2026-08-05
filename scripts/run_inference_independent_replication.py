"""Independent-seed replication of the newest inference-boundary findings."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import (
    within_block_permutation_indices,
    write_tsv,
)
from scripts.run_design_respecting_permutation import make_stratified_pair
from scripts.run_discrete_degeneracy_validation import make_boundary_pair
from scripts.run_local_salience_power import make_local_salience_pair
from scripts.run_robust_cdelta_grid import wilson


def _p_value(sx: np.ndarray, sy: np.ndarray, indices: np.ndarray) -> float:
    denominator = float(sx.mean() * sy.mean())
    observed = float(np.mean(sx * sy) / denominator)
    statistics = (sy[indices] @ sx) / sx.size / denominator
    return (int(np.sum(statistics >= observed)) + 1) / (indices.shape[0] + 1)


def run(
    *, repetitions: int = 3000, n_perm: int = 499, seed: int = 20260910
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    summaries: dict[tuple[str, str], dict[str, int]] = {
        ("block_conditional_null", "unrestricted"): {"reject": 0, "determined": 0},
        ("block_conditional_null", "within_block"): {"reject": 0, "determined": 0},
        ("bernoulli50_null", "unrestricted"): {"reject": 0, "determined": 0},
        ("local_clean_rho20", "unrestricted"): {"reject": 0, "determined": 0},
        ("local_contam_rho70", "unrestricted"): {"reject": 0, "determined": 0},
    }
    for _ in range(repetitions):
        x, y, blocks = make_stratified_pair(
            rng, 80, 4, 4.0, "conditional_null", 0.0
        )
        sx, sy = huber_reference_profile(x), huber_reference_profile(y)
        for scheme, indices in (
            (
                "unrestricted",
                np.asarray([rng.permutation(80) for _ in range(n_perm)]),
            ),
            (
                "within_block",
                within_block_permutation_indices(blocks, n_perm, rng),
            ),
        ):
            cell = summaries[("block_conditional_null", scheme)]
            cell["determined"] += 1
            cell["reject"] += int(_p_value(sx, sy, indices) < 0.05)

        x, y = make_boundary_pair(rng, 40, "null_bernoulli_50")
        sx, sy = huber_reference_profile(x), huber_reference_profile(y)
        cell = summaries[("bernoulli50_null", "unrestricted")]
        if sx.mean() > 0.0 and sy.mean() > 0.0:
            cell["determined"] += 1
            indices = np.asarray([rng.permutation(40) for _ in range(n_perm)])
            cell["reject"] += int(_p_value(sx, sy, indices) < 0.05)

        for family, rho, contamination, n in (
            ("local_clean_rho20", 0.2, 0.0, 80),
            ("local_contam_rho70", 0.7, 0.05, 320),
        ):
            x, y = make_local_salience_pair(rng, n, rho, contamination)
            sx, sy = huber_reference_profile(x), huber_reference_profile(y)
            cell = summaries[(family, "unrestricted")]
            cell["determined"] += 1
            indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
            cell["reject"] += int(_p_value(sx, sy, indices) < 0.05)

    rows: list[dict[str, float | int | str]] = []
    for (family, scheme), values in summaries.items():
        reject, determined = values["reject"], values["determined"]
        low, high = wilson(reject, repetitions)
        rows.append(
            {
                "family": family,
                "permutation_scheme": scheme,
                "method": "huber_primary",
                "repetitions": repetitions,
                "n_perm": n_perm,
                "determined_rate": determined / repetitions,
                "rejection_rate_all": reject / repetitions,
                "wilson_low_all": low,
                "wilson_high_all": high,
            }
        )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "inference_independent_replication_20260805.tsv",
        run(),
    )
