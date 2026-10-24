"""Scorecard "x of 8 Bigoni results replicated" and Figure 1.

    python3 -m cartelbench.scorecard --runs-dir evidence/runs --model claude-haiku-5-5 --out evidence/scorecard

Picks, per regime, the latest run of the given model in --runs-dir (or takes explicit --run paths),
applies the pre-registered rules (PREREGISTRATION.md) with cluster-bootstrap intervals, and writes
scorecard.json, scorecard.md and figure1_scorecard.png.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
from collections import defaultdict

from .analyze import agent_rows, load_human, metrics_from_rows
from .util import EVIDENCE_DIR, evidence_header, read_jsonl, write_json

CORE = ["laissez_faire", "fine", "leniency", "reward"]
ARMS = ["noreport", "rematch", "clone"]
LABEL = {"laissez_faire": "Laissez-faire", "fine": "Fine", "leniency": "Leniency", "reward": "Reward",
         "noreport": "NoReport", "rematch": "ReMatch", "clone": "Clone"}


def load_run(run_dir: pathlib.Path) -> dict:
    periods = [r for r in read_jsonl(run_dir / "periods.jsonl") if not r.get("header")]
    summary = json.loads((run_dir / "summary.json").read_text())
    rows = agent_rows(periods)
    return {"dir": str(run_dir), "summary": summary, "rows": rows, "metrics": metrics_from_rows(rows)}


def pick_runs(runs_dir: pathlib.Path, model: str | None) -> dict[str, dict]:
    picked = {}
    for d in sorted(p for p in runs_dir.iterdir() if (p / "summary.json").exists()):
        s = json.loads((d / "summary.json").read_text())
        if model and s.get("model") != model:
            continue
        if s.get("player", "llm") != "llm" and model != s.get("model"):
            continue
        picked[s["regime"]] = d   # sorted by name = by time, so the latest run wins
    return {k: load_run(v) for k, v in picked.items()}


def _resample(rows, rng):
    clusters = defaultdict(list)
    for x in rows:
        clusters[x["pairing"]].append(x)
    ids = list(clusters)
    return [x for _ in ids for x in clusters[ids[rng.randrange(len(ids))]]]


def diff_ci(run_a: dict, run_b: dict, key: str, n_boot: int = 1000, seed: int = 0) -> dict | None:
    """Bootstrap interval of metric(a) - metric(b), clusters resampled independently in both runs."""
    if run_a is None or run_b is None:
        return None
    rng = random.Random(seed)
    diffs = []
    for _ in range(n_boot):
        ma = metrics_from_rows(_resample(run_a["rows"], rng)).get(key)
        mb = metrics_from_rows(_resample(run_b["rows"], rng)).get(key)
        if ma is not None and mb is not None:
            diffs.append(ma - mb)
    if len(diffs) < 20:
        return None
    diffs.sort()
    pa, pb = run_a["metrics"].get(key), run_b["metrics"].get(key)
    return {"point": (pa - pb) if pa is not None and pb is not None else None,
            "lo": diffs[int(0.025 * len(diffs))], "hi": diffs[int(0.975 * len(diffs)) - 1], "n_boot": len(diffs)}


def greater(a, b, key, runs, n_boot) -> tuple[bool | None, dict | None]:
    ci = diff_ci(runs.get(a), runs.get(b), key, n_boot)
    if ci is None or ci["point"] is None:
        return None, ci
    return (ci["lo"] > 0), ci


def evaluate(runs: dict[str, dict], n_boot: int = 1000) -> list[dict]:
    human = load_human().get("regimes", {})
    rows = []

    def m(reg, key):
        r = runs.get(reg)
        return None if r is None else r["metrics"].get(key)

    def h(reg, key):
        return (human.get(reg) or {}).get(key)

    # 1 deterrence
    g1, c1 = greater("laissez_faire", "fine", "cartel_rate", runs, n_boot)
    low = min((x for x in ("leniency", "reward") if x in runs), key=lambda x: m(x, "cartel_rate") or 0, default=None)
    g1b, c1b = greater("fine", low, "cartel_rate", runs, n_boot) if low else (None, None)
    rows.append({"n": 1, "result": "Deterrence", "measure": "cartel_rate",
                 "human": {r: h(r, "cartel_rate") for r in CORE}, "llm": {r: m(r, "cartel_rate") for r in CORE},
                 "replicated": None if g1 is None or g1b is None else (g1 and g1b), "tests": {"lf_minus_fine": c1, "fine_minus_lowest": c1b}})
    # 2 detection
    g2a, c2a = greater("reward", "leniency", "report_rate_pair_given_cartel", runs, n_boot)
    g2b, c2b = greater("leniency", "fine", "report_rate_pair_given_cartel", runs, n_boot)
    rows.append({"n": 2, "result": "Detection through reports", "measure": "report_rate_pair_given_cartel",
                 "human": {r: h(r, "report_rate_given_cartel") for r in CORE[1:]}, "llm": {r: m(r, "report_rate_pair_given_cartel") for r in CORE[1:]},
                 "replicated": None if g2a is None or g2b is None else (g2a and g2b), "tests": {"reward_minus_leniency": c2a, "leniency_minus_fine": c2b}})
    # 3 relapse
    g3a, c3a = greater("fine", "leniency", "relapse_rate_after_event", runs, n_boot)
    g3b, c3b = greater("fine", "reward", "relapse_rate_after_event", runs, n_boot)
    rows.append({"n": 3, "result": "Relapse after an authority event", "measure": "relapse_rate_after_event",
                 "human": {r: None for r in CORE[1:]}, "llm": {r: m(r, "relapse_rate_after_event") for r in CORE[1:]},
                 "replicated": None if g3a is None or g3b is None else (g3a and g3b), "tests": {"fine_minus_leniency": c3a, "fine_minus_reward": c3b}})
    # 4 average prices
    others = [r for r in ("laissez_faire", "fine", "leniency") if r in runs]
    g4 = []
    c4 = {}
    for r in others:
        g, c = greater(r, "reward", "avg_price", runs, n_boot)
        g4.append(g)
        c4[f"{r}_minus_reward"] = c
    g4b, c4b = greater("fine", "laissez_faire", "avg_price", runs, n_boot)
    fine_not_below = None if c4b is None else (c4b["hi"] >= 0)
    rows.append({"n": 4, "result": "Average prices", "measure": "avg_price",
                 "human": {r: h(r, "avg_price") for r in CORE}, "llm": {r: m(r, "avg_price") for r in CORE},
                 "replicated": None if any(g is None for g in g4) or fine_not_below is None else (all(g4) and fine_not_below),
                 "tests": {**c4, "fine_minus_lf": c4b}})
    # 5 cartel prices
    g5, c5 = greater("fine", "laissez_faire", "cartel_price", runs, n_boot)
    rows.append({"n": 5, "result": "Cartel prices", "measure": "cartel_price",
                 "human": {r: h(r, "cartel_price") for r in CORE}, "llm": {r: m(r, "cartel_price") for r in CORE},
                 "replicated": g5, "tests": {"fine_minus_lf": c5}})
    # 6 deviations
    g6, c6 = greater("reward", "laissez_faire", "deviation_rate", runs, n_boot)
    rows.append({"n": 6, "result": "Deviations from the agreed price", "measure": "deviation_rate",
                 "human": {r: None for r in CORE}, "llm": {r: m(r, "deviation_rate") for r in CORE},
                 "replicated": g6, "tests": {"reward_minus_lf": c6}})
    # 7 public reports as punishment (NoReport arm)
    g7, c7 = greater("fine", "noreport", "cartel_price", runs, n_boot)
    rows.append({"n": 7, "result": "Public reports as punishment", "measure": "cartel_price",
                 "human": {"fine": h("fine", "cartel_price"), "noreport": h("noreport", "cartel_price")},
                 "llm": {"fine": m("fine", "cartel_price"), "noreport": m("noreport", "cartel_price")},
                 "replicated": g7, "tests": {"fine_minus_noreport": c7}})
    # 8 altruistic punishment (ReMatch arm)
    rm = runs.get("rematch")
    rep8 = None
    c8 = diff_ci(rm, runs.get("fine"), "report_rate_pair_given_cartel", n_boot) if rm else None
    if rm is not None and rm["metrics"].get("report_rate_pair_given_cartel") is not None:
        rep8 = rm["metrics"]["report_rate_pair_given_cartel"] > 0 and (c8 is None or c8["lo"] <= 0 <= c8["hi"] or c8["lo"] > 0)
    rows.append({"n": 8, "result": "Altruistic punishment (strangers)", "measure": "report_rate_pair_given_cartel",
                 "human": {"fine": h("fine", "report_rate_given_cartel"), "rematch": None},
                 "llm": {"fine": m("fine", "report_rate_pair_given_cartel"), "rematch": m("rematch", "report_rate_pair_given_cartel")},
                 "replicated": rep8, "tests": {"rematch_minus_fine": c8}})
    return rows


def fmt(v):
    if v is None:
        return "n/a"
    return f"{v:.3f}" if isinstance(v, float) else str(v)


def render_md(rows: list[dict], runs: dict, model: str | None) -> str:
    n_yes = sum(1 for r in rows if r["replicated"] is True)
    n_scored = sum(1 for r in rows if r["replicated"] is not None)
    out = [f"# Scorecard: {n_yes} of {n_scored} scored Bigoni results replicated ({model or 'all models'})", "",
           "| # | Result | Measure | Human | LLM | Replicated |", "|---|---|---|---|---|---|"]
    for r in rows:
        hum = ", ".join(f"{LABEL.get(k, k)} {fmt(v)}" for k, v in r["human"].items())
        llm = ", ".join(f"{LABEL.get(k, k)} {fmt(v)}" for k, v in r["llm"].items())
        rep = {True: "yes", False: "no", None: "not scored"}[r["replicated"]]
        out.append(f"| {r['n']} | {r['result']} | {r['measure']} | {hum} | {llm} | {rep} |")
    out += ["", "Runs used:"]
    for reg, run in runs.items():
        s = run["summary"]
        c = s.get("counts", {})
        out.append(f"- {LABEL.get(reg, reg)}: `{s['run_id']}` (model {s['model']}, seed {s['seed']}, pools {s.get('pools')}, "
                   f"pair-periods {run['metrics']['n_pair_periods']}, defaulted {c.get('defaulted', 0)} of {c.get('calls', 0)} calls, "
                   f"refusals {c.get('refusals', 0)})")
    return "\n".join(out) + "\n"


def render_figure(rows: list[dict], path: pathlib.Path, model: str | None) -> None:
    """Figure 1: one row per Bigoni result, one column per regime, each cell 'human / LLM'."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    n_yes = sum(1 for r in rows if r["replicated"] is True)
    n_scored = sum(1 for r in rows if r["replicated"] is not None)
    cols = ["#", "Bigoni result (measure)", "Laissez-faire", "Fine", "Leniency", "Reward", "Extra arm", "Replicated"]
    widths = [0.03, 0.25, 0.11, 0.11, 0.11, 0.11, 0.19, 0.09]
    xs = [sum(widths[:i]) for i in range(len(widths))]
    row_h = 0.075
    fig, ax = plt.subplots(figsize=(12, 7.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    top = 0.97
    ax.text(0, top + 0.015, f"Figure 1. Scorecard: {n_yes} of {n_scored} scored Bigoni results replicated by {model or 'the model'}",
            fontsize=12, weight="bold", va="bottom")
    y = top - 0.06
    for x, w, c in zip(xs, widths, cols):
        ax.add_patch(Rectangle((x, y - 0.04), w, 0.04, facecolor="#e9e9e9", edgecolor="#999999", linewidth=0.6))
        ax.text(x + 0.005, y - 0.02, c, fontsize=8.5, weight="bold", va="center")
    y -= 0.04
    ax.text(xs[2], y - 0.012, "cell: humans 2009 / LLM", fontsize=7, color="#555555", va="top")
    y -= 0.025
    for r in rows:
        h = row_h * 0.85
        color = {True: "#cfe8cf", False: "#f3cccc", None: "#e6e6e6"}[r["replicated"]]
        for x, w in zip(xs, widths):
            ax.add_patch(Rectangle((x, y - h), w, h, facecolor="white", edgecolor="#999999", linewidth=0.6))
        ax.add_patch(Rectangle((xs[7], y - h), widths[7], h, facecolor=color, edgecolor="#999999", linewidth=0.6))
        ax.text(xs[0] + 0.005, y - h / 2, str(r["n"]), fontsize=9, va="center")
        ax.text(xs[1] + 0.005, y - h / 2, f"{r['result']}\n({r['measure']})", fontsize=8, va="center")
        for k, reg in enumerate(["laissez_faire", "fine", "leniency", "reward"]):
            hv, lv = r["human"].get(reg), r["llm"].get(reg)
            if hv is None and lv is None:
                txt = "."
            else:
                txt = f"{fmt(hv)} / {fmt(lv)}"
            ax.text(xs[2 + k] + 0.005, y - h / 2, txt, fontsize=8, va="center")
        extra = [k for k in r["llm"] if k not in ("laissez_faire", "fine", "leniency", "reward")]
        if extra:
            k = extra[0]
            ax.text(xs[6] + 0.005, y - h / 2, f"{LABEL.get(k, k)}: {fmt(r['human'].get(k))} / {fmt(r['llm'].get(k))}", fontsize=8, va="center")
        else:
            ax.text(xs[6] + 0.005, y - h / 2, ".", fontsize=8, va="center")
        ax.text(xs[7] + 0.005, y - h / 2, {True: "yes", False: "no", None: "not scored"}[r["replicated"]], fontsize=9, va="center")
        y -= row_h
    ax.text(0, y - 0.01, "Human values: Bigoni, Fridolfsson, Le Coq and Spagnolo (2009), Tables 4 and 5; 'n/a' = not yet transcribed. "
            "LLM values: this harness, rules in PREREGISTRATION.md.", fontsize=7, color="#555555", va="top")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Scorecard x of 8 and Figure 1.")
    ap.add_argument("--runs-dir", type=pathlib.Path, default=EVIDENCE_DIR / "runs")
    ap.add_argument("--run", action="append", type=pathlib.Path, default=[], help="explicit run directory (repeatable)")
    ap.add_argument("--model", default=None, help="model id to select runs")
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--out", type=pathlib.Path, default=EVIDENCE_DIR / "scorecard")
    args = ap.parse_args(argv)
    if args.run:
        runs = {}
        for d in args.run:
            r = load_run(d)
            runs[r["summary"]["regime"]] = r
    else:
        runs = pick_runs(args.runs_dir, args.model)
    if not runs:
        print("no runs found")
        return 1
    rows = evaluate(runs, args.n_boot)
    args.out.mkdir(parents=True, exist_ok=True)
    header = evidence_header("python3 -m cartelbench.scorecard " + " ".join(argv or []))
    write_json(args.out / "scorecard.json", {**header, "model": args.model, "rows": rows,
                                              "runs": {k: v["summary"]["run_id"] for k, v in runs.items()},
                                              "metrics": {k: v["metrics"] for k, v in runs.items()}})
    md = render_md(rows, runs, args.model)
    (args.out / "scorecard.md").write_text(f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->\n" + md)
    render_figure(rows, args.out / "figure1_scorecard.png", args.model)
    print(md)
    print(f"wrote {args.out}/scorecard.json, scorecard.md, figure1_scorecard.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
