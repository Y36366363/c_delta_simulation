from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from cdelta import _wilson_interval, c_delta, permutation_test  # noqa: E402
from scripts.run_high_rep_overlap_cross_validation import (  # noqa: E402
    run_forced_overlap_cross_validation,
    run_random_set_null,
)
from scripts.run_teacher_claim_overlap_validation import (  # noqa: E402
    binary_overlap_correlation,
    binary_overlap_pmf,
    make_overlap_scenario,
    permutation_p_value,
    run_binary_overlap_bridge,
    wilson,
)


def read_tsv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def normalize(rows):
    return [dict(row) for row in rows]


def stringify(rows):
    return [{key: str(value) for key, value in row.items()} for row in rows]


def compare_rows(recomputed, stored, label):
    left = stringify(recomputed)
    right = normalize(stored)
    if left != right:
        for index, (a, b) in enumerate(zip(left, right)):
            if a != b:
                raise AssertionError(f"{label} differs at row {index}: {a} != {b}")
        raise AssertionError(f"{label} row count differs")


def audit_reproducibility():
    forced = run_forced_overlap_cross_validation()
    random_null, layers = run_random_set_null()
    binary = run_binary_overlap_bridge()
    compare_rows(
        forced,
        read_tsv(REPO / "results/forced_overlap_high_rep_20260801.tsv"),
        "forced overlap",
    )
    compare_rows(
        random_null,
        read_tsv(REPO / "results/random_set_null_high_rep_20260801.tsv"),
        "random null",
    )
    compare_rows(
        layers,
        read_tsv(REPO / "results/random_set_null_overlap_layers_20260801.tsv"),
        "random null layers",
    )
    compare_rows(
        binary,
        read_tsv(REPO / "results/binary_overlap_bridge_20260801.tsv"),
        "binary bridge",
    )
    return {
        "forced_rows": len(forced),
        "random_null_rows": len(random_null),
        "layer_rows": len(layers),
        "binary_rows": len(binary),
    }


def audit_fast_permutation_equivalence():
    mismatches = []
    comparisons = 0
    for kind_index, kind in enumerate(["l2", "l1"]):
        for background_index, background in enumerate(["normal", "t3", "t2"]):
            for overlap in range(5):
                for rep in range(4):
                    seed = 20910801 + kind_index * 1_000_000 + background_index * 100_000 + overlap * 1_000 + rep
                    x, y, _, _ = make_overlap_scenario(80, background, overlap / 4, seed)
                    result = c_delta(x, y, kind=kind)
                    fast = permutation_p_value(result.dx, result.dy, 199, seed + 77_000)
                    core = permutation_test(
                        x, y, kind=kind, n_perm=199, seed=seed + 77_000
                    )["p_value"]
                    comparisons += 1
                    if abs(fast - core) > 1e-15:
                        mismatches.append((kind, background, overlap, rep, fast, core))
    if mismatches:
        raise AssertionError(mismatches[:5])
    return {"comparisons": comparisons, "mismatches": 0}


def audit_binary_formula():
    checks = 0
    for n, k in [(20, 2), (40, 4), (80, 4), (100, 10)]:
        for overlap in range(k + 1):
            a = np.zeros(n)
            b = np.zeros(n)
            a[:k] = 1
            b[:overlap] = 1
            b[k:k + (k - overlap)] = 1
            empirical = float(np.corrcoef(a, b)[0, 1])
            theoretical = binary_overlap_correlation(n, k, overlap)
            if abs(empirical - theoretical) > 1e-12:
                raise AssertionError((n, k, overlap, empirical, theoretical))
            checks += 1
        probabilities = [binary_overlap_pmf(n, k, m) for m in range(k + 1)]
        if abs(sum(probabilities) - 1.0) > 1e-12:
            raise AssertionError((n, k, "pmf sum"))
        expectation = sum(m * p for m, p in enumerate(probabilities))
        if abs(expectation - k * k / n) > 1e-12:
            raise AssertionError((n, k, "pmf expectation"))
    return {"formula_checks": checks, "pmf_settings": 4}


def effective_monte_carlo_alpha(n_perm, nominal=0.05):
    ranks = np.arange(1, n_perm + 2)
    return float(np.mean(ranks / (n_perm + 1) < nominal))


def audit_intervals_and_null_reference():
    rows = read_tsv(REPO / "results/random_set_null_high_rep_20260801.tsv")
    interval_mismatches = []
    for row in rows:
        total = int(row["repetitions"])
        successes = round(float(row["rejection_rate"]) * total)
        a = wilson(successes, total)
        b = _wilson_interval(successes, total)
        # The project helper uses z=1.96 while the simulation helper uses the
        # more precise normal quantile. Differences below 2e-7 do not affect
        # the four-decimal reported endpoints.
        if max(abs(a[0] - b[0]), abs(a[1] - b[1])) > 2e-7:
            interval_mismatches.append(row)
        if round(a[0], 4) != float(row["wilson_low"]) or round(a[1], 4) != float(row["wilson_high"]):
            interval_mismatches.append(row)
    if interval_mismatches:
        raise AssertionError(interval_mismatches)
    return {
        "wilson_rows_checked": len(rows),
        "effective_alpha_199": effective_monte_carlo_alpha(199),
        "effective_alpha_399": effective_monte_carlo_alpha(399),
        "effective_alpha_499": effective_monte_carlo_alpha(499),
    }


if __name__ == "__main__":
    report = {
        "reproducibility": audit_reproducibility(),
        "permutation_equivalence": audit_fast_permutation_equivalence(),
        "binary_and_hypergeometric": audit_binary_formula(),
        "intervals_and_reference": audit_intervals_and_null_reference(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
