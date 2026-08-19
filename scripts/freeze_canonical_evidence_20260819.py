"""Freeze manuscript-facing evidence from existing, fixed-seed simulations.

This script does not run a new simulation.  It selects the predeclared rows
that support the paper's three claims and limitation, records their generating
seeds, and adds binomial Monte Carlo uncertainty in a common format.
"""

from __future__ import annotations

import csv
import hashlib
from math import sqrt
from pathlib import Path
from typing import Iterable

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    rows = list(rows)
    if not rows:
        raise ValueError("cannot write an empty table")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wilson(successes: int, repetitions: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if repetitions <= 0 or not 0 <= successes <= repetitions:
        raise ValueError("invalid binomial count")
    p = successes / repetitions
    denominator = 1.0 + z**2 / repetitions
    centre = (p + z**2 / (2.0 * repetitions)) / denominator
    half = (
        z
        * sqrt(p * (1.0 - p) / repetitions + z**2 / (4.0 * repetitions**2))
        / denominator
    )
    return centre - half, centre + half


def canonical_row(
    *,
    evidence_group: str,
    source: Path,
    scenario: str,
    n: int,
    repetitions: int,
    n_perm: int,
    seed: int,
    rejection: float,
    conditioning_index: float | str = "",
    notes: str,
) -> dict[str, object]:
    successes = int(round(rejection * repetitions))
    if not np.isclose(successes / repetitions, rejection, atol=1e-12):
        raise ValueError(f"{scenario}: rejection rate is inconsistent with count")
    low, high = wilson(successes, repetitions)
    return {
        "evidence_group": evidence_group,
        "source_file": str(source.relative_to(PROJECT_ROOT)),
        "source_sha256": sha256(source),
        "scenario": scenario,
        "n": n,
        "repetitions": repetitions,
        "n_perm": n_perm,
        "root_seed": seed,
        "rejections": successes,
        "rejection_rate": rejection,
        "monte_carlo_se": sqrt(rejection * (1.0 - rejection) / repetitions),
        "wilson_95_low": low,
        "wilson_95_high": high,
        "sqrt_n_sigma_min_j": conditioning_index,
        "notes": notes,
    }


def freeze_regular_calibration() -> list[dict[str, object]]:
    source = RESULTS_DIR / "studentized_permutation_stress_pilot_20260814.tsv"
    selected = {
        "independent_t5": "regular iid global null; finite fourth moment",
        "independent_strong_skew": "regular iid global null; strong marginal skew",
        "profile_null_t5_sign_link": "dependent but zero-profile-correlation weak null",
    }
    output = []
    for row in read_tsv(source):
        scenario = row["scenario"]
        if scenario not in selected:
            continue
        output.append(
            canonical_row(
                evidence_group="regular_calibration",
                source=source,
                scenario=scenario,
                n=int(row["n"]),
                repetitions=int(row["valid_repetitions"]),
                n_perm=int(row["n_perm"]),
                seed=2026081452,
                rejection=float(row["profile_local_rejection"]),
                notes=selected[scenario],
            )
        )
    if len(output) != len(selected):
        raise RuntimeError("regular calibration selection is incomplete")
    return output


def freeze_near_degenerate_failure() -> list[dict[str, object]]:
    source = RESULTS_DIR / "profile_regularity_comparison_pilot_20260816.tsv"
    selected = {0.03, 0.10, 0.20}
    output = []
    for row in read_tsv(source):
        radial_sd = float(row["radial_log_sd"])
        if radial_sd not in selected:
            continue
        output.append(
            canonical_row(
                evidence_group="near_degenerate_failure",
                source=source,
                scenario=f"shared_sign_independent_radii_sd_{radial_sd:g}",
                n=int(row["n"]),
                repetitions=int(row["repetitions"]),
                n_perm=int(row["n_perm"]),
                seed=2026081612,
                rejection=float(row["studentized_rejection"]),
                notes=(
                    "true profile weak null; complete studentization; reference "
                    "regularity increases with radial log-SD"
                ),
            )
        )
    if len(output) != len(selected):
        raise RuntimeError("near-degenerate selection is incomplete")
    return output


def bridge_seed(n: int, probability: float, family: str) -> int:
    families = ("uniform", "exponential", "half_normal", "scaled_beta12")
    return 2026081750 + n + int(round(10000 * probability)) + 100000 * families.index(family)


def freeze_bridge_recovery() -> list[dict[str, object]]:
    source = RESULTS_DIR / "profile_bridge_family_validation_pilot_20260817.tsv"
    jacobian_source = RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv"
    jacobian = {
        (row["scenario"], int(row["n"])): float(row["sqrt_n_minimum_singular_value"])
        for row in read_tsv(jacobian_source)
    }
    output = []
    for row in read_tsv(source):
        scenario = row["scenario"]
        n = int(row["n"])
        probability = float(row["bridge_probability"])
        family = row["bridge_family"]
        output.append(
            canonical_row(
                evidence_group="bridge_recovery",
                source=source,
                scenario=scenario,
                n=n,
                repetitions=int(row["repetitions"]),
                n_perm=int(row["n_perm"]),
                seed=bridge_seed(n, probability, family),
                rejection=float(row["studentized_rejection"]),
                conditioning_index=jacobian[(scenario, n)],
                notes="matched origin density; family-specific bridge shape",
            )
        )
    if len(output) != 24:
        raise RuntimeError("expected 24 matched bridge cells")
    return output


def freeze_family_residual() -> list[dict[str, object]]:
    source = RESULTS_DIR / "profile_bridge_family_validation_confirmatory_20260817.tsv"
    jacobian_source = RESULTS_DIR / "nuisance_jacobian_joined_cells_20260817.tsv"
    jacobian = {
        (row["scenario"], int(row["n"])): float(row["sqrt_n_minimum_singular_value"])
        for row in read_tsv(jacobian_source)
    }
    output = []
    for row in read_tsv(source):
        scenario = row["scenario"]
        n = int(row["n"])
        probability = float(row["bridge_probability"])
        family = row["bridge_family"]
        output.append(
            canonical_row(
                evidence_group="family_residual",
                source=source,
                scenario=scenario,
                n=n,
                repetitions=int(row["repetitions"]),
                n_perm=int(row["n_perm"]),
                seed=bridge_seed(n, probability, family),
                rejection=float(row["studentized_rejection"]),
                conditioning_index=jacobian[(scenario, n)],
                notes=(
                    "confirmatory matched-J transition cell; omnibus family "
                    "homogeneity p=0.0001305, Cramer's V=0.1014"
                ),
            )
        )
    if len(output) != 4:
        raise RuntimeError("expected four confirmatory family-residual cells")
    return output


def estimand_audit() -> list[dict[str, object]]:
    identity_source = RESULTS_DIR / "teacher_profile_pearson_20260807.tsv"
    identity = read_tsv(identity_source)
    cv_source = RESULTS_DIR / "fixed_correlation_cv_weighting_20260808.tsv"
    cv_rows = read_tsv(cv_source)
    population_rows = [row for row in cv_rows if int(row["n"]) == 100]
    high_cv_n2000 = next(
        row
        for row in cv_rows
        if float(row["sigma_x"]) == 1.5
        and float(row["sigma_y"]) == 1.5
        and int(row["n"]) == 2000
    )
    return [
        {
            "criterion": "algebraic_identity",
            "source_file": str(identity_source.relative_to(PROJECT_ROOT)),
            "value": max(float(row["identity_absolute_error"]) for row in identity),
            "implication": "C equals 1 + rho_P times the marginal CV product",
        },
        {
            "criterion": "permutation_p_equivalence",
            "source_file": str(identity_source.relative_to(PROJECT_ROOT)),
            "value": max(float(row["permutation_p_absolute_difference"]) for row in identity),
            "implication": "C and rho_P give identical fixed-margin permutation evidence",
        },
        {
            "criterion": "fixed_rho_population_C_range",
            "source_file": str(cv_source.relative_to(PROJECT_ROOT)),
            "value": max(float(row["population_cdelta_star"]) for row in population_rows)
            - min(float(row["population_cdelta_star"]) for row in population_rows),
            "implication": "at rho_P=0.30, changing only marginal heterogeneity moves C from 1.019 to 3.546",
        },
        {
            "criterion": "high_CV_C_sd_at_n2000",
            "source_file": str(cv_source.relative_to(PROJECT_ROOT)),
            "value": float(high_cv_n2000["sd_sample_cdelta_star"]),
            "implication": "raw C remains unstable under extreme profile heterogeneity",
        },
        {
            "criterion": "estimand_decision",
            "source_file": "derived from the two sources above",
            "value": "rho_P primary; C secondary",
            "implication": "rho_P isolates concordance; report C with both CVs when historical or scientific heterogeneity weighting is desired",
        },
    ]


def main() -> None:
    canonical = (
        freeze_regular_calibration()
        + freeze_near_degenerate_failure()
        + freeze_bridge_recovery()
        + freeze_family_residual()
    )
    write_tsv(RESULTS_DIR / "canonical_evidence_20260819.tsv", canonical)
    write_tsv(RESULTS_DIR / "estimand_choice_audit_20260819.tsv", estimand_audit())
    print(f"froze {len(canonical)} canonical evidence rows")


if __name__ == "__main__":
    main()
