#!/usr/bin/env python3
"""Figure: average price against the announced screen threshold, four models (round 7, F85, F86).

    python3 paper/figure_diagonal.py [--data cartelbench/evidence/round7/diagonal.json] [--out paper/figures/figure_diagonal.png]

Points are cell means with 95 percent cluster-bootstrap intervals over 4 pool sessions; filled markers where the
modal price equals the threshold. The dashed diagonal is price = threshold; the dotted line the Nash price 3.
Minimum font size 8 pt for print. Slopes in the legend are the registered estimates (F85).
"""
import argparse
import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

COLORS = {"Sonnet 5.5": "#2a78d6", "Haiku 5.5": "#eb6834", "Qwen2.5-32B": "#1baf7a", "Llama-3.1-8B": "#6250d6"}
MARKERS = {"Sonnet 5.5": "o", "Haiku 5.5": "s", "Qwen2.5-32B": "D", "Llama-3.1-8B": "^"}
SLOPE = {"Sonnet 5.5": "+0.98", "Haiku 5.5": "+0.70", "Qwen2.5-32B": "+0.68", "Llama-3.1-8B": "+0.31"}
OFFSET = {"Sonnet 5.5": -0.15, "Haiku 5.5": -0.05, "Qwen2.5-32B": 0.05, "Llama-3.1-8B": 0.15}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=pathlib.Path, default=pathlib.Path("cartelbench/evidence/round7/diagonal.json"))
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("paper/figures/figure_diagonal.png"))
    args = ap.parse_args()
    d = json.loads(args.data.read_text())
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 8})
    fig, ax = plt.subplots(figsize=(6.5, 2.7))
    ax.plot([2.6, 7.4], [2.6, 7.4], ls="--", color="#8a8984", lw=1, zorder=1)
    ax.axhline(3, ls=":", color="#b3b2ab", lw=1, zorder=1)
    ax.text(7.45, 7.35, "price = threshold", fontsize=8, color="#6b6a66", va="center")
    ax.text(7.45, 3.0, "Nash 3", fontsize=8, color="#6b6a66", va="center")
    for model in COLORS:
        rows = sorted((r for r in d["rows"] if r["model"] == model), key=lambda r: r["threshold"])
        if not rows:
            continue
        xs = [r["threshold"] + OFFSET[model] for r in rows]
        ys = [r["avg_price"] for r in rows]
        ax.plot(xs, ys, color=COLORS[model], lw=1.2, zorder=2)
        for r, x in zip(rows, xs):
            if r.get("avg_price_lo") is not None:
                ax.plot([x, x], [r["avg_price_lo"], r["avg_price_hi"]], color=COLORS[model], lw=1.2, zorder=2)
            filled = r.get("modal_price") == r["threshold"]
            ax.plot([x], [r["avg_price"]], marker=MARKERS[model], ms=5.5, color=COLORS[model],
                    mfc=COLORS[model] if filled else "white", mec=COLORS[model], ls="none", zorder=3)
        ax.plot([], [], marker=MARKERS[model], color=COLORS[model], ms=5.5, lw=1.2, label=f"{model}, slope {SLOPE[model]}")
    ax.set_xlabel("announced screen threshold (prices above it in two consecutive periods are fined)")
    ax.set_ylabel("average price")
    ax.set_xticks([3, 4, 5, 6, 7])
    ax.set_xlim(2.6, 8.4)
    ax.set_ylim(2.6, 7.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e6e5df", lw=0.6)
    ax.legend(loc="upper left", frameon=False, fontsize=8, handlelength=1.6)
    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=300)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
