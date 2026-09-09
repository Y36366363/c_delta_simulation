"""Four paired interventions specified in reference_pathway_protocol_20260909.md."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.cdelta import huber_profile_correlation_inference, _gaussian_kde_density
from scripts.robust_extension_utils import write_tsv
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from scripts.validate_active_nuisance_20260907 import wilson

K, C, ZCRIT = 1.4826, 1.345, 1.959963984540054
SEED, REPS = 2026090901, 2000
STAGES = ("population_reference", "population_scale", "population_median", "full_fit")


def generate(tau, n, rep, seed=SEED):
    rng = np.random.default_rng(
        np.random.SeedSequence([seed, round(100 * tau), n, rep])
    )
    signs = rng.choice((-1.0, 1.0), size=n)
    return signs * np.exp(tau * rng.normal(size=n)), signs * np.exp(
        tau * rng.normal(size=n)
    )


def fit_margin(w, stage):
    if stage == "population_reference":
        return 0.0, K, np.zeros(w.size)
    d = 1.0 if stage == "population_scale" else float(np.median(np.abs(w)))
    s = K * d
    score = lambda t: float(np.mean(np.clip((w - t) / s, -C, C)))
    t = float(brentq(score, float(np.min(w)), float(np.max(w)), xtol=1e-13))
    residual = (w - t) / s
    active = abs(residual) < C
    a, b = float(np.mean(active)), float(np.mean(residual * active))
    it = s / a * np.clip(residual, -C, C)
    if stage == "population_median":
        density = _gaussian_kde_density(w, d) + _gaussian_kde_density(w, -d)
        if not np.isfinite(density) or density <= 0:
            raise ValueError("invalid endpoint density")
        id_ = (0.5 - (abs(w) <= d)) / density
        it = it - b / a * K * id_
    return t, s, it


def profile_result(x, y, tx, ty, ix, iy):
    a, b = np.abs(x - tx), np.abs(y - ty)
    ac, bc = a - a.mean(), b - b.mean()
    vx, vy = np.mean(ac**2), np.mean(bc**2)
    if min(vx, vy) <= 0:
        raise ValueError("zero profile variance")
    denom = np.sqrt(vx * vy)
    rho = float(np.mean(ac * bc) / denom)
    direct = ac * bc / denom - rho / 2 * (ac**2 / vx + bc**2 / vy)
    gx, gy = np.mean(np.sign(x - tx)), np.mean(np.sign(y - ty))
    cx = (-np.mean(np.sign(x - tx) * b) + gx * b.mean()) / denom
    cx += rho * (np.mean(x - tx) - a.mean() * gx) / vx
    cy = (-np.mean(np.sign(y - ty) * a) + gy * a.mean()) / denom
    cy += rho * (np.mean(y - ty) - b.mean() * gy) / vy
    full = direct + cx * ix + cy * iy
    se_full = float(np.std(full, ddof=1) / np.sqrt(x.size))
    se_direct = float(np.std(direct, ddof=1) / np.sqrt(x.size))
    return rho, float(np.mean(a * b) / (a.mean() * b.mean())), se_full, se_direct


def one_stage(x, y, stage):
    root_gap = 0.0
    if stage == "full_fit":
        full = huber_profile_correlation_inference(x, y)
        tx, ty = full["reference_location_x"], full["reference_location_y"]
        sx, sy = full["reference_scale_x"], full["reference_scale_y"]
        rho, historical, _, direct_se = profile_result(x, y, tx, ty, 0.0, 0.0)
        se = full["standard_error"]
        for w, t, s in ((x, tx, sx), (y, ty, sy)):
            root = brentq(
                lambda u: np.mean(np.clip((w - u) / s, -C, C)),
                w.min(),
                w.max(),
                xtol=1e-13,
            )
            root_gap = max(root_gap, abs(root - t) / s)
    else:
        tx, sx, ix = fit_margin(x, stage)
        ty, sy, iy = fit_margin(y, stage)
        rho, historical, se, direct_se = profile_result(x, y, tx, ty, ix, iy)
    if (
        not np.all(np.isfinite([rho, historical, se, direct_se, tx, ty, sx, sy]))
        or min(se, direct_se) <= 0
    ):
        raise ValueError("nonfinite estimate or invalid SE")
    return {
        "estimate": rho,
        "historical_C": historical,
        "se_stage_aware": se,
        "se_direct_only": direct_se,
        "reject_stage_aware": int(abs(rho / se) > ZCRIT),
        "reject_direct_only": int(abs(rho / direct_se) > ZCRIT),
        "reference_x": tx,
        "reference_y": ty,
        "scale_x": sx,
        "scale_y": sy,
        "active_fraction_x": float(np.mean(abs((x - tx) / sx) < C)),
        "active_fraction_y": float(np.mean(abs((y - ty) / sy) < C)),
        "score_residual_max": max(
            abs(np.mean(np.clip((x - tx) / sx, -C, C))),
            abs(np.mean(np.clip((y - ty) / sy, -C, C))),
        ),
        "root_gap_in_scale_units": root_gap,
        "error": "",
    }


def run(reps=REPS):
    rows = []
    fields = (
        "estimate",
        "historical_C",
        "se_stage_aware",
        "se_direct_only",
        "reject_stage_aware",
        "reject_direct_only",
        "reference_x",
        "reference_y",
        "scale_x",
        "scale_y",
        "active_fraction_x",
        "active_fraction_y",
        "score_residual_max",
        "root_gap_in_scale_units",
        "error",
    )
    for tau in (0.10, 0.40):
        for n in (80, 640):
            for rep in range(reps):
                x, y = generate(tau, n, rep)
                base = {
                    "tau": tau,
                    "n": n,
                    "replication": rep,
                    "root_seed": SEED,
                    "sign_mean": float(np.mean(np.sign(x))),
                    "sample_mean_x": float(x.mean()),
                    "sample_mean_y": float(y.mean()),
                    "sample_median_x": float(np.median(x)),
                    "sample_median_y": float(np.median(y)),
                }
                for stage in STAGES:
                    try:
                        result = one_stage(x, y, stage)
                    except (ValueError, FloatingPointError, ZeroDivisionError) as error:
                        result = {key: np.nan for key in fields}
                        result["error"] = str(error)
                    rows.append({**base, "stage": stage, **result})
            print(f"completed tau={tau}, n={n}, repetitions={reps}", flush=True)
    return rows


def corr_mcse(x, y):
    a, b = x - x.mean(), y - y.mean()
    vx, vy = np.mean(a * a), np.mean(b * b)
    if min(vx, vy) <= 0:
        return np.nan, np.nan
    r = float(np.mean(a * b) / np.sqrt(vx * vy))
    influence = a * b / np.sqrt(vx * vy) - r / 2 * (a * a / vx + b * b / vy)
    return r, float(np.std(influence, ddof=1) / np.sqrt(len(x)))


def summarize(rows):
    output = []
    for tau in (0.10, 0.40):
        for n in (80, 640):
            for stage in STAGES:
                cell = [
                    r
                    for r in rows
                    if float(r["tau"]) == tau
                    and int(r["n"]) == n
                    and r["stage"] == stage
                ]
                valid = [r for r in cell if not r["error"]]
                if len(valid) < 2:
                    raise ValueError("insufficient valid replications")
                arr = lambda key: np.array([float(r[key]) for r in valid])
                tx, ty = arr("reference_x"), arr("reference_y")
                cor, cor_se = corr_mcse(tx, ty)
                out = {
                    "tau": tau,
                    "n": n,
                    "stage": stage,
                    "root_seed": SEED,
                    "replications": len(cell),
                    "valid": len(valid),
                    "failures": len(cell) - len(valid),
                    "mean_rho": float(arr("estimate").mean()),
                    "mean_rho_mcse": float(
                        arr("estimate").std(ddof=1) / np.sqrt(len(valid))
                    ),
                    "mean_C": float(arr("historical_C").mean()),
                    "reference_correlation": cor,
                    "reference_correlation_mcse": cor_se,
                    "mean_reference_product": float(np.mean(tx * ty)),
                    "mean_active_fraction": float(
                        np.mean(
                            (arr("active_fraction_x") + arr("active_fraction_y")) / 2
                        )
                    ),
                    "max_root_gap_in_scale_units": float(
                        arr("root_gap_in_scale_units").max()
                    ),
                    "max_score_residual": float(arr("score_residual_max").max()),
                    "scope": "empirical null rejection; not a finite-sample validity certificate",
                }
                for margin, t in (("x", tx), ("y", ty)):
                    rmse = float(np.sqrt(np.mean(t * t)))
                    out[f"reference_rmse_{margin}"] = rmse
                    out[f"reference_rmse_mcse_{margin}"] = (
                        float(np.std(t * t, ddof=1) / (2 * rmse * np.sqrt(len(t))))
                        if rmse
                        else 0.0
                    )
                    out[f"reference_minus_mean_rmse_{margin}"] = float(
                        np.sqrt(np.mean((t - arr(f"sample_mean_{margin}")) ** 2))
                    )
                    out[f"reference_sign_correlation_{margin}"] = corr_mcse(
                        t, arr("sign_mean")
                    )[0]
                    out[f"mean_scale_{margin}"] = float(arr(f"scale_{margin}").mean())
                    out[f"median_rmse_{margin}"] = float(
                        np.sqrt(np.mean(arr(f"sample_median_{margin}") ** 2))
                    )
                for track in ("stage_aware", "direct_only"):
                    count = int(arr(f"reject_{track}").sum())
                    lo, hi = wilson(count, len(valid))
                    out[f"{track}_rejections"] = count
                    out[f"{track}_rate"] = count / len(valid)
                    out[f"{track}_wilson_low"] = lo
                    out[f"{track}_wilson_high"] = hi
                    out[f"{track}_mcse"] = float(
                        np.sqrt(
                            count / len(valid) * (1 - count / len(valid)) / len(valid)
                        )
                    )
                output.append(out)
    return output


def paired(rows):
    output = []
    contrasts = list(zip(STAGES[:-1], STAGES[1:])) + [(STAGES[1], STAGES[3])]
    for tau in (0.1, 0.4):
        for n in (80, 640):
            by_stage = {
                stage: {
                    int(r["replication"]): r
                    for r in rows
                    if float(r["tau"]) == tau
                    and int(r["n"]) == n
                    and r["stage"] == stage
                    and not r["error"]
                }
                for stage in STAGES
            }
            for first, second in contrasts:
                ids = sorted(by_stage[first].keys() & by_stage[second].keys())
                out = {
                    "tau": tau,
                    "n": n,
                    "from_stage": first,
                    "to_stage": second,
                    "paired_valid": len(ids),
                }
                for metric in (
                    "reject_stage_aware",
                    "reject_direct_only",
                    "estimate",
                    "reference_x",
                    "reference_y",
                ):
                    power = 2 if metric.startswith("reference") else 1
                    difference = np.array(
                        [
                            float(by_stage[second][i][metric]) ** power
                            - float(by_stage[first][i][metric]) ** power
                            for i in ids
                        ]
                    )
                    name = metric if power == 1 else metric + "_mse"
                    out[name + "_difference"] = float(difference.mean())
                    out[name + "_paired_mcse"] = float(
                        difference.std(ddof=1) / np.sqrt(len(ids))
                    )
                output.append(out)
    return output


def model_checks():
    rows = []
    for tau in (0.1, 0.4):
        a = float(norm.cdf(np.log(C * K) / tau))
        # Distribution-level smooth score derivative, using analytic lognormal truncated moments.
        from scripts.validate_active_nuisance_20260907 import huber_score

        score = lambda t: 0.5 * (huber_score(t, K, tau) - huber_score(-t, K, tau))
        h = 1e-5
        numerical = (score(h) - score(-h)) / (2 * h)
        rows.append(
            {
                "tau": tau,
                "population_median": 0.0,
                "population_raw_mad": 1.0,
                "population_scale": K,
                "population_reference": 0.0,
                "population_rho": 0.0,
                "population_C": 1.0,
                "population_huber_active_probability": a,
                "population_huber_slope": -a / K,
                "numerical_huber_slope": numerical,
                "slope_error": abs(numerical + a / K),
                "radial_variance": float(np.exp(tau * tau) * np.expm1(tau * tau)),
                "median_center_density": 0.0,
            }
        )
    return rows


def root_sensitivity(rows):
    """Replay only flagged numerical roots, retaining original primary results."""
    output = []
    for row in rows:
        if (
            row["stage"] != "full_fit"
            or row["error"]
            or float(row["root_gap_in_scale_units"]) <= 1e-7
        ):
            continue
        tau, n, rep = float(row["tau"]), int(row["n"]), int(row["replication"])
        x, y = generate(tau, n, rep)
        fits = []
        for w in (x, y):
            m = float(np.median(w))
            d = float(np.median(abs(w - m)))
            s = K * d
            t = brentq(
                lambda t: np.mean(np.clip((w - t) / s, -C, C)),
                w.min(),
                w.max(),
                xtol=1e-13,
            )
            fm = _gaussian_kde_density(w, m)
            fp, fn = _gaussian_kde_density(w, m + d), _gaussian_kde_density(w, m - d)
            im = (0.5 - (w <= m)) / fm
            id_ = (0.5 - (abs(w - m) <= d) - (fp - fn) * im) / (fp + fn)
            residual = (w - t) / s
            active = abs(residual) < C
            a, b = np.mean(active), np.mean(residual * active)
            it = s / a * np.clip(residual, -C, C) - b / a * K * id_
            fits.append((t, it))
        rho, _, se, direct = profile_result(
            x, y, fits[0][0], fits[1][0], fits[0][1], fits[1][1]
        )
        output.append(
            {
                "tau": tau,
                "n": n,
                "replication": rep,
                "original_root_gap": float(row["root_gap_in_scale_units"]),
                "estimate_difference": rho - float(row["estimate"]),
                "relative_stage_aware_se_difference": se / float(row["se_stage_aware"])
                - 1,
                "stage_aware_rejection_changed": int(
                    int(abs(rho / se) > ZCRIT) != int(row["reject_stage_aware"])
                ),
                "direct_rejection_changed": int(
                    int(abs(rho / direct) > ZCRIT) != int(row["reject_direct_only"])
                ),
                "scope": "diagnostic only; original repetition retained",
            }
        )
    return output


def manifest():
    paths = [
        "scripts/run_reference_pathway_20260909.py",
        "src/cdelta.py",
        "scripts/validate_active_nuisance_20260907.py",
        "docs/reference_pathway_protocol_20260909.md",
    ]
    paths += [
        f"results/reference_pathway_{name}_20260909.tsv"
        for name in (
            "replications",
            "summary",
            "paired",
            "model_checks",
            "root_sensitivity",
        )
    ]
    write_tsv(
        ROOT / "results/reference_pathway_manifest_20260909.tsv",
        [{"path": p, "sha256_lf": normalized_text_sha256(ROOT / p)} for p in paths],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    path = ROOT / "results/reference_pathway_replications_20260909.tsv"
    if args.summarize_only:
        with path.open(newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
    else:
        rows = run()
        write_tsv(path, rows)
    summaries = summarize(rows)
    write_tsv(ROOT / "results/reference_pathway_summary_20260909.tsv", summaries)
    write_tsv(ROOT / "results/reference_pathway_paired_20260909.tsv", paired(rows))
    write_tsv(
        ROOT / "results/reference_pathway_model_checks_20260909.tsv", model_checks()
    )
    sensitivity = root_sensitivity(rows)
    if sensitivity:
        write_tsv(
            ROOT / "results/reference_pathway_root_sensitivity_20260909.tsv",
            sensitivity,
        )
    manifest()
    for row in summaries:
        print(
            {
                k: row[k]
                for k in (
                    "tau",
                    "n",
                    "stage",
                    "failures",
                    "mean_rho",
                    "stage_aware_rate",
                    "direct_only_rate",
                    "reference_rmse_x",
                    "reference_correlation",
                    "max_root_gap_in_scale_units",
                )
            }
        )


if __name__ == "__main__":
    main()
