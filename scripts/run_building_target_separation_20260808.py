"""Separate node-salience and dyadic-geometry targets in one building design."""

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


def _pearson(x: np.ndarray, y: np.ndarray) -> float:
    centered_x = x - np.mean(x)
    centered_y = y - np.mean(y)
    denominator = float(np.linalg.norm(centered_x) * np.linalg.norm(centered_y))
    return float(centered_x @ centered_y / denominator)


def _profile_statistics(
    sx: np.ndarray,
    sy: np.ndarray,
    indices: np.ndarray,
) -> dict[str, tuple[float, float]]:
    n_perm, n = indices.shape
    ratio_denominator = float(np.mean(sx) * np.mean(sy))
    ratio_observed = float(np.mean(sx * sy) / ratio_denominator)
    ratio_permuted = (sy[indices] @ sx) / n / ratio_denominator

    centered_x = sx - np.mean(sx)
    centered_y = sy - np.mean(sy)
    correlation_denominator = float(
        np.linalg.norm(centered_x) * np.linalg.norm(centered_y)
    )
    correlation_observed = float(
        centered_x @ centered_y / correlation_denominator
    )
    correlation_permuted = (
        centered_y[indices] @ centered_x / correlation_denominator
    )
    ratio_p = (1 + int(np.sum(ratio_permuted >= ratio_observed))) / (
        n_perm + 1
    )
    correlation_p = (
        1 + int(np.sum(correlation_permuted >= correlation_observed))
    ) / (n_perm + 1)
    return {
        "ratio": (ratio_observed, ratio_p),
        "correlation": (correlation_observed, correlation_p),
    }


def _distance_upper(values: np.ndarray) -> np.ndarray:
    upper = np.triu_indices(values.size, k=1)
    distances = np.abs(values[:, None] - values[None, :])
    return distances[upper]


def mantel_statistic(x: np.ndarray, y: np.ndarray) -> float:
    return _pearson(_distance_upper(x), _distance_upper(y))


def mantel_test(
    x: np.ndarray,
    y: np.ndarray,
    indices: np.ndarray,
) -> tuple[float, float]:
    upper = np.triu_indices(x.size, k=1)
    dx = np.abs(x[:, None] - x[None, :])[upper]
    dy_matrix = np.abs(y[:, None] - y[None, :])
    mean_dy = float(np.mean(dy_matrix[upper]))
    centered_dx = dx - np.mean(dx)
    centered_dy = dy_matrix[upper] - mean_dy
    denominator = float(
        np.linalg.norm(centered_dx) * np.linalg.norm(centered_dy)
    )
    observed = float(centered_dx @ centered_dy / denominator)
    permuted_dy = dy_matrix[
        indices[:, upper[0]],
        indices[:, upper[1]],
    ]
    statistics = (permuted_dy - mean_dy) @ centered_dx
    statistics = statistics / denominator
    p_value = (1 + int(np.sum(statistics >= observed))) / (indices.shape[0] + 1)
    return observed, p_value


def make_building_pair(
    rng: np.random.Generator,
    scenario: str,
    *,
    n_blocks: int = 4,
    rooms_per_block: int = 12,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    blocks = np.repeat(np.arange(n_blocks), rooms_per_block)
    locations = np.zeros(n_blocks)
    scales = np.geomspace(1.0, 2.5, n_blocks)
    x = np.empty(blocks.size)
    y = np.empty(blocks.size)

    for block in range(n_blocks):
        members = np.flatnonzero(blocks == block)
        location, scale = locations[block], scales[block]
        if scenario == "node_salience_sign_rewired":
            if rooms_per_block % 2:
                raise ValueError("node-salience construction requires an even block size")
            common = rng.normal(size=rooms_per_block // 2)
            radius_x = np.repeat(np.exp(0.55 * common), 2)
            radius_y = np.repeat(
                np.exp(
                    0.55
                    * (
                        0.55 * common
                        + np.sqrt(1.0 - 0.55**2)
                        * rng.normal(size=common.size)
                    )
                ),
                2,
            )
            signs_x = np.tile((1.0, -1.0), rooms_per_block // 2)
            pair_flips = rng.choice((-1.0, 1.0), size=rooms_per_block // 2)
            signs_y = signs_x * np.repeat(pair_flips, 2)
            x[members] = location + scale * signs_x * radius_x
            y[members] = location + scale * signs_y * radius_y
            continue

        if scenario == "shared_dyadic_geometry":
            common = rng.normal(size=rooms_per_block)
            x[members] = location + scale * common
            y[members] = location + scale * (
                0.70 * common
                + np.sqrt(1.0 - 0.70**2) * rng.normal(size=rooms_per_block)
            )
            continue

        x[members] = location + scale * rng.normal(size=rooms_per_block)
        y[members] = location + scale * rng.normal(size=rooms_per_block)
        if scenario == "conditional_null":
            continue
        if scenario == "matched_structural_extreme":
            selected = int(rng.choice(members))
            direction = float(rng.choice((-1.0, 1.0)))
            x[selected] += direction * 7.0 * scale
            y[selected] += direction * 7.0 * scale
            continue
        if scenario == "unmatched_extreme_negative_control":
            selected_x, selected_y = rng.choice(members, size=2, replace=False)
            x[selected_x] += float(rng.choice((-1.0, 1.0))) * 7.0 * scale
            y[selected_y] += float(rng.choice((-1.0, 1.0))) * 7.0 * scale
            continue
        raise ValueError(f"unknown scenario: {scenario}")
    return x, y, blocks


def run_building_simulation(
    *,
    repetitions: int = 800,
    n_perm: int = 399,
    seed: int = 20261008,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    scenarios = (
        "conditional_null",
        "node_salience_sign_rewired",
        "shared_dyadic_geometry",
        "matched_structural_extreme",
        "unmatched_extreme_negative_control",
    )
    rows: list[dict[str, float | int | str]] = []
    for scenario in scenarios:
        schemes = ("unrestricted", "within_building") if scenario == "conditional_null" else ("within_building",)
        summaries = {
            (scheme, method): {"reject": 0, "statistic": [], "p_value": [], "cv_product": []}
            for scheme in schemes
            for method in (
                "original_l2_cdelta",
                "huber_cdelta_star",
                "huber_profile_pearson",
                "huber_cap6_cdelta_star",
                "mantel",
            )
        }
        maximum_huber_p_difference = 0.0
        for _ in range(repetitions):
            x, y, blocks = make_building_pair(rng, scenario)
            profiles = {
                "original_l2": (divergence_vector(x), divergence_vector(y)),
                "huber": (huber_reference_profile(x), huber_reference_profile(y)),
                "huber_cap6": (
                    huber_reference_profile(x, cap=6.0),
                    huber_reference_profile(y, cap=6.0),
                ),
            }
            permutation_sets = {}
            if "unrestricted" in schemes:
                permutation_sets["unrestricted"] = np.asarray(
                    [rng.permutation(x.size) for _ in range(n_perm)]
                )
            if "within_building" in schemes:
                permutation_sets["within_building"] = within_block_permutation_indices(
                    blocks, n_perm, rng
                )
            for scheme, indices in permutation_sets.items():
                original = _profile_statistics(*profiles["original_l2"], indices)
                huber = _profile_statistics(*profiles["huber"], indices)
                cap6 = _profile_statistics(*profiles["huber_cap6"], indices)
                mantel_value, mantel_p = mantel_test(x, y, indices)
                outcomes = {
                    "original_l2_cdelta": original["ratio"],
                    "huber_cdelta_star": huber["ratio"],
                    "huber_profile_pearson": huber["correlation"],
                    "huber_cap6_cdelta_star": cap6["ratio"],
                    "mantel": (mantel_value, mantel_p),
                }
                maximum_huber_p_difference = max(
                    maximum_huber_p_difference,
                    abs(huber["ratio"][1] - huber["correlation"][1]),
                )
                cv_product = float(
                    np.std(profiles["huber"][0]) / np.mean(profiles["huber"][0])
                    * np.std(profiles["huber"][1]) / np.mean(profiles["huber"][1])
                )
                for method, (statistic, p_value) in outcomes.items():
                    cell = summaries[(scheme, method)]
                    cell["reject"] += int(p_value < 0.05)
                    cell["statistic"].append(statistic)
                    cell["p_value"].append(p_value)
                    if method in {"huber_cdelta_star", "huber_profile_pearson"}:
                        cell["cv_product"].append(cv_product)
        if maximum_huber_p_difference > 1e-12:
            raise AssertionError("Huber c_delta_star and Pearson p-values diverged")
        for (scheme, method), values in summaries.items():
            reject = int(values["reject"])
            low, high = wilson(reject, repetitions)
            rows.append(
                {
                    "scenario": scenario,
                    "permutation_scheme": scheme,
                    "method": method,
                    "n": 48,
                    "n_blocks": 4,
                    "rooms_per_block": 12,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "rejection_rate": reject / repetitions,
                    "wilson_low": low,
                    "wilson_high": high,
                    "mean_statistic": float(np.mean(values["statistic"])),
                    "median_p_value": float(np.median(values["p_value"])),
                    "mean_huber_cv_product": (
                        float(np.mean(values["cv_product"]))
                        if values["cv_product"]
                        else np.nan
                    ),
                    "maximum_huber_cdelta_pearson_p_difference": maximum_huber_p_difference,
                }
            )
    return rows


def fixed_correlation_cv_grid(
    *,
    target_correlation: float = 0.30,
    sample_sizes: tuple[int, ...] = (100, 500, 2000),
    repetitions: int = 3000,
    seed: int = 20261009,
) -> list[dict[str, float | int]]:
    rng = np.random.default_rng(seed)
    rows: list[dict[str, float | int]] = []
    for sigma_x, sigma_y in (
        (0.25, 0.25),
        (0.50, 0.50),
        (1.00, 1.00),
        (1.50, 1.50),
        (0.50, 1.50),
    ):
        cv_x = float(np.sqrt(np.exp(sigma_x**2) - 1.0))
        cv_y = float(np.sqrt(np.exp(sigma_y**2) - 1.0))
        population_cdelta = float(1.0 + target_correlation * cv_x * cv_y)
        latent_rho = float(np.log(population_cdelta) / (sigma_x * sigma_y))
        if not 0.0 <= latent_rho <= 1.0:
            raise ValueError("requested Pearson correlation is infeasible")
        for n in sample_sizes:
            coefficients, correlations = [], []
            for _ in range(repetitions):
                u = rng.normal(size=n)
                v = latent_rho * u + np.sqrt(1.0 - latent_rho**2) * rng.normal(size=n)
                sx = np.exp(sigma_x * u)
                sy = np.exp(sigma_y * v)
                coefficients.append(
                    float(np.mean(sx * sy) / (np.mean(sx) * np.mean(sy)))
                )
                correlations.append(_pearson(sx, sy))
            rows.append(
                {
                    "target_profile_correlation": target_correlation,
                    "sigma_x": sigma_x,
                    "sigma_y": sigma_y,
                    "latent_gaussian_correlation": latent_rho,
                    "population_cv_x": cv_x,
                    "population_cv_y": cv_y,
                    "population_cv_product": cv_x * cv_y,
                    "population_cdelta_star": population_cdelta,
                    "n": n,
                    "repetitions": repetitions,
                    "mean_sample_profile_correlation": float(
                        np.mean(correlations)
                    ),
                    "mean_sample_cdelta_star": float(np.mean(coefficients)),
                    "sd_sample_cdelta_star": float(np.std(coefficients)),
                    "relative_cdelta_bias": float(
                        np.mean(coefficients) / population_cdelta - 1.0
                    ),
                }
            )
    return rows


if __name__ == "__main__":
    write_tsv(
        PROJECT_ROOT / "results" / "building_target_separation_20260808.tsv",
        run_building_simulation(),
    )
    write_tsv(
        PROJECT_ROOT
        / "results"
        / "building_target_separation_replication_20260808.tsv",
        run_building_simulation(seed=20261018),
    )
    write_tsv(
        PROJECT_ROOT / "results" / "fixed_correlation_cv_weighting_20260808.tsv",
        fixed_correlation_cv_grid(),
    )
