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

from .analyze import agent_rows, cluster_key, load_human, metrics_from_rows
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
    ck = cluster_key(rows)
    clusters = defaultdict(list)
    for x in rows:
        clusters[x[ck]].append(x)
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


def human_span(key: str) -> float:
    """Stockholm-versus-Rome span for a measure (Table 8 of the paper); 0 until transcribed."""
    spans = load_human().get("city_span", {}) or {}
    return float(spans.get(key, 0.0) or 0.0)


def greater(a, b, key, runs, n_boot) -> tuple[bool | None, dict | None]:
    """True if metric(a) > metric(b) with an interval excluding zero and a gap beyond the human city span."""
    ci = diff_ci(runs.get(a), runs.get(b), key, n_boot)
    if ci is None or ci["point"] is None:
        return None, ci
    span = human_span(key)
    ci["span_required"] = span
    return (ci["lo"] > span), ci


def evaluate(runs: dict[str, dict], n_boot: int = 1000) -> list[dict]:
    """Scorecard rows per Results 1 to 8 of the paper (rules in PREREGISTRATION.md, amendment 2)."""
    human = load_human().get("regimes", {})
    rows = []

    def m(reg, key):
        r = runs.get(reg)
        return None if r is None else r["metrics"].get(key)

    def h(reg, key):
        return (human.get(reg) or {}).get(key)

    def both(x, y):
        return None if x is None or y is None else (x and y)

    # 1 deterrence (Result 1): cartel formation L-Faire > Fine > Leniency
    g1a, c1a = greater("laissez_faire", "fine", "cartel_formation_rate", runs, n_boot)
    g1b, c1b = greater("fine", "leniency", "cartel_formation_rate", runs, n_boot)
    rows.append({"n": 1, "result": "Cartel deterrence", "measure": "cartel_formation_rate",
                 "human": {r: h(r, "cartel_formation_rate") for r in CORE}, "llm": {r: m(r, "cartel_formation_rate") for r in CORE},
                 "replicated": both(g1a, g1b), "tests": {"lf_minus_fine": c1a, "fine_minus_leniency": c1b}})
    # 2 detection (Result 2): reports given cartel Leniency > Fine
    g2, c2 = greater("leniency", "fine", "report_rate_given_cartel", runs, n_boot)
    rows.append({"n": 2, "result": "Cartel detection through reports", "measure": "report_rate_given_cartel",
                 "human": {r: h(r, "report_rate_given_cartel") for r in CORE[1:]}, "llm": {r: m(r, "report_rate_given_cartel") for r in CORE[1:]},
                 "replicated": g2, "tests": {"leniency_minus_fine": c2}})
    # 3 recidivism (Result 3): immediate re-formation after conviction Fine > Leniency
    g3, c3 = greater("fine", "leniency", "relapse_rate_next_period", runs, n_boot)
    rows.append({"n": 3, "result": "Cartel recidivism", "measure": "relapse_rate_next_period",
                 "human": {"fine": 0.40, "leniency": None, "reward": None}, "llm": {r: m(r, "relapse_rate_next_period") for r in CORE[1:]},
                 "replicated": g3, "tests": {"fine_minus_leniency": c3}})
    # 4 average prices (Result 4): Fine > L-Faire; Leniency about L-Faire (reported, not scored)
    g4, c4 = greater("fine", "laissez_faire", "avg_price", runs, n_boot)
    c4b = diff_ci(runs.get("leniency"), runs.get("laissez_faire"), "avg_price", n_boot)
    rows.append({"n": 4, "result": "Average prices", "measure": "avg_price",
                 "human": {r: h(r, "avg_price") for r in CORE}, "llm": {r: m(r, "avg_price") for r in CORE},
                 "replicated": g4, "tests": {"fine_minus_lf": c4, "leniency_minus_lf_reported_only": c4b}})
    # 5 cartel prices (Result 5): Fine > L-Faire and Leniency > L-Faire
    g5a, c5a = greater("fine", "laissez_faire", "cartel_price", runs, n_boot)
    g5b, c5b = greater("leniency", "laissez_faire", "cartel_price", runs, n_boot)
    rows.append({"n": 5, "result": "Cartel prices", "measure": "cartel_price",
                 "human": {r: h(r, "cartel_price") for r in CORE}, "llm": {r: m(r, "cartel_price") for r in CORE},
                 "replicated": both(g5a, g5b), "tests": {"fine_minus_lf": c5a, "leniency_minus_lf": c5b}})
    # 6 deviations (Result 6): Fine < L-Faire and Leniency < L-Faire
    g6a, c6a = greater("laissez_faire", "fine", "deviation_rate", runs, n_boot)
    g6b, c6b = greater("laissez_faire", "leniency", "deviation_rate", runs, n_boot)
    rows.append({"n": 6, "result": "Price deviations", "measure": "deviation_rate",
                 "human": {r: h(r, "deviation_rate") for r in CORE}, "llm": {r: m(r, "deviation_rate") for r in CORE},
                 "replicated": both(g6a, g6b), "tests": {"lf_minus_fine": c6a, "lf_minus_leniency": c6b}})
    # 7 public reports as punishment (Result 7): cartel price Fine > NoReport
    g7, c7 = greater("fine", "noreport", "cartel_price", runs, n_boot)
    rows.append({"n": 7, "result": "Public reports as punishment", "measure": "cartel_price",
                 "human": {"fine": h("fine_rome", "cartel_price"), "noreport": h("noreport", "cartel_price")},
                 "llm": {"fine": m("fine", "cartel_price"), "noreport": m("noreport", "cartel_price")},
                 "replicated": g7, "tests": {"fine_minus_noreport": c7}})
    # 8 altruistic punishment (Result 8): public reports given only the rival deviated, ReMatch > 0 and not below Fine
    key8 = "public_report_rate_given_only_rival_deviated"
    rm = runs.get("rematch")
    c8 = diff_ci(rm, runs.get("fine"), key8, n_boot) if rm else None
    rep8 = None
    if rm is not None and rm["metrics"].get(key8) is not None:
        rep8 = rm["metrics"][key8] > 0 and (c8 is None or c8["hi"] >= 0)
    rows.append({"n": 8, "result": "Public reports as altruistic punishment", "measure": key8,
                 "human": {"fine": h("fine_rome", key8), "rematch": h("rematch", key8)},
                 "llm": {"fine": m("fine", key8), "rematch": m("rematch", key8)},
                 "replicated": rep8, "tests": {"rematch_minus_fine": c8}})
    return rows


def fmt(v):
    if v is None:
        return "n/a"
    return f"{v:.3f}" if isinstance(v, float) else str(v)


CAPTION = ("Rule (pre-registered): a result counts as reproduced when the LLM shows the same direction as the humans and the "
           "95 percent cluster-bootstrap interval of the regime difference (clusters: independent pool sessions) excludes zero "
           "and, where the Stockholm-versus-Rome span of the measure is known, exceeds that span. Three states: reproduced, "
           "not reproduced, not tested (arm not run). Denominator: results tested.")


def render_md(rows: list[dict], runs: dict, model: str | None) -> str:
    n_yes = sum(1 for r in rows if r["replicated"] is True)
    n_scored = sum(1 for r in rows if r["replicated"] is not None)
    out = [f"# Scorecard: {n_yes} of {n_scored} tested Bigoni results reproduced ({model or 'all models'})", "", CAPTION, "",
           "| # | Result | Measure | Human | LLM | Replicated |", "|---|---|---|---|---|---|"]
    for r in rows:
        hum = ", ".join(f"{LABEL.get(k, k)} {fmt(v)}" for k, v in r["human"].items())
        llm = ", ".join(f"{LABEL.get(k, k)} {fmt(v)}" for k, v in r["llm"].items())
        rep = {True: "reproduced", False: "not reproduced", None: "not tested"}[r["replicated"]]
        out.append(f"| {r['n']} | {r['result']} | {r['measure']} | {hum} | {llm} | {rep} |")
    out += ["", "## n-table", "", "| regime | run | model | pool sessions | duopoles | periods per pool | pair-periods | calls | refusals | invalid JSON | errors | defaulted | cost USD |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for reg, run in runs.items():
        s = run["summary"]
        c = s.get("counts", {})
        n = s.get("n_table", {})
        cost = n.get("cost_usd")
        out.append(f"| {LABEL.get(reg, reg)} | `{s['run_id']}` | {s['model']} | {s.get('pools')} | {s.get('duopoles')} | "
                   f"{', '.join(str(v) for v in (s.get('periods_per_pool') or {}).values())} | {run['metrics']['n_pair_periods']} | "
                   f"{c.get('calls', 0)} | {c.get('refusals', 0)} | {c.get('invalid_json', 0)} | {c.get('errors', 0)} | "
                   f"{c.get('defaulted', 0)} | {'n/a' if cost is None else f'{cost:.2f}'} |")
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
    ax.text(0, top + 0.015, f"Figure 1b. Scorecard: {n_yes} of {n_scored} tested Bigoni results reproduced by {model or 'the model'}",
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
        ax.text(xs[7] + 0.005, y - h / 2, {True: "yes", False: "no", None: "not tested"}[r["replicated"]], fontsize=9, va="center")
        y -= row_h
    ax.text(0, y - 0.01, "Human values: Bigoni, Fridolfsson, Le Coq and Spagnolo (IFN WP 738, 2011), Tables 3, 4, 5 and Section 5.2.3; 'n/a' = not reported. "
            "LLM values: this harness, rules in PREREGISTRATION.md.", fontsize=7, color="#555555", va="top")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def render_dotplot(rows: list[dict], runs: dict, path: pathlib.Path, model: str | None, n_boot: int = 300) -> None:
    """Figure 1: one panel per Bigoni result, x = regime, dots = humans (pooled, Stockholm, Rome) and LLM with interval."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from .analyze import cluster_bootstrap

    human = load_human()
    cities = human.get("cities", {})  # optional: {"stockholm": {regime: {measure: v}}, "rome": {...}}
    hkey = {}
    n_yes = sum(1 for r in rows if r["replicated"] is True)
    n_scored = sum(1 for r in rows if r["replicated"] is not None)
    fig, axes = plt.subplots(2, 4, figsize=(14, 6.4))
    for r, ax in zip(rows, axes.flat):
        regs = list(r["llm"].keys())
        xs = list(range(len(regs)))
        hv = [r["human"].get(k) for k in regs]
        lv = [r["llm"].get(k) for k in regs]
        los, his = [], []
        for k in regs:
            run = runs.get(k)
            ci = None
            if run is not None and run["metrics"].get(r["measure"]) is not None:
                ci = cluster_bootstrap(run["rows"], [r["measure"]], n_boot=n_boot).get(r["measure"])
            los.append(None if ci is None else ci["lo"])
            his.append(None if ci is None else ci["hi"])
        for city, marker in (("stockholm", "<"), ("rome", ">")):
            cv = [((cities.get(city) or {}).get(k) or {}).get(r["measure"]) for k in regs]
            if any(v is not None for v in cv):
                ax.scatter([x for x, v in zip(xs, cv) if v is not None], [v for v in cv if v is not None], marker=marker,
                           s=36, color="#7a7a7a", label=city.capitalize(), zorder=3)
        ax.scatter([x for x, v in zip(xs, hv) if v is not None], [v for v in hv if v is not None], marker="o", s=48,
                   facecolors="white", edgecolors="#333333", label="Humans (pooled)", zorder=4)
        for x, v, lo, hi in zip(xs, lv, los, his):
            if v is None:
                continue
            if lo is not None:
                ax.plot([x + 0.15, x + 0.15], [lo, hi], color="#1f5fa8", linewidth=1.5, zorder=2)
            ax.scatter([x + 0.15], [v], marker="s", s=44, color="#1f5fa8", label="LLM" if x == xs[0] else None, zorder=5)
        state = {True: "reproduced", False: "not reproduced", None: "not tested"}[r["replicated"]]
        ax.set_title(f"{r['n']}. {r['result']}\n{state}", fontsize=9, loc="left",
                     color={True: "#2a7a2a", False: "#a83232", None: "#666666"}[r["replicated"]])
        ax.set_xticks(xs)
        ax.set_xticklabels([LABEL.get(k, k) for k in regs], fontsize=7, rotation=20)
        ax.set_ylabel(r["measure"], fontsize=7)
        ax.tick_params(axis="y", labelsize=7)
        ax.grid(axis="y", linewidth=0.3, alpha=0.5)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8, frameon=False)
    fig.suptitle(f"Figure 1. Humans (Bigoni et al. 2011) versus LLM ({model or 'model'}) per Bigoni result: {n_yes} of {n_scored} tested results reproduced. "
                 "Bars: 95 percent cluster-bootstrap intervals over pool sessions.", fontsize=10, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
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
    render_figure(rows, args.out / "figure1b_scorecard_table.png", args.model)
    render_dotplot(rows, runs, args.out / "figure1_dotplot.png", args.model, n_boot=min(300, args.n_boot))
    print(md)
    print(f"wrote {args.out}/scorecard.json, scorecard.md, figure1_dotplot.png, figure1b_scorecard_table.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
