import numpy as np

from scripts.summarize_nuisance_jacobian_20260817 import fit_logit_model


def test_logit_model_recovers_exact_linear_predictor():
    predictor = np.linspace(-2.0, 2.0, 20)
    probability = 1.0 / (1.0 + np.exp(-(0.3 - 0.7 * predictor)))
    r_squared, rmse = fit_logit_model(
        probability, repetitions=1_000_000, predictors=predictor[:, None]
    )
    assert r_squared > 0.999999
    assert rmse < 1e-4
