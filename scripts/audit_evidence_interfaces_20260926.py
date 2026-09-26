"""Independent bounded checks of retained S2/S3 claims; no new designs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta, expon, halfnorm, lognorm, uniform

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run_reference_pathway_20260909 import generate
from scripts.run_profile_bridge_family_validation_20260817 import generate_family_bridge_profile_null
from scripts.run_studentized_permutation_weak_null_20260814 import profile_studentized_permutation_test, random_indices
from src.cdelta import huber_profile_correlation_inference, _huber_location_influence

K, C = 1.4826, 1.345


def read(name):
    with (ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def symmetric_index(family, epsilon, n):
    """Symmetry makes J diagonal; no historical Jacobian routine is used."""
    families = {"uniform": uniform(0, 1), "exponential": expon(scale=1),
                "half_normal": halfnorm(scale=np.sqrt(2 / np.pi)),
                "scaled_beta12": beta(1, 2, scale=2)}
    if family == "hyperexponential":
        qc = lambda x: .5 * expon(scale=2).cdf(x) + .5 * expon(scale=2/3).cdf(x)
        qp = lambda x: .5 * expon(scale=2).pdf(x) + .5 * expon(scale=2/3).pdf(x)
    else:
        qc, qp = families[family].cdf, families[family].pdf
    radial = lognorm(s=.1)
    cdf = lambda x: (1-epsilon) * radial.cdf(x) + epsilon * qc(x)
    pdf = lambda x: (1-epsilon) * radial.pdf(x) + epsilon * qp(x)
    d = brentq(lambda x: cdf(x)-.5, .1, 2., xtol=1e-14)
    diagonal = [d * epsilon / 2, d * pdf(d), -cdf(C*K*d) / K]
    return np.sqrt(n) * min(abs(v) for v in diagonal), diagonal, d


def bridge_indices():
    frozen = {(r["scenario"], int(r["n"])): float(r["sqrt_n_minimum_singular_value"])
              for r in read("nuisance_jacobian_joined_cells_20260817.tsv")}
    records = []
    for panel in ("pilot", "confirmatory"):
        for r in read(f"profile_bridge_family_validation_{panel}_20260817.tsv"):
            n, e = int(r["n"]), float(r["bridge_probability"])
            index, diagonal, d = symmetric_index(r["bridge_family"], e, n)
            saved = frozen[r["scenario"], n]
            records.append(dict(panel=panel, family=r["bridge_family"], n=n, epsilon=e,
                diagonal=diagonal, raw_mad=d, computed=index, saved=saved, absolute_gap=abs(index-saved)))
    for r in read("claim3_prospective_family_validation_20260825.tsv"):
        n, e = int(r["n"]), float(r["bridge_probability"])
        index, diagonal, d = symmetric_index("hyperexponential", e, n)
        saved = float(r["conditioning_index"])
        records.append(dict(panel="prospective", family="hyperexponential", n=n, epsilon=e,
            diagonal=diagonal, raw_mad=d, computed=index, saved=saved, absolute_gap=abs(index-saved)))
    assert len(records) == 34
    assert max(r["absolute_gap"] for r in records) < 1e-10
    return records


def severe_linearity():
    rows = [r for r in read("reference_pathway_replications_20260909.tsv")
            if float(r["tau"]) == .1 and r["stage"] in ("population_scale", "population_median")]
    assert len(rows) == 8000
    arrays = {}
    max_residual = max_mean_gap = max_if_gap = 0.
    for r in rows:
        key = int(r["n"]), int(r["replication"])
        if key not in arrays:
            arrays[key] = generate(.1, *key)
        for j, w in zip(("x", "y"), arrays[key]):
            t, s = float(r["reference_"+j]), float(r["scale_"+j])
            u = (w-t)/s
            max_residual = max(max_residual, float(np.max(abs(u))))
            max_mean_gap = max(max_mean_gap, abs(t-float(w.mean())))
            # In the realized linear regime A=1 and B is the empirical mean
            # score. For stage3 retain the actual KDE/MAD path separately.
            assert float(r["active_fraction_"+j]) == 1.
            max_if_gap = max(max_if_gap, float(np.max(abs(s*np.clip(u,-C,C)-(w-w.mean())))))
    assert max_residual < C and max_mean_gap < 1e-12 and max_if_gap < 1e-12
    return dict(stage_rows=8000, distinct_existing_datasets=len(arrays), marginal_fits=16000,
                max_absolute_standardized_residual=max_residual, clipping_threshold=C,
                max_absolute_location_minus_sample_mean=max_mean_gap,
                max_fixed_scale_if_minus_centered_observation=max_if_gap,
                scope="Original draws regenerated at stored references; no fitting or new scientific design.")


def centered_complete_if(x,y):
    """Reconstruct Section S3.2 directly without five-moment gradients."""
    kwargs=dict(huber_c=C,density_method="kde",analytic_density=None,density_folds=5,density_seed=2026081401)
    tx,_,ix=_huber_location_influence(x,**kwargs)
    ty,_,iy=_huber_location_influence(y,**kwargs)
    a,b=abs(x-tx),abs(y-ty)
    ac,bc=a-a.mean(),b-b.mean()
    va,vb=np.mean(ac*ac),np.mean(bc*bc)
    D=np.sqrt(va*vb);rho=np.mean(ac*bc)/D
    gx,gy=np.mean(np.sign(x-tx)),np.mean(np.sign(y-ty))
    hx,hy=np.mean(np.sign(x-tx)*b),np.mean(np.sign(y-ty)*a)
    gamma_x=(-hx+b.mean()*gx)/D+rho*(np.mean(x-tx)-a.mean()*gx)/va
    gamma_y=(-hy+a.mean()*gy)/D+rho*(np.mean(y-ty)-b.mean()*gy)/vb
    direct=ac*bc/D-rho/2*(ac*ac/va+bc*bc/vb)
    influence=direct+gamma_x*ix+gamma_y*iy
    influence-=influence.mean()
    return influence, gamma_x, gamma_y


def orbit_crosscheck():
    records = []
    for family_i, family in enumerate(("uniform", "exponential", "half_normal", "scaled_beta12")):
        n, e = 80, .05
        seed = 2026081750+n+round(10000*e)+100000*family_i
        rng = np.random.default_rng(seed)
        x, y = generate_family_bridge_profile_null(rng,n,radial_log_sd=.1,bridge_probability=e,bridge_family=family)
        # First three orbit members are a prefix of the stored-cell procedure;
        # this is an implementation check, not a new p-value estimate.
        indices = random_indices(rng,n,3)
        cached = profile_studentized_permutation_test(x,y,indices)
        initial = huber_profile_correlation_inference(x,y)
        max_z_gap = abs(initial["z_statistic"]-cached["z_statistic"])
        max_ref_gap = 0.
        max_if_gap=max_gamma_gap=0.
        for i, p in enumerate([np.arange(n),*indices],start=-1):
            fresh = huber_profile_correlation_inference(x,y[p])
            if i>=0:
                max_z_gap = max(max_z_gap,abs(fresh["z_statistic"]-cached["permuted_z"][i]))
            for j in ("x", "y"):
                max_ref_gap=max(max_ref_gap,abs(fresh["reference_location_"+j]-initial["reference_location_"+j]))
            independent_if,gx,gy=centered_complete_if(x,y[p])
            max_if_gap=max(max_if_gap,float(np.max(abs(independent_if-fresh["influence"]))))
            max_gamma_gap=max(max_gamma_gap,abs(gx-fresh["location_coefficient_x"]),abs(gy-fresh["location_coefficient_y"]))
        assert max_z_gap < 1e-9 and max_ref_gap < 1e-12 and max_if_gap<1e-9 and max_gamma_gap<1e-10
        records.append(dict(family=family,n=n,epsilon=e,seed=seed,original_replication=0,
                            sampled_orbit_members=3,max_z_gap=max_z_gap,max_reference_gap=max_ref_gap,
                            max_centered_vs_five_moment_if_gap=max_if_gap,max_gamma_gap=max_gamma_gap))
    return records


def main(path):
    if path.exists():
        raise FileExistsError("Preserve existing reports")
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/"results").glob("*.tsv")}
    out=dict(date="2026-09-26", bridge_indices=bridge_indices(), severe_linearity=severe_linearity(),
             orbit_crosschecks=orbit_crosscheck(),new_design_cells=0,all_passed=True)
    out["frozen_tsv_unchanged"]=all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==v for p,v in hashes.items())
    assert out["frozen_tsv_unchanged"]
    out["source_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out["scope"]="Deterministic source/evidence interfaces; not mathematical peer review, fresh calibration, or new family exploration."
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("all_passed","new_design_cells","frozen_tsv_unchanged","severe_linearity")},indent=2))


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--report",type=Path,required=True)
    main(p.parse_args().report)
