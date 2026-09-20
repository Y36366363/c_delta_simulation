"""One prespecified moderate-skew law; numerical engine adapted from Sept 7.

See docs/moderate_benchmark_protocol_20260920.md. No coverage-selected design.
Historical engine and production API remain untouched.
"""
from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import norm
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.robust_extension_utils import write_tsv
from scripts.run_population_skew_influence_validation import _mixture_quantile
from src.cdelta import huber_profile_correlation_inference

SIGMA, LATENT_RHO, K, C = 0.30, 0.40, 1.4826, 1.345
ROOT_SEED = 2026092001
SIZES = (160, 640, 2560)
REPS = 2000
ZCRIT = float(norm.ppf(0.975))


def below_moment(t, power=0, mu=0.0, sigma=SIGMA):
    """E[W**power 1(W <= t)] for log W ~ N(mu,sigma**2)."""
    log_t = np.log(max(float(t), np.finfo(float).tiny))
    value = np.exp(power * mu + 0.5 * power**2 * sigma**2) * ndtr(
        (log_t - mu - power * sigma**2) / sigma
    )
    return value if t > 0 else np.zeros_like(value)


def radius_mean(t, mu=0.0, sigma=SIGMA):
    return (
        np.exp(mu + 0.5 * sigma**2)
        - t
        + 2 * (t * below_moment(t, 0, mu, sigma) - below_moment(t, 1, mu, sigma))
    )


def huber_score(t, scale, sigma=SIGMA):
    lo, hi = t - C * scale, t + C * scale
    active = below_moment(hi, sigma=sigma) - below_moment(lo, sigma=sigma)
    truncated = below_moment(hi, 1, sigma=sigma) - below_moment(lo, 1, sigma=sigma)
    return float(
        (truncated - t * active) / scale
        + C * (1 - below_moment(hi, sigma=sigma) - below_moment(lo, sigma=sigma))
    )


def marginal_fit(epsilon=0.0, point=1.0):
    cdf = lambda t: float(below_moment(t))
    m = (
        1.0
        if epsilon == 0
        else _mixture_quantile(cdf, point, epsilon, 0.5, 1e-12, 1000.0)
    )
    rcdf = lambda d: cdf(m + d) - cdf(m - d)
    d = (
        brentq(lambda d: rcdf(d) - 0.5, 0.0, 10.0, xtol=1e-14)
        if epsilon == 0
        else _mixture_quantile(rcdf, abs(point - m), epsilon, 0.5, 0.0, 1000.0)
    )
    s = K * d
    t = brentq(
        lambda t: (1 - epsilon) * huber_score(t, s)
        + epsilon * np.clip((point - t) / s, -C, C),
        1e-10,
        100.0,
        xtol=1e-14,
    )
    return float(m), float(d), float(s), float(t)


def moments(tx, ty, tol=1e-11):
    """Exact marginal moments and conditional one-dimensional integration.

    Gaussian integration is truncated at 12 SD. The tail error is negligible
    here; validate against the separate knot-split tensor calculation below.
    """
    conditional_sd = SIGMA * np.sqrt(1 - LATENT_RHO**2)

    def cross_integral(t1, t2, signed=False):
        split = np.log(t1) / SIGMA

        def integrand(z):
            x = np.exp(SIGMA * z)
            multiplier = np.sign(x - t1) if signed else abs(x - t1)
            return float(
                norm.pdf(z)
                * multiplier
                * radius_mean(t2, SIGMA * LATENT_RHO * z, conditional_sd)
            )

        return sum(
            quad(integrand, a, b, epsabs=tol, epsrel=tol)[0]
            for a, b in ((-12.0, split), (split, 12.0))
        )

    ex = np.exp(SIGMA**2 / 2)
    ex2 = np.exp(2 * SIGMA**2)
    return {
        "cross": cross_integral(tx, ty),
        "mean_x": float(radius_mean(tx)),
        "mean_y": float(radius_mean(ty)),
        "square_x": float(ex2 - 2 * tx * ex + tx**2),
        "square_y": float(ex2 - 2 * ty * ex + ty**2),
        "g_x": float(1 - 2 * below_moment(tx)),
        "g_y": float(1 - 2 * below_moment(ty)),
        "h_x": cross_integral(tx, ty, True),
        "h_y": cross_integral(ty, tx, True),
        "centered_x": float(ex - tx),
        "centered_y": float(ex - ty),
    }


def rho_gradient(m):
    vx = m["square_x"] - m["mean_x"] ** 2
    vy = m["square_y"] - m["mean_y"] ** 2
    denom = np.sqrt(vx * vy)
    rho = (m["cross"] - m["mean_x"] * m["mean_y"]) / denom
    grad = np.array(
        [
            1 / denom,
            -m["mean_y"] / denom + rho * m["mean_x"] / vx,
            -m["mean_x"] / denom + rho * m["mean_y"] / vy,
            -rho / (2 * vx),
            -rho / (2 * vy),
        ]
    )
    cx = (-m["h_x"] + m["g_x"] * m["mean_y"]) / denom + rho * (
        m["centered_x"] - m["mean_x"] * m["g_x"]
    ) / vx
    cy = (-m["h_y"] + m["mean_x"] * m["g_y"]) / denom + rho * (
        m["centered_y"] - m["mean_y"] * m["g_y"]
    ) / vy
    return float(rho), grad, float(cx), float(cy)


@lru_cache(maxsize=1)
def population():
    fit = marginal_fit()
    mom = moments(fit[3], fit[3])
    return fit, mom, rho_gradient(mom)


def location_if(x, fit):
    m, d, s, t = fit
    pdf = lambda w: 0.0 if w <= 0 else norm.pdf(np.log(w) / SIGMA) / (SIGMA * w)
    im = (0.5 - (x <= m)) / pdf(m)
    id_ = (0.5 - (np.abs(x - m) <= d) - (pdf(m + d) - pdf(m - d)) * im) / (
        pdf(m + d) + pdf(m - d)
    )
    a = float(below_moment(t + C * s) - below_moment(t - C * s))
    b = float((below_moment(t + C * s, 1) - below_moment(t - C * s, 1) - t * a) / s)
    direct = s / a * np.clip((x - t) / s, -C, C)
    return direct - b / a * K * id_, direct


def population_if(x, y):
    fit, m, (rho, grad, cx, cy) = population()
    a, b = np.abs(x - fit[3]), np.abs(y - fit[3])
    direct = (
        grad[0] * (a * b - m["cross"])
        + grad[1] * (a - m["mean_x"])
        + grad[2] * (b - m["mean_y"])
        + grad[3] * (a * a - m["square_x"])
        + grad[4] * (b * b - m["square_y"])
    )
    ix, fx = location_if(x, fit)
    iy, fy = location_if(y, fit)
    nuisance = cx * ix + cy * iy
    mad = cx * (ix - fx) + cy * (iy - fy)
    return direct, nuisance, mad


def tensor_check(order=48):
    fit, m, (rho, grad, cx, cy) = population()
    median, d, s, t = fit
    knots = [median - d, median, median + d, t - C * s, t, t + C * s]
    bounds = sorted(
        set(
            [-12.0, 12.0]
            + [
                float(np.log(v) / SIGMA)
                for v in knots
                if v > 0 and -12 < np.log(v) / SIGMA < 12
            ]
        )
    )
    nodes, weights = leggauss(order)
    z = np.concatenate(
        [(a + b) / 2 + (b - a) / 2 * nodes for a, b in zip(bounds[:-1], bounds[1:])]
    )
    w = np.concatenate([(b - a) / 2 * weights for a, b in zip(bounds[:-1], bounds[1:])])
    u, v = z[:, None], z[None, :]
    density = np.exp(
        -(u * u - 2 * LATENT_RHO * u * v + v * v) / (2 * (1 - LATENT_RHO**2))
    )
    joint = w[:, None] * w[None, :] * density / (2 * np.pi * np.sqrt(1 - LATENT_RHO**2))
    x, y = np.exp(SIGMA * u), np.exp(SIGMA * v)
    direct, nuisance, mad = population_if(x, y)
    full = direct + nuisance
    integration = lambda f: float(np.sum(joint * f))
    cross = integration(np.abs(x - t) * np.abs(y - t))
    return {
        "order_per_interval": order,
        "rho_p": rho,
        "huber_location": t,
        "mad": d,
        "location_coefficient_x": cx,
        "location_coefficient_y": cy,
        "mass_error": abs(integration(1) - 1),
        "cross_moment_error": abs(cross - m["cross"]),
        "full_if_mean": integration(full),
        "mad_if_component_mean": integration(mad),
        "full_if_variance": integration(full**2),
        "direct_if_variance": integration(direct**2),
        "nuisance_if_variance": integration(nuisance**2),
        "twice_direct_nuisance_covariance": 2 * integration(direct * nuisance),
        "mad_component_rms": np.sqrt(integration(mad**2)),
    }


def run(out):
    import json, time, importlib.metadata
    from scripts.validate_active_nuisance_20260907 import direct_estimate_se, summarize, paired_differences
    from scripts import validate_active_nuisance_20260907 as historical
    started=time.perf_counter()
    out.mkdir(parents=True,exist_ok=True)
    stem='moderate_benchmark'
    if list(out.glob(stem+'_*_20260920.*')):
        raise FileExistsError('Use a fresh output directory or remove no existing records')
    original={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'results').glob('*.tsv')}
    checks=[tensor_check(j) for j in (48,72)]
    assert max(r['cross_moment_error'] for r in checks)<1e-8
    assert abs(checks[0]['full_if_variance']/checks[1]['full_if_variance']-1)<1e-7
    assert abs(checks[-1]['rho_p'])>1e-4 and abs(checks[-1]['location_coefficient_x'])>1e-4
    write_tsv(out/f'{stem}_population_20260920.tsv',checks)
    print('POPULATION',checks[-1],flush=True)
    truth=population()[2][0];t=population()[0][3]
    rows=[];solver=[]
    for n in SIZES:
        for rep in range(REPS):
            rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([ROOT_SEED,n,rep])))
            z=rng.standard_normal((n,2));x=np.exp(SIGMA*z[:,0]);y=np.exp(SIGMA*(LATENT_RHO*z[:,0]+np.sqrt(1-LATENT_RHO**2)*z[:,1]))
            base=dict(n=n,replication=rep,root_seed=ROOT_SEED,truth=truth)
            try:
                full=huber_profile_correlation_inference(x,y,null_value=truth,reference_solver='score_checked')
                methods={'complete_kde':(full['estimate'],full['standard_error']),
                    'direct_only_ablation':direct_estimate_se(x,y,full['reference_location_x'],full['reference_location_y']),
                    'oracle_fixed_reference':direct_estimate_se(x,y,t,t)}
                for name,(est,se) in methods.items():
                    assert np.isfinite(est+se) and se>0
                    rows.append({**base,'method':name,'estimate':est,'se':se,'z':(est-truth)/se,
                        'covered':int(abs(est-truth)<=ZCRIT*se),'coefficient_x':full['location_coefficient_x'],
                        'coefficient_y':full['location_coefficient_y'],'error':''})
                old=huber_profile_correlation_inference(x,y,null_value=truth,reference_solver='legacy')
                q=max(abs(np.mean(np.clip((w-old['reference_location_'+j])/old['reference_scale_'+j],-C,C))) for j,w in [('x',x),('y',y)])
                row={**base,'error':'','delta_estimate_checked_se_units':(old['estimate']-full['estimate'])/full['standard_error'],
                    'relative_se_delta':old['standard_error']/full['standard_error']-1,
                    'max_reference_gap_scale_units':max(abs(old['reference_location_'+j]-full['reference_location_'+j])/full['reference_scale_'+j] for j in ('x','y')),
                    'sqrt_n_legacy_score_residual':np.sqrt(n)*q,
                    'coverage_decision_changed':int((abs(old['estimate']-truth)<=ZCRIT*old['standard_error'])!=(abs(full['estimate']-truth)<=ZCRIT*full['standard_error']))}
                for j in ('x','y'):
                    for key,val in full['solver_diagnostics'][j].items():row[j+'_'+key]=val
                solver.append(row)
            except (ValueError,RuntimeError,FloatingPointError,AssertionError) as exc:
                if not any(r['n']==n and r['replication']==rep for r in rows):
                    for name in ('complete_kde','direct_only_ablation','oracle_fixed_reference'):
                        rows.append({**base,'method':name,'estimate':np.nan,'se':np.nan,'z':np.nan,'covered':0,'coefficient_x':np.nan,'coefficient_y':np.nan,'error':str(exc)})
                solver.append({**base,'error':str(exc)})
            if (rep+1)%500==0:print('DATASETS',n,rep+1,flush=True)
    summary=summarize(rows)
    for r in summary:
        selected=[v for v in rows if v['n']==r['n'] and v['method']==r['method'] and not v['error']]
        r['below_truth_misses']=sum(v['z'] < -ZCRIT for v in selected)
        r['above_truth_misses']=sum(v['z'] > ZCRIT for v in selected)
        r['primary_reference_solver']='score_checked'
    write_tsv(out/f'{stem}_replications_20260920.tsv',rows)
    write_tsv(out/f'{stem}_summary_20260920.tsv',summary)
    write_tsv(out/f'{stem}_paired_20260920.tsv',paired_differences(rows))
    # Rectangular failure records retain all scheduled datasets.
    columns=list(dict.fromkeys(k for r in solver for k in r))
    write_tsv(out/f'{stem}_solver_20260920.tsv',[{k:r.get(k,'') for k in columns} for r in solver])
    sensitivity=[]
    try:
        for clip in (1.,1.345,1.5):
            historical.C=clip;historical.population.cache_clear()
            fit,mom,(target,_,cx,cy)=historical.population()
            sensitivity.append(dict(log_sd=.6,latent_rho=.4,c=clip,k=K,ck=clip*K,reference=fit[3],rho_p=target,coefficient_x=cx))
    finally:
        historical.C=1.345;historical.population.cache_clear()
    write_tsv(out/f'{stem}_constant_sensitivity_20260920.tsv',sensitivity)
    valid=[r for r in solver if not r['error']]
    report=dict(protocol_sha256=hashlib.sha256((ROOT/'docs/moderate_benchmark_protocol_20260920.md').read_bytes()).hexdigest(),
        datasets=6000,method_rows=len(rows),new_design_cells=3,failures=sum(bool(r['error']) for r in solver),
        method_error_rows=sum(bool(r['error']) for r in rows),
        residual_passes=sum(r[j+'_exact_residual_passed'] for r in valid for j in ('x','y')),
        solver_decisions_changed=sum(r['coverage_decision_changed'] for r in valid),
        max_estimate_delta_checked_se_units=max(abs(r['delta_estimate_checked_se_units']) for r in valid),
        max_relative_se_delta=max(abs(r['relative_se_delta']) for r in valid),
        max_sqrt_n_legacy_score_residual=max(r['sqrt_n_legacy_score_residual'] for r in valid),
        numerical_threshold_breaches=sum(abs(r['delta_estimate_checked_se_units'])>=1e-4 or abs(r['relative_se_delta'])>=1e-4 for r in valid),
        frozen_inputs_unchanged=all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in original.items()),
        original_tsv_sha256=original,elapsed_seconds=time.perf_counter()-started,
        sources={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ('src/cdelta.py','scripts/run_moderate_benchmark_20260920.py','scripts/validate_active_nuisance_20260907.py')},
        environment=dict(python=platform.python_version(),executable=sys.executable,isolated_venv=sys.prefix!=sys.base_prefix,packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}))
    assert report['frozen_inputs_unchanged']
    (out/f'{stem}_audit_20260920.json').write_text(json.dumps(report,indent=2)+'\n')
    print('COMPLETE', {k:v for k,v in report.items() if k not in ('sources','original_tsv_sha256','environment')},flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir',type=Path,required=True)
    run(parser.parse_args().out_dir)

