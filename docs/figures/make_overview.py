"""Overview figure of the four models from the Cartel Risk Cards (recorded runs only, no API call).

    python3 docs/figures/make_overview.py [--out docs/figures/model_overview.png] [--dark-out docs/figures/model_overview_dark.png]

Reads cartelbench/evidence/risk_cards/risk_cards.json (written by python3 cartelbench/scripts/risk_card.py) and
cartelbench/data/human_baseline.json, draws one panel per measure with one row per model, and writes the plotted
numbers next to the figure as model_overview.json so that every value in the picture can be checked against its
source key in the risk cards. The dark-mode copy (light ink, lifted hues, GitHub's dark surface) is the same picture
for viewers with a dark theme.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
CARDS = ROOT / "cartelbench/evidence/risk_cards/risk_cards.json"
HUMANS = ROOT / "cartelbench/data/human_baseline.json"

MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "qwen2.5-32b-instruct", "llama-3.1-8b-instruct"]
# One fixed colour per model, the same hues as paper/figure_diagonal.py; the row label carries the identity,
# the colour only repeats it. Checked for colour-vision deficiency (deutan, protan, tritan) before use.
COLORS = {"claude-haiku-5-5": "#eb6834", "claude-sonnet-5-5": "#2a78d6",
          "qwen2.5-32b-instruct": "#16996a", "llama-3.1-8b-instruct": "#6250d6"}
INK, MUTED, GRID, HUMAN = "#0b0b0b", "#52514e", "#e4e3df", "#6b6a66"
THEMES = {
    "light": {"colors": COLORS, "ink": INK, "muted": MUTED, "grid": GRID, "human": HUMAN, "bg": "white", "ring": "white"},
    "dark": {"colors": {"claude-haiku-5-5": "#e66b38", "claude-sonnet-5-5": "#4489de",
                        "qwen2.5-32b-instruct": "#21a06d", "llama-3.1-8b-instruct": "#8c7ce8"},
             "ink": "#e6edf3", "muted": "#9da7b3", "grid": "#30363d", "human": "#b1bac4", "bg": "#0d1117", "ring": "#0d1117"},
}


def panels(cards: dict, humans: dict) -> list[dict]:
    """One entry per panel: title, per-model value with its source key, the human or reference value, x-range."""
    h = humans["regimes"]
    out = []

    def pick(section: str, *keys):
        vals = {}
        for m in MODELS:
            v = cards[m]["sections"].get(section, {})
            for k in keys:
                v = v.get(k, {}) if isinstance(v, dict) else {}
            vals[m] = v.get("point") if isinstance(v, dict) else v
        return vals

    out.append({"title": "Cartel incidence,\nno authority", "key": "formation.incidence",
                "values": pick("formation", "incidence"), "human": h["laissez_faire"]["cartel_incidence"],
                "human_label": "students", "xlim": (0, 1.08), "fmt": "{:.3f}"})
    out.append({"title": "Cartel incidence,\nfine", "key": "deterrence.fine_incidence",
                "values": pick("deterrence", "fine_incidence"), "human": h["fine"]["cartel_incidence"],
                "human_label": "students", "xlim": (0, 1.08), "fmt": "{:.3f}"})
    out.append({"title": "Average price,\nreward", "key": "reward.avg_price",
                "values": pick("reward", "avg_price"), "human": h["reward"]["avg_price"],
                "human_label": "students", "xlim": (2.4, 9.6), "fmt": "{:.2f}", "nash": 3})
    out.append({"title": "Average price,\nno price channel", "key": "silent.nocomm_avg_price",
                "values": pick("silent", "nocomm_avg_price"), "human": None,
                "human_label": None, "xlim": (2.4, 9.6), "fmt": "{:.2f}", "nash": 3})
    share = {}
    for m in MODELS:
        cell = [c for c in cards[m]["sections"]["threshold"] if c.get("p") == 4][0]
        v = cell["share_at_threshold"]
        share[m] = v["point"] if isinstance(v, dict) else v
    out.append({"title": "Share of prices exactly\nat the announced threshold 4", "key": "threshold[p=4].share_at_threshold",
                "values": share, "human": None, "human_label": None, "xlim": (0, 1.08), "fmt": "{:.2f}"})
    return out


def draw(cards: dict, humans: dict, out: pathlib.Path, theme: str = "light") -> list[dict]:
    t = THEMES[theme]
    colors, ink, muted, grid, human = t["colors"], t["ink"], t["muted"], t["grid"], t["human"]
    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "figure.facecolor": t["bg"], "axes.facecolor": t["bg"]})
    ps = panels(cards, humans)
    fig, axes = plt.subplots(1, len(ps), figsize=(13.5, 3.4), sharey=True)
    ys = list(range(len(MODELS)))[::-1]
    for ax, p in zip(axes, ps):
        ax.set_title(p["title"], fontsize=10.5, loc="left", color=ink)
        lo, hi = p["xlim"]
        if p.get("nash") is not None:
            ax.axvline(p["nash"], color=muted, lw=0.8, ls=":", zorder=1)
            ax.text(p["nash"] + 0.1, ys[-1] - 0.75, "Nash 3", fontsize=10, color=muted, va="center")
        if p["human"] is not None:
            ax.axvline(p["human"], color=human, lw=0.8, ls="--", zorder=1)
            ax.text(p["human"], ys[0] + 0.72, f"{p['human_label']} {p['fmt'].format(p['human'])}", fontsize=10,
                    color=human, ha="center", va="bottom")
        for y, m in zip(ys, MODELS):
            v = p["values"][m]
            ax.plot([lo, v], [y, y], color=colors[m], lw=2.2, solid_capstyle="round", zorder=2)
            ax.plot([v], [y], marker="o", ms=8, color=colors[m], mec=t["ring"], mew=1.2, zorder=3)
            ax.text(v + (hi - lo) * 0.035, y, p["fmt"].format(v), fontsize=10, color=ink, va="center")
        ax.set_xlim(lo, hi)
        ax.set_ylim(-1.1, len(MODELS) - 0.3 + 0.9)
        ax.set_yticks(ys)
        ax.set_yticklabels([cards[m]["name"] for m in MODELS], fontsize=10.5, color=ink)
        ax.grid(axis="x", color=grid, lw=0.6)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(muted)
        ax.tick_params(axis="x", colors=muted, labelsize=10)
        ax.tick_params(axis="y", length=0)
    fig.text(0.5, -0.04,
             "From the Cartel Risk Cards (cartelbench/evidence/risk_cards/risk_cards.json). Dashed line: human subjects "
             "of Bigoni et al. (2012); dotted line: competitive (Nash) price 3. No channel: no price discussion possible.",
             ha="center", fontsize=10, color=muted)
    fig.tight_layout(w_pad=1.2)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=t["bg"])
    return [{"panel": p["title"].replace("\n", " "), "risk_card_key": p["key"], "human": p["human"],
             "values": {cards[m]["name"]: p["values"][m] for m in MODELS}} for p in ps]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "docs/figures/model_overview.png")
    ap.add_argument("--dark-out", type=pathlib.Path, default=ROOT / "docs/figures/model_overview_dark.png")
    args = ap.parse_args()
    cards = json.loads(CARDS.read_text())
    humans = json.loads(HUMANS.read_text())
    rows = draw(cards["cards"], humans, args.out)
    draw(cards["cards"], humans, args.dark_out, theme="dark")
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    except OSError:
        commit = "unknown"
    side = args.out.with_suffix(".json")
    side.write_text(json.dumps({
        "generated_by": "python3 docs/figures/make_overview.py",
        "commit": commit,
        "time": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "Do not edit by hand. Values copied from risk_cards.json (commit " + cards["commit"][:7] + ").",
        "risk_cards_commit": cards["commit"],
        "panels": rows,
    }, indent=1) + "\n")
    print(f"wrote {args.out}, {args.dark_out} and {side}")


if __name__ == "__main__":
    main()
