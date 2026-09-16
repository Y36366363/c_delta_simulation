"""Replay the existing 41-dataset selection through the integrated public API."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.cdelta import huber_profile_correlation_inference as infer
from scripts.audit_proof_solver_20260914 import datasets, candidate_margin
from scripts.run_reference_pathway_20260909 import profile_result, ZCRIT


def run(legacy_path):
    spec = importlib.util.spec_from_file_location('rho_legacy_audit', legacy_path)
    legacy = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = legacy
    spec.loader.exec_module(legacy)
    rows = []
    for meta, x, y in datasets():
        before = legacy.huber_profile_correlation_inference(x,y,null_value=meta['truth'])
        current = infer(x,y,null_value=meta['truth'])
        assert before.keys() == current.keys()
        for key in before:
            if isinstance(before[key], np.ndarray):
                np.testing.assert_array_equal(before[key], current[key])
            else:
                assert before[key] == current[key], (meta,key)
        start = time.perf_counter()
        out = infer(x,y,null_value=meta['truth'],reference_solver='score_checked')
        elapsed = time.perf_counter()-start
        tx,sx,ix,dx = candidate_margin(x)
        ty,sy,iy,dy = candidate_margin(y)
        rho,_,se,_ = profile_result(x,y,tx,ty,ix,iy)
        assert abs(out['estimate']-rho)<1e-12 and abs(out['standard_error']-se)<1e-12
        assert out['solver_diagnostics']['x']==dx and out['solver_diagnostics']['y']==dy
        rows.append({**meta, 'default_bitwise_equal':True,
            'estimate_delta':out['estimate']-current['estimate'],
            'relative_se_delta':out['standard_error']/current['standard_error']-1,
            'decision_changed':bool((abs(out['z_statistic'])<=ZCRIT)!=(abs(current['z_statistic'])<=ZCRIT)),
            'prototype_estimate_gap':out['estimate']-rho,'prototype_se_gap':out['standard_error']-se,
            'elapsed_seconds_including_exact_check':elapsed,'diagnostics':out['solver_diagnostics']})
    assert len(rows)==41
    return {'scope':'public API integration; same bounded selection, not new coverage evidence',
        'legacy_source_sha256':hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
        'current_source_sha256':hashlib.sha256((ROOT/'src/cdelta.py').read_bytes()).hexdigest(),
        'new_simulation_cells':0,'datasets':len(rows),'margins_checked':2*len(rows),
        'default_bitwise_equal_all':True,'prototype_matches_all':True,
        'decisions_changed':sum(r['decision_changed'] for r in rows),
        'max_abs_estimate_delta':max(abs(r['estimate_delta']) for r in rows),
        'max_abs_relative_se_delta':max(abs(r['relative_se_delta']) for r in rows),
        'rows':rows}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--legacy-source',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    if args.report.exists():
        raise FileExistsError('Choose a fresh audit output')
    result=run(args.legacy_source)
    args.report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
