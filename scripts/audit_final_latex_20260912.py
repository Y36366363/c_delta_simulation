"""Read the actual single-file LaTeX and reconcile all 19 existing tables.

No source writes. Table data come from the dated integration calculations,
whose sources and bounded stored-reference replay remain separately audited.
This checks table cells and row identity, not every numerical claim in prose.
"""
from __future__ import annotations
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.integrate_manuscript_20260911 import make_tables
from scripts.audit_manuscript_completion_20260910 import build_audit

MAP = {
    'S2.1': 'bridge', 'S2.2': 'matched', 'S2.3': 'prospective',
    'S3.1': 'wald_seeds', 'S3.2': 'pathway_all',
    'S3.3': 'pathway_refs', 'S3.4': 'pathway_pairs', 'S3.5': 'skew_full',
    'S3.6': 'skew_uncertainty', 'S3.7': 'skew_pairs', 'S3.8': 'c_summaries',
    'S3.9': 'skew_diagnostics', 'S3.10': 'root_flags',
    'S3.11': 'permutation_seeds', 'S3.12': 'source_ledger',
    'regular': 'main_wald', 'coverage': 'main_skew',
    'stages': 'main_pathway', 'references': 'main_reference',
}
NUM = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')

def normal(s):
    s = s.replace(r'\allowbreak{}', '').replace(r'\texttt', '')
    s = s.replace(r'\_', '_').replace(r'\%', '%').replace('$', '')
    s = s.replace('{', '').replace('}', '').replace('−', '-').replace('–','--')
    return re.sub(r'\s+', '', s)

def equivalent(a, b):
    a, b = normal(a), normal(b)
    # Keep NA distinct from 0, family/stage names and punctuation intact.
    if NUM.sub('#', a) != NUM.sub('#', b):
        return False
    return [Decimal(x) for x in NUM.findall(a)] == [Decimal(x) for x in NUM.findall(b)]

def markdown_rows(s):
    lines = [x for x in s.splitlines() if x.startswith('|')]
    return [[v.strip() for v in x.strip('|').split('|')] for x in lines[2:]]

def extract(text):
    found = {}
    for block in re.findall(r'\\begin\{table\}.*?\\end\{table\}', text, re.S):
        ident = re.search(r'\\label\{tab:([^}]+)\}', block)
        if ident is None:
            ident = re.search(r'\\textbf\{Table (S\d+\.\d+)\.\}', block)
        if ident is None:
            raise AssertionError('Table without a recognized identity')
        name = ident[1]
        if name in found:
            raise AssertionError('Duplicate table: ' + name)
        data = block.split(r'\midrule', 1)[1].split(r'\bottomrule', 1)[0]
        data = data.replace(r'\midrule', '')
        found[name] = [[v.strip() for v in row.split('&')]
                       for row in data.split(r'\\') if row.strip()]
    return found

def expected_rows(tables):
    expected = {name: markdown_rows(tables[key]) for name, key in MAP.items()}
    aliases = {'Normal/sign':'Normal-margin shared sign',
               't5':r'Independent $t_5$', 'Strong skew':'Independent strong skew'}
    expected['regular'] = [[aliases[r[0]]] + r[1:]
                           for r in expected['regular'] if r[1] in ('640','2560')]
    for r in expected['stages']:
        r[1] = {'Fixed ref.':'Fixed reference', 'Full':'Full fit'}.get(r[1], r[1])
    labels = {'R':'Fixed reference', 'S':'Fixed scale', 'M':'Fixed median', 'F':'Full fit'}
    expected['references'] = [[labels[r[0]]] + r[1:4] for r in expected['references']]
    return expected

def validate(text, tables):
    found, expected = extract(text), expected_rows(tables)
    assert set(found) == set(expected), ('table identities', set(found)^set(expected))
    count = 0
    for name, rows in expected.items():
        actual = found[name]
        assert len(actual) == len(rows), (name, 'row count', len(actual), len(rows))
        for i, (got, want) in enumerate(zip(actual, rows)):
            assert len(got) == len(want), (name, i, 'column count')
            for j, (a,b) in enumerate(zip(got, want)):
                assert equivalent(a,b), (name, i, j, a, b)
                count += 1
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    assert len(labels) == len(set(labels)), 'Duplicate LaTeX label'
    citations = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text)
    used = {k.strip() for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}', text) for k in group.split(',')}
    assert used <= set(citations), ('Unresolved citation keys', used-set(citations))
    refs = re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', text)
    assert set(refs) <= set(labels), ('Unresolved references', set(refs)-set(labels))
    return {'tables_checked':len(found), 'cells_checked':count,
            'all_passed':True, 'scope':'table bodies, table identities, citation and reference keys; not all prose numbers'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tex', type=Path)
    parser.add_argument('--report', type=Path)
    args=parser.parse_args()
    prior=build_audit()
    assert prior['all_passed'], 'Historical provenance failure; investigate before proceeding'
    tables,replay=make_tables()
    result=validate(args.tex.read_text(), tables)
    result.update(tex=str(args.tex.resolve()), sha256=hashlib.sha256(args.tex.read_bytes()).hexdigest(),
                  historical_checks=len(prior['checks']), bounded_stored_reference_replay=replay)
    if args.report:
        args.report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ('tables_checked','cells_checked','all_passed','sha256','scope')}))

if __name__ == '__main__':
    main()
