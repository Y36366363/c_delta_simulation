"""Source-directed positioning of rho_P against Stavig and classical alternatives.

This audit uses deterministic target-separation witnesses.  It deliberately
does not add a distribution or simulation grid.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import huber_reference_profile
from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"


def stavig_interval_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    """Return Stavig's (1982) interval-level absolute-deviation coefficient.

    The definition uses marginal standard scores with population-standard-
    deviation convention, followed by the paper's finite-n normalizer.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x and y must be one-dimensional and equally sized")
    if x.size < 2 or np.std(x, ddof=0) == 0 or np.std(y, ddof=0) == 0:
        raise ValueError("both variables must have positive dispersion")
    zx = (x - np.mean(x)) / np.std(x, ddof=0)
    zy = (y - np.mean(y)) / np.std(y, ddof=0)
    normalizer = np.sqrt(4.0 * (x.size**2 - 1.0) / 3.0)
    return float(1.0 - np.sum(np.abs(zx - zy)) / normalizer)


def robust_profile_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Return the manuscript estimand's sample analogue."""
    px = huber_reference_profile(np.asarray(x, dtype=float))
    py = huber_reference_profile(np.asarray(y, dtype=float))
    return float(np.corrcoef(px, py)[0, 1])


def _witnesses() -> dict[str, tuple[np.ndarray, np.ndarray, str]]:
    x = np.array([-1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6], dtype=float)
    sign_rewired = np.array(
        [-1, 1, 2, -2, -3, 3, 4, -4, -5, 5, 6, -6], dtype=float
    )
    return {
        "identical_signed_values": (
            x,
            x.copy(),
            "agreement on the trivial equality case",
        ),
        "global_sign_reversal": (
            x,
            -x,
            "identical radial profiles but opposite signed standardized values",
        ),
        "within_radius_sign_rewiring": (
            x,
            sign_rewired,
            "identical radial profiles with selected signs reassigned",
        ),
    }


def target_separation_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for scenario, (x, y, interpretation) in _witnesses().items():
        px = huber_reference_profile(x)
        py = huber_reference_profile(y)
        rows.append(
            {
                "scenario": scenario,
                "n": x.size,
                "stavig_interval_r_ad": stavig_interval_coefficient(x, y),
                "rho_p": robust_profile_correlation(x, y),
                "raw_pearson": float(np.corrcoef(x, y)[0, 1]),
                "profile_max_abs_difference": float(np.max(np.abs(px - py))),
                "interpretation": interpretation,
            }
        )
    return rows


def positioning_rows() -> list[dict[str, str]]:
    """Return a compact, source-audited manuscript positioning table."""
    return [
        {
            "method": "Hoorn c_d",
            "input_object": "within-margin all-to-all divergence rows",
            "center_or_transform": "pairwise Euclidean divergence aggregation",
            "direction_retained": "no",
            "scientific_target": "whether internal divergence patterns match across paired groups",
            "overlap_with_rho_p": "same broad divergence-similarity question",
            "decisive_difference": "all-to-all geometry rather than profiles around a fitted reference",
            "manuscript_role": "historical predecessor and motivation",
            "primary_source": "https://arxiv.org/abs/2510.16717",
        },
        {
            "method": "Stavig ranked r_ad",
            "input_object": "paired ranks",
            "center_or_transform": "L1 rank difference normalized by its independence expectation",
            "direction_retained": "yes, through rank ordering",
            "scientific_target": "rank agreement; identical to Spearman footrule form",
            "overlap_with_rho_p": "uses absolute differences in its formula only",
            "decisive_difference": "compares paired ranks, not paired marginal radii",
            "manuscript_role": "resolve the absolute-deviation naming collision",
            "primary_source": "https://doi.org/10.2466/pms.1982.54.1.164",
        },
        {
            "method": "Stavig interval r_AD",
            "input_object": "paired marginal standard scores",
            "center_or_transform": "mean/SD standardization followed by L1 paired discrepancy",
            "direction_retained": "yes",
            "scientific_target": "agreement of signed standardized paired values",
            "overlap_with_rho_p": "uses absolute loss and marginal standardization",
            "decisive_difference": "L1 discrepancy of signed z scores, not Corr of unsigned robust radii",
            "manuscript_role": "closest title match but a different estimand",
            "primary_source": "https://doi.org/10.2466/pms.1982.54.1.164",
        },
        {
            "method": "fixed-reference absolute-deviation Pearson",
            "input_object": "paired |X-t_x| and |Y-t_y|",
            "center_or_transform": "externally fixed marginal references",
            "direction_retained": "no",
            "scientific_target": "linear co-movement of two fixed radial profiles",
            "overlap_with_rho_p": "same correlation functional after profiles are formed",
            "decisive_difference": "does not account for estimated median/MAD-Huber references",
            "manuscript_role": "closest algebraic ancestor; scalar transformation alone is not novelty",
            "primary_source": "Pearson correlation applied after a prespecified transformation",
        },
        {
            "method": "Pearson correlation",
            "input_object": "paired raw values",
            "center_or_transform": "mean-centered covariance standardized by SDs",
            "direction_retained": "yes",
            "scientific_target": "linear raw-value association",
            "overlap_with_rho_p": "rho_P is Pearson correlation after generated profile transforms",
            "decisive_difference": "raw signed association rather than divergence-profile similarity",
            "manuscript_role": "classical baseline and algebraic building block",
            "primary_source": "standard classical definition",
        },
        {
            "method": "Spearman/Kendall",
            "input_object": "paired ranks or concordant pairs",
            "center_or_transform": "marginal ranks or pairwise order signs",
            "direction_retained": "yes, through ordering",
            "scientific_target": "monotone association or concordance",
            "overlap_with_rho_p": "nonparametric association comparators",
            "decisive_difference": "ordering association is not radial-profile association",
            "manuscript_role": "classical monotone alternatives",
            "primary_source": "standard classical definitions",
        },
        {
            "method": "robust raw-data correlation",
            "input_object": "paired raw values",
            "center_or_transform": "robust covariance/location/scale constructions",
            "direction_retained": "yes",
            "scientific_target": "outlier-resistant raw-value association",
            "overlap_with_rho_p": "shares robust nuisance estimation concerns",
            "decisive_difference": "robustifies raw association, whereas rho_P targets fitted radial profiles",
            "manuscript_role": "prevents an unsupported globally robust correlation claim",
            "primary_source": "https://doi.org/10.1093/biomet/62.3.531",
        },
        {
            "method": "MAD/median principal-variable correlation",
            "input_object": "signed standardized sums and differences of paired raw values",
            "center_or_transform": "median/MAD marginal standardization and robust scales of principal variables",
            "direction_retained": "yes",
            "scientific_target": "outlier-resistant signed raw-value correlation",
            "overlap_with_rho_p": "uses median/MAD nuisance fits and absolute deviations inside robust scales",
            "decisive_difference": "robustifies signed correlation; it does not correlate unsigned marginal radii",
            "manuscript_role": "closest robust-correlation family; Huber/MAD ingredients alone are not novelty",
            "primary_source": "https://doi.org/10.1016/S0167-7152(02)00058-5",
        },
        {
            "method": "Gini correlation",
            "input_object": "paired raw values and marginal ranks/CDF values",
            "center_or_transform": "covariance with a rank transform",
            "direction_retained": "yes",
            "scientific_target": "signed raw association between Pearson and rank approaches",
            "overlap_with_rho_p": "alternative marginally transformed association measure",
            "decisive_difference": "not a correlation between fitted unsigned divergence profiles",
            "manuscript_role": "broader transformed-correlation context",
            "primary_source": "https://doi.org/10.1080/03610928708829359",
        },
        {
            "method": "distance correlation",
            "input_object": "double-centered pairwise distance matrices",
            "center_or_transform": "all pairwise distances with U/V-style centering",
            "direction_retained": "not directly",
            "scientific_target": "general dependence; zero characterizes independence under conditions",
            "overlap_with_rho_p": "both use geometric deviation information",
            "decisive_difference": "omnibus dependence target rather than matched radial-profile similarity",
            "manuscript_role": "modern general-dependence comparator",
            "primary_source": "https://doi.org/10.1214/009053607000000505",
        },
        {
            "method": "Mantel statistic/test",
            "input_object": "two pairwise dissimilarity matrices",
            "center_or_transform": "association across dyadic matrix entries",
            "direction_retained": "depends on dissimilarity definition",
            "scientific_target": "matrix-level association under label permutation",
            "overlap_with_rho_p": "compares two systems of within-sample dissimilarity",
            "decisive_difference": "dyadic edges are dependent and are not IID paired node profiles",
            "manuscript_role": "all-to-all/dyadic alternative with a distinct inferential unit",
            "primary_source": "https://aacrjournals.org/cancerres/article/27/2_Part_1/209/476508/",
        },
    ]


def positioning_audit() -> list[dict[str, object]]:
    rows = {row["scenario"]: row for row in target_separation_rows()}
    x, y, _ = _witnesses()["within_radius_sign_rewiring"]
    x_affine = 3.7 * x + 11.0
    y_affine = 0.8 * y - 4.0
    stavig_affine_error = abs(
        stavig_interval_coefficient(x, y)
        - stavig_interval_coefficient(x_affine, y_affine)
    )
    rho_affine_error = abs(
        robust_profile_correlation(x, y)
        - robust_profile_correlation(x_affine, y_affine)
    )

    checks = [
        (
            "identity_agreement",
            abs(float(rows["identical_signed_values"]["stavig_interval_r_ad"]) - 1.0),
            1e-14,
            "both measures equal one when signed observations are identical",
        ),
        (
            "sign_reversal_preserves_rho_p",
            abs(float(rows["global_sign_reversal"]["rho_p"]) - 1.0),
            1e-14,
            "rho_P intentionally treats equal radii as equal profiles",
        ),
        (
            "sign_reversal_separates_stavig_from_rho_p",
            float(rows["global_sign_reversal"]["stavig_interval_r_ad"]),
            -0.10,
            "Stavig retains signed z-score information and becomes negative",
        ),
        (
            "sign_rewiring_preserves_rho_p",
            abs(float(rows["within_radius_sign_rewiring"]["rho_p"]) - 1.0),
            1e-14,
            "equal robust-reference radii imply equal profiles despite sign rewiring",
        ),
        (
            "sign_rewiring_separates_targets",
            -abs(
                float(rows["within_radius_sign_rewiring"]["stavig_interval_r_ad"])
                - float(rows["within_radius_sign_rewiring"]["rho_p"])
            ),
            -0.20,
            "the two coefficients differ materially on a same-profile witness",
        ),
        (
            "stavig_positive_affine_invariance",
            stavig_affine_error,
            1e-14,
            "separate positive affine transforms cancel under marginal z scoring",
        ),
        (
            "rho_p_positive_affine_invariance",
            rho_affine_error,
            1e-12,
            "separate positive affine transforms preserve robust radial profiles",
        ),
    ]
    return [
        {
            "check": name,
            "observed": observed,
            "criterion": "less_than_or_equal_to",
            "threshold": threshold,
            "passed": int(observed <= threshold),
            "interpretation": interpretation,
        }
        for name, observed, threshold, interpretation in checks
    ]


def main() -> None:
    target_rows = target_separation_rows()
    table_rows = positioning_rows()
    audit_rows = positioning_audit()
    write_tsv(RESULTS_DIR / "stavig_target_separation_20260902.tsv", target_rows)
    write_tsv(
        RESULTS_DIR / "classical_alternative_positioning_20260902.tsv", table_rows
    )
    write_tsv(RESULTS_DIR / "stavig_positioning_audit_20260902.tsv", audit_rows)
    for row in target_rows:
        print(row)
    for row in audit_rows:
        print(row)
    if not all(int(row["passed"]) for row in audit_rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
