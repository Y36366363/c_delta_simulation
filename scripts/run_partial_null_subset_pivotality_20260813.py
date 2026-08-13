"""Stress-test partial nulls and subset pivotality for standardized maxT.

The component permutation tests share one label-randomization null.  The
models below therefore target weaker, statistic-specific zero-effect nulls:
zero population profile correlation or zero population Mantel correlation.
They diagnose, rather than assume, whether the null component remains pivotal
when the other component is non-null.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_application_node_decomposition_20260812 import _component_statistics
from scripts.run_node_dyad_mixture_20260808 import _fast_within_block_indices
from scripts.run_robust_cdelta_grid import wilson


RESULTS_DIR = PROJECT_ROOT / "results"
ALPHA = 0.05


def _raw_components(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    sx = huber_reference_profile(x)
    sy = huber_reference_profile(y)
    profile = float(np.corrcoef(sx, sy)[0, 1])
    upper = np.triu_indices(x.size, 1)
    dx = np.abs(x[:, None] - x[None, :])[upper]
    dy = np.abs(y[:, None] - y[None, :])[upper]
    return profile, float(np.corrcoef(dx, dy)[0, 1])


def make_profile_null_mantel_alt(
    rng: np.random.Generator, *, size: int = 60
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Independent radii but a shared balanced sign skeleton.

    The population Huber centres are zero and the two population radial
    profiles are independent, whereas the shared sign partition supplies a
    dyadic-distance signal.  Radii are not duplicated, avoiding pseudo-
    replication in the finite-sample diagnostic.
    """
    if size % 2:
        raise ValueError("size must be even for an exactly balanced sign skeleton")
    rx = np.exp(0.65 * rng.normal(size=size))
    ry = np.exp(0.65 * rng.normal(size=size))
    signs = np.concatenate((-np.ones(size // 2), np.ones(size // 2)))
    rng.shuffle(signs)
    x = signs * rx
    y = signs * ry
    return x, y, np.zeros(x.size, dtype=int)


def make_profile_matched_global_null(
    rng: np.random.Generator, *, size: int = 60
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x, y, blocks = make_profile_null_mantel_alt(rng, size=size)
    return x, rng.permutation(y), blocks


_MAGNITUDES = np.linspace(0.8, 1.2, 60)
_X_SIGNS = np.asarray(
    [1.0 if char == "+" else -1.0 for char in
     "-++++++-++++++----+-++-++++-------++---+++-++--++----+-+----"]
)
_NEGATIVE_SIGNS = np.asarray(
    [1.0 if char == "+" else -1.0 for char in
     "+--+++---+--++++---++++-+-+--+-+-++--++-++----+-+---++--+-++"]
)
_X_TEMPLATE = _MAGNITUDES * _X_SIGNS
_NEGATIVE_GEOMETRY = _MAGNITUDES * _NEGATIVE_SIGNS


def make_mantel_null_profile_alt(
    rng: np.random.Generator,
    *,
    mixing: float,
    noise_sd: float = 0.03,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Near-zero Mantel effect with a retained robust-radius profile signal."""
    x = _X_TEMPLATE + noise_sd * rng.normal(size=_X_TEMPLATE.size)
    y = (
        (1.0 - mixing) * _NEGATIVE_GEOMETRY
        + mixing * _X_TEMPLATE
        + noise_sd * rng.normal(size=_X_TEMPLATE.size)
    )
    order = rng.permutation(_X_TEMPLATE.size)
    return x[order], y[order], np.zeros(_X_TEMPLATE.size, dtype=int)


def make_mantel_matched_global_null(
    rng: np.random.Generator,
    *,
    mixing: float,
    noise_sd: float = 0.03,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x, y, blocks = make_mantel_null_profile_alt(
        rng, mixing=mixing, noise_sd=noise_sd
    )
    return x, rng.permutation(y), blocks


def calibrate_mantel_null(
    *, seed: int, repetitions: int = 20_000, noise_sd: float = 0.03
) -> dict[str, float]:
    """Common-random-number bisection for E[Mantel] = 0."""
    rng = np.random.default_rng(seed)
    noise_x = noise_sd * rng.normal(size=(repetitions, _X_TEMPLATE.size))
    noise_y = noise_sd * rng.normal(size=(repetitions, _X_TEMPLATE.size))
    upper_indices = np.triu_indices(_X_TEMPLATE.size, 1)

    def mean_effect(mixing: float) -> float:
        values = []
        for start in range(0, repetitions, 250):
            stop = min(start + 250, repetitions)
            x = _X_TEMPLATE[None, :] + noise_x[start:stop]
            y = (
                (1.0 - mixing) * _NEGATIVE_GEOMETRY[None, :]
                + mixing * _X_TEMPLATE[None, :]
                + noise_y[start:stop]
            )
            dx = np.abs(x[:, :, None] - x[:, None, :])[
                :, upper_indices[0], upper_indices[1]
            ]
            dy = np.abs(y[:, :, None] - y[:, None, :])[
                :, upper_indices[0], upper_indices[1]
            ]
            centered_dx = dx - np.mean(dx, axis=1, keepdims=True)
            centered_dy = dy - np.mean(dy, axis=1, keepdims=True)
            values.extend(
                np.sum(centered_dx * centered_dy, axis=1)
                / np.sqrt(
                    np.sum(centered_dx**2, axis=1)
                    * np.sum(centered_dy**2, axis=1)
                )
            )
        return float(np.mean(values))

    lower, upper = 0.0, 0.10
    lower_effect = mean_effect(lower)
    upper_effect = mean_effect(upper)
    if not lower_effect < 0.0 < upper_effect:
        raise RuntimeError("Mantel calibration interval does not bracket zero")
    for _ in range(16):
        middle = (lower + upper) / 2.0
        middle_effect = mean_effect(middle)
        if middle_effect < 0.0:
            lower = middle
        else:
            upper = middle
    mixing = (lower + upper) / 2.0
    mantel_effect = mean_effect(mixing)
    profile_values = []
    for index in range(min(repetitions, 2_000)):
        y = (
            (1.0 - mixing) * _NEGATIVE_GEOMETRY
            + mixing * _X_TEMPLATE
            + noise_y[index]
        )
        profile_values.append(
            np.corrcoef(
                huber_reference_profile(_X_TEMPLATE + noise_x[index]),
                huber_reference_profile(y),
            )[0, 1]
        )
    profile_effect = float(np.mean(profile_values))
    return {
        "mixing": mixing,
        "mean_mantel_effect": mantel_effect,
        "mean_profile_effect": profile_effect,
        "calibration_repetitions": repetitions,
        "noise_sd": noise_sd,
    }


def _orbit_diagnostics(
    global_observed: np.ndarray, global_permuted: np.ndarray
) -> dict[str, float]:
    orbit = np.vstack((global_observed, global_permuted))
    z = (orbit - np.mean(orbit, axis=0)) / np.std(orbit, axis=0)
    max_reference = np.max(z[1:], axis=1)
    return {
        "profile_z": float(z[0, 0]),
        "mantel_z": float(z[0, 1]),
        "max_critical_95": float(np.quantile(max_reference, 0.95, method="higher")),
        "reference_z_correlation": float(np.corrcoef(z[1:, 0], z[1:, 1])[0, 1]),
    }


def _max_t_outcomes(
    global_observed: np.ndarray, global_permuted: np.ndarray
) -> dict[str, float]:
    """The fixed-component and standardized-max portion of the main rule."""
    n_perm = global_permuted.shape[0]
    fixed = (1.0 + np.sum(global_permuted >= global_observed, axis=0)) / (
        n_perm + 1.0
    )
    orbit = np.vstack((global_observed, global_permuted))
    z = (orbit - np.mean(orbit, axis=0)) / np.std(orbit, axis=0)
    max_reference = np.max(z[1:], axis=1)
    adjusted = np.asarray(
        [
            (1.0 + np.sum(max_reference >= z[0, component])) / (n_perm + 1.0)
            for component in range(2)
        ]
    )
    return {
        "profile_p": float(fixed[0]),
        "mantel_p": float(fixed[1]),
        "adjusted_profile_p": float(adjusted[0]),
        "adjusted_mantel_p": float(adjusted[1]),
        "standardized_max_p": float(np.min(adjusted)),
    }


def simulate_scenario(
    generator,
    *,
    repetitions: int,
    n_perm: int,
    seed: int,
) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    records = []
    for _ in range(repetitions):
        x, y, blocks = generator(rng)
        indices = _fast_within_block_indices(blocks, n_perm, rng)
        components = _component_statistics(x, y, blocks, indices)
        outcomes = _max_t_outcomes(components[0], components[1])
        profile_effect, mantel_effect = _raw_components(x, y)
        record = {
            "profile_effect": profile_effect,
            "mantel_effect": mantel_effect,
            **_orbit_diagnostics(components[0], components[1]),
        }
        record.update(
            {
                key: float(outcomes[key])
                for key in (
                    "profile_p",
                    "mantel_p",
                    "adjusted_profile_p",
                    "adjusted_mantel_p",
                    "standardized_max_p",
                )
            }
        )
        records.append(record)
    return records


def _ks_distance(x: np.ndarray, y: np.ndarray) -> float:
    support = np.sort(np.concatenate((x, y)))
    return float(
        np.max(
            np.abs(
                np.searchsorted(np.sort(x), support, side="right") / x.size
                - np.searchsorted(np.sort(y), support, side="right") / y.size
            )
        )
    )


def summarize_pair(
    global_records: list[dict[str, float]],
    partial_records: list[dict[str, float]],
    *,
    path: str,
    null_component: str,
    repetitions: int,
    n_perm: int,
    phase: str,
) -> list[dict[str, float | int | str]]:
    null_p = f"{null_component}_p"
    adjusted_p = f"adjusted_{null_component}_p"
    null_z = f"{null_component}_z"
    false_component = "mantel" if null_component == "profile" else "profile"
    global_z = np.asarray([row[null_z] for row in global_records])
    partial_z = np.asarray([row[null_z] for row in partial_records])
    ks = _ks_distance(global_z, partial_z)
    rows = []
    for scenario, records in (("global_null", global_records), ("partial_null", partial_records)):
        z = np.asarray([row[null_z] for row in records])
        unadjusted_count = sum(row[null_p] <= ALPHA for row in records)
        adjusted_count = sum(row[adjusted_p] <= ALPHA for row in records)
        unadjusted_ci = wilson(unadjusted_count, repetitions)
        adjusted_ci = wilson(adjusted_count, repetitions)
        rows.append(
            {
                "phase": phase,
                "path": path,
                "scenario": scenario,
                "null_component": null_component,
                "false_component": false_component,
                "repetitions": repetitions,
                "n_perm": n_perm,
                "mean_null_effect": float(np.mean([r[f"{null_component}_effect"] for r in records])),
                "mean_false_effect": float(np.mean([r[f"{false_component}_effect"] for r in records])),
                "mean_null_z": float(np.mean(z)),
                "sd_null_z": float(np.std(z, ddof=1)),
                "null_z_q05": float(np.quantile(z, 0.05)),
                "null_z_q95": float(np.quantile(z, 0.95)),
                "unadjusted_null_rejection": unadjusted_count / repetitions,
                "unadjusted_wilson_low": unadjusted_ci[0],
                "unadjusted_wilson_high": unadjusted_ci[1],
                "adjusted_null_rejection": adjusted_count / repetitions,
                "adjusted_wilson_low": adjusted_ci[0],
                "adjusted_wilson_high": adjusted_ci[1],
                "false_component_rejection": float(
                    np.mean([r[f"{false_component}_p"] <= ALPHA for r in records])
                ),
                "omnibus_rejection": float(
                    np.mean([r["standardized_max_p"] <= ALPHA for r in records])
                ),
                "mean_max_critical_95": float(np.mean([r["max_critical_95"] for r in records])),
                "mean_reference_z_correlation": float(
                    np.mean([r["reference_z_correlation"] for r in records])
                ),
                "ks_null_z_vs_global": 0.0 if scenario == "global_null" else ks,
            }
        )
    return rows


def run_validation(
    *, profile_repetitions: int, mantel_repetitions: int, n_perm: int, seed: int, phase: str
) -> tuple[list[dict[str, float | int | str]], dict[str, float]]:
    calibration = calibrate_mantel_null(
        seed=seed + 1, repetitions=20_000 if phase == "confirmatory" else 4_000
    )
    mixing = calibration["mixing"]
    profile_global = simulate_scenario(
        make_profile_matched_global_null,
        repetitions=profile_repetitions,
        n_perm=n_perm,
        seed=seed + 10,
    )
    profile_partial = simulate_scenario(
        make_profile_null_mantel_alt,
        repetitions=profile_repetitions,
        n_perm=n_perm,
        seed=seed + 20,
    )
    mantel_global = simulate_scenario(
        lambda rng: make_mantel_matched_global_null(rng, mixing=mixing),
        repetitions=mantel_repetitions,
        n_perm=n_perm,
        seed=seed + 30,
    )
    mantel_partial = simulate_scenario(
        lambda rng: make_mantel_null_profile_alt(rng, mixing=mixing),
        repetitions=mantel_repetitions,
        n_perm=n_perm,
        seed=seed + 40,
    )
    rows = summarize_pair(
        profile_global,
        profile_partial,
        path="profile_null_mantel_alt",
        null_component="profile",
        repetitions=profile_repetitions,
        n_perm=n_perm,
        phase=phase,
    )
    rows.extend(
        summarize_pair(
            mantel_global,
            mantel_partial,
            path="mantel_null_profile_alt",
            null_component="mantel",
            repetitions=mantel_repetitions,
            n_perm=n_perm,
            phase=phase,
        )
    )
    return rows, calibration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "confirmatory"), default="pilot")
    args = parser.parse_args()
    if args.phase == "pilot":
        settings = dict(profile_repetitions=120, mantel_repetitions=300, n_perm=199, seed=2026081301)
    else:
        settings = dict(profile_repetitions=500, mantel_repetitions=500, n_perm=499, seed=2026081302)
    rows, calibration = run_validation(phase=args.phase, **settings)
    RESULTS_DIR.mkdir(exist_ok=True)
    write_tsv(RESULTS_DIR / f"partial_null_subset_pivotality_{args.phase}_20260813.tsv", rows)
    write_tsv(
        RESULTS_DIR / f"partial_null_calibration_{args.phase}_20260813.tsv",
        [{"phase": args.phase, **calibration}],
    )
    for row in rows:
        print(row)
    print({"calibration": calibration})


if __name__ == "__main__":
    main()
