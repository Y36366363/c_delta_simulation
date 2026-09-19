"""Negative controls for retained historical aggregate comparison."""
import pytest
from scripts.reproduce_retained_history_20260918 import compare_retained

@pytest.mark.parametrize('field', ['root_cell_seed','repetitions','n_perm','n_bootstrap',
    'observed_rejections','studentized_rejection','rejection_rate','below_truth_miss_count'])
def test_exact_fields_reject_even_subtolerance_changes(field):
    expected={'scenario':'a',field:'1','estimate':'.2'}
    actual={**expected,field:1+1e-12}
    assert not compare_retained([actual],[expected],('scenario',))['passed']

def test_numeric_rounding_is_distinct_from_a_changed_count():
    expected={'scenario':'a','repetitions':150,'estimate':.2}
    assert compare_retained([{**expected,'estimate':.2+1e-12}],[expected],('scenario',))['passed']
