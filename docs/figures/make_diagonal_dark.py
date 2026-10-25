"""Dark-mode display copy of the main figure for the README (docs/figures/diagonal_dark.png).

    python3 docs/figures/make_diagonal_dark.py [--out docs/figures/diagonal_dark.png]

The figure of record is cartelbench/evidence/round7/diagonal.png, drawn by `python3 -m cartelbench.round7 figure`
from the recorded runs. This script redraws the same layout from that command's data file,
cartelbench/evidence/round7/diagonal.json, with light ink for GitHub's dark theme; it reads no run and changes
no number. The README shows this copy only when the viewer's theme is dark.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "cartelbench/evidence/round7/diagonal.json"
MODELS = ["Haiku 5.5", "Sonnet 5.5", "Qwen2.5-32B", "Llama-3.1-8B"]
BG, INK, MUTED, GRID = "#0d1117", "#e6edf3", "#9da7b3", "#30363d"
C_AVG, C_MODE = "#79b3f5", "#ff9f73"  # the light figure's blue and orange, lifted for a dark surface


def draw(data: dict, out: pathlib.Path) -> None:
    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
                         "xtick.labelsize": 8, "ytick.labelsize": 8, "text.color": INK, "axes.labelcolor": INK,
                         "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": MUTED,
                         "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG})
    rows_all = data["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6), sharex=True, sharey=True)
    for ax, m in zip(axes.flat, MODELS):
        rows = [d for d in rows_all if d["model"] == m]
        ax.plot([2.5, 7.5], [2.5, 7.5], color=MUTED, lw=1, ls="--", zorder=1)
        ax.axhline(data["nash_price"], color=MUTED, lw=0.8, ls=":", zorder=1)
        ax.axhline(data["joint_optimum"], color=MUTED, lw=0.8, ls=":", zorder=1)
        ax.text(7.45, 3.12, f"Nash {data['nash_price']}", ha="right", va="bottom", fontsize=8, color=MUTED)
        ax.text(7.45, 8.88, f"joint optimum {data['joint_optimum']}", ha="right", va="top", fontsize=8, color=MUTED)
        ax.text(6.55, 6.95, "price = p", fontsize=8, color=MUTED, ha="right", va="bottom")
        xs = [d["threshold"] for d in rows]
        ys = [d["avg_price"] for d in rows]
        err = [[d["avg_price"] - d["avg_price_lo"] for d in rows], [d["avg_price_hi"] - d["avg_price"] for d in rows]]
        ax.errorbar(xs, ys, yerr=err, fmt="o", color=C_AVG, ms=6, lw=2, capsize=3, label="average price, 95% CI", zorder=3)
        ax.plot(xs, [d["modal_price"] for d in rows], "D", mfc="none", mec=C_MODE, mew=1.6, ms=8, label="modal price", zorder=4)
        for d in rows:
            ax.annotate(f"{d['share_at_threshold']:.0%}", (d["threshold"], d["avg_price"]), textcoords="offset points",
                        xytext=(9, 0), ha="left", va="center", fontsize=8, color=INK)
        ax.set_title(m, color=INK, loc="left")
        ax.set_xlim(2.5, 7.5)
        ax.set_ylim(1.5, 10)
        ax.set_xticks(range(3, 8))
        ax.grid(True, color=GRID, lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.supxlabel("announced threshold p (penalty if both prices are above p in 2 consecutive periods)", fontsize=9, y=0.045, color=INK)
    for ax in axes[:, 0]:
        ax.set_ylabel("price")
    axes[0, 0].legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), frameon=False)
    fig.text(0.01, 0.005, "Percent next to each point: share of prices exactly at the threshold. No price channel; 20 duopoles in 4 pools per cell.",
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "docs/figures/diagonal_dark.png")
    args = ap.parse_args()
    data = json.loads(DATA.read_text())
    draw(data, args.out)
    print(f"wrote {args.out} from {DATA.relative_to(ROOT)} (commit {data['commit'][:7]})")


if __name__ == "__main__":
    main()
