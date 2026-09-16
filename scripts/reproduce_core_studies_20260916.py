"""Reproduce two complete existing studies in a historical-source snapshot.

No default solver changes, new cells, or writes to frozen tables. Scope is
specified in docs/core_reproduction_protocol_20260916.md.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = '32f0dd80097bb1a7c207b18edcb8b54069ea473291627e649a717705a23d5be7'
TOLERANCE = 1e-10
EXACT = {'n','replication','root_seed','covered','reject_stage_aware','reject_direct_only',
         'replications','valid','failures','coverage_count','stage_aware_rejections',
         'direct_only_rejections','paired_valid','only_full_covers','only_direct_covers',
         'stage_aware_rejection_changed','direct_rejection_changed'}


def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f,delimiter='\t'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(actual, expected, keys):
    def index(rows):
        out={}
        for row in rows:
            key=tuple(str(row[k]) for k in keys)
            if key in out:
                raise ValueError('duplicate row '+str(key))
            out[key]=row
        return out
    a,b=index(actual),index(expected)
    if a.keys()!=b.keys():
        raise ValueError('row identities differ')
    mismatches=[];count=0;max_gap=0.;worst=None;exact_fields=0
    for key,row in a.items():
        if row.keys()!=b[key].keys():
            raise ValueError('column identities differ')
        for field,value in row.items():
            want=b[key][field];count+=1
            try:
                x,y=float(value),float(want)
            except (TypeError,ValueError):
                ok=str(value)==str(want)
            else:
                if not math.isfinite(x) or not math.isfinite(y):
                    ok=(math.isnan(x) and math.isnan(y)) or x==y
                elif field in EXACT or field in keys:
                    exact_fields+=1;ok=x==y
                else:
                    gap=abs(x-y)/max(1.,abs(y))
                    if gap>max_gap:max_gap,worst=gap,{'key':key,'field':field}
                    ok=gap<=TOLERANCE
            if not ok:
                mismatches.append({'key':key,'field':field,'actual':str(value),'stored':str(want)})
    return {'rows':len(a),'fields':count,'exact_numeric_fields':exact_fields,
            'max_scaled_numeric_gap':max_gap,'worst':worst,'mismatches':mismatches,
            'passed':not mismatches}


def run():
    start=time.perf_counter()
    snapshot=Path(tempfile.mkdtemp(prefix='rho_core_reproduction_20260916_')).resolve()
    for directory in ('src','scripts'):
        shutil.copytree(ROOT/directory,snapshot/directory,ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(ROOT/'archive/source_snapshots/cdelta_20260914.py',snapshot/'src/cdelta.py')
    assert digest(snapshot/'src/cdelta.py')==HISTORICAL
    sources={}
    for manifest,runner in [('active_nuisance_manifest_20260907.tsv','validate_active_nuisance_20260907.py'),
                            ('reference_pathway_manifest_20260909.tsv','run_reference_pathway_20260909.py')]:
        expected=next(r['sha256_lf'] for r in read(ROOT/'results'/manifest) if r['path']=='scripts/'+runner)
        raw=(snapshot/'scripts'/runner).read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')
        assert hashlib.sha256(raw).hexdigest()==expected
        sources['scripts/'+runner]=digest(snapshot/'scripts'/runner)
    sys.path.insert(0,str(snapshot))
    from scripts import validate_active_nuisance_20260907 as skew
    from scripts import run_reference_pathway_20260909 as pathway
    from scripts.robust_extension_utils import write_tsv
    import src.cdelta as core
    for module in (skew,pathway,core):
        assert Path(module.__file__).resolve().is_relative_to(snapshot)
    comparisons={};input_hashes={};output_hashes={}
    def check(name,rows,keys):
        original=ROOT/'results'/name
        before=digest(original);input_hashes[name]=before
        comparisons[name]=compare(rows,read(original),keys)
        path=snapshot/'reproduced'/name;write_tsv(path,rows)
        output_hashes[name]=digest(path)
        assert digest(original)==before
        print(name,comparisons[name]['rows'],'rows',comparisons[name]['passed'],flush=True)
    rows=skew.simulate()
    check('active_nuisance_replications_20260907.tsv',rows,('n','replication','method'))
    check('active_nuisance_summary_20260907.tsv',skew.summarize(rows),('n','method'))
    check('active_nuisance_paired_20260907.tsv',skew.paired_differences(rows),('n',))
    skew_errors=sum(bool(r['error']) for r in rows)
    rows=pathway.run()
    check('reference_pathway_replications_20260909.tsv',rows,('tau','n','replication','stage'))
    check('reference_pathway_summary_20260909.tsv',pathway.summarize(rows),('tau','n','stage'))
    check('reference_pathway_paired_20260909.tsv',pathway.paired(rows),('tau','n','from_stage','to_stage'))
    check('reference_pathway_model_checks_20260909.tsv',pathway.model_checks(),('tau',))
    check('reference_pathway_root_sensitivity_20260909.tsv',pathway.root_sensitivity(rows),('tau','n','replication'))
    assert all(digest(ROOT/'results'/p)==h for p,h in input_hashes.items())
    sources['src/cdelta.py']=digest(snapshot/'src/cdelta.py')
    # Hash every copied source, including imported helpers, for the run snapshot.
    snapshot_hashes={str(p.relative_to(snapshot)):digest(p)
                     for folder in ('src','scripts') for p in sorted((snapshot/folder).rglob('*.py'))}
    return {'scope':'complete replication arrays and listed derived tables for two core studies; not full project reproduction',
            'new_simulation_cells':0,'datasets_reproduced':14000,'replication_rows':50000,
            'skew_error_rows':skew_errors,'pathway_error_rows':sum(bool(r['error']) for r in rows),
            'all_passed':all(r['passed'] for r in comparisons.values()),'numeric_tolerance':TOLERANCE,
            'elapsed_seconds':time.perf_counter()-start,'snapshot':str(snapshot),
            'environment':{'python':platform.python_version(),'executable':sys.executable,
                           'isolated_venv':sys.prefix!=sys.base_prefix,
                           'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()}},
            'sources':sources,'snapshot_source_sha256':snapshot_hashes,
            'frozen_input_sha256':input_hashes,'reproduced_output_sha256':output_hashes,
            'frozen_inputs_unchanged':True,'comparisons':comparisons}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    if args.report.exists():raise FileExistsError('Choose a fresh report path')
    report=run()
    args.report.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ('datasets_reproduced','replication_rows','all_passed','elapsed_seconds','snapshot')},indent=2))
    if not report['all_passed']:raise SystemExit(1)
