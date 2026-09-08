"""One-law primary-estimand coverage check with independently integrated truth.

See docs/active_nuisance_validation_protocol_20260907.md. No permutation,
new family grid, selected seed, or coverage-dependent stopping is used.
"""

from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import norm
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.robust_extension_utils import write_tsv
from scripts.run_population_skew_influence_validation import _mixture_quantile
from src.cdelta import huber_profile_correlation_inference

SIGMA, LATENT_RHO, K, C = 0.60, 0.40, 1.4826, 1.345
ROOT_SEED = 2026090701
SIZES = (160, 640, 2560)
REPS = 2000
ZCRIT = float(norm.ppf(0.975))


def below_moment(t, power=0, mu=0.0, sigma=SIGMA):
    """E[W**power 1(W <= t)] for log W ~ N(mu,sigma**2)."""
    log_t = np.log(max(float(t), np.finfo(float).tiny))
    value = np.exp(power * mu + 0.5 * power**2 * sigma**2) * ndtr(
        (log_t - mu - power * sigma**2) / sigma
    )
    return value if t > 0 else np.zeros_like(value)


def radius_mean(t, mu=0.0, sigma=SIGMA):
    return (
        np.exp(mu + 0.5 * sigma**2)
        - t
        + 2 * (t * below_moment(t, 0, mu, sigma) - below_moment(t, 1, mu, sigma))
    )


def huber_score(t, scale, sigma=SIGMA):
    lo, hi = t - C * scale, t + C * scale
    active = below_moment(hi, sigma=sigma) - below_moment(lo, sigma=sigma)
    truncated = below_moment(hi, 1, sigma=sigma) - below_moment(lo, 1, sigma=sigma)
    return float(
        (truncated - t * active) / scale
        + C * (1 - below_moment(hi, sigma=sigma) - below_moment(lo, sigma=sigma))
    )


def marginal_fit(epsilon=0.0, point=1.0):
    cdf = lambda t: float(below_moment(t))
    m = (
        1.0
        if epsilon == 0
        else _mixture_quantile(cdf, point, epsilon, 0.5, 1e-12, 1000.0)
    )
    rcdf = lambda d: cdf(m + d) - cdf(m - d)
    d = (
        brentq(lambda d: rcdf(d) - 0.5, 0.0, 10.0, xtol=1e-14)
        if epsilon == 0
        else _mixture_quantile(rcdf, abs(point - m), epsilon, 0.5, 0.0, 1000.0)
    )
    s = K * d
    t = brentq(
        lambda t: (1 - epsilon) * huber_score(t, s)
        + epsilon * np.clip((point - t) / s, -C, C),
        1e-10,
        100.0,
        xtol=1e-14,
    )
    return float(m), float(d), float(s), float(t)


def moments(tx, ty, tol=1e-11):
    """Exact marginal moments and conditional one-dimensional integration.

    Gaussian integration is truncated at 12 SD. The tail error is negligible
    here; validate against the separate knot-split tensor calculation below.
    """
    conditional_sd = SIGMA * np.sqrt(1 - LATENT_RHO**2)

    def cross_integral(t1, t2, signed=False):
        split = np.log(t1) / SIGMA

        def integrand(z):
            x = np.exp(SIGMA * z)
            multiplier = np.sign(x - t1) if signed else abs(x - t1)
            return float(
                norm.pdf(z)
                * multiplier
                * radius_mean(t2, SIGMA * LATENT_RHO * z, conditional_sd)
            )

        return sum(
            quad(integrand, a, b, epsabs=tol, epsrel=tol)[0]
            for a, b in ((-12.0, split), (split, 12.0))
        )

    ex = np.exp(SIGMA**2 / 2)
    ex2 = np.exp(2 * SIGMA**2)
    return {
        "cross": cross_integral(tx, ty),
        "mean_x": float(radius_mean(tx)),
        "mean_y": float(radius_mean(ty)),
        "square_x": float(ex2 - 2 * tx * ex + tx**2),
        "square_y": float(ex2 - 2 * ty * ex + ty**2),
        "g_x": float(1 - 2 * below_moment(tx)),
        "g_y": float(1 - 2 * below_moment(ty)),
        "h_x": cross_integral(tx, ty, True),
        "h_y": cross_integral(ty, tx, True),
        "centered_x": float(ex - tx),
        "centered_y": float(ex - ty),
    }


def rho_gradient(m):
    vx = m["square_x"] - m["mean_x"] ** 2
    vy = m["square_y"] - m["mean_y"] ** 2
    denom = np.sqrt(vx * vy)
    rho = (m["cross"] - m["mean_x"] * m["mean_y"]) / denom
    grad = np.array(
        [
            1 / denom,
            -m["mean_y"] / denom + rho * m["mean_x"] / vx,
            -m["mean_x"] / denom + rho * m["mean_y"] / vy,
            -rho / (2 * vx),
            -rho / (2 * vy),
        ]
    )
    cx = (-m["h_x"] + m["g_x"] * m["mean_y"]) / denom + rho * (
        m["centered_x"] - m["mean_x"] * m["g_x"]
    ) / vx
    cy = (-m["h_y"] + m["mean_x"] * m["g_y"]) / denom + rho * (
        m["centered_y"] - m["mean_y"] * m["g_y"]
    ) / vy
    return float(rho), grad, float(cx), float(cy)


@lru_cache(maxsize=1)
def population():
    fit = marginal_fit()
    mom = moments(fit[3], fit[3])
    return fit, mom, rho_gradient(mom)


def location_if(x, fit):
    m, d, s, t = fit
    pdf = lambda w: 0.0 if w <= 0 else norm.pdf(np.log(w) / SIGMA) / (SIGMA * w)
    im = (0.5 - (x <= m)) / pdf(m)
    id_ = (0.5 - (np.abs(x - m) <= d) - (pdf(m + d) - pdf(m - d)) * im) / (
        pdf(m + d) + pdf(m - d)
    )
    a = float(below_moment(t + C * s) - below_moment(t - C * s))
    b = float((below_moment(t + C * s, 1) - below_moment(t - C * s, 1) - t * a) / s)
    direct = s / a * np.clip((x - t) / s, -C, C)
    return direct - b / a * K * id_, direct


def population_if(x, y):
    fit, m, (rho, grad, cx, cy) = population()
    a, b = np.abs(x - fit[3]), np.abs(y - fit[3])
    direct = (
        grad[0] * (a * b - m["cross"])
        + grad[1] * (a - m["mean_x"])
        + grad[2] * (b - m["mean_y"])
        + grad[3] * (a * a - m["square_x"])
        + grad[4] * (b * b - m["square_y"])
    )
    ix, fx = location_if(x, fit)
    iy, fy = location_if(y, fit)
    nuisance = cx * ix + cy * iy
    mad = cx * (ix - fx) + cy * (iy - fy)
    return direct, nuisance, mad


def tensor_check(order=48):
    fit, m, (rho, grad, cx, cy) = population()
    median, d, s, t = fit
    knots = [median - d, median, median + d, t - C * s, t, t + C * s]
    bounds = sorted(
        set(
            [-12.0, 12.0]
            + [
                float(np.log(v) / SIGMA)
                for v in knots
                if v > 0 and -12 < np.log(v) / SIGMA < 12
            ]
        )
    )
    nodes, weights = leggauss(order)
    z = np.concatenate(
        [(a + b) / 2 + (b - a) / 2 * nodes for a, b in zip(bounds[:-1], bounds[1:])]
    )
    w = np.concatenate([(b - a) / 2 * weights for a, b in zip(bounds[:-1], bounds[1:])])
    u, v = z[:, None], z[None, :]
    density = np.exp(
        -(u * u - 2 * LATENT_RHO * u * v + v * v) / (2 * (1 - LATENT_RHO**2))
    )
    joint = w[:, None] * w[None, :] * density / (2 * np.pi * np.sqrt(1 - LATENT_RHO**2))
    x, y = np.exp(SIGMA * u), np.exp(SIGMA * v)
    direct, nuisance, mad = population_if(x, y)
    full = direct + nuisance
    integration = lambda f: float(np.sum(joint * f))
    cross = integration(np.abs(x - t) * np.abs(y - t))
    return {
        "order_per_interval": order,
        "rho_p": rho,
        "huber_location": t,
        "mad": d,
        "location_coefficient_x": cx,
        "location_coefficient_y": cy,
        "mass_error": abs(integration(1) - 1),
        "cross_moment_error": abs(cross - m["cross"]),
        "full_if_mean": integration(full),
        "mad_if_component_mean": integration(mad),
        "full_if_variance": integration(full**2),
        "direct_if_variance": integration(direct**2),
        "nuisance_if_variance": integration(nuisance**2),
        "twice_direct_nuisance_covariance": 2 * integration(direct * nuisance),
        "mad_component_rms": np.sqrt(integration(mad**2)),
    }


def contamination_checks():
    fit, m, (rho, grad, cx, cy) = population()
    points = {
        "matched_high": (0.99, 0.99),
        "unmatched_x_high": (0.99, 0.60),
        "central_regular": (0.55, 0.45),
        "low_high": (0.01, 0.99),
    }
    rows = []
    for name, probabilities in points.items():
        x, y = np.exp(SIGMA * norm.ppf(probabilities))
        direct, nuisance, mad = population_if(x, y)
        analytic = float(direct + nuisance)
        for eps in (1e-4, 1e-5, 1e-6):
            tx, ty = marginal_fit(eps, x)[3], marginal_fit(eps, y)[3]
            mix = moments(tx, ty)
            atom = {
                "cross": abs(x - tx) * abs(y - ty),
                "mean_x": abs(x - tx),
                "mean_y": abs(y - ty),
                "square_x": (x - tx) ** 2,
                "square_y": (y - ty) ** 2,
            }
            for key, val in atom.items():
                mix[key] = (1 - eps) * mix[key] + eps * val
            fd = (rho_gradient(mix)[0] - rho) / eps
            rows.append(
                {
                    "point": name,
                    "epsilon": eps,
                    "population_rho_p": rho,
                    "analytic_influence": analytic,
                    "finite_difference": fd,
                    "scaled_error": abs(fd - analytic) / (1 + abs(analytic)),
                    "reference_component": float(nuisance),
                    "mad_component": float(mad),
                }
            )
    return rows


def mechanism_checks():
    """Population algebra only, not an added Monte Carlo scenario."""
    tau, step = 0.10, 1e-5
    signed_score = lambda t: 0.5 * (huber_score(t, K, tau) - huber_score(-t, K, tau))
    analytic = -float(ndtr(np.log(C * K) / tau)) / K
    numerical = (signed_score(step) - signed_score(-step)) / (2 * step)
    # Product law: independent bounded radii and one common symmetric sign.
    grid = np.array(
        [(s, rx, ry) for s in (-1.0, 1.0) for rx in (1.0, 2.0) for ry in (1.0, 3.0)]
    )
    sign, rx, ry = grid.T
    tx, ty = 0.2, -0.3
    corr = float(np.corrcoef(np.abs(sign * rx - tx), np.abs(sign * ry - ty))[0, 1])
    expected = tx * ty / np.sqrt((np.var(rx) + tx**2) * (np.var(ry) + ty**2))
    cancellation = float(
        max(abs(np.mean(sign)), abs(np.mean(sign * rx)), abs(np.mean(sign * ry)))
    )
    return [
        {
            "check": "signed_lognormal_huber_slope",
            "observed": numerical,
            "reference": analytic,
            "error": abs(numerical - analytic),
            "passed": int(abs(numerical - analytic) < 1e-9),
            "scope": "tau=.10; population scale fixed at K; slope is not flat",
        },
        {
            "check": "shared_sign_reference_coefficients_cancel",
            "observed": cancellation,
            "reference": 0.0,
            "error": cancellation,
            "passed": int(cancellation < 1e-14),
            "scope": "algebraic orthogonality is not exclusive to independence",
        },
        {
            "check": "imposed_offset_profile_identity",
            "observed": corr,
            "reference": expected,
            "error": abs(corr - expected),
            "passed": int(abs(corr - expected) < 1e-14),
            "scope": "fixed offsets, not a fitted-reference selection probability",
        },
        {
            "check": "binary_zero_reference_radius_variance",
            "observed": float(np.var(np.abs(sign))),
            "reference": 0.0,
            "error": 0.0,
            "passed": int(np.var(np.abs(sign)) == 0),
            "scope": "profile correlation undefined at this binary zero-reference boundary",
        },
    ]


def direct_estimate_se(x, y, tx, ty):
    a, b = np.abs(x - tx), np.abs(y - ty)
    ac, bc = a - np.mean(a), b - np.mean(b)
    vx, vy = np.mean(ac**2), np.mean(bc**2)
    rho = np.mean(ac * bc) / np.sqrt(vx * vy)
    influence = ac * bc / np.sqrt(vx * vy) - rho / 2 * (ac**2 / vx + bc**2 / vy)
    return float(rho), float(np.std(influence, ddof=1) / np.sqrt(x.size))


def wilson(count, n):
    p = count / n
    den = 1 + ZCRIT**2 / n
    center = (p + ZCRIT**2 / (2 * n)) / den
    half = ZCRIT * np.sqrt(p * (1 - p) / n + ZCRIT**2 / (4 * n * n)) / den
    return center - half, center + half


def simulate(sizes=SIZES, reps=REPS, seed=ROOT_SEED):
    truth = population()[2][0]
    t = population()[0][3]
    rows = []
    for n in sizes:
        for rep in range(reps):
            rng = np.random.default_rng(np.random.SeedSequence([seed, n, rep]))
            z = rng.standard_normal((n, 2))
            x = np.exp(SIGMA * z[:, 0])
            y = np.exp(
                SIGMA * (LATENT_RHO * z[:, 0] + np.sqrt(1 - LATENT_RHO**2) * z[:, 1])
            )
            base = {"n": n, "replication": rep, "root_seed": seed, "truth": truth}
            try:
                full = huber_profile_correlation_inference(x, y, null_value=truth)
                direct = direct_estimate_se(
                    x, y, full["reference_location_x"], full["reference_location_y"]
                )
                oracle = direct_estimate_se(x, y, t, t)
                for method, (estimate, se) in {
                    "complete_kde": (full["estimate"], full["standard_error"]),
                    "direct_only_ablation": direct,
                    "oracle_fixed_reference": oracle,
                }.items():
                    if not np.isfinite(estimate + se) or se <= 0:
                        raise ValueError("nonfinite or nonpositive inference")
                    rows.append(
                        {
                            **base,
                            "method": method,
                            "estimate": estimate,
                            "se": se,
                            "z": (estimate - truth) / se,
                            "covered": int(abs(estimate - truth) <= ZCRIT * se),
                            "coefficient_x": full["location_coefficient_x"],
                            "coefficient_y": full["location_coefficient_y"],
                            "error": "",
                        }
                    )
            except (ValueError, FloatingPointError) as error:
                # Preserve this replication as a failure for all paired methods.
                rows = [
                    r for r in rows if not (r["n"] == n and r["replication"] == rep)
                ]
                for method in (
                    "complete_kde",
                    "direct_only_ablation",
                    "oracle_fixed_reference",
                ):
                    rows.append(
                        {
                            **base,
                            "method": method,
                            "estimate": np.nan,
                            "se": np.nan,
                            "z": np.nan,
                            "covered": 0,
                            "coefficient_x": np.nan,
                            "coefficient_y": np.nan,
                            "error": str(error),
                        }
                    )
        print(f"completed n={n}, replications={reps}", flush=True)
    return rows


def summarize(rows):
    output = []
    for n in sorted({int(r["n"]) for r in rows}):
        for method in (
            "complete_kde",
            "direct_only_ablation",
            "oracle_fixed_reference",
        ):
            all_cell = [r for r in rows if int(r["n"]) == n and r["method"] == method]
            cell = [r for r in all_cell if not r["error"]]
            estimates = np.array([float(r["estimate"]) for r in cell])
            se = np.array([float(r["se"]) for r in cell])
            z = np.array([float(r["z"]) for r in cell])
            count = sum(int(r["covered"]) for r in cell)
            lo, hi = wilson(count, len(cell))
            output.append(
                {
                    "n": n,
                    "method": method,
                    "root_seed": int(all_cell[0]["root_seed"]),
                    "replications": len(all_cell),
                    "valid": len(cell),
                    "failures": len(all_cell) - len(cell),
                    "truth": float(cell[0]["truth"]),
                    "bias": float(np.mean(estimates) - float(cell[0]["truth"])),
                    "bias_mcse": float(np.std(estimates, ddof=1) / np.sqrt(len(cell))),
                    "empirical_sd": float(np.std(estimates, ddof=1)),
                    "mean_se": float(np.mean(se)),
                    "se_sd_ratio": float(np.mean(se) / np.std(estimates, ddof=1)),
                    "coverage_count": count,
                    "coverage": count / len(cell),
                    "coverage_mcse": np.sqrt(
                        (count / len(cell)) * (1 - count / len(cell)) / len(cell)
                    ),
                    "wilson_low": lo,
                    "wilson_high": hi,
                    "mean_width": float(2 * ZCRIT * np.mean(se)),
                    "z_mean": float(np.mean(z)),
                    "z_sd": float(np.std(z, ddof=1)),
                    "z_q025": float(np.quantile(z, 0.025)),
                    "z_q975": float(np.quantile(z, 0.975)),
                    "mean_coefficient_x": float(
                        np.mean([float(r["coefficient_x"]) for r in cell])
                    ),
                }
            )
    return output


def paired_differences(rows):
    output = []
    for n in sorted({int(r["n"]) for r in rows}):
        full = {
            int(r["replication"]): r
            for r in rows
            if int(r["n"]) == n and r["method"] == "complete_kde" and not r["error"]
        }
        direct = {
            int(r["replication"]): r
            for r in rows
            if int(r["n"]) == n
            and r["method"] == "direct_only_ablation"
            and not r["error"]
        }
        ids = sorted(full.keys() & direct.keys())
        diff = np.array(
            [int(full[i]["covered"]) - int(direct[i]["covered"]) for i in ids]
        )
        output.append(
            {
                "n": n,
                "paired_valid": len(ids),
                "coverage_full_minus_direct": float(diff.mean()),
                "paired_mcse": float(diff.std(ddof=1) / np.sqrt(len(ids))),
                "only_full_covers": int(np.sum(diff == 1)),
                "only_direct_covers": int(np.sum(diff == -1)),
                "maximum_estimate_difference": max(
                    abs(float(full[i]["estimate"]) - float(direct[i]["estimate"]))
                    for i in ids
                ),
            }
        )
    return output


def write_provenance(out_dir):
    """Hashes identify the checked sources and stored outputs, not a new run."""
    paths = [
        Path(__file__),
        ROOT / "src/cdelta.py",
        ROOT / "docs/active_nuisance_validation_protocol_20260907.md",
    ]
    paths += sorted(out_dir.glob("active_nuisance_*.tsv"))
    rows = []
    for path in paths:
        if path.name == "active_nuisance_manifest_20260907.tsv":
            continue
        data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        rows.append(
            {
                "path": (
                    str(path.relative_to(ROOT))
                    if path.is_relative_to(ROOT)
                    else str(path)
                ),
                "sha256_lf": hashlib.sha256(data).hexdigest(),
                "python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": scipy.__version__,
                "rng": "PCG64; SeedSequence([root,n,rep])",
                "source_base_commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
            }
        )
    write_tsv(out_dir / "active_nuisance_manifest_20260907.tsv", rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=REPS)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--numerical-only", action="store_true")
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.summarize_only:
        with (args.out_dir / "active_nuisance_replications_20260907.tsv").open(
            newline=""
        ) as f:
            rows = list(csv.DictReader(f, delimiter="\t"))
        write_tsv(
            args.out_dir / "active_nuisance_summary_20260907.tsv", summarize(rows)
        )
        write_tsv(
            args.out_dir / "active_nuisance_paired_20260907.tsv",
            paired_differences(rows),
        )
        write_provenance(args.out_dir)
        return
    checks = [tensor_check(order) for order in (24, 48, 72)]
    derivatives = contamination_checks()
    write_tsv(args.out_dir / "active_nuisance_population_20260907.tsv", checks)
    write_tsv(args.out_dir / "active_nuisance_derivative_20260907.tsv", derivatives)
    write_tsv(
        args.out_dir / "active_nuisance_mechanism_scope_20260907.tsv",
        mechanism_checks(),
    )
    print(checks[-1], flush=True)
    if not args.numerical_only:
        rows = simulate(reps=args.reps)
        write_tsv(args.out_dir / "active_nuisance_replications_20260907.tsv", rows)
        write_tsv(
            args.out_dir / "active_nuisance_summary_20260907.tsv", summarize(rows)
        )
        write_tsv(
            args.out_dir / "active_nuisance_paired_20260907.tsv",
            paired_differences(rows),
        )
        write_provenance(args.out_dir)


if __name__ == "__main__":
    main()
