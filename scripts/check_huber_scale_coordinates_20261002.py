"""Deterministic raw-MAD versus scaled-MAD Huber derivative check.

Uses closed-form lognormal truncated moments and newly written score equations.
Does not import a production IF, generate Monte Carlo samples, or alter frozen
results. Agreement corroborates the coordinate algebra, not proof validity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import norm


def check():
    sigma, k, c = .6, 1.4826, 1.345

    def cdf(x):
        return float(ndtr(math.log(x) / sigma)) if x > 0 else 0.

    def truncated_mean(x):
        return (float(math.exp(.5 * sigma**2) * ndtr((math.log(x) - sigma**2) / sigma))
                if x > 0 else 0.)

    def density(x):
        return float(norm.pdf(math.log(x) / sigma) / (sigma * x)) if x > 0 else 0.

    def score(location, raw_mad):
        scale = k * raw_mad
        low, high = location - c * scale, location + c * scale
        active_probability = cdf(high) - cdf(low)
        active_first_moment = truncated_mean(high) - truncated_mean(low)
        return ((active_first_moment - location * active_probability) / scale
                + c * (1 - cdf(high) - cdf(low)))

    def clipped(u):
        return max(-c, min(c, u))

    median = 1.
    raw_mad = brentq(lambda d: cdf(median + d) - cdf(median - d) - .5,
                     0., 2., xtol=1e-14)
    location = brentq(lambda t: score(t, raw_mad), .01, 10., xtol=1e-14)
    scale = k * raw_mad
    active_probability = cdf(location + c * scale) - cdf(location - c * scale)
    active_score_mean = ((truncated_mean(location + c * scale)
                          - truncated_mean(location - c * scale)
                          - location * active_probability) / scale)
    step = 1e-6
    derivative_d = -active_score_mean / raw_mad
    derivative_t = -active_probability / scale
    finite_d = (score(location, raw_mad + step) - score(location, raw_mad - step)) / (2 * step)
    finite_t = (score(location + step, raw_mad) - score(location - step, raw_mad)) / (2 * step)
    wrong_d = -active_score_mean / scale
    if not (abs(active_score_mean) > .1 and abs(derivative_d - finite_d) < 1e-7
            and abs(derivative_t - finite_t) < 1e-7 and abs(wrong_d - finite_d) > .1):
        raise AssertionError("Coordinate derivative check failed")

    epsilon = 1e-7
    records = []
    for point in (.3, .8, 1.3, 3.):
        median_if = (.5 - (point <= median)) / density(median)
        mad_if = ((.5 - (abs(point - median) <= raw_mad)
                   - (density(median + raw_mad) - density(median - raw_mad)) * median_if)
                  / (density(median + raw_mad) + density(median - raw_mad)))
        direct = scale / active_probability * clipped((point - location) / scale)
        with_k = direct - k * active_score_mean / active_probability * mad_if
        without_k = direct - active_score_mean / active_probability * mad_if
        perturbed_median = brentq(
            lambda m: (1 - epsilon) * cdf(m) + epsilon * (point <= m) - .5,
            .01, 5., xtol=1e-14)
        perturbed_mad = brentq(
            lambda d: ((1 - epsilon) * (cdf(perturbed_median + d) - cdf(perturbed_median - d))
                       + epsilon * (abs(point - perturbed_median) <= d) - .5),
            0., 5., xtol=1e-14)
        perturbed_location = brentq(
            lambda t: (1 - epsilon) * score(t, perturbed_mad)
                      + epsilon * clipped((point - t) / (k * perturbed_mad)),
            .01, 10., xtol=1e-14)
        finite_difference = (perturbed_location - location) / epsilon
        correct_error = abs(finite_difference - with_k)
        missing_k_error = abs(finite_difference - without_k)
        if not (correct_error < 5e-6 and missing_k_error > .01):
            raise AssertionError(f"Contamination coordinate check failed at {point}")
        records.append({
            "point": point, "epsilon": epsilon, "median_if": median_if, "raw_mad_if": mad_if,
            "if_with_k": with_k, "if_without_k": without_k,
            "contamination_finite_difference": finite_difference,
            "correct_absolute_error": correct_error, "missing_k_absolute_error": missing_k_error,
        })

    return {
        "all_passed": True, "new_simulation_cells": 0,
        "law": "log W ~ Normal(0, 0.6^2), the existing September 7 marginal",
        "parameters": {"sigma": sigma, "k": k, "c": c},
        "population": {"median": median, "raw_mad": raw_mad, "scale": scale,
                       "huber_location": location, "A": active_probability, "B": active_score_mean},
        "score_derivatives": {"step": step, "raw_d_analytic": derivative_d,
                              "raw_d_central_difference": finite_d,
                              "T_analytic": derivative_t, "T_central_difference": finite_t,
                              "wrong_raw_d_derivative_if_treated_as_s": wrong_d},
        "contamination_directions": records,
        "max_correct_if_error": max(r["correct_absolute_error"] for r in records),
        "min_missing_k_if_error": min(r["missing_k_absolute_error"] for r in records),
        "coordinate_identities": {
            "raw_mad_d": "IF_T = (s/A) psi - (k B/A) IF_d",
            "scaled_mad_s": "IF_T = (s/A) psi - (B/A) IF_s; IF_s = k IF_d",
            "J0_huber_row": ["0", "-B/d", "-A/(k*d)"],
            "standardized_J_huber_row": ["0", "-B", "-A/k"],
        },
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
                        "isolated_venv": sys.prefix != sys.base_prefix,
                        "note": "Recorded runtime only; no new dependency-isolated reproduction is claimed."},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Deterministic numerical differentiation and an explicit no-k negative comparator. Not simulation, independent mathematical peer review, or a proof of regular inference.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise FileExistsError("Use a fresh report path; prior evidence is not overwritten")
    report = check()
    with args.report.open("x") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({key: report[key] for key in
                     ("all_passed", "new_simulation_cells", "max_correct_if_error", "min_missing_k_if_error")},
                     indent=2))
