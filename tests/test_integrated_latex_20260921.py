"""Negative controls for the actual integrated manuscript and unchanged proof."""
import json
import os
from pathlib import Path
import pytest
from scripts.audit_integrated_latex_20260921 import ROOT,load_summary,make_tables,validate

@pytest.fixture(scope='module')
def inputs():
    path=os.environ.get('RHOP_MANUSCRIPT_PATH')
    if not path:pytest.skip('Set RHOP_MANUSCRIPT_PATH to September 21 author LaTeX')
    delivery=json.loads((ROOT/'results/manuscript_delivery_20260918.json').read_text())
    return Path(path).read_text(),Path(delivery['manuscript']['tex']).read_text(),make_tables()[0],load_summary()

def test_actual_integrated_manuscript(inputs):
    assert validate(*inputs)['numerical_tables_total']==21

@pytest.mark.parametrize('old,new',[
    ('160 & F & 0.9045','160 & F & 0.9545'),
    ('2560 & F & -0.00124','2560 & F & -0.01240'),
    ('.9270 & [.9148,.9376]','.9500 & [.9148,.9376]'),
    ('Here is the class verification used for R6','Changed proof text'),
    ('This study did not yield the hoped-for','This study did yield the hoped-for'),
])
def test_changed_value_or_claim_is_rejected(inputs,old,new):
    text,prior,tables,summary=inputs
    assert old in text
    with pytest.raises(AssertionError):validate(text.replace(old,new,1),prior,tables,summary)
