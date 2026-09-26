"""Negative controls for claims of dependency-isolated reproduction."""
from copy import deepcopy
import pytest
from scripts.reproduce_verified_environment_20260925 import validate_environment, compare_tables


def valid_probe():
    return dict(prefix="/tmp/venv", base_prefix="/opt/python", isolated_venv=True,
                isolated_mode=True, enable_user_site=False,
                pyvenv_config="include-system-site-packages = false\n",
                module_versions={"numpy": "1.26.4", "scipy": "1.16.3"},
                module_paths={"numpy": "/tmp/venv/lib/python/site-packages/numpy/__init__.py",
                              "scipy": "/tmp/venv/lib/python/site-packages/scipy/__init__.py"},
                sys_path=["/opt/python/lib", "/tmp/venv/lib/python/site-packages"])


def test_valid_isolated_environment():
    assert validate_environment(valid_probe())


@pytest.mark.parametrize("case", ["lost_config", "base_prefix", "inherited_site", "outside_numpy", "outside_path", "wrong_version", "user_site", "no_isolated_flag"])
def test_invalid_isolation_is_rejected(case):
    probe = deepcopy(valid_probe())
    if case == "lost_config":
        probe["pyvenv_config"] = None
    elif case == "base_prefix":
        probe["base_prefix"] = probe["prefix"]
    elif case == "inherited_site":
        probe["pyvenv_config"] = "include-system-site-packages = true\n"
    elif case == "outside_numpy":
        probe["module_paths"]["numpy"] = "/opt/python/lib/site-packages/numpy/__init__.py"
    elif case == "outside_path":
        probe["sys_path"].append("/opt/python/lib/site-packages")
    elif case == "wrong_version":
        probe["module_versions"]["scipy"] = "1.17.0"
    elif case == "user_site":
        probe["enable_user_site"] = True
    else:
        probe["isolated_mode"] = False
    with pytest.raises(AssertionError):
        validate_environment(probe)


def test_roundoff_is_not_reported_as_exact_equality():
    outcome = compare_tables([["estimate"], ["0.5"]], [["estimate"], ["0.5000000000000001"]])
    assert outcome["passed"] and not outcome["exact_cell_equality"]
    assert outcome["differing_numeric_cells"] == 1


@pytest.mark.parametrize("field,left,right", [
    ("estimate", "0.5", "0.5001"),
    ("covered", "1", "0"),
    ("root_seed", "2026092001", "2026092002"),
    ("x_score_exact_denominator", "1000000000000000000", "1000000000000000001"),
])
def test_substantive_or_exact_field_mismatch_is_rejected(field, left, right):
    with pytest.raises(AssertionError):
        compare_tables([[field], [left]], [[field], [right]])
