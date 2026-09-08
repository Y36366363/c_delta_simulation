"""Numerical correctness and provenance, not assertions of desired coverage."""

import csv
import hashlib
from pathlib import Path

from scripts.validate_active_nuisance_20260907 import (
    ROOT_SEED,
    contamination_checks,
    huber_score,
    mechanism_checks,
    population,
    simulate,
    summarize,
    tensor_check,
    paired_differences,
)

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def test_population_truth_has_an_independent_quadrature_check():
    a, b = tensor_check(24), tensor_check(48)
    assert abs(a["full_if_variance"] - b["full_if_variance"]) < 1e-8
    assert b["cross_moment_error"] < 1e-10
    assert b["mass_error"] < 1e-10
    assert abs(b["full_if_mean"]) < 1e-10
    assert abs(b["mad_if_component_mean"]) < 1e-10
    assert abs(huber_score(population()[0][3], population()[0][2])) < 1e-12
    assert 0.19 < b["rho_p"] < 0.20


def test_reference_and_mad_paths_are_active_but_covariance_cannot_be_dropped():
    row = tensor_check(24)
    assert abs(row["location_coefficient_x"]) > 0.1
    assert row["mad_component_rms"] > 0.02
    assert (
        abs(
            row["full_if_variance"]
            - row["direct_if_variance"]
            - row["nuisance_if_variance"]
            - row["twice_direct_nuisance_covariance"]
        )
        < 1e-12
    )


def test_split_population_contamination_derivatives_converge():
    rows = contamination_checks()
    for point in {row["point"] for row in rows}:
        ordered = sorted(
            [r for r in rows if r["point"] == point], key=lambda r: r["epsilon"]
        )
        assert ordered[0]["scaled_error"] < 3e-5
        assert (
            ordered[0]["scaled_error"]
            < ordered[1]["scaled_error"]
            < ordered[2]["scaled_error"]
        )


def test_mechanism_scope_checks_do_not_require_flat_huber_curvature():
    rows = mechanism_checks()
    assert all(r["passed"] for r in rows)
    assert abs(rows[0]["observed"]) > 0.6
    assert rows[-1]["observed"] == 0


def test_replication_streams_replay_stored_results_without_resimulation_selection():
    stored = read("active_nuisance_replications_20260907.tsv")
    replay = simulate(reps=1)
    for row in replay:
        expected = next(
            r
            for r in stored
            if int(r["n"]) == row["n"]
            and int(r["replication"]) == 0
            and r["method"] == row["method"]
        )
        assert row["root_seed"] == ROOT_SEED
        assert not row["error"]
        assert abs(row["estimate"] - float(expected["estimate"])) < 1e-12
        assert abs(row["se"] - float(expected["se"])) < 1e-12


def test_frozen_summaries_reconstruct_and_keep_failures_and_paired_uncertainty():
    rows = read("active_nuisance_replications_20260907.tsv")
    assert len(rows) == 18000
    assert {int(r["n"]) for r in rows} == {160, 640, 2560}
    assert len({(r["n"], r["replication"], r["method"]) for r in rows}) == len(rows)
    for expected, actual in zip(
        read("active_nuisance_summary_20260907.tsv"), summarize(rows)
    ):
        for key in (
            "coverage",
            "wilson_low",
            "wilson_high",
            "bias",
            "bias_mcse",
            "failures",
            "mean_width",
        ):
            assert abs(float(expected[key]) - actual[key]) < 1e-12
        assert actual["valid"] + actual["failures"] == 2000
        assert actual["wilson_low"] <= actual["coverage"] <= actual["wilson_high"]
    for row in paired_differences(rows):
        assert row["paired_valid"] == 2000
        assert row["paired_mcse"] >= 0
        assert row["maximum_estimate_difference"] < 1e-12


def test_source_and_output_manifest_hashes_are_current():
    rows = read("active_nuisance_manifest_20260907.tsv")
    assert len(rows) >= 9
    for row in rows:
        data = (
            (ROOT / row["path"])
            .read_bytes()
            .replace(b"\r\n", b"\n")
            .replace(b"\r", b"\n")
        )
        assert hashlib.sha256(data).hexdigest() == row["sha256_lf"]


def test_active_manuscript_preserves_refined_claim_boundaries():
    text = (ROOT / "docs/manuscript_draft_sections_3_5_20260904.md").read_text()
    assert "central Huber reference equation is nearly flat" not in text
    for marker in (
        "nonregular",
        "not nearly flat",
        "imposed",
        "undefined",
        "score covariance",
        "not proof that all remaining differences",
        "Forneron, J.-J.",
    ):
        assert marker in text
    assert "Andrews, D. W. K., and Mikusheva, A." not in text
