"""Exact residual negative controls and numerical parameter isolation."""
from scripts.audit_moderate_benchmark_20260920 import exact_residual_ok
from scripts import run_moderate_benchmark_20260920 as new
from scripts import validate_active_nuisance_20260907 as old

def test_changed_sample_size_or_rational_residual_fails():
    row={'n':'160','x_score_exact_numerator':'1','x_score_exact_denominator':str(160*10**8)}
    assert exact_residual_ok(row,'x')
    assert not exact_residual_ok({**row,'n':'161'},'x')
    assert not exact_residual_ok({**row,'x_score_exact_numerator':'2'},'x')
    assert exact_residual_ok({**row,'x_score_exact_numerator':'-1'},'x')

def test_new_sigma_does_not_reuse_old_bound_default_arguments():
    # Important when copying a numerical engine whose function defaults bind sigma.
    assert new.below_moment(1.,1)!=old.below_moment(1.,1)
    assert new.below_moment(1.,1)==new.below_moment(1.,1,sigma=.3)
    assert old.below_moment(1.,1)==old.below_moment(1.,1,sigma=.6)
