import numpy as np

from scripts.run_mad_ratio_crossvalidation_20260817 import (
    margin_scale_iqr_ratio,
    run_ratio_cell,
)


def test_mad_iqr_ratio_is_affine_invariant():
    values = np.array([-3.0, -1.0, 0.0, 0.5, 2.0, 8.0])
    assert np.isclose(
        margin_scale_iqr_ratio(values),
        margin_scale_iqr_ratio(4.0 - 2.0 * values),
    )


def test_ratio_crossvalidation_smoke_has_ordered_warning_rates():
    row = run_ratio_cell(
        repetitions=20,
        n=40,
        seed=1,
        design="sigma",
        scenario="sigma_0.1",
        radial_log_sd=0.1,
    )
    assert row["ratio_below_0p25_rate"] <= row["ratio_below_0p4_rate"]
    assert row["ratio_below_0p4_rate"] <= row["ratio_below_0p5_rate"]
