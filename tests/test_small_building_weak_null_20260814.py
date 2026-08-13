import numpy as np

from scripts.run_small_building_weak_null_20260814 import (
    cluster_inference,
    make_clustered_pair,
)
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


def test_building_generator_has_declared_independent_units():
    x, y, blocks = make_clustered_pair(
        np.random.default_rng(143),
        n_buildings=6,
        rooms_per_building=10,
        scenario="skew_scale_cluster_null",
    )
    assert x.shape == y.shape == blocks.shape == (60,)
    assert np.bincount(blocks).tolist() == [10] * 6


def test_cluster_inference_uses_building_summed_scores_and_valid_p_values():
    rng = np.random.default_rng(144)
    x, y, blocks = make_clustered_pair(
        rng,
        n_buildings=6,
        rooms_per_building=12,
        scenario="gaussian_cluster_null",
    )
    fitted = profile_weak_null_test(x, y)
    result = cluster_inference(
        float(fitted["estimate"]), np.asarray(fitted["influence"]), blocks
    )
    assert result["cluster_standard_error"] > 0.0
    assert 0.0 <= result["cluster_t_p"] <= 1.0
    assert 0.0 <= result["signflip_p"] <= 1.0
    assert 1.0 / 6.0 <= result["max_cluster_score_share"] <= 1.0
