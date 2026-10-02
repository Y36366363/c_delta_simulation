"""Source reconciliation for the six-section Hoorn author revision.

No new numerical experiment or proof certification. Historic table identities
remain recognizable when their placement or captions change.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_final_latex_20260912 import extract,equivalent,expected_rows,make_tables
from scripts.audit_integrated_latex_20260921 import expected_new,load_summary
from scripts.audit_submission_interfaces_20260926 import check_keys
from scripts.audit_manuscript_completion_20260910 import build_audit

LEDGER_RELOCATIONS={
    'W':('Main Table 1; S3.1',r'Table~\ref{tab:regular}; S3.1'),
    'PS':('Main Tables 3--4; S3.2--3',r'Tables~\ref{tab:stages}--\ref{tab:references}; S3.2--3'),
    'AS':('Main Table 2; S3.5--6',r'Table~\ref{tab:coverage}; S3.5--6'),
}


def relocated_ledger(rows):
    output=[list(row) for row in rows]
    for row in output:
        if row[0] in LEDGER_RELOCATIONS:
            old,new=LEDGER_RELOCATIONS[row[0]]
            assert equivalent(row[1],old),('unexpected source-ledger cell',row)
            row[1]=new
    return output


def read(name):
    with (ROOT/'results'/name).open(newline='') as stream:
        return list(csv.DictReader(stream,delimiter='\t'))


def interval(row,lo,hi):
    return f"[{float(row[lo]):.4f},{float(row[hi]):.4f}]"


def expected_compact():
    stages={'population_reference':'Fixed reference','population_scale':'Fixed scale',
            'population_median':'Fixed median','full_fit':'Full fit'}
    staged=[]
    for row in read('reference_pathway_summary_20260909.tsv'):
        if float(row['tau']) != .1:continue
        staged.append([row['n'],stages[row['stage']],f"{float(row['mean_rho']):.4f}",
            f"{float(row['stage_aware_rate']):.4f}",interval(row,'stage_aware_wilson_low','stage_aware_wilson_high'),
            f"{float(row['direct_only_rate']):.4f}"])
    regular=[]
    labels={'profile_null_normal_sign_link':'Normal shared sign','independent_t5':r'Independent $t_5$',
            'independent_strong_skew':'Independent strong skew'}
    for row in read('claim1_wald_validation_20260823.tsv'):
        if int(row['n']) not in (640,2560):continue
        regular.append([labels[row['scenario']],row['n'],f"{float(row['rejection_rate']):.4f}",
                        interval(row,'wilson_95_low','wilson_95_high')])
    for filename,label in (('active_nuisance_summary_20260907.tsv',r'Lognormal SD $.6$'),
                           ('moderate_benchmark_summary_20260920.tsv',r'Lognormal SD $.3$')):
        for row in read(filename):
            if row['method'] != 'complete_kde':continue
            regular.append([label,row['n'],f"{float(row['coverage']):.4f}",interval(row,'wilson_low','wilson_high')])
    assert len(staged)==8 and len(regular)==10
    return {'staged_compact':staged,'regular_compact':regular}


def compact_table_latex():
    rows=expected_compact()
    staged=r'''\begin{table}[htbp]
\centering\small
\caption{Shared-sign reference pathway at $\tau=.10$. Each cell uses 2,000
paired datasets. Stage-aware and direct-only columns report empirical null
rejection at nominal .05; the interval describes Monte Carlo uncertainty.
These nonregular cells are mechanism evidence, not validity checks.}
\label{tab:staged_compact}
\begin{tabular}{rlrccc}
\toprule
$n$ & References & Mean $\widehat\rho_P$ & Stage-aware & 95\% Wilson & Direct-only\\
\midrule
'''
    staged+='\n'.join(' & '.join(row)+r' \\' for row in rows['staged_compact'])
    staged+='\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table}'+'\n'
    regular=r'''\begin{table}[htbp]
\centering\small
\caption{Selected complete-IF regular-law checks. The first four rows are
null rejection rates (nominal .05; 1,000 datasets per row); the remaining
rows are coverage probabilities (nominal .95; 2,000 datasets per row).
Wilson intervals describe Monte Carlo uncertainty. Both nonzero lognormal
laws have latent correlation $.4$. All direct-only and oracle comparisons
and all six original null cells remain in Supplement S3.}
\label{tab:regular_compact}
\begin{tabular}{lrcc}
\toprule
Law & $n$ & Rejection / coverage & 95\% Wilson\\
\midrule
'''
    regular+='\n'.join(' & '.join(row)+r' \\' for row in rows['regular_compact'])
    regular+='\n'+r'\bottomrule'+'\n'+r'\end{tabular}'+'\n'+r'\end{table}'+'\n'
    return {'staged_compact':staged,'regular_compact':regular}


def validate_tables(text,old,expected):
    expected={key:(relocated_ledger(rows) if key=='S3.12' else rows) for key,rows in expected.items()}
    found=extract(text)
    assert set(found)==set(expected),('table inventory',set(found)^set(expected))
    count=0
    for key,rows in expected.items():
        assert len(found[key])==len(rows),(key,'row count')
        for i,(actual,wanted) in enumerate(zip(found[key],rows)):
            assert len(actual)==len(wanted),(key,i,'column count')
            for j,(a,b) in enumerate(zip(actual,wanted)):
                assert equivalent(a,b),(key,i,j,a,b)
                count+=1
    old_found=extract(old)
    assert len(old_found)==21
    for key,rows in old_found.items():
        wanted=relocated_ledger(rows) if key=='S3.12' else rows
        assert found[key]==wanted,('historical numerical body changed',key)
    return dict(tables_checked=len(found),cells_checked=count,historical_tables=21,
                historical_cells=1182,selected_main_tables=2,selected_main_cells=count-1182,
                historical_rows_identical_except_declared_ledger_relocations=True,
                data_table_bodies_identical=20,declared_ledger_relocations=LEDGER_RELOCATIONS)


def run(tex):
    delivery=json.loads((ROOT/'results/manuscript_delivery_20261002.json').read_text())
    prior=Path(delivery['manuscript']['tex'])
    digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    assert digest(prior)==delivery['manuscript']['tex_sha256']
    old,new=prior.read_text(),tex.read_text()
    tables,replay=make_tables()
    expected={**expected_rows(tables),**expected_new(load_summary()),**expected_compact()}
    result=validate_tables(new,old,expected)
    assert r'\appendix' in new
    body=new.split(r'\appendix',1)[0]
    sections=re.findall(r'\\section\{',body)
    assert len(sections)==6,('main section count',len(sections))
    titles=re.findall(r'\\section\{([^}]+)\}',body)
    assert not any(re.search('conditioning|permutation',title,re.I) for title in titles),'conditioning/permutation promoted to a main section'
    assert set(extract(body))=={'staged_compact','regular_compact'},'main table inventory'
    assert set(extract(new.split(r'\appendix',1)[1]))==set(extract(old)),'retained supplement table inventory'
    historical=build_audit();assert historical['all_passed']
    moderate=json.loads((ROOT/'results/completion_delivery_20260920.json').read_text())['evidence_sha256']
    assert all(digest(ROOT/name)==saved for name,saved in moderate.items()),'moderate-study frozen evidence changed'
    selected_sources=('reference_pathway_summary_20260909.tsv','claim1_wald_validation_20260823.tsv',
                      'active_nuisance_summary_20260907.tsv','moderate_benchmark_summary_20260920.tsv')
    result.update(all_passed=True,key_counts=check_keys(new),main_sections=6,
        historical_checks=len(historical['checks']),tex=str(tex.resolve()),tex_sha256=digest(tex),
        prior_tex_sha256=digest(prior),audit_source_sha256=digest(__file__),
        selected_source_sha256={name:digest(ROOT/'results'/name) for name in selected_sources},
        moderate_frozen_files_checked=len(moderate),
        bounded_stored_reference_replay=replay,new_design_cells=0,
        scope='All retained and selected table rows, relocation inventory, references and source provenance; not mathematical proof, literature completeness or every prose number.')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tex',type=Path);p.add_argument('--report',type=Path)
    a=p.parse_args()
    if a.report and a.report.exists():raise FileExistsError('Use a new report path')
    out=run(a.tex)
    if a.report:a.report.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='bounded_stored_reference_replay'},indent=2))
