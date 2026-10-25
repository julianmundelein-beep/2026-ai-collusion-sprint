"""Round 6 analyses ("loss and stakes"), as registered in PREREGISTRATION.md amendment 7.

    python3 -m cartelbench.round6 cost        # cost plan before the first call (budget section of amendment 7)
    python3 -m cartelbench.round6 plan        # the launch order with seeds and the stop rule (prints commands)
    python3 -m cartelbench.round6 arms        # (A) every arm against the original instructions, readings
    python3 -m cartelbench.round6 frame       # (B) S2: loss frame minus gain frame, the loss-aversion test
    python3 -m cartelbench.round6 deterrence  # (C) regime effects within each arm against the original
    python3 -m cartelbench.round6 humans      # (D) scorecard per arm and distance to the human values
    python3 -m cartelbench.round6 all

Samples are fixed by model, regime and seed (below), never by "latest run". Results go to evidence/round6/.
"""
from __future__ import annotations

import argparse
import json
import random
import sys

from .analyze import load_human
from .pools import RUNS_DIR, cluster_parts, find_run, merge_runs, permutation_test, scorecard_permutations
from .round5 import _ci, _p, own_ci
from .scorecard import LABEL, diff_ci, evaluate
from .util import EVIDENCE_DIR, evidence_header, write_json

OUT = EVIDENCE_DIR / "round6"
H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
NAME = {H: "Haiku 5.5", S: "Sonnet 5.5"}
REGS = ["laissez_faire", "fine", "leniency"]
ARMS = ["s1_money", "s2_loss", "s2_gain", "s3_exit", "s4_all"]
ARM_LABEL = {"s1_money": "S1 money", "s2_loss": "S2 loss frame", "s2_gain": "S2 gain frame", "s3_exit": "S3 bankruptcy",
             "s4_all": "S4 all together", "s2_loss_b": "S2 loss frame, wording b", "s2_gain_b": "S2 gain frame, wording b"}

# references: the original instructions (amendment 4: Haiku 8 pools, Sonnet 4 pools) and the paraphrase (amendment 4 (c))
BASE = {H: {"laissez_faire": [1, 41], "fine": [2, 42], "leniency": [3, 43]},
        S: {"laissez_faire": [21, 51], "fine": [22, 52], "leniency": [23, 53]}}
PARAPHRASE = {"laissez_faire": 61, "fine": 62, "leniency": 63}

# seeds of amendment 7: (model, arm, regime) -> seed; LAUNCH is the registered order
SEEDS = {}
for _i, _arm in enumerate(["s1_money", "s2_loss", "s2_gain", "s3_exit", "s4_all"]):
    for _j, _reg in enumerate(REGS):
        SEEDS[(H, _arm, _reg)] = 201 + 10 * _i + _j          # 201..203, 211..213, 221..223, 231..233, 241..243
        SEEDS[(S, _arm, _reg)] = 301 + 10 * _i + _j          # 301..303, ...
SEEDS[(H, "s2_loss_b", "fine")] = 252
SEEDS[(H, "s2_gain_b", "fine")] = 262

LAUNCH = (
    # Haiku 5.5: all 15 cells of the design plus the wording control, the loss-aversion test first
    [(H, a, r) for a in ("s2_loss", "s2_gain") for r in ("fine", "leniency", "laissez_faire")]
    + [(H, "s2_loss_b", "fine"), (H, "s2_gain_b", "fine")]
    + [(H, "s4_all", r) for r in ("fine", "leniency", "laissez_faire")]
    + [(H, "s1_money", r) for r in ("fine", "leniency", "laissez_faire")]
    + [(H, "s3_exit", r) for r in ("fine", "leniency", "laissez_faire")]
    # Sonnet 5.5: prohibited regimes only (laissez-faire is at its ceiling, incidence 1.000, and costs twice as much)
    + [(S, "s2_loss", "fine"), (S, "s2_gain", "fine"), (S, "s4_all", "fine"), (S, "s4_all", "leniency"),
       (S, "s2_loss", "leniency"), (S, "s2_gain", "leniency"), (S, "s1_money", "fine"), (S, "s3_exit", "fine")]
)

CAP_USD = 30.0
GROWTH = 1.10          # longer instructions and the account line in every question (expected)
UPPER = 1.5            # upper bound: the largest measured cost per duopoly of the cell times this factor

KEYS = ["cartel_formation_rate", "cartel_incidence", "avg_price", "report_rate_given_cartel", "relapse_rate_next_period"]
SECONDARY = ["comm_attempt_rate", "deviation_rate", "cartel_price", "late_avg_price"]
MARGIN = {"cartel_formation_rate": 0.15, "cartel_incidence": 0.15, "avg_price": 1.0, "report_rate_given_cartel": 0.15,
          "relapse_rate_next_period": 0.15, "comm_attempt_rate": 0.15, "deviation_rate": 0.15, "cartel_price": 1.0,
          "late_avg_price": 1.0}
PRIMARY = {H: "cartel_formation_rate", S: "avg_price"}


def run_command(model: str, arm: str, regime: str) -> str:
    return (f"python3 -m cartelbench.run --regime {regime} --model {model} --duopoles 20 --pools 4 "
            f"--seed {SEEDS[(model, arm, regime)]} --stakes {arm}")


def load(model: str, seeds: list[int], regime: str) -> dict:
    return merge_runs([find_run(model, regime, s) for s in seeds])


def try_arm(model: str, arm: str, regime: str) -> dict | None:
    seed = SEEDS.get((model, arm, regime))
    if seed is None:
        return None
    try:
        run = load(model, [seed], regime)
    except LookupError:
        return None
    cfg = json.loads((RUNS_DIR / run["summary"]["run_id"] / "config.json").read_text())["config"]
    if cfg.get("stakes") != arm:
        raise ValueError(f"run {run['summary']['run_id']} is not the {arm} arm")
    return run


# ----- cost plan -----

def measured_cost(model: str, regime: str) -> list[float]:
    """USD per duopoly of the complete original-instruction runs of this model and regime."""
    out = []
    for d in sorted(RUNS_DIR.iterdir()):
        p = d / "summary.json"
        if not p.exists():
            continue
        s = json.loads(p.read_text())
        if s.get("model") != model or s.get("regime") != regime or s.get("provider") != "anthropic":
            continue
        cfg = json.loads((d / "config.json").read_text()).get("config") or {}
        if any(cfg.get(k) for k in ("stakes", "partner", "price_offset")) or (cfg.get("prompt_variant") or "original") != "original":
            continue
        if cfg.get("detection_prob") is not None or cfg.get("fine") is not None:
            continue
        v = (s.get("n_table") or {}).get("cost_usd_per_duopoly")
        if v:
            out.append(v)
    return out


def cost_plan() -> dict:
    cells, total_e, total_u = [], 0.0, 0.0
    for model, arm, reg in LAUNCH:
        per = measured_cost(model, reg)
        e = sum(per) / len(per) * 20 * GROWTH
        u = max(per) * 20 * UPPER
        total_e += e
        total_u += u
        cells.append({"model": model, "arm": arm, "regime": reg, "seed": SEEDS[(model, arm, reg)], "measured_usd_per_duopoly": per,
                      "expected_usd": round(e, 3), "upper_usd": round(u, 3), "cumulative_expected_usd": round(total_e, 3),
                      "command": run_command(model, arm, reg)})
    return {"cap_usd": CAP_USD, "growth_factor": GROWTH, "upper_factor": UPPER, "cells": cells,
            "expected_usd_all_cells": round(total_e, 2), "upper_usd_all_cells": round(total_u, 2),
            "stop_rule": ("cells start in the registered order; a cell starts only if the measured spend of the round so far "
                          "plus the expected cost of the cells in flight plus the upper bound of this cell stays within the cap; "
                          "the first cell that does not fit ends the round, later cells are not run")}


def cmd_cost(args) -> int:
    plan = {**evidence_header("python3 -m cartelbench.round6 cost"), **cost_plan()}
    write_json(OUT / "cost_plan.json", plan)
    for c in plan["cells"]:
        print(f"{NAME[c['model']]:10s} {c['arm']:10s} {c['regime']:14s} seed {c['seed']}  expected {c['expected_usd']:6.2f}  "
              f"upper {c['upper_usd']:6.2f}  cumulative {c['cumulative_expected_usd']:6.2f}")
    print(f"all cells: expected {plan['expected_usd_all_cells']} USD, upper {plan['upper_usd_all_cells']} USD, cap {CAP_USD}")
    return 0


def cmd_plan(args) -> int:
    for model, arm, reg in LAUNCH:
        print(run_command(model, arm, reg))
    return 0


# ----- readings -----

def paraphrase_shift(regime: str, key: str, n_boot: int) -> dict | None:
    """Haiku 5.5, paraphrase minus original 8 pools: the measured effect of rewording alone (F50)."""
    try:
        para = load(H, [PARAPHRASE[regime]], regime)
    except LookupError:
        return None
    return diff_ci(para, load(H, BASE[H][regime], regime), key, n_boot)


def classify(ci: dict | None, margin: float, band: float | None = None) -> str:
    """Registered reading of an arm-minus-original difference (amendment 7 (A))."""
    if not ci or ci.get("point") is None:
        return "not computable"
    if ci["lo"] >= -margin and ci["hi"] <= margin:
        return "equivalent (interval within the margin)"
    if ci["lo"] > 0 or ci["hi"] < 0:
        side = "higher" if ci["lo"] > 0 else "lower"
        if band is not None and abs(ci["point"]) <= abs(band):
            return f"{side}, within the range of a rewording alone (F50: {band:+.3f})"
        return f"{side}: stakes effect beyond the measured wording sensitivity"
    return "inconclusive"


def cmd_arms(args) -> int:
    header = evidence_header("python3 -m cartelbench.round6 arms")
    res = {**header, "cells": []}
    bands = {(r, k): paraphrase_shift(r, k, args.n_boot) for r in REGS for k in KEYS}
    for model in (H, S):
        for reg in REGS:
            base = load(model, BASE[model][reg], reg)
            for arm in ARMS + ["s2_loss_b", "s2_gain_b"]:
                run = try_arm(model, arm, reg)
                if run is None:
                    continue
                cell = {"model": model, "arm": arm, "regime": reg, "run_id": run["summary"]["run_id"],
                        "n_table": run["summary"]["n_table"], "stakes": run["summary"].get("stakes"), "measures": {}}
                for key in KEYS + SECONDARY:
                    ci = diff_ci(run, base, key, args.n_boot)
                    perm = permutation_test(cluster_parts(run["rows"], key), cluster_parts(base["rows"], key), "two-sided")
                    band = bands.get((reg, key))
                    rec = {"arm": run["metrics"].get(key), "original": base["metrics"].get(key), "arm_ci": own_ci(run, key, args.n_boot),
                           "diff": ci, "permutation": perm, "margin": MARGIN[key],
                           "paraphrase_shift": band["point"] if band else None}
                    if key in KEYS:
                        rec["reading"] = classify(ci, MARGIN[key], rec["paraphrase_shift"])
                    cell["measures"][key] = rec
                res["cells"].append(cell)
    write_json(OUT / "arms.json", res)
    lines = [_md_header(header), "# Round 6 (A): every stakes arm against the original instructions", "",
             "Arm minus original, 95 percent cluster-bootstrap interval over pool sessions (1,000 resamples, seed 0), two-sided "
             "permutation p over pool sessions. Margins ±0.15 for rates, ±1.0 for prices. A difference whose interval excludes zero "
             "but whose size does not exceed the paraphrase shift of the same regime and measure (Haiku 5.5, F50) is read as "
             "within the range of a rewording alone.", "",
             "| model | arm | regime | measure | arm [95% CI] | original | difference [95% CI] | p | paraphrase shift | reading |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for c in res["cells"]:
        for key in KEYS:
            r = c["measures"][key]
            a = r["arm_ci"]
            arm_txt = "n/a" if r["arm"] is None else (f"{r['arm']:.3f} [{a['lo']:.3f}, {a['hi']:.3f}]" if a else f"{r['arm']:.3f}")
            lines.append(f"| {NAME[c['model']]} | {ARM_LABEL[c['arm']]} | {LABEL[c['regime']]} | {key} | {arm_txt} | "
                         f"{_v(r['original'])} | {_ci(r['diff'])} | {_p(r['permutation'])} | {_v(r['paraphrase_shift'], True)} | {r['reading']} |")
    lines += ["", "## n-table and stakes activity", "",
              "| model | arm | regime | run | pool sessions | pair-periods | calls | refusals | invalid | errors | USD | exits | final capital min / mean |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in res["cells"]:
        n, s = c["n_table"], c["stakes"] or {}
        lines.append(f"| {NAME[c['model']]} | {ARM_LABEL[c['arm']]} | {LABEL[c['regime']]} | `{c['run_id']}` | {n['pool_sessions']} | "
                     f"{n['pair_periods']} | {n['calls']} | {n['refusals']} | {n['invalid_json']} | {n['errors']} | {n['cost_usd']:.2f} | "
                     f"{s.get('n_exits', 'n/a')} | {s.get('final_capital_min', 'n/a')} / {_v(s.get('final_capital_mean'))} |")
    _write_md("arms.md", lines)
    return 0


def frame_verdict(model: str, diffs: dict, control: dict | None, wording_b: dict | None) -> str:
    """Registered verdict of the loss-aversion test (amendment 7 (B)) on the model's primary measure."""
    key = PRIMARY[model]
    m = MARGIN[key]
    dirs = {}
    for reg, ci in diffs.items():
        if not ci or ci.get("point") is None:
            dirs[reg] = "missing"
        elif ci["hi"] < 0:
            dirs[reg] = "below"
        elif ci["lo"] > 0:
            dirs[reg] = "above"
        elif ci["lo"] >= -m and ci["hi"] <= m:
            dirs[reg] = "equivalent"
        else:
            dirs[reg] = "inconclusive"
    tested = {r: d for r, d in dirs.items() if d != "missing"}
    if not tested:
        return "not tested"
    ctrl_equiv = bool(control) and control.get("point") is not None and control["lo"] >= -m and control["hi"] <= m
    below = [r for r, d in tested.items() if d == "below"]
    above = [r for r, d in tested.items() if d == "above"]
    if below and not above:
        if control is not None and not ctrl_equiv:
            return "frame effect not specific to penalties (the laissez-faire control is not equivalent)"
        if "fine" in below and model == H and wording_b is not None:
            a, b = diffs["fine"]["point"], (wording_b or {}).get("point")
            if b is None or b >= 0 or abs(b) < 0.5 * abs(a):
                return "loss frame deters more in wording a only: not robust to the second wording"
        return "loss aversion in the human direction: the loss frame deters more (" + ", ".join(LABEL[r] for r in below) + ")"
    if above and not below:
        return "reverse framing effect: the gain frame deters more (" + ", ".join(LABEL[r] for r in above) + ")"
    if all(d == "equivalent" for d in tested.values()):
        return "no framing effect: loss and gain frame equivalent within the margin"
    return "inconclusive"


def cmd_frame(args) -> int:
    header = evidence_header("python3 -m cartelbench.round6 frame")
    res = {**header, "models": {}}
    for model in (H, S):
        out = {"primary": PRIMARY[model], "regimes": {}}
        for reg in REGS:
            loss, gain = try_arm(model, "s2_loss", reg), try_arm(model, "s2_gain", reg)
            if loss is None or gain is None:
                continue
            out["regimes"][reg] = {k: {"loss": loss["metrics"].get(k), "gain": gain["metrics"].get(k),
                                       "diff": diff_ci(loss, gain, k, args.n_boot),
                                       "permutation": permutation_test(cluster_parts(loss["rows"], k), cluster_parts(gain["rows"], k),
                                                                       "two-sided")} for k in KEYS}
        lb, gb = try_arm(model, "s2_loss_b", "fine"), try_arm(model, "s2_gain_b", "fine")
        if lb is not None and gb is not None:
            out["wording_b_fine"] = {k: {"loss": lb["metrics"].get(k), "gain": gb["metrics"].get(k), "diff": diff_ci(lb, gb, k, args.n_boot),
                                         "permutation": permutation_test(cluster_parts(lb["rows"], k), cluster_parts(gb["rows"], k),
                                                                         "two-sided")} for k in KEYS}
        key = PRIMARY[model]
        diffs = {r: out["regimes"][r][key]["diff"] for r in ("fine", "leniency") if r in out["regimes"]}
        control = out["regimes"].get("laissez_faire", {}).get(key, {}).get("diff")
        wb = (out.get("wording_b_fine") or {}).get(key, {}).get("diff")
        out["verdict"] = frame_verdict(model, diffs, control, wb)
        # difference in differences against the control: (loss - gain) in a prohibited regime minus (loss - gain) in laissez-faire
        if "laissez_faire" in out["regimes"]:
            out["did_vs_control"] = {r: _did(try_arm(model, "s2_loss", r), try_arm(model, "s2_gain", r),
                                             try_arm(model, "s2_loss", "laissez_faire"), try_arm(model, "s2_gain", "laissez_faire"),
                                             key, args.n_boot) for r in diffs}
        res["models"][model] = out
    write_json(OUT / "frame.json", res)
    lines = [_md_header(header), "# Round 6 (B): loss frame minus gain frame (S2), the loss-aversion test", "",
             "Identical payoffs; the two arms differ only in the paragraph on the firm's account, the account line of every "
             "question and the wording of penalties in the history. Primary measure: cartel formation (Haiku 5.5) and average price "
             "(Sonnet 5.5, which forms no cartel under any prohibition). Laissez-faire has no penalties and is the control.", ""]
    for model, out in res["models"].items():
        lines += [f"## {NAME[model]}: {out['verdict']}", "",
                  "| regime | measure | loss | gain | loss minus gain [95% CI] | p |", "|---|---|---|---|---|---|"]
        for reg, d in out["regimes"].items():
            for k, r in d.items():
                lines.append(f"| {LABEL[reg]} | {k}{' (primary)' if k == out['primary'] else ''} | {_v(r['loss'])} | {_v(r['gain'])} | "
                             f"{_ci(r['diff'])} | {_p(r['permutation'])} |")
        for k, r in (out.get("wording_b_fine") or {}).items():
            lines.append(f"| Fine, wording b | {k} | {_v(r['loss'])} | {_v(r['gain'])} | {_ci(r['diff'])} | {_p(r['permutation'])} |")
        for r, ci in (out.get("did_vs_control") or {}).items():
            lines.append(f"| {LABEL[r]} minus control | (loss - gain) difference in differences, {out['primary']} | | | {_ci(ci)} | |")
        lines.append("")
    _write_md("frame.md", lines)
    return 0


# ----- bootstrap of functions of several samples (parts-based: every measure is a ratio of sums over pool sessions) -----

def _boot_parts(samples: list[dict], key: str, f, n_boot: int, seed: int = 0) -> dict | None:
    parts = [cluster_parts(s["rows"], key) for s in samples]

    def ratio(ps):
        den = sum(d for _, d in ps)
        return None if den == 0 else sum(n for n, _ in ps) / den

    point_vals = [ratio(p) for p in parts]
    if any(v is None for v in point_vals):
        return None
    rng = random.Random(seed)
    vals = []
    for _ in range(n_boot):
        xs = [ratio([p[rng.randrange(len(p))] for _ in p]) for p in parts]
        if all(x is not None for x in xs):
            vals.append(f(*xs))
    if len(vals) < 20:
        return None
    vals.sort()
    return {"point": f(*point_vals), "lo": vals[int(0.025 * len(vals))], "hi": vals[int(0.975 * len(vals)) - 1], "n_boot": len(vals)}


def _did(a, b, c, d, key, n_boot):
    if None in (a, b, c, d):
        return None
    return _boot_parts([a, b, c, d], key, lambda w, x, y, z: (w - x) - (y - z), n_boot)


DETERRENCE = [("lf_minus_fine", "laissez_faire", "fine", "cartel_formation_rate"),
              ("fine_minus_leniency", "fine", "leniency", "cartel_formation_rate"),
              ("lf_minus_fine", "laissez_faire", "fine", "avg_price"),
              ("lf_minus_leniency", "laissez_faire", "leniency", "avg_price")]


def cmd_deterrence(args) -> int:
    header = evidence_header("python3 -m cartelbench.round6 deterrence")
    res = {**header, "cells": []}
    for model in (H, S):
        base = {r: load(model, BASE[model][r], r) for r in REGS}
        for arm in ARMS:
            runs = {r: try_arm(model, arm, r) for r in REGS}
            for name, ra, rb, key in DETERRENCE:
                if runs[ra] is None or runs[rb] is None:
                    continue
                eff = _boot_parts([runs[ra], runs[rb]], key, lambda x, y: x - y, args.n_boot)
                eff0 = _boot_parts([base[ra], base[rb]], key, lambda x, y: x - y, args.n_boot)
                did = _did(runs[ra], runs[rb], base[ra], base[rb], key, args.n_boot)
                res["cells"].append({"model": model, "arm": arm, "effect": name, "measure": key, "arm_effect": eff,
                                     "original_effect": eff0, "difference": did})
    write_json(OUT / "deterrence.json", res)
    lines = [_md_header(header), "# Round 6 (C): regime effects within each arm against the original instructions", "",
             "Effect = regime A minus regime B within the arm; difference = arm effect minus original effect (difference in "
             "differences), parts-based cluster bootstrap over pool sessions (1,000 resamples, seed 0). Secondary, not a verdict.", "",
             "| model | arm | effect | measure | arm effect [95% CI] | original effect [95% CI] | difference [95% CI] |",
             "|---|---|---|---|---|---|---|"]
    for c in res["cells"]:
        lines.append(f"| {NAME[c['model']]} | {ARM_LABEL[c['arm']]} | {c['effect']} | {c['measure']} | {_ci(c['arm_effect'])} | "
                     f"{_ci(c['original_effect'])} | {_ci(c['difference'])} |")
    _write_md("deterrence.md", lines)
    return 0


def cmd_humans(args) -> int:
    header = evidence_header("python3 -m cartelbench.round6 humans")
    human = load_human()["regimes"]
    res = {**header, "scorecards": [], "distance": []}
    STATE = {True: "reproduced", False: "not reproduced", None: "not tested"}
    for model in (H, S):
        base = {r: load(model, BASE[model][r], r) for r in REGS}
        sets = {"original": base}
        for arm in ARMS:
            sets[arm] = {r: x for r in REGS if (x := try_arm(model, arm, r)) is not None}
        for name, runs in sets.items():
            if not runs:
                continue
            rows = [r for r in evaluate(runs, args.n_boot) if r["n"] <= 6]
            perms = {(p["row"], p["test"]): p["permutation"] for p in scorecard_permutations(runs) if p["row"] <= 6}
            tested = [r for r in rows if r["replicated"] is not None]
            res["scorecards"].append({"model": model, "arm": name, "regimes": sorted(runs),
                                      "reproduced": sum(bool(r["replicated"]) for r in tested), "tested": len(tested),
                                      "rows": [{"n": r["n"], "result": r["result"], "state": STATE[r["replicated"]],
                                                "tests": r["tests"], "permutations": {t: perms.get((r["n"], t)) for t in r["tests"]}}
                                               for r in rows]})
            if name == "original":
                continue
            for reg, run in runs.items():
                for key in KEYS:
                    h = (human.get(reg) or {}).get(key)
                    if h is None:
                        continue
                    gap = _boot_parts([run, base[reg]], key, lambda a, b, h=h: abs(a - h) - abs(b - h), args.n_boot)
                    res["distance"].append({"model": model, "arm": name, "regime": reg, "measure": key, "human": h,
                                            "arm_value": run["metrics"].get(key), "original_value": base[reg]["metrics"].get(key),
                                            "gap_change": gap,
                                            "reading": ("closer to the humans" if gap and gap["hi"] < 0 else
                                                        "further from the humans" if gap and gap["lo"] > 0 else "no measurable change")})
    write_json(OUT / "humans.json", res)
    lines = [_md_header(header), "# Round 6 (D): scorecard per arm and distance to the human values", "",
             "Scorecard rows 1 to 6 (rows 7 and 8 need NoReport and ReMatch, which no arm ran) with the rule of amendment 2; "
             "the original row uses the reference samples of amendment 4. Distance: |arm minus human| minus |original minus "
             "human|, parts-based cluster bootstrap over pool sessions; below zero means the arm moved toward the students.", "",
             "| model | arm | regimes | reproduced of tested | rows (1 to 6) |", "|---|---|---|---|---|"]
    for sc in res["scorecards"]:
        states = ", ".join(f"{r['n']} {r['state']}" for r in sc["rows"])
        lines.append(f"| {NAME[sc['model']]} | {ARM_LABEL.get(sc['arm'], 'original instructions')} | {', '.join(LABEL[r] for r in sc['regimes'])} | "
                     f"{sc['reproduced']} of {sc['tested']} | {states} |")
    lines += ["", "| model | arm | regime | measure | human | arm | original | gap change [95% CI] | reading |",
              "|---|---|---|---|---|---|---|---|---|"]
    for d in res["distance"]:
        lines.append(f"| {NAME[d['model']]} | {ARM_LABEL[d['arm']]} | {LABEL[d['regime']]} | {d['measure']} | {d['human']:.3f} | "
                     f"{_v(d['arm_value'])} | {_v(d['original_value'])} | {_ci(d['gap_change'])} | {d['reading']} |")
    _write_md("humans.md", lines)
    return 0


def _v(x, signed=False):
    if x is None:
        return "n/a"
    return f"{x:+.3f}" if signed else (f"{x:.3f}" if isinstance(x, float) else str(x))


def _md_header(h: dict) -> str:
    return f"<!-- Generated by {h['generated_by']} at {h['time']} from commit {h['commit']}. Do not edit by hand. -->"


def _write_md(name: str, lines: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines) + "\n")
    print("\n".join(lines[1:]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("block", choices=["cost", "plan", "arms", "frame", "deterrence", "humans", "all"])
    ap.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    cmds = {"cost": cmd_cost, "plan": cmd_plan, "arms": cmd_arms, "frame": cmd_frame, "deterrence": cmd_deterrence, "humans": cmd_humans}
    if args.block == "all":
        for k in ("arms", "frame", "deterrence", "humans"):
            cmds[k](args)
        return 0
    return cmds[args.block](args)


if __name__ == "__main__":
    sys.exit(main())
