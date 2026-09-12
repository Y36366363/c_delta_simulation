"""Bounded replay of existing datasets and full-IF bracketed-root sensitivity.

Selection was fixed in docs/manuscript_interface_protocol_20260912.md.
Never writes frozen results. This is not a new Monte Carlo study.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import scipy
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.cdelta import huber_profile_correlation_inference, _gaussian_kde_density
from scripts.run_reference_pathway_20260909 import generate, one_stage, profile_result, STAGES
from scripts.validate_active_nuisance_20260907 import direct_estimate_se

REPS=(0,1,2,10,100,500,1000,1500,1999)
K,C,Z=1.4826,1.345,1.959963984540054
TRUTH,TPOP=.19347511885804566,1.079808860961767

def read(name):
    with (ROOT/'results'/name).open() as f:
        return list(csv.DictReader(f,delimiter='\t'))

def bracket(w):
    m=float(np.median(w)); d=float(np.median(abs(w-m))); s=K*d
    score=lambda t: float(np.mean(np.clip((w-t)/s,-C,C)))
    t=brentq(score,float(w.min()),float(w.max()),xtol=1e-13)
    fm,fp,fn=(_gaussian_kde_density(w,u) for u in (m,m+d,m-d))
    im=(.5-(w<=m))/fm
    id_=(.5-(abs(w-m)<=d)-(fp-fn)*im)/(fp+fn)
    u=(w-t)/s; active=abs(u)<C; a=float(np.mean(active)); b=float(np.mean(u*active))
    it=s/a*np.clip(u,-C,C)-b/a*K*id_
    return t,s,it

def sensitivity(x,y,truth,meta):
    f=huber_profile_correlation_inference(x,y,null_value=truth)
    tx,sx,ix=bracket(x); ty,sy,iy=bracket(y)
    rho,_,se,dse=profile_result(x,y,tx,ty,ix,iy)
    _,base_dse=direct_estimate_se(x,y,f['reference_location_x'],f['reference_location_y'])
    base_rho=float(f['estimate']); base_se=float(f['standard_error'])
    rootgap=max(abs(tx-f['reference_location_x'])/sx,abs(ty-f['reference_location_y'])/sy)
    score=max(abs(np.mean(np.clip((w-f['reference_location_'+label])/s,-C,C)))
              for w,label,s in ((x,'x',sx),(y,'y',sy)))
    return {**meta,'n':len(x),'truth':truth,
        'sqrt_n_score_residual':float(np.sqrt(len(x))*score),
        'root_gap_scale_units':float(rootgap),'estimate_change':rho-base_rho,
        'estimate_change_over_original_se':(rho-base_rho)/base_se,
        'relative_full_se_change':se/base_se-1,'relative_direct_se_change':dse/base_dse-1,
        'full_decision_changed':int((abs(rho-truth)<=Z*se)!=(abs(base_rho-truth)<=Z*base_se)),
        'direct_decision_changed':int((abs(rho-truth)<=Z*dse)!=(abs(base_rho-truth)<=Z*base_dse))}

def run():
    skew={ (int(r['n']),int(r['replication']),r['method']):r
          for r in read('active_nuisance_replications_20260907.tsv') }
    pathway={ (float(r['tau']),int(r['n']),int(r['replication']),r['stage']):r
          for r in read('reference_pathway_replications_20260909.tsv') }
    rows=[]; gaps=[]; records=0; decisions=0
    def compare(actual,stored,fields,decision_fields):
        nonlocal records,decisions
        assert not stored['error']
        for a,b in fields:
            gap=abs(float(actual[a])-float(stored[b]))/max(1,abs(float(stored[b])))
            gaps.append(gap)
            assert gap<1e-10,(a,b,gap)
        for a,b in decision_fields:
            assert int(actual[a])==int(stored[b]),(a,b)
            decisions+=1
        records+=1
    for n in (160,640,2560):
        for rep in REPS:
            rng=np.random.default_rng(np.random.SeedSequence([2026090701,n,rep]))
            z=rng.standard_normal((n,2)); x=np.exp(.6*z[:,0]); y=np.exp(.6*(.4*z[:,0]+np.sqrt(1-.4**2)*z[:,1]))
            full=huber_profile_correlation_inference(x,y,null_value=TRUTH)
            methods={'complete_kde':(full['estimate'],full['standard_error']),
                     'direct_only_ablation':direct_estimate_se(x,y,full['reference_location_x'],full['reference_location_y']),
                     'oracle_fixed_reference':direct_estimate_se(x,y,TPOP,TPOP)}
            for method,(rho,se) in methods.items():
                compare({'estimate':rho,'se':se,'covered':abs(rho-TRUTH)<=Z*se},skew[n,rep,method],
                        [('estimate','estimate'),('se','se')],[('covered','covered')])
            rows.append(sensitivity(x,y,TRUTH,{'study':'skew','tau':'NA','replication':rep,'previous_flag':0}))
    for tau in (.1,.4):
        for n in (80,640):
            reps=(0,1,1999,70,1622) if (tau,n)==(.1,640) else (0,1,1999)
            for rep in reps:
                x,y=generate(tau,n,rep)
                for stage in STAGES:
                    actual=one_stage(x,y,stage)
                    fields=('estimate','historical_C','se_stage_aware','se_direct_only','reference_x','reference_y','scale_x','scale_y')
                    ds=('reject_stage_aware','reject_direct_only')
                    compare(actual,pathway[tau,n,rep,stage],[(k,k) for k in fields],[(k,k) for k in ds])
                rows.append(sensitivity(x,y,0.,{'study':'pathway','tau':tau,'replication':rep,'previous_flag':int(rep in (70,1622))}))
    metrics=('sqrt_n_score_residual','root_gap_scale_units','estimate_change','estimate_change_over_original_se','relative_full_se_change','relative_direct_se_change')
    summaries={}
    for study in ('skew','pathway'):
        chosen=[r for r in rows if r['study']==study]
        summaries[study]={'datasets':len(chosen),**{ 'max_abs_'+k:max(abs(r[k]) for r in chosen) for k in metrics},
                          'full_decisions_changed':sum(r['full_decision_changed'] for r in chosen),
                          'direct_decisions_changed':sum(r['direct_decision_changed'] for r in chosen)}
    files=('src/cdelta.py','scripts/run_reference_pathway_20260909.py',
           'scripts/validate_active_nuisance_20260907.py','scripts/replay_manuscript_interfaces_20260912.py',
           'docs/manuscript_interface_protocol_20260912.md','requirements-manuscript-audit.txt',
           'results/active_nuisance_replications_20260907.tsv','results/reference_pathway_replications_20260909.tsv')
    report={'scope':'bounded existing-seed replay; not full Monte Carlo reproduction or solver convergence theorem',
            'new_simulation_cells':0,'existing_datasets_replayed':len(rows),'saved_method_stage_rows_checked':records,
            'saved_decisions_checked':decisions,'max_scale_normalized_saved_gap':max(gaps),
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                           'executable':sys.executable,'prefix':sys.prefix,'base_prefix':sys.base_prefix,
                           'isolated_venv':sys.prefix!=sys.base_prefix},
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},
            'summaries':summaries,'rows':rows,'all_replay_checks_passed':True}
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args(); report=run()
    args.report.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ('existing_datasets_replayed','saved_method_stage_rows_checked','saved_decisions_checked','max_scale_normalized_saved_gap','environment','summaries')}))
