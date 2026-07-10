"""Utilities for a first simulation study of c_delta.

The implementation follows the coefficient as a comparison of internal
divergence vectors. It intentionally keeps the formulas explicit so the code can
serve as a discussion artifact with a supervisor.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


Array = np.ndarray


@dataclass(frozen=True)
class CDeltaResult:
    raw: float
    normalized_pairing: float
    direction_correlation: float
    dx: Array
    dy: Array
    status: str = "ok"


def _as_1d(values: Array | list[float], name: str) -> Array:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if arr.size < 3:
        raise ValueError(f"{name} must contain at least three observations")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def _background_sample(
    rng: np.random.Generator,
    n: int,
    background: str,
) -> Array:
    if background == "normal":
        return rng.normal(size=n)
    if background == "t3":
        return rng.standard_t(df=3, size=n)
    if background == "t2":
        return rng.standard_t(df=2, size=n)
    if background == "lognormal":
        values = rng.lognormal(mean=0.0, sigma=0.8, size=n)
        return (values - float(values.mean())) / float(values.std())

    raise ValueError(f"unknown background: {background}")


def divergence_vector(values: Array | list[float], *, kind: str = "l2") -> Array:
    """Return each observation's average divergence from all others."""
    x = _as_1d(values, "values")
    diffs = x[:, None] - x[None, :]
    mask = ~np.eye(x.size, dtype=bool)

    if kind == "l2":
        squared = diffs**2
        return np.sqrt(squared[mask].reshape(x.size, x.size - 1).mean(axis=1))
    if kind == "l1":
        absolute = np.abs(diffs)
        return absolute[mask].reshape(x.size, x.size - 1).mean(axis=1)

    raise ValueError("kind must be 'l2' or 'l1'")


def c_delta(
    x: Array | list[float],
    y: Array | list[float],
    *,
    kind: str = "l2",
    zero_policy: str = "undetermined",
) -> CDeltaResult:
    """Compute raw c_delta and a sample-dependent pairing normalization.

    The normalized value uses the maximum dot product obtainable by re-pairing
    the two divergence vectors, which is a finite-sample upper anchor for the
    observed x-y pairing. This is a pragmatic simulation anchor, not a universal
    theoretical bound.
    """
    x_arr = _as_1d(x, "x")
    y_arr = _as_1d(y, "y")
    if x_arr.size != y_arr.size:
        raise ValueError("x and y must have the same length")

    dx = divergence_vector(x_arr, kind=kind)
    dy = divergence_vector(y_arr, kind=kind)
    mean_dx = float(dx.mean())
    mean_dy = float(dy.mean())

    if mean_dx == 0.0 or mean_dy == 0.0:
        message = "undetermined due to data limitations"
        if zero_policy in {"undetermined", "nan"}:
            return CDeltaResult(np.nan, np.nan, np.nan, dx, dy, message)
        raise ValueError(message)

    raw = float(np.dot(dx, dy) / (mean_dx * mean_dy))
    max_pairing = float(
        np.dot(np.sort(dx), np.sort(dy)) / (mean_dx * mean_dy)
    )
    normalized = raw / max_pairing if max_pairing > 0.0 else np.nan

    if np.std(dx) == 0.0 or np.std(dy) == 0.0:
        direction = np.nan
    else:
        direction = float(np.corrcoef(dx, dy)[0, 1])

    return CDeltaResult(raw, float(normalized), direction, dx, dy)


def permutation_test(
    x: Array | list[float],
    y: Array | list[float],
    *,
    n_perm: int = 999,
    seed: int | None = None,
    kind: str = "l2",
) -> dict[str, float]:
    """Permutation test for paired divergence-structure signal."""
    rng = np.random.default_rng(seed)
    y_arr = _as_1d(y, "y")
    observed = c_delta(x, y_arr, kind=kind).raw
    exceed = 0

    for _ in range(n_perm):
        permuted = rng.permutation(y_arr)
        stat = c_delta(x, permuted, kind=kind).raw
        exceed += stat >= observed

    p_value = (exceed + 1) / (n_perm + 1)
    return {"observed": observed, "p_value": float(p_value)}


def bootstrap_ci(
    x: Array | list[float],
    y: Array | list[float],
    *,
    n_boot: int = 1000,
    seed: int | None = None,
    alpha: float = 0.05,
    kind: str = "l2",
) -> dict[str, float]:
    """Percentile paired bootstrap interval for raw c_delta."""
    rng = np.random.default_rng(seed)
    x_arr = _as_1d(x, "x")
    y_arr = _as_1d(y, "y")
    if x_arr.size != y_arr.size:
        raise ValueError("x and y must have the same length")

    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, x_arr.size, size=x_arr.size)
        try:
            stats.append(c_delta(x_arr[idx], y_arr[idx], kind=kind).raw)
        except ValueError:
            continue

    if not stats:
        raise ValueError("all bootstrap samples had zero divergence")

    lower, upper = np.quantile(stats, [alpha / 2, 1 - alpha / 2])
    return {
        "estimate": c_delta(x_arr, y_arr, kind=kind).raw,
        "lower": float(lower),
        "upper": float(upper),
        "n_used": float(len(stats)),
    }


def make_scenario(
    name: str,
    n: int,
    *,
    seed: int | None = None,
) -> tuple[Array, Array]:
    """Generate paired samples for pilot simulations."""
    rng = np.random.default_rng(seed)

    if name == "null_normal":
        return rng.normal(size=n), rng.normal(size=n)
    if name == "aligned_normal":
        x = rng.normal(size=n)
        return x, x + rng.normal(scale=0.25, size=n)
    if name == "inverted_divergence":
        x = np.linspace(-2.0, 2.0, n) + rng.normal(scale=0.05, size=n)
        y = -np.abs(x) + rng.normal(scale=0.05, size=n)
        return x, y
    if name == "heavy_tailed":
        return rng.standard_t(df=3, size=n), rng.standard_t(df=3, size=n)
    if name == "skewed":
        return rng.lognormal(mean=0.0, sigma=0.8, size=n), rng.lognormal(
            mean=0.0, sigma=0.8, size=n
        )
    if name == "contaminated_aligned":
        x = rng.normal(size=n)
        y = x + rng.normal(scale=0.35, size=n)
        k = max(1, n // 20)
        idx = rng.choice(n, size=k, replace=False)
        x[idx] += rng.normal(loc=8.0, scale=1.0, size=k)
        y[idx] += rng.normal(loc=8.0, scale=1.0, size=k)
        return x, y
    if name == "matched_extreme":
        return make_extreme_scenario(name, n, seed=seed)[:2]
    if name == "mismatched_extreme":
        return make_extreme_scenario(name, n, seed=seed)[:2]
    if name == "x_only_extreme":
        return make_extreme_scenario(name, n, seed=seed)[:2]
    if name == "y_only_extreme":
        return make_extreme_scenario(name, n, seed=seed)[:2]

    raise ValueError(f"unknown scenario: {name}")


def make_extreme_scenario(
    name: str,
    n: int,
    *,
    seed: int | None = None,
    magnitude: float = 8.0,
    background: str = "normal",
) -> tuple[Array, Array, list[int]]:
    """Generate scenarios with retained extreme observations.

    The returned index list identifies observations used for sensitivity
    exclusion. The main statistical analysis should keep these observations.
    """
    if n < 4:
        raise ValueError("n must be at least four for extreme-value scenarios")

    rng = np.random.default_rng(seed)
    x = _background_sample(rng, n, background)
    y = _background_sample(rng, n, background)

    if name == "null_normal":
        return x, y, []
    if name == "matched_extreme":
        x[-1] = magnitude
        y[-1] = magnitude
        return x, y, [n - 1]
    if name == "mismatched_extreme":
        x[-1] = magnitude
        y[0] = magnitude
        return x, y, [0, n - 1]
    if name == "x_only_extreme":
        x[-1] = magnitude
        return x, y, [n - 1]
    if name == "y_only_extreme":
        y[-1] = magnitude
        return x, y, [n - 1]

    raise ValueError(f"unknown extreme scenario: {name}")


def _drop_indices(x: Array, y: Array, indices: list[int]) -> tuple[Array, Array]:
    if not indices:
        return x, y
    mask = np.ones(x.size, dtype=bool)
    mask[indices] = False
    return x[mask], y[mask]


def outlier_influence_summary(
    *,
    n: int = 40,
    seed: int = 123,
    n_perm: int = 499,
    background: str = "normal",
) -> list[dict[str, float | str]]:
    """Compare retained and sensitivity-excluded extreme observations.

    The main analysis keeps the extreme value. Exclusion is reported only as a
    sensitivity comparison because the extreme value may define the group's
    divergence structure.
    """
    rows = []
    scenarios = [
        "null_normal",
        "matched_extreme",
        "mismatched_extreme",
        "x_only_extreme",
        "y_only_extreme",
    ]
    for offset, scenario in enumerate(scenarios):
        x, y, extreme_indices = make_extreme_scenario(
            scenario, n, seed=seed + offset, background=background
        )
        kept = c_delta(x, y)
        kept_perm = permutation_test(
            x, y, n_perm=n_perm, seed=seed + 1000 + offset
        )
        sensitivity_x, sensitivity_y = _drop_indices(x, y, extreme_indices)
        excluded = c_delta(sensitivity_x, sensitivity_y)
        rows.append(
            {
                "scenario": scenario,
                "main_raw": round(kept.raw, 4),
                "main_norm": round(kept.normalized_pairing, 4),
                "main_corr": round(kept.direction_correlation, 4),
                "main_perm_p": round(kept_perm["p_value"], 4),
                "sensitivity_raw_without_extreme_indices": round(excluded.raw, 4),
                "raw_change": round(kept.raw - excluded.raw, 4),
            }
        )
    return rows


def repeated_outlier_simulation(
    *,
    n: int = 40,
    repetitions: int = 300,
    n_perm: int = 99,
    seed: int = 123,
    magnitude: float = 8.0,
    background: str = "normal",
    alpha: float = 0.05,
) -> list[dict[str, float | str]]:
    """Repeated simulation for matched and unmatched extreme observations."""
    scenarios = [
        "null_normal",
        "matched_extreme",
        "mismatched_extreme",
        "x_only_extreme",
        "y_only_extreme",
    ]
    accum: dict[str, list[dict[str, float]]] = {scenario: [] for scenario in scenarios}

    for rep in range(repetitions):
        for scenario_offset, scenario in enumerate(scenarios):
            scenario_seed = seed + rep * 100 + scenario_offset
            x, y, extreme_indices = make_extreme_scenario(
                scenario,
                n,
                seed=scenario_seed,
                magnitude=magnitude,
                background=background,
            )
            kept = c_delta(x, y)
            perm = permutation_test(
                x,
                y,
                n_perm=n_perm,
                seed=seed + 1_000_000 + rep * 100 + scenario_offset,
            )
            sensitivity_x, sensitivity_y = _drop_indices(x, y, extreme_indices)
            excluded = c_delta(sensitivity_x, sensitivity_y)
            accum[scenario].append(
                {
                    "raw": kept.raw,
                    "norm": kept.normalized_pairing,
                    "corr": kept.direction_correlation,
                    "p": perm["p_value"],
                    "reject": float(perm["p_value"] < alpha),
                    "raw_change": kept.raw - excluded.raw,
                }
            )

    rows = []
    for scenario in scenarios:
        values = accum[scenario]
        rows.append(
            {
                "scenario": scenario,
                "repetitions": repetitions,
                "magnitude": magnitude,
                "background": background,
                "alpha": alpha,
                "mean_raw": round(float(np.mean([v["raw"] for v in values])), 4),
                "sd_raw": round(float(np.std([v["raw"] for v in values], ddof=1)), 4),
                "mean_norm": round(float(np.mean([v["norm"] for v in values])), 4),
                "mean_corr": round(float(np.mean([v["corr"] for v in values])), 4),
                "rejection_rate": round(
                    float(np.mean([v["reject"] for v in values])), 4
                ),
                "mean_raw_change": round(
                    float(np.mean([v["raw_change"] for v in values])), 4
                ),
            }
        )
    return rows


def magnitude_grid_simulation(
    *,
    n: int = 40,
    repetitions: int = 200,
    n_perm: int = 99,
    seed: int = 123,
    magnitudes: list[float] | None = None,
    background: str = "normal",
    alpha: float = 0.05,
) -> list[dict[str, float | str]]:
    """Track when a matched extreme value begins to define structure."""
    if magnitudes is None:
        magnitudes = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]

    rows = []
    for mag_offset, magnitude in enumerate(magnitudes):
        values = []
        for rep in range(repetitions):
            x, y, extreme_indices = make_extreme_scenario(
                "matched_extreme",
                n,
                seed=seed + mag_offset * 10_000 + rep,
                magnitude=magnitude,
                background=background,
            )
            kept = c_delta(x, y)
            perm = permutation_test(
                x,
                y,
                n_perm=n_perm,
                seed=seed + 2_000_000 + mag_offset * 10_000 + rep,
            )
            sensitivity_x, sensitivity_y = _drop_indices(x, y, extreme_indices)
            excluded = c_delta(sensitivity_x, sensitivity_y)
            values.append(
                {
                    "raw": kept.raw,
                    "corr": kept.direction_correlation,
                    "reject": float(perm["p_value"] < alpha),
                    "raw_change": kept.raw - excluded.raw,
                }
            )
        rows.append(
            {
                "scenario": "matched_extreme",
                "magnitude": magnitude,
                "repetitions": repetitions,
                "background": background,
                "alpha": alpha,
                "mean_raw": round(float(np.mean([v["raw"] for v in values])), 4),
                "mean_corr": round(float(np.mean([v["corr"] for v in values])), 4),
                "rejection_rate": round(
                    float(np.mean([v["reject"] for v in values])), 4
                ),
                "mean_raw_change": round(
                    float(np.mean([v["raw_change"] for v in values])), 4
                ),
            }
        )
    return rows


def power_curve_simulation(
    *,
    sample_sizes: list[int] | None = None,
    magnitudes: list[float] | None = None,
    repetitions: int = 120,
    n_perm: int = 199,
    seed: int = 123,
    background: str = "normal",
    alpha: float = 0.05,
) -> list[dict[str, float | str]]:
    """Estimate matched-extreme power curves across n and magnitude."""
    if sample_sizes is None:
        sample_sizes = [15, 20, 40]
    if magnitudes is None:
        magnitudes = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]

    rows = []
    for n_offset, n in enumerate(sample_sizes):
        for mag_offset, magnitude in enumerate(magnitudes):
            values = []
            for rep in range(repetitions):
                row_seed = seed + n_offset * 100_000 + mag_offset * 10_000 + rep
                x, y, extreme_indices = make_extreme_scenario(
                    "matched_extreme",
                    n,
                    seed=row_seed,
                    magnitude=magnitude,
                    background=background,
                )
                kept = c_delta(x, y)
                perm = permutation_test(
                    x,
                    y,
                    n_perm=n_perm,
                    seed=seed + 3_000_000 + n_offset * 100_000 + mag_offset * 10_000 + rep,
                )
                sensitivity_x, sensitivity_y = _drop_indices(x, y, extreme_indices)
                excluded = c_delta(sensitivity_x, sensitivity_y)
                values.append(
                    {
                        "raw": kept.raw,
                        "corr": kept.direction_correlation,
                        "reject": float(perm["p_value"] < alpha),
                        "raw_change": kept.raw - excluded.raw,
                    }
                )
            rows.append(
                {
                    "n": n,
                    "magnitude": magnitude,
                    "background": background,
                    "alpha": alpha,
                    "repetitions": repetitions,
                    "mean_raw": round(float(np.mean([v["raw"] for v in values])), 4),
                    "mean_corr": round(float(np.mean([v["corr"] for v in values])), 4),
                    "rejection_rate": round(
                        float(np.mean([v["reject"] for v in values])), 4
                    ),
                    "mean_raw_change": round(
                        float(np.mean([v["raw_change"] for v in values])), 4
                    ),
                }
            )
    return rows


def background_extreme_simulation(
    *,
    backgrounds: list[str] | None = None,
    scenarios: list[str] | None = None,
    n: int = 40,
    magnitude: float = 8.0,
    repetitions: int = 120,
    n_perm: int = 199,
    seed: int = 123,
    alpha: float = 0.05,
) -> list[dict[str, float | str]]:
    """Compare extreme-value alignment under non-normal backgrounds."""
    if backgrounds is None:
        backgrounds = ["normal", "t3", "lognormal"]
    if scenarios is None:
        scenarios = [
            "null_normal",
            "matched_extreme",
            "mismatched_extreme",
            "x_only_extreme",
            "y_only_extreme",
        ]

    rows = []
    for bg_offset, background in enumerate(backgrounds):
        for scenario_offset, scenario in enumerate(scenarios):
            values = []
            for rep in range(repetitions):
                row_seed = seed + bg_offset * 100_000 + scenario_offset * 10_000 + rep
                x, y, extreme_indices = make_extreme_scenario(
                    scenario,
                    n,
                    seed=row_seed,
                    magnitude=magnitude,
                    background=background,
                )
                kept = c_delta(x, y)
                perm = permutation_test(
                    x,
                    y,
                    n_perm=n_perm,
                    seed=seed + 4_000_000 + bg_offset * 100_000 + scenario_offset * 10_000 + rep,
                )
                sensitivity_x, sensitivity_y = _drop_indices(x, y, extreme_indices)
                excluded = c_delta(sensitivity_x, sensitivity_y)
                values.append(
                    {
                        "raw": kept.raw,
                        "corr": kept.direction_correlation,
                        "reject": float(perm["p_value"] < alpha),
                        "raw_change": kept.raw - excluded.raw,
                    }
                )
            rows.append(
                {
                    "background": background,
                    "scenario": scenario,
                    "n": n,
                    "magnitude": magnitude,
                    "alpha": alpha,
                    "repetitions": repetitions,
                    "mean_raw": round(float(np.mean([v["raw"] for v in values])), 4),
                    "mean_corr": round(float(np.mean([v["corr"] for v in values])), 4),
                    "rejection_rate": round(
                        float(np.mean([v["reject"] for v in values])), 4
                    ),
                    "mean_raw_change": round(
                        float(np.mean([v["raw_change"] for v in values])), 4
                    ),
                }
            )
    return rows


def nominal_size_simulation(
    *,
    backgrounds: list[str] | None = None,
    scenarios: list[str] | None = None,
    n: int = 40,
    magnitude: float = 8.0,
    repetitions: int = 200,
    n_perm: int = 499,
    seed: int = 123,
    alphas: list[float] | None = None,
) -> list[dict[str, float | str]]:
    """Check empirical size for null and mismatched controls."""
    if backgrounds is None:
        backgrounds = ["normal", "t3", "lognormal"]
    if scenarios is None:
        scenarios = ["null_normal", "mismatched_extreme"]
    if alphas is None:
        alphas = [0.05, 0.01]

    rows = []
    for bg_offset, background in enumerate(backgrounds):
        for scenario_offset, scenario in enumerate(scenarios):
            p_values = []
            for rep in range(repetitions):
                row_seed = seed + bg_offset * 100_000 + scenario_offset * 10_000 + rep
                x, y, _ = make_extreme_scenario(
                    scenario,
                    n,
                    seed=row_seed,
                    magnitude=magnitude,
                    background=background,
                )
                perm = permutation_test(
                    x,
                    y,
                    n_perm=n_perm,
                    seed=seed + 5_000_000 + bg_offset * 100_000 + scenario_offset * 10_000 + rep,
                )
                p_values.append(perm["p_value"])
            for alpha in alphas:
                rows.append(
                    {
                        "background": background,
                        "scenario": scenario,
                        "n": n,
                        "magnitude": magnitude,
                        "alpha": alpha,
                        "repetitions": repetitions,
                        "n_perm": n_perm,
                        "empirical_size": round(
                            float(np.mean([p < alpha for p in p_values])), 4
                        ),
                        "mean_p": round(float(np.mean(p_values)), 4),
                    }
                )
    return rows


def summarize_scenarios(
    scenarios: list[str],
    *,
    n: int = 50,
    seed: int = 123,
    n_perm: int = 199,
    n_boot: int = 300,
) -> list[dict[str, float | str]]:
    """Run a compact pilot summary for several scenarios."""
    rows = []
    for offset, scenario in enumerate(scenarios):
        x, y = make_scenario(scenario, n, seed=seed + offset)
        result = c_delta(x, y)
        perm = permutation_test(x, y, n_perm=n_perm, seed=seed + 1000 + offset)
        ci = bootstrap_ci(x, y, n_boot=n_boot, seed=seed + 2000 + offset)
        rows.append(
            {
                "scenario": scenario,
                "raw": round(result.raw, 4),
                "normalized_pairing": round(result.normalized_pairing, 4),
                "direction_correlation": round(result.direction_correlation, 4),
                "perm_p": round(perm["p_value"], 4),
                "ci_lower": round(ci["lower"], 4),
                "ci_upper": round(ci["upper"], 4),
            }
        )
    return rows
