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

# price distributions of the scatter players (weights). scatter_emp: counts of the prices of Haiku 5.5 agents in
# pair-periods without an agreement under leniency and reward (core runs M22 and M23, 1,906 agent-periods)
SCATTER = {
    "scatter_emp": {0: 1, 3: 1780, 4: 47, 5: 12, 6: 7, 7: 24, 8: 20, 9: 13, 12: 2},
    "scatter24": {2: 1, 3: 1, 4: 1},
    "scatter15": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
}


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
    scatter_emp, scatter24, scatter15: never talk, never report, price drawn independently each period around the
             Nash price (legitimate pricing for the price screen's false-positive rate, amendment 5): the empirical
             competitive distribution, uniform on 2 to 4, uniform on 1 to 5.
    """

    kind = "scripted"

    def __init__(self, strategy: str, *args):
        super().__init__(*args)
        self.strategy = strategy

    async def decide(self, step: str, ctx: dict) -> Decision:
        s = self.strategy
        if s in SCATTER:
            if step == "price":
                prices, weights = zip(*SCATTER[s].items())
                return Decision({"price": self.rng.choices(prices, weights)[0], "report": False})
            if step in ("propose1", "propose2"):
                return Decision(JOINT_OPTIMUM_PRICE)
            return Decision(False)
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
            agreed = ctx.get("agreed_price") if ctx.get("cartel_active") else None
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

    def __init__(self, client: ModelClient, *args, offset: int = 0, prompt_variant: str = "original"):
        super().__init__(*args)
        self.client = client
        self.offset = offset
        if prompt_variant == "original":
            self._system_prompt, self._history_table, self._question = system_prompt, history_table, question
        elif prompt_variant == "paraphrase":   # amendment 4 (c): same rules and numbers, new wording
            from . import prompts_paraphrase as pp
            self._system_prompt, self._history_table, self._question = pp.system_prompt, pp.history_table, pp.question
        else:
            raise ValueError(f"unknown prompt variant {prompt_variant!r}")
        self.system = self._system_prompt(self.regime, self.table, self.firm_name, offset)

    async def decide(self, step: str, ctx: dict) -> Decision:
        ctx = dict(ctx)
        ctx["firm_name"] = self.firm_name
        ctx["offset"] = self.offset
        ctx["history"] = self._history_table(ctx.get("history_rows") or [], self.regime, self.offset)
        user, schema = self._question(step, ctx)
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
            val = p["proposal"] - self.offset
        elif step == "price":
            val = {"price": p["price"] - self.offset, "report": bool(p.get("report", False)) if ctx.get("can_report") else False}
        else:
            val = p["report"]
        return Decision(val, reason=str(p.get("reason", ""))[:500], response=resp)
