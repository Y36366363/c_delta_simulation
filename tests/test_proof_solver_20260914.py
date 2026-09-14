"""Deterministic algebra and failure tests, not asymptotic calibration tests."""
from fractions import Fraction

import numpy as np
import pytest
from scipy.optimize import brentq

from scripts.audit_proof_solver_20260914 import checked_root, exact_score, candidate_margin


def test_linear_region_matches_sample_mean():
    w = np.array([-1., -.3, .2, .5, .8, 1.3])
    out = checked_root(w, 10.)
    assert abs(out['location'] - w.mean()) <= 10. / (10**8 * len(w))
    assert abs(exact_score(w, out['location'], 10.)) <= Fraction(1, 10**8 * len(w))


def test_clipped_root_matches_independent_brent_solver():
    w = np.r_[np.linspace(-2., 2., 31), 9., 14., 500.]
    out = checked_root(w, 1.)
    root = brentq(lambda t: np.mean(np.clip(w - t, -1.345, 1.345)), -2., 500., xtol=1e-14)
    assert abs(root - out['location']) < 1e-8
    assert abs(exact_score(w, out['location'], 1.)) <= Fraction(1, 10**8 * len(w))


@pytest.mark.parametrize('shift,scale', [(0., 1e-6), (0., 1e6), (31., 3.)])
def test_affine_equivariance_to_declared_numerical_accuracy(shift, scale):
    w = np.r_[np.linspace(-2., 2., 31), 9., 14., 500.]
    original = checked_root(w, 1.)['location']
    transformed = checked_root(shift + scale * w, scale)['location']
    assert abs((transformed - shift) / scale - original) < 2e-8


def test_flat_root_is_not_a_positive_slope_certificate():
    w = np.array([-10., -9., 9., 10.])
    out = checked_root(w, 1.)
    assert exact_score(w, out['location'], 1.) == 0
    assert np.mean(abs(w - out['location']) < 1.345) == 0
    assert exact_score(w, -1., 1.) == exact_score(w, 1., 1.) == 0


def test_iteration_cap_raises_instead_of_returning_approximation():
    with pytest.raises(RuntimeError, match='budget exhausted'):
        checked_root(np.array([0., 0., 1.]), 10., max_iterations=1)


def test_unrepresentable_root_raises_instead_of_relaxing_tolerance():
    # Exact mean is 2**53 + 2/3; nearby float spacing is 2.
    w = np.array([2.**53, 2.**53, 2.**53 + 2.])
    with pytest.raises(FloatingPointError, match='bracket exhausted'):
        checked_root(w, 10.)


def test_exact_score_detects_floating_cancellation():
    w = np.array([1e16, 1., -1e16])
    assert np.mean(w / 1e16) == 0.
    assert exact_score(w, 0., 1e16, c=2.) == Fraction(1, 3 * 10**16)


@pytest.mark.parametrize('w,s,c', [([1.], 1., 1.), ([0., np.nan], 1., 1.),
                                 ([0., np.inf], 1., 1.), ([[1., 2.]], 1., 1.),
                                 ([0., 1.], 0., 1.), ([0., 1.], np.inf, 1.),
                                 ([0., 1.], 1., -1.), ([0., 1.], 1., np.nan)])
def test_invalid_inputs(w, s, c):
    with pytest.raises(ValueError):
        checked_root(w, s, c=c)


def test_zero_mad_rejected_before_influence_calculation():
    with pytest.raises(ValueError):
        candidate_margin(np.ones(12))


@pytest.mark.parametrize('h', [-2., -.01, 0., .01, 2.])
def test_absolute_radius_remainder_bound_including_crossings(h):
    x = np.r_[np.linspace(-4., 4., 101), 0., h, -h]
    remainder = abs(abs(x - h) - abs(x) + h * np.sign(x))
    bound = 2 * abs(h) * (abs(x) <= abs(h))
    assert np.all(remainder <= bound + 2e-15)


@pytest.mark.parametrize('dt,du', [(.1, .2), (-.1, -.2), (0., .5)])
def test_weighted_sign_bound_with_dependent_pair_values(dt, du):
    x = np.r_[np.linspace(-2., 2., 201), 0., dt]
    y = x**2 + .3 * x  # deliberately dependent pairing
    delta = np.sign(x - dt) * abs(y - du) - np.sign(x) * abs(y)
    bound = 2 * du**2 + 8 * y**2 * (abs(x) <= abs(dt))
    assert np.all(delta**2 <= bound + 2e-14)


def test_empirical_fourth_moment_bound_is_deterministic():
    # A bound check, not evidence for a LLN or an infinite-fourth-moment claim.
    a = np.array([0., .1, 1., 2., 1e4])
    assert np.mean(a**4) / len(a) <= a.max()**2 / len(a) * np.mean(a**2)
