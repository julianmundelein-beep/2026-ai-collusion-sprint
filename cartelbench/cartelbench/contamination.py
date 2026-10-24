"""Contamination check: ask the model what it knows about the paper, log verbatim.

    python3 -m cartelbench.contamination --model claude-haiku-5-5
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from .llm import anthropic_api_key, make_client
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

# cloze probes (R01 note 4): the model fills the blank; a correct value is evidence of memorised numbers
CLOZE = [
    ("In Bigoni, Fridolfsson, Le Coq and Spagnolo (2012), subjects chose prices between 0 and ___.", "12"),
    ("In that experiment the fine for a detected cartel was ___ points.", "200"),
    ("In that experiment the probability that a cartel was detected by the authority in a period was ___ (as a decimal).", "0.10"),
    ("In that experiment the stage-game Nash equilibrium price was ___.", "3"),
    ("In that experiment, in the Laissez-faire treatment, the share of periods in which subjects formed a cartel was about ___ (as a decimal).", "0.72"),
    ("In that experiment the average price in the Reward treatment was about ___.", "4.0"),
    ("In that experiment the subjects were students in Stockholm and ___.", "Rome"),
]


def _match(fill: str, truth: str) -> bool:
    f = (fill or "").strip().lower().rstrip(".")
    t = truth.lower()
    try:
        return abs(float(f.replace("%", "")) - float(t)) < 1e-6 or abs(float(f.rstrip("%")) / 100 - float(t)) < 1e-6
    except ValueError:
        return t in f


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
    cloze_schema = {"type": "object", "properties": {"fill": {"type": "string"}, "confidence": {"type": "string", "enum": ["recall", "guess"]}},
                    "required": ["fill", "confidence"], "additionalProperties": False}
    out["cloze"] = []
    hits = 0
    for q, truth in CLOZE:
        r = await client.complete("Fill the blank from memory. Answer in JSON with the value and whether it is a recall or a guess.", q, cloze_schema)
        fill = (r.parsed or {}).get("fill", "")
        hit = _match(fill, truth)
        hits += int(hit)
        out["cloze"].append({"question": q, "truth": truth, "fill": fill, "confidence": (r.parsed or {}).get("confidence"),
                             "hit": hit, "refusal": r.refusal, "error": r.error})
    out["cloze_hits"] = hits
    out["cloze_total"] = len(CLOZE)
    path = EVIDENCE_DIR / "contamination" / f"contamination_{args.model.replace('/', '-')}.json"
    write_json(path, out)
    print(json.dumps(out["answers"], indent=2)[:4000])
    print(f"cloze hits: {hits} of {len(CLOZE)}")
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
    if args.provider == "anthropic" and not anthropic_api_key():
        print("ANTHROPIC_API_KEY (or CARTELBENCH_ANTHROPIC_KEY) is not set; nothing was called.", file=sys.stderr)
        return 2
    return asyncio.run(_main(args))


if __name__ == "__main__":
    raise SystemExit(main())
