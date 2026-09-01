from pathlib import Path
import sys

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_profile_correlation_inference, huber_reference_profile
from scripts.audit_public_rho_api_20260901 import public_rho_api_audit


def test_public_rho_api_audit_passes_without_new_distribution_grid():
    rows = public_rho_api_audit()
    assert len(rows) == 8
    assert all(int(row["passed"]) for row in rows)


def test_public_rho_api_estimate_is_the_robust_reference_profile_correlation():
    rng = np.random.default_rng(2026090101)
    x = rng.normal(size=160)
    y = 0.4 * x + rng.normal(size=x.size)
    fitted = huber_profile_correlation_inference(x, y)
    expected = np.corrcoef(huber_reference_profile(x), huber_reference_profile(y))[0, 1]
    assert float(fitted["estimate"]) == pytest.approx(float(expected), abs=1e-14)
    assert float(fitted["standard_error"]) > 0.0
    assert 0.0 <= float(fitted["p_value"]) <= 1.0
    assert abs(float(np.mean(np.asarray(fitted["influence"])))) < 1e-12


def test_public_rho_api_rejects_nonregular_or_invalid_requests():
    regular = np.linspace(-2.0, 2.0, 20)
    with pytest.raises(ValueError, match="zero MAD|degenerate"):
        huber_profile_correlation_inference(regular, np.ones(20))
    with pytest.raises(ValueError, match="between -1 and 1"):
        huber_profile_correlation_inference(regular, regular**2, null_value=1.1)
    with pytest.raises(ValueError, match="at least 12"):
        huber_profile_correlation_inference(regular[:10], regular[:10] ** 2)


def test_public_api_documentation_freezes_the_manuscript_boundaries():
    api_doc = " ".join((huber_profile_correlation_inference.__doc__ or "").split())
    report = " ".join(
        (PROJECT_ROOT / "docs" / "public_rho_api_validation_20260901.md")
        .read_text()
        .split()
    )
    assert "pointwise Wald inference" in api_doc
    assert "not a uniform guarantee" in api_doc
    assert "globally robust correlation coefficient" in api_doc
    assert "pointwise, not uniform" in report
    assert "can cause" in report
    assert "first-order organizer, not a universal cutoff" in report
