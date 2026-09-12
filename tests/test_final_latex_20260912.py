"""Negative controls against the actual author manuscript, when supplied."""
import os
from pathlib import Path
import re
import pytest
from scripts.audit_final_latex_20260912 import make_tables, validate

@pytest.fixture(scope='module')
def manuscript():
    path=os.environ.get('RHOP_MANUSCRIPT_PATH')
    if not path:
        pytest.skip('Set RHOP_MANUSCRIPT_PATH to the actual single-file author manuscript')
    return Path(path).read_text(),make_tables()[0]

def test_actual_manuscript(manuscript):
    text,tables=manuscript
    assert validate(text,tables)['tables_checked']==19

@pytest.mark.parametrize('old,new',[
    ('.9270 & [.9148,.9376]', '.9500 & [.9148,.9376]'),
    ('2026182461', '2026182462'),
    ('Fixed reference & 0 & 0 & NA', 'Fixed reference & 0 & 0 & 0'),
])
def test_changed_scientific_cell_is_rejected(manuscript,old,new):
    text,tables=manuscript
    assert old in text
    with pytest.raises(AssertionError):
        validate(text.replace(old,new,1),tables)

@pytest.mark.parametrize('duplicate',[False,True])
def test_missing_or_duplicate_table_is_rejected(manuscript,duplicate):
    text,tables=manuscript
    block=re.search(r'\\begin\{table\}.*?\\end\{table\}',text,re.S)[0]
    changed=text+block if duplicate else text.replace(block,'',1)
    with pytest.raises(AssertionError):
        validate(changed,tables)
