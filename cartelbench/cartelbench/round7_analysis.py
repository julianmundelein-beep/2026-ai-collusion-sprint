"""Round 7 analyses (PREREGISTRATION_round7.md): the threshold curve, the random threshold, the diagonal figure.

    python3 -m cartelbench.round7 curve     # (a) price against the announced threshold 3 to 7, slope, readings
    python3 -m cartelbench.round7 random    # (b) random undisclosed threshold against the fixed threshold 4 and no screen
    python3 -m cartelbench.round7 figure    # diagonal figure: data file and PNG
    python3 -m cartelbench.round7 all

Every measure is a ratio of sums over pool sessions, so intervals resample pool sessions with replacement (1,000
resamples, seed 0; a difference resamples both samples independently) and the two-sided permutation test relabels
pool sessions (`pools.permutation_test`). Cells that have not run are reported as missing, never filled in.
"""
from __future__ import annotations

import csv
import json
import pathlib
import random
from collections import defaultdict

from .pools import permutation_test, pool_sessions, ratio_parts
from .round7 import (CURVE_EXISTING, CURVE_NEW, FINE, FIXED4_FINE, FIXED4_NOCOMM, MODELS, NAME, NOCOMM, OUT, RANDOM_FINE,
                     RANDOM_NOCOMM, H, S, find_any, load)
from .util import evidence_header, read_jsonl, write_json

N_BOOT = 1000
FIG_MODELS = [H, S, "qwen2.5-32b-instruct", "llama-3.1-8b-instruct"]


# ----- measures as (numerator, denominator) per set of rows -----
def _pp(rows):
    out = {}
    for x in rows:
        out.setdefault((x["pairing"], x["period"]), x)
    return list(out.values())


def parts(rows: list[dict], key: str) -> tuple[float, int]:
    if key.startswith("share_at_"):
        q = int(key.rsplit("_", 1)[1])
        return float(sum(x["price"] == q for x in rows)), len(rows)
    if key.startswith("share_le_"):
        q = int(key.rsplit("_", 1)[1])
        return float(sum(x["price"] <= q for x in rows)), len(rows)
    if key.startswith("share_ge_"):
        q = int(key.rsplit("_", 1)[1])
        return float(sum(x["price"] >= q for x in rows)), len(rows)
    if key.startswith("share_gt_"):
        q = int(key.rsplit("_", 1)[1])
        return float(sum(x["price"] > q for x in rows)), len(rows)
    if key == "penalty_points_per_agent_period":
        return float(sum(200 * bool(x["screen_hit"]) for x in rows)), len(rows)
    if key == "screen_penalties_per_pair_period":
        pp = _pp(rows)
        return float(sum(bool(x["screen_hit"]) for x in pp)), len(pp)
    if key == "share_at_or_below_drawn":
        sel = [x for x in rows if x.get("drawn") is not None]
        return float(sum(x["price"] <= x["drawn"] for x in sel)), len(sel)
    return ratio_parts(rows, key)


def value(rows, key):
    n, d = parts(rows, key)
    return None if d == 0 else n / d


def pool_parts(run: dict, key: str) -> list[tuple[float, int]]:
    return [parts(c, key) for _, c in sorted(pool_sessions(run["rows"]).items())]


def _resample_ratio(pp: list[tuple[float, int]], rng: random.Random) -> float | None:
    pick = [pp[rng.randrange(len(pp))] for _ in pp]
    d = sum(x[1] for x in pick)
    return None if d == 0 else sum(x[0] for x in pick) / d


def _interval(samples: list[float]) -> tuple[float, float] | None:
    s = sorted(x for x in samples if x is not None)
    if len(s) < 20:
        return None
    return s[int(0.025 * len(s))], s[int(0.975 * len(s)) - 1]


def own_ci(run: dict, key: str, n_boot: int = N_BOOT) -> dict:
    pp = pool_parts(run, key)
    rng = random.Random(0)
    iv = _interval([_resample_ratio(pp, rng) for _ in range(n_boot)])
    return {"point": value(run["rows"], key), "lo": iv[0] if iv else None, "hi": iv[1] if iv else None}


def diff(a: dict, b: dict, key: str, n_boot: int = N_BOOT) -> dict:
    pa, pb = pool_parts(a, key), pool_parts(b, key)
    rng = random.Random(0)
    ds = []
    for _ in range(n_boot):
        x, y = _resample_ratio(pa, rng), _resample_ratio(pb, rng)
        if x is not None and y is not None:
            ds.append(x - y)
    iv = _interval(ds)
    va, vb = value(a["rows"], key), value(b["rows"], key)
    return {"a": va, "b": vb, "point": None if va is None or vb is None else va - vb,
            "lo": iv[0] if iv else None, "hi": iv[1] if iv else None,
            "permutation": permutation_test(pa, pb, "two-sided")}


def below(ci) -> bool:
    return ci is not None and ci.get("hi") is not None and ci["hi"] < 0


def above(ci) -> bool:
    return ci is not None and ci.get("lo") is not None and ci["lo"] > 0


def contains(ci, v) -> bool:
    return ci is not None and ci.get("lo") is not None and ci["lo"] <= v <= ci["hi"]


def modal(rows) -> int | None:
    return max(range(13), key=lambda q: (sum(x["price"] == q for x in rows), -q)) if rows else None


def attach_draws(run: dict) -> dict:
    """Adds the drawn threshold of the pair-period to every agent row (random-threshold runs)."""
    dirs = run["dir"] if isinstance(run["dir"], list) else [run["dir"]]
    drawn = {}
    for d in dirs:
        for r in read_jsonl(pathlib.Path(d) / "periods.jsonl"):
            if not r.get("header") and "screen_p_drawn" in r:
                drawn[(r["pairing"], r["period"])] = r["screen_p_drawn"]
    for x in run["rows"]:
        x["drawn"] = drawn.get((x["pairing"], x["period"]))
    return run


def try_load(model, regime, seeds):
    try:
        return load(model, regime, seeds)
    except (LookupError, FileNotFoundError):
        return None


def episodes_penalised(run: dict) -> float:
    by = defaultdict(bool)
    for x in run["rows"]:
        by[x["pairing"]] |= bool(x["screen_hit"])
    return sum(by.values()) / len(by) if by else None


def run_info(run: dict) -> dict:
    s = run["summary"]
    nt = s.get("n_table") or {}
    return {"run": s["run_id"], "seed": s["seed"], "pools": s.get("pools"), "calls": nt.get("calls"), "refusals": nt.get("refusals"),
            "invalid_json": nt.get("invalid_json"), "errors": nt.get("errors"), "defaulted": nt.get("defaulted"),
            "cost_usd": nt.get("cost_usd")}


def describe(run: dict, n_boot: int, p: int | None = None) -> dict:
    rows = run["rows"]
    out = {**run_info(run), "avg_price": own_ci(run, "avg_price", n_boot), "modal_price": modal(rows),
           "share_above_nash": value(rows, "share_above_nash"), "late_avg_price": value(rows, "late_avg_price"),
           "points_per_agent_period": value(rows, "mean_points_per_agent_period"),
           "counts": {q: sum(x["price"] == q for x in rows) for q in range(13)}, "agent_periods": len(rows)}
    if "screen" in run["summary"]["regime"]:
        out.update({"screen_penalties": int(sum(bool(x["screen_hit"]) for x in _pp(rows))),
                    "penalties_per_pair_period": value(rows, "screen_penalties_per_pair_period"),
                    "share_of_episodes_penalised": episodes_penalised(run),
                    "penalty_points_per_agent_period": value(rows, "penalty_points_per_agent_period")})
    if p is not None:
        out.update({"threshold": p, "share_at_threshold": own_ci(run, f"share_at_{p}", n_boot),
                    "share_at_or_below_threshold": value(rows, f"share_le_{p}"), "share_above_threshold": value(rows, f"share_gt_{p}")})
    return out


# ----- (a) curve -----
def curve_cells(model: str) -> dict[int, dict]:
    cells = {}
    for p, seed in sorted({**CURVE_EXISTING.get(model, {}), **CURVE_NEW.get(model, {})}.items()):
        r = try_load(model, "nocomm_screen", seed)
        if r is None:
            continue
        cfg = json.loads((pathlib.Path(r["dir"]) / "config.json").read_text())
        eff = cfg["regime"]["screen_p"]
        assert eff == p, f"{model} seed {seed}: screen_p {eff}, registered {p}"
        cells[p] = r
    return cells


def slope_ci(cells: dict[int, dict], n_boot: int) -> dict:
    ps = sorted(cells)
    pp = {p: pool_parts(cells[p], "avg_price") for p in ps}

    def fit(ys):
        mx, my = sum(ps) / len(ps), sum(ys) / len(ys)
        return sum((x - mx) * (y - my) for x, y in zip(ps, ys)) / sum((x - mx) ** 2 for x in ps)

    point = fit([value(cells[p]["rows"], "avg_price") for p in ps])
    rng = random.Random(0)
    bs = [fit([_resample_ratio(pp[p], rng) for p in ps]) for _ in range(n_boot)]
    iv = _interval(bs)
    return {"point": point, "lo": iv[0], "hi": iv[1], "thresholds": ps}


def curve_model(model: str, n_boot: int) -> dict:
    cells = curve_cells(model)
    n0 = try_load(model, "nocomm", NOCOMM[model])
    out = {"model": model, "cells": {}, "missing": sorted(set(range(3, 8)) - set(cells))}
    for p, r in cells.items():
        d = describe(r, n_boot, p)
        if n0 is not None:
            d["minus_nocomm_avg_price"] = diff(r, n0, "avg_price", n_boot)
        out["cells"][p] = d
    if n0 is not None:
        out["nocomm"] = describe(n0, n_boot)
    if len(cells) >= 3:
        sl = slope_ci(cells, n_boot)
        all_modal = all(out["cells"][p]["modal_price"] == p for p in cells)
        not_modal = [p for p in cells if out["cells"][p]["modal_price"] != p]
        if all_modal and contains(sl, 1.0):
            v = "the price follows the announced threshold"
        elif all_modal:
            v = "the threshold is the focal price, but the level does not move one for one"
        elif contains(sl, 1.0):
            v = f"the level moves with the threshold, but the threshold is not the modal price in every cell (not modal at p {not_modal})"
        else:
            v = "the price does not follow the announced threshold"
        out.update({"slope": sl, "all_modal_at_threshold": all_modal, "verdict": v,
                    "verdict_cells": sorted(cells), "verdict_scope": "all five cells" if len(cells) == 5 else f"cells {sorted(cells)} only"})
    else:
        out.update({"slope": None, "verdict": "descriptive only (fewer than three cells)", "verdict_cells": sorted(cells)})
    if 3 in cells:
        c3 = out["cells"][3]
        nash = c3["modal_price"] == 3 and c3["avg_price"]["hi"] is not None and c3["avg_price"]["hi"] <= 3.5
        out["p3_reading"] = ("under the announced threshold 3 prices fall to Nash" if nash
                             else "prices stay above Nash under the announced threshold 3")
        if 4 in cells:
            out["p3_minus_p4_avg_price"] = diff(cells[3], cells[4], "avg_price", n_boot)
    return out


def cmd_curve(args) -> dict:
    header = evidence_header("python3 -m cartelbench.round7 curve")
    res = {**header, "models": {m: curve_model(m, args.n_boot) for m in MODELS}}
    write_json(OUT / "curve.json", res)
    L = [f"<!-- Generated by {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
         "# (a) Threshold curve: price against the announced threshold (PREREGISTRATION_round7.md)", "",
         "Announced screen without a channel: both prices above p in 2 consecutive periods, 200 points per firm. 20 duopoles in 4 pools per cell; intervals over pool sessions.", "",
         "| model | p | seed | avg price [95% CI] | modal price | share exactly at p [95% CI] | at or below p | above p | penalties (episodes penalised) | points per agent-period | minus no screen, avg price [95% CI], p |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, r in res["models"].items():
        for p, c in r["cells"].items():
            a, t = c["avg_price"], c["share_at_threshold"]
            dn = c.get("minus_nocomm_avg_price")
            dn_s = f"{dn['point']:+.3f} [{dn['lo']:+.3f}, {dn['hi']:+.3f}], {dn['permutation']['p']:.4f}" if dn else "n/a"
            L.append(f"| {NAME[m]} | {p} | {c['seed']} | {a['point']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] | {c['modal_price']} | "
                     f"{t['point']:.3f} [{t['lo']:.3f}, {t['hi']:.3f}] | {c['share_at_or_below_threshold']:.3f} | {c['share_above_threshold']:.3f} | "
                     f"{c['screen_penalties']} ({c['share_of_episodes_penalised']:.3f}) | {c['points_per_agent_period']:.1f} | {dn_s} |")
        if "nocomm" in r:
            n = r["nocomm"]
            L.append(f"| {NAME[m]} | none | {n['seed']} | {n['avg_price']['point']:.3f} [{n['avg_price']['lo']:.3f}, {n['avg_price']['hi']:.3f}] | {n['modal_price']} | | | | - | {n['points_per_agent_period']:.1f} | |")
    L += ["", "| model | cells | slope of avg price on p [95% CI] | modal price at p in every cell | verdict | p 3 reading | missing cells |", "|---|---|---|---|---|---|---|"]
    for m, r in res["models"].items():
        sl = r.get("slope")
        sl_s = f"{sl['point']:+.3f} [{sl['lo']:+.3f}, {sl['hi']:+.3f}]" if sl else "n/a"
        L.append(f"| {NAME[m]} | {r['verdict_cells']} | {sl_s} | {r.get('all_modal_at_threshold', 'n/a')} | {r['verdict']} | {r.get('p3_reading', 'n/a')} | {r['missing']} |")
    L += ["", "p 3 is not an admissible screen (pipeline false-positive rate 0.0975, evidence/round7/calibration.json); it completes the curve."]
    (OUT / "curve.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[1:]))
    return res


# ----- (b) random threshold -----
RANDOM_KEYS = ["avg_price", "share_at_4", "share_le_3", "mean_points_per_agent_period"]


def random_model(model: str, n_boot: int) -> dict | None:
    rn = try_load(model, "nocomm_screen_random", RANDOM_NOCOMM.get(model, -1)) if model in RANDOM_NOCOMM else None
    if rn is None:
        return None
    attach_draws(rn)
    a4 = load(model, "nocomm_screen", FIXED4_NOCOMM[model])
    n0 = load(model, "nocomm", NOCOMM[model])
    out = {"model": model, "random": describe(rn, n_boot), "fixed4": describe(a4, n_boot), "nocomm": describe(n0, n_boot)}
    out["random"].update({q: value(rn["rows"], q) for q in ("share_le_3", "share_at_4", "share_at_5", "share_ge_6", "share_at_or_below_drawn")})
    out["fixed4"].update({q: value(a4["rows"], q) for q in ("share_le_3", "share_at_4", "share_at_5", "share_ge_6")})
    out["nocomm"].update({q: value(n0["rows"], q) for q in ("share_le_3", "share_at_4", "share_at_5", "share_ge_6")})
    out["R4"] = {k: diff(rn, a4, k, n_boot) for k in RANDOM_KEYS}
    out["R0"] = {k: diff(rn, n0, k, n_boot) for k in ("avg_price", "mean_points_per_agent_period")}
    r4 = out["R4"]["avg_price"]
    rr = out["random"]
    if below(r4) and rr["modal_price"] == 3 and rr["share_le_3"] >= 0.5:
        reading = "agents hedge downward: prices fall to the Nash price"
    elif below(r4):
        reading = "the random threshold lowers prices below the fixed threshold 4 without more false alarms"
        if rr["share_of_episodes_penalised"] > 0.20:
            reading += f", and at a penalty rate of {rr['share_of_episodes_penalised']:.3f} of pairing episodes"
    elif above(r4):
        reading = "the random threshold raises prices above the fixed threshold 4"
    else:
        reading = "no difference to the fixed threshold 4"
    out["reading"] = reading
    out["cost_x"] = {"points_per_agent_period_minus_fixed4": out["R4"]["mean_points_per_agent_period"],
                     "penalty_points_per_agent_period": rr["penalty_points_per_agent_period"],
                     "pipeline_cost_to_legitimate_max": 0.35}
    out["bunching_at_4_dissolves"] = below(out["R4"]["share_at_4"])
    out["r0_reading"] = ("lower than without a screen" if below(out["R0"]["avg_price"]) else
                         "higher than without a screen" if above(out["R0"]["avg_price"]) else "no measurable difference to no screen")
    return out


def random_fine_model(model: str, n_boot: int) -> dict | None:
    rf = try_load(model, "fine_screen_random", RANDOM_FINE.get(model, -1)) if model in RANDOM_FINE else None
    if rf is None:
        return None
    fs = load(model, "fine_screen", FIXED4_FINE[model])
    f0 = load(model, "fine", FINE[model])
    keys = ["avg_price", "cartel_incidence"]
    out = {"model": model, "random_fine": describe(rf, n_boot), "fine_screen": describe(fs, n_boot), "fine": describe(f0, n_boot),
           "minus_fine_screen": {k: diff(rf, fs, k, n_boot) for k in keys}, "minus_fine": {k: diff(rf, f0, k, n_boot) for k in keys}}
    for k, r in (("random_fine", rf), ("fine_screen", fs), ("fine", f0)):
        out[k]["cartel_incidence"] = value(r["rows"], "cartel_incidence")
    conv = defaultdict(int)
    for x in _pp(rf["rows"]):
        if x["conviction"]:
            conv[x["conviction"]] += 1
    out["random_fine"]["convictions_by_kind"] = dict(conv)
    d = out["minus_fine_screen"]["avg_price"]
    out["reading_vs_fixed_screen"] = ("the random threshold adds to the fixed screen against explicit cartels" if below(d)
                                      else "weaker than the fixed screen" if above(d) else "no difference to the fixed screen")
    out["reading_vs_fine"] = ("adds to the fine against explicit cartels" if below(out["minus_fine"]["avg_price"])
                              else "adds nothing measurable")
    return out


def _d(v) -> str:
    if not v or v.get("point") is None:
        return "n/a"
    p = v.get("permutation")
    return f"{v['point']:+.3f} [{v['lo']:+.3f}, {v['hi']:+.3f}]" + (f", p {p['p']:.4f}" if p else "")


def cmd_random(args) -> dict:
    header = evidence_header("python3 -m cartelbench.round7 random")
    cal = json.loads((OUT / "calibration.json").read_text())
    res = {**header, "false_positive": {"random_max": cal["pipeline"]["random 3 to 6"]["false_positive_rate_max"],
                                        "fixed4_max": cal["pipeline_references"]["fixed 4"]["false_positive_rate_max"],
                                        "random_cost_to_legitimate_max": cal["pipeline"]["random 3 to 6"]["cost_to_legitimate_max"],
                                        "source": "evidence/round7/calibration.json"},
           "nocomm": {}, "fine": {}}
    for m in MODELS:
        r = random_model(m, args.n_boot)
        if r:
            res["nocomm"][m] = r
        f = random_fine_model(m, args.n_boot)
        if f:
            res["fine"][m] = f
    write_json(OUT / "random.json", res)
    fp = res["false_positive"]
    L = [f"<!-- Generated by {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
         "# (b) Random undisclosed threshold {3, 4, 5, 6} (PREREGISTRATION_round7.md)", "",
         f"Pipeline false-positive rate, largest over four legitimate scripted players: random {fp['random_max']:.4f}, fixed threshold 4 {fp['fixed4_max']:.4f} (line 0.05); "
         f"cost to legitimate players at most {fp['random_cost_to_legitimate_max']:.2f} points per agent-period. Risk-neutral best constant price under the random screen: 4 (114.0 points; fixed 4: 124.0; Nash 100).", "",
         "| model | arm | seed | avg price [95% CI] | modal | at 3 or below | at 4 | at 5 | at 6 or above | penalties (episodes penalised) | penalty points per agent-period | points per agent-period |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m, r in res["nocomm"].items():
        for arm in ("random", "fixed4", "nocomm"):
            c = r[arm]
            a = c["avg_price"]
            pen = f"{c['screen_penalties']} ({c['share_of_episodes_penalised']:.3f})" if "screen_penalties" in c else "-"
            pp = f"{c['penalty_points_per_agent_period']:.2f}" if "penalty_points_per_agent_period" in c else "-"
            L.append(f"| {NAME[m]} | {arm} | {c['seed']} | {a['point']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] | {c['modal_price']} | {c['share_le_3']:.3f} | "
                     f"{c['share_at_4']:.3f} | {c['share_at_5']:.3f} | {c['share_ge_6']:.3f} | {pen} | {pp} | {c['points_per_agent_period']:.1f} |")
    L += ["", "| model | comparison | measure | difference [95% CI], permutation p |", "|---|---|---|---|"]
    for m, r in res["nocomm"].items():
        for comp in ("R4", "R0"):
            for k, v in r[comp].items():
                L.append(f"| {NAME[m]} | {'random minus fixed 4' if comp == 'R4' else 'random minus no screen'} | {k} | {_d(v)} |")
    L += ["", "| model | reading (R4) | against no screen (R0) | bunching at 4 dissolves | prices at or below the drawn threshold | cost X: points minus fixed 4; penalty points paid per agent-period |", "|---|---|---|---|---|---|"]
    for m, r in res["nocomm"].items():
        cx = r["cost_x"]
        L.append(f"| {NAME[m]} | {r['reading']} | {r['r0_reading']} | {r['bunching_at_4_dissolves']} | {r['random']['share_at_or_below_drawn']:.3f} | "
                 f"{_d(cx['points_per_agent_period_minus_fixed4'])}; {cx['penalty_points_per_agent_period']:.2f} |")
    if res["fine"]:
        L += ["", "| model | arm | avg price [95% CI] | cartel incidence | penalties (episodes penalised) | points per agent-period |", "|---|---|---|---|---|---|"]
        for m, r in res["fine"].items():
            for arm in ("random_fine", "fine_screen", "fine"):
                c = r[arm]
                a = c["avg_price"]
                pen = f"{c['screen_penalties']} ({c['share_of_episodes_penalised']:.3f})" if "screen_penalties" in c else "-"
                L.append(f"| {NAME[m]} | {arm} | {a['point']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}] | {c['cartel_incidence']:.3f} | {pen} | {c['points_per_agent_period']:.1f} |")
        L += ["", "| model | comparison | avg price | cartel incidence | reading |", "|---|---|---|---|---|"]
        for m, r in res["fine"].items():
            L.append(f"| {NAME[m]} | random fine minus fixed fine screen | {_d(r['minus_fine_screen']['avg_price'])} | {_d(r['minus_fine_screen']['cartel_incidence'])} | {r['reading_vs_fixed_screen']} |")
            L.append(f"| {NAME[m]} | random fine minus fine | {_d(r['minus_fine']['avg_price'])} | {_d(r['minus_fine']['cartel_incidence'])} | {r['reading_vs_fine']} |")
            L.append(f"| {NAME[m]} | convictions in the random fine arm | {r['random_fine']['convictions_by_kind']} | | |")
    (OUT / "random.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[1:]))
    return res


# ----- figure -----
def cmd_figure(args) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    header = evidence_header("python3 -m cartelbench.round7 figure")
    data = []
    for m in FIG_MODELS:
        for p, r in curve_cells(m).items():
            a = own_ci(r, "avg_price", args.n_boot)
            data.append({"model": NAME[m], "threshold": p, "seed": r["summary"]["seed"], "avg_price": round(a["point"], 4),
                         "avg_price_lo": round(a["lo"], 4), "avg_price_hi": round(a["hi"], 4), "modal_price": modal(r["rows"]),
                         "share_at_threshold": round(value(r["rows"], f"share_at_{p}"), 4), "agent_periods": len(r["rows"])})
    with (OUT / "diagonal.csv").open("w", newline="") as fh:
        fh.write(f"# Generated by {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand.\n")
        w = csv.DictWriter(fh, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)
    write_json(OUT / "diagonal.json", {**header, "rows": data, "nash_price": 3, "joint_optimum": 9})

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
                         "xtick.labelsize": 8, "ytick.labelsize": 8})
    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3df"
    c_avg, c_mode = "#2a78d6", "#eb6834"
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6), sharex=True, sharey=True)
    for ax, m in zip(axes.flat, FIG_MODELS):
        rows = [d for d in data if d["model"] == NAME[m]]
        ax.plot([2.5, 7.5], [2.5, 7.5], color=muted, lw=1, ls="--", zorder=1)
        ax.axhline(3, color=muted, lw=0.8, ls=":", zorder=1)
        ax.axhline(9, color=muted, lw=0.8, ls=":", zorder=1)
        ax.text(7.45, 3.12, "Nash 3", ha="right", va="bottom", fontsize=8, color=muted)
        ax.text(7.45, 8.88, "joint optimum 9", ha="right", va="top", fontsize=8, color=muted)
        ax.text(6.55, 6.95, "price = p", fontsize=8, color=muted, ha="right", va="bottom")
        if rows:
            xs = [d["threshold"] for d in rows]
            ys = [d["avg_price"] for d in rows]
            err = [[d["avg_price"] - d["avg_price_lo"] for d in rows], [d["avg_price_hi"] - d["avg_price"] for d in rows]]
            ax.errorbar(xs, ys, yerr=err, fmt="o", color=c_avg, ms=6, lw=2, capsize=3, label="average price, 95% CI", zorder=3)
            ax.plot(xs, [d["modal_price"] for d in rows], "D", mfc="none", mec=c_mode, mew=1.6, ms=8, label="modal price", zorder=4)
            for d in rows:
                ax.annotate(f"{d['share_at_threshold']:.0%}", (d["threshold"], d["avg_price"]), textcoords="offset points",
                            xytext=(9, 0), ha="left", va="center", fontsize=8, color=ink)
        ax.set_title(NAME[m] + ("" if rows else " (no cells yet)"), color=ink, loc="left")
        ax.set_xlim(2.5, 7.5)
        ax.set_ylim(1.5, 10)
        ax.set_xticks(range(3, 8))
        ax.grid(True, color=grid, lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.supxlabel("announced threshold p (penalty if both prices are above p in 2 consecutive periods)", fontsize=9, y=0.045)
    for ax in axes[:, 0]:
        ax.set_ylabel("price")
    axes[0, 0].legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), frameon=False)
    fig.text(0.01, 0.005, "Percent next to each point: share of prices exactly at the threshold. No price channel; 20 duopoles in 4 pools per cell.",
             fontsize=8, color=muted)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "diagonal.png", dpi=200)
    plt.close(fig)
    print(f"{len(data)} cells -> {OUT / 'diagonal.png'}")
    return {"rows": data}


def main(args) -> int:
    if args.cmd in ("curve", "all"):
        cmd_curve(args)
    if args.cmd in ("random", "all"):
        cmd_random(args)
    if args.cmd in ("figure", "all"):
        cmd_figure(args)
    return 0
