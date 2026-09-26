"""Analytic symmetry anchors independent of the historical Jacobian code."""
import numpy as np
import pytest
from scripts.audit_evidence_interfaces_20260926 import symmetric_index


@pytest.mark.parametrize("family",["uniform","exponential","half_normal","scaled_beta12","hyperexponential"])
def test_pure_bridge_medians_and_density_anchors(family):
    # epsilon=1 removes the lognormal component, leaving tractable radius laws.
    from scipy.stats import halfnorm
    medians={"uniform":.5,"exponential":np.log(2),
             "half_normal":halfnorm(scale=np.sqrt(2/np.pi)).ppf(.5),
             "scaled_beta12":2*(1-1/np.sqrt(2))}
    _, diagonal, d=symmetric_index(family,1.,80)
    if family in medians:
        assert d==pytest.approx(medians[family],abs=1e-12)
    assert diagonal[0]==d/2
    assert diagonal[1]>0 and diagonal[2]<0
