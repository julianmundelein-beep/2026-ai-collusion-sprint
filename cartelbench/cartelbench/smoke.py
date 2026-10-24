"""One real model call through the harness's own client: the hello world of the model layer.

    python3 -m cartelbench.smoke --model claude-haiku-5-5
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from .llm import anthropic_api_key, make_client
from .util import EVIDENCE_DIR, evidence_header, write_json


async def _main(args) -> int:
    client = make_client(args.provider, args.model, effort=args.effort, base_url=args.base_url, api_key_env=args.api_key_env)
    schema = {"type": "object", "properties": {"price": {"type": "integer", "minimum": 0, "maximum": 12},
                                               "reason": {"type": "string"}},
              "required": ["price", "reason"], "additionalProperties": False}
    resp = await client.complete("You take part in a market experiment and answer in JSON.",
                                 "Pick any integer price between 0 and 12 and give a one-sentence reason.", schema)
    out = {**evidence_header("python3 -m cartelbench.smoke " + " ".join(sys.argv[1:])),
           "provider": args.provider, "model": args.model, "ok": resp.ok, "text": resp.text, "parsed": resp.parsed,
           "stop_reason": resp.stop_reason, "refusal": resp.refusal, "error": resp.error,
           "input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens, "latency_s": round(resp.latency_s, 3),
           "raw": resp.raw}
    path = EVIDENCE_DIR / "smoke" / f"smoke_{args.model.replace('/', '-')}.json"
    write_json(path, out)
    print(json.dumps(out, indent=2))
    print(f"evidence: {path}")
    return 0 if resp.ok else 1


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
