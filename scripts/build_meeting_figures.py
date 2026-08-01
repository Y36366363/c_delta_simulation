from pathlib import Path
import csv
from math import comb

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "results"
OUT = PROJECT_ROOT / "figures"
OUT.mkdir(exist_ok=True)


def read_tsv(name):
    with (ROOT / name).open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


plt.rcParams.update({
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 160,
    "savefig.dpi": 300,
})


def overlap_power():
    rows = read_tsv("forced_overlap_high_rep_20260801.tsv")
    colors = {"normal": "#2f6f9f", "t3": "#d98c2b", "t2": "#a64b5b"}
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6), sharey=True)
    for axis, kind in zip(axes, ["l2", "l1"]):
        for background in ["normal", "t3", "t2"]:
            subset = sorted(
                [r for r in rows if r["kind"] == kind and r["background"] == background],
                key=lambda r: float(r["overlap_fraction"]),
            )
            x = [float(r["overlap_fraction"]) for r in subset]
            y = [float(r["rejection_rate"]) for r in subset]
            low = [float(r["wilson_low"]) for r in subset]
            high = [float(r["wilson_high"]) for r in subset]
            axis.plot(x, y, marker="o", linewidth=2, color=colors[background], label=background)
            axis.fill_between(x, low, high, color=colors[background], alpha=0.12)
            axis.axhline(0.045, color="#666666", linewidth=1, linestyle="--")
        axis.set_title(kind.upper())
        axis.set_xlabel("Paired standout overlap fraction")
        axis.set_xticks([0, .25, .5, .75, 1])
        axis.set_ylim(-.02, 1.04)
        axis.grid(axis="y", alpha=.2)
    axes[0].set_ylabel("Permutation rejection rate")
    axes[1].legend(frameon=False, title="Background", loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "overlap_fraction_rejection_rate.png", bbox_inches="tight")
    plt.close(fig)


def theory_vs_continuous():
    rows = read_tsv("forced_overlap_high_rep_20260801.tsv")
    colors = {"normal": "#2f6f9f", "t3": "#d98c2b", "t2": "#a64b5b"}
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6), sharex=True, sharey=True)
    for axis, kind in zip(axes, ["l2", "l1"]):
        axis.plot([-.08, 1.02], [-.08, 1.02], color="#777777", linestyle="--", linewidth=1, label="identity")
        for background in ["normal", "t3", "t2"]:
            subset = sorted(
                [r for r in rows if r["kind"] == kind and r["background"] == background],
                key=lambda r: int(r["overlap"]),
            )
            x = [float(r["binary_theory_correlation"]) for r in subset]
            y = [float(r["mean_divergence_correlation"]) for r in subset]
            axis.plot(x, y, marker="o", linewidth=2, color=colors[background], label=background)
        axis.axhline(0, color="#999999", linewidth=.8)
        axis.axvline(0, color="#999999", linewidth=.8)
        axis.set_title(kind.upper())
        axis.set_xlabel("Binary-overlap theoretical correlation")
        axis.grid(alpha=.18)
    axes[0].set_ylabel("Mean continuous divergence correlation")
    axes[1].legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "binary_theory_vs_continuous_divergence.png", bbox_inches="tight")
    plt.close(fig)


def overlap_null_distribution():
    rows = read_tsv("random_set_null_overlap_layers_20260801.tsv")
    counts = {m: 0 for m in range(5)}
    total = 0
    for row in rows:
        m = int(row["overlap"])
        count = int(row["count"])
        counts[m] += count
        total += count
    observed = [counts[m] / total for m in range(3)]
    theoretical = [comb(4, m) * comb(76, 4-m) / comb(80, 4) for m in range(3)]
    x = np.arange(3)
    width = .36
    fig, axis = plt.subplots(figsize=(6.8, 3.8))
    bars1 = axis.bar(x-width/2, theoretical, width, color="#2f6f9f", alpha=.8, label="Hypergeometric theory")
    bars2 = axis.bar(x+width/2, observed, width, color="#d98c2b", alpha=.85, label="Observed (18,000 null datasets)")
    for bars in [bars1, bars2]:
        for bar in bars:
            axis.text(bar.get_x()+bar.get_width()/2, bar.get_height()+.015, f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=9)
    axis.set_xticks(x, ["0", "1", "2"])
    axis.set_xlabel("Realized paired standout overlap M")
    axis.set_ylabel("Probability")
    axis.set_ylim(0, .9)
    axis.legend(frameon=False)
    axis.grid(axis="y", alpha=.2)
    axis.text(.98, .73, "Theory: P(M ≥ 3) = 0.000193", transform=axis.transAxes, ha="right", color="#555555")
    fig.tight_layout()
    fig.savefig(OUT / "random_set_overlap_hypergeometric.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    overlap_power()
    theory_vs_continuous()
    overlap_null_distribution()
