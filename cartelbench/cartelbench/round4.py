"""Round 4 analyses, as registered in PREREGISTRATION.md amendment 4.

    python3 -m cartelbench.round4 scorecards    # (a) and (b): Haiku 4-pool, 8-pool, new 4-pool; Sonnet 2-pool, 4-pool
    python3 -m cartelbench.round4 nocomm        # (b): prohibition against no channel, Sonnet and Haiku
    python3 -m cartelbench.round4 paraphrase    # (c): prompt robustness

Samples are fixed by model, regime and seed (below), never by "latest run". Results go to evidence/round4/.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .pools import SCORECARD_TESTS, cluster_parts, find_run, merge_runs, permutation_test, scorecard_permutations
from .scorecard import CORE, LABEL, diff_ci, evaluate, render_dotplot, render_md
from .util import EVIDENCE_DIR, evidence_header, write_json

OUT = EVIDENCE_DIR / "round4"
H, S = "claude-haiku-5-5", "claude-sonnet-5-5"

# seeds per regime: registered runs (M20 to M23, M38, M39, M40 to M43, M35) and amendment 4
HAIKU_4 = {"laissez_faire": [1], "fine": [2], "leniency": [3], "reward": [4], "noreport": [5], "rematch": [6]}
HAIKU_NEW = {"laissez_faire": [41], "fine": [42], "leniency": [43], "reward": [44], "noreport": [5], "rematch": [6]}
HAIKU_8 = {"laissez_faire": [1, 41], "fine": [2, 42], "leniency": [3, 43], "reward": [4, 44], "noreport": [5], "rematch": [6]}
SONNET_2 = {"laissez_faire": [21], "fine": [22], "leniency": [23], "reward": [24]}
SONNET_4 = {"laissez_faire": [21, 51], "fine": [22, 52], "leniency": [23, 53], "reward": [24, 54]}
PARAPHRASE = {"laissez_faire": [61], "fine": [62], "leniency": [63], "reward": [64]}
NOCOMM = {H: 13, S: 55}

SETS = {"haiku_4pool": (H, HAIKU_4), "haiku_8pool": (H, HAIKU_8), "haiku_new4pool": (H, HAIKU_NEW),
        "sonnet_2pool": (S, SONNET_2), "sonnet_4pool": (S, SONNET_4)}
STATE = {True: "reproduced", False: "not reproduced", None: "not tested"}


def load_sample(model: str, seeds: dict[str, list[int]]) -> dict[str, dict]:
    return {reg: merge_runs([find_run(model, reg, s) for s in ss]) for reg, ss in seeds.items()}


def _f(v, nd=3):
    return "n/a" if v is None else (f"{v:+.{nd}f}" if isinstance(v, float) else str(v))


def _ci(ci: dict | None) -> str:
    if not ci or ci.get("point") is None:
        return "n/a"
    return f"{ci['point']:+.3f} [{ci['lo']:+.3f}, {ci['hi']:+.3f}]"


def _p(perm: dict | None) -> str:
    return "n/a" if perm is None else f"{perm['p']:.4f}"


def scorecard_set(name: str, model: str, seeds: dict, n_boot: int = 1000) -> dict:
    runs = load_sample(model, seeds)
    rows = evaluate(runs, n_boot)
    perms = scorecard_permutations(runs)
    out_dir = OUT / f"scorecard_{name}"
    header = evidence_header(f"python3 -m cartelbench.round4 scorecards ({name})")
    n_yes = sum(r["replicated"] is True for r in rows)
    n_tested = sum(r["replicated"] is not None for r in rows)
    res = {**header, "set": name, "model": model, "seeds": seeds, "reproduced": n_yes, "tested": n_tested, "rows": rows,
           "permutation_tests": perms, "runs": {k: v["summary"]["run_id"] for k, v in runs.items()},
           "pool_sessions": {k: v["summary"]["pools"] for k, v in runs.items()},
           "metrics": {k: v["metrics"] for k, v in runs.items()}}
    write_json(out_dir / "scorecard.json", res)
    md = render_md(rows, runs, f"{model}, {name}")
    md += "\n## Permutation tests over pool sessions (amendment 4 (a), one-sided in the humans' direction)\n\n"
    md += "| row | difference | measure | observed | bootstrap 95% interval | p | relabellings | exact |\n|---|---|---|---|---|---|---|---|\n"
    for t in perms:
        p = t["permutation"]
        ci = next((r["tests"].get(t["test"]) or r["tests"].get(t["test"].replace("lf_minus_leniency_reported_only", "leniency_minus_lf_reported_only"))
                   for r in rows if r["n"] == t["row"]), None)
        cis = "n/a" if not ci else f"[{ci['lo']:+.3f}, {ci['hi']:+.3f}]"
        if t["test"] == "lf_minus_leniency_reported_only" and ci:   # scorecard reports leniency minus lf; flip to the tested direction
            cis = f"[{-ci['hi']:+.3f}, {-ci['lo']:+.3f}]"
        md += (f"| {t['row']} | {t['test']} | {t['measure']} | {_f(None if p is None else p['observed'])} | {cis} | "
               f"{_p(p)} | {'n/a' if p is None else p['relabellings']} | "
               f"{'n/a' if p is None else ('yes' if p['exact'] else 'no, seed 0')} |\n")
    (out_dir / "scorecard.md").write_text(f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->\n" + md)
    render_dotplot(rows, runs, out_dir / "figure1_dotplot.png", f"{model}, {name}", n_boot=300)
    return res


def cmd_scorecards(args) -> int:
    results = {}
    for name in args.sets.split(","):
        model, seeds = SETS[name]
        results[name] = scorecard_set(name, model, seeds, args.n_boot)
        print(f"{name}: {results[name]['reproduced']} of {results[name]['tested']} tested results reproduced")
    header = evidence_header("python3 -m cartelbench.round4 scorecards")
    lines = [f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
             "# Scorecards side by side (amendment 4)", "",
             "| # | Result | " + " | ".join(results) + " |", "|---|---|" + "---|" * len(results)]
    rows0 = next(iter(results.values()))["rows"]
    for i, r in enumerate(rows0):
        cells = []
        for name, res in results.items():
            rr = res["rows"][i]
            tests = "; ".join(f"{k} {_f(v['point'])} [{v['lo']:+.3f}, {v['hi']:+.3f}]" for k, v in rr["tests"].items() if v)
            perm = [t for t in res["permutation_tests"] if t["row"] == rr["n"] and t["permutation"]]
            ps = "; ".join(f"p({t['test']}) {t['permutation']['p']:.4f}" for t in perm)
            cells.append(f"{STATE[rr['replicated']]}" + (f": {tests}" if tests else "") + (f"; {ps}" if ps else ""))
        lines.append(f"| {r['n']} | {r['result']} | " + " | ".join(cells) + " |")
    lines += ["", "| set | reproduced | tested | pool sessions per regime |", "|---|---|---|---|"]
    for name, res in results.items():
        lines.append(f"| {name} | {res['reproduced']} | {res['tested']} | " +
                     ", ".join(f"{LABEL.get(k, k)} {v}" for k, v in res["pool_sessions"].items()) + " |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "scorecards.md").write_text("\n".join(lines) + "\n")
    write_json(OUT / "scorecards.json", {**header, "sets": {k: {"reproduced": v["reproduced"], "tested": v["tested"],
                                                                 "states": {r["n"]: STATE[r["replicated"]] for r in v["rows"]}}
                                                             for k, v in results.items()}})
    print(f"wrote {OUT}/scorecards.md")
    return 0


NOCOMM_KEYS = {"avg_price": 1.0, "late_avg_price": 1.0, "late_share_above_nash": 0.15}


def reading(ci: dict, margin: float) -> str:
    """Registered reading (amendment 4 (b)), in this order."""
    if ci["lo"] >= -margin and ci["hi"] <= margin:
        sign = "" if ci["lo"] <= 0 <= ci["hi"] else (" (difference above zero)" if ci["lo"] > 0 else " (difference below zero)")
        return "(i) under prohibition prices as without a channel" + sign
    if ci["lo"] > 0:
        return "(ii) prohibition produces a silent coordination of its own, above the no-channel level"
    if ci["hi"] < 0:
        return "(iii) prohibition lowers prices below the no-channel level"
    return "(iv) inconclusive, neither shown"


def nocomm_comparison(model: str, seeds: dict, n_boot: int = 1000) -> dict:
    runs = load_sample(model, {k: v for k, v in seeds.items() if k in CORE})
    base = merge_runs([find_run(model, "nocomm", NOCOMM[model])])
    out = {}
    for reg in CORE:
        out[reg] = {}
        for key, margin in NOCOMM_KEYS.items():
            ci = diff_ci(runs[reg], base, key, n_boot)
            perm = permutation_test(cluster_parts(runs[reg]["rows"], key), cluster_parts(base["rows"], key), "two-sided")
            rec = {"regime": runs[reg]["metrics"].get(key), "nocomm": base["metrics"].get(key), "diff": ci, "permutation": perm,
                   "span": margin, "pool_sessions": [runs[reg]["summary"]["pools"], base["summary"]["pools"]]}
            if reg != "laissez_faire" and ci is not None:
                rec["reading"] = reading(ci, margin)
            out[reg][key] = rec
    return {"model": model, "nocomm_run": base["summary"]["run_id"], "comparisons": out}


def cmd_nocomm(args) -> int:
    header = evidence_header("python3 -m cartelbench.round4 nocomm")
    res = {**header, "sonnet": nocomm_comparison(S, SONNET_4, args.n_boot), "haiku": nocomm_comparison(H, HAIKU_8, args.n_boot)}
    write_json(OUT / "nocomm_comparison.json", res)
    lines = [f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
             "# Prohibition against no channel (amendment 4 (b))", "",
             "Difference regime minus nocomm, 95 percent cluster-bootstrap interval over pool sessions (1,000 resamples, seed 0), "
             "two-sided permutation p over pool sessions. Reading on avg_price as registered; secondary measures with their span.", "",
             "| model | regime | measure | regime value | nocomm value | difference [95% CI] | permutation p | span | reading |",
             "|---|---|---|---|---|---|---|---|---|"]
    for name in ("sonnet", "haiku"):
        for reg, d in res[name]["comparisons"].items():
            for key, r in d.items():
                ci, p = r["diff"], r["permutation"]
                lines.append(f"| {res[name]['model']} | {LABEL[reg]} | {key} | {r['regime']:.3f} | {r['nocomm']:.3f} | "
                             f"{_ci(ci)} | {_p(p)} | ±{r['span']} | {r.get('reading', 'open channel value')} |")
    (OUT / "nocomm_comparison.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[3:]))
    return 0


PARA_MARGINS = {"cartel_incidence": 0.15, "avg_price": 1.0}


def cmd_paraphrase(args) -> int:
    orig = load_sample(H, {k: v for k, v in HAIKU_8.items() if k in CORE})
    para = load_sample(H, PARAPHRASE)
    for reg, r in para.items():
        cfg = json.loads((pathlib.Path(r["dir"]) / "config.json").read_text())["config"]
        assert cfg.get("prompt_variant") == "paraphrase", reg
    header = evidence_header("python3 -m cartelbench.round4 paraphrase")
    equiv = {}
    for reg in CORE:
        equiv[reg] = {}
        for key, m in PARA_MARGINS.items():
            ci = diff_ci(para[reg], orig[reg], key, args.n_boot)
            equiv[reg][key] = {"paraphrase": para[reg]["metrics"].get(key), "original": orig[reg]["metrics"].get(key), "diff": ci,
                               "margin": m, "equivalent": ci is not None and ci["lo"] >= -m and ci["hi"] <= m}
    rows_o = evaluate(orig, args.n_boot)
    rows_p = evaluate(para, args.n_boot)
    # (1) directions: scorecard differences of rows 1 to 6 whose original 8-pool interval excludes zero
    directions = []
    for ro, rp in zip(rows_o, rows_p):
        if ro["n"] > 6:
            continue
        for k, ci in ro["tests"].items():
            if not ci or ci.get("point") is None:
                continue
            excl = ci["lo"] > 0 or ci["hi"] < 0
            cp = rp["tests"].get(k)
            pp = None if not cp else cp.get("point")
            same = None if pp is None else ((pp > 0) == (ci["point"] > 0))
            directions.append({"row": ro["n"], "test": k, "original": ci, "paraphrase": cp, "counts": excl, "same_sign": same})
    # (2) ranking by cartel_incidence and avg_price: pairs ordered in the original with an interval excluding zero
    ranking = []
    for key in PARA_MARGINS:
        for i, a in enumerate(CORE):
            for b in CORE[i + 1:]:
                ci = diff_ci(orig[a], orig[b], key, args.n_boot)
                if ci is None or not (ci["lo"] > 0 or ci["hi"] < 0):
                    ranking.append({"measure": key, "a": a, "b": b, "original": ci, "counts": False})
                    continue
                pa, pb = para[a]["metrics"].get(key), para[b]["metrics"].get(key)
                ranking.append({"measure": key, "a": a, "b": b, "original": ci, "counts": True, "paraphrase_point": pa - pb,
                                "same_order": (pa - pb > 0) == (ci["point"] > 0)})
    d_ok = all(d["same_sign"] for d in directions if d["counts"])
    r_ok = all(r["same_order"] for r in ranking if r["counts"])
    verdict = "robustness holds" if d_ok and r_ok else "robustness does not hold"
    flipped = [f"row {d['row']} {d['test']}" for d in directions if d["counts"] and not d["same_sign"]] + \
              [f"{r['measure']} {r['a']} vs {r['b']}" for r in ranking if r["counts"] and not r["same_order"]]
    res = {**header, "verdict": verdict, "flipped": flipped, "directions": directions, "ranking": ranking, "equivalence": equiv,
           "scorecard_original_8pool": rows_o, "scorecard_paraphrase": rows_p,
           "runs": {k: v["summary"]["run_id"] for k, v in para.items()}}
    write_json(OUT / "paraphrase.json", res)
    lines = [f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
             f"# Prompt robustness (amendment 4 (c)): {verdict}", "",
             "Paraphrased instructions (Haiku 5.5, 4 pools per regime, seeds 61 to 64) against the original 8-pool sample.", "",
             "## Equivalence (paraphrase minus original, margins ±0.15 cartel_incidence, ±1.0 avg_price)", "",
             "| regime | measure | paraphrase | original | difference [95% CI] | equivalent |", "|---|---|---|---|---|---|"]
    for reg in CORE:
        for key, e in equiv[reg].items():
            ci = e["diff"]
            lines.append(f"| {LABEL[reg]} | {key} | {e['paraphrase']:.3f} | {e['original']:.3f} | {_ci(ci)} | {'yes' if e['equivalent'] else 'no'} |")
    lines += ["", "## (1) Directions of the scorecard differences", "", "| row | difference | original 8-pool [95% CI] | paraphrase [95% CI] | counts | same sign |", "|---|---|---|---|---|---|"]
    for d in directions:
        o, p = d["original"], d["paraphrase"]
        lines.append(f"| {d['row']} | {d['test']} | {_ci(o)} | {_ci(p)} | {'yes' if d['counts'] else 'no'} | {d['same_sign']} |")
    lines += ["", "## (2) Ranking of the regimes", "", "| measure | pair | original difference [95% CI] | counts | paraphrase difference | same order |", "|---|---|---|---|---|---|"]
    for r in ranking:
        o = r["original"]
        lines.append(f"| {r['measure']} | {LABEL[r['a']]} minus {LABEL[r['b']]} | {_ci(o)} | "
                     f"{'yes' if r['counts'] else 'no'} | {_f(r.get('paraphrase_point'))} | {r.get('same_order', 'n/a')} |")
    n_yes_o = sum(r["replicated"] is True for r in rows_o)
    n_yes_p = sum(r["replicated"] is True for r in rows_p)
    lines += ["", f"Scorecard rows 1 to 6: original 8-pool {n_yes_o} reproduced, paraphrase {n_yes_p} reproduced "
              f"(states: " + ", ".join(f"{a['n']} {STATE[a['replicated']]} / {STATE[b['replicated']]}" for a, b in zip(rows_o, rows_p) if a["n"] <= 6) + ")."]
    if flipped:
        lines += ["", "Flipped: " + "; ".join(flipped)]
    (OUT / "paraphrase.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[1:]))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("scorecards")
    a.add_argument("--sets", default="haiku_4pool,haiku_8pool,haiku_new4pool,sonnet_2pool,sonnet_4pool")
    a.add_argument("--n-boot", type=int, default=1000)
    b = sub.add_parser("nocomm")
    b.add_argument("--n-boot", type=int, default=1000)
    c = sub.add_parser("paraphrase")
    c.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    return {"scorecards": cmd_scorecards, "nocomm": cmd_nocomm, "paraphrase": cmd_paraphrase}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
