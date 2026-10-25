"""Launch the round-6 cells in the registered order with the stop rule of amendment 7.

    python3 scripts/round6_launch.py --model claude-haiku-5-5 --parallel 4 --concurrency 5
    python3 scripts/round6_launch.py --model claude-sonnet-5-5 --parallel 3 --concurrency 6

A cell starts only if the measured spend of the round so far (summary.json of the complete round-6 runs) plus the
expected cost of the cells in flight plus the upper bound of this cell stays within the cap; the first cell that does
not fit ends the launch, later cells are not run. Cells that already have a complete run are skipped (no rerun).
Progress lines go to evidence/round6/launch_log.jsonl.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cartelbench.round6 import CAP_USD, LAUNCH, OUT, SEEDS, cost_plan  # noqa: E402
from cartelbench.util import CODE_DIR, EVIDENCE_DIR, now_iso  # noqa: E402

RUNS = EVIDENCE_DIR / "runs"
LOG = OUT / "launch_log.jsonl"


def log(row: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as fh:
        fh.write(json.dumps({**row, "time": now_iso()}) + "\n")
    print(json.dumps(row), flush=True)


def round6_runs() -> dict[tuple, dict]:
    """Complete runs of the round-6 cells, by (model, arm, regime)."""
    seeds = {v: k for k, v in SEEDS.items()}
    out = {}
    for d in sorted(RUNS.iterdir()):
        p = d / "summary.json"
        if not p.exists():
            continue
        s = json.loads(p.read_text())
        key = seeds.get(s.get("seed"))
        if key and key[0] == s.get("model") and key[2] == s.get("regime"):
            cfg = json.loads((d / "config.json").read_text()).get("config") or {}
            if cfg.get("stakes") == key[1]:
                out[key] = s
    return out


def spent() -> float:
    return sum((s.get("n_table") or {}).get("cost_usd") or 0.0 for s in round6_runs().values())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--cap", type=float, default=CAP_USD)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    plan = {(c["model"], c["arm"], c["regime"]): c for c in cost_plan()["cells"]}
    queue = [k for k in LAUNCH if k[0] == args.model]
    done = round6_runs()
    running: dict[tuple, subprocess.Popen] = {}
    stopped = False
    while queue or running:
        for k, proc in list(running.items()):
            if proc.poll() is not None:
                log({"event": "end", "cell": k, "returncode": proc.returncode, "spent_usd": round(spent(), 3)})
                del running[k]
                if proc.returncode != 0:
                    stopped = True        # an API or billing error ends the round (amendment 7)
                    log({"event": "stop", "reason": f"cell {k} failed with return code {proc.returncode}"})
        while queue and not stopped and len(running) < args.parallel:
            k = queue[0]
            if k in done:
                queue.pop(0)
                log({"event": "skip", "cell": k, "reason": "complete run exists"})
                continue
            in_flight = sum(plan[r]["expected_usd"] for r in running)
            need = spent() + in_flight + plan[k]["upper_usd"]
            if need > args.cap:
                stopped = True
                log({"event": "stop", "reason": "cap", "cell": k, "spent_usd": round(spent(), 3), "in_flight_expected_usd": round(in_flight, 3),
                     "upper_usd": plan[k]["upper_usd"], "cap_usd": args.cap, "not_run": [list(q) for q in queue]})
                break
            queue.pop(0)
            cmd = [sys.executable, "-m", "cartelbench.run", "--regime", k[2], "--model", k[0], "--duopoles", "20", "--pools", "4",
                   "--seed", str(SEEDS[k]), "--stakes", k[1], "--concurrency", str(args.concurrency)]
            log({"event": "start", "cell": k, "command": " ".join(cmd[1:]), "check_usd": round(need, 3)})
            if args.dry_run:
                continue
            out = open(OUT / f"stdout_{k[1]}_{k[2]}_s{SEEDS[k]}.txt", "w")
            running[k] = subprocess.Popen(cmd, cwd=CODE_DIR, stdout=out, stderr=subprocess.STDOUT)
        if stopped and not running:
            break
        if args.dry_run:
            break
        time.sleep(20)
    log({"event": "finished", "model": args.model, "spent_usd": round(spent(), 3)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
