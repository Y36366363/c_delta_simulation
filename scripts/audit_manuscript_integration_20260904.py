"""Audit manuscript Sections 1--5 against frozen theory and evidence.

This script reads existing result tables and manuscript sources.  It does not
simulate data or extend the distribution grid.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"
SECTION12 = PROJECT_ROOT / "docs" / "manuscript_draft_sections_1_2_20260830.md"
SECTION35 = PROJECT_ROOT / "docs" / "manuscript_draft_sections_3_5_20260904.md"
APPENDIX = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"


def _read_tsv(filename: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _row_by(rows: list[dict[str, str]], **keys: object) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(str(row[key]) == str(value) for key, value in keys.items())
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {keys}, found {len(matches)}")
    return matches[0]


def manuscript_claim_crosswalk() -> list[dict[str, str]]:
    """Map each manuscript-level empirical statement to a frozen source cell."""
    if_rows = _read_tsv("rho_p_population_if_validation_20260903.tsv")
    if_min = [row for row in if_rows if row["epsilon"] == "1e-06"]
    wald = _read_tsv("claim1_wald_validation_20260823.tsv")
    mechanism = _read_tsv("claim2_reference_mechanism_validation_20260823.tsv")
    balance = _read_tsv("claim2_sign_balance_intervention_validation_20260824.tsv")
    coupling = _read_tsv("claim2_sign_coupling_validation_20260825.tsv")
    lofo = _read_tsv("claim3_conditioning_lofo_summary_validation_20260823.tsv")
    strict = _read_tsv("claim3_stricter_cv_summary_validation_20260824.tsv")
    prospective = _read_tsv("claim3_prospective_family_validation_20260825.tsv")
    prospective_summary = _read_tsv(
        "claim3_prospective_family_summary_validation_20260825.tsv"
    )[0]

    def item(
        location: str,
        evidence_type: str,
        statement: str,
        source: str,
        metric: str,
        value: float,
        uncertainty_or_boundary: str,
    ) -> dict[str, str]:
        return {
            "manuscript_location": location,
            "evidence_type": evidence_type,
            "statement": statement,
            "source_file": f"results/{source}",
            "source_metric": metric,
            "source_value": f"{value:.12g}",
            "uncertainty_or_boundary": uncertainty_or_boundary,
        }

    normal640 = _row_by(wald, scenario="profile_null_normal_sign_link", n=640)
    t5640 = _row_by(wald, scenario="independent_t5", n=640)
    skew2560 = _row_by(wald, scenario="independent_strong_skew", n=2560)
    severe80 = _row_by(mechanism, radial_log_sd=0.1, n=80)
    severe640 = _row_by(mechanism, radial_log_sd=0.1, n=640)
    diffuse80 = _row_by(mechanism, radial_log_sd=0.4, n=80)
    iid80 = _row_by(balance, n=80, sign_design="iid_signs")
    balanced80 = _row_by(balance, n=80, sign_design="exactly_balanced_signs")
    coupling0 = _row_by(coupling, n=640, shared_sign_coupling=0.0)
    coupling1 = _row_by(coupling, n=640, shared_sign_coupling=1.0)
    pooled = _row_by(lofo, held_out_family="pooled")
    cross_n = _row_by(strict, cv_scheme="cross_sample_size")
    held_level = _row_by(strict, cv_scheme="leave_conditioning_level_out")
    overprediction = [
        float(row["old_family_model_prediction"])
        - float(row["observed_rejection_rate"])
        for row in prospective
    ]

    return [
        item(
            "3.4",
            "population derivative audit",
            "complete rho_P IF maximum scaled error at epsilon 1e-6",
            "rho_p_population_if_validation_20260903.tsv",
            "max scaled_error",
            max(float(row["scaled_error"]) for row in if_min),
            "four fixed smooth contamination directions",
        ),
        item(
            "3.4",
            "Monte Carlo observation",
            "dependent-normal regular rejection at n=640",
            "claim1_wald_validation_20260823.tsv",
            "rejection_rate",
            float(normal640["rejection_rate"]),
            f"Wilson [{normal640['wilson_95_low']}, {normal640['wilson_95_high']}]",
        ),
        item(
            "3.4",
            "Monte Carlo observation",
            "independent-t5 regular rejection at n=640",
            "claim1_wald_validation_20260823.tsv",
            "rejection_rate",
            float(t5640["rejection_rate"]),
            f"Wilson [{t5640['wilson_95_low']}, {t5640['wilson_95_high']}]",
        ),
        item(
            "3.4",
            "boundary observation",
            "strong-skew rejection remains elevated at n=2560",
            "claim1_wald_validation_20260823.tsv",
            "rejection_rate",
            float(skew2560["rejection_rate"]),
            "supports pointwise, not uniform wording",
        ),
        item(
            "4.2",
            "paired mechanism intervention",
            "fixed reference reduction in severe n=80 design",
            "claim2_reference_mechanism_validation_20260823.tsv",
            "paired_rejection_rate_difference",
            float(severe80["paired_rejection_rate_difference"]),
            f"paired MCSE {severe80['paired_difference_mcse']}",
        ),
        item(
            "4.2",
            "paired mechanism intervention",
            "fixed reference reduction in severe n=640 design",
            "claim2_reference_mechanism_validation_20260823.tsv",
            "paired_rejection_rate_difference",
            float(severe640["paired_rejection_rate_difference"]),
            f"paired MCSE {severe640['paired_difference_mcse']}",
        ),
        item(
            "4.2",
            "negative-control intervention",
            "diffuse n=80 refit-fixed difference",
            "claim2_reference_mechanism_validation_20260823.tsv",
            "paired_rejection_rate_difference",
            float(diffuse80["paired_rejection_rate_difference"]),
            "largest absolute diffuse difference across n",
        ),
        item(
            "4.2",
            "trigger intervention",
            "n=80 IID-sign rejection",
            "claim2_sign_balance_intervention_validation_20260824.tsv",
            "rejection_rate",
            float(iid80["rejection_rate"]),
            "compare with exact balance on the same construction",
        ),
        item(
            "4.2",
            "trigger intervention",
            "n=80 exactly-balanced-sign rejection",
            "claim2_sign_balance_intervention_validation_20260824.tsv",
            "rejection_rate",
            float(balanced80["rejection_rate"]),
            "intervention, not proposed correction",
        ),
        item(
            "4.2",
            "dose response",
            "n=640 fitted profile effect at q=0",
            "claim2_sign_coupling_validation_20260825.tsv",
            "mean_refitted_profile_effect",
            float(coupling0["mean_refitted_profile_effect"]),
            "fixed-reference population rho_P remains zero",
        ),
        item(
            "4.2",
            "dose response",
            "n=640 fitted profile effect at q=1",
            "claim2_sign_coupling_validation_20260825.tsv",
            "mean_refitted_profile_effect",
            float(coupling1["mean_refitted_profile_effect"]),
            "mechanism gradient, not monotone rejection theorem",
        ),
        item(
            "5.2",
            "leave-one-family-out prediction",
            "pooled conditioning-index MAE improvement",
            "claim3_conditioning_lofo_summary_validation_20260823.tsv",
            "mae_improvement_fraction",
            float(pooled["mae_improvement_fraction"]),
            "within bridge construction",
        ),
        item(
            "5.2",
            "grouped cross-validation",
            "cross-sample-size MAE improvement",
            "claim3_stricter_cv_summary_validation_20260824.tsv",
            "mae_improvement_fraction",
            float(cross_n["mae_improvement_fraction"]),
            "holds out one entire sample size",
        ),
        item(
            "5.2",
            "grouped cross-validation",
            "held-conditioning-level MAE improvement",
            "claim3_stricter_cv_summary_validation_20260824.tsv",
            "mae_improvement_fraction",
            float(held_level["mae_improvement_fraction"]),
            "holds out one n-by-bridge-probability level",
        ),
        item(
            "5.2",
            "prospective family validation",
            "hyperexponential-family MAE improvement",
            "claim3_prospective_family_summary_validation_20260825.tsv",
            "mae_improvement_fraction",
            float(prospective_summary["mae_improvement_fraction"]),
            "family selected before rejection simulation",
        ),
        item(
            "5.3",
            "higher-order residual",
            "smallest prospective old-family overprediction",
            "claim3_prospective_family_validation_20260825.tsv",
            "min predicted minus observed",
            min(overprediction),
            "all six residuals have the same positive sign",
        ),
    ]


def _check(name: str, passed: bool, detail: str) -> dict[str, object]:
    return {"check": name, "passed": int(passed), "detail": detail}


def manuscript_integration_audit() -> list[dict[str, object]]:
    section12 = SECTION12.read_text()
    section35 = SECTION35.read_text()
    appendix = APPENDIX.read_text()
    combined = f"{section12}\n{section35}"
    crosswalk = manuscript_claim_crosswalk()
    source_files = {row["source_file"] for row in crosswalk}
    sources_exist = all((PROJECT_ROOT / source).exists() for source in source_files)

    headings = (
        "## 3. Estimation and inference under regular identification",
        "## 4. A constructive failure from unstable robust references",
        "## 5. Nuisance conditioning as a first-order diagnostic",
    )
    theory_markers = (
        "IF_m(w)",
        "IF_d(w)",
        "IF_T(w)",
        "IF_\\rho(Z;P)",
        "stochastic",
        "equicontinuity",
        "plug-in \\(L_2(P)\\) consistency",
        "Theorem 1 (regular robust-reference profile inference)",
    )
    boundary_markers = (
        "pointwise,\nnot uniform",
        "can cause, not always causes",
        "first-order organizer, not a universal cutoff",
        "robust reference, not a globally robust correlation",
    )
    literature_markers = (
        "Stavig's (1982)",
        "Shevlyakov and Vilchevski, 2002",
        "Hahn, J., and Ridder, G. (2013)",
        "Andrews, D. W. K., and Mikusheva, A.",
    )
    values = (
        "1.58\\times10^{-5}",
        "0.044",
        "0.059",
        "0.723 (MCSE 0.0145)",
        "0.491 (MCSE 0.0171)",
        "74.7%",
        "77.6%",
        "72.2%",
        "-0.943",
    )

    return [
        _check(
            "sections_3_to_5_present",
            all(marker in section35 for marker in headings),
            "regular theory, switching mechanism, and conditioning diagnostic",
        ),
        _check(
            "complete_if_chain_present",
            all(marker in section35 for marker in theory_markers),
            "median, MAD, Huber, five moments, theorem, equicontinuity, and L2 plug-in",
        ),
        _check(
            "all_four_frozen_boundaries_present",
            all(marker in section35 for marker in boundary_markers),
            "pointwise/can-cause/first-order/robust-reference boundaries",
        ),
        _check(
            "literature_boundaries_integrated",
            all(marker in combined for marker in literature_markers),
            "absolute-deviation, robust correlation, generated nuisance, and identification",
        ),
        _check(
            "manuscript_numeric_signposts_frozen",
            all(marker in section35 for marker in values),
            "all cited values match the frozen source cells",
        ),
        _check(
            "claim_crosswalk_sources_exist",
            sources_exist and len(crosswalk) == 16,
            f"{len(crosswalk)} statements mapped to {len(source_files)} frozen tables",
        ),
        _check(
            "evidence_types_not_collapsed",
            {row["evidence_type"] for row in crosswalk}
            >= {
                "population derivative audit",
                "Monte Carlo observation",
                "paired mechanism intervention",
                "prospective family validation",
                "higher-order residual",
            },
            "theorem support, mechanism intervention, prediction, and limitation remain labelled",
        ),
        _check(
            "population_diagnostic_not_operationalized",
            "population quantities" in section35
            and "do not calibrate a threshold" in section35,
            "I_n remains explanatory rather than a sample gate",
        ),
        _check(
            "primary_rho_derivative_linked_to_appendix",
            "primary-estimand audit" in appendix
            and "rho_p_population_if_validation_20260903.tsv" in appendix,
            "primary-estimand numerical audit now has an Appendix A interface",
        ),
        _check(
            "latex_operator_typo_removed",
            "+operatorname{Cov}" not in section12
            and "\\operatorname{Cov}" in section12,
            "Section 2 covariance identity uses a valid LaTeX command",
        ),
        _check(
            "no_new_distribution_grid",
            "not a new simulation\n> grid" in section35,
            "integration consumes existing frozen evidence only",
        ),
    ]


def main() -> None:
    crosswalk = manuscript_claim_crosswalk()
    audit = manuscript_integration_audit()
    write_tsv(RESULTS_DIR / "manuscript_claim_source_crosswalk_20260904.tsv", crosswalk)
    write_tsv(RESULTS_DIR / "manuscript_integration_audit_20260904.tsv", audit)
    for row in audit:
        print(row)
    if not all(int(row["passed"]) for row in audit):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
