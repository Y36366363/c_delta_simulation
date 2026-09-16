"""Negative controls for scientific reproduction comparisons, not new runs."""
import pytest
from scripts.reproduce_core_studies_20260916 import compare


def row(**updates):
    return {'n':'80','replication':'7','root_seed':'42','covered':'1',
            'estimate':'.927','error':'','extra':'nan',**updates}


def test_nan_status_and_small_rounding_are_preserved():
    r=compare([row(estimate=.927+1e-12,extra=float('nan'))],[row()],('n','replication'))
    assert r['passed'] and r['rows']==1


@pytest.mark.parametrize('change',[{'covered':'0'},{'covered':1+1e-12},
    {'root_seed':'43'},{'estimate':'.95'},{'extra':'0'},{'error':'solver failed'}])
def test_changed_decisions_seeds_values_or_failures_are_rejected(change):
    assert not compare([row(**change)],[row()],('n','replication'))['passed']


def test_duplicate_and_missing_rows_are_rejected():
    with pytest.raises(ValueError,match='duplicate'):
        compare([row(),row()],[row()],('n','replication'))
    with pytest.raises(ValueError,match='identities'):
        compare([],[row()],('n','replication'))


def test_missing_column_is_rejected():
    a=row();a.pop('error')
    with pytest.raises(ValueError,match='column identities'):
        compare([a],[row()],('n','replication'))
