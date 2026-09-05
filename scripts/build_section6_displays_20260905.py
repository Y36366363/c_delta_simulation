"""Build Section 6 manuscript displays from frozen claim evidence only.

This is a reporting script, not a simulation.  It reads fixed-seed result
tables, writes four display-specific machine-readable tables plus a source
manifest, and renders three publication-oriented figures.  The script keeps
the theorem-aligned Wald evidence distinct from both the finite-sample
mechanism interventions and the fully recomputed studentized-permutation
evidence.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/c_delta_matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/private/tmp/c_delta_xdg_cache")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(PROJECT_ROOT))

from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

WALD_TRACK = "Wald; theorem-aligned regular-IID evidence"
MECHANISM_TRACK = "Empirical finite-sample Wald intervention; outside theorem calibration"
PERMUTATION_TRACK = "Fully recomputed studentized permutation; empirical evidence"
PERMUTATION_BOUNDARY = (
    "not direct validation of iid Wald theorem; exact only under declared group invariance"
)

FAMILY_LABELS = {
    "exponential": "Exponential",
    "half_normal": "Half-normal",
    "scaled_beta12": "Scaled Beta(1,2)",
    "uniform": "Uniform",
    "hyperexponential": "Hyperexponential",
}
FAMILY_COLORS = {
    "exponential": "#1b6ca8",
    "half_normal": "#db6d00",
    "scaled_beta12": "#228b5a",
    "uniform": "#8b5fbf",
    "hyperexponential": "#b23a48",
}


def _read_tsv(filename: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _int(row: dict[str, str], key: str) -> int:
    return int(row[key])


def _find_one(rows: list[dict[str, str]], **criteria: object) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(str(row[name]) == str(value) for name, value in criteria.items())
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one row for {criteria}, found {len(matches)}")
    return matches[0]


def _family_epsilon(scenario: str) -> tuple[str, float]:
    family, epsilon = scenario.rsplit("_epsilon_", maxsplit=1)
    return family, float(epsilon)


def _source_hash(filename: str) -> str:
    return normalized_text_sha256(RESULTS_DIR / filename)


def build_wald_table() -> list[dict[str, object]]:
    """Select the six theorem-aligned regular-IID Wald cells."""
    source = "claim1_wald_validation_20260823.tsv"
    rows = _read_tsv(source)
    selections = (
        ("profile_null_normal_sign_link", 160, "Dependent-normal profile weak null", "regular calibration"),
        ("profile_null_normal_sign_link", 640, "Dependent-normal profile weak null", "regular calibration"),
        ("independent_t5", 320, "Independent t(5) global null", "regular calibration"),
        ("independent_t5", 640, "Independent t(5) global null", "regular calibration"),
        ("independent_strong_skew", 640, "Independent strong-skew null", "pointwise convergence boundary"),
        ("independent_strong_skew", 2560, "Independent strong-skew null", "pointwise convergence boundary"),
    )
    display_rows: list[dict[str, object]] = []
    for scenario, n, label, role in selections:
        row = _find_one(rows, scenario=scenario, n=n)
        display_rows.append(
            {
                "display_id": "Table_2",
                "evidence_track": WALD_TRACK,
                "theorem_relation": "finite-sample check aligned with Theorem 1 at a fixed regular IID law",
                "scenario": scenario,
                "display_label": label,
                "display_role": role,
                "n": _int(row, "n"),
                "repetitions": _int(row, "repetitions"),
                "root_cell_seed": _int(row, "root_cell_seed"),
                "rejection_rate": _float(row, "rejection_rate"),
                "monte_carlo_se": _float(row, "monte_carlo_se"),
                "wilson_95_low": _float(row, "wilson_95_low"),
                "wilson_95_high": _float(row, "wilson_95_high"),
                "studentized_z_sd": _float(row, "sd_z"),
                "source_file": f"results/{source}",
                "source_sha256": _source_hash(source),
            }
        )
    return display_rows


def build_mechanism_table() -> list[dict[str, object]]:
    """Assemble causal switching interventions without calling them calibration."""
    source_main = "claim2_reference_mechanism_validation_20260823.tsv"
    source_balance = "claim2_sign_balance_intervention_validation_20260824.tsv"
    source_coupling = "claim2_sign_coupling_validation_20260825.tsv"
    main = _read_tsv(source_main)
    balance = _read_tsv(source_balance)
    coupling = _read_tsv(source_coupling)
    display_rows: list[dict[str, object]] = []

    for radial_log_sd in (0.1, 0.4):
        for n in (80, 640):
            row = _find_one(main, radial_log_sd=radial_log_sd, n=n)
            display_rows.append(
                {
                    "display_id": "Figure_1A",
                    "evidence_track": MECHANISM_TRACK,
                    "theorem_relation": "paired refit-versus-fixed intervention; not a Theorem 1 calibration cell",
                    "intervention": "reference_fit",
                    "radial_log_sd": radial_log_sd,
                    "n": n,
                    "design": "fitted_reference",
                    "repetitions": _int(row, "repetitions"),
                    "root_cell_seed": _int(row, "root_cell_seed"),
                    "rejection_rate": _float(row, "fitted_reference_rejection_rate"),
                    "wilson_95_low": _float(row, "fitted_wilson_95_low"),
                    "wilson_95_high": _float(row, "fitted_wilson_95_high"),
                    "mean_profile_effect": _float(row, "mean_fitted_reference_effect"),
                    "paired_difference": _float(row, "paired_rejection_rate_difference"),
                    "paired_difference_mcse": _float(row, "paired_difference_mcse"),
                    "source_file": f"results/{source_main}",
                    "source_sha256": _source_hash(source_main),
                }
            )
            display_rows.append(
                {
                    "display_id": "Figure_1A",
                    "evidence_track": MECHANISM_TRACK,
                    "theorem_relation": "paired fixed-reference contrast; not a Theorem 1 calibration cell",
                    "intervention": "reference_fit",
                    "radial_log_sd": radial_log_sd,
                    "n": n,
                    "design": "fixed_symmetry_reference",
                    "repetitions": _int(row, "repetitions"),
                    "root_cell_seed": _int(row, "root_cell_seed"),
                    "rejection_rate": _float(row, "fixed_center_rejection_rate"),
                    "wilson_95_low": _float(row, "fixed_center_wilson_95_low"),
                    "wilson_95_high": _float(row, "fixed_center_wilson_95_high"),
                    "mean_profile_effect": _float(row, "mean_fixed_center_effect"),
                    "paired_difference": _float(row, "paired_rejection_rate_difference"),
                    "paired_difference_mcse": _float(row, "paired_difference_mcse"),
                    "source_file": f"results/{source_main}",
                    "source_sha256": _source_hash(source_main),
                }
            )

    for n in (80, 640):
        for sign_design in ("iid_signs", "exactly_balanced_signs"):
            row = _find_one(balance, n=n, sign_design=sign_design)
            display_rows.append(
                {
                    "display_id": "Figure_1B",
                    "evidence_track": MECHANISM_TRACK,
                    "theorem_relation": "trigger intervention; not a proposed correction or theorem calibration",
                    "intervention": "sign_balance",
                    "radial_log_sd": _float(row, "radial_log_sd"),
                    "n": n,
                    "design": sign_design,
                    "repetitions": _int(row, "repetitions"),
                    "root_cell_seed": _int(row, "root_cell_seed"),
                    "rejection_rate": _float(row, "rejection_rate"),
                    "wilson_95_low": _float(row, "wilson_95_low"),
                    "wilson_95_high": _float(row, "wilson_95_high"),
                    "mean_profile_effect": _float(row, "mean_profile_effect"),
                    "mean_maximum_absolute_huber_center": _float(row, "mean_maximum_absolute_huber_center"),
                    "mean_absolute_sign_imbalance": _float(row, "mean_absolute_sign_imbalance"),
                    "source_file": f"results/{source_balance}",
                    "source_sha256": _source_hash(source_balance),
                }
            )

    for n in (80, 640):
        for shared_sign_coupling in (0.0, 0.25, 0.5, 0.75, 1.0):
            row = _find_one(coupling, n=n, shared_sign_coupling=shared_sign_coupling)
            display_rows.append(
                {
                    "display_id": "Figure_1C",
                    "evidence_track": MECHANISM_TRACK,
                    "theorem_relation": "empirical mechanism dose response; not a monotone-rejection theorem",
                    "intervention": "shared_sign_coupling",
                    "n": n,
                    "shared_sign_coupling": shared_sign_coupling,
                    "repetitions": _int(row, "repetitions"),
                    "root_cell_seed": _int(row, "root_cell_seed"),
                    "mean_refitted_profile_effect": _float(row, "mean_refitted_profile_effect"),
                    "mean_fixed_zero_profile_effect": _float(row, "mean_fixed_zero_profile_effect"),
                    "mean_huber_center_product": _float(row, "mean_huber_center_product"),
                    "refitted_rejection_rate": _float(row, "refitted_rejection_rate"),
                    "fixed_zero_rejection_rate": _float(row, "fixed_zero_rejection_rate"),
                    "source_file": f"results/{source_coupling}",
                    "source_sha256": _source_hash(source_coupling),
                }
            )
    return display_rows


def build_bridge_table() -> list[dict[str, object]]:
    """Extract all 24 frozen bridge cells, retaining their exact track label."""
    source = "canonical_evidence_20260819.tsv"
    source_rows = _read_tsv(source)
    display_rows: list[dict[str, object]] = []
    for row in source_rows:
        if row["evidence_group"] != "bridge_recovery":
            continue
        family, epsilon = _family_epsilon(row["scenario"])
        display_rows.append(
            {
                "display_id": "Figure_2",
                "evidence_track": PERMUTATION_TRACK,
                "theorem_relation": row["theorem_alignment"],
                "family": family,
                "family_label": FAMILY_LABELS[family],
                "epsilon": epsilon,
                "n": _int(row, "n"),
                "repetitions": _int(row, "repetitions"),
                "n_perm": _int(row, "n_perm"),
                "root_cell_seed": _int(row, "root_seed"),
                "rejection_rate": _float(row, "rejection_rate"),
                "monte_carlo_se": _float(row, "monte_carlo_se"),
                "wilson_95_low": _float(row, "wilson_95_low"),
                "wilson_95_high": _float(row, "wilson_95_high"),
                "conditioning_index": _float(row, "sqrt_n_sigma_min_j"),
                "source_file": row["source_file"],
                "source_sha256": row["source_sha256"],
            }
        )
    return display_rows


def build_residual_table() -> list[dict[str, object]]:
    """Join the frozen matched-index and prospective-residual evidence."""
    canonical_source = "canonical_evidence_20260819.tsv"
    prospective_source = "claim3_prospective_family_validation_20260825.tsv"
    display_rows: list[dict[str, object]] = []
    for row in _read_tsv(canonical_source):
        if row["evidence_group"] != "family_residual":
            continue
        family, epsilon = _family_epsilon(row["scenario"])
        display_rows.append(
            {
                "display_id": "Figure_3A",
                "evidence_track": PERMUTATION_TRACK,
                "theorem_relation": row["theorem_alignment"],
                "evidence_component": "matched_index_legacy_family",
                "family": family,
                "family_label": FAMILY_LABELS[family],
                "epsilon": epsilon,
                "n": _int(row, "n"),
                "repetitions": _int(row, "repetitions"),
                "n_perm": _int(row, "n_perm"),
                "root_cell_seed": _int(row, "root_seed"),
                "conditioning_index": _float(row, "sqrt_n_sigma_min_j"),
                "observed_rejection_rate": _float(row, "rejection_rate"),
                "wilson_95_low": _float(row, "wilson_95_low"),
                "wilson_95_high": _float(row, "wilson_95_high"),
                "model_prediction": "",
                "absolute_prediction_error": "",
                "source_file": row["source_file"],
                "source_sha256": row["source_sha256"],
            }
        )
    for row in _read_tsv(prospective_source):
        family = row["family"]
        display_rows.append(
            {
                "display_id": "Figure_3B",
                "evidence_track": PERMUTATION_TRACK,
                "theorem_relation": PERMUTATION_BOUNDARY,
                "evidence_component": "prospective_fifth_family_prediction",
                "family": family,
                "family_label": FAMILY_LABELS[family],
                "epsilon": _float(row, "bridge_probability"),
                "n": _int(row, "n"),
                "repetitions": _int(row, "repetitions"),
                "n_perm": _int(row, "n_perm"),
                "root_cell_seed": _int(row, "root_cell_seed"),
                "conditioning_index": _float(row, "conditioning_index"),
                "observed_rejection_rate": _float(row, "observed_rejection_rate"),
                "wilson_95_low": _float(row, "wilson_95_low"),
                "wilson_95_high": _float(row, "wilson_95_high"),
                "model_prediction": _float(row, "old_family_model_prediction"),
                "absolute_prediction_error": _float(row, "absolute_prediction_error"),
                "source_file": f"results/{prospective_source}",
                "source_sha256": _source_hash(prospective_source),
            }
        )
    return display_rows


def build_manifest() -> list[dict[str, object]]:
    """Record every source used by a Section 6 display and its evidence role."""
    entries = (
        ("Table_2", WALD_TRACK, "claim1_wald_validation_20260823.tsv", "six fixed regular-IID Wald cells"),
        ("Figure_1", MECHANISM_TRACK, "claim2_reference_mechanism_validation_20260823.tsv", "paired refit-versus-fixed intervention"),
        ("Figure_1", MECHANISM_TRACK, "claim2_sign_balance_intervention_validation_20260824.tsv", "sign-balance trigger intervention"),
        ("Figure_1", MECHANISM_TRACK, "claim2_sign_coupling_validation_20260825.tsv", "shared-sign coupling dose response"),
        ("Figure_2", PERMUTATION_TRACK, "canonical_evidence_20260819.tsv", "24 frozen bridge-recovery cells"),
        ("Figure_3", PERMUTATION_TRACK, "canonical_evidence_20260819.tsv", "four frozen matched-index family-residual cells"),
        ("Figure_3", PERMUTATION_TRACK, "claim3_prospective_family_validation_20260825.tsv", "six prospective fifth-family cells"),
    )
    return [
        {
            "display_id": display_id,
            "evidence_track": track,
            "source_file": f"results/{source}",
            "source_sha256": _source_hash(source),
            "source_role": role,
        }
        for display_id, track, source, role in entries
    ]


def _save_figure(figure: plt.Figure, stem: str) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    for extension in ("png", "pdf"):
        figure.savefig(
            FIGURES_DIR / f"{stem}.{extension}",
            dpi=320 if extension == "png" else None,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(figure)


def _rectangularize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Give heterogeneous intervention rows one explicit TSV schema.

    Figure 1 combines three intervention types.  Blank cells mean that a
    quantity was not measured in that intervention, rather than a numerical
    zero.  This keeps the reporting file rectangular without inventing values.
    """
    terminal_fields = ("source_file", "source_sha256")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in terminal_fields and field not in fields:
                fields.append(field)
    fields.extend(
        field for field in terminal_fields if any(field in row for row in rows)
    )
    return [{field: row.get(field, "") for field in fields} for row in rows]


def render_mechanism_figure(rows: list[dict[str, object]]) -> None:
    """Render Figure 1 as a causal intervention sequence, not a calibration plot."""
    figure, axes = plt.subplots(1, 3, figsize=(13.4, 3.9), constrained_layout=True)
    panel_a = [row for row in rows if row["display_id"] == "Figure_1A" and row["radial_log_sd"] == 0.1]
    panel_b = [row for row in rows if row["display_id"] == "Figure_1B"]
    panel_c = [row for row in rows if row["display_id"] == "Figure_1C"]

    ax = axes[0]
    positions = np.arange(2)
    width = 0.33
    for offset, design, label, color in (
        (-width / 2, "fitted_reference", "Refit robust reference", "#b23a48"),
        (width / 2, "fixed_symmetry_reference", "Fixed symmetry reference", "#1b6ca8"),
    ):
        selected = sorted(
            [row for row in panel_a if row["design"] == design], key=lambda row: int(row["n"])
        )
        rates = [float(row["rejection_rate"]) for row in selected]
        lower = [rate - float(row["wilson_95_low"]) for rate, row in zip(rates, selected, strict=True)]
        upper = [float(row["wilson_95_high"]) - rate for rate, row in zip(rates, selected, strict=True)]
        ax.bar(positions + offset, rates, width, label=label, color=color, alpha=0.9)
        ax.errorbar(positions + offset, rates, yerr=[lower, upper], fmt="none", color="black", capsize=3, lw=0.9)
    ax.axhline(0.05, color="black", ls="--", lw=0.9)
    ax.set_xticks(positions, ("n = 80", "n = 640"))
    ax.set_ylim(0.0, 0.92)
    ax.set_ylabel("Rejection probability")
    ax.set_title("A. Paired reference intervention\n(separated modes, $\\tau=0.10$)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax = axes[1]
    for offset, design, label, color in (
        (-width / 2, "iid_signs", "IID signs", "#b23a48"),
        (width / 2, "exactly_balanced_signs", "Exactly balanced", "#228b5a"),
    ):
        selected = sorted(
            [row for row in panel_b if row["design"] == design], key=lambda row: int(row["n"])
        )
        rates = [float(row["rejection_rate"]) for row in selected]
        lower = [rate - float(row["wilson_95_low"]) for rate, row in zip(rates, selected, strict=True)]
        upper = [float(row["wilson_95_high"]) - rate for rate, row in zip(rates, selected, strict=True)]
        ax.bar(positions + offset, rates, width, label=label, color=color, alpha=0.9)
        ax.errorbar(positions + offset, rates, yerr=[lower, upper], fmt="none", color="black", capsize=3, lw=0.9)
    ax.axhline(0.05, color="black", ls="--", lw=0.9)
    ax.set_xticks(positions, ("n = 80", "n = 640"))
    ax.set_ylim(0.0, 0.92)
    ax.set_ylabel("Rejection probability")
    ax.set_title("B. Sign-balance trigger intervention\n(same two-mode construction)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax = axes[2]
    for n, color, marker in ((80, "#b23a48", "o"), (640, "#1b6ca8", "s")):
        selected = sorted(
            [row for row in panel_c if int(row["n"]) == n],
            key=lambda row: float(row["shared_sign_coupling"]),
        )
        coupling = [float(row["shared_sign_coupling"]) for row in selected]
        refitted = [float(row["mean_refitted_profile_effect"]) for row in selected]
        fixed = [float(row["mean_fixed_zero_profile_effect"]) for row in selected]
        ax.plot(coupling, refitted, color=color, marker=marker, lw=1.8, label=f"Refit, n = {n}")
        ax.plot(coupling, fixed, color=color, marker=marker, lw=1.0, ls="--", alpha=0.8, label=f"Fixed, n = {n}")
    ax.axhline(0.0, color="black", lw=0.8)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.07, 0.90)
    ax.set_xlabel("Shared-sign coupling $q$")
    ax.set_ylabel("Mean profile correlation estimate")
    ax.set_title("C. Coupling dose response\n(fixed-reference target is zero)")
    ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="upper left")

    figure.suptitle(
        "Figure 1. Empirical switching interventions (finite-sample Wald contrasts; not theorem calibration)",
        fontsize=11,
        y=1.15,
    )
    _save_figure(figure, "manuscript_figure1_reference_switching_20260905")


def render_bridge_figure(rows: list[dict[str, object]]) -> None:
    """Render the full frozen bridge evidence in separate sample-size panels."""
    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.0), sharey=True, constrained_layout=True)
    for ax, n in zip(axes, (80, 320), strict=True):
        for family in ("exponential", "half_normal", "scaled_beta12", "uniform"):
            selected = sorted(
                [row for row in rows if int(row["n"]) == n and row["family"] == family],
                key=lambda row: float(row["conditioning_index"]),
            )
            x = np.asarray([float(row["conditioning_index"]) for row in selected])
            y = np.asarray([float(row["rejection_rate"]) for row in selected])
            lower = y - np.asarray([float(row["wilson_95_low"]) for row in selected])
            upper = np.asarray([float(row["wilson_95_high"]) for row in selected]) - y
            ax.errorbar(
                x,
                y,
                yerr=np.vstack((lower, upper)),
                color=FAMILY_COLORS[family],
                marker="o",
                ms=4.5,
                lw=1.5,
                capsize=2.5,
                label=FAMILY_LABELS[family],
            )
        ax.axhline(0.05, color="black", ls="--", lw=0.9, label="Nominal .05")
        ax.set_xlim(0.12, 1.90)
        ax.set_ylim(0.0, 0.68)
        ax.set_xlabel(r"$I_n = \sqrt{n}\,\sigma_{\min}(J)$")
        ax.set_title(f"n = {n}")
        ax.grid(axis="y", color="0.9", lw=0.6)
    axes[0].set_ylabel("Rejection probability")
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")
    figure.suptitle(
        "Figure 2. Frozen bridge transition: fully recomputed studentized-permutation evidence only\n"
        "(150 replications and 99 permutations per cell; empirical, not Wald-theorem validation)",
        fontsize=10.5,
        y=1.15,
    )
    _save_figure(figure, "manuscript_figure2_conditioning_bridge_20260905")


def render_residual_figure(rows: list[dict[str, object]]) -> None:
    """Render matched-index family residuals and prospective prediction residuals."""
    figure, axes = plt.subplots(1, 2, figsize=(10.7, 4.0), constrained_layout=True)
    legacy = [row for row in rows if row["evidence_component"] == "matched_index_legacy_family"]
    prospective = [row for row in rows if row["evidence_component"] == "prospective_fifth_family_prediction"]

    ax = axes[0]
    legacy = sorted(legacy, key=lambda row: ("exponential", "half_normal", "scaled_beta12", "uniform").index(str(row["family"])))
    positions = np.arange(len(legacy))
    rates = np.asarray([float(row["observed_rejection_rate"]) for row in legacy])
    lower = rates - np.asarray([float(row["wilson_95_low"]) for row in legacy])
    upper = np.asarray([float(row["wilson_95_high"]) for row in legacy]) - rates
    colors = [FAMILY_COLORS[str(row["family"])] for row in legacy]
    ax.bar(positions, rates, color=colors, alpha=0.9)
    ax.errorbar(positions, rates, yerr=np.vstack((lower, upper)), fmt="none", color="black", capsize=3, lw=0.9)
    ax.axhline(0.05, color="black", ls="--", lw=0.9)
    ax.set_xticks(positions, ("Exponential", "Half-normal", "Beta(1,2)", "Uniform"), rotation=18, ha="right")
    ax.set_ylim(0.0, 0.46)
    ax.set_ylabel("Rejection probability")
    ax.set_title(
        "A. Legacy families at matched\n"
        r"first-order index ($I_n \approx 0.445$)"
    )
    ax.text(0.02, 0.95, "Homogeneity p = .0001305\nCramér's V = .1014", transform=ax.transAxes, va="top", fontsize=8.5)

    ax = axes[1]
    markers = {80: "o", 320: "s"}
    annotation_offsets = {
        (80, 0.05): (5, 4),
        (80, 0.10): (5, -11),
        (80, 0.20): (5, 8),
        (320, 0.05): (5, 5),
        (320, 0.10): (5, -4),
        (320, 0.20): (5, 4),
    }
    for row in prospective:
        epsilon = float(row["epsilon"])
        n = int(row["n"])
        prediction = float(row["model_prediction"])
        observed = float(row["observed_rejection_rate"])
        lower = observed - float(row["wilson_95_low"])
        upper = float(row["wilson_95_high"]) - observed
        ax.errorbar(
            prediction,
            observed,
            yerr=[[lower], [upper]],
            fmt="none",
            color="0.25",
            capsize=2,
            lw=0.8,
            zorder=2,
        )
        ax.scatter(
            prediction,
            observed,
            color={0.05: "#b23a48", 0.1: "#db6d00", 0.2: "#1b6ca8"}[epsilon],
            marker=markers[n],
            s=48,
            zorder=3,
        )
        ax.annotate(
            f"{n}, {epsilon:.2f}",
            (prediction, observed),
            xytext=annotation_offsets[(n, epsilon)],
            textcoords="offset points",
            fontsize=7,
        )
    ax.plot((0.0, 0.62), (0.0, 0.62), color="black", ls="--", lw=0.9)
    ax.set_xlim(0.0, 0.62)
    ax.set_ylim(0.0, 0.62)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Old-family index-model prediction")
    ax.set_ylabel("Hyperexponential observed rejection")
    ax.set_title("B. Prospective fifth-family residual\n(all predictions lie above observed rates)")
    epsilon_handles = [
        plt.Line2D([], [], marker="o", color="none", markerfacecolor=color, markeredgecolor=color, label=label)
        for color, label in (("#b23a48", "$\\epsilon=.05$"), ("#db6d00", "$\\epsilon=.10$"), ("#1b6ca8", "$\\epsilon=.20$"))
    ]
    size_handles = [
        plt.Line2D([], [], marker=marker, color="black", ls="none", label=f"n = {n}")
        for n, marker in ((80, "o"), (320, "s"))
    ]
    ax.legend(handles=epsilon_handles + size_handles, frameon=False, fontsize=7.5, ncol=2, loc="upper left")

    figure.suptitle(
        "Figure 3. Higher-order family residuals: fully recomputed studentized-permutation evidence only",
        fontsize=10.5,
        y=1.04,
    )
    _save_figure(figure, "manuscript_figure3_family_residual_20260905")


def build_all_displays() -> dict[str, list[dict[str, object]]]:
    """Write display tables, source manifest, and all three frozen-data figures."""
    tables = {
        "section6_display_table2_wald_20260905.tsv": build_wald_table(),
        "section6_display_figure1_mechanism_20260905.tsv": build_mechanism_table(),
        "section6_display_figure2_bridge_20260905.tsv": build_bridge_table(),
        "section6_display_figure3_residual_20260905.tsv": build_residual_table(),
        "section6_display_manifest_20260905.tsv": build_manifest(),
    }
    for filename, rows in tables.items():
        write_tsv(RESULTS_DIR / filename, _rectangularize(rows))
    render_mechanism_figure(tables["section6_display_figure1_mechanism_20260905.tsv"])
    render_bridge_figure(tables["section6_display_figure2_bridge_20260905.tsv"])
    render_residual_figure(tables["section6_display_figure3_residual_20260905.tsv"])
    return tables


def main() -> None:
    tables = build_all_displays()
    for filename, rows in tables.items():
        print(f"{filename}: {len(rows)} rows")


if __name__ == "__main__":
    main()
