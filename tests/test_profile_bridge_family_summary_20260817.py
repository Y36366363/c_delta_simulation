import numpy as np

from scripts.summarize_profile_bridge_family_validation_20260817 import (
    fit_family_models,
    holm_adjust,
)


def test_holm_adjust_is_monotone_in_ordered_p_values():
    adjusted = holm_adjust(np.array([0.01, 0.03, 0.20]))
    assert np.allclose(adjusted, [0.03, 0.06, 0.20])


def test_family_model_detects_no_gain_when_families_match():
    rows = []
    for family in ("uniform", "exponential", "half_normal", "scaled_beta12"):
        for kappa, rejection in ((0.2, 0.5), (0.8, 0.3), (3.2, 0.1)):
            rows.append(
                {
                    "repetitions": "1000",
                    "studentized_rejection": str(rejection),
                    "n_epsilon_squared": str(kappa),
                    "bridge_family": family,
                }
            )
    models = fit_family_models(rows)
    assert models[0]["r_squared"] > 0.98
    assert abs(models[1]["r_squared"] - models[0]["r_squared"]) < 1e-12
