"""Deterministic full-text formula checks, not a competing-method experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

def run(source):
    x=np.array([1.,3.,4.,6.,6.5]); y=np.array([1.,4.,2.,9.,6.]); m=1.5
    p=np.median(y-m*x); pc=np.median(y+m*x)
    sa=np.sum(abs(y-m*x-p)); sb=np.sum(abs(y+m*x-pc))
    slopes={float((y[i]-y[j])/(x[i]-x[j])) for i in range(5) for j in range(i)}
    slopes |= {-v for v in slopes}|{0.}
    def ratio(h):
        return np.sum(abs(y-h*x-np.median(y-h*x)))/np.sum(abs(y+h*x-np.median(y+h*x)))
    best=min(slopes,key=ratio)
    assert p==-.5 and pc==8.5 and best==1.5 and round(1-sa/sb,2)==.69
    xx=np.array([-3.,-1.,0.,1.,3.]); yy=-xx
    assert np.median(xx)==np.median(yy)==0
    assert np.sum(abs(yy+xx))==0 and np.sum(abs(yy-xx))>0
    assert np.corrcoef(abs(xx),abs(yy))[0,1]==1
    return dict(source_pdf_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        source_pages='5853-5855, 5862', paper_table1=dict(x=x.tolist(),y=y.tolist(),
        best_slope=best,intercept=p,counter_intercept=pc,SAE_positive=sa,SAE_negative=sb,
        q=sa/sb,r_prime=1-sa/sb), exact_separating_example=dict(x=xx.tolist(),y=yy.tolist(),
        pareto_r_prime=-1,profile_correlation=1,reference_x=0,reference_y=0),
        scope='deterministic formula checks; not an implementation or simulation comparison; endpoint example is outside positive-IF-variance Wald conditions',
        all_passed=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    if args.report.exists():raise FileExistsError('Use a fresh report path')
    result=run(args.source)
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print('Formula checks passed')
