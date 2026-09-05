"""Audit the manuscript Section 6 displays and their inference-track boundaries.

The audit is deliberately read-only with respect to scientific evidence: it
checks that the reporting artifacts retain frozen source cells and do not mix
the theorem-aligned Wald and empirical permutation tracks.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.build_section6_displays_20260905 import (
    MECHANISM_TRACK,
    PERMUTATION_BOUNDARY,
    PERMUTATION_TRACK,
    WALD_TRACK,
    build_bridge_table,
    build_manifest,
    build_mechanism_table,
    build_residual_table,
    build_wald_table,
)
from scripts.robust_extension_utils import write_tsv


RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"
SECTION6 = PROJECT_ROOT / "docs" / "manuscript_draft_section_6_20260905.md"


def _read_tsv(filename: str) -> list[dict[str, str]]:
    with (RESULTS_DIR / filename).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def _same_float(left: str | float, right: str | float) -> bool:
    return abs(float(left) - float(right)) < 1e-14


def _check(name: str, passed: bool, detail: str) -> dict[str, object]:
    return {"check": name, "passed": int(passed), "detail": detail}


def section6_display_audit() -> list[dict[str, object]]:
    wald = _read_tsv("section6_display_table2_wald_20260905.tsv")
    mechanism = _read_tsv("section6_display_figure1_mechanism_20260905.tsv")
    bridge = _read_tsv("section6_display_figure2_bridge_20260905.tsv")
    residual = _read_tsv("section6_display_figure3_residual_20260905.tsv")
    manifest = _read_tsv("section6_display_manifest_20260905.tsv")
    section6 = SECTION6.read_text()
    generated_script = (PROJECT_ROOT / "scripts" / "build_section6_displays_20260905.py").read_text()

    expected = {
        "section6_display_table2_wald_20260905.tsv": build_wald_table(),
        "section6_display_figure1_mechanism_20260905.tsv": build_mechanism_table(),
        "section6_display_figure2_bridge_20260905.tsv": build_bridge_table(),
        "section6_display_figure3_residual_20260905.tsv": build_residual_table(),
        "section6_display_manifest_20260905.tsv": build_manifest(),
    }
    stored = {
        "section6_display_table2_wald_20260905.tsv": wald,
        "section6_display_figure1_mechanism_20260905.tsv": mechanism,
        "section6_display_figure2_bridge_20260905.tsv": bridge,
        "section6_display_figure3_residual_20260905.tsv": residual,
        "section6_display_manifest_20260905.tsv": manifest,
    }
    regeneration_match = all(
        len(stored[name]) == len(expected[name])
        and all(
            all(
                str(actual[key]) == str(value)
                if not isinstance(value, float)
                else _same_float(actual[key], value)
                for key, value in regenerated.items()
            )
            for actual, regenerated in zip(stored[name], expected[name], strict=True)
        )
        for name in expected
    )

    figure_paths = [
        FIGURES_DIR / "manuscript_figure1_reference_switching_20260905.png",
        FIGURES_DIR / "manuscript_figure1_reference_switching_20260905.pdf",
        FIGURES_DIR / "manuscript_figure2_conditioning_bridge_20260905.png",
        FIGURES_DIR / "manuscript_figure2_conditioning_bridge_20260905.pdf",
        FIGURES_DIR / "manuscript_figure3_family_residual_20260905.png",
        FIGURES_DIR / "manuscript_figure3_family_residual_20260905.pdf",
    ]
    source_files_current = all(
        (PROJECT_ROOT / row["source_file"]).exists() for row in manifest
    )

    return [
        _check(
            "display_tables_rebuild_exactly_from_frozen_sources",
            regeneration_match,
            "five display artifacts match reporting-script reconstruction",
        ),
        _check(
            "table2_is_exclusively_theorem_aligned_wald",
            len(wald) == 6 and {row["evidence_track"] for row in wald} == {WALD_TRACK},
            f"{len(wald)} selected regular-IID rows",
        ),
        _check(
            "figure1_is_explicit_noncalibration_mechanism_evidence",
            len(mechanism) == 22
            and {row["evidence_track"] for row in mechanism} == {MECHANISM_TRACK}
            and all("not" in row["theorem_relation"] for row in mechanism),
            f"{len(mechanism)} intervention rows; no permutation rows",
        ),
        _check(
            "figure2_is_exclusively_empirical_permutation_bridge_evidence",
            len(bridge) == 24
            and {row["evidence_track"] for row in bridge} == {PERMUTATION_TRACK}
            and {row["theorem_relation"] for row in bridge} == {PERMUTATION_BOUNDARY},
            f"{len(bridge)} bridge cells with explicit permutation boundary",
        ),
        _check(
            "figure3_is_exclusively_empirical_permutation_residual_evidence",
            len(residual) == 10
            and {row["evidence_track"] for row in residual} == {PERMUTATION_TRACK}
            and all(row["theorem_relation"] == PERMUTATION_BOUNDARY for row in residual),
            f"{len(residual)} matched-index plus prospective residual cells",
        ),
        _check(
            "display_source_manifest_is_current_and_complete",
            len(manifest) == 7 and source_files_current,
            f"{len(manifest)} source entries; all source files present",
        ),
        _check(
            "section6_states_track_and_claim_boundaries",
            all(
                phrase in section6
                for phrase in (
                    "Wald theorem-aligned track",
                    "fully recomputed studentized-permutation track",
                    "not a weak-null permutation theorem",
                    "pointwise, not uniform",
                    "not a universal cutoff",
                )
            ),
            "required track labels and claim boundaries are present",
        ),
        _check(
            "section6_never_mixes_wald_and_permutation_in_one_display",
            "No main display combines the two tracks." in section6,
            "explicit display-separation statement present",
        ),
        _check(
            "display_builder_does_not_introduce_simulation_or_grid_search",
            all(
                token not in generated_script
                for token in (
                    "default_rng",
                    "np.random",
                    "profile_weak_null_test",
                    "profile_studentized_permutation_test",
                )
            ),
            "reporting script only reads frozen tables and renders displays",
        ),
        _check(
            "all_rendered_figure_formats_are_present_and_nonempty",
            all(path.exists() and path.stat().st_size > 10_000 for path in figure_paths),
            ",".join(path.name for path in figure_paths),
        ),
    ]


def main() -> None:
    rows = section6_display_audit()
    write_tsv(RESULTS_DIR / "section6_display_audit_20260905.tsv", rows)
    for row in rows:
        print(row)
    if not all(int(row["passed"]) for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
