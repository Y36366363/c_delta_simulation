from scripts.run_skew_mechanism_factorial_20260811 import (
    FACTORIAL_CONFIGURATIONS,
    MAGNITUDE_SKEW_CONFIGURATIONS,
    factorial_contrasts,
    signed_lognormal_skewness,
)


def test_factorial_has_all_four_unique_cells():
    cells = {
        (int(row["node_skew"]), int(row["dyad_skew"]))
        for row in FACTORIAL_CONFIGURATIONS
    }
    assert cells == {(0, 0), (1, 0), (0, 1), (1, 1)}
    assert len({str(row["name"]) for row in FACTORIAL_CONFIGURATIONS}) == 4
    assert len(MAGNITUDE_SKEW_CONFIGURATIONS) == 2
    assert all(float(row["positive_sign_probability"]) == 0.5 for row in MAGNITUDE_SKEW_CONFIGURATIONS)


def test_factorial_contrasts_recover_additive_main_effects():
    values = {(0, 0): 1.0, (1, 0): 3.0, (0, 1): 4.0, (1, 1): 6.0}
    contrasts = factorial_contrasts(values)
    assert contrasts["balanced_gaussian_cell"] == 1.0
    assert contrasts["node_skew_main_effect"] == 2.0
    assert contrasts["dyad_skew_main_effect"] == 3.0
    assert contrasts["node_by_dyad_interaction"] == 0.0
    assert contrasts["joint_skew_cell"] == 6.0


def test_balanced_equal_scale_signed_lognormal_is_symmetric():
    assert abs(signed_lognormal_skewness(0.5, 0.7)) < 1e-12
    assert signed_lognormal_skewness(0.5, 0.7, 0.8, 1.0) < -0.4
