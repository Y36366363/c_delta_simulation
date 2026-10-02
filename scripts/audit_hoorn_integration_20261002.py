"""Read-only source audit for the privately communicated Hoorn revision.

This verifies scope, numerical tables and links, not proof correctness or
publication status of the private source.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_submission_interfaces_20260926 import check_tables, check_keys, segment
from scripts.audit_final_latex_20260912 import make_tables, expected_rows
from scripts.audit_integrated_latex_20260921 import expected_new, load_summary
from scripts.audit_manuscript_completion_20260910 import build_audit

def run(path):
    delivery=json.loads((ROOT/'results/manuscript_delivery_20260926.json').read_text())
    prior=Path(delivery['manuscript']['tex']);old=prior.read_text();new=path.read_text()
    assert hashlib.sha256(prior.read_bytes()).hexdigest()==delivery['manuscript']['tex_sha256']
    ledger=json.loads((path.parent/'reviewed_changes.json').read_text())
    assert ledger['prior_tex_sha256']==delivery['manuscript']['tex_sha256']
    rebuilt=old
    for change in ledger['changes']:
        assert rebuilt.count(change['before'])==1
        rebuilt=rebuilt.replace(change['before'],change['after'],1)
    assert rebuilt==new and hashlib.sha256(new.encode()).hexdigest()==ledger['tex_sha256']
    tables,_=make_tables()
    result=check_tables(new,old,{**expected_rows(tables),**expected_new(load_summary())})
    preserved=[]
    for name,start,end in [
        ('Sections3--7',r'\section{Complete influence-function inference}',r'\section{Discussion}'),
        ('Appendices and S1--S3',r'\appendix',r'\begin{thebibliography}')]:
        a=segment(old,start,end);b=segment(new,start,end)
        # Only the new audit command and author checklist change in the latter block.
        for change in ledger['changes']:
            if change['before'] in a:a=a.replace(change['before'],change['after'],1)
        assert a==b,name
        preserved.append(name)
    historical=build_audit();assert historical['all_passed']
    result.update(all_passed=True,tex=str(path.resolve()),tex_sha256=ledger['tex_sha256'],
      prior_tex_sha256=ledger['prior_tex_sha256'],reviewed_changes=len(ledger['changes']),
      key_counts=check_keys(new),preserved_blocks=preserved,historical_checks=len(historical['checks']),
      new_design_cells=0,scope='Private-source attribution and text revision; numerical evidence unchanged; no independent mathematical review',
      audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('tex',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    r=run(a.tex)
    if a.report:
        assert not a.report.exists();a.report.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
