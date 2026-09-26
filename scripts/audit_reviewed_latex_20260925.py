"""Read-only audit for the focused September 25 revision.

Reuse source reconciliation for 21 numerical tables while allowing only the
reviewed sign-boundary and KDE-context edits within S1.1--S1.6. Check the
new independent records and the environment qualification explicitly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_integrated_latex_20260921 import load_summary, make_tables, validate as validate21
from scripts.audit_manuscript_completion_20260910 import build_audit

PROOF_EDITS = [
    ('Signs are affine transformations of half-line indicators, with the value at equality treated separately on a probability-zero boundary.',
     r'''With $\operatorname{sign}(0)=0$, write
$\operatorname{sign}(w-t)=1\{w>t\}-1\{w<t\}$.
Both strict half-line indicator classes are VC, so finite-sum closure
handles the equality convention exactly, including when $t$ is
estimated from the sample.'''),
    (r'Partition its subgraph by \(x\le t\) and \(y\le u\). On each of four regions the function equals one of \(y-u,u-y,-(y-u),-(u-y)\).',
     r'''Partition its subgraph by the three cases $x<t$, $x=t$, and $x>t$,
and by $y\le u$ or $y>u$. The equality piece is identically zero;
on the remaining pieces the function is one of
$y-u,u-y,-(y-u),-(u-y)$.'''),
    ('is needed. The general uniform-KDE literature \\citep{gineguillou2002}\nprovides context; the argument here explicitly supplies the bandwidth\nstep needed by the default implementation.',
     r'''is needed. Uniform-KDE and uniform-in-bandwidth results provide context
\citep{gineguillou2002,einmahl2005}, including data-driven bandwidths.
The elementary argument here supplies the local consistency required
by the implemented Gaussian kernel, without substituting a global
bounded-density or uniform-continuity assumption for the local conditions.'''),
]


def validate(text, baseline21, baseline18, tables, summary):
    begin,end=r'\subsection*{S1.1',r'\subsection*{S1.7'
    old_block=baseline21.split(begin,1)[1].split(end,1)[0]
    new_block=text.split(begin,1)[1].split(end,1)[0]
    expected=old_block
    for before,after in PROOF_EDITS:
        assert expected.count(before)==1,'Proof-edit anchor changed'
        expected=expected.replace(before,after,1)
    assert new_block==expected,'Unexpected proof edit beyond the reviewed boundary/KDE changes'
    # Project only explicitly verified edits away for the legacy preservation checks.
    projection=text.replace(new_block,old_block,1).replace('25 September 2026','21 September 2026',1)
    projection=projection.replace(r'scripts/audit\_reviewed\_latex\_20260925.py',r'scripts/audit\_integrated\_latex\_20260921.py')
    result=validate21(projection,baseline18,tables,summary)
    old_tables=re.findall(r'\\begin\{table\}.*?\\end\{table\}',baseline21,re.S)
    assert len(old_tables)==21 and all(block in text for block in old_tables),'Numerical result table changed'
    keys=re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text)
    used={key.strip() for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}',text) for key in group.split(',')}
    assert len(keys)==len(set(keys)) and used<=set(keys),'Citation error'
    for key in ('afuecheta2023','holzmann2025','einmahl2005'):
        assert key in used,'Missing verified source'
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
    assert len(labels)==len(set(labels)) and set(refs)<=set(labels),'Reference error'
    for phrase in ('package isolation was overstated','not independent reimplementation',
                   'not the absolute-value correlation operation itself',
                   'not an active-nuisance\nvalidation',
                   'do not assert exact reflection\nequivariance of every finite-sample studentizer',
                   'The equality piece is identically zero'):
        assert phrase in text,('Missing scope qualification',phrase)
    assert 'snapshot in the recorded isolated environment' not in text
    result['scope']='All21 numerical tables and selected new prose/qualifications; exact reviewed proof edits; not independent mathematical peer review.'
    result['preserved_blocks']=[x for x in result['preserved_blocks'] if x!='S1.1--S1.6']
    result['reviewed_local_proof_edits']=len(PROOF_EDITS)
    result['all_21_table_blocks_preserved']=True
    return result


def run(tex):
    d21=json.loads((ROOT/'results/manuscript_delivery_20260921.json').read_text())
    d18=json.loads((ROOT/'results/manuscript_delivery_20260918.json').read_text())
    p21,p18=(Path(d['manuscript']['tex']) for d in (d21,d18))
    for p,d in ((p21,d21),(p18,d18)):
        assert hashlib.sha256(p.read_bytes()).hexdigest()==d['manuscript']['tex_sha256']
    hist=build_audit();assert hist['all_passed']
    tables,replay=make_tables()
    result=validate(tex.read_text(),p21.read_text(),p18.read_text(),tables,load_summary())
    records={name:json.loads((ROOT/'results'/name).read_text()) for name in
        ('environment_reproduction_20260925.json','record_identity_audit_20260925.json','target_comparison_20260925.json')}
    assert all(r['all_passed'] for r in records.values())
    environment=records['environment_reproduction_20260925.json']
    # Runtime is revalidated by its own dated fail-closed wrapper, not by folder names.
    assert environment['all_passed']
    result.update(tex=str(tex.resolve()),tex_sha256=hashlib.sha256(tex.read_bytes()).hexdigest(),
        audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        historical_checks=len(hist['checks']),bounded_stored_reference_replay=replay,
        new_report_sha256={name:hashlib.sha256((ROOT/'results'/name).read_bytes()).hexdigest() for name in records})
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tex',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    result=run(a.tex)
    if a.report:
        if a.report.exists():raise FileExistsError('Use a new audit path')
        a.report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='bounded_stored_reference_replay'},indent=2))
