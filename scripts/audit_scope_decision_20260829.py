"""Audit the construct and estimand consequences of the supervisor decision."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import center_salience_vector, divergence_vector, l2_divergence_closed_form
from scripts.freeze_canonical_evidence_20260819 import estimand_audit
from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def scope_decision_audit() -> list[dict[str, object]]:
    """Return deterministic checks supporting the old/new paper separation."""
    x = np.asarray((-8.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0))
    all_to_all = divergence_vector(x, kind="l2")
    closed_form = l2_divergence_closed_form(x)
    closed_form_error = float(np.max(np.abs(all_to_all - closed_form)))

    robust_profile = center_salience_vector(x, center="huber")
    standardized_all_to_all = (
        all_to_all - float(np.mean(all_to_all))
    ) / float(np.std(all_to_all))
    standardized_robust = (
        robust_profile - float(np.mean(robust_profile))
    ) / float(np.std(robust_profile))
    construct_gap = float(
        np.max(np.abs(standardized_all_to_all - standardized_robust))
    )

    estimand = {row["criterion"]: row for row in estimand_audit()}
    rows = [
        {
            "check": "old_l2_all_to_all_closed_form",
            "value": closed_form_error,
            "comparison": "less_than",
            "threshold": 1e-12,
            "passed": int(closed_form_error < 1e-12),
            "interpretation": "old L2 row divergence is exactly a nonlinear mean-centred radial profile",
        },
        {
            "check": "old_and_robust_profiles_not_same_functional",
            "value": construct_gap,
            "comparison": "greater_than",
            "threshold": 0.10,
            "passed": int(construct_gap > 0.10),
            "interpretation": "standardizing does not make the all-to-all and Huber-reference profiles identical",
        },
        {
            "check": "C_rho_CV_identity",
            "value": float(estimand["algebraic_identity"]["value"]),
            "comparison": "less_than",
            "threshold": 2e-15,
            "passed": int(float(estimand["algebraic_identity"]["value"]) < 2e-15),
            "interpretation": "C is rho_P multiplied by marginal profile heterogeneity around its null value",
        },
        {
            "check": "fixed_margin_permutation_p_equivalence",
            "value": float(estimand["permutation_p_equivalence"]["value"]),
            "comparison": "equal_to",
            "threshold": 0.0,
            "passed": int(float(estimand["permutation_p_equivalence"]["value"]) == 0.0),
            "interpretation": "making rho_P primary does not discard fixed-margin permutation evidence",
        },
        {
            "check": "C_changes_at_fixed_rho",
            "value": float(estimand["fixed_rho_population_C_range"]["value"]),
            "comparison": "greater_than",
            "threshold": 2.5,
            "passed": int(float(estimand["fixed_rho_population_C_range"]["value"]) > 2.5),
            "interpretation": "C mixes profile similarity with marginal heterogeneity and is therefore secondary",
        },
    ]
    return rows


def main() -> None:
    rows = scope_decision_audit()
    write_tsv(RESULTS_DIR / "scope_decision_audit_20260829.tsv", rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
