"""Expanded cross-validation of cap 6 and neighbouring cap values."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import divergence_vector, huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import wilson


METHODS = {
    "original_l2": lambda z: divergence_vector(z, kind="l2"),
    "uncapped": lambda z: huber_reference_profile(z),
    "cap_5.5": lambda z: huber_reference_profile(z, cap=5.5),
    "cap_6": lambda z: huber_reference_profile(z, cap=6.0),
    "cap_6.5": lambda z: huber_reference_profile(z, cap=6.5),
}


def _background(
    rng: np.random.Generator, n: int, kind: str
) -> tuple[np.ndarray, np.ndarray]:
    if kind == "normal":
        return rng.normal(size=n), rng.normal(size=n)
    if kind == "t2":
        return rng.standard_t(2, n), rng.standard_t(2, n)
    if kind == "t3":
        return rng.standard_t(3, n), rng.standard_t(3, n)
    raise ValueError(kind)


def _signal_count(n: int, mode: str) -> int:
    if mode == "fixed1":
        return 1
    if mode == "fraction5":
        return max(1, round(0.05 * n))
    raise ValueError(mode)


def null_contamination(
    rng: np.random.Generator,
    n: int,
    fraction: float,
    magnitude: float,
) -> tuple[np.ndarray, np.ndarray]:
    x, y = _background(rng, n, "normal")
    k = max(1, round(fraction * n))
    x[rng.choice(n, k, replace=False)] += magnitude
    y[rng.choice(n, k, replace=False)] += magnitude
    return x, y


def matched_signal(
    rng: np.random.Generator,
    n: int,
    mode: str,
    signal_magnitude: float,
    background: str,
) -> tuple[np.ndarray, np.ndarray]:
    x, y = _background(rng, n, background)
    indices = rng.choice(n, _signal_count(n, mode), replace=False)
    x[indices] += signal_magnitude
    y[indices] += signal_magnitude
    return x, y


def masked_signal(
    rng: np.random.Generator,
    n: int,
    mode: str,
    signal_magnitude: float,
    contaminant_magnitude: float,
    background: str,
) -> tuple[np.ndarray, np.ndarray]:
    x, y = matched_signal(rng, n, mode, signal_magnitude, background)
    ix, iy = rng.choice(n, 2, replace=False)
    x[ix] += contaminant_magnitude
    y[iy] += contaminant_magnitude
    return x, y


def run_condition(
    *,
    family: str,
    n: int,
    parameters: dict[str, float | str],
    repetitions: int,
    n_perm: int,
    rng: np.random.Generator,
) -> list[dict[str, float | int | str]]:
    counts = {method: 0 for method in METHODS}
    for _ in range(repetitions):
        if family == "null_contamination":
            x, y = null_contamination(
                rng, n, float(parameters["fraction"]), float(parameters["contaminant_magnitude"])
            )
        elif family == "matched_core":
            x, y = matched_signal(
                rng,
                n,
                str(parameters["signal_mode"]),
                float(parameters["signal_magnitude"]),
                str(parameters["background"]),
            )
        elif family == "masked_signal":
            x, y = masked_signal(
                rng,
                n,
                str(parameters["signal_mode"]),
                float(parameters["signal_magnitude"]),
                float(parameters["contaminant_magnitude"]),
                str(parameters["background"]),
            )
        else:
            raise ValueError(family)
        indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
        outcomes = common_permutation_pvalues(
            {method: fn(x) for method, fn in METHODS.items()},
            {method: fn(y) for method, fn in METHODS.items()},
            indices,
        )
        for method, (p_value, _, _) in outcomes.items():
            counts[method] += int(p_value < 0.05)
    rows: list[dict[str, float | int | str]] = []
    for method, reject in counts.items():
        low, high = wilson(reject, repetitions)
        row: dict[str, float | int | str] = {
            "family": family,
            "n": n,
            "method": method,
            "repetitions": repetitions,
            "n_perm": n_perm,
            "rejection_rate": reject / repetitions,
            "wilson_low": low,
            "wilson_high": high,
        }
        row.update(parameters)
        rows.append(row)
    return rows


def run(
    *, repetitions: int = 1000, n_perm: int = 499, seed: int = 20260827
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    for n in (20, 40, 80, 160):
        for fraction in (0.01, 0.05, 0.10):
            for contaminant_magnitude in (10.0, 20.0, 50.0):
                rows.extend(
                    run_condition(
                        family="null_contamination",
                        n=n,
                        parameters={
                            "fraction": fraction,
                            "contaminant_magnitude": contaminant_magnitude,
                            "signal_mode": "",
                            "signal_magnitude": "",
                            "background": "normal",
                        },
                        repetitions=repetitions,
                        n_perm=n_perm,
                        rng=rng,
                    )
                )
        for signal_mode in ("fixed1", "fraction5"):
            for signal_magnitude in (4.0, 6.0, 8.0):
                for background in ("normal", "t2"):
                    rows.extend(
                        run_condition(
                            family="matched_core",
                            n=n,
                            parameters={
                                "fraction": "",
                                "contaminant_magnitude": "",
                                "signal_mode": signal_mode,
                                "signal_magnitude": signal_magnitude,
                                "background": background,
                            },
                            repetitions=repetitions,
                            n_perm=n_perm,
                            rng=rng,
                        )
                    )
        for signal_mode in ("fixed1", "fraction5"):
            for signal_magnitude in (4.0, 6.0):
                for contaminant_magnitude in (10.0, 20.0, 50.0):
                    for background in ("normal", "t3"):
                        rows.extend(
                            run_condition(
                                family="masked_signal",
                                n=n,
                                parameters={
                                    "fraction": "",
                                    "contaminant_magnitude": contaminant_magnitude,
                                    "signal_mode": signal_mode,
                                    "signal_magnitude": signal_magnitude,
                                    "background": background,
                                },
                                repetitions=repetitions,
                                n_perm=n_perm,
                                rng=rng,
                            )
                        )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "cap6_expanded_cross_validation_20260805.tsv",
        run(),
    )
