import csv
from pathlib import Path

import numpy as np

from scripts.run_reference_pathway_20260909 import (
    STAGES,
    K,
    C,
    generate,
    one_stage,
    fit_margin,
    profile_result,
    summarize,
    paired,
    model_checks,
    root_sensitivity,
)
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from src.cdelta import huber_profile_correlation_inference

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / "results" / f"reference_pathway_{name}_20260909.tsv").open(
        newline=""
    ) as f:
        return list(csv.DictReader(f, delimiter="\t"))


def test_fixed_scale_linear_huber_matches_sample_mean_on_the_declared_sample():
    x, y = generate(0.1, 80, 0)
    for w in (x, y):
        for stage in ("population_scale", "population_median"):
            t, s, it = fit_margin(w, stage)
            assert np.max(abs((w - t) / s)) < C
            assert abs(t - w.mean()) < 1e-12
            np.testing.assert_allclose(it, w - w.mean(), atol=1e-12)


def test_full_stage_matches_public_estimator_and_se():
    for tau, n in ((0.1, 80), (0.1, 640), (0.4, 80), (0.4, 640)):
        x, y = generate(tau, n, 0)
        stage = one_stage(x, y, "full_fit")
        public = huber_profile_correlation_inference(x, y)
        assert abs(stage["estimate"] - public["estimate"]) < 1e-12
        assert stage["se_stage_aware"] == public["standard_error"]


def test_stage_aware_gradient_matches_moment_chain_on_arbitrary_influences():
    x, y = generate(0.4, 80, 2)
    tx, sx, ix = fit_margin(x, "population_median")
    ty, sy, iy = fit_margin(y, "population_median")
    rho, _, se, _ = profile_result(x, y, tx, ty, ix, iy)
    a, b = abs(x - tx), abs(y - ty)
    m = np.array([np.mean(a * b), a.mean(), b.mean(), np.mean(a * a), np.mean(b * b)])
    vx, vy = np.var(a), np.var(b)
    den = np.sqrt(vx * vy)
    gradient = np.array(
        [
            1 / den,
            -b.mean() / den + rho * a.mean() / vx,
            -a.mean() / den + rho * b.mean() / vy,
            -rho / (2 * vx),
            -rho / (2 * vy),
        ]
    )
    influences = np.column_stack((a * b, a, b, a * a, b * b)) - m
    influences -= ix[:, None] * np.array(
        [
            np.mean(np.sign(x - tx) * b),
            np.mean(np.sign(x - tx)),
            0,
            2 * np.mean(x - tx),
            0,
        ]
    )
    influences -= iy[:, None] * np.array(
        [
            np.mean(np.sign(y - ty) * a),
            0,
            np.mean(np.sign(y - ty)),
            0,
            2 * np.mean(y - ty),
        ]
    )
    assert abs(se - np.std(influences @ gradient, ddof=1) / np.sqrt(len(x))) < 1e-12


def test_frozen_repetitions_have_complete_stage_accounting_and_replay():
    rows = read("replications")
    assert len(rows) == 32000
    assert len({(r["tau"], r["n"], r["replication"], r["stage"]) for r in rows}) == len(
        rows
    )
    for stage in STAGES:
        r = next(
            r
            for r in rows
            if r["tau"] == "0.1"
            and r["n"] == "80"
            and r["replication"] == "0"
            and r["stage"] == stage
        )
        replay = one_stage(*generate(0.1, 80, 0), stage)
        for key in ("estimate", "se_stage_aware", "reference_x", "reference_y"):
            assert abs(float(r[key]) - replay[key]) < 1e-12


def test_summaries_keep_constant_reference_correlation_undefined_and_rebuild():
    rows = read("replications")
    stored = read("summary")
    rebuilt = summarize(rows)
    assert len(stored) == len(rebuilt) == 16
    for a, b in zip(stored, rebuilt, strict=True):
        assert b["valid"] + b["failures"] == 2000
        for key in (
            "mean_rho",
            "stage_aware_rate",
            "direct_only_rate",
            "reference_rmse_x",
            "mean_scale_x",
        ):
            assert abs(float(a[key]) - b[key]) < 1e-12
        if b["stage"] == "population_reference":
            assert b["reference_rmse_x"] == b["reference_rmse_y"] == 0
            assert np.isnan(b["reference_correlation"])
            assert b["stage_aware_rate"] == b["direct_only_rate"]
        assert (
            b["stage_aware_wilson_low"]
            <= b["stage_aware_rate"]
            <= b["stage_aware_wilson_high"]
        )
    for a, b in zip(read("paired"), paired(rows), strict=True):
        assert b["paired_valid"] == 2000
        assert abs(float(a["estimate_difference"]) - b["estimate_difference"]) < 1e-12


def test_singular_median_and_nonflat_huber_are_distinguished():
    rows = model_checks()
    for row in rows:
        assert row["population_raw_mad"] == 1
        assert row["population_rho"] == 0 and row["population_C"] == 1
        assert row["slope_error"] < 1e-8
        assert abs(row["population_huber_slope"]) > 0.6
        assert row["median_center_density"] == 0
    # Population uniqueness does not imply uniqueness in every finite sample.
    separated = np.array([-4.0, -3.0, 3.0, 4.0])
    for t in (-0.5, 0.0, 0.5):
        residual = (separated - t) / K
        assert np.mean(np.clip(residual, -C, C)) == 0
        assert not np.any(abs(residual) < C)


def test_sample_covariance_identity_keeps_empirical_cross_terms():
    x, y = generate(0.1, 80, 3)
    s = np.sign(x)
    rx, ry = abs(x), abs(y)
    tx, ty = x.mean(), y.mean()
    assert min(rx) > abs(tx) and min(ry) > abs(ty)
    cov = lambda a, b: np.mean((a - a.mean()) * (b - b.mean()))
    expected = cov(rx, ry) - tx * cov(s, ry) - ty * cov(rx, s) + tx * ty * np.var(s)
    assert abs(cov(abs(x - tx), abs(y - ty)) - expected) < 1e-14


def test_pairing_permutation_leaves_marginal_reference_fits_unchanged():
    x, y = generate(0.4, 80, 7)
    a = huber_profile_correlation_inference(x, y)
    b = huber_profile_correlation_inference(x, y[::-1])
    for key in (
        "reference_location_x",
        "reference_location_y",
        "reference_scale_x",
        "reference_scale_y",
    ):
        assert abs(a[key] - b[key]) < 1e-12
    assert abs(a["estimate"] - b["estimate"]) > 1e-5


def test_flagged_roots_are_disclosed_and_primary_results_are_not_replaced():
    rows = read("replications")
    stored = read("root_sensitivity")
    sensitivity = root_sensitivity(rows)
    assert len(sensitivity) == len(stored) == 2
    for a, b in zip(stored, sensitivity, strict=True):
        assert abs(float(a["estimate_difference"]) - b["estimate_difference"]) < 1e-12
        assert b["stage_aware_rejection_changed"] == b["direct_rejection_changed"] == 0


def test_pathway_manifest_and_bounded_model_text():
    for row in read("manifest"):
        assert normalized_text_sha256(ROOT / row["path"]) == row["sha256_lf"]
    text = (ROOT / "docs/shared_sign_model_result_20260909.md").read_text()
    assert "conditional rate-balance heuristic" in text
    assert "sample covariance" in text
    assert "not a proved local" in text.replace("**", "")
    assert "exact sign balance" in text
    assert text.count(r"\[") == text.count(r"\]")
