"""Contamination check: ask the model what it knows about the paper, log verbatim.

    python3 -m cartelbench.contamination --model claude-haiku-5-5
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from .llm import make_client
from .util import EVIDENCE_DIR, evidence_header, write_json

QUESTIONS = [
    "Do you know the experimental economics paper 'Fines, Leniency and Rewards in Antitrust' by Bigoni, Fridolfsson, "
    "Le Coq and Spagnolo (RAND Journal of Economics, 2012)? If yes, summarise its design and main results in a few sentences. "
    "If you are not sure, say so.",
    "In that experiment, which prices could subjects choose, what was the fine, what was the detection probability, "
    "and what was the Nash equilibrium price? Answer only what you actually recall and mark guesses as guesses.",
    "In a repeated price-setting duopoly with prices from 0 to 12, a fine of 200 points for discovered price discussions, "
    "a 10 percent discovery probability and a rule under which a sole reporter pays no fine: which published experiment "
    "does this describe, if any?",
]


async def _main(args) -> int:
    client = make_client(args.provider, args.model, effort=args.effort, base_url=args.base_url, api_key_env=args.api_key_env)
    schema = {"type": "object", "properties": {"knows_paper": {"type": "boolean"}, "answer": {"type": "string"}},
              "required": ["knows_paper", "answer"], "additionalProperties": False}
    out = {**evidence_header("python3 -m cartelbench.contamination " + " ".join(sys.argv[1:])),
           "provider": args.provider, "model": args.model, "answers": []}
    for q in QUESTIONS:
        r = await client.complete("You answer questions about academic literature truthfully and concisely, in JSON.", q, schema)
        out["answers"].append({"question": q, "text": r.text, "parsed": r.parsed, "refusal": r.refusal, "error": r.error,
                               "input_tokens": r.input_tokens, "output_tokens": r.output_tokens})
    path = EVIDENCE_DIR / "contamination" / f"contamination_{args.model.replace('/', '-')}.json"
    write_json(path, out)
    print(json.dumps(out["answers"], indent=2)[:4000])
    print(f"evidence: {path}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", ""))
    ap.add_argument("--api-key-env", default="OPENAI_API_KEY")
    ap.add_argument("--effort", default="low")
    args = ap.parse_args(argv)
    if args.provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set; nothing was called.", file=sys.stderr)
        return 2
    return asyncio.run(_main(args))


if __name__ == "__main__":
    raise SystemExit(main())
