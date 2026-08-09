import numpy as np

from scripts.run_signal_strength_external_grid_20260809 import (
    EXTERNAL_COMBINATIONS,
    validate_models,
)


def test_external_grid_has_one_new_row_and_column_without_duplicates():
    assert len(EXTERNAL_COMBINATIONS) == 7
    assert len(set(EXTERNAL_COMBINATIONS)) == 7
    assert {(node, dyad) for node, dyad in EXTERNAL_COMBINATIONS if node == 0.65} == {
        (0.65, 0.30),
        (0.65, 0.45),
        (0.65, 0.65),
        (0.65, 0.80),
    }
    assert {(node, dyad) for node, dyad in EXTERNAL_COMBINATIONS if dyad == 0.30} == {
        (0.35, 0.30),
        (0.55, 0.30),
        (0.65, 0.30),
        (0.75, 0.30),
    }


def test_external_validation_recovers_exact_synthetic_prediction():
    observed = 1.0 / (1.0 + np.exp(-(-1.0 + 0.5 * np.log(0.55 / 0.30))))
    crossovers = [
        {
            "node_strength": 0.55,
            "dyad_strength": 0.30,
            "crossover_estimate": observed,
        }
    ]
    models = [
        {
            "model": "raw_ratio",
            "n_combinations": 9,
            "intercept": -1.0,
            "coefficient_1": 0.5,
            "coefficient_2": np.nan,
        }
    ]
    metrics, predictions = validate_models(crossovers, models)
    assert abs(predictions[0]["crossover_error"]) < 1e-12
    assert abs(predictions[0]["logit_residual"]) < 1e-12
    assert metrics[0]["external_rmse_crossover"] < 1e-12
