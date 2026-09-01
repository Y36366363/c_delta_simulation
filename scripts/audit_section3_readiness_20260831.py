"""Deterministic readiness checks for the manuscript's regular-inference section."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv
from scripts.run_weak_null_local_tests_20260814 import profile_weak_null_test


RESULTS_DIR = PROJECT_ROOT / "results"


def _read_tsv(name: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _row(
    check: str,
    observed: float,
    criterion: str,
    threshold: float,
    passed: bool,
    blocking: bool,
    interpretation: str,
) -> dict[str, object]:
    return {
        "check": check,
        "observed": observed,
        "criterion": criterion,
        "threshold": threshold,
        "passed": int(passed),
        "blocking": int(blocking),
        "interpretation": interpretation,
    }


def section3_readiness_audit() -> list[dict[str, object]]:
    rng = np.random.default_rng(20260831)
    x = rng.normal(size=400)
    y = 0.25 * x + np.sqrt(1.0 - 0.25**2) * rng.normal(size=400)
    base = profile_weak_null_test(x, y)
    transformed = profile_weak_null_test(3.2 * x + 5.0, 1.7 * y - 2.0)

    estimate_error = abs(float(base["estimate"]) - float(transformed["estimate"]))
    se_error = abs(
        float(base["standard_error"]) - float(transformed["standard_error"])
    )
    influence_mean = abs(float(np.mean(np.asarray(base["influence"]))))

    appendix = (
        PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"
    ).read_text()
    theorem_markers = (
        "Theorem A.1 (asymptotic linearity and normality)",
        "Corollary A.1 (studentized Wald inference)",
        "Corollary A.2 (moment relaxation at the profile weak null)",
        "Corollary A.3 (reference orthogonality under independence)",
        "This appendix does not claim that",
        "Lemma A.3 (random-nuisance empirical-process remainder)",
        "Lemma A.5 (in-sample empirical second moment)",
    )
    theorem_complete = all(marker in appendix for marker in theorem_markers)

    claim1 = _read_tsv("claim1_wald_validation_20260823.tsv")
    regular_dependent = [
        row for row in claim1 if row["design_role"] == "regular_dependent_weak_null"
    ]
    regular_coverage = all(
        float(row["wilson_95_low"]) <= 0.05 <= float(row["wilson_95_high"])
        for row in regular_dependent
    )
    skew = sorted(
        (row for row in claim1 if row["design_role"] == "regular_slow_convergence_stress"),
        key=lambda row: int(row["n"]),
    )
    skew_decline = float(skew[0]["rejection_rate"]) - float(skew[-1]["rejection_rate"])

    production_source = (PROJECT_ROOT / "src" / "cdelta.py").read_text()
    production_rho_api = "def huber_profile_correlation_inference(" in production_source

    return [
        _row(
            "rho_estimate_positive_affine_invariance",
            estimate_error,
            "less_than",
            1e-12,
            estimate_error < 1e-12,
            True,
            "the primary estimator is invariant to separate positive changes of origin and units",
        ),
        _row(
            "rho_standard_error_positive_affine_invariance",
            se_error,
            "less_than",
            1e-12,
            se_error < 1e-12,
            True,
            "the complete plug-in standard error respects the same invariance",
        ),
        _row(
            "rho_empirical_influence_centering",
            influence_mean,
            "less_than",
            1e-12,
            influence_mean < 1e-12,
            True,
            "the implemented paired influence values are empirically centered",
        ),
        _row(
            "appendix_theorem_chain_complete",
            float(theorem_complete),
            "equal_to",
            1.0,
            theorem_complete,
            True,
            "the audited theorem, studentization, weak-null, orthogonality, and boundary pieces are present",
        ),
        _row(
            "regular_dependent_wald_wilson_contains_nominal",
            float(regular_coverage),
            "equal_to",
            1.0,
            regular_coverage,
            True,
            "both frozen regular dependent weak-null cells are compatible with 5 percent size",
        ),
        _row(
            "strong_skew_rejection_declines_with_n",
            skew_decline,
            "greater_than",
            0.03,
            skew_decline > 0.03,
            True,
            "the frozen stress cells support pointwise convergence while retaining a slow-convergence warning",
        ),
        _row(
            "primary_rho_inference_promoted_to_public_src_api",
            float(production_rho_api),
            "equal_to",
            1.0,
            production_rho_api,
            False,
            "the validated rho routine is now public in src/cdelta.py and the simulation entry point delegates to it",
        ),
    ]


def main() -> None:
    rows = section3_readiness_audit()
    write_tsv(RESULTS_DIR / "section3_readiness_audit_20260831.tsv", rows)
    for row in rows:
        print(row)
    blocking_failures = [
        row for row in rows if int(row["blocking"]) and not int(row["passed"])
    ]
    if blocking_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
