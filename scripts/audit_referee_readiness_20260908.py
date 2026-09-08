"""Referee-oriented diagnostics from frozen draws; no new simulation grid.

Population-variance intervals are infeasible diagnostic counterfactuals, not
recommended intervals. Root replays use only nine already simulated samples.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.robust_extension_utils import write_tsv
from scripts.freeze_canonical_evidence_20260819 import normalized_text_sha256
from scripts.validate_active_nuisance_20260907 import (
    SIGMA,
    LATENT_RHO,
    ROOT_SEED,
    C,
    ZCRIT,
    wilson,
)
from src.cdelta import huber_profile_correlation_inference


def read(name):
    with (ROOT / "results" / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def coverage_diagnostics():
    rows = read("active_nuisance_replications_20260907.tsv")
    pop = read("active_nuisance_population_20260907.tsv")[-1]
    output = []
    for n in (160, 640, 2560):
        for method in ("complete_kde", "oracle_fixed_reference"):
            selected = [r for r in rows if int(r["n"]) == n and r["method"] == method]
            valid = [r for r in selected if not r["error"]]
            errors = np.array([float(r["estimate"]) - float(r["truth"]) for r in valid])
            fitted_se = np.array([float(r["se"]) for r in valid])
            variance_key = (
                "full_if_variance" if method == "complete_kde" else "direct_if_variance"
            )
            pop_se = np.sqrt(float(pop[variance_key]) / n)
            for scale_name, se in (
                ("reported_plugin", fitted_se),
                ("infeasible_population_asymptotic", np.full(len(valid), pop_se)),
            ):
                z = errors / se
                below = int(np.sum(z < -ZCRIT))
                above = int(np.sum(z > ZCRIT))
                count = len(valid) - below - above
                lo, hi = wilson(count, len(valid))
                lower_lo, lower_hi = wilson(below, len(valid))
                upper_lo, upper_hi = wilson(above, len(valid))
                paired_delta = (np.abs(z) <= ZCRIT).astype(int) - (
                    np.abs(errors / fitted_se) <= ZCRIT
                ).astype(int)
                u = errors / pop_se
                delta = se / pop_se - 1
                interaction = -u * delta
                remainder = u * delta**2 / (1 + delta)
                output.append(
                    {
                        "n": n,
                        "method": method,
                        "scale": scale_name,
                        "replications": len(selected),
                        "valid": len(valid),
                        "failures": len(selected) - len(valid),
                        "coverage_count": count,
                        "coverage": count / len(valid),
                        "wilson_low": lo,
                        "wilson_high": hi,
                        "mean_interval_width": float(2 * ZCRIT * np.mean(se)),
                        "coverage_difference_from_plugin": float(np.mean(paired_delta)),
                        "paired_difference_mcse": float(
                            np.std(paired_delta, ddof=1) / np.sqrt(len(valid))
                        ),
                        "identity_mean_u": float(np.mean(u)),
                        "identity_mean_minus_u_delta": float(np.mean(interaction)),
                        "identity_mean_remainder": float(np.mean(remainder)),
                        "identity_max_error": float(
                            np.max(np.abs(z - u - interaction - remainder))
                        ),
                        "below_truth_miss_count": below,
                        "below_truth_miss_rate": below / len(valid),
                        "below_truth_wilson_low": lower_lo,
                        "below_truth_wilson_high": lower_hi,
                        "above_truth_miss_count": above,
                        "above_truth_miss_rate": above / len(valid),
                        "above_truth_wilson_low": upper_lo,
                        "above_truth_wilson_high": upper_hi,
                        "population_asymptotic_se": pop_se,
                        "empirical_sd_over_population_se": float(
                            np.std(errors, ddof=1) / pop_se
                        ),
                        "error_se_correlation": float(
                            np.corrcoef(errors, fitted_se)[0, 1]
                        ),
                        "z_mean": float(np.mean(z)),
                        "z_sd": float(np.std(z, ddof=1)),
                        "z_q025": float(np.quantile(z, 0.025)),
                        "z_q975": float(np.quantile(z, 0.975)),
                        "scope": "post hoc diagnostic on frozen samples; not an interval recommendation",
                    }
                )
    return output


def root_replay():
    output = []
    for n in (160, 640, 2560):
        for rep in (0, 1, 2):
            rng = np.random.default_rng(np.random.SeedSequence([ROOT_SEED, n, rep]))
            z = rng.standard_normal((n, 2))
            x = np.exp(SIGMA * z[:, 0])
            y = np.exp(
                SIGMA * (LATENT_RHO * z[:, 0] + np.sqrt(1 - LATENT_RHO**2) * z[:, 1])
            )
            fit = huber_profile_correlation_inference(x, y)
            for label, values in (("x", x), ("y", y)):
                location = float(fit[f"reference_location_{label}"])
                scale = float(fit[f"reference_scale_{label}"])
                score = lambda t: float(np.mean(np.clip((values - t) / scale, -C, C)))
                exact = brentq(
                    score, float(values.min()), float(values.max()), xtol=1e-13
                )
                output.append(
                    {
                        "n": n,
                        "replication": rep,
                        "margin": label,
                        "root_seed": ROOT_SEED,
                        "absolute_score_residual": abs(score(location)),
                        "sqrt_n_score_residual": np.sqrt(n) * abs(score(location)),
                        "root_difference_in_scale_units": abs(location - exact) / scale,
                        "passed": int(abs(location - exact) / scale < 1e-7),
                        "scope": "18 fixed regular fits; not an arbitrary-law convergence guarantee",
                    }
                )
    return output


def write_manifest():
    paths = [
        "scripts/audit_referee_readiness_20260908.py",
        "src/cdelta.py",
        "results/active_nuisance_replications_20260907.tsv",
        "results/active_nuisance_population_20260907.tsv",
        "results/referee_coverage_diagnostics_20260908.tsv",
        "results/referee_root_replay_20260908.tsv",
    ]
    write_tsv(
        ROOT / "results/referee_diagnostics_manifest_20260908.tsv",
        [{"path": p, "sha256_lf": normalized_text_sha256(ROOT / p)} for p in paths],
    )


def main():
    diagnostics, roots = coverage_diagnostics(), root_replay()
    write_tsv(ROOT / "results/referee_coverage_diagnostics_20260908.tsv", diagnostics)
    write_tsv(ROOT / "results/referee_root_replay_20260908.tsv", roots)
    write_manifest()
    for row in diagnostics:
        print(
            {
                key: row[key]
                for key in (
                    "n",
                    "method",
                    "scale",
                    "coverage",
                    "below_truth_miss_rate",
                    "above_truth_miss_rate",
                    "error_se_correlation",
                )
            }
        )
    print(
        "max root difference:", max(r["root_difference_in_scale_units"] for r in roots)
    )
    if not all(r["passed"] for r in roots):
        raise SystemExit("root audit failed")


if __name__ == "__main__":
    main()
