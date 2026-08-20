from pathlib import Path

import numpy as np

from scripts.audit_mad_convention_20260820 import (
    lower_empirical_median,
    lower_quantile_median_mad,
    numpy_median_mad,
    run_audit,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPENDIX = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"
AUDIT = PROJECT_ROOT / "docs" / "entropy_mad_permutation_decision_20260820.md"


def test_even_sample_conventions_are_explicitly_different():
    sample = np.array([[0.0, 1.0, 4.0, 10.0]])
    numpy_median, numpy_mad = numpy_median_mad(sample)
    lower_median, lower_mad = lower_quantile_median_mad(sample)
    assert numpy_median[0] == 2.5
    assert lower_median[0] == 1.0
    assert numpy_mad[0] == 2.0
    assert lower_mad[0] == 1.0
    assert lower_empirical_median(sample, axis=1)[0] == 1.0


def test_odd_sample_median_conventions_coincide():
    sample = np.array([[0.0, 1.0, 4.0, 10.0, 20.0]])
    numpy_median, _ = numpy_median_mad(sample)
    lower_median, _ = lower_quantile_median_mad(sample)
    assert numpy_median[0] == lower_median[0] == 4.0


def test_small_fixed_seed_audit_shows_root_n_convention_gap_shrinking():
    rows = run_audit(repetitions=1200, sample_sizes=(40, 160, 640))
    grouped = {}
    for row in rows:
        grouped.setdefault((row["distribution"], row["quantity"]), []).append(row)
    for values in grouped.values():
        values.sort(key=lambda row: row["n"])
        assert values[-1]["sqrt_n_times_median_abs_difference"] < values[0][
            "sqrt_n_times_median_abs_difference"
        ]


def test_appendix_maps_classes_and_freezes_permutation_scope():
    appendix = APPENDIX.read_text()
    audit = AUDIT.read_text()
    assert "Theorem 2.6.7" in appendix
    assert "van der Vaart and Wellner (2007) now applies" in appendix
    assert "NumPy midpoint convention" in appendix
    assert "not required for the present paper" in appendix
    assert "sign-times-radius" in audit
    assert "Mazumder" in audit and "Serfling" in audit
