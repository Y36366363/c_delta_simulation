"""Reject unreviewed proof edits and scientific-cell corruption in author LaTeX."""
import json
import os
from pathlib import Path
import pytest
from scripts.audit_reviewed_latex_20260925 import ROOT,load_summary,make_tables,validate

@pytest.fixture(scope='module')
def inputs():
    path=os.environ.get('RHOP_MANUSCRIPT_PATH')
    if not path:pytest.skip('Set RHOP_MANUSCRIPT_PATH to September25 author LaTeX')
    def prior(date):
        d=json.loads((ROOT/f'results/manuscript_delivery_{date}.json').read_text())
        return Path(d['manuscript']['tex']).read_text()
    return Path(path).read_text(),prior('20260921'),prior('20260918'),make_tables()[0],load_summary()

def test_reviewed_manuscript(inputs):
    assert validate(*inputs)['all_21_table_blocks_preserved']

@pytest.mark.parametrize('old,new',[
 ('The equality piece is identically zero','The equality piece can be dropped'),
 ('0.9045','0.9545'),
 ('package isolation was overstated','package isolation was demonstrated'),
 ('not the absolute-value correlation operation itself','the absolute-value correlation operation itself'),
 ('Here is the class verification used for R6','A substituted unsupported proof'),
])
def test_rejects_changed_proof_result_or_scope(inputs,old,new):
    text,*rest=inputs;assert old in text
    with pytest.raises(AssertionError):validate(text.replace(old,new,1),*rest)
