"""Round 7, as registered in PREREGISTRATION_round7.md: the threshold curve and the random, undisclosed threshold.

    python3 -m cartelbench.round7 cost                      # cost plan before the first call
    python3 -m cartelbench.round7 launch --block haiku      # Haiku cells with the stop rule (cap 7 USD)
    python3 -m cartelbench.round7 launch --block sonnet     # Sonnet random arm, only under the programme-total rule
    python3 -m cartelbench.round7 run-cell -- <run args>    # one cell (cartelbench.run), launch lines to evidence/round7/
    python3 -m cartelbench.round7 spend                     # Anthropic spend: ledger total plus round-7 runs
    python3 -m cartelbench.round7 curve | random | figure | all

Runs of this round live in evidence/round7/runs/ (the open models may also land in evidence/provider2/runs/); samples are
fixed by model, regime and seed, never by "latest run". Results go to evidence/round7/.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

from .pools import RUNS_DIR, find_run, merge_runs
from .util import CODE_DIR, EVIDENCE_DIR, evidence_header, now_iso, write_json

OUT = EVIDENCE_DIR / "round7"
R7_RUNS = OUT / "runs"
P2_RUNS = EVIDENCE_DIR / "provider2" / "runs"
H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
Q, L = "qwen2.5-32b-instruct", "llama-3.1-8b-instruct"
NAME = {H: "Haiku 5.5", S: "Sonnet 5.5", Q: "Qwen2.5-32B", L: "Llama-3.1-8B"}
MODELS = [H, S, Q, L]

# new cells: (model, regime, seed, screen_p); registered in PREREGISTRATION_round7.md
CELLS = [
    (H, "nocomm_screen", 701, 3), (H, "nocomm_screen", 702, 6), (H, "nocomm_screen", 703, 7),
    (H, "nocomm_screen_random", 711, None), (H, "fine_screen_random", 712, None),
    (S, "nocomm_screen_random", 721, None), (S, "nocomm_screen", 722, 3), (S, "nocomm_screen", 723, 6), (S, "nocomm_screen", 724, 7),
    (Q, "nocomm_screen", 731, 3), (Q, "nocomm_screen", 733, 6), (Q, "nocomm_screen", 734, 7),
    (Q, "nocomm_screen_random", 735, None), (Q, "fine_screen_random", 736, None), (Q, "nocomm_screen", 732, 5),
    (L, "nocomm_screen", 741, 3), (L, "nocomm_screen", 743, 6), (L, "nocomm_screen", 744, 7),
    (L, "nocomm_screen_random", 745, None), (L, "fine_screen_random", 746, None), (L, "nocomm_screen", 742, 5),
]
# existing cells of the curve: threshold -> seed (amendment 5: p 4; amendment 6: p 5)
CURVE_EXISTING = {H: {4: 72, 5: 92}, S: {4: 71, 5: 91}, Q: {4: 121}, L: {4: 124}}
CURVE_NEW = {m: {p: s for mm, r, s, p in CELLS if mm == m and r == "nocomm_screen"} for m in MODELS}
# references (amendments 4 to 6)
NOCOMM = {H: 13, S: 55, Q: 13, L: 123}
FIXED4_NOCOMM = {H: 72, S: 71, Q: 121, L: 124}
FIXED4_FINE = {H: 73, Q: 122, L: 125}
FINE = {H: (2, 42), Q: (2,), L: (2,)}
RANDOM_NOCOMM = {m: s for m, r, s, p in CELLS if r == "nocomm_screen_random"}
RANDOM_FINE = {m: s for m, r, s, p in CELLS if r == "fine_screen_random"}

# budget (PREREGISTRATION_round7.md, budget and addendum 1): Haiku block cap; Sonnet under the programme limit
HAIKU_CAP_USD = 7.0
PROGRAMME_LIMIT_USD = 100.0     # addendum 1 (Julian): replaces the gate of 95 and the limit of 98 USD
UPPER_FACTOR = 2.0
LEDGER_TOTAL_BEFORE = 88.418755475     # evidence/ledger/ledger.json at commit 650a0c1 (M98)


def runs_dirs(model: str) -> list[pathlib.Path]:
    return [d for d in (R7_RUNS, P2_RUNS if model in (Q, L) else RUNS_DIR) if d.exists()]


def find_any(model: str, regime: str, seed: int) -> pathlib.Path:
    hits = []
    for d in runs_dirs(model):
        try:
            hits.append(find_run(model, regime, seed, d))
        except LookupError:
            pass
    if len(hits) != 1:
        raise LookupError(f"{len(hits)} complete runs for {model} {regime} seed {seed}")
    return hits[0]


def load(model: str, regime: str, seeds) -> dict:
    seeds = (seeds,) if isinstance(seeds, int) else tuple(seeds)
    return merge_runs([find_any(model, regime, s) for s in seeds])


# ----- cost -----
def measured_per_duopoly(model: str, regime: str, seeds) -> list[float]:
    out = []
    for s in seeds:
        summ = json.loads((find_any(model, regime, s) / "summary.json").read_text())
        out.append(summ["n_table"]["cost_usd"] / summ["n_table"]["duopoles"])
    return out


def cost_plan() -> dict:
    base = {H: {"nocomm": measured_per_duopoly(H, "nocomm_screen", (72, 92)), "fine": measured_per_duopoly(H, "fine_screen", (73,))},
            S: {"nocomm": measured_per_duopoly(S, "nocomm_screen", (71, 91))}}
    cells = []
    for model, reg, seed, p in CELLS:
        if model not in base:
            cells.append({"model": model, "regime": reg, "seed": seed, "screen_p": p, "provider": "modal (local session)",
                          "command": run_command(model, reg, seed, p)})
            continue
        per = base[model]["fine" if reg.startswith("fine") else "nocomm"]
        e = sum(per) / len(per) * 20
        cells.append({"model": model, "regime": reg, "seed": seed, "screen_p": p, "measured_usd_per_duopoly": per,
                      "expected_usd": round(e, 3), "upper_usd": round(max(per) * 20 * UPPER_FACTOR, 3),
                      "command": run_command(model, reg, seed, p)})
    hk = [c for c in cells if c["model"] == H]
    sn = [c for c in cells if c["model"] == S]
    return {"cells": cells, "haiku_expected_usd": round(sum(c["expected_usd"] for c in hk), 3),
            "haiku_upper_usd": round(sum(c["upper_usd"] for c in hk), 3), "haiku_cap_usd": HAIKU_CAP_USD,
            "sonnet_expected_usd": round(sum(c["expected_usd"] for c in sn), 3), "sonnet_upper_usd": round(sum(c["upper_usd"] for c in sn), 3),
            "ledger_total_before_usd": LEDGER_TOTAL_BEFORE, "programme_limit_usd": PROGRAMME_LIMIT_USD,
            "upper_factor": UPPER_FACTOR,
            "stop_rule": ("Haiku: cells start in the registered order; a cell starts only if the round's measured Haiku spend plus "
                          "the expected cost of the cells in flight plus this cell's upper bound stays within 7 USD; the first "
                          "cell that does not fit ends the block. Sonnet (addendum 1): cells in the order random, p 3, p 6, p 7; "
                          "a cell starts only if the Anthropic programme total spent so far (ledger total before the round plus "
                          "every round-7 run, partial runs included) plus the upper bounds of the cells in flight plus this "
                          "cell's upper bound stays within 100 USD; while it does not fit and cells are in flight it waits for "
                          "them; if it does not fit with no cell in flight, the block ends and later cells are not run.")}


def run_command(model: str, regime: str, seed: int, p: int | None) -> str:
    base = (f"python3 -m cartelbench.round7 run-cell -- --regime {regime} --model {model} --duopoles 20 --pools 4 "
            f"--seed {seed}" + (f" --screen-p {p}" if p is not None else "") + f" --out-dir {R7_RUNS.relative_to(CODE_DIR)}")
    if model in (Q, L):
        base += " --provider openai --base-url $OPENAI_BASE_URL --api-key-env <as in PREREGISTRATION_provider2.md>"
    return base


def cmd_cost(args) -> int:
    plan = {**evidence_header("python3 -m cartelbench.round7 cost"), **cost_plan()}
    write_json(OUT / "cost_plan.json", plan)
    for c in plan["cells"]:
        print(f"{NAME[c['model']]:12s} {c['regime']:22s} seed {c['seed']} p {c['screen_p']}  expected {c.get('expected_usd', '-')}  upper {c.get('upper_usd', '-')}")
    print(f"Haiku expected {plan['haiku_expected_usd']} upper {plan['haiku_upper_usd']} (cap {HAIKU_CAP_USD}); "
          f"Sonnet expected {plan['sonnet_expected_usd']} upper {plan['sonnet_upper_usd']}")
    return 0


# ----- spend -----
def round7_runs(model: str | None = None) -> list[dict]:
    out = []
    if not R7_RUNS.exists():
        return out
    for d in sorted(R7_RUNS.iterdir()):
        p = d / "summary.json"
        if p.exists():
            s = json.loads(p.read_text())
            if model is None or s.get("model") == model:
                out.append(s)
    return out


def launched_partial_cost() -> float:
    """Cost of round-7 Anthropic runs that ended without summary.json (aborted): from their calls.jsonl."""
    from .pricing import cost_usd
    total = 0.0
    if not R7_RUNS.exists():
        return 0.0
    for d in sorted(R7_RUNS.iterdir()):
        if (d / "summary.json").exists() or not (d / "calls.jsonl").exists():
            continue
        model = None
        tok = [0, 0, 0, 0]
        for line in (d / "calls.jsonl").read_text().splitlines()[1:]:
            c = json.loads(line)
            model = c["model"]
            tok = [tok[0] + c["input_tokens"], tok[1] + c["output_tokens"], tok[2] + c["cache_read_tokens"], tok[3] + c["cache_write_tokens"]]
        if model in (H, S):
            total += cost_usd(model, *tok)
    return total


def spend() -> dict:
    ledger = json.loads((EVIDENCE_DIR / "ledger" / "ledger.json").read_text())
    before = sum((r.get("cost_usd") or 0) for r in ledger["runs"])
    by_model = {}
    for s in round7_runs():
        if s.get("provider") == "anthropic":
            by_model[s["model"]] = by_model.get(s["model"], 0.0) + (s["n_table"]["cost_usd"] or 0)
    aborted = launched_partial_cost()
    r7 = sum(by_model.values()) + aborted
    return {"ledger_total_usd": before, "ledger_commit": ledger.get("commit"), "round7_by_model_usd": by_model,
            "round7_aborted_usd": aborted, "round7_usd": r7, "programme_total_usd": before + r7}


def cmd_spend(args) -> int:
    s = {**evidence_header("python3 -m cartelbench.round7 spend"), **spend()}
    write_json(OUT / "spend.json", s)
    print(json.dumps(s, indent=2))
    return 0


# ----- launch -----
def log(row: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "launch_log.jsonl").open("a") as fh:
        fh.write(json.dumps({**row, "time": now_iso()}) + "\n")
    print(json.dumps(row), flush=True)


def complete_cell(model: str, regime: str, seed: int) -> dict | None:
    for s in round7_runs(model):
        if s["regime"] == regime and s["seed"] == seed:
            return s
    return None


def cmd_launch(args) -> int:
    plan = cost_plan()
    model = H if args.block == "haiku" else S
    cells = [c for c in plan["cells"] if c["model"] == model]
    running: list[tuple[dict, subprocess.Popen]] = []

    def measured() -> float:
        return sum((s["n_table"]["cost_usd"] or 0) for s in round7_runs(model)) + launched_partial_cost()

    def reap() -> None:
        for c, proc in running[:]:
            if proc.poll() is not None:
                running.remove((c, proc))
                done = complete_cell(c["model"], c["regime"], c["seed"])
                log({"event": "end", "cell": f"{c['regime']} s{c['seed']}", "returncode": proc.returncode,
                     "cost_usd": done["n_table"]["cost_usd"] if done else None})

    for c in cells:
        if complete_cell(c["model"], c["regime"], c["seed"]):
            log({"event": "skip", "cell": f"{c['regime']} s{c['seed']}", "reason": "complete run exists"})
            continue
        while len(running) >= args.parallel:
            time.sleep(10)
            reap()
        reap()
        in_flight = sum(x["expected_usd"] for x, _ in running)
        if model == H:
            need = measured() + in_flight + c["upper_usd"]
            if need > HAIKU_CAP_USD:
                log({"event": "stop", "cell": f"{c['regime']} s{c['seed']}", "spend": measured(), "in_flight": in_flight,
                     "upper": c["upper_usd"], "cap": HAIKU_CAP_USD})
                break
        else:
            # addendum 1: spent so far plus the upper bounds of the cells in flight and of this cell within 100 USD
            while True:
                reap()
                total = spend()["programme_total_usd"]
                upper_in_flight = sum(x["upper_usd"] for x, _ in running)
                if total + upper_in_flight + c["upper_usd"] <= PROGRAMME_LIMIT_USD or not running:
                    break
                time.sleep(15)
            if total + upper_in_flight + c["upper_usd"] > PROGRAMME_LIMIT_USD:
                log({"event": "stop", "cell": f"{c['regime']} s{c['seed']}", "programme_total": total, "upper_in_flight": upper_in_flight,
                     "upper": c["upper_usd"], "limit": PROGRAMME_LIMIT_USD})
                break
        cmd = [sys.executable, "-m", "cartelbench.round7", "run-cell", "--"] + c["command"].split(" -- ", 1)[1].split() + \
              ["--concurrency", str(args.concurrency)]
        log({"event": "start", "cell": f"{c['regime']} s{c['seed']}", "command": " ".join(cmd[1:]), "expected": c["expected_usd"],
             "upper": c["upper_usd"]})
        logf = (OUT / "logs").joinpath(f"{c['regime']}_s{c['seed']}.log")
        logf.parent.mkdir(parents=True, exist_ok=True)
        running.append((c, subprocess.Popen(cmd, cwd=CODE_DIR, stdout=logf.open("w"), stderr=subprocess.STDOUT)))
        time.sleep(2)
    while running:
        time.sleep(10)
        reap()
    log({"event": "block done", "block": args.block, "spend": spend()})
    return 0


def cmd_run_cell(args) -> int:
    from . import run as run_mod
    run_mod.LAUNCH_LOG = OUT / "launches.jsonl"     # the round's launch lines stay in the round's folder
    return run_mod.main(args.rest)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("cost")
    sub.add_parser("spend")
    la = sub.add_parser("launch")
    la.add_argument("--block", choices=["haiku", "sonnet"], required=True)
    la.add_argument("--parallel", type=int, default=5)
    la.add_argument("--concurrency", type=int, default=4)
    rc = sub.add_parser("run-cell")
    rc.add_argument("rest", nargs=argparse.REMAINDER)
    for name in ("curve", "random", "figure", "all"):
        p = sub.add_parser(name)
        p.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    if args.cmd == "run-cell" and args.rest and args.rest[0] == "--":
        args.rest = args.rest[1:]
    if args.cmd in ("curve", "random", "figure", "all"):
        from . import round7_analysis as an
        return an.main(args)
    return {"cost": cmd_cost, "spend": cmd_spend, "launch": cmd_launch, "run-cell": cmd_run_cell}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
