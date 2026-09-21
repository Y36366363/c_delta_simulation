"""Audit the integrated author LaTeX against frozen tables and the prior proof.

Read-only: checks all 21 numerical tables, selected new claims, preserved
proof blocks and references. This is not mathematical peer review.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_final_latex_20260912 import extract, equivalent, make_tables, validate as old_validate
from scripts.audit_manuscript_completion_20260910 import build_audit

EXTRA = {'S3.13', 'S3.14'}

def load_summary():
    with (ROOT / 'results/moderate_benchmark_summary_20260920.tsv').open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def expected_new(summary):
    out = {key: [] for key in EXTRA}
    labels = {'complete_kde': 'F', 'direct_only_ablation': 'D', 'oracle_fixed_reference': 'O'}
    for r in summary:
        prefix = [r['n'], labels[r['method']]]
        out['S3.13'].append(prefix + [
            f"{float(r['coverage']):.4f}", f"{float(r['coverage_mcse']):.5f}",
            f"[{float(r['wilson_low']):.4f},{float(r['wilson_high']):.4f}]",
            f"{int(r['below_truth_misses']) / int(r['valid']):.4f}",
            f"{int(r['above_truth_misses']) / int(r['valid']):.4f}"])
        out['S3.14'].append(prefix + [f"{float(r[k]):.{digits}f}" for k, digits in
            [('bias',5),('bias_mcse',5),('empirical_sd',5),('mean_se',5),('se_sd_ratio',4),('mean_width',4)]])
    return out

def segment(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

def validate(text, old, tables, summary):
    all_found = extract(text)
    assert set(all_found) == set(extract(old)) | EXTRA, 'Changed numerical table inventory'
    def remove_new(match):
        block = match[0]
        return '' if any(r'\textbf{Table ' + k + '.}' in block for k in EXTRA) else block
    historical = re.sub(r'\\begin\{table\}.*?\\end\{table\}', remove_new, text, flags=re.S)
    prior = old_validate(historical, tables)
    new_cells = 0
    for key, rows in expected_new(summary).items():
        assert len(all_found[key]) == len(rows), (key, 'row count')
        for i, (got, want) in enumerate(zip(all_found[key], rows)):
            assert len(got) == len(want), (key, i, 'column count')
            for j, (a,b) in enumerate(zip(got,want)):
                assert equivalent(a,b), (key,i,j,a,b)
                new_cells += 1
    # Preserve the accepted mathematical argument; changes here require a new review.
    preserved = [
        ('Introduction', r'\section{Introduction}', r'\section{Profiles,'),
        ('Complete IF and theorem', r'\section{Complete influence-function inference}', r'\section{A worked'),
        ('Appendix A and B', r'\section{Regularity conditions and a compact proof route}', r'\section{Supplementary materials}'),
        ('S1.1--S1.6', r'\subsection*{S1.1', r'\subsection*{S1.7'),
        ('S2', r'\section*{Supplement S2.', r'\section*{Supplement S3.'),
    ]
    for name,a,b in preserved:
        assert segment(text,a,b) == segment(old,a,b), ('Unexpected change',name)
    assert text.split(r'\begin{document}')[0].replace('21 September 2026','18 September 2026') == old.split(r'\begin{document}')[0], 'Preamble changed'
    # Existing result table bodies must be byte-identical, not merely rounded equivalents.
    old_blocks = re.findall(r'\\begin\{table\}.*?\\end\{table\}', old, re.S)
    assert all(block in text for block in old_blocks), 'Historical table changed'
    keys = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text)
    assert len(keys)==len(set(keys)), 'Duplicate bibliography key'
    for required in ('all three Wilson intervals still\nexclude $.95$',
                     'This study did not yield the hoped-for\nnominal-coverage example.',
                     'not third-party preregistration',
                     'not independent reimplementation',
                     'Independent\nmathematical review remains outstanding',
                     'API default remains unchanged'):
        assert required in text, ('Missing scope qualification', required)
    assert 'mathematical review and full-study reproduction remain outstanding' not in text
    assert 'scripts/audit\\_integrated\\_latex\\_20260921.py' in text
    for r in summary:
        assert int(r['valid']) == 2000 and int(r['failures']) == 0
    return {'all_passed':True,'historical_tables_checked':prior['tables_checked'],
        'historical_cells_checked':prior['cells_checked'],'new_tables_checked':2,
        'new_cells_checked':new_cells,'numerical_tables_total':21,
        'preserved_blocks':[r[0] for r in preserved],
        'scope':'Numerical tables, selected scope qualifications, preserved text and citation/reference keys; not proof validity or every prose number.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('tex',type=Path);p.add_argument('--report',type=Path)
    a=p.parse_args()
    delivery=json.loads((ROOT/'results/manuscript_delivery_20260918.json').read_text())
    old_path=Path(delivery['manuscript']['tex']);old=old_path.read_text()
    assert hashlib.sha256(old_path.read_bytes()).hexdigest()==delivery['manuscript']['tex_sha256']
    frozen=json.loads((ROOT/'results/completion_delivery_20260920.json').read_text())
    assert all(hashlib.sha256((ROOT/key).read_bytes()).hexdigest()==value for key,value in frozen['evidence_sha256'].items())
    historical=build_audit();assert historical['all_passed']
    tables,replay=make_tables()
    result=validate(a.tex.read_text(),old,tables,load_summary())
    result.update(tex=str(a.tex.resolve()),tex_sha256=hashlib.sha256(a.tex.read_bytes()).hexdigest(),
        audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        historical_checks=len(historical['checks']),bounded_stored_reference_replay=replay,
        new_frozen_evidence_hashes_checked=len(frozen['evidence_sha256']))
    if a.report:
        assert not a.report.exists(),'Use a fresh report path'
        a.report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='bounded_stored_reference_replay'},indent=2))

if __name__=='__main__':main()
