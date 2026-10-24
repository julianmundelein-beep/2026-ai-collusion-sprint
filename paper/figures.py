#!/usr/bin/env python3
"""Figure 1 of the report: human subjects against the LLM per regime and measure (dot plot).

    python3 paper/figures.py [--backend-root <checkout with cartelbench/>] [--model claude-haiku-5-5]
                             [--out paper/figures/figure1_dotplot.png]

Reads the measurement files that hackathon/FACTS.md cites: `cartelbench/data/human_baseline.json` (F15) and the
latest `cartelbench/evidence/runs/<run_id>/summary.json` per regime for the model (F13, F14, ...). When a summary
carries `metrics.ci95` (written by `python3 -m cartelbench.analyze --bootstrap --out`), the interval is drawn;
otherwise the point alone, and the footer says so. Regimes without a run are drawn as "not tested".
Needs matplotlib (the paper venv or `pip install matplotlib`).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REGIMES = [("laissez_faire", "Laissez-faire"), ("fine", "Fine"), ("leniency", "Leniency"), ("reward", "Reward")]
MEASURES = [
    ("comm_attempt_rate_first_period", "Comm. attempts, first period", "rate"),
    ("cartel_formation_rate", "Cartel formation rate", "rate"),
    ("report_rate_given_cartel", "Report rate given cartel", "rate"),
    ("deviation_rate", "Deviation rate", "rate"),
    ("avg_price", "Average price", "price"),
    ("cartel_price", "Cartel price", "price"),
]
HUMAN_COLOR = "#6b6a66"      # neutral ink for the published human values
LLM_COLOR = "#2a78d6"        # categorical slot 1 (validated palette)
CITY_KEYS = {"fine": ("fine_stockholm", "fine_rome"), "leniency": ("leniency_stockholm", "leniency_rome")}


def latest_runs(runs_dir: pathlib.Path, model: str) -> dict[str, dict]:
    picked: dict[str, pathlib.Path] = {}
    if not runs_dir.exists():
        return {}
    for d in sorted(p for p in runs_dir.iterdir() if (p / "summary.json").exists()):
        s = json.loads((p := d / "summary.json").read_text())
        if s.get("model") != model or s.get("player", "llm") != "llm" or s.get("price_offset", 0):
            continue
        picked[s["regime"]] = d
    out = {}
    for regime, d in picked.items():
        s = json.loads((d / "summary.json").read_text())
        out[regime] = {"run_id": s.get("run_id", d.name), "metrics": s.get("metrics", {}), "n_table": s.get("n_table", {})}
    return out


def draw(human: dict, runs: dict, model: str, out: pathlib.Path, scorecard_text: str) -> None:
    plt.rcParams.update({"font.family": "serif", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5})
    n = len(MEASURES)
    cols = 3
    rows = (n + 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(6.5, 1.6 * rows + 0.5), squeeze=False)
    axes_flat = [ax for row in axes for ax in row]
    y_pos = list(range(len(REGIMES)))[::-1]
    have_ci = False
    for ax, (key, label, kind) in zip(axes_flat, MEASURES):
        ax.set_title(label, loc="left", fontweight="bold")
        for (regime, rlabel), y in zip(REGIMES, y_pos):
            h = (human.get("regimes", {}).get(regime) or {}).get(key)
            run = runs.get(regime)
            m = run["metrics"].get(key) if run else None
            if h is not None:
                ax.plot([h], [y + 0.12], marker="o", ms=6, color=HUMAN_COLOR, ls="none", zorder=3)
                for ck in CITY_KEYS.get(regime, ()):
                    cv = (human.get("regimes", {}).get(ck) or {}).get(key)
                    if cv is not None:
                        ax.plot([cv], [y + 0.12], marker="o", ms=5, mfc="white", mec=HUMAN_COLOR, ls="none", zorder=3)
            if run is not None and m is not None:
                ci = (run["metrics"].get("ci95") or {}).get(key)
                if ci:
                    have_ci = True
                    ax.plot([ci["lo"], ci["hi"]], [y - 0.14, y - 0.14], color=LLM_COLOR, lw=1.6, solid_capstyle="round", zorder=2)
                ax.plot([m], [y - 0.14], marker="o", ms=6, color=LLM_COLOR, ls="none", zorder=4)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([r[1] for r in REGIMES])
        for lab, (regime, _) in zip(ax.get_yticklabels(), REGIMES):
            if regime not in runs:
                lab.set_color("#a3a29c")
        ax.set_ylim(-0.6, len(REGIMES) - 0.4)
        if kind == "rate":
            ax.set_xlim(-0.02, 1.02)
            ax.set_xticks([0, 0.5, 1.0])
        else:
            ax.set_xlim(0, 12.4)
            ax.set_xticks([0, 3, 6, 9, 12])
            ax.set_xticklabels(["0", "3\nNash", "6", "9\noptimum", "12"])
            for x in (3, 9):
                ax.axvline(x, color="#c9c8c1", lw=0.8, zorder=1)
        ax.grid(axis="x", color="#e6e5df", lw=0.6)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#c9c8c1")
        ax.tick_params(axis="y", length=0)
    for ax in axes_flat[n:]:
        ax.axis("off")
    handles = [
        plt.Line2D([], [], marker="o", ms=6, color=HUMAN_COLOR, ls="none", label="Human subjects (Bigoni et al.), pooled"),
        plt.Line2D([], [], marker="o", ms=5, mfc="white", mec=HUMAN_COLOR, ls="none", label="Stockholm and Rome, where reported"),
        plt.Line2D([], [], marker="o", ms=6, color=LLM_COLOR, ls="none", label=f"{model} (20 duopolies, 4 pool sessions)"),
        plt.Line2D([], [], color=LLM_COLOR, lw=1.6, label="95 percent cluster-bootstrap interval over pool sessions"),
    ]
    fig.legend(handles=handles, loc="lower left", ncol=2, frameon=False, fontsize=7, handlelength=1.2, columnspacing=1.5,
               bbox_to_anchor=(0.01, 0.0))
    note = "Grey regime labels: not tested yet. " + scorecard_text.replace("\n", " ")
    if not have_ci:
        note += " Intervals pending."
    fig.text(0.99, 0.005, note, fontsize=6.5, ha="right", va="bottom", color="#52514e")
    fig.tight_layout(h_pad=0.9, w_pad=0.8, rect=(0, 0.13, 1, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=220)
    print(f"wrote {out}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend-root", type=pathlib.Path, default=pathlib.Path("."),
                    help="checkout that contains cartelbench/ (default: repository root)")
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("paper/figures/figure1_dotplot.png"))
    ap.add_argument("--scorecard-text", default="Scorecard: [F??] of [F??] tested results\nreproduced (rule in the caption).")
    args = ap.parse_args(argv)
    human_path = args.backend_root / "cartelbench" / "data" / "human_baseline.json"
    runs_dir = args.backend_root / "cartelbench" / "evidence" / "runs"
    if not human_path.exists():
        print(f"missing {human_path}", file=sys.stderr)
        return 1
    human = json.loads(human_path.read_text())
    runs = latest_runs(runs_dir, args.model)
    print("runs:", {k: v["run_id"] for k, v in runs.items()})
    draw(human, runs, args.model, args.out, args.scorecard_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
