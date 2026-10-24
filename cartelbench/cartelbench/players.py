"""Players: scripted strategies (no API) and the LLM seller."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from .game import NASH_PRICE, JOINT_OPTIMUM_PRICE, PayoffTable
from .llm import ModelClient, ModelResponse
from .prompts import history_table, question, system_prompt
from .regimes import Regime

DEFAULT_ACTION = {"talk": False, "proposal": JOINT_OPTIMUM_PRICE, "price": NASH_PRICE, "report": False}


@dataclass
class Decision:
    value: Any
    reason: str = ""
    response: ModelResponse | None = None
    defaulted: bool = False


class Player:
    kind = "base"

    def __init__(self, agent_id: str, firm_name: str, regime: Regime, table: PayoffTable, rng: random.Random):
        self.agent_id = agent_id
        self.firm_name = firm_name
        self.regime = regime
        self.table = table
        self.rng = rng

    async def decide(self, step: str, ctx: dict) -> Decision:
        raise NotImplementedError


class ScriptedPlayer(Player):
    """Strategies used by the tests and as the naive baseline.

    collude: always talk, propose 9, set the agreed price (or 9), never report.
    deviate: always talk, propose 9, undercut with the best reply to the agreed price, report secretly.
    nash:    never talk, price 3, never report.
    random:  uniform choices everywhere.
    tit:     talk, propose 9; set agreed price unless the rival undercut last period, then price 3; never report.
    """

    kind = "scripted"

    def __init__(self, strategy: str, *args):
        super().__init__(*args)
        self.strategy = strategy

    async def decide(self, step: str, ctx: dict) -> Decision:
        s = self.strategy
        if s == "random":
            if step == "talk":
                return Decision(self.rng.random() < 0.5)
            if step in ("propose1", "propose2"):
                return Decision(self.rng.randint(0, 12))
            if step == "price":
                return Decision({"price": self.rng.randint(0, 12), "report": self.rng.random() < 0.5})
            return Decision(self.rng.random() < 0.5)
        if step == "talk":
            return Decision(s != "nash")
        if step in ("propose1", "propose2"):
            return Decision(JOINT_OPTIMUM_PRICE)
        if step == "price":
            agreed = ctx.get("agreed_price")
            if s == "nash":
                return Decision({"price": NASH_PRICE, "report": False})
            if s == "collude":
                return Decision({"price": agreed if agreed is not None else JOINT_OPTIMUM_PRICE, "report": False})
            if s == "deviate":
                target = agreed if agreed is not None else JOINT_OPTIMUM_PRICE
                return Decision({"price": self.table.best_reply(target), "report": bool(ctx.get("can_report"))})
            if s == "tit":
                hist = ctx.get("history_rows") or []
                if hist and hist[-1]["agreed_price"] is not None and hist[-1]["rival_price"] < hist[-1]["agreed_price"]:
                    return Decision({"price": NASH_PRICE, "report": False})
                return Decision({"price": agreed if agreed is not None else JOINT_OPTIMUM_PRICE, "report": False})
        if step == "public_report":
            return Decision(s == "deviate")
        raise ValueError(step)


class LLMPlayer(Player):
    kind = "llm"

    def __init__(self, client: ModelClient, *args):
        super().__init__(*args)
        self.client = client
        self.system = system_prompt(self.regime, self.table, self.firm_name)

    async def decide(self, step: str, ctx: dict) -> Decision:
        ctx = dict(ctx)
        ctx["firm_name"] = self.firm_name
        ctx["history"] = history_table(ctx.get("history_rows") or [], self.regime)
        user, schema = question(step, ctx)
        resp = await self.client.complete(self.system, user, schema)
        resp.prompt_user = user
        if not resp.ok:
            if step == "price":
                val = {"price": DEFAULT_ACTION["price"], "report": False}
            else:
                key = {"talk": "talk", "propose1": "proposal", "propose2": "proposal", "public_report": "report"}[step]
                val = DEFAULT_ACTION[key]
            return Decision(val, reason="", response=resp, defaulted=True)
        p = resp.parsed
        if step == "talk":
            val = p["talk"]
        elif step in ("propose1", "propose2"):
            val = p["proposal"]
        elif step == "price":
            val = {"price": p["price"], "report": bool(p.get("report", False)) if ctx.get("can_report") else False}
        else:
            val = p["report"]
        return Decision(val, reason=str(p.get("reason", ""))[:500], response=resp)
