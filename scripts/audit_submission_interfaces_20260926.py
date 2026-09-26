"""Read-only table, provenance and revision-interface audit of the author source.

Unlike earlier version audits, this permits the documented local proof repairs.
Presence of a qualification or a reviewed change is not mathematical validation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_final_latex_20260912 import extract, equivalent, expected_rows, make_tables
from scripts.audit_integrated_latex_20260921 import expected_new, load_summary
from scripts.audit_manuscript_completion_20260910 import build_audit

QUALIFICATIONS = {
    "limiting_covariance": "limiting nuisance covariance",
    "actual_covariance_requires_more": "uniform integrability of the scaled squared errors",
    "squared_closure_L1": "squared closure requires only an integrable envelope",
    "local_density_only": "without requiring a density away from the local neighborhoods",
    "localized_midpoint_scores": "possible midpoint-induced tie",
    "weak_null_centered_cross_term": "Cauchy--Schwarz controls its cross term",
    "weak_null_empirical_not_population": "When fourth moments are infinite",
    "all_three_population_inactive": "All three null designs have zero population reference coefficients",
    "finite_B": "do not estimate an exhaustive-permutation rule",
    "prediction_uncertainty": "excluding training and prediction uncertainty",
    "standard_theory_scope": "specializes standard multistep influence propagation",
    "failed_positive_benchmark": "This study did not yield the hoped-for nominal-coverage example",
    "independent_review_open": "mathematical review remains outstanding",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compact(text):
    return re.sub(r"\s+", " ", text).strip()


def segment(text, start, end):
    assert text.count(start) == 1, ("missing/duplicate section anchor", start)
    remainder = text.split(start, 1)[1]
    assert end in remainder, ("missing section end", end)
    return remainder.split(end, 1)[0]


def table_blocks(text):
    return re.findall(r"\\begin\{table\}.*?\\end\{table\}", text, re.S)


def check_keys(text):
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    assert len(labels) == len(set(labels)), "Duplicate LaTeX label"
    keys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", text)
    assert len(keys) == len(set(keys)), "Duplicate bibliography key"
    citations = {key.strip() for group in re.findall(r"\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}", text) for key in group.split(",")}
    assert citations <= set(keys), ("unresolved citation", citations - set(keys))
    refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", text))
    assert refs <= set(labels), ("unresolved cross-reference", refs - set(labels))
    return dict(labels=len(labels), bibliography_keys=len(keys), used_citation_keys=len(citations), referenced_labels=len(refs))


def check_tables(text, prior, expected):
    found = extract(text)
    assert set(found) == set(expected), ("numerical table inventory", set(found) ^ set(expected))
    cells = 0
    for key, rows in expected.items():
        assert len(found[key]) == len(rows), (key, "row count")
        for i, (actual, wanted) in enumerate(zip(found[key], rows)):
            assert len(actual) == len(wanted), (key, i, "column count")
            for j, (left, right) in enumerate(zip(actual, wanted)):
                assert equivalent(left, right), (key, i, j, left, right)
                cells += 1
    before, after = table_blocks(prior), table_blocks(text)
    assert len(before) == len(after) == 21, "numerical table count changed"
    assert before == after, "one or more numerical table blocks changed"
    assert len(found) == 21 and cells == 1182, (len(found), cells)
    return dict(numerical_tables=21, numerical_cells=cells, numerical_blocks_byte_identical=True)


def validate(text, prior, expected):
    result = check_tables(text, prior, expected)
    preserved = [
        ("Introduction", r"\section{Introduction}", r"\section{Profiles,"),
        ("Appendix B proposition proof", r"\section{Proof for the shared-sign construction}", r"\section{Supplementary materials}"),
        ("S1.7 software boundary", r"\subsection*{S1.7 Software boundary}", r"\section*{Supplement S2."),
    ]
    for label, start, end in preserved:
        assert segment(text, start, end) == segment(prior, start, end), ("preserved block changed", label)
    before = prior.split(r"\begin{document}", 1)[0]
    after = text.split(r"\begin{document}", 1)[0].replace("26 September 2026", "25 September 2026")
    assert after == before, "preamble changed beyond the version date"
    flattened = compact(text)
    for label, requirement in QUALIFICATIONS.items():
        assert compact(requirement) in flattened, ("missing repaired qualification", label)
    math = re.sub(r"\s+", "", text)
    for expression in (
        r"\widehat{\IF}_\rho=\widehatH+\rhophat\widehatK",
        r"P_n\widehatK^2",
        r"\gamma_X",
        r"\frac{-h_X+\mu_bg_X}{D}",
        r"\rhop\frac{\E(X-T_X)-\mu_ag_X}{v_a}",
    ):
        assert expression in math, ("missing repaired formula interface", expression)
    result.update(all_passed=True, preserved_blocks=[item[0] for item in preserved],
                  preamble_preserved_except_date=True, key_counts=check_keys(text),
                  checked_qualification_interfaces=list(QUALIFICATIONS),
                  scope="Source-derived table cells, preserved blocks, keys and declared local-repair interfaces; not proof validity, literature completeness, layout or every prose number.")
    return result


def main(tex, report):
    if report is not None and report.exists():
        raise FileExistsError("Preserve existing reports; choose a new path")
    delivery = json.loads((ROOT / "results/manuscript_delivery_20260925.json").read_text())
    prior = Path(delivery["manuscript"]["tex"])
    assert sha256(prior) == delivery["manuscript"]["tex_sha256"], "prior author source changed"
    historical = build_audit()
    assert historical["all_passed"] and len(historical["checks"]) == 172
    tables, replay = make_tables()
    expected = {**expected_rows(tables), **expected_new(load_summary())}
    result = validate(tex.read_text(), prior.read_text(), expected)
    evidence_path = ROOT / "results/evidence_interfaces_20260926.json"
    evidence = json.loads(evidence_path.read_text())
    assert evidence["all_passed"] and evidence["frozen_tsv_unchanged"] and evidence["new_design_cells"] == 0
    assert evidence["source_sha256"] == sha256(ROOT / "scripts/audit_evidence_interfaces_20260926.py")
    changes = tex.parent / "reviewed_changes.json"
    assert changes.is_file(), "reviewed change ledger missing"
    ledger = json.loads(changes.read_text())
    assert isinstance(ledger, dict) and ledger.get("changes"), "empty reviewed change ledger"
    assert ledger["prior_tex_sha256"] == sha256(prior) and ledger["tex_sha256"] == sha256(tex), "change ledger source hash mismatch"
    reconstructed = prior.read_text()
    for edit in ledger["changes"]:
        assert reconstructed.count(edit["before"]) == 1, "change ledger anchor is missing or ambiguous"
        reconstructed = reconstructed.replace(edit["before"], edit["after"], 1)
    assert reconstructed == tex.read_text(), "unrecorded author-source edit"
    result.update(tex=str(tex.resolve()), tex_sha256=sha256(tex), prior_tex=str(prior),
                  prior_tex_sha256=sha256(prior), audit_source_sha256=sha256(__file__),
                  historical_checks=172, bounded_stored_reference_replay=replay,
                  evidence_interfaces_report_sha256=sha256(evidence_path),
                  reviewed_changes_sha256=sha256(changes),
                  reviewed_changes_count=len(ledger["changes"]), change_ledger_reconstructs_source=True,
                  change_ledger_scope="Recorded changes are for scope review, not evidence of mathematical validity.")
    if report is not None:
        report.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k:v for k,v in result.items() if k != "bounded_stored_reference_replay"}, indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex",type=Path); parser.add_argument("--report",type=Path)
    args=parser.parse_args(); main(args.tex,args.report)
