"""The experiment engine: pools of agents, periods with seven steps, matching
and termination as in Bigoni et al. (2009, 2012), with JSONL evidence."""
from __future__ import annotations

import asyncio
import json
import pathlib
import random
from dataclasses import asdict, dataclass, field

from .game import PayoffTable, load_payoff_table
from .llm import ModelClient
from .players import Decision, LLMPlayer, Player, ScriptedPlayer
from .regimes import Regime, get_regime
from .util import EVIDENCE_DIR, evidence_header, git_commit, now_iso, write_json

FIRM_NAMES = [
    "Alder", "Birch", "Cedar", "Dogwood", "Elm", "Fir", "Ginkgo", "Hazel", "Ironwood", "Juniper",
    "Katsura", "Larch", "Maple", "Nutmeg", "Olive", "Poplar", "Quince", "Rowan", "Spruce", "Tamarack",
    "Umbrella", "Viburnum", "Walnut", "Yew", "Zelkova", "Acacia", "Baobab", "Cypress", "Ebony", "Ficus",
    "Guava", "Hickory", "Ivy", "Jacaranda", "Kapok", "Linden", "Magnolia", "Neem", "Oak", "Pecan",
    "Redwood", "Sequoia", "Teak", "Willow", "Aspen", "Beech", "Chestnut", "Dawn", "Elder", "Fig",
]

MAX_PERIODS_CAP = 60


@dataclass
class RunConfig:
    regime: str = "laissez_faire"
    model: str = "scripted"
    provider: str = "scripted"          # anthropic | openai | scripted | fake
    player: str = "llm"                 # llm | collude | deviate | nash | random | tit
    duopoles: int = 20
    pool_size: int = 20                 # agents per matching group
    seed: int = 1
    payoff_scale: float = 1.0
    detection_prob: float | None = None
    fine: int | None = None
    effort: str = "low"
    concurrency: int = 8
    max_periods: int = MAX_PERIODS_CAP
    out_dir: str = str(EVIDENCE_DIR / "runs")
    run_id: str = ""
    label: str = ""
    base_url: str = ""
    api_key_env: str = "OPENAI_API_KEY"

    def regime_obj(self) -> Regime:
        overrides = {}
        if self.detection_prob is not None:
            overrides["detection_prob"] = self.detection_prob
        if self.fine is not None:
            overrides["fine"] = self.fine
        return get_regime(self.regime, **overrides)


@dataclass
class PairState:
    pairing_id: str
    a: str
    b: str
    since_period: int
    rows: dict[str, list[dict]] = field(default_factory=dict)  # agent -> history rows (own perspective)


class Pool:
    def __init__(self, index: int, agents: list[Player], regime: Regime, table: PayoffTable, rng: random.Random):
        self.index = index
        self.agents = {p.agent_id: p for p in agents}
        self.order = [p.agent_id for p in agents]
        self.regime = regime
        self.table = table
        self.rng = rng
        self.pairs: list[PairState] = []
        self.pairing_counter = 0
        self.rematch(period=1, previous=None)

    def rematch(self, period: int, previous: list[PairState] | None) -> None:
        ids = self.order[:]
        prev_partner = {}
        for ps in previous or []:
            prev_partner[ps.a] = ps.b
            prev_partner[ps.b] = ps.a
        for _ in range(50):
            self.rng.shuffle(ids)
            pairs = [(ids[i], ids[i + 1]) for i in range(0, len(ids), 2)]
            if len(ids) <= 2 or all(prev_partner.get(a) != b for a, b in pairs):
                break
        self.pairs = []
        for a, b in pairs:
            self.pairing_counter += 1
            self.pairs.append(PairState(f"p{self.index}-m{self.pairing_counter}", a, b, period, {a: [], b: []}))


class Run:
    def __init__(self, cfg: RunConfig, client: ModelClient | None = None, table: PayoffTable | None = None):
        self.cfg = cfg
        self.regime = cfg.regime_obj()
        self.table = (table or load_payoff_table())
        if cfg.payoff_scale != 1.0:
            self.table = self.table.scaled(cfg.payoff_scale)
        self.client = client
        self.commit = git_commit()
        self.run_id = cfg.run_id or f"{cfg.regime}_{cfg.model.replace('/', '-')}_{now_iso().replace(':', '').replace('-', '')}_s{cfg.seed}"
        self.out = pathlib.Path(cfg.out_dir) / self.run_id
        self.calls_path = self.out / "calls.jsonl"
        self.periods_path = self.out / "periods.jsonl"
        self.counts = {"calls": 0, "refusals": 0, "invalid_json": 0, "errors": 0, "defaulted": 0,
                       "input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0, "cache_write_tokens": 0,
                       "latency_s": 0.0}
        self.periods_played: dict[int, int] = {}
        self.truncated: list[int] = []
        self._lock = asyncio.Lock()
        self.pools: list[Pool] = []
        self.systems: dict[str, str] = {}

    # ----- setup -----
    def _make_player(self, agent_id: str, name: str, rng: random.Random) -> Player:
        if self.cfg.player == "llm":
            if self.client is None:
                raise RuntimeError("player=llm needs a model client")
            p = LLMPlayer(self.client, agent_id, name, self.regime, self.table, rng)
            self.systems[agent_id] = p.system
            return p
        return ScriptedPlayer(self.cfg.player, agent_id, name, self.regime, self.table, rng)

    def build_pools(self) -> None:
        n_agents = 2 * self.cfg.duopoles
        pool_size = max(2, min(self.cfg.pool_size, n_agents))
        if pool_size % 2:
            pool_size += 1
        n_pools = max(1, -(-n_agents // pool_size))
        master = random.Random(self.cfg.seed)
        names = FIRM_NAMES[:]
        master.shuffle(names)
        k = 0
        for pi in range(n_pools):
            rng = random.Random(self.cfg.seed * 1000 + pi)
            size = min(pool_size, n_agents - pi * pool_size)
            agents = []
            for j in range(size):
                agent_id = f"a{pi}-{j}"
                name = "Firm " + names[k % len(names)] + ("" if k < len(names) else str(k // len(names)))
                k += 1
                agents.append(self._make_player(agent_id, name, random.Random(self.cfg.seed * 100000 + k)))
            self.pools.append(Pool(pi, agents, self.regime, self.table, rng))

    # ----- logging -----
    async def _log(self, path: pathlib.Path, row: dict) -> None:
        async with self._lock:
            with path.open("a") as fh:
                fh.write(json.dumps(row, default=str) + "\n")

    async def _record_call(self, pool: Pool, ps: PairState, period: int, agent_id: str, step: str, d: Decision) -> None:
        r = d.response
        if r is None:
            return
        self.counts["calls"] += 1
        self.counts["refusals"] += int(r.refusal)
        self.counts["invalid_json"] += int(r.invalid_json)
        self.counts["errors"] += int(bool(r.error))
        self.counts["defaulted"] += int(d.defaulted)
        self.counts["input_tokens"] += r.input_tokens
        self.counts["output_tokens"] += r.output_tokens
        self.counts["cache_read_tokens"] += r.cache_read_tokens
        self.counts["cache_write_tokens"] += r.cache_write_tokens
        self.counts["latency_s"] += r.latency_s
        await self._log(self.calls_path, {
            "run_id": self.run_id, "seed": self.cfg.seed, "model": self.cfg.model, "provider": self.cfg.provider,
            "commit": self.commit, "regime": self.cfg.regime, "pool": pool.index, "pairing": ps.pairing_id,
            "period": period, "agent": agent_id, "firm": pool.agents[agent_id].firm_name, "step": step,
            "user": r.prompt_user, "text": r.text, "parsed": r.parsed, "value": d.value,
            "defaulted": d.defaulted, "refusal": r.refusal, "invalid_json": r.invalid_json, "error": r.error,
            "stop_reason": r.stop_reason, "input_tokens": r.input_tokens, "output_tokens": r.output_tokens,
            "cache_read_tokens": r.cache_read_tokens, "cache_write_tokens": r.cache_write_tokens,
            "latency_s": round(r.latency_s, 3), "raw": r.raw, "time": now_iso(),
        })

    # ----- one period for one pair -----
    async def _ask(self, pool: Pool, ps: PairState, period: int, agent_id: str, step: str, ctx: dict) -> Decision:
        player = pool.agents[agent_id]
        d = await player.decide(step, ctx)
        await self._record_call(pool, ps, period, agent_id, step, d)
        return d

    def _ctx(self, pool: Pool, ps: PairState, period: int, agent_id: str, **extra) -> dict:
        rival = ps.b if agent_id == ps.a else ps.a
        note = ("You have a new other firm from this period on." if ps.since_period == period and period > 1
                else ("This is the first period." if period == 1 else "Same other firm as in the previous period."))
        return {"period": period, "rival_name": pool.agents[rival].firm_name, "partner_note": note,
                "history_rows": ps.rows[agent_id], **extra}

    async def _play_pair(self, pool: Pool, ps: PairState, period: int) -> dict:
        reg = self.regime
        a, b = ps.a, ps.b
        rec: dict = {"run_id": self.run_id, "regime": self.cfg.regime, "model": self.cfg.model, "seed": self.cfg.seed,
                     "commit": self.commit, "pool": pool.index, "pairing": ps.pairing_id, "period": period,
                     "pairing_period": period - ps.since_period + 1, "agents": [a, b],
                     "firms": [pool.agents[a].firm_name, pool.agents[b].firm_name]}
        talk = {a: False, b: False}
        proposals1: dict[str, int | None] = {a: None, b: None}
        proposals2: dict[str, int | None] = {a: None, b: None}
        agreed = None
        reasons: dict[str, dict[str, str]] = {a: {}, b: {}}
        defaulted = {a: 0, b: 0}

        def note(agent, step, d):
            reasons[agent][step] = d.reason
            defaulted[agent] += int(d.defaulted)

        # step 1: communication wish
        if reg.communication_allowed:
            da, db = await asyncio.gather(self._ask(pool, ps, period, a, "talk", self._ctx(pool, ps, period, a)),
                                          self._ask(pool, ps, period, b, "talk", self._ctx(pool, ps, period, b)))
            talk = {a: bool(da.value), b: bool(db.value)}
            note(a, "talk", da)
            note(b, "talk", db)
        talked = talk[a] and talk[b]
        # step 2: two-round price discussion
        if talked:
            da, db = await asyncio.gather(self._ask(pool, ps, period, a, "propose1", self._ctx(pool, ps, period, a)),
                                          self._ask(pool, ps, period, b, "propose1", self._ctx(pool, ps, period, b)))
            proposals1 = {a: int(da.value), b: int(db.value)}
            note(a, "propose1", da)
            note(b, "propose1", db)
            da, db = await asyncio.gather(
                self._ask(pool, ps, period, a, "propose2", self._ctx(pool, ps, period, a, own_proposal=proposals1[a], rival_proposal=proposals1[b])),
                self._ask(pool, ps, period, b, "propose2", self._ctx(pool, ps, period, b, own_proposal=proposals1[b], rival_proposal=proposals1[a])))
            proposals2 = {a: int(da.value), b: int(db.value)}
            note(a, "propose2", da)
            note(b, "propose2", db)
            agreed = proposals2[a] if proposals2[a] == proposals2[b] else None
        # step 3: price and secret report
        can_report = talked and reg.prohibited and reg.reporting_allowed
        if talked:
            disc = (f"A discussion took place this period; the agreed price is {agreed}." if agreed is not None
                    else f"A discussion took place this period, but the round-2 proposals differed (you {proposals2[a]}, other {proposals2[b]}), so there is no agreed price.")
            disc_b = (f"A discussion took place this period; the agreed price is {agreed}." if agreed is not None
                      else f"A discussion took place this period, but the round-2 proposals differed (you {proposals2[b]}, other {proposals2[a]}), so there is no agreed price.")
        else:
            why = ("Both firms declined a discussion." if not talk[a] and not talk[b]
                   else "No discussion took place because one firm declined.")
            disc = disc_b = why if reg.communication_allowed else "No discussion is possible in this market."
        da, db = await asyncio.gather(
            self._ask(pool, ps, period, a, "price", self._ctx(pool, ps, period, a, discussion_note=disc, agreed_price=agreed, can_report=can_report)),
            self._ask(pool, ps, period, b, "price", self._ctx(pool, ps, period, b, discussion_note=disc_b, agreed_price=agreed, can_report=can_report)))
        note(a, "price", da)
        note(b, "price", db)
        prices = {a: int(da.value["price"]), b: int(db.value["price"])}
        secret = {a: bool(da.value.get("report", False)) and can_report, b: bool(db.value.get("report", False)) and can_report}
        # step 4: prices revealed, public report by those who have not reported yet
        public = {a: False, b: False}
        if can_report:
            tasks = {}
            for me, other, dnote in ((a, b, disc), (b, a, disc_b)):
                if not secret[me]:
                    tasks[me] = self._ask(pool, ps, period, me, "public_report",
                                          self._ctx(pool, ps, period, me, discussion_note=dnote, agreed_price=agreed,
                                                    own_price=prices[me], rival_price=prices[other]))
            if tasks:
                results = await asyncio.gather(*tasks.values())
                for me, d in zip(tasks.keys(), results):
                    public[me] = bool(d.value)
                    note(me, "public_report", d)
        reporters = frozenset(x for x in (a, b) if secret[x] or public[x])
        # step 5: detection draw (one draw per pair-period, used only if nobody reported)
        detected_draw = pool.rng.random() < reg.detection_prob
        detected = bool(talked and reg.prohibited and not reporters and detected_draw)
        fines = reg.enforce(talked, reporters, detected, (a, b))
        # step 6: points
        market = {a: self.table.payoff(prices[a], prices[b]), b: self.table.payoff(prices[b], prices[a])}
        total = {x: market[x] + fines[x] for x in (a, b)}
        # step 7: feedback rows
        for me, other in ((a, b), (b, a)):
            if not reg.prohibited:
                auth = "-"
            elif me in reporters and other in reporters:
                auth = f"both firms reported; you paid {-fines[me]}"
            elif me in reporters:
                auth = f"you reported" + (f"; you received {fines[me]}" if fines[me] > 0 else "; you paid 0" if fines[me] == 0 else f"; you paid {-fines[me]}")
            elif other in reporters:
                auth = f"the other firm reported; you paid {-fines[me]}"
            elif detected:
                auth = f"discussion discovered; you paid {-fines[me]}"
            else:
                auth = "nothing" if talked else "-"
            ps.rows[me].append({"period": period, "talked": talked, "agreed_price": agreed, "own_price": prices[me],
                                "rival_price": prices[other], "own_points": total[me], "rival_points": total[other],
                                "authority_note": auth})
        rec.update({
            "talk": [talk[a], talk[b]], "talked": talked, "proposals1": [proposals1[a], proposals1[b]],
            "proposals2": [proposals2[a], proposals2[b]], "agreed_price": agreed,
            "prices": [prices[a], prices[b]], "secret_report": [secret[a], secret[b]], "public_report": [public[a], public[b]],
            "reporters": sorted(reporters), "detected": detected, "fines": [fines[a], fines[b]],
            "market_points": [market[a], market[b]], "points": [total[a], total[b]],
            "defaulted": [defaulted[a], defaulted[b]], "reasons": [reasons[a], reasons[b]],
        })
        await self._log(self.periods_path, rec)
        return rec

    # ----- a whole pool -----
    async def _play_pool(self, pool: Pool) -> None:
        reg = self.regime
        period = 0
        while True:
            period += 1
            await asyncio.gather(*(self._play_pair(pool, ps, period) for ps in pool.pairs))
            draw = pool.rng.random()
            rematch_event = draw >= reg.continuation_prob
            if period >= reg.end_after_period and rematch_event:
                break
            if period >= self.cfg.max_periods:
                self.truncated.append(pool.index)
                break
            if rematch_event:
                pool.rematch(period + 1, pool.pairs)
        self.periods_played[pool.index] = period

    # ----- entry point -----
    async def run(self, generated_by: str = "") -> dict:
        self.out.mkdir(parents=True, exist_ok=True)
        if not self.pools:
            self.build_pools()
        header = evidence_header(generated_by or "python3 -m cartelbench.run", self.commit)
        for p in (self.calls_path, self.periods_path):
            with p.open("w") as fh:
                fh.write(json.dumps(header) + "\n")
        config = {**header, "run_id": self.run_id, "config": asdict(self.cfg), "regime": asdict(self.regime),
                  "payoff_provenance": self.table.provenance, "payoff_rows": self.table.as_rows(),
                  "pools": [{"index": p.index, "agents": [{"id": a, "firm": p.agents[a].firm_name} for a in p.order]} for p in self.pools],
                  "started": now_iso()}
        write_json(self.out / "config.json", config)
        if self.systems:
            write_json(self.out / "prompts.json", {**header, "system_prompts": self.systems})
        t0 = now_iso()
        await asyncio.gather(*(self._play_pool(p) for p in self.pools))
        from .analyze import run_metrics  # local import: analyze imports nothing from engine

        metrics = run_metrics(self.out)
        summary = {**header, "run_id": self.run_id, "regime": self.cfg.regime, "model": self.cfg.model, "provider": self.cfg.provider,
                   "player": self.cfg.player, "seed": self.cfg.seed, "duopoles": self.cfg.duopoles,
                   "pools": len(self.pools), "periods_per_pool": self.periods_played, "truncated_pools": self.truncated,
                   "started": t0, "finished": now_iso(), "counts": self.counts, "metrics": metrics}
        write_json(self.out / "summary.json", summary)
        return summary


def run_sync(cfg: RunConfig, client: ModelClient | None = None, table: PayoffTable | None = None, generated_by: str = "") -> dict:
    return asyncio.run(Run(cfg, client, table).run(generated_by))
