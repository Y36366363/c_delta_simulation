"""Application-oriented node decomposition and adaptive permutation pilot."""

from __future__ import annotations

from math import exp, sqrt
import argparse
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_building_target_separation_20260808 import (
    _distance_upper,
    _pearson,
    _profile_statistics,
    mantel_test,
)
from scripts.run_node_dyad_mixture_20260808 import _fast_within_block_indices
from scripts.run_robust_cdelta_grid import wilson


def _correlated_normals(
    rng: np.random.Generator, size: int, correlation: float
) -> tuple[np.ndarray, np.ndarray]:
    if not -1.0 <= correlation <= 1.0:
        raise ValueError("correlation must lie in [-1, 1]")
    x = rng.normal(size=size)
    y = correlation * x + sqrt(max(0.0, 1.0 - correlation**2)) * rng.normal(
        size=size
    )
    return x, y


def _paired_signs(
    rng: np.random.Generator,
    size: int,
    positive_probability: float,
    agreement_probability: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Sample signs with equal declared margins and declared agreement.

    The discordant cells receive equal mass.  Feasibility requires
    ``agreement_probability >= abs(2 * positive_probability - 1)``.
    """
    if not 0.0 <= positive_probability <= 1.0:
        raise ValueError("positive_probability must lie in [0, 1]")
    disagreement = 1.0 - agreement_probability
    probabilities = np.asarray(
        (
            positive_probability - disagreement / 2.0,
            disagreement / 2.0,
            disagreement / 2.0,
            1.0 - positive_probability - disagreement / 2.0,
        )
    )
    if np.min(probabilities) < -1e-12:
        raise ValueError("positive probability and agreement are incompatible")
    cells = rng.choice(4, size=size, p=np.maximum(probabilities, 0.0))
    signs_x = np.where(np.isin(cells, (0, 1)), 1.0, -1.0)
    signs_y = np.where(np.isin(cells, (0, 2)), 1.0, -1.0)
    return signs_x, signs_y


def make_application_building_pair(
    rng: np.random.Generator,
    *,
    positive_probability: float = 0.50,
    sign_agreement: float = 0.50,
    magnitude_sigma: float = 0.60,
    magnitude_rho: float = 0.00,
    center_sd: float = 0.80,
    center_rho: float = 0.80,
    dyadic_weight: float = 0.00,
    dyadic_rho: float = 0.00,
    n_blocks: int = 6,
    rooms_per_block: int = 10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    """Generate a building model with separately controlled node mechanisms.

    ``sign_agreement`` controls directional agreement of deviations,
    ``magnitude_sigma`` controls radial heterogeneity while ``magnitude_rho``
    controls whether that heterogeneity is shared, and ``center_sd`` controls
    between-building centre offsets.  The latter is a block-level nuisance for
    within-building randomization, even when the offsets correlate by margin.
    """
    if not 0.0 <= sign_agreement <= 1.0:
        raise ValueError("sign_agreement must lie in [0, 1]")
    if magnitude_sigma < 0.0 or center_sd < 0.0:
        raise ValueError("scale parameters must be nonnegative")
    if not 0.0 <= dyadic_weight <= 1.0:
        raise ValueError("dyadic_weight must lie in [0, 1]")

    blocks = np.repeat(np.arange(n_blocks), rooms_per_block)
    block_scale = np.geomspace(1.0, 2.0, n_blocks)
    center_x, center_y = _correlated_normals(rng, n_blocks, center_rho)
    x = np.empty(blocks.size)
    y = np.empty(blocks.size)
    agreements = []
    positive_x = []
    positive_y = []
    log_radii_x = []
    log_radii_y = []
    for block in range(n_blocks):
        members = np.flatnonzero(blocks == block)
        signs_x, signs_y = _paired_signs(
            rng, rooms_per_block, positive_probability, sign_agreement
        )
        matched = signs_x == signs_y
        radius_x, radius_y = _correlated_normals(
            rng, rooms_per_block, magnitude_rho
        )
        # exp(sigma Z) / exp(sigma^2) has unit second moment.  This keeps
        # variance comparable while sigma changes radial heterogeneity.
        node_x = signs_x * np.exp(magnitude_sigma * radius_x) / exp(
            magnitude_sigma**2
        )
        node_y = signs_y * np.exp(magnitude_sigma * radius_y) / exp(
            magnitude_sigma**2
        )
        dyad_x, dyad_y = _correlated_normals(rng, rooms_per_block, dyadic_rho)
        within_x = sqrt(1.0 - dyadic_weight) * node_x + sqrt(
            dyadic_weight
        ) * dyad_x
        within_y = sqrt(1.0 - dyadic_weight) * node_y + sqrt(
            dyadic_weight
        ) * dyad_y
        x[members] = center_sd * center_x[block] + block_scale[block] * within_x
        y[members] = center_sd * center_y[block] + block_scale[block] * within_y
        agreements.extend(matched.tolist())
        positive_x.extend((signs_x > 0.0).tolist())
        positive_y.extend((signs_y > 0.0).tolist())
        log_radii_x.extend((magnitude_sigma * radius_x).tolist())
        log_radii_y.extend((magnitude_sigma * radius_y).tolist())
    diagnostics = {
        "realized_sign_agreement": float(np.mean(agreements)),
        "realized_positive_probability_x": float(np.mean(positive_x)),
        "realized_positive_probability_y": float(np.mean(positive_y)),
        "realized_log_radius_sd_x": float(np.std(log_radii_x)),
        "realized_log_radius_sd_y": float(np.std(log_radii_y)),
        "realized_log_radius_correlation": float(
            np.corrcoef(log_radii_x, log_radii_y)[0, 1]
        ),
        "realized_center_correlation": float(np.corrcoef(center_x, center_y)[0, 1]),
    }
    return x, y, blocks, diagnostics


def _component_statistics(
    x: np.ndarray,
    y: np.ndarray,
    blocks: np.ndarray,
    indices: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return global and blockwise profile/Mantel statistics over an orbit sample."""
    sx = huber_reference_profile(x)
    sy = huber_reference_profile(y)
    profile = _profile_statistics(sx, sy, indices)
    profile_observed = profile["correlation"][0]
    centered_x = sx - np.mean(sx)
    centered_y = sy - np.mean(sy)
    profile_denominator = float(np.linalg.norm(centered_x) * np.linalg.norm(centered_y))
    profile_permuted = centered_y[indices] @ centered_x / profile_denominator

    mantel_observed, _ = mantel_test(x, y, indices)
    upper = np.triu_indices(x.size, k=1)
    dx = np.abs(x[:, None] - x[None, :])[upper]
    dy_matrix = np.abs(y[:, None] - y[None, :])
    centered_dx = dx - np.mean(dx)
    centered_dy = dy_matrix[upper] - np.mean(dy_matrix[upper])
    mantel_denominator = float(np.linalg.norm(centered_dx) * np.linalg.norm(centered_dy))
    mantel_permuted = (
        dy_matrix[indices[:, upper[0]], indices[:, upper[1]]]
        - np.mean(dy_matrix[upper])
    ) @ centered_dx / mantel_denominator

    block_observed = []
    block_permuted = []
    for label in np.unique(blocks):
        members = np.flatnonzero(blocks == label)
        local_indices = indices[:, members]
        local_sx = sx[members]
        local_sy = sy[members]
        centered_local_x = local_sx - np.mean(local_sx)
        centered_local_y = local_sy - np.mean(local_sy)
        profile_scale = float(
            np.linalg.norm(centered_local_x) * np.linalg.norm(centered_local_y)
        )
        local_profile_observed = float(
            centered_local_x @ centered_local_y / profile_scale
        )
        local_profile_permuted = (
            (sy[local_indices] - np.mean(local_sy)) @ centered_local_x / profile_scale
        )

        local_x, local_y = x[members], y[members]
        local_upper = np.triu_indices(members.size, k=1)
        local_dx = np.abs(local_x[:, None] - local_x[None, :])[local_upper]
        local_dy_matrix = np.abs(local_y[:, None] - local_y[None, :])
        centered_local_dx = local_dx - np.mean(local_dx)
        centered_local_dy = local_dy_matrix[local_upper] - np.mean(
            local_dy_matrix[local_upper]
        )
        local_mantel_scale = float(
            np.linalg.norm(centered_local_dx) * np.linalg.norm(centered_local_dy)
        )
        local_mantel_observed = float(
            centered_local_dx @ centered_local_dy / local_mantel_scale
        )
        within_positions = np.searchsorted(members, local_indices)
        local_permuted_dy = local_dy_matrix[
            within_positions[:, local_upper[0]],
            within_positions[:, local_upper[1]],
        ]
        local_mantel_permuted = (
            local_permuted_dy - np.mean(local_dy_matrix[local_upper])
        ) @ centered_local_dx / local_mantel_scale
        block_observed.append((local_profile_observed, local_mantel_observed))
        block_permuted.append(
            np.column_stack((local_profile_permuted, local_mantel_permuted))
        )
    return (
        np.asarray((profile_observed, mantel_observed)),
        np.column_stack((profile_permuted, mantel_permuted)),
        np.asarray(block_observed),
        np.stack(block_permuted, axis=1),
    )


def cross_validated_weight_statistic(
    block_scores: np.ndarray, *, temperature: float = 4.0
) -> tuple[np.ndarray, np.ndarray]:
    """Leave-one-building-out continuous method weighting.

    The returned first array is one statistic per orbit element and the second
    is the mean profile weight.  Input shape is ``(orbit, blocks, 2)``.
    """
    if block_scores.ndim != 3 or block_scores.shape[2] != 2:
        raise ValueError("block_scores must have shape (orbit, blocks, 2)")
    if block_scores.shape[1] < 2 or temperature <= 0.0:
        raise ValueError("at least two blocks and positive temperature are required")
    total = np.sum(block_scores, axis=1, keepdims=True)
    training_mean = (total - block_scores) / (block_scores.shape[1] - 1)
    difference = training_mean[:, :, 0] - training_mean[:, :, 1]
    profile_weight = 1.0 / (1.0 + np.exp(-temperature * difference))
    heldout_score = (
        profile_weight * block_scores[:, :, 0]
        + (1.0 - profile_weight) * block_scores[:, :, 1]
    )
    return np.mean(heldout_score, axis=1), np.mean(profile_weight, axis=1)


def adaptive_permutation_outcomes(
    global_observed: np.ndarray,
    global_permuted: np.ndarray,
    block_observed: np.ndarray,
    block_permuted: np.ndarray,
    *,
    temperature: float = 4.0,
) -> dict[str, float]:
    """Compare fixed, naive, nested-max and LOO-weight permutation rules."""
    n_perm = global_permuted.shape[0]
    fixed_p = [
        (1 + int(np.sum(global_permuted[:, j] >= global_observed[j])))
        / (n_perm + 1)
        for j in range(2)
    ]
    selected = int(global_observed[1] > global_observed[0])
    naive_p = fixed_p[selected]
    max_observed = float(np.max(global_observed))
    max_permuted = np.max(global_permuted, axis=1)
    nested_max_p = (1 + int(np.sum(max_permuted >= max_observed))) / (n_perm + 1)

    observed_cv, observed_weights = cross_validated_weight_statistic(
        block_observed[None, :, :], temperature=temperature
    )
    permuted_cv, permuted_weights = cross_validated_weight_statistic(
        block_permuted, temperature=temperature
    )
    retrained_cv_p = (1 + int(np.sum(permuted_cv >= observed_cv[0]))) / (
        n_perm + 1
    )
    observed_training_total = np.sum(block_observed, axis=0, keepdims=True)
    observed_training = (
        observed_training_total - block_observed
    ) / (block_observed.shape[0] - 1)
    frozen_profile_weight = 1.0 / (
        1.0
        + np.exp(
            -temperature * (observed_training[:, 0] - observed_training[:, 1])
        )
    )
    frozen_permuted = np.mean(
        frozen_profile_weight[None, :] * block_permuted[:, :, 0]
        + (1.0 - frozen_profile_weight[None, :]) * block_permuted[:, :, 1],
        axis=1,
    )
    frozen_cv_p = (1 + int(np.sum(frozen_permuted >= observed_cv[0]))) / (
        n_perm + 1
    )
    return {
        "profile_p": fixed_p[0],
        "mantel_p": fixed_p[1],
        "naive_selected_p": naive_p,
        "nested_max_p": nested_max_p,
        "cv_retrained_p": retrained_cv_p,
        "cv_frozen_p": frozen_cv_p,
        "observed_profile_weight": float(observed_weights[0]),
        "mean_permuted_profile_weight": float(np.mean(permuted_weights)),
    }


def run_decomposition_grid(
    *, repetitions: int, n_perm: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    for positive_probability in (0.50, 0.70):
        for sign_agreement in (0.50, 0.75):
            for magnitude_sigma in (0.35, 0.85):
                for center_sd in (0.0, 1.0):
                    summaries = {
                        method: {"reject": 0, "p": [], "weight": []}
                        for method in (
                            "profile",
                            "mantel",
                            "naive_selected",
                            "nested_max",
                            "cv_retrained",
                            "cv_frozen",
                        )
                    }
                    diagnostics = []
                    for _ in range(repetitions):
                        x, y, blocks, diagnostic = make_application_building_pair(
                            rng,
                            positive_probability=positive_probability,
                            sign_agreement=sign_agreement,
                            magnitude_sigma=magnitude_sigma,
                            magnitude_rho=0.55,
                            center_sd=center_sd,
                            center_rho=0.80,
                            dyadic_weight=0.15,
                            dyadic_rho=0.50,
                        )
                        indices = _fast_within_block_indices(blocks, n_perm, rng)
                        outcomes = adaptive_permutation_outcomes(
                            *_component_statistics(x, y, blocks, indices)
                        )
                        diagnostics.append(diagnostic)
                        for method in summaries:
                            p_value = float(outcomes[f"{method}_p"])
                            summaries[method]["reject"] += int(p_value < 0.05)
                            summaries[method]["p"].append(p_value)
                            summaries[method]["weight"].append(
                                outcomes["observed_profile_weight"]
                            )
                    for method, summary in summaries.items():
                        low, high = wilson(int(summary["reject"]), repetitions)
                        rows.append(
                            {
                                "phase": phase,
                                "positive_probability": positive_probability,
                                "sign_agreement": sign_agreement,
                                "magnitude_sigma": magnitude_sigma,
                                "magnitude_rho": 0.55,
                                "center_sd": center_sd,
                                "center_rho": 0.80,
                                "dyadic_weight": 0.15,
                                "dyadic_rho": 0.50,
                                "method": method,
                                "repetitions": repetitions,
                                "n_perm": n_perm,
                                "rejection_rate": int(summary["reject"])
                                / repetitions,
                                "wilson_low": low,
                                "wilson_high": high,
                                "median_p_value": float(np.median(summary["p"])),
                                "mean_observed_profile_weight": float(
                                    np.mean(summary["weight"])
                                ),
                                "mean_realized_sign_agreement": float(
                                    np.mean(
                                        [
                                            d["realized_sign_agreement"]
                                            for d in diagnostics
                                        ]
                                    )
                                ),
                                "mean_realized_positive_probability": float(
                                    np.mean(
                                        [
                                            (
                                                d["realized_positive_probability_x"]
                                                + d["realized_positive_probability_y"]
                                            )
                                            / 2
                                            for d in diagnostics
                                        ]
                                    )
                                ),
                                "mean_realized_log_radius_sd": float(
                                    np.mean(
                                        [
                                            (
                                                d["realized_log_radius_sd_x"]
                                                + d["realized_log_radius_sd_y"]
                                            )
                                            / 2
                                            for d in diagnostics
                                        ]
                                    )
                                ),
                                "mean_realized_log_radius_correlation": float(
                                    np.mean(
                                        [
                                            d["realized_log_radius_correlation"]
                                            for d in diagnostics
                                        ]
                                    )
                                ),
                                "mean_realized_center_correlation": float(
                                    np.mean(
                                        [
                                            d["realized_center_correlation"]
                                            for d in diagnostics
                                        ]
                                    )
                                ),
                            }
                        )
    return rows


def run_null_calibration(
    *, repetitions: int, n_perm: int, seed: int, phase: str
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    rows = []
    scenarios = (
        {
            "name": "correlated_building_centers",
            "magnitude_sigma": 0.70,
            "center_sd": 1.20,
            "center_rho": 0.85,
            "dyadic_weight": 0.20,
            "n_blocks": 6,
            "rooms_per_block": 10,
        },
        {
            "name": "high_magnitude_heterogeneity",
            "magnitude_sigma": 1.10,
            "center_sd": 0.00,
            "center_rho": 0.00,
            "dyadic_weight": 0.20,
            "n_blocks": 6,
            "rooms_per_block": 10,
        },
        {
            "name": "few_buildings_correlated_centers",
            "magnitude_sigma": 0.70,
            "center_sd": 1.20,
            "center_rho": 0.85,
            "dyadic_weight": 0.20,
            "n_blocks": 3,
            "rooms_per_block": 16,
        },
        {
            "name": "dyad_dominant_independent_null",
            "magnitude_sigma": 0.70,
            "center_sd": 0.50,
            "center_rho": 0.50,
            "dyadic_weight": 0.80,
            "n_blocks": 6,
            "rooms_per_block": 10,
        },
    )
    for scenario in scenarios:
        summaries = {
            method: {"reject": 0, "p": []}
            for method in (
                "profile",
                "mantel",
                "naive_selected",
                "nested_max",
                "cv_retrained",
                "cv_frozen",
            )
        }
        weights = []
        for _ in range(repetitions):
            x, y, blocks, _ = make_application_building_pair(
                rng,
                sign_agreement=0.50,
                magnitude_sigma=float(scenario["magnitude_sigma"]),
                magnitude_rho=0.00,
                center_sd=float(scenario["center_sd"]),
                center_rho=float(scenario["center_rho"]),
                dyadic_weight=float(scenario["dyadic_weight"]),
                dyadic_rho=0.00,
                n_blocks=int(scenario["n_blocks"]),
                rooms_per_block=int(scenario["rooms_per_block"]),
            )
            indices = _fast_within_block_indices(blocks, n_perm, rng)
            outcomes = adaptive_permutation_outcomes(
                *_component_statistics(x, y, blocks, indices)
            )
            weights.append(outcomes["observed_profile_weight"])
            for method, summary in summaries.items():
                p_value = float(outcomes[f"{method}_p"])
                summary["reject"] += int(p_value < 0.05)
                summary["p"].append(p_value)
        for method, summary in summaries.items():
            low, high = wilson(int(summary["reject"]), repetitions)
            rows.append(
                {
                    "phase": phase,
                    "scenario": str(scenario["name"]),
                    "method": method,
                    "n_blocks": int(scenario["n_blocks"]),
                    "rooms_per_block": int(scenario["rooms_per_block"]),
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejection_rate": int(summary["reject"]) / repetitions,
                    "wilson_low": low,
                    "wilson_high": high,
                    "median_p_value": float(np.median(summary["p"])),
                    "mean_observed_profile_weight": float(np.mean(weights)),
                }
            )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--section", choices=("all", "decomposition", "null"), default="all"
    )
    arguments = parser.parse_args()
    if arguments.section in ("all", "decomposition"):
        for phase, seed in (("seed1", 20261201), ("seed2", 20261202)):
            write_tsv(
                PROJECT_ROOT / "results" / f"application_node_decomposition_{phase}_20260812.tsv",
                run_decomposition_grid(
                    repetitions=400, n_perm=199, seed=seed, phase=phase
                ),
            )
    if arguments.section in ("all", "null"):
        for phase, seed in (("seed1", 20261211), ("seed2", 20261212)):
            write_tsv(
                PROJECT_ROOT / "results" / f"adaptive_weight_null_{phase}_20260812.tsv",
                run_null_calibration(
                    repetitions=1000, n_perm=199, seed=seed, phase=phase
                ),
            )
