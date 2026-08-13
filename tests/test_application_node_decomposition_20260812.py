import numpy as np
from itertools import permutations, product

from scripts.run_application_node_decomposition_20260812 import (
    adaptive_permutation_outcomes,
    cross_validated_weight_statistic,
    make_application_building_pair,
    _paired_signs,
    _component_statistics,
)
from scripts.summarize_application_node_decomposition_20260812 import (
    combine_rates,
    decomposition_effects,
)


def test_application_generator_separates_declared_mechanisms():
    rng = np.random.default_rng(10)
    x, y, blocks, diagnostics = make_application_building_pair(
        rng,
        positive_probability=0.7,
        sign_agreement=0.8,
        magnitude_sigma=0.9,
        magnitude_rho=0.6,
        center_sd=1.0,
        center_rho=0.7,
    )
    assert x.shape == y.shape == blocks.shape == (60,)
    assert len(np.unique(blocks)) == 6
    assert 0.0 <= diagnostics["realized_sign_agreement"] <= 1.0
    assert diagnostics["realized_log_radius_sd_x"] > 0.5


def test_paired_signs_have_separate_margin_and_agreement_controls():
    signs_x, signs_y = _paired_signs(
        np.random.default_rng(11), 200_000, 0.70, 0.75
    )
    assert abs(np.mean(signs_x > 0) - 0.70) < 0.005
    assert abs(np.mean(signs_y > 0) - 0.70) < 0.005
    assert abs(np.mean(signs_x == signs_y) - 0.75) < 0.005


def test_cross_validated_weight_is_continuous_and_prefers_profile():
    scores = np.zeros((3, 4, 2))
    scores[:, :, 0] = 0.8
    scores[:, :, 1] = 0.1
    statistic, weight = cross_validated_weight_statistic(scores)
    assert np.all(weight > 0.9)
    assert np.all(statistic > 0.7)


def test_nested_rules_return_valid_probability_range():
    global_observed = np.array([0.4, 0.2])
    global_permuted = np.array([[0.1, 0.3], [0.5, 0.0], [-0.2, 0.1]])
    block_observed = np.array([[0.4, 0.1], [0.3, 0.0], [0.5, 0.2]])
    block_permuted = np.stack(
        [block_observed - 0.2, block_observed + 0.1, -block_observed]
    )
    outcomes = adaptive_permutation_outcomes(
        global_observed, global_permuted, block_observed, block_permuted
    )
    for key, value in outcomes.items():
        if key.endswith("_p"):
            assert 0.0 < value <= 1.0
    assert 0.0 < outcomes["observed_profile_weight"] < 1.0
    assert 0.0 < outcomes["observed_standardized_profile_weight"] < 1.0
    assert 0.0 < outcomes["standardized_max_p"] <= 1.0
    assert 0.0 < outcomes["cv_standardized_p"] <= 1.0
    assert outcomes["standardized_winner"] in {"profile", "mantel"}
    assert outcomes["standardized_max_p"] == min(
        outcomes["adjusted_profile_p"], outcomes["adjusted_mantel_p"]
    )
    assert outcomes["adjusted_profile_p"] >= outcomes["profile_p"]
    assert outcomes["adjusted_mantel_p"] >= outcomes["mantel_p"]


def test_retrained_cv_statistic_has_exact_orbit_rank_validity():
    blocks = np.repeat(np.arange(2), 3)
    x = np.array([-1.8, 0.2, 1.1, -0.7, 0.5, 2.0])
    y = np.array([1.4, -0.4, 0.1, 1.7, -1.2, 0.3])
    members = [np.flatnonzero(blocks == label) for label in np.unique(blocks)]
    group = []
    for choices in product(*(list(permutations(group)) for group in members)):
        index = np.arange(blocks.size)
        for target, choice in zip(members, choices):
            index[target] = choice
        group.append(index)
    group = np.asarray(group)
    orbit_statistics = []
    standardized_p_values = []
    standardized_max_p_values = []
    for index in group:
        permuted_y = y[index]
        components = _component_statistics(x, permuted_y, blocks, group)
        _, _, block_observed, _ = components
        statistic, _ = cross_validated_weight_statistic(block_observed[None, :, :])
        orbit_statistics.append(float(statistic[0]))
        outcomes = adaptive_permutation_outcomes(*components)
        standardized_p_values.append(outcomes["cv_standardized_p"])
        standardized_max_p_values.append(outcomes["standardized_max_p"])
    orbit_statistics = np.asarray(orbit_statistics)
    exact_p = np.mean(
        orbit_statistics[None, :] >= orbit_statistics[:, None], axis=1
    )
    for alpha in (0.05, 0.10, 0.20):
        assert np.mean(exact_p <= alpha) <= alpha + 1e-12
        assert np.mean(np.asarray(standardized_p_values) <= alpha) <= alpha + 1e-12
        assert (
            np.mean(np.asarray(standardized_max_p_values) <= alpha)
            <= alpha + 1e-12
        )


def test_combiner_recovers_counts_and_factor_effects():
    runs = [
        [
            {
                "sign_agreement": sign,
                "positive_probability": positive,
                "magnitude_sigma": sigma,
                "center_sd": center,
                "method": "profile",
                "repetitions": "100",
                "rejection_rate": str(
                    0.10
                    + (0.20 if sign == "0.75" else 0.0)
                    + (0.10 if sigma == "0.85" else 0.0)
                    - (0.05 if center == "1.0" else 0.0)
                ),
            }
            for positive in ("0.5", "0.7")
            for sign in ("0.5", "0.75")
            for sigma in ("0.35", "0.85")
            for center in ("0.0", "1.0")
        ]
    ]
    combined = combine_rates(
        runs,
        (
            "positive_probability",
            "sign_agreement",
            "magnitude_sigma",
            "center_sd",
            "method",
        ),
    )
    assert sum(int(row["reject_count"]) for row in combined) == 360
    effects = decomposition_effects(combined)
    sign = next(row for row in effects if row["factor"] == "sign_agreement")
    assert abs(float(sign["average_power_main_effect"]) - 0.20) < 1e-12
