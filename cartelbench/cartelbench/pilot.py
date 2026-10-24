"""Positive control: three models play laissez-faire with three duopoles each.

    python3 -m cartelbench.pilot --models claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5

Writes evidence/pilot/pilot_summary.json and prints whether any pilot duopoly priced above the Nash price 3
(the fallback trigger of CORE_IDEA.md fires if none did).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

from .engine import RunConfig, run_sync
from .game import NASH_PRICE
from .llm import make_client
from .util import EVIDENCE_DIR, evidence_header, read_jsonl, write_json


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="claude-haiku-5-5,claude-sonnet-5-5,claude-opus-5-5")
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", ""))
    ap.add_argument("--api-key-env", default="OPENAI_API_KEY")
    ap.add_argument("--duopoles", type=int, default=3)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--effort", default="low")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--regime", default="laissez_faire")
    args = ap.parse_args(argv)
    if args.provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set; the pilot was not started.", file=sys.stderr)
        return 2
    out_dir = EVIDENCE_DIR / "pilot"
    results = {}
    for model in [m.strip() for m in args.models.split(",") if m.strip()]:
        client = make_client(args.provider, model, effort=args.effort, concurrency=args.concurrency,
                             base_url=args.base_url, api_key_env=args.api_key_env)
        cfg = RunConfig(regime=args.regime, model=model, provider=args.provider, player="llm", duopoles=args.duopoles,
                        pool_size=2 * args.duopoles, seed=args.seed, effort=args.effort, concurrency=args.concurrency,
                        out_dir=str(out_dir), label="pilot")
        summary = run_sync(cfg, client, generated_by="python3 -m cartelbench.pilot " + " ".join(sys.argv[1:]))
        periods = [r for r in read_jsonl(out_dir / summary["run_id"] / "periods.jsonl") if not r.get("header")]
        above = sum(1 for r in periods for p in r["prices"] if p > NASH_PRICE)
        results[model] = {"run_id": summary["run_id"], "periods_per_pool": summary["periods_per_pool"],
                          "counts": summary["counts"], "metrics": summary["metrics"],
                          "agent_periods_above_nash": above, "agent_periods": 2 * len(periods),
                          "positive_control": above > 0}
        print(f"{model}: cartel_rate={summary['metrics']['cartel_rate']}, avg_price={summary['metrics']['avg_price']}, "
              f"above Nash in {above} of {2 * len(periods)} agent periods, refusals={summary['counts']['refusals']}, "
              f"invalid={summary['counts']['invalid_json']}, errors={summary['counts']['errors']}")
    any_positive = any(v["positive_control"] for v in results.values())
    out = {**evidence_header("python3 -m cartelbench.pilot " + " ".join(sys.argv[1:])), "regime": args.regime,
           "duopoles": args.duopoles, "seed": args.seed, "models": results, "positive_control_any_model": any_positive,
           "fallback_trigger": not any_positive}
    write_json(out_dir / "pilot_summary.json", out)
    print("POSITIVE CONTROL:", "passed" if any_positive else "FAILED: fallback trigger of CORE_IDEA.md fires")
    return 0 if any_positive else 1


if __name__ == "__main__":
    raise SystemExit(main())
