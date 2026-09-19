"""Reproduce retained historical panels without writes to frozen evidence."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reproduce_core_studies_20260916 import read, digest, compare, HISTORICAL


def compare_retained(actual, expected, keys):
    """Require exact design/count/rate fields in addition to numeric agreement."""
    result = compare(actual, expected, keys)
    by_key = {tuple(str(r[k]) for k in keys):r for r in expected}
    fields = {'root_cell_seed','repetitions','valid_repetitions','n_perm','n_bootstrap',
        'observed_rejections','studentized_rejection','rejection_rate','observed_rejection_rate',
        'below_truth_miss_count','above_truth_miss_count','passed','order_per_interval'}
    for row in actual:
        key=tuple(str(row[k]) for k in keys)
        for field in fields & row.keys():
            if float(row[field]) != float(by_key[key][field]):
                result['mismatches'].append(dict(key=key,field=field,reason='exact field mismatch'))
    result['passed'] = not result['mismatches']
    return result


def bridge_job(snapshot, row):
    sys.path.insert(0, snapshot)
    import scripts
    scripts.__path__ = [str(Path(snapshot)/'scripts')]
    from scripts.run_profile_bridge_family_validation_20260817 import run_family_cell, BRIDGE_FAMILIES
    assert Path(sys.modules[run_family_cell.__module__].__file__).resolve().is_relative_to(snapshot)
    assert Path(sys.modules['cdelta'].__file__).resolve().is_relative_to(snapshot)
    n, eps, family = int(row['n']), float(row['bridge_probability']), row['bridge_family']
    result = run_family_cell(repetitions=int(row['repetitions']), n=n,
        n_perm=int(row['n_perm']), n_bootstrap=int(row['n_bootstrap']),
        seed=2026081750+n+round(10000*eps)+100000*BRIDGE_FAMILIES.index(family),
        phase=row['phase'], bridge_probability=eps, bridge_family=family)
    return result


def run(workers=4):
    start = time.perf_counter()
    snapshot = Path(tempfile.mkdtemp(prefix='rho_retained_20260918_')).resolve()
    for directory in ('src', 'scripts'):
        shutil.copytree(ROOT/directory, snapshot/directory, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(ROOT/'archive/source_snapshots/cdelta_20260914.py', snapshot/'src/cdelta.py')
    assert digest(snapshot/'src/cdelta.py') == HISTORICAL
    (snapshot/'results').mkdir()
    # Snapshot all TSV inputs so older fixed-output paths cannot touch the repository.
    for p in (ROOT/'results').glob('*.tsv'):
        shutil.copyfile(p, snapshot/'results'/p.name)
    input_hashes = {p.name:digest(p) for p in (ROOT/'results').glob('*.tsv')}
    comparisons = {}
    def check(name, rows, keys):
        result = compare_retained(rows, read(ROOT/'results'/name), keys)
        comparisons[name] = result
        from scripts.robust_extension_utils import write_tsv
        write_tsv(snapshot/'reproduced'/name, rows)
        print(name, 'PASS' if result['passed'] else 'FAIL', result['max_scaled_numeric_gap'], flush=True)
        if not result['passed']:
            print(json.dumps(result['mismatches'][:5]), flush=True)
            raise AssertionError(name)
        return rows
    print('SNAPSHOT', snapshot, flush=True)
    # Start independent historical cells. Every worker retains the original runner.
    names = ['profile_bridge_family_validation_pilot_20260817.tsv',
             'profile_bridge_family_validation_confirmatory_20260817.tsv']
    outputs = {name:[] for name in names}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(bridge_job, str(snapshot), r):name
                   for name in names for r in read(ROOT/'results'/name)}
        for future in as_completed(futures):
            name = futures[future]; row = future.result(); outputs[name].append(row)
            print('CELL', row['phase'], row['scenario'], row['n'], 'completed', flush=True)
    # Imports must resolve exclusively to the separate historical snapshot.
    sys.path.insert(0, str(snapshot))
    import scripts
    scripts.__path__ = [str(snapshot/'scripts')]
    from scripts import run_claim_validation_20260823 as wald
    from scripts import run_claim_external_validation_20260825 as prospective
    from scripts import run_nuisance_jacobian_20260817 as jac
    from scripts import audit_referee_readiness_20260908 as diagnostics
    from scripts import validate_active_nuisance_20260907 as skew
    from scripts.robust_extension_utils import write_tsv
    import src.cdelta as core
    for module in (wald, prospective, jac, diagnostics, skew, core):
        assert Path(module.__file__).resolve().is_relative_to(snapshot), module.__file__
    for name in names:
        # Match source row order before training: floating reduction order matters.
        lookup = {(r['scenario'],str(r['n'])):r for r in outputs[name]}
        ordered = [lookup[r['scenario'],r['n']] for r in read(ROOT/'results'/name)]
        check(name, ordered, ('scenario','n'))
        write_tsv(snapshot/'results'/name, ordered)
    check('claim1_wald_validation_20260823.tsv', wald.run_claim1(1000), ('scenario','n'))
    # Recompute population indices used in retained S2 cells and predictor fitting.
    joined = read(snapshot/'results/nuisance_jacobian_joined_cells_20260817.tsv')
    selected = {(r['scenario'],str(r['n'])) for r in outputs[names[0]]}
    expected, actual = [], []
    for r in joined:
        if (r['scenario'],r['n']) not in selected: continue
        family, eps = r['scenario'].rsplit('_epsilon_',1)
        nuisance = jac.population_nuisance(jac.symmetric_bridge_distribution(float(eps),family))
        new = dict(r)
        new['sqrt_n_minimum_singular_value'] = int(r['n'])**.5 * float(nuisance['minimum_singular_value'])
        expected.append({'scenario':r['scenario'],'n':r['n'],'index':r['sqrt_n_minimum_singular_value']})
        actual.append({'scenario':r['scenario'],'n':r['n'],'index':new['sqrt_n_minimum_singular_value']})
        r.update(new)
    assert len(actual)==24
    comparisons['retained_population_indices'] = compare(actual, expected, ('scenario','n'))
    assert comparisons['retained_population_indices']['passed']
    write_tsv(snapshot/'results/nuisance_jacobian_joined_cells_20260817.tsv', joined)
    rows, _ = prospective.claim3_prospective_family_validation(200,99)
    check('claim3_prospective_family_validation_20260825.tsv', rows, ('family','n','bridge_probability'))
    check('active_nuisance_population_20260907.tsv', [skew.tensor_check(k) for k in (24,48,72)], ('order_per_interval',))
    deriv = skew.contamination_checks()
    check('active_nuisance_derivative_20260907.tsv', deriv, tuple(list(deriv[0])[:2]))
    check('referee_coverage_diagnostics_20260908.tsv', diagnostics.coverage_diagnostics(), ('n','method','scale'))
    check('referee_root_replay_20260908.tsv', diagnostics.root_replay(), ('n','replication','margin'))
    unchanged = all(digest(ROOT/'results'/name)==h for name,h in input_hashes.items())
    assert unchanged
    return dict(all_passed=all(r['passed'] for r in comparisons.values()),
        scope='retained older Wald/S2 panels, population indices, skew quadrature/derivatives and post hoc diagnostics',
        new_simulation_cells=0, dataset_executions=12800, distinct_datasets=12200,
        overlap_note='600 pilot datasets recur in the four 500-dataset confirmations',
        permutations=673200, bootstrap_reference_fits=2228800,
        elapsed_seconds=time.perf_counter()-start, snapshot=str(snapshot), workers=workers,
        numeric_tolerance=1e-10, frozen_inputs_unchanged=unchanged,
        comparisons=comparisons, frozen_input_sha256=input_hashes,
        snapshot_source_sha256={str(p.relative_to(snapshot)):digest(p)
            for d in ('src','scripts') for p in sorted((snapshot/d).rglob('*.py'))},
        environment=dict(python=platform.python_version(), executable=sys.executable,
            isolated_venv=sys.prefix!=sys.base_prefix,
            packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()}))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=4)
    args=parser.parse_args()
    if args.report.exists(): raise FileExistsError('Use a fresh report path')
    result=run(args.workers)
    args.report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('ALL PASSED',result['all_passed'], 'SECONDS',result['elapsed_seconds'],flush=True)
