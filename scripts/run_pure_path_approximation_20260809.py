"""Population approximations for the pure node and pure dyadic paths."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


LOG_RADIUS_SIGMA = 0.55


def absolute_normal_correlation(rho: float) -> float:
    """Correlation of absolute values from a standard bivariate normal."""
    term = np.sqrt(1.0 - rho**2) + rho * np.arcsin(rho)
    return float((2.0 / np.pi * term - 2.0 / np.pi) / (1.0 - 2.0 / np.pi))


def dyad_path_cdelta_star(rho: float) -> float:
    """Population ratio E|X||Y| / (E|X| E|Y|) for bivariate normal data."""
    return float(np.sqrt(1.0 - rho**2) + rho * np.arcsin(rho))


def node_path_cdelta_star(rho: float, sigma: float = LOG_RADIUS_SIGMA) -> float:
    """Population ratio for correlated lognormal radii."""
    return float(np.exp(sigma**2 * rho))


def node_radius_correlation(rho: float, sigma: float = LOG_RADIUS_SIGMA) -> float:
    numerator = np.exp(sigma**2 * rho) - 1.0
    denominator = np.exp(sigma**2) - 1.0
    return float(numerator / denominator)


def _batch_estimates(
    rng: np.random.Generator,
    path: str,
    rho: float,
    batch_size: int,
) -> tuple[float, float, float]:
    common_1 = rng.normal(size=batch_size)
    noise_1 = rng.normal(size=batch_size)
    common_2 = rng.normal(size=batch_size)
    noise_2 = rng.normal(size=batch_size)
    if path == "dyad":
        x1 = common_1
        y1 = rho * common_1 + np.sqrt(1.0 - rho**2) * noise_1
        x2 = common_2
        y2 = rho * common_2 + np.sqrt(1.0 - rho**2) * noise_2
    elif path == "node":
        radius_x1 = np.exp(LOG_RADIUS_SIGMA * common_1)
        radius_y1 = np.exp(
            LOG_RADIUS_SIGMA
            * (rho * common_1 + np.sqrt(1.0 - rho**2) * noise_1)
        )
        radius_x2 = np.exp(LOG_RADIUS_SIGMA * common_2)
        radius_y2 = np.exp(
            LOG_RADIUS_SIGMA
            * (rho * common_2 + np.sqrt(1.0 - rho**2) * noise_2)
        )
        x1 = rng.choice((-1.0, 1.0), size=batch_size) * radius_x1
        y1 = rng.choice((-1.0, 1.0), size=batch_size) * radius_y1
        x2 = rng.choice((-1.0, 1.0), size=batch_size) * radius_x2
        y2 = rng.choice((-1.0, 1.0), size=batch_size) * radius_y2
    else:
        raise ValueError(path)
    radius_x, radius_y = np.abs(x1), np.abs(y1)
    cdelta = float(np.mean(radius_x * radius_y) / (np.mean(radius_x) * np.mean(radius_y)))
    profile_correlation = float(np.corrcoef(radius_x, radius_y)[0, 1])
    mantel_correlation = float(
        np.corrcoef(np.abs(x1 - x2), np.abs(y1 - y2))[0, 1]
    )
    return cdelta, profile_correlation, mantel_correlation


def run(
    *,
    n_batches: int = 20,
    batch_size: int = 50_000,
    seed: int = 20261040,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for path, strengths in (
        ("node", (0.35, 0.55, 0.65, 0.75)),
        ("dyad", (0.30, 0.45, 0.65, 0.80)),
    ):
        for rho in strengths:
            estimates = np.asarray(
                [
                    _batch_estimates(rng, path, rho, batch_size)
                    for _ in range(n_batches)
                ]
            )
            if path == "node":
                analytic_cdelta = node_path_cdelta_star(rho)
                analytic_profile = node_radius_correlation(rho)
                analytic_mantel = np.nan
            else:
                analytic_cdelta = dyad_path_cdelta_star(rho)
                analytic_profile = absolute_normal_correlation(rho)
                analytic_mantel = analytic_profile
            means = np.mean(estimates, axis=0)
            standard_errors = np.std(estimates, axis=0, ddof=1) / np.sqrt(n_batches)
            rows.append(
                {
                    "path": path,
                    "latent_correlation": rho,
                    "log_radius_sigma": LOG_RADIUS_SIGMA if path == "node" else np.nan,
                    "analytic_cdelta_star": analytic_cdelta,
                    "analytic_profile_correlation": analytic_profile,
                    "analytic_mantel_correlation": analytic_mantel,
                    "mc_cdelta_star": float(means[0]),
                    "mc_profile_correlation": float(means[1]),
                    "mc_mantel_correlation": float(means[2]),
                    "mc_cdelta_standard_error": float(standard_errors[0]),
                    "mc_profile_standard_error": float(standard_errors[1]),
                    "mc_mantel_standard_error": float(standard_errors[2]),
                    "profile_minus_mantel_correlation": float(means[1] - means[2]),
                    "cdelta_absolute_formula_error": abs(float(means[0]) - analytic_cdelta),
                    "profile_absolute_formula_error": abs(float(means[1]) - analytic_profile),
                    "mantel_absolute_formula_error": (
                        abs(float(means[2]) - analytic_mantel)
                        if np.isfinite(analytic_mantel)
                        else np.nan
                    ),
                    "n_batches": n_batches,
                    "batch_size": batch_size,
                    "total_dyads": n_batches * batch_size,
                }
            )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "pure_path_population_approximation_20260809.tsv",
        run(),
    )
