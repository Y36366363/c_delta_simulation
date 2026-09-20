"""Check the new bounded study against stored draws, exact residuals and derivatives."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import norm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import run_moderate_benchmark_20260920 as model
from scripts.validate_active_nuisance_20260907 import summarize,paired_differences
from scripts.reproduce_core_studies_20260916 import compare

def read(name):
    with (ROOT/'results'/f'moderate_benchmark_{name}_20260920.tsv').open() as f:
        return list(csv.DictReader(f,delimiter='\t'))

def exact_residual_ok(row, margin):
    value=Fraction(int(row[margin+'_score_exact_numerator']),int(row[margin+'_score_exact_denominator']))
    return abs(value)<=Fraction(1,10**8*int(row['n']))

def run():
    rows=read('replications');solver=read('solver');summary=read('summary');paired=read('paired')
    assert len(rows)==18000 and len(solver)==6000
    ids={(int(r['n']),int(r['replication']),r['method']) for r in rows}
    assert len(ids)==18000
    methods=('complete_kde','direct_only_ablation','oracle_fixed_reference')
    assert ids=={(n,i,m) for n in (160,640,2560) for i in range(2000) for m in methods}
    for r in rows:
        assert not r['error'] and int(r['root_seed'])==2026092001
        assert np.isfinite(float(r['estimate'])+float(r['se'])) and float(r['se'])>0
        assert int(r['covered'])==int(abs(float(r['estimate'])-float(r['truth']))<=norm.ppf(.975)*float(r['se']))
    assert len({(r['n'],r['replication']) for r in solver})==6000
    assert all(not r['error'] and exact_residual_ok(r,j) for r in solver for j in ('x','y'))
    # Convert stored strings to the numeric API expected by the old summarizer.
    numeric=[{k:v if k in ('method','error') else float(v) for k,v in r.items()} for r in rows]
    numeric=[{**r,'n':int(r['n']),'replication':int(r['replication']),'root_seed':int(r['root_seed'])} for r in numeric]
    base=summarize(numeric)
    want=[{k:r[k] for k in base[0]} for r in summary]
    assert compare(base,want,('n','method'))['passed']
    assert compare(paired_differences(numeric),paired,('n',))['passed']
    for r in summary:
        cell=[v for v in rows if v['n']==r['n'] and v['method']==r['method']]
        assert int(r['below_truth_misses'])==sum(float(v['z']) < -norm.ppf(.975) for v in cell)
        assert int(r['above_truth_misses'])==sum(float(v['z']) > norm.ppf(.975) for v in cell)
    # Post-run validation of the copied numerical engine: four contamination directions.
    derivatives=[];rho=model.population()[2][0]
    for probs in ((.99,.99),(.99,.60),(.55,.45),(.01,.99)):
        x,y=np.exp(model.SIGMA*norm.ppf(probs));eps=1e-6
        direct,nuisance,_=model.population_if(x,y);analytic=float(direct+nuisance)
        tx,ty=model.marginal_fit(eps,x)[3],model.marginal_fit(eps,y)[3]
        mix=model.moments(tx,ty);a,b=abs(x-tx),abs(y-ty)
        for k,v in dict(cross=a*b,mean_x=a,mean_y=b,square_x=a*a,square_y=b*b).items():mix[k]=(1-eps)*mix[k]+eps*v
        fd=(model.rho_gradient(mix)[0]-rho)/eps
        gap=abs(fd-analytic)/(1+abs(analytic))
        derivatives.append(dict(probabilities=probs,analytic=analytic,finite_difference=fd,scaled_error=gap))
        assert gap<5e-4
    # Normal-model conventions, calculated rather than borrowed as guarantees.
    c=1.345;a=2*norm.cdf(c)-1
    epsi2=a-2*c*norm.pdf(c)+c*c*(1-a)
    old=json.loads((ROOT/'results/moderate_benchmark_audit_20260920.json').read_text())
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in old['original_tsv_sha256'].items())
    return dict(all_passed=True,method_rows=18000,solver_rows=6000,exact_marginal_residuals=12000,
        derivative_checks=derivatives,normal_mad_factor=1/norm.ppf(.75),normal_huber_efficiency=a*a/epsi2,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        note='Post-run deterministic validation, not a new design or independent proof review')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    if args.report.exists():raise FileExistsError('Use a fresh report path')
    r=run();args.report.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
