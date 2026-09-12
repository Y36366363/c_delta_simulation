"""Evidence-integration safeguards, not statistical calibration tests."""
from pathlib import Path
import pytest

from scripts.integrate_manuscript_20260911 import (
    DOCS, ROOT, make_tables, read, replay_cvs, replace_tables,
)


@pytest.fixture(scope="module")
def assembled():
    return make_tables()


def test_actual_display_blocks_match_sources_and_replayed_cvs(assembled):
    tables, replay = assembled
    used=[]
    for path in DOCS.values():
        text=(ROOT/path).read_text()
        expected,keys=replace_tables(text,tables)
        assert text==expected
        used.extend(keys)
    assert len(used)==len(set(used))==len(tables)
    assert replay["new_simulation_cells"]==replay["new_reference_fits"]==0
    assert replay["stored_stage_records_checked"]==8000
    assert max(replay["max_absolute_replay_gaps"].values())<1e-10


def test_optimistic_coverage_edit_is_rejected(assembled):
    tables,_=assembled
    original=(ROOT/DOCS["main"]).read_text()
    changed=original.replace("| 2560 | 0.9270 |", "| 2560 | 0.9500 |")
    assert changed!=original
    reconciled,_=replace_tables(changed,tables)
    assert reconciled!=changed and reconciled==original


def test_corrupt_stored_reference_fails_replay():
    records=read("reference_pathway_replications_20260909.tsv")
    for r in records:
        if r["n"]=="640" and float(r["tau"])==.1 and r["stage"]=="population_reference":
            r["reference_x"]="10.0"
            break
    with pytest.raises(AssertionError):
        replay_cvs(records)


def test_permutation_seed_overlap_is_not_an_independent_confirmation():
    pilot=read("section6_display_figure2_bridge_20260905.tsv")
    confirm=read("section6_display_figure3_residual_20260905.tsv")
    for r in confirm:
        if r["evidence_component"]!="matched_index_legacy_family":
            continue
        p=next(p for p in pilot if (p["family"],p["n"],p["epsilon"])==
               (r["family"],r["n"],r["epsilon"]))
        assert p["root_cell_seed"]==r["root_cell_seed"]
        assert p["n_perm"]==r["n_perm"]=="99"
    note=(ROOT/"docs/supplement_S2_20260911.md").read_text()
    assert "first 150 datasets overlap" in note
