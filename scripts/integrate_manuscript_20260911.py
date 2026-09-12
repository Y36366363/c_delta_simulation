"""Assemble existing evidence into manuscript tables; default is a read-only audit.

No fitting, new simulation cells, permutation runs, or frozen-file writes.
The only RNG use replays 2,000 already recorded pathway datasets at stored
references, to recover marginal CVs and verify the original rho and C.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_manuscript_completion_20260910 import build_audit

DOCS = {
    "main": "docs/manuscript_integrated_20260911.md",
    "s2": "docs/supplement_S2_20260911.md",
    "s3": "docs/supplement_S3_20260911.md",
}
REPORT = ROOT / "results/manuscript_integration_20260911.json"
STAGE = {"population_reference": "R", "population_scale": "S",
         "population_median": "M", "full_fit": "F"}
STAGE_LONG = {"R": "Fixed ref.", "S": "Fixed scale", "M": "Fixed median", "F": "Full"}
METHOD = {"complete_kde": "F", "direct_only_ablation": "D", "oracle_fixed_reference": "O"}
FAMILY = {"uniform": "Uniform", "exponential": "Exp", "half_normal": "Half-normal",
          "scaled_beta12": "Beta", "hyperexponential": "Hyperexp"}
LAW = {"profile_null_normal_sign_link": "Normal/sign", "independent_t5": "t5",
       "independent_strong_skew": "Strong skew"}


def read(name):
    with (ROOT / "results" / name).open(newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def number(x, digits=4):
    val = float(x)
    return "NA" if not np.isfinite(val) else f"{val:.{digits}f}"


def interval(row, low, high):
    return f"[{number(row[low])}, {number(row[high])}]"


def mdtable(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join("---" for _ in headers) + " |"] +
                     ["| " + " | ".join(map(str, row)) + " |" for row in rows])


def summary(vals):
    vals = np.asarray(vals)
    return {"mean": float(np.mean(vals)), "mcse": float(np.std(vals, ddof=1) / np.sqrt(len(vals)))}


def replay_cvs(records):
    selected = [r for r in records if float(r["tau"]) == .1 and int(r["n"]) == 640]
    assert len(selected) == 8000
    by_rep = defaultdict(list)
    for r in selected:
        assert not r["error"]
        by_rep[int(r["replication"])].append(r)
    assert set(by_rep) == set(range(2000))
    values = defaultdict(lambda: defaultdict(list))
    gaps = dict(rho=0., C=0., identity=0.)
    for rep, rows in sorted(by_rep.items()):
        assert len(rows) == 4 and {r["stage"] for r in rows} == set(STAGE)
        assert {int(r["root_seed"]) for r in rows} == {2026090901}
        # Independently repeat the recorded generator's exact order.
        rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([2026090901, 10, 640, rep])))
        sign = rng.choice((-1., 1.), size=640)
        x = sign * np.exp(.1 * rng.normal(size=640))
        y = sign * np.exp(.1 * rng.normal(size=640))
        for r in rows:
            a = abs(x - float(r["reference_x"]))
            b = abs(y - float(r["reference_y"]))
            cvx, cvy = np.std(a) / np.mean(a), np.std(b) / np.mean(b)
            rho = np.corrcoef(a, b)[0, 1]
            c = np.mean(a*b) / (np.mean(a)*np.mean(b))
            gaps["rho"] = max(gaps["rho"], abs(rho - float(r["estimate"])))
            gaps["C"] = max(gaps["C"], abs(c - float(r["historical_C"])))
            gaps["identity"] = max(gaps["identity"], abs(c - (1 + rho*cvx*cvy)))
            for key, value in (("C", float(r["historical_C"])), ("CV_X", cvx), ("CV_Y", cvy)):
                values[r["stage"]][key].append(value)
    assert max(gaps.values()) < 1e-10, gaps
    return {s: {k: summary(v) for k, v in cols.items()} for s, cols in values.items()}, gaps


SOURCES = [
    ("W", "section6_display_table2_wald_20260905.tsv", "Main Table 1; S3.1"),
    ("W0", "claim1_wald_validation_20260823.tsv", "Regular-null source/denominators"),
    ("B", "section6_display_figure2_bridge_20260905.tsv", "S2.1; legacy Figure 2"),
    ("F", "section6_display_figure3_residual_20260905.tsv", "S2.2–3; legacy Figure 3"),
    ("D", "section6_display_manifest_20260905.tsv", "Legacy display source hashes"),
    ("P", "reference_pathway_replications_20260909.tsv", "All 32,000 stage records"),
    ("PS", "reference_pathway_summary_20260909.tsv", "Main Tables 3–4; S3.2–3"),
    ("PP", "reference_pathway_paired_20260909.tsv", "S3.4 paired contrasts"),
    ("PR", "reference_pathway_root_sensitivity_20260909.tsv", "S3.10 retained root flags"),
    ("PM", "reference_pathway_manifest_20260909.tsv", "Pathway provenance"),
    ("A", "active_nuisance_replications_20260907.tsv", "18,000 method records"),
    ("AS", "active_nuisance_summary_20260907.tsv", "Main Table 2; S3.5–6"),
    ("AP", "active_nuisance_paired_20260907.tsv", "S3.7 paired coverage"),
    ("AT", "active_nuisance_population_20260907.tsv", "Population truth and IF variance"),
    ("AD", "active_nuisance_derivative_20260907.tsv", "Contamination derivative check"),
    ("AM", "active_nuisance_manifest_20260907.tsv", "Skew provenance"),
    ("Q", "referee_coverage_diagnostics_20260908.tsv", "S3.9 post hoc tail diagnostics"),
    ("QR", "referee_root_replay_20260908.tsv", "18 regular reference replays"),
    ("QM", "referee_diagnostics_manifest_20260908.tsv", "Post hoc provenance"),
]


def make_tables():
    w = read(SOURCES[0][1])
    b = read("section6_display_figure2_bridge_20260905.tsv")
    f = read("section6_display_figure3_residual_20260905.tsv")
    p = read("reference_pathway_summary_20260909.tsv")
    pr = read("reference_pathway_replications_20260909.tsv")
    a = read("active_nuisance_summary_20260907.tsv")
    pp = read("reference_pathway_paired_20260909.tsv")
    ar = read("active_nuisance_replications_20260907.tsv")
    assert len(p) == 16 and len(pr) == 32000 and len(ar) == 18000
    assert len(b) == 24 and len(f) == 10 and len(a) == 9 and len(w) == 6
    assert all(int(r["valid"]) == 2000 and int(r["failures"]) == 0 for r in p+a)
    assert all(int(r["valid_repetitions"]) == 1000 and int(r["failures"]) == 0
               for r in read("claim1_wald_validation_20260823.tsv"))
    cv, gaps = replay_cvs(pr)
    for r in p:
        if float(r["tau"]) == .1 and int(r["n"]) == 640:
            assert abs(cv[r["stage"]]["C"]["mean"] - float(r["mean_C"])) < 1e-12
    t = {}
    t["main_wald"] = mdtable(["Law", "n", "Rejection", "MCSE", "95% Wilson"],
        [[LAW[r["scenario"]], r["n"], number(r["rejection_rate"]), number(r["monte_carlo_se"]), interval(r,"wilson_95_low","wilson_95_high")] for r in w])
    skewrows=[]
    for n in (160,640,2560):
        methods={r["method"]:r for r in a if int(r["n"])==n}
        full=methods["complete_kde"]
        skewrows.append([n,number(full["coverage"]),interval(full,"wilson_low","wilson_high"),number(methods["direct_only_ablation"]["coverage"]),number(methods["oracle_fixed_reference"]["coverage"]),number(full["se_sd_ratio"])])
    t["main_skew"]=mdtable(["n","Full","95% Wilson","Direct","Oracle","SE/SD"],skewrows)
    t["main_pathway"]=mdtable(["n","Stage","Mean rho","Stage-aware","Direct-only"],
        [[r["n"],STAGE_LONG[STAGE[r["stage"]]],number(r["mean_rho"]),number(r["stage_aware_rate"]),number(r["direct_only_rate"])] for r in p if float(r["tau"])==.1])
    refrows=[]
    for r in p:
        if float(r["tau"])==.1 and int(r["n"])==640:
            cs=cv[r["stage"]]
            refrows.append([STAGE[r["stage"]],number(r["reference_rmse_x"],5),number(r["reference_rmse_y"],5),number(r["reference_correlation"],5),number(cs["C"]["mean"],6),number(cs["CV_X"]["mean"],5),number(cs["CV_Y"]["mean"],5)])
    t["main_reference"]=mdtable(["Stage*","RMSE X","RMSE Y","Corr(TX,TY)","Mean C","Mean CVx","Mean CVy"],refrows)+"\n\n*R: fixed reference; S: fixed scale; M: fixed median; F: full fit."
    t["bridge"]=mdtable(["Family","n","epsilon","Index","Rejection","95% Wilson"],
        [[FAMILY[r["family"]],r["n"],r["epsilon"],number(r["conditioning_index"]),number(r["rejection_rate"]),interval(r,"wilson_95_low","wilson_95_high")] for r in b])
    matched=[r for r in f if r["evidence_component"]=="matched_index_legacy_family"]
    prospective=[r for r in f if r not in matched]
    t["matched"]=mdtable(["Family","Index","Rejection","95% Wilson"],
        [[FAMILY[r["family"]],number(r["conditioning_index"]),number(r["observed_rejection_rate"]),interval(r,"wilson_95_low","wilson_95_high")] for r in matched])
    t["prospective"]=mdtable(["n","epsilon","Index","Predicted","Observed","95% Wilson"],
        [[r["n"],r["epsilon"],number(r["conditioning_index"]),number(r["model_prediction"]),number(r["observed_rejection_rate"]),interval(r,"wilson_95_low","wilson_95_high")] for r in prospective])
    t["wald_seeds"]=mdtable(["j","Law","n","Cell seed"],[[i,LAW[r["scenario"]],r["n"],r["root_cell_seed"]] for i,r in enumerate(w,1)])
    t["pathway_all"]=mdtable(["tau","n","Stage","Mean rho","Rejection","95% Wilson"],
        [[r["tau"],r["n"],STAGE[r["stage"]],number(r["mean_rho"]),number(r["stage_aware_rate"]),interval(r,"stage_aware_wilson_low","stage_aware_wilson_high")] for r in p])
    t["pathway_refs"]=mdtable(["tau","n","Stage","Direct rate","RMSE X","RMSE Y","Corr(TX,TY)"],
        [[r["tau"],r["n"],STAGE[r["stage"]],number(r["direct_only_rate"]),number(r["reference_rmse_x"],5),number(r["reference_rmse_y"],5),number(r["reference_correlation"],5)] for r in p])
    t["pathway_pairs"]=mdtable(["tau","n","Contrast","Delta rejection (MCSE)","Delta rho (MCSE)"],
        [[r["tau"],r["n"],STAGE[r["from_stage"]]+" to "+STAGE[r["to_stage"]],f'{number(r["reject_stage_aware_difference"])} ({number(r["reject_stage_aware_paired_mcse"],5)})',f'{number(r["estimate_difference"])} ({number(r["estimate_paired_mcse"],5)})'] for r in pp])
    t["skew_full"]=mdtable(["n","Method","Bias","Bias MCSE","SD","Mean SE","SE/SD"],
        [[r["n"],METHOD[r["method"]],number(r["bias"],5),number(r["bias_mcse"],5),number(r["empirical_sd"],5),number(r["mean_se"],5),number(r["se_sd_ratio"])] for r in a])
    t["skew_uncertainty"]=mdtable(["n","Method","Coverage","MCSE","95% Wilson","Mean width"],
        [[r["n"],METHOD[r["method"]],number(r["coverage"]),number(r["coverage_mcse"],5),interval(r,"wilson_low","wilson_high"),number(r["mean_width"])] for r in a])
    t["skew_pairs"]=mdtable(["n","Paired R","Coverage difference","Paired MCSE","Full only","Direct only"],
        [[r["n"],r["paired_valid"],number(r["coverage_full_minus_direct"]),number(r["paired_mcse"],6),r["only_full_covers"],r["only_direct_covers"]] for r in read("active_nuisance_paired_20260907.tsv")])
    t["c_summaries"]=mdtable(["Stage","C (MCSE)","CVx (MCSE)","CVy (MCSE)"],
        [[STAGE[s]]+[f'{number(cv[s][key]["mean"],6)} ({number(cv[s][key]["mcse"],6)})' for key in ("C","CV_X","CV_Y")] for s in STAGE])
    diagnostics=[r for r in read("referee_coverage_diagnostics_20260908.tsv") if r["method"]=="complete_kde"]
    t["skew_diagnostics"]=mdtable(["n","SE","Coverage","Below","Above","Coverage delta","Paired MCSE"],
        [[r["n"],"P" if r["scale"]=="reported_plugin" else "V",number(r["coverage"]),number(r["below_truth_miss_rate"]),number(r["above_truth_miss_rate"]),number(r["coverage_difference_from_plugin"]),number(r["paired_difference_mcse"],5)] for r in diagnostics])
    t["root_flags"]=mdtable(["Rep","Root gap / scale","Delta rho","Relative delta SE","Decisions changed"],
        [[r["replication"],f'{float(r["original_root_gap"]):.7g}',f'{float(r["estimate_difference"]):.7g}',f'{float(r["relative_stage_aware_se_difference"]):.7g}',r["stage_aware_rejection_changed"]+" / "+r["direct_rejection_changed"]] for r in read("reference_pathway_root_sensitivity_20260909.tsv")])
    t["permutation_seeds"]=mdtable(["Panel","Family","n","epsilon","R","Cell seed"],
        [["P",FAMILY[r["family"]],r["n"],r["epsilon"],r["repetitions"],r["root_cell_seed"]] for r in b]+
        [["C" if r in matched else "H",FAMILY[r["family"]],r["n"],r["epsilon"],r["repetitions"],r["root_cell_seed"]] for r in f])
    # Short IDs keep the source ledger usable; filenames follow as a list.
    t["source_ledger"]=mdtable(["ID","Used for"],[[key,role] for key,_,role in SOURCES])+"\n\n"+"\n".join(f"- {key}: `results/{path}`." for key,path,_ in SOURCES)
    return t, {"existing_datasets_replayed":2000,"stored_stage_records_checked":8000,
               "max_absolute_replay_gaps":gaps,"secondary_summaries":cv,
               "new_simulation_cells":0,"new_reference_fits":0}


def replace_tables(text, tables):
    used=[]
    def sub(match):
        key=match.group(1)
        if key not in tables:
            raise ValueError(f"unknown table block {key}")
        used.append(key)
        return f"<!-- table:{key} -->\n{tables[key]}\n<!-- /table:{key} -->"
    output=re.sub(r"<!-- table:([a-z_]+) -->.*?<!-- /table:\1 -->",sub,text,flags=re.S)
    return output,used


def run(write=False):
    prior=build_audit()
    assert prior["all_passed"], "Frozen provenance or historical audit failed; investigate before editing"
    tables,replay=make_tables()
    checks=[]
    all_used=[]
    for name,path in DOCS.items():
        target=ROOT/path
        before=target.read_text()
        after,used=replace_tables(before,tables)
        all_used.extend(used)
        if write:
            target.write_text(after)
        for key in used:
            expected=f"<!-- table:{key} -->\n{tables[key]}\n<!-- /table:{key} -->"
            checks.append({"check":f"display:{key}","passed":expected in target.read_text(),"file":path})
    assert len(all_used)==len(set(all_used))==len(tables), "Missing or duplicated table blocks"
    checks.append({"check":"historical_audit","passed":prior["all_passed"],"checks":len(prior["checks"])})
    checks.append({"check":"bounded_seed_replay","passed":True,**replay})
    paths={"results/"+p for _,p,_ in SOURCES}
    paths.update(prior["source_hashes_lf"])
    paths.update(["src/cdelta.py", "scripts/integrate_manuscript_20260911.py",
                  "scripts/run_claim_validation_20260823.py", "scripts/audit_wald_convergence_20260822.py",
                  "scripts/run_profile_bridge_family_validation_20260817.py",
                  "scripts/run_claim_external_validation_20260825.py",
                  "scripts/run_studentized_permutation_weak_null_20260814.py",
                  "scripts/run_reference_pathway_20260909.py"])
    hashes={}
    for path in sorted(paths):
        raw=(ROOT/path).read_bytes()
        hashes[path]={"sha256":hashlib.sha256(raw).hexdigest(),
                      "sha256_lf":hashlib.sha256(raw.replace(b"\r\n",b"\n")).hexdigest()}
    report={"date":"2026-09-11","scope":"internal author integration; not independent proof review or clean reproduction",
            "tables_checked":len(tables),"all_passed":all(r["passed"] for r in checks),
            "checks":checks,"sources":hashes,"numpy_replay_version":np.__version__,**replay}
    doc_paths=list(DOCS.values())+["docs/supplement_S1_20260911.md",
                                  "docs/manuscript_references_20260911.md"]
    report["document_sha256"]={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in doc_paths}
    if write:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:report[k] for k in ("tables_checked","all_passed","new_simulation_cells","existing_datasets_replayed","max_absolute_replay_gaps")}))
    if not report["all_passed"]:
        raise AssertionError([r for r in checks if not r["passed"]])
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true",help="refresh new draft tables and new report only")
    run(parser.parse_args().write)
