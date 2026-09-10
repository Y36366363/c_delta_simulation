"""Read-only reconciliation of manuscript tables, proof boundaries and sources.

No simulation, bootstrap or permutation is run. Optional CLI output is a new
JSON audit, never a rewrite of a frozen scientific table.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_section6_displays_20260905 import section6_display_audit
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from scripts.validate_active_nuisance_20260907 import wilson

SECTION6 = "docs/manuscript_draft_section_6_20260905.md"
APPENDIX = "docs/appendix_asymptotic_theory_20260819.md"
OUTPUT = "results/manuscript_completion_audit_20260910.json"
NUMBER = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def read(name):
    with (ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def one(rows, **keys):
    selected = [r for r in rows if all(str(r[k]) == str(v) for k, v in keys.items())]
    if len(selected) != 1:
        raise ValueError(f"expected one source row for {keys}; found {len(selected)}")
    return selected[0]


def table(text, heading):
    body = text.split(heading, 1)[1].split("\n### ", 1)[0]
    lines = re.findall(r"^\|.*\|$", body, flags=re.MULTILINE)
    if len(lines) < 3:
        raise ValueError(f"missing table at {heading}")
    return [[c.strip() for c in line.strip("|").split("|")] for line in lines[2:]]


def numerical_cell_checks(label, cells, expected, source):
    tokens = NUMBER.findall(" ".join(cells))
    if len(tokens) != len(expected):
        return [
            {
                "check": label + ":shape",
                "passed": False,
                "detail": f"{len(tokens)} displayed numbers; expected {len(expected)}",
            }
        ]
    checks = []
    for i, (token, value) in enumerate(zip(tokens, expected, strict=True)):
        value = float(value)
        if "." in token or "e" in token.lower():
            mantissa, _, exponent = token.lower().partition("e")
            decimals = len(mantissa.partition(".")[2])
            tolerance = 0.5000001 * 10 ** (int(exponent or 0) - decimals)
        else:
            tolerance = 0.0
        checks.append(
            {
                "check": f"{label}:{i}",
                "passed": abs(float(token) - value) <= tolerance,
                "displayed": token,
                "source_value": value,
                "rounding_tolerance": tolerance,
                "source": source,
            }
        )
    return checks


def display_checks(section6=None):
    text = section6 if section6 is not None else (ROOT / SECTION6).read_text()
    checks = []
    wald_source = "section6_display_table2_wald_20260905.tsv"
    wald = read(wald_source)
    displayed = table(text, "### 6.2 Regular IID Wald evidence")
    if len(displayed) != len(wald):
        raise ValueError("Wald table row count changed")
    for i, (cells, row) in enumerate(zip(displayed, wald, strict=True)):
        keys = (
            "n",
            "repetitions",
            "rejection_rate",
            "monte_carlo_se",
            "wilson_95_low",
            "wilson_95_high",
            "studentized_z_sd",
        )
        checks += numerical_cell_checks(
            f"wald:{i}", cells[1:], [row[k] for k in keys], wald_source
        )

    skew_source = "active_nuisance_summary_20260907.tsv"
    skew = read(skew_source)
    displayed = table(
        text, "### 6.6 Targeted nonzero-effect, active-nuisance follow-up"
    )
    if len(displayed) != 3:
        raise ValueError("active-nuisance table row count changed")
    for cells in displayed:
        n = cells[0]
        full = one(skew, n=n, method="complete_kde")
        direct = one(skew, n=n, method="direct_only_ablation")
        oracle = one(skew, n=n, method="oracle_fixed_reference")
        expected = [
            n,
            full["coverage"],
            full["wilson_low"],
            full["wilson_high"],
            full["se_sd_ratio"],
            direct["coverage"],
            oracle["coverage"],
        ]
        checks += numerical_cell_checks(f"active:{n}", cells, expected, skew_source)

    pathway_source = "reference_pathway_summary_20260909.tsv"
    pathway = read(pathway_source)
    displayed = table(
        text, "### 6.7 Supervisor-directed four-stage reference comparison"
    )
    if len(displayed) != 4:
        raise ValueError("pathway main table row count changed")
    for cells in displayed:
        tau, n = float(cells[0]), cells[1]
        fixed = one(pathway, tau=tau, n=n, stage="population_scale")
        full = one(pathway, tau=tau, n=n, stage="full_fit")
        expected = [tau, n] + [
            row[key]
            for key in ("mean_rho", "stage_aware_rate", "direct_only_rate")
            for row in (fixed, full)
        ]
        checks += numerical_cell_checks(
            f"pathway:{tau}:{n}", cells, expected, pathway_source
        )
    return checks


def uncertainty_checks():
    checks = []
    for row in read("reference_pathway_summary_20260909.tsv"):
        for track in ("stage_aware", "direct_only"):
            count, valid = int(row[track + "_rejections"]), int(row["valid"])
            rate = count / valid
            lo, hi = wilson(count, valid)
            mcse = (rate * (1 - rate) / valid) ** 0.5
            expected = (rate, lo, hi, mcse)
            actual = [
                float(row[track + suffix])
                for suffix in ("_rate", "_wilson_low", "_wilson_high", "_mcse")
            ]
            checks.append(
                {
                    "check": f"MC:{row['tau']}:{row['n']}:{row['stage']}:{track}",
                    "passed": all(abs(a - b) < 1e-12 for a, b in zip(actual, expected)),
                    "detail": "count, Wilson interval and binomial Monte Carlo SE",
                }
            )
    return checks


def proof_and_scope_checks():
    appendix = (ROOT / APPENDIX).read_text()
    s12 = (ROOT / "docs/manuscript_draft_sections_1_2_20260830.md").read_text()
    s35 = (ROOT / "docs/manuscript_draft_sections_3_5_20260904.md").read_text()
    placement = " ".join(
        (ROOT / "docs/manuscript_completion_review_20260910.md").read_text().split()
    )
    specifications = {
        "reduced_C_proof": "No root-n expansion" in appendix and "M_C=" in appendix,
        "paired_six_dimensional_stack": "theta_{XY}" in appendix
        and "score covariance need not be" in appendix,
        "empirical_not_population_L2_under_weak_moments": "This last argument is in the empirical"
        in appendix,
        "coefficient_and_weight_localization": "localization includes the finitely many fitted scalar"
        in appendix,
        "unstudentized_ranking_boundary": "does not equate p-values" in appendix,
        "section2_unchanged_margins": "Re-pairing leaves each marginal sample" in s12,
        "formula_command_repaired": "^2,qquad" not in s12 and r"^2,\qquad" in s12,
        "unbridged_zero_index_disclosed": "I_n=0 throughout" in s35,
        "placement_not_approval": "pending supervisor confirmation" in placement,
        "application_is_not_assumed_IID": "No dataset has passed this gate"
        in placement,
        "review_is_not_independent_certification": "not independent mathematical peer review"
        in placement,
    }
    return [
        {
            "check": k,
            "passed": v,
            "detail": "source wording safeguard, not a proof certificate",
        }
        for k, v in specifications.items()
    ]


def build_audit():
    checks = display_checks() + uncertainty_checks() + proof_and_scope_checks()
    checks += [{**r, "passed": bool(r["passed"])} for r in section6_display_audit()]
    manifests = (
        "active_nuisance_manifest_20260907.tsv",
        "referee_diagnostics_manifest_20260908.tsv",
        "reference_pathway_manifest_20260909.tsv",
    )
    for manifest in manifests:
        for row in read(manifest):
            checks.append(
                {
                    "check": "hash:" + row["path"],
                    "passed": normalized_text_sha256(ROOT / row["path"])
                    == row["sha256_lf"],
                    "detail": manifest,
                }
            )
    paths = [
        SECTION6,
        APPENDIX,
        "docs/manuscript_draft_sections_1_2_20260830.md",
        "docs/manuscript_draft_sections_3_5_20260904.md",
        "docs/manuscript_draft_section_8_20260908.md",
        "docs/manuscript_completion_review_20260910.md",
        "docs/manuscript_review_frontmatter_20260910.md",
        "scripts/audit_manuscript_completion_20260910.py",
    ]
    paths += ["results/" + name for name in manifests]
    return {
        "date": "2026-09-10",
        "new_simulation_cells": 0,
        "scope": "internal reconciliation; not independent mathematical peer review or clean-environment reproduction",
        "display_number_checks": len(display_checks()),
        "checks": checks,
        "all_passed": all(r["passed"] for r in checks),
        "source_hashes_lf": {p: normalized_text_sha256(ROOT / p) for p in paths},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    audit = build_audit()
    if args.write_report:
        (ROOT / OUTPUT).write_text(json.dumps(audit, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            {
                "checks": len(audit["checks"]),
                "all_passed": audit["all_passed"],
                "display_numbers": audit["display_number_checks"],
                "new_simulation_cells": 0,
            }
        )
    )
    if not audit["all_passed"]:
        for row in audit["checks"]:
            if not row["passed"]:
                print(row)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
