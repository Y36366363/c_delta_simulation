"""Exploratory multivariate extensions of the robust-reference profile."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import common_permutation_pvalues, write_tsv
from scripts.run_robust_cdelta_grid import wilson


def original_multivariate_l2(z: np.ndarray) -> np.ndarray:
    differences = z[:, None, :] - z[None, :, :]
    squared = np.sum(differences**2, axis=2)
    mask = ~np.eye(z.shape[0], dtype=bool)
    return np.sqrt(squared[mask].reshape(z.shape[0], z.shape[0] - 1).mean(axis=1))


def spatial_median(z: np.ndarray, tolerance: float = 1e-10) -> np.ndarray:
    location = np.median(z, axis=0)
    for _ in range(200):
        distances = np.linalg.norm(z - location, axis=1)
        if np.any(distances < tolerance):
            candidate = z[int(np.argmin(distances))]
            nonzero = distances >= tolerance
            residual_direction = np.sum(
                (z[nonzero] - candidate) / distances[nonzero, None], axis=0
            )
            if np.linalg.norm(residual_direction) <= np.sum(~nonzero):
                return candidate.copy()
            distances = np.maximum(distances, tolerance)
        weights = 1.0 / np.maximum(distances, tolerance)
        updated = np.sum(weights[:, None] * z, axis=0) / np.sum(weights)
        if np.linalg.norm(updated - location) < tolerance:
            return updated
        location = updated
    return location


def spatial_median_profile(z: np.ndarray) -> np.ndarray:
    location = spatial_median(z)
    radii = np.linalg.norm(z - location, axis=1)
    scale = float(np.median(radii))
    if scale == 0.0:
        scale = float(np.mean(radii))
    return radii / scale if scale > 0.0 else np.zeros(z.shape[0])


def coordinate_huber_profile(z: np.ndarray) -> np.ndarray:
    coordinate_scores = np.column_stack(
        [huber_reference_profile(z[:, column]) for column in range(z.shape[1])]
    )
    return np.linalg.norm(coordinate_scores, axis=1)


def profiles(z: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "original_multivariate_l2": original_multivariate_l2(z),
        "coordinate_huber": coordinate_huber_profile(z),
        "spatial_median_radius": spatial_median_profile(z),
    }


def _directions(rng: np.random.Generator, n: int, dimension: int) -> np.ndarray:
    values = rng.normal(size=(n, dimension))
    return values / np.linalg.norm(values, axis=1, keepdims=True)


def make_scenario(
    name: str, n: int, dimension: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    if name == "null_normal":
        return rng.normal(size=(n, dimension)), rng.normal(size=(n, dimension))
    if name == "diffuse_radial":
        radii = rng.lognormal(0.0, 0.45, size=n)
        x = _directions(rng, n, dimension) * radii[:, None]
        y_radii = np.maximum(0.05, radii + rng.normal(0.0, 0.18, size=n))
        y = _directions(rng, n, dimension) * y_radii[:, None]
        return x, y
    background = "normal" if name != "t3_matched" else "t3"
    if background == "normal":
        x = rng.normal(size=(n, dimension))
        y = rng.normal(size=(n, dimension))
    else:
        x = rng.standard_t(3, size=(n, dimension))
        y = rng.standard_t(3, size=(n, dimension))
    matched = rng.choice(n, size=max(1, round(0.05 * n)), replace=False)
    x[matched] += 7.0 * _directions(rng, len(matched), dimension)
    y[matched] += 7.0 * _directions(rng, len(matched), dimension)
    if name == "unmatched_masking":
        available = np.setdiff1d(np.arange(n), matched)
        ix, iy = rng.choice(available, size=2, replace=False)
        x[ix] += 20.0 * _directions(rng, 1, dimension)[0]
        y[iy] += 20.0 * _directions(rng, 1, dimension)[0]
    return x, y


def rotation_diagnostic(seed: int = 20260813) -> list[dict[str, float | str]]:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(80, 5))
    z[0] += 12.0 * _directions(rng, 1, 5)[0]
    q, _ = np.linalg.qr(rng.normal(size=(5, 5)))
    rotated = z @ q
    rows = []
    for method in profiles(z):
        before, after = profiles(z)[method], profiles(rotated)[method]
        rows.append(
            {
                "method": method,
                "maximum_absolute_rotation_error": float(np.max(np.abs(before - after))),
                "profile_correlation_after_rotation": float(np.corrcoef(before, after)[0, 1]),
            }
        )
    return rows


def run(
    *, repetitions: int = 1500, n_perm: int = 499, seed: int = 20260814
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int | str]] = []
    scenarios = ("null_normal", "matched_radial", "diffuse_radial", "t3_matched", "unmatched_masking")
    for n in (40, 80):
        for dimension in (1, 2, 5, 10):
            for scenario in scenarios:
                summary = {method: 0 for method in profiles(rng.normal(size=(n, dimension)))}
                for _ in range(repetitions):
                    x, y = make_scenario(scenario, n, dimension, rng)
                    indices = np.asarray([rng.permutation(n) for _ in range(n_perm)])
                    outcomes = common_permutation_pvalues(profiles(x), profiles(y), indices)
                    for method, (p_value, _, _) in outcomes.items():
                        summary[method] += int(p_value < 0.05)
                for method, reject in summary.items():
                    low, high = wilson(reject, repetitions)
                    rows.append(
                        {
                            "n": n,
                            "dimension": dimension,
                            "scenario": scenario,
                            "method": method,
                            "repetitions": repetitions,
                            "n_perm": n_perm,
                            "rejection_rate": reject / repetitions,
                            "wilson_low": low,
                            "wilson_high": high,
                        }
                    )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "multivariate_rotation_diagnostic_20260804.tsv",
        rotation_diagnostic(),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "multivariate_robust_pilot_20260804.tsv",
        run(),
    )
