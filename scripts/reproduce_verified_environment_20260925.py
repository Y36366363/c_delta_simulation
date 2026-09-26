"""Repeat the existing moderate study after verifying dependency isolation.

The September 18--21 records explicitly report isolated_venv=False.  Their
source-snapshot reproduction remains evidence, but is not a clean dependency
environment run.  This dated follow-up preserves all those historical records.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "d4ae9c6067a829bc78c8ef776605f9bf7c4ad32f"
EXPECTED_VERSIONS = {"numpy": "1.26.4", "scipy": "1.16.3"}
# Reuse the declared September 16 reproduction tolerance; retain exact status
# separately, so roundoff agreement cannot be reported as bitwise equality.
SCALED_TOLERANCE = 1e-10
PROBE = r'''
import importlib.metadata, json, pathlib, platform, site, sys
import numpy, scipy
prefix=pathlib.Path(sys.prefix).resolve()
config=prefix/'pyvenv.cfg'
print(json.dumps(dict(
    python=platform.python_version(), executable=sys.executable,
    prefix=str(prefix), base_prefix=str(pathlib.Path(sys.base_prefix).resolve()),
    isolated_venv=sys.prefix!=sys.base_prefix, enable_user_site=site.ENABLE_USER_SITE,
    isolated_mode=bool(sys.flags.isolated),
    pyvenv_config=config.read_text() if config.exists() else None,
    module_versions={'numpy':numpy.__version__,'scipy':scipy.__version__},
    module_paths={'numpy':str(pathlib.Path(numpy.__file__).resolve()),
                  'scipy':str(pathlib.Path(scipy.__file__).resolve())},
    sys_path=sys.path,
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()})))
'''


def validate_environment(probe):
    """Reject lost venv configuration and dependencies imported outside it."""
    prefix = Path(probe["prefix"])
    assert probe["isolated_venv"] and probe["prefix"] != probe["base_prefix"], "not a virtual environment"
    assert probe["isolated_mode"] and probe["enable_user_site"] is False, "isolation flags missing"
    config = probe["pyvenv_config"] or ""
    options = dict(line.lower().split("=", 1) for line in config.splitlines() if "=" in line)
    options = {key.strip(): value.strip() for key, value in options.items()}
    assert options.get("include-system-site-packages") == "false", "system site packages are enabled or config missing"
    assert probe["module_versions"] == EXPECTED_VERSIONS, "numerical versions changed"
    for name, path in probe["module_paths"].items():
        assert Path(path).is_relative_to(prefix), f"{name} imported outside virtual environment"
    for path in probe["sys_path"]:
        if "site-packages" in Path(path).parts:
            assert Path(path).is_relative_to(prefix), "external site-packages on search path"
    return True


def environment_probe(python):
    probe = json.loads(subprocess.check_output([str(python), "-I", "-c", PROBE], text=True))
    validate_environment(probe)
    return probe


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tsv_rows(path):
    with Path(path).open(newline="") as stream:
        return list(csv.reader(stream, delimiter="\t"))


def compare_tables(expected, actual):
    assert expected and actual and expected[0] == actual[0], "table header mismatch"
    assert len(expected) == len(actual), "table row count mismatch"
    strict = {"n", "replication", "root_seed", "method", "covered", "error",
              "coverage_count", "valid", "failures", "replications", "below_truth_misses",
              "above_truth_misses", "primary_reference_solver", "paired_valid",
              "only_full_covers", "only_direct_covers", "coverage_decision_changed"}
    maximum, differences = 0.0, 0
    for before, after in zip(expected[1:], actual[1:]):
        assert len(before) == len(after) == len(expected[0]), "ragged table row"
        for name, left, right in zip(expected[0], before, after):
            if left == right:
                continue
            assert name not in strict and not name.endswith(("_numerator", "_denominator", "_passed")), f"exact field differs: {name}"
            a, b = float(left), float(right)
            assert math.isfinite(a) and math.isfinite(b), "nonfinite mismatch"
            gap = abs(a - b) / max(1.0, abs(a), abs(b))
            assert gap <= SCALED_TOLERANCE, f"numeric discrepancy too large: {name}"
            maximum = max(maximum, gap)
            differences += 1
    return dict(rows=len(actual)-1, columns=len(actual[0]), passed=True,
                exact_cell_equality=differences == 0, differing_numeric_cells=differences,
                max_scaled_error=maximum, scaled_tolerance=SCALED_TOLERANCE)


def run(python, report_path):
    if report_path.exists():
        raise FileExistsError("Preserve the existing report; choose a new path")
    started = time.perf_counter()
    pre = environment_probe(python)
    original = {str(p.relative_to(ROOT)): sha256(p) for p in (ROOT / "results").glob("*.tsv")}
    temp = Path(tempfile.mkdtemp(prefix="rho_verified_replay_20260925_"))
    source, output = temp / "source", temp / "replay"
    source.mkdir()
    archive = subprocess.check_output(["git", "archive", SOURCE_COMMIT], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(source, filter="data")
    command = [str(python), "-I", str(source / "scripts/run_moderate_benchmark_20260920.py"), "--out-dir", str(output)]
    (temp / "pre_execution.json").write_text(json.dumps(dict(environment=pre, command=command,
        source_commit=SOURCE_COMMIT, source_archive_sha256=hashlib.sha256(archive).hexdigest(),
        wrapper_sha256=sha256(__file__)), indent=2) + "\n")
    subprocess.run(command, cwd=source, check=True)
    post = environment_probe(python)
    (temp / "post_execution_environment.json").write_text(json.dumps(post, indent=2) + "\n")
    assert pre == post, "dependency environment changed during reproduction"
    comparisons = {}
    for kind in ("constant_sensitivity", "paired", "population", "replications", "solver", "summary"):
        name = f"moderate_benchmark_{kind}_20260920.tsv"
        expected, actual = tsv_rows(ROOT / "results" / name), tsv_rows(output / name)
        comparisons[name] = {**compare_tables(expected, actual),
                            "frozen_sha256": sha256(ROOT / "results" / name), "replay_sha256": sha256(output / name)}
    frozen_unchanged = all(sha256(ROOT / p) == digest for p, digest in original.items())
    assert frozen_unchanged, "frozen TSV changed"
    runner = json.loads((output / "moderate_benchmark_audit_20260920.json").read_text())
    assert runner["environment"]["isolated_venv"] is True
    assert runner["datasets"] == 6000 and runner["method_rows"] == 18000
    assert runner["failures"] == runner["method_error_rows"] == 0
    historical = {}
    for name in ("core_reproduction_20260916.json", "retained_history_reproduction_20260918.json", "moderate_benchmark_audit_20260920.json", "moderate_reproduction_20260921.json"):
        record = json.loads((ROOT / "results" / name).read_text())
        historical[name] = {"sha256": sha256(ROOT / "results" / name),
                            "recorded_isolated_venv": record["environment"]["isolated_venv"]}
    result = dict(date="2026-09-25", all_passed=True, source_commit=SOURCE_COMMIT,
                  source_archive_sha256=hashlib.sha256(archive).hexdigest(),
                  wrapper_sha256=sha256(__file__), command=command,
                  snapshot=str(source), output=str(output),
                  environment_pre=pre, environment_post=post, environment_unchanged=True,
                  source_sha256=runner["sources"], comparisons=comparisons,
                  frozen_tsv_count=len(original), frozen_tsv_unchanged=frozen_unchanged,
                  original_tsv_sha256=original, historical_record_status=historical,
                  datasets_replayed=6000, method_records_replayed=18000, solver_records_replayed=6000,
                  new_design_cells=0, elapsed_seconds=time.perf_counter() - started,
                  comparison_note="Exact equality is recorded separately. The 1e-10 scaled tolerance is inherited from September 16; all labels, IDs, seeds, decisions and exact rational residuals must match exactly. A first September 25 execution completed without errors but the initial strict string-comparison wrapper stopped on floating-point differences; this final execution retains pre/post probes before comparison and does not suppress that distinction.",
                  scope="Original-seed moderate-study replay in a verified no-system-site virtual environment and isolated source snapshot; not independent implementation, calibration evidence, or mathematical review.",
                  correction="September 18, 20 and 21 manifests record isolated_venv=false. Source isolation and numerical agreement remain valid, but those executions must not be described as verified dependency-isolated runs. The cause of the lost historical virtual-environment configuration is not established. Historical outputs are preserved.")
    report_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("all_passed", "datasets_replayed", "method_records_replayed", "new_design_cells", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    run(args.python, args.report)
