"""Supplement the September 20 audit with exact record joins and affine checks.

Read-only on frozen evidence. The fixed-seed API examples are deterministic
unit checks, not new Monte Carlo calibration cells. No old audit is replaced.
"""
import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROOT_SEED = 2026092001
SAMPLE_SIZES = (160, 640, 2560)
REPLICATIONS = 2000
METHODS = ("complete_kde", "direct_only_ablation", "oracle_fixed_reference")
EXPECTED_TRUTH = 0.1625386847281758
DATASET_KEYS = {(n, rep) for n in SAMPLE_SIZES for rep in range(REPLICATIONS)}
RESULT_FILES = tuple(
    ROOT / "results" / f"moderate_benchmark_{name}_20260920.tsv"
    for name in ("replications", "solver", "population", "summary", "paired", "constant_sensitivity")
)


class AuditFailure(ValueError):
    """A stored evidence identity or numerical invariant does not match."""


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def read_tsv(path):
    with Path(path).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def finite_number(row, field, label):
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise AuditFailure(f"{label}: missing or invalid {field}") from exc
    require(math.isfinite(value), f"{label}: nonfinite {field}")
    return value


def integer(row, field, label):
    try:
        value = int(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise AuditFailure(f"{label}: missing or invalid integer {field}") from exc
    require(str(value) == str(row[field]), f"{label}: noncanonical integer {field}")
    return value


def record_key(row, label):
    return integer(row, "n", label), integer(row, "replication", label)


def metadata(row, label, truth):
    # An empty error field is the only success encoding in these source TSVs.
    # In particular, do not interpret nonempty strings 'False' or '0' as success.
    require(row.get("error") == "", f"{label}: missing or nonempty error field")
    require(integer(row, "root_seed", label) == ROOT_SEED, f"{label}: wrong root seed")
    require(finite_number(row, "truth", label) == truth, f"{label}: wrong truth")


def validate_records(method_rows, solver_rows, population_rows):
    """Reject duplicate/missing/out-of-schedule rows before cross-table joins."""
    require(len(population_rows) == 2, "population: expected the two stored integration orders")
    require({integer(r, "order_per_interval", "population") for r in population_rows} == {48, 72},
            "population: wrong integration orders")
    require(all(finite_number(r, "rho_p", "population") == EXPECTED_TRUTH for r in population_rows),
            "population: changed reference truth")
    require(len(method_rows) == len(DATASET_KEYS) * len(METHODS), "method: wrong row count")
    require(len(solver_rows) == len(DATASET_KEYS), "solver: wrong row count")

    method_index = {}
    method_counts = Counter()
    for row in method_rows:
        key = record_key(row, "method")
        method = row.get("method")
        require(method in METHODS, "method: unexpected method name")
        full_key = (*key, method)
        require(full_key not in method_index, f"method: duplicate key {full_key}")
        method_index[full_key] = row
        method_counts[method] += 1
        metadata(row, f"method {full_key}", EXPECTED_TRUTH)
        for field in ("estimate", "se", "z", "coefficient_x", "coefficient_y"):
            finite_number(row, field, f"method {full_key}")
        require(float(row["se"]) > 0, f"method {full_key}: nonpositive SE")
        require(integer(row, "covered", "method") in (0, 1), "method: invalid coverage flag")
    expected_methods = {(*key, method) for key in DATASET_KEYS for method in METHODS}
    require(set(method_index) == expected_methods, "method: scheduled key set mismatch")
    require(all(method_counts[method] == len(DATASET_KEYS) for method in METHODS),
            "method: per-method count mismatch")

    solver_index = {}
    residual_checks = 0
    for row in solver_rows:
        key = record_key(row, "solver")
        require(key not in solver_index, f"solver: duplicate key {key}")
        solver_index[key] = row
        metadata(row, f"solver {key}", EXPECTED_TRUTH)
        for field in ("delta_estimate_checked_se_units", "relative_se_delta",
                      "max_reference_gap_scale_units", "sqrt_n_legacy_score_residual"):
            finite_number(row, field, f"solver {key}")
        require(integer(row, "coverage_decision_changed", "solver") == 0,
                "solver: changed coverage decision conflicts with the retained result")
        for margin in ("x", "y"):
            prefix = f"solver {key}, {margin}"
            numerator = integer(row, margin + "_score_exact_numerator", prefix)
            denominator = integer(row, margin + "_score_exact_denominator", prefix)
            require(denominator > 0, f"{prefix}: nonpositive residual denominator")
            residual = Fraction(numerator, denominator)
            threshold = Fraction(1, 10**8 * key[0])
            require(abs(residual) <= threshold, f"{prefix}: exact residual inequality failed")
            require(row.get(margin + "_exact_residual_passed") == "True",
                    f"{prefix}: missing or false pass flag")
            require(finite_number(row, margin + "_tolerance", prefix) == float(threshold),
                    f"{prefix}: inconsistent tolerance")
            require(finite_number(row, margin + "_score_exact_float", prefix) == float(residual),
                    f"{prefix}: exact residual/float mismatch")
            for field in ("_location", "_score_float"):
                finite_number(row, margin + field, prefix)
            for field in ("_iterations", "_exact_checks"):
                require(integer(row, margin + field, prefix) > 0, f"{prefix}: invalid {field}")
            residual_checks += 1
    require(set(solver_index) == DATASET_KEYS, "solver: scheduled key set mismatch")
    require(set(solver_index) == {key[:2] for key in method_index}, "method/solver join mismatch")
    for key, row in solver_index.items():
        for method in METHODS:
            paired = method_index[(*key, method)]
            require(row["root_seed"] == paired["root_seed"], "joined seed mismatch")
            require(float(row["truth"]) == float(paired["truth"]), "joined truth mismatch")
    return {
        "datasets": len(solver_index), "method_rows": len(method_rows),
        "solver_rows": len(solver_rows), "method_counts": dict(method_counts),
        "exact_marginal_residuals": residual_checks,
        "scheduled_keys_and_cross_table_joins_passed": True,
        "root_seed": ROOT_SEED, "truth": EXPECTED_TRUTH,
    }


def affine_case(n):
    """Document the <= sample-median equality term instead of hiding it."""
    import numpy as np
    from src.cdelta import huber_profile_correlation_inference

    rng = np.random.default_rng(20260925)
    z = rng.normal(size=(n, 2))
    x = np.exp(.4 * z[:, 0])
    y = np.exp(.3 * (.45 * z[:, 0] + np.sqrt(1 - .45**2) * z[:, 1]))
    base = huber_profile_correlation_inference(x, y, reference_solver="score_checked")
    transforms = (("positive", 2., 3., .5, -1.), ("reflected_x", -2., 3., .5, -1.))
    cases = []
    for name, ax, bx, ay, by in transforms:
        changed_x, changed_y = ax * x + bx, ay * y + by
        changed = huber_profile_correlation_inference(changed_x, changed_y, reference_solver="score_checked")
        predicted = np.zeros(n)
        equality_counts = {}
        for margin, raw, scaled, slope, shift in (("x", x, changed_x, ax, bx),
                                                 ("y", y, changed_y, ay, by)):
            median = np.median(raw)
            mad = np.median(np.abs(raw - median))
            transformed_median = np.median(scaled)
            transformed_mad = np.median(np.abs(scaled - transformed_median))
            np.testing.assert_allclose(transformed_median, slope * median + shift, rtol=1e-13, atol=1e-13)
            np.testing.assert_allclose(transformed_mad, abs(slope) * mad, rtol=1e-13, atol=1e-13)
            np.testing.assert_allclose(changed["reference_location_" + margin],
                                       slope * base["reference_location_" + margin] + shift,
                                       rtol=2e-10, atol=2e-10)
            np.testing.assert_allclose(changed["reference_scale_" + margin],
                                       abs(slope) * base["reference_scale_" + margin],
                                       rtol=1e-13, atol=1e-13)
            equality_counts[margin] = {
                "median": int(np.sum(raw == median)),
                "mad_boundary": int(np.sum(np.abs(raw - median) == mad)),
            }
            if slope < 0:
                # Under reflection, the two MAD boundary densities exchange,
                # while the absolute-deviation indicator itself is unchanged.
                # The non-negating <= median equality is the extra IF term.
                bandwidth = 1.06 * np.std(raw, ddof=1) * n**(-.2)
                def density(t):
                    return np.mean(np.exp(-.5 * ((raw - t) / bandwidth)**2)) / (np.sqrt(2*np.pi) * bandwidth)
                f0, fp, fm = (density(t) for t in (median, median + mad, median - mad))
                u = (raw - base["reference_location_" + margin]) / base["reference_scale_" + margin]
                active = np.abs(u) < 1.345
                a, b = np.mean(active), np.mean(u * active)
                delta = base["location_coefficient_" + margin] * 1.4826 * b * (fp - fm) / (a * f0 * (fp + fm))
                predicted += delta * (raw == median)
        predicted -= np.mean(predicted)
        difference = changed["influence"] - base["influence"]
        np.testing.assert_allclose(changed["estimate"], base["estimate"], rtol=2e-10, atol=2e-10)
        np.testing.assert_allclose(difference, predicted, rtol=2e-8, atol=2e-9)
        expected_se = np.std(base["influence"] + predicted, ddof=1) / np.sqrt(n)
        np.testing.assert_allclose(changed["standard_error"], expected_se, rtol=2e-9, atol=2e-10)
        cases.append({
            "n": n, "transformation": name, "equality_counts": equality_counts,
            "estimate_gap": float(changed["estimate"] - base["estimate"]),
            "standard_error_gap": float(changed["standard_error"] - base["standard_error"]),
            "max_if_gap": float(np.max(np.abs(difference))),
            "max_equality_prediction_error": float(np.max(np.abs(difference - predicted))),
        })
    return cases


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run():
    hashes = {str(path.relative_to(ROOT)): sha256(path) for path in RESULT_FILES}
    report = validate_records(*(read_tsv(path) for path in RESULT_FILES[:3]))
    report["affine_checks"] = affine_case(95) + affine_case(96)
    require(hashes == {str(path.relative_to(ROOT)): sha256(path) for path in RESULT_FILES},
            "source evidence changed during this audit")
    provenance = RESULT_FILES + (Path(__file__), ROOT / "tests/test_record_identity_20260925.py",
        ROOT / "src/cdelta.py", ROOT / "scripts/run_moderate_benchmark_20260920.py",
        ROOT / "docs/moderate_benchmark_protocol_20260920.md")
    report.update(all_passed=True, source_sha256={str(p.relative_to(ROOT)): sha256(p) for p in provenance},
        frozen_evidence_unchanged=True, new_simulation_cells=0,
        note="Supplementary record-identity and deterministic API audit; not mathematical peer review or calibration evidence.",
        affine_scope="Median/MAD/Huber references and rho obey the checked affine laws. Under reflection the <= plug-in median equality creates the explicitly predicted finite-sample full-IF/SE difference for the odd sample. MAD absolute-deviation equality membership is invariant. No API convention is changed.")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError("Use a fresh report path")
    report = run()
    with args.report.open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print(json.dumps(report, indent=2))
