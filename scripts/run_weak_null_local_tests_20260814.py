"""Studentized local weak-null tests for profile and Mantel correlations."""

from __future__ import annotations

import argparse
from math import sqrt
from pathlib import Path
from statistics import NormalDist
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from cdelta import _huber_location_influence, huber_reference_profile
from scripts.robust_extension_utils import write_tsv
from scripts.run_robust_cdelta_grid import wilson


RESULTS_DIR = PROJECT_ROOT / "results"
NORMAL = NormalDist()


def _correlation_delta(
    mean_a: float,
    mean_b: float,
    mean_ab: float,
    mean_a2: float,
    mean_b2: float,
) -> tuple[float, np.ndarray]:
    """Correlation and gradient in moment order (ab, a, b, a2, b2)."""
    covariance = mean_ab - mean_a * mean_b
    variance_a = mean_a2 - mean_a**2
    variance_b = mean_b2 - mean_b**2
    if variance_a <= 0.0 or variance_b <= 0.0:
        raise ValueError("correlation is undetermined for a degenerate margin")
    denominator = sqrt(variance_a * variance_b)
    correlation = covariance / denominator
    gradient = np.asarray(
        (
            1.0 / denominator,
            -mean_b / denominator + correlation * mean_a / variance_a,
            -mean_a / denominator + correlation * mean_b / variance_b,
            -0.5 * correlation / variance_a,
            -0.5 * correlation / variance_b,
        )
    )
    return correlation, gradient


def _p_value(z_statistic: float, alternative: str) -> float:
    if alternative == "greater":
        return 1.0 - NORMAL.cdf(z_statistic)
    if alternative == "less":
        return NORMAL.cdf(z_statistic)
    if alternative == "two-sided":
        return 2.0 * (1.0 - NORMAL.cdf(abs(z_statistic)))
    raise ValueError("alternative must be 'greater', 'less', or 'two-sided'")


def profile_weak_null_test(
    x: np.ndarray,
    y: np.ndarray,
    *,
    null_value: float = 0.0,
    alternative: str = "two-sided",
    huber_c: float = 1.345,
    density_method: str = "kde",
    small_sample_correction: str = "sample",
) -> dict[str, float | np.ndarray]:
    """Full-IF Wald test of Corr(|X-T_X|, |Y-T_Y|) = null_value.

    Marginal MAD scaling cancels from Pearson correlation, but MAD still enters
    indirectly through each Huber location influence function.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 12:
        raise ValueError("x and y must be matching one-dimensional arrays of size >= 12")
    tx, _, location_if_x = _huber_location_influence(
        x,
        huber_c=huber_c,
        density_method=density_method,
        analytic_density=None,
        density_folds=5,
        density_seed=2026081401,
    )
    ty, _, location_if_y = _huber_location_influence(
        y,
        huber_c=huber_c,
        density_method=density_method,
        analytic_density=None,
        density_folds=5,
        density_seed=2026081402,
    )
    a = np.abs(x - tx)
    b = np.abs(y - ty)
    moments = np.asarray((np.mean(a * b), np.mean(a), np.mean(b), np.mean(a**2), np.mean(b**2)))
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    direct_moment_if = np.column_stack(
        (a * b, a, b, a**2, b**2)
    ) - moments
    direct_if = direct_moment_if @ gradient

    mean_a, mean_b = moments[1], moments[2]
    variance_a = moments[3] - mean_a**2
    variance_b = moments[4] - mean_b**2
    denominator = sqrt(variance_a * variance_b)
    sign_x = np.sign(x - tx)
    sign_y = np.sign(y - ty)
    covariance_tx = -np.mean(sign_x * b) + np.mean(sign_x) * mean_b
    covariance_ty = -np.mean(a * sign_y) + mean_a * np.mean(sign_y)
    variance_tx = -2.0 * np.mean(x - tx) + 2.0 * mean_a * np.mean(sign_x)
    variance_ty = -2.0 * np.mean(y - ty) + 2.0 * mean_b * np.mean(sign_y)
    coefficient_x = covariance_tx / denominator - 0.5 * estimate * variance_tx / variance_a
    coefficient_y = covariance_ty / denominator - 0.5 * estimate * variance_ty / variance_b
    influence = direct_if + coefficient_x * location_if_x + coefficient_y * location_if_y
    influence -= np.mean(influence)
    factors = {"hc0": 1.0, "sample": x.size / (x.size - 1.0), "hc1": x.size / (x.size - 6.0)}
    if small_sample_correction not in factors:
        raise ValueError("small_sample_correction must be hc0, sample, or hc1")
    influence_variance = float(np.mean(influence**2) * factors[small_sample_correction])
    standard_error = sqrt(influence_variance / x.size)
    if standard_error <= 0.0:
        raise ValueError("profile weak-null standard error is degenerate")
    z_statistic = (estimate - null_value) / standard_error
    return {
        "estimate": float(estimate),
        "standard_error": float(standard_error),
        "z_statistic": float(z_statistic),
        "p_value": float(_p_value(z_statistic, alternative)),
        "influence_variance": influence_variance,
        "location_coefficient_x": float(coefficient_x),
        "location_coefficient_y": float(coefficient_y),
        "influence": influence,
    }


def profile_jackknife_test(
    x: np.ndarray,
    y: np.ndarray,
    *,
    null_value: float = 0.0,
    alternative: str = "two-sided",
) -> dict[str, float | np.ndarray]:
    """Full-refit delete-one studentization of the Huber-profile correlation."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 12:
        raise ValueError("x and y must be matching one-dimensional arrays of size >= 12")
    estimate = float(
        np.corrcoef(huber_reference_profile(x), huber_reference_profile(y))[0, 1]
    )
    leave_one_out = np.empty(x.size)
    keep = np.ones(x.size, dtype=bool)
    for index in range(x.size):
        keep[index] = False
        leave_one_out[index] = np.corrcoef(
            huber_reference_profile(x[keep]), huber_reference_profile(y[keep])
        )[0, 1]
        keep[index] = True
    standard_error = sqrt(
        (x.size - 1.0) / x.size
        * float(np.sum((leave_one_out - np.mean(leave_one_out)) ** 2))
    )
    z_statistic = (estimate - null_value) / standard_error
    return {
        "estimate": estimate,
        "standard_error": standard_error,
        "z_statistic": float(z_statistic),
        "p_value": float(_p_value(z_statistic, alternative)),
        "leave_one_out": leave_one_out,
    }


def mantel_weak_null_test(
    x: np.ndarray,
    y: np.ndarray,
    *,
    null_value: float = 0.0,
    alternative: str = "two-sided",
    small_sample_correction: str = "sample",
) -> dict[str, float | np.ndarray]:
    """Hájek-projection Wald test for the distance-correlation U-functional."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 12:
        raise ValueError("x and y must be matching one-dimensional arrays of size >= 12")
    upper = np.triu_indices(x.size, 1)
    dx_matrix = np.abs(x[:, None] - x[None, :])
    dy_matrix = np.abs(y[:, None] - y[None, :])
    a = dx_matrix[upper]
    b = dy_matrix[upper]
    kernels = np.column_stack((a * b, a, b, a**2, b**2))
    moments = np.mean(kernels, axis=0)
    estimate, gradient = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    conditional = np.column_stack(
        (
            np.sum(dx_matrix * dy_matrix, axis=1),
            np.sum(dx_matrix, axis=1),
            np.sum(dy_matrix, axis=1),
            np.sum(dx_matrix**2, axis=1),
            np.sum(dy_matrix**2, axis=1),
        )
    ) / (x.size - 1.0)
    # For an order-two U-statistic, IF(z) = 2{E[h(z,Z')] - theta}.
    moment_influence = 2.0 * (conditional - moments)
    influence = moment_influence @ gradient
    influence -= np.mean(influence)
    factors = {"hc0": 1.0, "sample": x.size / (x.size - 1.0), "hc1": x.size / (x.size - 5.0)}
    if small_sample_correction not in factors:
        raise ValueError("small_sample_correction must be hc0, sample, or hc1")
    influence_variance = float(np.mean(influence**2) * factors[small_sample_correction])
    standard_error = sqrt(influence_variance / x.size)
    if standard_error <= 0.0:
        raise ValueError("Mantel weak-null standard error is degenerate")
    z_statistic = (estimate - null_value) / standard_error
    return {
        "estimate": float(estimate),
        "standard_error": float(standard_error),
        "z_statistic": float(z_statistic),
        "p_value": float(_p_value(z_statistic, alternative)),
        "influence_variance": influence_variance,
        "influence": influence,
    }


def mantel_jackknife_test(
    x: np.ndarray,
    y: np.ndarray,
    *,
    null_value: float = 0.0,
    alternative: str = "two-sided",
) -> dict[str, float | np.ndarray]:
    """Delete-one-node studentization of the Mantel U-functional."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 12:
        raise ValueError("x and y must be matching one-dimensional arrays of size >= 12")
    dx = np.abs(x[:, None] - x[None, :])
    dy = np.abs(y[:, None] - y[None, :])
    kernel_matrices = np.stack((dx * dy, dx, dy, dx**2, dy**2), axis=2)
    total = np.sum(kernel_matrices, axis=(0, 1)) / 2.0
    denominator = x.size * (x.size - 1.0) / 2.0
    moments = total / denominator
    estimate, _ = _correlation_delta(
        moments[1], moments[2], moments[0], moments[3], moments[4]
    )
    removed = np.sum(kernel_matrices, axis=1)
    loo_denominator = (x.size - 1.0) * (x.size - 2.0) / 2.0
    leave_one_out = np.empty(x.size)
    for index in range(x.size):
        loo = (total - removed[index]) / loo_denominator
        leave_one_out[index], _ = _correlation_delta(
            loo[1], loo[2], loo[0], loo[3], loo[4]
        )
    standard_error = sqrt(
        (x.size - 1.0) / x.size
        * float(np.sum((leave_one_out - np.mean(leave_one_out)) ** 2))
    )
    z_statistic = (estimate - null_value) / standard_error
    return {
        "estimate": float(estimate),
        "standard_error": standard_error,
        "z_statistic": float(z_statistic),
        "p_value": float(_p_value(z_statistic, alternative)),
        "leave_one_out": leave_one_out,
    }


def holm_adjust(p_profile: float, p_mantel: float) -> tuple[float, float]:
    """Two-hypothesis Holm/closed-Bonferroni adjusted p-values."""
    p = np.asarray((p_profile, p_mantel))
    order = np.argsort(p)
    adjusted = np.empty(2)
    adjusted[order[0]] = min(1.0, 2.0 * p[order[0]])
    adjusted[order[1]] = max(adjusted[order[0]], p[order[1]])
    return float(adjusted[0]), float(adjusted[1])


def calibrate_mantel_partial_mixture(*, seed: int, draws: int = 500_000) -> dict[str, float]:
    """Calibrate an iid weak Mantel null with a nonzero profile correlation."""
    rng = np.random.default_rng(seed)
    x1 = rng.uniform(-1.0, 1.0, draws)
    x2 = rng.uniform(-1.0, 1.0, draws)
    u1 = rng.uniform(size=draws)
    u2 = rng.uniform(size=draws)
    eps1 = 0.02 * rng.normal(size=draws)
    eps2 = 0.02 * rng.normal(size=draws)

    def effect(aligned_probability: float) -> float:
        y1 = np.where(u1 < aligned_probability, x1, 1.0 / (0.1 + np.abs(x1))) + eps1
        y2 = np.where(u2 < aligned_probability, x2, 1.0 / (0.1 + np.abs(x2))) + eps2
        return float(np.corrcoef(np.abs(x1 - x2), np.abs(y1 - y2))[0, 1])

    lower, upper = 0.55, 0.75
    if not effect(lower) < 0.0 < effect(upper):
        raise RuntimeError("Mantel weak-null calibration does not bracket zero")
    for _ in range(20):
        middle = (lower + upper) / 2.0
        if effect(middle) < 0.0:
            lower = middle
        else:
            upper = middle
    probability = (lower + upper) / 2.0
    check_rng = np.random.default_rng(seed + 1)
    x = check_rng.uniform(-1.0, 1.0, min(draws, 100_000))
    choose = check_rng.uniform(size=x.size) < probability
    y = np.where(choose, x, 1.0 / (0.1 + np.abs(x))) + 0.02 * check_rng.normal(size=x.size)
    profile = profile_weak_null_test(x[:20_000], y[:20_000], density_method="kde")
    return {
        "aligned_probability": probability,
        "mean_mantel_effect": effect(probability),
        "profile_effect_check": float(profile["estimate"]),
        "calibration_draws": draws,
    }


def generate_scenario(
    rng: np.random.Generator, scenario: str, n: int, aligned_probability: float
) -> tuple[np.ndarray, np.ndarray]:
    if scenario in {"global_null_profile_margins", "profile_null_mantel_alt"}:
        sign_x = rng.choice((-1.0, 1.0), size=n)
        sign_y = sign_x if scenario == "profile_null_mantel_alt" else rng.choice((-1.0, 1.0), size=n)
        x = sign_x * np.exp(0.65 * rng.normal(size=n))
        y = sign_y * np.exp(0.65 * rng.normal(size=n))
        return x, y
    if scenario in {"global_null_mantel_margins", "mantel_null_profile_alt"}:
        x = rng.uniform(-1.0, 1.0, n)
        latent = x if scenario == "mantel_null_profile_alt" else rng.uniform(-1.0, 1.0, n)
        choose = rng.uniform(size=n) < aligned_probability
        y = np.where(choose, latent, 1.0 / (0.1 + np.abs(latent)))
        y += 0.02 * rng.normal(size=n)
        return x, y
    if scenario == "both_positive_alt":
        z = rng.normal(size=n)
        x = rng.choice((-1.0, 1.0), size=n) * np.exp(0.65 * z)
        y = np.sign(x) * np.exp(0.65 * (0.55 * z + sqrt(1.0 - 0.55**2) * rng.normal(size=n)))
        return x, y
    raise ValueError(f"unknown scenario: {scenario}")


def run_validation(
    *, repetitions: int, sample_sizes: tuple[int, ...], seed: int, phase: str
) -> tuple[list[dict[str, float | int | str]], dict[str, float]]:
    calibration = calibrate_mantel_partial_mixture(
        seed=seed + 100, draws=500_000 if phase == "confirmatory" else 100_000
    )
    aligned_probability = calibration["aligned_probability"]
    rng = np.random.default_rng(seed)
    rows = []
    scenarios = (
        "global_null_profile_margins",
        "profile_null_mantel_alt",
        "global_null_mantel_margins",
        "mantel_null_profile_alt",
        "both_positive_alt",
    )
    for n in sample_sizes:
        for scenario in scenarios:
            records = []
            for _ in range(repetitions):
                x, y = generate_scenario(rng, scenario, n, aligned_probability)
                profile = profile_weak_null_test(x, y)
                mantel = mantel_weak_null_test(x, y)
                profile_jackknife = profile_jackknife_test(x, y)
                mantel_jackknife = mantel_jackknife_test(x, y)
                adjusted_profile, adjusted_mantel = holm_adjust(
                    float(profile_jackknife["p_value"]),
                    float(mantel_jackknife["p_value"]),
                )
                records.append(
                    (
                        float(profile["estimate"]), float(profile["z_statistic"]), float(profile["p_value"]),
                        float(mantel["estimate"]), float(mantel["z_statistic"]), float(mantel["p_value"]),
                        float(profile_jackknife["z_statistic"]), float(profile_jackknife["p_value"]),
                        float(mantel_jackknife["z_statistic"]), float(mantel_jackknife["p_value"]),
                        adjusted_profile, adjusted_mantel,
                    )
                )
            values = np.asarray(records)
            profile_true = scenario in {"global_null_profile_margins", "profile_null_mantel_alt", "global_null_mantel_margins"}
            mantel_true = scenario in {"global_null_profile_margins", "global_null_mantel_margins", "mantel_null_profile_alt"}
            any_true_raw = np.zeros(repetitions, dtype=bool)
            any_true_holm = np.zeros(repetitions, dtype=bool)
            if profile_true:
                any_true_raw |= values[:, 7] <= 0.05
                any_true_holm |= values[:, 10] <= 0.05
            if mantel_true:
                any_true_raw |= values[:, 9] <= 0.05
                any_true_holm |= values[:, 11] <= 0.05
            holm_count = int(np.sum(any_true_holm))
            holm_interval = wilson(holm_count, repetitions)
            rows.append(
                {
                    "phase": phase,
                    "scenario": scenario,
                    "n": n,
                    "repetitions": repetitions,
                    "mean_profile_effect": float(np.mean(values[:, 0])),
                    "mean_profile_z": float(np.mean(values[:, 1])),
                    "sd_profile_z": float(np.std(values[:, 1], ddof=1)),
                    "profile_sandwich_rejection": float(np.mean(values[:, 2] <= 0.05)),
                    "mean_profile_jackknife_z": float(np.mean(values[:, 6])),
                    "sd_profile_jackknife_z": float(np.std(values[:, 6], ddof=1)),
                    "profile_jackknife_rejection": float(np.mean(values[:, 7] <= 0.05)),
                    "holm_profile_rejection": float(np.mean(values[:, 10] <= 0.05)),
                    "mean_mantel_effect": float(np.mean(values[:, 3])),
                    "mean_mantel_z": float(np.mean(values[:, 4])),
                    "sd_mantel_z": float(np.std(values[:, 4], ddof=1)),
                    "mantel_sandwich_rejection": float(np.mean(values[:, 5] <= 0.05)),
                    "mean_mantel_jackknife_z": float(np.mean(values[:, 8])),
                    "sd_mantel_jackknife_z": float(np.std(values[:, 8], ddof=1)),
                    "mantel_jackknife_rejection": float(np.mean(values[:, 9] <= 0.05)),
                    "holm_mantel_rejection": float(np.mean(values[:, 11] <= 0.05)),
                    "raw_true_null_fwer": float(np.mean(any_true_raw)),
                    "holm_true_null_fwer": holm_count / repetitions,
                    "holm_fwer_wilson_low": holm_interval[0],
                    "holm_fwer_wilson_high": holm_interval[1],
                    "both_holm_rejection": float(np.mean((values[:, 10] <= 0.05) & (values[:, 11] <= 0.05))),
                }
            )
    return rows, calibration


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pilot", "confirmatory"), default="pilot")
    args = parser.parse_args()
    settings = (
        dict(repetitions=200, sample_sizes=(80,), seed=2026081401)
        if args.phase == "pilot"
        else dict(repetitions=1_000, sample_sizes=(80, 160), seed=2026081402)
    )
    rows, calibration = run_validation(phase=args.phase, **settings)
    RESULTS_DIR.mkdir(exist_ok=True)
    write_tsv(RESULTS_DIR / f"weak_null_local_tests_{args.phase}_20260814.tsv", rows)
    write_tsv(RESULTS_DIR / f"weak_null_local_calibration_{args.phase}_20260814.tsv", [{"phase": args.phase, **calibration}])
    for row in rows:
        print(row)
    print({"calibration": calibration})


if __name__ == "__main__":
    main()
