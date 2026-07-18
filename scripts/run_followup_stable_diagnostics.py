from pathlib import Path
import csv
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from cdelta import (
    _wilson_interval,
    c_delta,
    make_independent_extreme_scenario,
    make_multi_extreme_scenario,
)


RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"


def write_tsv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"no rows to write for {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def p_value_summary(p_values: list[float]) -> dict[str, float]:
    arr = np.asarray(p_values, dtype=float)
    return {
        "mean_p": round(float(arr.mean()), 4),
        "p05": round(float(np.quantile(arr, 0.05)), 4),
        "p50": round(float(np.quantile(arr, 0.50)), 4),
        "p95": round(float(np.quantile(arr, 0.95)), 4),
    }


def fast_permutation_p_value(
    dx: np.ndarray,
    dy: np.ndarray,
    observed: float,
    *,
    n_perm: int,
    seed: int,
) -> float:
    """Compute the same upper-tail permutation p-value in vectorized batches."""
    rng = np.random.default_rng(seed)
    n = dx.size
    order = np.argsort(rng.random((n_perm, n)), axis=1)
    mean_dx = float(dx.mean())
    mean_dy = float(dy.mean())
    stats = np.mean(dx[None, :] * dy[order], axis=1) / (mean_dx * mean_dy)
    return float((np.sum(stats >= observed) + 1) / (n_perm + 1))


def run_flagged_null_checks() -> list[dict]:
    """Re-test yesterday's largest independent-null flags with more repetition."""
    settings = [
        {"target_source": "extended_0.25", "kind": "l2", "background": "normal", "n": 160, "k": 1, "magnitude": 2.5},
        {"target_source": "extended_0.35", "kind": "l2", "background": "normal", "n": 160, "k": 2, "magnitude": 4.0},
        {"target_source": "extended_0.35", "kind": "l2", "background": "normal", "n": 160, "k": 3, "magnitude": 3.5},
        {"target_source": "extended_0.35", "kind": "l1", "background": "normal", "n": 160, "k": 2, "magnitude": 3.5},
        {"target_source": "extended_0.35", "kind": "l1", "background": "normal", "n": 160, "k": 3, "magnitude": 3.5},
        {"target_source": "extended_0.35", "kind": "l2", "background": "t2", "n": 40, "k": 1, "magnitude": 10.0},
        {"target_source": "extended_0.35", "kind": "l1", "background": "t2", "n": 40, "k": 1, "magnitude": 10.0},
        {"target_source": "extended_0.35", "kind": "l1", "background": "lognormal", "n": 40, "k": 3, "magnitude": 4.5},
    ]
    repetitions = 1200
    n_perm = 799
    alpha = 0.05
    rows = []
    for setting_offset, setting in enumerate(settings):
        p_values = []
        overlaps = []
        norm_values = []
        corr_values = []
        for rep in range(repetitions):
            seed = 20260718 + setting_offset * 2_000_000 + rep
            x, y, x_idx, y_idx = make_independent_extreme_scenario(
                n=setting["n"],
                k=setting["k"],
                seed=seed,
                magnitude=setting["magnitude"],
                background=setting["background"],
            )
            result = c_delta(x, y, kind=setting["kind"])
            p_value = fast_permutation_p_value(
                result.dx,
                result.dy,
                result.raw,
                n_perm=n_perm,
                seed=seed + 1_000_000,
            )
            p_values.append(p_value)
            overlaps.append(len(set(x_idx).intersection(y_idx)))
            norm_values.append(result.normalized_pairing)
            corr_values.append(result.direction_correlation)

        reject_count = int(sum(p < alpha for p in p_values))
        lo, hi = _wilson_interval(reject_count, repetitions)
        row = {
            **setting,
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
        rows.append(row)
    return rows


def run_power_curve_checks() -> list[dict]:
    """Power curves over sample size, magnitude, and subgroup size."""
    rows = []
    alpha = 0.05
    repetitions = 180
    n_perm = 299
    magnitudes = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for n_offset, n in enumerate([20, 40, 80, 160]):
            for k_offset, k in enumerate([1, 2, 3]):
                if n < 2 * k + 2:
                    continue
                for mag_offset, magnitude in enumerate(magnitudes):
                    p_values = []
                    norm_values = []
                    corr_values = []
                    for rep in range(repetitions):
                        seed = (
                            20260718
                            + kind_offset * 10_000_000
                            + n_offset * 1_000_000
                            + k_offset * 100_000
                            + mag_offset * 10_000
                            + rep
                        )
                        x, y, _ = make_multi_extreme_scenario(
                            n=n,
                            k=k,
                            seed=seed,
                            magnitude=magnitude,
                            background="normal",
                            matched=True,
                        )
                        result = c_delta(x, y, kind=kind)
                        p_value = fast_permutation_p_value(
                            result.dx,
                            result.dy,
                            result.raw,
                            n_perm=n_perm,
                            seed=seed + 1_000_000,
                        )
                        p_values.append(p_value)
                        norm_values.append(result.normalized_pairing)
                        corr_values.append(result.direction_correlation)
                    reject_count = int(sum(p < alpha for p in p_values))
                    lo, hi = _wilson_interval(reject_count, repetitions)
                    rows.append(
                        {
                            "kind": kind,
                            "background": "normal",
                            "n": n,
                            "k_extremes": k,
                            "magnitude": magnitude,
                            "scenario": "matched",
                            "alpha": alpha,
                            "repetitions": repetitions,
                            "n_perm": n_perm,
                            "reject_count": reject_count,
                            "rejection_rate": round(reject_count / repetitions, 4),
                            "wilson_low": round(float(lo), 4),
                            "wilson_high": round(float(hi), 4),
                            "mean_norm": round(float(np.mean(norm_values)), 4),
                            "mean_corr": round(float(np.mean(corr_values)), 4),
                            **p_value_summary(p_values),
                        }
                    )
    return rows


def run_heavy_tail_gradient() -> list[dict]:
    """Compare matched power and independent-null size across tail gradients."""
    rows = []
    alpha = 0.05
    repetitions = 300
    n_perm = 399
    backgrounds = ["normal", "t5", "t3", "t2", "lognormal"]
    # t5 is generated locally because the core background helper currently
    # supports only normal, t3, t2, and lognormal.
    for kind_offset, kind in enumerate(["l2", "l1"]):
        for bg_offset, background in enumerate(backgrounds):
            for scenario_offset, scenario in enumerate(["matched", "independent_null"]):
                p_values = []
                norm_values = []
                corr_values = []
                overlaps = []
                for rep in range(repetitions):
                    seed = (
                        20260718
                        + kind_offset * 10_000_000
                        + bg_offset * 1_000_000
                        + scenario_offset * 100_000
                        + rep
                    )
                    if background == "t5":
                        rng = np.random.default_rng(seed)
                        x = rng.standard_t(df=5, size=80)
                        y = rng.standard_t(df=5, size=80)
                        x_idx = np.arange(78, 80)
                        if scenario == "matched":
                            y_idx = x_idx
                        else:
                            y_idx = np.sort(rng.choice(80, size=2, replace=False))
                        x[x_idx] = 8.0
                        y[y_idx] = 8.0
                        overlaps.append(len(set(x_idx.tolist()).intersection(y_idx.tolist())))
                    elif scenario == "matched":
                        x, y, _ = make_multi_extreme_scenario(
                            n=80,
                            k=2,
                            seed=seed,
                            magnitude=8.0,
                            background=background,
                            matched=True,
                        )
                        overlaps.append(2)
                    else:
                        x, y, x_idx, y_idx = make_independent_extreme_scenario(
                            n=80,
                            k=2,
                            seed=seed,
                            magnitude=8.0,
                            background=background,
                        )
                        overlaps.append(len(set(x_idx).intersection(y_idx)))

                    result = c_delta(x, y, kind=kind)
                    p_value = fast_permutation_p_value(
                        result.dx,
                        result.dy,
                        result.raw,
                        n_perm=n_perm,
                        seed=seed + 1_000_000,
                    )
                    p_values.append(p_value)
                    norm_values.append(result.normalized_pairing)
                    corr_values.append(result.direction_correlation)

                reject_count = int(sum(p < alpha for p in p_values))
                lo, hi = _wilson_interval(reject_count, repetitions)
                rows.append(
                    {
                        "kind": kind,
                        "background": background,
                        "n": 80,
                        "k_extremes": 2,
                        "magnitude": 8.0,
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


def make_figures(flag_rows: list[dict], power_rows: list[dict], tail_rows: list[dict]) -> None:
    FIGURES_DIR.mkdir(exist_ok=True)

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

    def canvas(width: int = 1500, height: int = 900):
        img = Image.new("RGB", (width, height), "white")
        return img, ImageDraw.Draw(img)

    def draw_axes(draw, left, top, right, bottom, title, xlabel, ylabel):
        draw.line((left, bottom, right, bottom), fill="black", width=2)
        draw.line((left, top, left, bottom), fill="black", width=2)
        draw.text((left, 24), title, fill="black", font=font(30, True))
        draw.text(((left + right) // 2 - 90, bottom + 58), xlabel, fill="black", font=font(22))
        label_font = font(22)
        label_box = Image.new("RGBA", (360, 40), (255, 255, 255, 0))
        label_draw = ImageDraw.Draw(label_box)
        label_draw.text((0, 6), ylabel, fill="black", font=label_font)
        rotated = label_box.rotate(90, expand=True)
        draw.bitmap((24, top + (bottom - top) // 2 - rotated.size[1] // 2), rotated, fill=None)
        for value in [0.0, 0.25, 0.5, 0.75, 1.0]:
            y = bottom - value * (bottom - top)
            draw.line((left - 8, y, left, y), fill="black", width=2)
            draw.text((left - 62, y - 12), f"{value:.2f}", fill="black", font=font(18))
            draw.line((left, y, right, y), fill=(228, 228, 228), width=1)

    def ymap(value, top, bottom):
        return bottom - max(0.0, min(1.0, float(value))) * (bottom - top)

    img, draw = canvas(1600, 920)
    labels = [
        f"{r['kind']}/{r['background']}\nn={r['n']}, k={r['k']}"
        for r in flag_rows
    ]
    rates = [r["rejection_rate"] for r in flag_rows]
    left, top, right, bottom = 135, 100, 1540, 700
    draw_axes(
        draw,
        left,
        top,
        right,
        bottom,
        "High-replication checks for flagged null settings",
        "flagged setting",
        "rejection rate",
    )
    alpha_y = ymap(0.05, top, bottom)
    for x0 in range(left, right, 24):
        draw.line((x0, alpha_y, min(x0 + 12, right), alpha_y), fill=(180, 0, 0), width=2)
    step = (right - left) / (len(labels) - 1)
    for idx, row in enumerate(flag_rows):
        x = left + idx * step
        y = ymap(row["rejection_rate"], top, bottom)
        lo_y = ymap(row["wilson_low"], top, bottom)
        hi_y = ymap(row["wilson_high"], top, bottom)
        draw.line((x, lo_y, x, hi_y), fill=(40, 95, 160), width=3)
        draw.line((x - 10, lo_y, x + 10, lo_y), fill=(40, 95, 160), width=3)
        draw.line((x - 10, hi_y, x + 10, hi_y), fill=(40, 95, 160), width=3)
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(40, 95, 160))
        lines = labels[idx].split("\n")
        draw.text((x - 54, bottom + 22), lines[0], fill="black", font=font(16))
        draw.text((x - 54, bottom + 44), lines[1], fill="black", font=font(16))
    img.save(FIGURES_DIR / "flagged_null_high_replication_20260718.png")

    for kind in ["l2", "l1"]:
        img, draw = canvas(1500, 900)
        left, top, right, bottom = 135, 100, 1400, 710
        draw_axes(
            draw,
            left,
            top,
            right,
            bottom,
            f"Power curve for one matched extreme pair ({kind})",
            "matched extreme magnitude",
            "rejection rate",
        )
        draw.line((left, ymap(0.8, top, bottom), right, ymap(0.8, top, bottom)), fill=(80, 80, 80), width=2)
        colors = {
            20: (55, 105, 180),
            40: (218, 125, 48),
            80: (70, 150, 90),
            160: (170, 70, 70),
        }
        min_mag, max_mag = 1.5, 10.0
        def xmap(mag):
            return left + (float(mag) - min_mag) / (max_mag - min_mag) * (right - left)
        for mag in [2, 4, 6, 8, 10]:
            x_tick = xmap(mag)
            draw.line((x_tick, bottom, x_tick, bottom + 8), fill="black", width=2)
            draw.text((x_tick - 10, bottom + 14), str(mag), fill="black", font=font(18))
        for n in [20, 40, 80, 160]:
            subset = [
                r for r in power_rows
                if r["kind"] == kind and r["k_extremes"] == 1 and r["n"] == n
            ]
            subset = sorted(subset, key=lambda r: r["magnitude"])
            points = [(xmap(r["magnitude"]), ymap(r["rejection_rate"], top, bottom)) for r in subset]
            for p0, p1 in zip(points, points[1:]):
                draw.line((*p0, *p1), fill=colors[n], width=4)
            for x, y in points:
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=colors[n])
            lx, ly = right - 180, top + 30 + [20, 40, 80, 160].index(n) * 34
            draw.line((lx, ly + 10, lx + 36, ly + 10), fill=colors[n], width=4)
            draw.text((lx + 46, ly), f"n={n}", fill="black", font=font(18))
        img.save(FIGURES_DIR / f"power_curve_k1_{kind}_20260718.png")

    img, draw = canvas(1500, 860)
    order = ["normal", "t5", "t3", "t2", "lognormal"]
    left, top, right, bottom = 135, 100, 1400, 680
    draw_axes(
        draw,
        left,
        top,
        right,
        bottom,
        "Heavy-tail gradient at n=80, k=2, magnitude=8",
        "background distribution",
        "matched rejection rate",
    )
    group_width = (right - left) / len(order)
    bar_width = group_width * 0.28
    colors = {"l2": (55, 105, 180), "l1": (218, 125, 48)}
    for offset, kind in enumerate(["l2", "l1"]):
        subset = [
            r for r in tail_rows
            if r["kind"] == kind and r["scenario"] == "matched"
        ]
        values = {
            r["background"]: r["rejection_rate"]
            for r in subset
        }
        for idx, background in enumerate(order):
            center = left + group_width * idx + group_width / 2
            x0 = center + (offset - 0.5) * bar_width * 1.4
            y = ymap(values[background], top, bottom)
            draw.rectangle((x0 - bar_width / 2, y, x0 + bar_width / 2, bottom), fill=colors[kind])
            draw.text((x0 - 20, y - 26), f"{values[background]:.2f}", fill="black", font=font(15))
            if offset == 0:
                draw.text((center - 38, bottom + 18), background, fill="black", font=font(18))
        lx, ly = right - 170, bottom + 54 + offset * 34
        draw.rectangle((lx, ly, lx + 30, ly + 18), fill=colors[kind])
        draw.text((lx + 42, ly - 2), kind, fill="black", font=font(18))
    img.save(FIGURES_DIR / "heavy_tail_gradient_20260718.png")


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    flag_rows = run_flagged_null_checks()
    power_rows = run_power_curve_checks()
    tail_rows = run_heavy_tail_gradient()

    write_tsv(RESULTS_DIR / "flagged_null_high_replication_20260718.tsv", flag_rows)
    write_tsv(RESULTS_DIR / "power_curve_stable_20260718.tsv", power_rows)
    write_tsv(RESULTS_DIR / "heavy_tail_gradient_20260718.tsv", tail_rows)
    make_figures(flag_rows, power_rows, tail_rows)


if __name__ == "__main__":
    main()
