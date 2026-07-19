from pathlib import Path
import csv
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from cdelta import _wilson_interval, c_delta, divergence_vector


RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"


def write_tsv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def background_sample(rng: np.random.Generator, n: int, df_label: str) -> np.ndarray:
    if df_label == "normal":
        return rng.normal(size=n)
    df = float(df_label[1:])
    return rng.standard_t(df=df, size=n)


def make_tail_scenario(
    *,
    n: int,
    k: int,
    magnitude: float,
    df_label: str,
    scenario: str,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    rng = np.random.default_rng(seed)
    x = background_sample(rng, n, df_label)
    y = background_sample(rng, n, df_label)
    x_idx = np.arange(n - k, n)
    if scenario == "matched":
        y_idx = x_idx
    elif scenario == "independent_null":
        y_idx = np.sort(rng.choice(n, size=k, replace=False))
    else:
        raise ValueError(f"unknown scenario: {scenario}")
    x[x_idx] = magnitude
    y[y_idx] = magnitude
    overlap = len(set(x_idx.tolist()).intersection(y_idx.tolist()))
    return x, y, overlap


def fast_permutation_p_value(
    dx: np.ndarray,
    dy: np.ndarray,
    observed: float,
    *,
    n_perm: int,
    seed: int,
) -> float:
    rng = np.random.default_rng(seed)
    n = dx.size
    order = np.argsort(rng.random((n_perm, n)), axis=1)
    mean_dx = float(dx.mean())
    mean_dy = float(dy.mean())
    stats = np.mean(dx[None, :] * dy[order], axis=1) / (mean_dx * mean_dy)
    return float((np.sum(stats >= observed) + 1) / (n_perm + 1))


def p_value_summary(p_values: list[float]) -> dict[str, float]:
    arr = np.asarray(p_values, dtype=float)
    return {
        "mean_p": round(float(arr.mean()), 4),
        "p05": round(float(np.quantile(arr, 0.05)), 4),
        "p50": round(float(np.quantile(arr, 0.50)), 4),
        "p95": round(float(np.quantile(arr, 0.95)), 4),
    }


def run_tail_factor_grid() -> list[dict]:
    rows = []
    df_labels = ["normal", "t10", "t8", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    n_values = [40, 80, 160]
    k_values = [1, 2, 3]
    magnitudes = [4.0, 6.0, 8.0]
    kinds = ["l2", "l1"]
    scenarios = ["matched", "independent_null"]
    repetitions = 120
    n_perm = 299
    alpha = 0.05

    for kind_offset, kind in enumerate(kinds):
        for df_offset, df_label in enumerate(df_labels):
            for n_offset, n in enumerate(n_values):
                for k_offset, k in enumerate(k_values):
                    for mag_offset, magnitude in enumerate(magnitudes):
                        for scenario_offset, scenario in enumerate(scenarios):
                            p_values = []
                            norm_values = []
                            corr_values = []
                            overlaps = []
                            for rep in range(repetitions):
                                seed = (
                                    20260719
                                    + kind_offset * 100_000_000
                                    + df_offset * 10_000_000
                                    + n_offset * 1_000_000
                                    + k_offset * 100_000
                                    + mag_offset * 10_000
                                    + scenario_offset * 1_000
                                    + rep
                                )
                                x, y, overlap = make_tail_scenario(
                                    n=n,
                                    k=k,
                                    magnitude=magnitude,
                                    df_label=df_label,
                                    scenario=scenario,
                                    seed=seed,
                                )
                                result = c_delta(x, y, kind=kind)
                                p_value = fast_permutation_p_value(
                                    result.dx,
                                    result.dy,
                                    result.raw,
                                    n_perm=n_perm,
                                    seed=seed + 50_000_000,
                                )
                                p_values.append(p_value)
                                norm_values.append(result.normalized_pairing)
                                corr_values.append(result.direction_correlation)
                                overlaps.append(overlap)

                            reject_count = int(sum(p < alpha for p in p_values))
                            lo, hi = _wilson_interval(reject_count, repetitions)
                            rows.append(
                                {
                                    "kind": kind,
                                    "df_label": df_label,
                                    "n": n,
                                    "k_extremes": k,
                                    "magnitude": magnitude,
                                    "scenario": scenario,
                                    "alpha": alpha,
                                    "repetitions": repetitions,
                                    "n_perm": n_perm,
                                    "reject_count": reject_count,
                                    "rejection_rate": round(reject_count / repetitions, 4),
                                    "wilson_low": round(float(lo), 4),
                                    "wilson_high": round(float(hi), 4),
                                    "mean_norm": round(float(np.mean(norm_values)), 4),
                                    "mean_corr": round(float(np.mean(corr_values)), 4),
                                    "mean_index_overlap": round(float(np.mean(overlaps)), 4),
                                    **p_value_summary(p_values),
                                }
                            )
    return rows


def run_background_noise_grid() -> list[dict]:
    rows = []
    df_labels = ["normal", "t10", "t8", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    repetitions = 600
    n = 80
    for kind in ["l2", "l1"]:
        for df_offset, df_label in enumerate(df_labels):
            means = []
            cvs = []
            q95s = []
            maxes = []
            for rep in range(repetitions):
                rng = np.random.default_rng(20260719 + df_offset * 10_000 + rep)
                x = background_sample(rng, n, df_label)
                dx = divergence_vector(x, kind=kind)
                means.append(float(dx.mean()))
                cvs.append(float(dx.std() / dx.mean()))
                q95s.append(float(np.quantile(dx, 0.95)))
                maxes.append(float(dx.max()))
            rows.append(
                {
                    "kind": kind,
                    "df_label": df_label,
                    "n": n,
                    "repetitions": repetitions,
                    "mean_divergence": round(float(np.mean(means)), 4),
                    "mean_divergence_cv": round(float(np.mean(cvs)), 4),
                    "mean_q95_divergence": round(float(np.mean(q95s)), 4),
                    "mean_max_divergence": round(float(np.mean(maxes)), 4),
                    "q95_to_mean_ratio": round(float(np.mean(q95s) / np.mean(means)), 4),
                    "max_to_mean_ratio": round(float(np.mean(maxes) / np.mean(means)), 4),
                }
            )
    return rows


def run_tail_null_validation() -> list[dict]:
    """Higher-replication null validation for the central tail-gradient slice."""
    rows = []
    df_labels = ["normal", "t10", "t8", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    repetitions = 800
    n_perm = 499
    alpha = 0.05
    n = 80
    k = 2
    magnitude = 8.0

    for kind_offset, kind in enumerate(["l2", "l1"]):
        for df_offset, df_label in enumerate(df_labels):
            p_values = []
            overlaps = []
            corr_values = []
            norm_values = []
            for rep in range(repetitions):
                seed = 20260719 + kind_offset * 10_000_000 + df_offset * 100_000 + rep
                x, y, overlap = make_tail_scenario(
                    n=n,
                    k=k,
                    magnitude=magnitude,
                    df_label=df_label,
                    scenario="independent_null",
                    seed=seed,
                )
                result = c_delta(x, y, kind=kind)
                p_value = fast_permutation_p_value(
                    result.dx,
                    result.dy,
                    result.raw,
                    n_perm=n_perm,
                    seed=seed + 50_000_000,
                )
                p_values.append(p_value)
                overlaps.append(overlap)
                corr_values.append(result.direction_correlation)
                norm_values.append(result.normalized_pairing)

            reject_count = int(sum(p < alpha for p in p_values))
            lo, hi = _wilson_interval(reject_count, repetitions)
            rows.append(
                {
                    "kind": kind,
                    "df_label": df_label,
                    "n": n,
                    "k_extremes": k,
                    "magnitude": magnitude,
                    "scenario": "independent_null",
                    "alpha": alpha,
                    "repetitions": repetitions,
                    "n_perm": n_perm,
                    "reject_count": reject_count,
                    "rejection_rate": round(reject_count / repetitions, 4),
                    "wilson_low": round(float(lo), 4),
                    "wilson_high": round(float(hi), 4),
                    "mean_norm": round(float(np.mean(norm_values)), 4),
                    "mean_corr": round(float(np.mean(corr_values)), 4),
                    "mean_index_overlap": round(float(np.mean(overlaps)), 4),
                    **p_value_summary(p_values),
                }
            )
    return rows


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def ymap(value: float, top: int, bottom: int) -> float:
    return bottom - max(0.0, min(1.0, value)) * (bottom - top)


def draw_axes(draw, left, top, right, bottom, title, xlabel, ylabel):
    draw.text((left, 22), title, fill="black", font=font(30, True))
    draw.line((left, bottom, right, bottom), fill="black", width=2)
    draw.line((left, top, left, bottom), fill="black", width=2)
    draw.text(((left + right) // 2 - 120, bottom + 62), xlabel, fill="black", font=font(22))
    draw.text((14, top + 180), ylabel, fill="black", font=font(22))
    for value in [0, 0.25, 0.5, 0.75, 1.0]:
        y = ymap(value, top, bottom)
        draw.line((left - 8, y, left, y), fill="black", width=2)
        draw.text((left - 64, y - 11), f"{value:.2f}", fill="black", font=font(18))
        draw.line((left, y, right, y), fill=(226, 226, 226), width=1)


def make_figures(grid_rows: list[dict], noise_rows: list[dict]) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    labels = ["normal", "t10", "t8", "t5", "t4", "t3", "t2.5", "t2.2", "t2"]
    x_positions = {label: idx for idx, label in enumerate(labels)}
    colors = {
        4.0: (65, 105, 180),
        6.0: (220, 130, 45),
        8.0: (80, 150, 90),
    }

    for kind in ["l2", "l1"]:
        img = Image.new("RGB", (1600, 920), "white")
        draw = ImageDraw.Draw(img)
        left, top, right, bottom = 120, 100, 1500, 700
        draw_axes(
            draw,
            left,
            top,
            right,
            bottom,
            f"Matched power over tail heaviness ({kind}, n=80, k=2)",
            "tail setting",
            "rejection rate",
        )
        step = (right - left) / (len(labels) - 1)
        for idx, label in enumerate(labels):
            x = left + idx * step
            draw.line((x, bottom, x, bottom + 8), fill="black", width=2)
            draw.text((x - 28, bottom + 18), label, fill="black", font=font(16))
        for magnitude in [4.0, 6.0, 8.0]:
            subset = [
                r for r in grid_rows
                if r["kind"] == kind
                and r["scenario"] == "matched"
                and int(r["n"]) == 80
                and int(r["k_extremes"]) == 2
                and float(r["magnitude"]) == magnitude
            ]
            subset = sorted(subset, key=lambda r: x_positions[r["df_label"]])
            points = [
                (
                    left + x_positions[r["df_label"]] * step,
                    ymap(float(r["rejection_rate"]), top, bottom),
                )
                for r in subset
            ]
            for p0, p1 in zip(points, points[1:]):
                draw.line((*p0, *p1), fill=colors[magnitude], width=4)
            for x, y in points:
                draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=colors[magnitude])
            lx, ly = right - 175, top + 32 + [4.0, 6.0, 8.0].index(magnitude) * 34
            draw.line((lx, ly, lx + 34, ly), fill=colors[magnitude], width=4)
            draw.text((lx + 45, ly - 12), f"mag={magnitude:g}", fill="black", font=font(18))
        img.save(FIGURES_DIR / f"tail_df_power_n80_k2_{kind}_20260719.png")

    img = Image.new("RGB", (1600, 920), "white")
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = 120, 100, 1500, 700
    draw_axes(
        draw,
        left,
        top,
        right,
        bottom,
        "Independent-null size across tail heaviness (n=80, k=2, mag=8)",
        "tail setting",
        "rejection rate",
    )
    alpha_y = ymap(0.05, top, bottom)
    for x0 in range(left, right, 24):
        draw.line((x0, alpha_y, min(x0 + 12, right), alpha_y), fill=(180, 0, 0), width=2)
    step = (right - left) / (len(labels) - 1)
    kind_colors = {"l2": (65, 105, 180), "l1": (220, 130, 45)}
    for idx, label in enumerate(labels):
        x = left + idx * step
        draw.line((x, bottom, x, bottom + 8), fill="black", width=2)
        draw.text((x - 28, bottom + 18), label, fill="black", font=font(16))
    for kind in ["l2", "l1"]:
        subset = [
            r for r in grid_rows
            if r["kind"] == kind
            and r["scenario"] == "independent_null"
            and int(r["n"]) == 80
            and int(r["k_extremes"]) == 2
            and float(r["magnitude"]) == 8.0
        ]
        subset = sorted(subset, key=lambda r: x_positions[r["df_label"]])
        points = [
            (
                left + x_positions[r["df_label"]] * step,
                ymap(float(r["rejection_rate"]), top, bottom),
            )
            for r in subset
        ]
        for p0, p1 in zip(points, points[1:]):
            draw.line((*p0, *p1), fill=kind_colors[kind], width=4)
        for x, y in points:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=kind_colors[kind])
        lx, ly = right - 150, top + 32 + ["l2", "l1"].index(kind) * 34
        draw.line((lx, ly, lx + 34, ly), fill=kind_colors[kind], width=4)
        draw.text((lx + 45, ly - 12), kind, fill="black", font=font(18))
    img.save(FIGURES_DIR / "tail_df_null_size_n80_k2_mag8_20260719.png")

    img = Image.new("RGB", (1600, 900), "white")
    draw = ImageDraw.Draw(img)
    draw.text((100, 28), "Tail divergence noise increases as df decreases (n=80)", fill="black", font=font(30, True))
    left, top, right, bottom = 130, 105, 1500, 700
    draw.line((left, bottom, right, bottom), fill="black", width=2)
    draw.line((left, top, left, bottom), fill="black", width=2)
    max_value = max(float(r["max_to_mean_ratio"]) for r in noise_rows)
    for tick in [0, 1, 2, 3, 4, 5, 6]:
        y = bottom - tick / 6 * (bottom - top)
        draw.line((left, y, right, y), fill=(226, 226, 226), width=1)
        draw.text((left - 48, y - 10), str(tick), fill="black", font=font(18))
    bar_group = (right - left) / len(labels)
    bar_width = bar_group * 0.28
    for idx, label in enumerate(labels):
        center = left + bar_group * idx + bar_group / 2
        draw.text((center - 28, bottom + 18), label, fill="black", font=font(16))
        for kind_offset, kind in enumerate(["l2", "l1"]):
            row = next(r for r in noise_rows if r["df_label"] == label and r["kind"] == kind)
            value = float(row["max_to_mean_ratio"])
            y = bottom - value / max_value * (bottom - top)
            x = center + (kind_offset - 0.5) * bar_width * 1.35
            draw.rectangle((x - bar_width / 2, y, x + bar_width / 2, bottom), fill=kind_colors[kind])
    for kind_offset, kind in enumerate(["l2", "l1"]):
        lx, ly = right - 150, top + 32 + kind_offset * 34
        draw.rectangle((lx, ly, lx + 30, ly + 18), fill=kind_colors[kind])
        draw.text((lx + 42, ly - 2), kind, fill="black", font=font(18))
    draw.text((690, bottom + 62), "tail setting", fill="black", font=font(22))
    draw.text((15, top + 170), "max / mean divergence", fill="black", font=font(22))
    img.save(FIGURES_DIR / "tail_df_background_noise_20260719.png")

    img = Image.new("RGB", (1600, 920), "white")
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = 120, 100, 1500, 700
    draw_axes(
        draw,
        left,
        top,
        right,
        bottom,
        "Higher-replication independent-null validation (n=80, k=2, mag=8)",
        "tail setting",
        "rejection rate",
    )
    alpha_y = ymap(0.05, top, bottom)
    for x0 in range(left, right, 24):
        draw.line((x0, alpha_y, min(x0 + 12, right), alpha_y), fill=(180, 0, 0), width=2)
    validation_path = RESULTS_DIR / "tail_df_null_validation_20260719.tsv"
    if validation_path.exists():
        with validation_path.open() as f:
            validation_rows = list(csv.DictReader(f, delimiter="\t"))
    else:
        validation_rows = []
    step = (right - left) / (len(labels) - 1)
    for idx, label in enumerate(labels):
        x = left + idx * step
        draw.line((x, bottom, x, bottom + 8), fill="black", width=2)
        draw.text((x - 28, bottom + 18), label, fill="black", font=font(16))
    for kind in ["l2", "l1"]:
        subset = [r for r in validation_rows if r["kind"] == kind]
        subset = sorted(subset, key=lambda r: x_positions[r["df_label"]])
        points = [
            (
                left + x_positions[r["df_label"]] * step,
                ymap(float(r["rejection_rate"]), top, bottom),
            )
            for r in subset
        ]
        for p0, p1 in zip(points, points[1:]):
            draw.line((*p0, *p1), fill=kind_colors[kind], width=4)
        for x, y in points:
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=kind_colors[kind])
        lx, ly = right - 150, top + 32 + ["l2", "l1"].index(kind) * 34
        draw.line((lx, ly, lx + 34, ly), fill=kind_colors[kind], width=4)
        draw.text((lx + 45, ly - 12), kind, fill="black", font=font(18))
    img.save(FIGURES_DIR / "tail_df_null_validation_20260719.png")


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)
    grid_rows = run_tail_factor_grid()
    noise_rows = run_background_noise_grid()
    validation_rows = run_tail_null_validation()
    write_tsv(RESULTS_DIR / "tail_df_factor_grid_20260719.tsv", grid_rows)
    write_tsv(RESULTS_DIR / "tail_df_background_noise_20260719.tsv", noise_rows)
    write_tsv(RESULTS_DIR / "tail_df_null_validation_20260719.tsv", validation_rows)
    make_figures(grid_rows, noise_rows)


if __name__ == "__main__":
    main()
