"""Separate node-sign and dyadic-margin skew mechanisms in a 2x2 study."""

from __future__ import annotations

import csv
from math import sqrt
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_signal_strength_surface_20260809 import COARSE_WEIGHTS
from scripts.run_skew_mixed_path_derivatives_20260810 import (
    combine_skew_power_runs,
    derivative_batch,
    estimate_skew_crossovers,
    run_skew_power_grid,
    summarize,
)


def _configuration(
    name: str,
    *,
    node_skew: bool,
    dyad_skew: bool,
) -> dict[str, float | str]:
    return {
        "name": name,
        "node_rho": 0.55,
        "dyad_rho": 0.70,
        "weight": 0.216,
        "positive_sign_probability": 0.80 if node_skew else 0.50,
        "node_sigma": 0.70,
        "dyad_sigma": 0.80,
        "dyad_distribution": "lognormal" if dyad_skew else "gaussian",
        "node_skew": int(node_skew),
        "dyad_skew": int(dyad_skew),
    }


FACTORIAL_CONFIGURATIONS = (
    _configuration("balanced_node_gaussian_dyad", node_skew=False, dyad_skew=False),
    _configuration("imbalanced_node_gaussian_dyad", node_skew=True, dyad_skew=False),
    _configuration("balanced_node_lognormal_dyad", node_skew=False, dyad_skew=True),
    _configuration("imbalanced_node_lognormal_dyad", node_skew=True, dyad_skew=True),
)


MAGNITUDE_SKEW_CONFIGURATIONS = (
    {
        **_configuration(
            "balanced_magnitude_skew_gaussian_dyad",
            node_skew=False,
            dyad_skew=False,
        ),
        "positive_radius_multiplier": 0.80,
        "negative_radius_multiplier": 1.0,
        "magnitude_skew": 1,
    },
    {
        **_configuration(
            "balanced_magnitude_skew_lognormal_dyad",
            node_skew=False,
            dyad_skew=True,
        ),
        "positive_radius_multiplier": 0.80,
        "negative_radius_multiplier": 1.0,
        "magnitude_skew": 1,
    },
)


def factorial_contrasts(values: dict[tuple[int, int], float]) -> dict[str, float]:
    c00, c10 = values[(0, 0)], values[(1, 0)]
    c01, c11 = values[(0, 1)], values[(1, 1)]
    return {
        "balanced_gaussian_cell": c00,
        "node_skew_main_effect": ((c10 + c11) - (c00 + c01)) / 2.0,
        "dyad_skew_main_effect": ((c01 + c11) - (c00 + c10)) / 2.0,
        "node_by_dyad_interaction": c11 - c10 - c01 + c00,
        "joint_skew_cell": c11,
    }


def signed_lognormal_skewness(
    positive_probability: float,
    sigma: float,
    positive_multiplier: float = 1.0,
    negative_multiplier: float = 1.0,
) -> float:
    raw_1 = np.exp(0.5 * sigma**2) * (
        positive_probability * positive_multiplier
        - (1.0 - positive_probability) * negative_multiplier
    )
    raw_2 = np.exp(2.0 * sigma**2) * (
        positive_probability * positive_multiplier**2
        + (1.0 - positive_probability) * negative_multiplier**2
    )
    raw_3 = np.exp(4.5 * sigma**2) * (
        positive_probability * positive_multiplier**3
        - (1.0 - positive_probability) * negative_multiplier**3
    )
    variance = raw_2 - raw_1**2
    central_3 = raw_3 - 3.0 * raw_1 * raw_2 + 2.0 * raw_1**3
    return float(central_3 / variance**1.5)


def make_marginal_skewness_rows() -> list[dict[str, float | str]]:
    rows = []
    for configuration in (*FACTORIAL_CONFIGURATIONS, *MAGNITUDE_SKEW_CONFIGURATIONS):
        dyad_distribution = str(configuration["dyad_distribution"])
        dyad_sigma = float(configuration["dyad_sigma"])
        dyad_skewness = (
            0.0
            if dyad_distribution == "gaussian"
            else float(
                (np.exp(dyad_sigma**2) + 2.0)
                * sqrt(np.exp(dyad_sigma**2) - 1.0)
            )
        )
        rows.append(
            {
                "configuration": str(configuration["name"]),
                "node_marginal_skewness": signed_lognormal_skewness(
                    float(configuration["positive_sign_probability"]),
                    float(configuration["node_sigma"]),
                    float(configuration.get("positive_radius_multiplier", 1.0)),
                    float(configuration.get("negative_radius_multiplier", 1.0)),
                ),
                "dyad_marginal_skewness": dyad_skewness,
                "positive_sign_probability": float(configuration["positive_sign_probability"]),
            }
        )
    return rows


def _configuration_key(name: str) -> tuple[int, int]:
    for configuration in FACTORIAL_CONFIGURATIONS:
        if str(configuration["name"]) == name:
            return int(configuration["node_skew"]), int(configuration["dyad_skew"])
    raise ValueError(name)


def make_contrast_rows(
    population_rows: list[dict[str, float | int | str]],
    crossover_rows: list[dict[str, float | int | str]],
) -> list[dict[str, float | str]]:
    output = []
    preferred = [row for row in population_rows if float(row["epsilon"]) == 0.0005]
    for method in ("profile_correlation", "cdelta_star", "mantel"):
        selected = [row for row in preferred if str(row["method"]) == method]
        for metric in (
            "full_pathwise_slope",
            "mad_indirect_effect_component",
            "total_location_effect_component",
        ):
            values = {
                _configuration_key(str(row["configuration"])): float(row[metric])
                for row in selected
            }
            contrasts = factorial_contrasts(values)
            for contrast, estimate in contrasts.items():
                output.append(
                    {
                        "source": "population_derivative",
                        "method": method,
                        "metric": metric,
                        "contrast": contrast,
                        "estimate": estimate,
                    }
                )
    crossover_values = {
        _configuration_key(str(row["configuration"])): float(row["crossover_estimate"])
        for row in crossover_rows
    }
    for contrast, estimate in factorial_contrasts(crossover_values).items():
        output.append(
            {
                "source": "finite_sample_power",
                "method": "profile_minus_mantel",
                "metric": "crossover_estimate",
                "contrast": contrast,
                "estimate": estimate,
            }
        )
    return output


def run_population_factorial() -> tuple[
    list[dict[str, float | int | str]],
    list[dict[str, float | int | str]],
    list[dict[str, float | int | str]],
]:
    seed_outputs = []
    for phase, seed in (("seed1", 20261110), ("seed2", 20261111)):
        rng = np.random.default_rng(seed)
        raw = []
        for configuration in FACTORIAL_CONFIGURATIONS:
            for batch in range(6):
                for row in derivative_batch(
                    rng,
                    250_000,
                    configuration,
                    epsilons=(0.0005, 0.001),
                ):
                    raw.append({"seed": seed, "batch": batch, **row})
        seed_outputs.append(raw)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mechanism_population_{phase}_20260811.tsv",
            summarize(raw, phase),
        )
    combined_raw = [row for rows in seed_outputs for row in rows]
    combined = summarize(combined_raw, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_population_combined_20260811.tsv",
        combined,
    )
    return seed_outputs[0], seed_outputs[1], combined


def _local_weights_from_coarse(
    coarse_crossovers: list[dict[str, float | int | str]],
) -> dict[str, tuple[float, ...]]:
    output = {}
    for row in coarse_crossovers:
        low = float(row["bracket_low"])
        high = float(row["bracket_high"])
        if not np.isfinite(low) or not np.isfinite(high):
            raise ValueError("coarse grid did not bracket a factorial crossover")
        start = max(0.0, low - 0.075)
        stop = min(1.0, high + 0.075)
        count = int(round((stop - start) / 0.025))
        output[str(row["configuration"])] = tuple(
            round(start + 0.025 * index, 3) for index in range(count + 1)
        )
    return output


def run_power_factorial() -> tuple[
    list[dict[str, float | int | str]],
    list[dict[str, float | int | str]],
]:
    coarse = run_skew_power_grid(
        COARSE_WEIGHTS,
        repetitions=250,
        n_perm=199,
        seed=20261120,
        phase="coarse",
        configurations=FACTORIAL_CONFIGURATIONS,
    )
    coarse_crossovers = estimate_skew_crossovers(coarse, "coarse")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_power_coarse_20260811.tsv",
        coarse,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_power_coarse_crossovers_20260811.tsv",
        coarse_crossovers,
    )
    weights = _local_weights_from_coarse(coarse_crossovers)
    runs = []
    for phase_index, phase in enumerate(("local_seed1", "local_seed2")):
        phase_rows = []
        for configuration_index, configuration in enumerate(FACTORIAL_CONFIGURATIONS):
            name = str(configuration["name"])
            phase_rows.extend(
                run_skew_power_grid(
                    weights[name],
                    repetitions=600,
                    n_perm=199,
                    seed=20261121 + 100 * phase_index + configuration_index,
                    phase=phase,
                    configurations=(configuration,),
                )
            )
        runs.append(phase_rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mechanism_power_{phase}_20260811.tsv",
            phase_rows,
        )
    combined = combine_skew_power_runs(tuple(runs))
    crossovers = estimate_skew_crossovers(combined, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_power_combined_20260811.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_power_crossovers_20260811.tsv",
        crossovers,
    )
    return combined, crossovers


def run_magnitude_skew_controls() -> tuple[
    list[dict[str, float | int | str]],
    list[dict[str, float | int | str]],
]:
    population_raw = []
    for seed in (20261130, 20261131):
        rng = np.random.default_rng(seed)
        for configuration in MAGNITUDE_SKEW_CONFIGURATIONS:
            for batch in range(6):
                for row in derivative_batch(
                    rng,
                    250_000,
                    configuration,
                    epsilons=(0.0005, 0.001),
                ):
                    population_raw.append({"seed": seed, "batch": batch, **row})
    population = summarize(population_raw, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_population_20260811.tsv",
        population,
    )

    coarse = run_skew_power_grid(
        COARSE_WEIGHTS,
        repetitions=250,
        n_perm=199,
        seed=20261132,
        phase="coarse",
        configurations=MAGNITUDE_SKEW_CONFIGURATIONS,
    )
    coarse_crossovers = estimate_skew_crossovers(coarse, "coarse")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_coarse_20260811.tsv",
        coarse,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_coarse_crossovers_20260811.tsv",
        coarse_crossovers,
    )
    weights = _local_weights_from_coarse(coarse_crossovers)
    runs = []
    for phase_index, phase in enumerate(("local_seed1", "local_seed2")):
        phase_rows = []
        for configuration_index, configuration in enumerate(MAGNITUDE_SKEW_CONFIGURATIONS):
            name = str(configuration["name"])
            phase_rows.extend(
                run_skew_power_grid(
                    weights[name],
                    repetitions=600,
                    n_perm=199,
                    seed=20261133 + 100 * phase_index + configuration_index,
                    phase=phase,
                    configurations=(configuration,),
                )
            )
        runs.append(phase_rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mechanism_magnitude_power_{phase}_20260811.tsv",
            phase_rows,
        )
    extension_weights = tuple(np.round(np.arange(0.20, 0.401, 0.025), 3))
    for phase_index, phase in enumerate(("extension_seed1", "extension_seed2")):
        rows = run_skew_power_grid(
            extension_weights,
            repetitions=600,
            n_perm=199,
            seed=20261135 + 100 * phase_index,
            phase=phase,
            configurations=(MAGNITUDE_SKEW_CONFIGURATIONS[1],),
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mechanism_magnitude_power_{phase}_20260811.tsv",
            rows,
        )
    combined = combine_skew_power_runs(tuple(runs))
    crossovers = estimate_skew_crossovers(combined, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_combined_20260811.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_crossovers_20260811.tsv",
        crossovers,
    )
    return population, crossovers


def continue_magnitude_extension() -> list[dict[str, float | int | str]]:
    def read_rows(phase: str) -> list[dict[str, str]]:
        with (
            PROJECT_ROOT
            / "results"
            / f"skew_mechanism_magnitude_power_{phase}_20260811.tsv"
        ).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle, delimiter="\t"))

    runs: list[list[dict[str, float | int | str]]] = [
        read_rows(phase)  # type: ignore[list-item]
        for phase in ("local_seed1", "local_seed2")
    ]
    extension_weights = tuple(np.round(np.arange(0.20, 0.401, 0.025), 3))
    for phase_index, phase in enumerate(("extension_seed1", "extension_seed2")):
        rows = run_skew_power_grid(
            extension_weights,
            repetitions=600,
            n_perm=199,
            seed=20261135 + 100 * phase_index,
            phase=phase,
            configurations=(MAGNITUDE_SKEW_CONFIGURATIONS[1],),
        )
        runs.append(rows)
        write_tsv(
            PROJECT_ROOT / "results" / f"skew_mechanism_magnitude_power_{phase}_20260811.tsv",
            rows,
        )
    combined = combine_skew_power_runs(tuple(runs))
    crossovers = estimate_skew_crossovers(combined, "combined")
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_combined_20260811.tsv",
        combined,
    )
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_power_crossovers_20260811.tsv",
        crossovers,
    )
    return crossovers


def make_magnitude_comparison_rows(
    factorial_crossovers: list[dict[str, float | int | str]],
    magnitude_crossovers: list[dict[str, float | int | str]],
) -> list[dict[str, float | str]]:
    values = {
        str(row["configuration"]): float(row["crossover_estimate"])
        for row in [*factorial_crossovers, *magnitude_crossovers]
    }
    output = []
    for dyad in ("gaussian", "lognormal"):
        balanced = values[f"balanced_node_{dyad}_dyad"]
        prevalence = values[f"imbalanced_node_{dyad}_dyad"]
        magnitude = values[f"balanced_magnitude_skew_{dyad}_dyad"]
        output.extend(
            (
                {
                    "dyad_margin": dyad,
                    "comparison": "balanced_reference",
                    "estimate": balanced,
                },
                {
                    "dyad_margin": dyad,
                    "comparison": "sign_prevalence_shift",
                    "estimate": prevalence - balanced,
                },
                {
                    "dyad_margin": dyad,
                    "comparison": "magnitude_skew_shift",
                    "estimate": magnitude - balanced,
                },
            )
        )
    return output


def run() -> None:
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_marginal_skewness_20260811.tsv",
        make_marginal_skewness_rows(),
    )
    _, _, population = run_population_factorial()
    _, crossovers = run_power_factorial()
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_factorial_contrasts_20260811.tsv",
        make_contrast_rows(population, crossovers),
    )
    _, magnitude_crossovers = run_magnitude_skew_controls()
    write_tsv(
        PROJECT_ROOT / "results" / "skew_mechanism_magnitude_comparisons_20260811.tsv",
        make_magnitude_comparison_rows(crossovers, magnitude_crossovers),
    )


if __name__ == "__main__":
    run()
