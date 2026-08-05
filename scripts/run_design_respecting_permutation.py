"""Validate unrestricted and within-block inference for robust c_delta."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import (
    within_block_permutation_indices,
    write_tsv,
)
from scripts.run_robust_cdelta_grid import wilson


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "huber_primary": lambda z: huber_reference_profile(z),
    "huber_cap6": lambda z: huber_reference_profile(z, cap=6.0),
}


def make_stratified_pair(
    rng: np.random.Generator,
    n: int,
    n_blocks: int,
    scale_ratio: float,
    family: str,
    signal_magnitude: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if n % n_blocks:
        raise ValueError("n must be divisible by n_blocks")
    blocks = np.repeat(np.arange(n_blocks), n // n_blocks)
    block_scales = np.geomspace(1.0, scale_ratio, n_blocks)
    scales = block_scales[blocks]
    x = rng.normal(size=n) * scales
    y = rng.normal(size=n) * scales
    if family == "matched_within_block":
        k = max(1, round(0.05 * n))
        selected = rng.choice(n, k, replace=False)
        x[selected] += signal_magnitude * scales[selected]
        y[selected] += signal_magnitude * scales[selected]
    elif family != "conditional_null":
        raise ValueError(family)
    return x, y, blocks


def _permutation_outcomes(
    profiles_x: dict[str, np.ndarray],
    profiles_y: dict[str, np.ndarray],
    indices: np.ndarray,
) -> dict[str, tuple[float, float, float]]:
    outcomes: dict[str, tuple[float, float, float]] = {}
    for method, sx in profiles_x.items():
        sy = profiles_y[method]
        denominator = float(sx.mean() * sy.mean())
        observed = float(np.mean(sx * sy) / denominator)
        statistics = (sy[indices] @ sx) / sx.size / denominator
        p_value = (int(np.sum(statistics >= observed)) + 1) / (indices.shape[0] + 1)
        outcomes[method] = (p_value, observed, float(np.mean(statistics)))
    return outcomes


def run(
    *, repetitions: int = 1500, n_perm: int = 499, seed: int = 20260903
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (40, 80, 160):
        for n_blocks in (2, 4):
            for scale_ratio in (2.0, 4.0):
                settings = [("conditional_null", 0.0)] + [
                    ("matched_within_block", magnitude) for magnitude in (4.0, 6.0)
                ]
                for family, signal_magnitude in settings:
                    summaries = {
                        (scheme, method): {"reject": 0, "observed": [], "reference": []}
                        for scheme in ("unrestricted", "within_block")
                        for method in METHODS
                    }
                    for _ in range(repetitions):
                        x, y, blocks = make_stratified_pair(
                            rng,
                            n,
                            n_blocks,
                            scale_ratio,
                            family,
                            signal_magnitude,
                        )
                        profiles_x = {method: fn(x) for method, fn in METHODS.items()}
                        profiles_y = {method: fn(y) for method, fn in METHODS.items()}
                        permutations = {
                            "unrestricted": np.asarray(
                                [rng.permutation(n) for _ in range(n_perm)]
                            ),
                            "within_block": within_block_permutation_indices(
                                blocks, n_perm, rng
                            ),
                        }
                        for scheme, indices in permutations.items():
                            outcomes = _permutation_outcomes(
                                profiles_x, profiles_y, indices
                            )
                            for method, (p_value, observed, reference) in outcomes.items():
                                cell = summaries[(scheme, method)]
                                cell["reject"] += int(p_value < 0.05)
                                cell["observed"].append(observed)
                                cell["reference"].append(reference)
                    for (scheme, method), values in summaries.items():
                        reject = int(values["reject"])
                        low, high = wilson(reject, repetitions)
                        rows.append(
                            {
                                "family": family,
                                "n": n,
                                "n_blocks": n_blocks,
                                "scale_ratio": scale_ratio,
                                "signal_magnitude": signal_magnitude,
                                "permutation_scheme": scheme,
                                "method": method,
                                "repetitions": repetitions,
                                "n_perm": n_perm,
                                "rejection_rate": reject / repetitions,
                                "wilson_low": low,
                                "wilson_high": high,
                                "mean_observed_cdelta": float(
                                    np.mean(values["observed"])
                                ),
                                "mean_permutation_reference": float(
                                    np.mean(values["reference"])
                                ),
                            }
                        )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "design_respecting_permutation_20260805.tsv",
        run(),
    )
