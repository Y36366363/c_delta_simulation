"""Diagnostic score-checked roots; no public API or frozen-output changes.

Protocol: docs/proof_solver_protocol_20260914.md. An exact rational residual
check concerns represented floats, not population regularity or universal
floating-point solvability. Never use the 41 selected datasets as a size study.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import platform
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.cdelta import _gaussian_kde_density, huber_profile_correlation_inference
from scripts.run_reference_pathway_20260909 import generate, profile_result
from scripts.replay_manuscript_interfaces_20260912 import REPS, TRUTH, K, C, Z


def exact_score(values, location, scale, c=C):
    """Real-arithmetic empirical score for these exact represented floats."""
    t, s, clip = map(Fraction.from_float, map(float, (location, scale, c)))
    total = Fraction(0)
    for w in values:
        u = (Fraction.from_float(float(w)) - t) / s
        total += min(clip, max(-clip, u))
    return total / len(values)


def checked_root(values, scale, *, c=C, max_iterations=512):
    """Bisection accepted only after an exact |score| <= 1/(10^8 n) check.

    The iteration cap is a failure guard. Failure does not relax the threshold.
    Root existence on [min(values), max(values)] follows from score signs;
    uniqueness and a positive active fraction are not guaranteed.
    """
    w = np.asarray(values, dtype=float)
    if w.ndim != 1 or w.size < 2 or not np.all(np.isfinite(w)):
        raise ValueError('finite one-dimensional sample of length >= 2 required')
    if not np.isfinite(scale) or scale <= 0 or not np.isfinite(c) or c <= 0:
        raise ValueError('finite positive scale and c required')
    if not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError('positive integer iteration budget required')
    tolerance = Fraction(1, 10**8 * w.size)
    lo, hi = float(w.min()), float(w.max())
    exact_checks = 0
    for iteration in range(1, max_iterations + 1):
        t = lo / 2 + hi / 2
        # Subtraction can overflow for extreme but finite opposite endpoints.
        # Clipping infinite residuals is defined; a NaN score is not accepted.
        with np.errstate(over='ignore'):
            q = float(np.mean(np.clip((w - t) / scale, -c, c)))
        if not np.isfinite(q):
            raise FloatingPointError('nonfinite numerical score')
        if abs(q) <= 2 * float(tolerance):
            exact = exact_score(w, t, scale, c)
            exact_checks += 1
            if abs(exact) <= tolerance:
                return {'location': t, 'score_float': q,
                        'score_exact_float': float(exact),
                        'score_exact_numerator': str(exact.numerator),
                        'score_exact_denominator': str(exact.denominator),
                        'tolerance': float(tolerance), 'iterations': iteration,
                        'exact_checks': exact_checks, 'exact_residual_passed': True}
            q = float(exact)
        if t == lo or t == hi:
            raise FloatingPointError('floating-point bracket exhausted before residual acceptance')
        if q > 0:
            lo = t
        else:
            hi = t
    raise RuntimeError('iteration budget exhausted before residual acceptance')


def candidate_margin(w):
    median = float(np.median(w))
    mad = float(np.median(abs(w - median)))
    scale = K * mad
    root = checked_root(w, scale)
    t = root['location']
    fm, fp, fn = (_gaussian_kde_density(w, u)
                  for u in (median, median + mad, median - mad))
    if min(fm, fp, fn) <= 0 or not np.all(np.isfinite((fm, fp, fn))):
        raise ValueError('invalid density plug-ins')
    im = (.5 - (w <= median)) / fm
    id_ = (.5 - (abs(w - median) <= mad) - (fp - fn) * im) / (fp + fn)
    u = (w - t) / scale
    active = abs(u) < C
    a, b = float(np.mean(active)), float(np.mean(u * active))
    if a <= 0:
        raise ValueError('zero active fraction: a small root residual is not valid inference')
    it = scale / a * np.clip(u, -C, C) - b / a * K * id_
    return t, scale, it, root


def datasets():
    for n in (160, 640, 2560):
        for rep in REPS:
            rng = np.random.default_rng(np.random.SeedSequence([2026090701, n, rep]))
            z = rng.standard_normal((n, 2))
            x = np.exp(.6 * z[:, 0])
            y = np.exp(.6 * (.4 * z[:, 0] + np.sqrt(1 - .4**2) * z[:, 1]))
            yield {'study': 'skew', 'n': n, 'replication': rep, 'truth': TRUTH}, x, y
    for tau in (.1, .4):
        for n in (80, 640):
            reps = (0, 1, 1999, 70, 1622) if (tau, n) == (.1, 640) else (0, 1, 1999)
            for rep in reps:
                x, y = generate(tau, n, rep)
                yield {'study': 'pathway', 'n': n, 'tau': tau,
                       'replication': rep, 'truth': 0.}, x, y


def run():
    rows, margins, failures = [], [], []
    for meta, x, y in datasets():
        try:
            old = huber_profile_correlation_inference(x, y, null_value=meta['truth'])
            fitted = []
            for label, w in (('x', x), ('y', y)):
                t, s, it, root = candidate_margin(w)
                old_score = exact_score(w, old['reference_location_' + label], s)
                margins.append({**meta, 'margin': label, **root,
                                'legacy_score_exact_float': float(old_score),
                                'legacy_meets_new_residual_rule': abs(old_score) <= Fraction(1, 10**8 * len(w)),
                                'root_gap_scale_units': (t - old['reference_location_' + label]) / s})
                fitted.append((t, s, it))
            (tx, sx, ix), (ty, sy, iy) = fitted
            rho, _, se, dse = profile_result(x, y, tx, ty, ix, iy)
            _, _, _, old_dse = profile_result(x, y, old['reference_location_x'],
                                             old['reference_location_y'], 0., 0.)
            if not np.all(np.isfinite((rho, se, dse))) or min(se, dse) <= 0:
                raise ValueError('invalid candidate target or standard error')
            rows.append({**meta, 'estimate_delta': rho - old['estimate'],
                         'estimate_delta_over_original_se': (rho - old['estimate']) / old['standard_error'],
                         'relative_full_se_delta': se / old['standard_error'] - 1,
                         'relative_direct_se_delta': dse / old_dse - 1,
                         'full_decision_changed': bool((abs(rho - meta['truth']) <= Z * se) !=
                                                      (abs(old['estimate'] - meta['truth']) <= Z * old['standard_error'])),
                         'direct_decision_changed': bool((abs(rho - meta['truth']) <= Z * dse) !=
                                                        (abs(old['estimate'] - meta['truth']) <= Z * old_dse))})
        except (ValueError, RuntimeError, FloatingPointError, ZeroDivisionError) as exc:
            failures.append({**meta, 'error': str(exc)})
    summaries = {}
    for study in ('skew', 'pathway'):
        rr = [r for r in rows if r['study'] == study]
        mm = [r for r in margins if r['study'] == study]
        summaries[study] = {'datasets': len(rr), 'margins': len(mm),
            'legacy_fails_new_residual_rule': sum(not m['legacy_meets_new_residual_rule'] for m in mm),
            'max_abs_legacy_score': max((abs(m['legacy_score_exact_float']) for m in mm), default=None),
            'max_abs_candidate_score': max((abs(m['score_exact_float']) for m in mm), default=None),
            'max_iterations': max((m['iterations'] for m in mm), default=None),
            **{'max_abs_' + k: max((abs(r[k]) for r in rr), default=None) for k in
               ('estimate_delta', 'estimate_delta_over_original_se', 'relative_full_se_delta', 'relative_direct_se_delta')},
            **{k: sum(r[k] for r in rr) for k in ('full_decision_changed', 'direct_decision_changed')}}
    paths = ('src/cdelta.py', 'scripts/audit_proof_solver_20260914.py',
             'scripts/replay_manuscript_interfaces_20260912.py',
             'scripts/run_reference_pathway_20260909.py',
             'docs/proof_solver_protocol_20260914.md',
             'results/active_nuisance_replications_20260907.tsv',
             'results/reference_pathway_replications_20260909.tsv')
    return {'scope': 'targeted internal proof/solver audit; not independent peer review or calibration',
            'candidate_only': True, 'public_api_changed': False, 'new_simulation_cells': 0,
            'datasets_attempted': 41, 'datasets_completed': len(rows), 'failures': failures,
            'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                            'executable': sys.executable},
            'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            'summaries': summaries, 'margins': margins, 'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError('Refusing to overwrite an existing audit; choose a new output path')
    report = run()
    args.report.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
    print(json.dumps({k: report[k] for k in ('datasets_completed', 'failures', 'summaries')}, indent=2))
    if report['failures']:
        raise SystemExit(1)
