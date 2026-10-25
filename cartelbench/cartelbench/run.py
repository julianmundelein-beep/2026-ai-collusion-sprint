"""One command per regime and model.

    python3 -m cartelbench.run --regime fine --model claude-haiku-5-5 --duopoles 20 --seed 1
    python3 -m cartelbench.run --regime laissez_faire --player collude --duopoles 3 --seed 1   (no API)
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

from .engine import RunConfig, run_sync
from .llm import anthropic_api_key, make_client
from .regimes import REGIMES
from .util import EVIDENCE_DIR, git_commit, now_iso

LAUNCH_LOG = EVIDENCE_DIR / "ledger" / "launches.jsonl"


def log_launch(row: dict, path=None) -> None:
    """Run ledger (amendment 4 (d)): one line when a run starts and one when it ends, so aborted runs stay listed."""
    path = pathlib.Path(path or LAUNCH_LOG)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(row, default=str) + "\n")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Run one regime of the Bigoni duopoly with LLM or scripted sellers.")
    ap.add_argument("--regime", choices=sorted(REGIMES), default="laissez_faire")
    ap.add_argument("--model", default="claude-haiku-5-5", help="model id (ignored for scripted players)")
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", ""), help="OpenAI-compatible endpoint (provider openai)")
    ap.add_argument("--api-key-env", default="OPENAI_API_KEY", help="env var holding the key for provider openai")
    ap.add_argument("--player", choices=["llm", "collude", "deviate", "nash", "random", "tit", "scatter_emp", "scatter24", "scatter15"],
                    default="llm")
    ap.add_argument("--duopoles", type=int, default=20)
    ap.add_argument("--pools", type=int, default=4, help="independent pool sessions, the bootstrap unit (default 4 pools of 10 agents)")
    ap.add_argument("--pool-size", type=int, default=0, help="agents per pool; 0 = 2 * duopoles / pools (paper: 20)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--price-offset", type=int, default=0, help="contamination test: show prices shifted by this amount (grid 0+k to 12+k)")
    ap.add_argument("--payoff-scale", type=float, default=1.0, help="robustness: multiply the payoff table")
    ap.add_argument("--detection", type=float, default=None, help="override detection probability (dose)")
    ap.add_argument("--fine", type=int, default=None, help="override the fine")
    ap.add_argument("--effort", default="low", help="Claude effort level")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--max-periods", type=int, default=60)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--run-id", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--prompt-variant", choices=["original", "paraphrase"], default="original",
                    help="instruction wording (paraphrase: prompt-robustness arm, amendment 4 (c))")
    ap.add_argument("--screen-p", type=int, default=None, help="threshold of a screen regime (amendment 6, N2; default: the regime's)")
    ap.add_argument("--partner", choices=["nash", "scatter_emp", "scatter24", "scatter15", "collude", "deviate", "tit"], default="",
                    help="scripted partner (amendment 6, K): every duopole pairs one LLM agent with this scripted player")
    ap.add_argument("--stakes", choices=["s1_money", "s2_loss", "s2_gain", "s3_exit", "s4_all", "s2_loss_b", "s2_gain_b"], default="",
                    help="stakes arm (amendment 7): money frame, loss or gain frame, bankruptcy; rules and points unchanged")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    cfg = RunConfig(regime=args.regime, model=args.model if args.player == "llm" else f"scripted-{args.player}",
                    provider=args.provider if args.player == "llm" else "scripted", player=args.player,
                    duopoles=args.duopoles, pools=args.pools, pool_size=args.pool_size, seed=args.seed, price_offset=args.price_offset,
                    payoff_scale=args.payoff_scale,
                    detection_prob=args.detection, fine=args.fine, effort=args.effort, concurrency=args.concurrency,
                    max_periods=args.max_periods, run_id=args.run_id, label=args.label, base_url=args.base_url,
                    api_key_env=args.api_key_env, prompt_variant=args.prompt_variant, screen_p=args.screen_p, partner=args.partner,
                    stakes=args.stakes)
    if args.out_dir:
        cfg.out_dir = args.out_dir
    client = None
    if args.player == "llm":
        if args.provider == "anthropic" and not anthropic_api_key():
            print("ANTHROPIC_API_KEY is not set: no paid call is made. Set it (locally in .env, in the cloud as the "
                  "environment variable CARTELBENCH_ANTHROPIC_KEY) or use --player collude for a scripted run.", file=sys.stderr)
            return 2
        client = make_client(args.provider, args.model, effort=args.effort, concurrency=args.concurrency,
                             base_url=args.base_url, api_key_env=args.api_key_env)
    if not cfg.run_id:
        tag = (f"_vs-{cfg.partner}" if cfg.partner else "") + (f"_stakes-{cfg.stakes}" if cfg.stakes else "")   # scripted partner (amendment 6, K); the Claude K runs of
        cfg.run_id = f"{cfg.regime}_{cfg.model.replace('/', '-')}{tag}_{now_iso().replace(':', '').replace('-', '')}_s{cfg.seed}"
        # seeds 101 to 106 predate this tag and carry the partner in config.json only
    argline = " ".join(argv or sys.argv[1:])
    log_launch({"event": "start", "run_id": cfg.run_id, "args": argline, "out_dir": cfg.out_dir, "commit": git_commit(), "time": now_iso()})
    try:
        summary = run_sync(cfg, client, generated_by="python3 -m cartelbench.run " + argline)
    except BaseException as exc:  # noqa: BLE001 (also KeyboardInterrupt: the run is listed as aborted)
        log_launch({"event": "end", "run_id": cfg.run_id, "status": "aborted", "error": f"{type(exc).__name__}: {str(exc)[:300]}", "time": now_iso()})
        raise
    log_launch({"event": "end", "run_id": cfg.run_id, "status": "complete", "cost_usd": summary["n_table"].get("cost_usd"),
                "calls": summary["n_table"].get("calls"), "time": now_iso()})
    m = summary["metrics"]
    print(json.dumps({"run_id": summary["run_id"], "periods_per_pool": summary["periods_per_pool"],
                      "n_table": summary["n_table"],
                      "cartel_incidence": m.get("cartel_incidence"), "cartel_formation_rate": m.get("cartel_formation_rate"),
                      "avg_price": m.get("avg_price"), "cartel_price": m.get("cartel_price"),
                      "deviation_rate": m.get("deviation_rate"), "report_rate_given_cartel": m.get("report_rate_given_cartel")},
                     indent=2))
    print(f"evidence: {cfg.out_dir}/{summary['run_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
