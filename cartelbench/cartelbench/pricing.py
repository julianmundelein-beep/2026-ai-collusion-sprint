"""USD per million tokens, Anthropic first-party API (skill claude-api, cached 2026-10-06).
Cache reads are billed at a tenth of the input price (Opus 5.5: 0.20 USD per million, a twentieth), cache writes at 1.25 times. Haiku 5.5 prices hold up
to 100K prompt tokens, which every call here stays under. Unknown models cost 0 and are flagged."""
from __future__ import annotations

PRICES_USD_PER_M = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-6": (5.00, 25.00),
}

CACHE_READ_USD_PER_M = {"claude-opus-5-5": 0.20}


def cost_usd(model: str, input_tokens: int, output_tokens: int, cache_read: int = 0, cache_write: int = 0) -> float | None:
    if model not in PRICES_USD_PER_M:
        return None
    pi, po = PRICES_USD_PER_M[model]
    # Anthropic usage: input_tokens excludes cached and cache-written tokens, which come in their own fields
    pc = CACHE_READ_USD_PER_M.get(model, pi * 0.1)
    return (input_tokens * pi + cache_read * pc + cache_write * pi * 1.25 + output_tokens * po) / 1e6
