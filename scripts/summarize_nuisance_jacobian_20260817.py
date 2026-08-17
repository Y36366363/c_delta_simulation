"""Join population nuisance Jacobians to matched-family simulation cells."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np
from scipy.stats import spearmanr


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def fit_logit_model(
    response_probability: np.ndarray,
    repetitions: int,
    predictors: np.ndarray,
) -> tuple[float, float]:
    smoothed = (
        np.asarray(response_probability, dtype=float) * repetitions + 0.5
    ) / (repetitions + 1.0)
    response = np.log(smoothed / (1.0 - smoothed))
    design = np.column_stack((np.ones(response.size), predictors))
    fitted = design @ np.linalg.lstsq(design, response, rcond=None)[0]
    residual = float(np.sum((response - fitted) ** 2))
    total = float(np.sum((response - np.mean(response)) ** 2))
    return 1.0 - residual / total, float(np.sqrt(np.mean((response - fitted) ** 2)))


def main() -> None:
    with (
        RESULTS_DIR / "nuisance_jacobian_population_20260817.tsv"
    ).open(newline="") as stream:
        population_rows = list(csv.DictReader(stream, delimiter="\t"))
    population = {row["scenario"]: row for row in population_rows}
    with (
        RESULTS_DIR / "profile_bridge_family_validation_pilot_20260817.tsv"
    ).open(newline="") as stream:
        simulation = list(csv.DictReader(stream, delimiter="\t"))

    joined = []
    for row in simulation:
        key = f"{row['bridge_family']}_epsilon_{float(row['bridge_probability']):g}"
        nuisance = population[key]
        n = int(row["n"])
        joined.append(
            {
                "scenario": key,
                "n": n,
                "studentized_rejection": float(row["studentized_rejection"]),
                "sqrt_n_minimum_singular_value": np.sqrt(n)
                * float(nuisance["minimum_singular_value"]),
                "jacobian_condition_number": float(
                    nuisance["jacobian_condition_number"]
                ),
                "standardized_median_density": float(
                    nuisance["standardized_median_density"]
                ),
                "standardized_mad_density_sum": float(
                    nuisance["standardized_mad_density_sum"]
                ),
                "huber_location_curvature": float(
                    nuisance["huber_location_curvature"]
                ),
            }
        )
    write_tsv(RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv", joined)

    rejection = np.asarray([row["studentized_rejection"] for row in joined])
    diagnostic_specs = (
        ("sqrt_n_minimum_singular_value", -1.0),
        ("jacobian_condition_number", 1.0),
        ("standardized_median_density", -1.0),
        ("standardized_mad_density_sum", -1.0),
        ("huber_location_curvature", -1.0),
    )
    associations = []
    for name, orientation in diagnostic_specs:
        values = orientation * np.asarray([float(row[name]) for row in joined])
        correlation, p_value = spearmanr(values, rejection)
        associations.append(
            {
                "population_risk_diagnostic": name,
                "risk_orientation": "larger" if orientation > 0 else "smaller",
                "spearman_rejection": float(correlation),
                "spearman_p": float(p_value),
            }
        )
    write_tsv(
        RESULTS_DIR / "nuisance_jacobian_diagnostic_associations_20260817.tsv",
        associations,
    )

    repetitions = int(simulation[0]["repetitions"])
    identification = np.log(
        [row["sqrt_n_minimum_singular_value"] for row in joined]
    )
    mad_density = np.log([row["standardized_mad_density_sum"] for row in joined])
    curvature = np.log([row["huber_location_curvature"] for row in joined])
    models = []
    for name, predictors in (
        ("minimum_singular_value_only", identification[:, None]),
        (
            "full_first_order_jacobian",
            np.column_stack((identification, mad_density, curvature)),
        ),
    ):
        r_squared, rmse = fit_logit_model(rejection, repetitions, predictors)
        models.append(
            {
                "model": name,
                "parameters_including_intercept": predictors.shape[1] + 1,
                "r_squared": r_squared,
                "rmse_logit": rmse,
            }
        )
    write_tsv(RESULTS_DIR / "nuisance_jacobian_models_20260817.tsv", models)
    for row in associations + models:
        print(row)


if __name__ == "__main__":
    main()
