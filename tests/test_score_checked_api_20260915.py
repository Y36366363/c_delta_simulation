"""Integration checks for the opt-in solver; no calibration assertions."""
from fractions import Fraction
import numpy as np
import pytest
from src.cdelta import huber_profile_correlation_inference as infer
from src.cdelta import _huber_score_checked_root, _huber_exact_score
from scripts.audit_proof_solver_20260914 import candidate_margin
from scripts.run_reference_pathway_20260909 import profile_result, generate


def sample():
    w = np.linspace(-2., 2., 60)
    return w, np.sin(w) + .2 * w**2


def test_full_if_matches_separate_dated_prototype_on_known_flag():
    x, y = generate(.1, 640, 70)
    out = infer(x, y, reference_solver='score_checked')
    tx, sx, ix, _ = candidate_margin(x)
    ty, sy, iy, _ = candidate_margin(y)
    rho, _, se, _ = profile_result(x, y, tx, ty, ix, iy)
    assert out['estimate'] == pytest.approx(rho, abs=1e-13)
    assert out['standard_error'] == pytest.approx(se, abs=1e-13)
    for label, w in [('x', x), ('y', y)]:
        d = out['solver_diagnostics'][label]
        assert abs(_huber_exact_score(w, out['reference_location_' + label],
                                     out['reference_scale_' + label])) <= Fraction(1, 10**8 * len(w))
        assert d['exact_residual_passed']


def test_default_has_unchanged_fields_and_explicit_legacy_matches():
    x, y = sample()
    a, b = infer(x, y), infer(x, y, reference_solver='legacy')
    assert 'solver_diagnostics' not in a
    assert a.keys() == b.keys()
    for k in a:
        if isinstance(a[k], np.ndarray):
            np.testing.assert_array_equal(a[k], b[k])
        else:
            assert a[k] == b[k]


@pytest.mark.parametrize('kwargs', [{'reference_solver':'wrong'},
    {'reference_solver':'score_checked','solver_max_iterations':0},
    {'reference_solver':'score_checked','solver_max_iterations':2.5},
    {'reference_solver':'score_checked','solver_max_iterations':True}])
def test_invalid_options(kwargs):
    with pytest.raises(ValueError):
        infer(*sample(), **kwargs)


def test_public_api_propagates_exhausted_budget_without_fallback():
    with pytest.raises(RuntimeError, match='budget exhausted'):
        infer(*sample(), reference_solver='score_checked', solver_max_iterations=1)


def test_core_resolution_failure_is_explicit():
    with pytest.raises(FloatingPointError, match='bracket exhausted'):
        _huber_score_checked_root([2.**53, 2.**53, 2.**53 + 2.], 10.)


@pytest.mark.parametrize('correction', ['hc0','sample','hc1'])
def test_opt_in_preserves_studentizer_corrections(correction):
    x, y = sample()
    out = infer(x, y, reference_solver='score_checked', small_sample_correction=correction)
    factor = {'hc0':1., 'sample':60/59, 'hc1':60/54}[correction]
    expected = np.sqrt(np.mean(out['influence']**2) * factor / 60)
    assert out['standard_error'] == expected


def test_small_residual_does_not_override_degenerate_profile_check():
    with pytest.raises(ValueError, match='degenerate margin'):
        infer(np.tile([-1.,1.],30), np.linspace(-2.,2.,60), reference_solver='score_checked')


def test_frozen_source_resolver_rejects_corruption_and_unregistered_hashes(tmp_path):
    from pathlib import Path
    from scripts.verify_frozen_sources import frozen_source_check, LEGACY_CDELTA_HASH, LEGACY_CDELTA_PATH, ROOT
    target = tmp_path / LEGACY_CDELTA_PATH
    target.parent.mkdir(parents=True)
    target.write_bytes((ROOT / LEGACY_CDELTA_PATH).read_bytes())
    assert frozen_source_check('src/cdelta.py', LEGACY_CDELTA_HASH, root=tmp_path)['passed']
    assert not frozen_source_check('other.py', LEGACY_CDELTA_HASH, root=tmp_path)['passed']
    assert not frozen_source_check('src/cdelta.py', '0'*64, root=tmp_path)['passed']
    target.write_bytes(target.read_bytes() + b'\n# unexpected alteration\n')
    assert not frozen_source_check('src/cdelta.py', LEGACY_CDELTA_HASH, root=tmp_path)['passed']
