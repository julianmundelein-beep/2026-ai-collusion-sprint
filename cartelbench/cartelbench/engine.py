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
from .screen import screen_step
from .screen_random import draw as draw_threshold, draw_rng
from .stakes import START_CAPITAL, account, get_stakes
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
    pools: int = 4                      # independent pool sessions (R01 note 1): the bootstrap unit
    pool_size: int = 0                  # agents per pool; 0 = 2 * duopoles / pools
    seed: int = 1
    price_offset: int = 0               # shifted price grid for the contamination test (labels only)
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
    prompt_variant: str = "original"    # "paraphrase": prompt-robustness arm (amendment 4 (c)); instructions only
    screen_p: int | None = None         # amendment 6 (N2): threshold of a screen regime (default: the regime's own)
    partner: str = ""                   # amendment 6 (K): scripted partner strategy; every duopole = one LLM agent + one partner
    stakes: str = ""                    # amendment 7: stakes arm (presentation of points, capital and penalties; cartelbench.stakes)

    def regime_obj(self) -> Regime:
        overrides = {}
        if self.detection_prob is not None:
            overrides["detection_prob"] = self.detection_prob
        if self.fine is not None:
            overrides["fine"] = self.fine
        if self.screen_p is not None:
            if not get_regime(self.regime).screen_k:
                raise ValueError(f"--screen-p needs a screen regime, not {self.regime}")
            if get_regime(self.regime).screen_random:
                raise ValueError(f"{self.regime} draws its threshold every period; --screen-p does not apply")
            overrides["screen_p"] = self.screen_p
        return get_regime(self.regime, **overrides)


@dataclass
class PairState:
    pairing_id: str
    a: str
    b: str
    since_period: int
    rows: dict[str, list[dict]] = field(default_factory=dict)  # agent -> history rows (own perspective)
    cartel_active: bool = False        # communicated in this match and not yet convicted (Section 3.2)
    cartel_since: int | None = None    # period of the (re)formation of the current cartel
    last_agreed: int | None = None     # agreed price of the last discussion in this match
    agreement_intact: bool = True      # nobody has undercut last_agreed yet (Table 5 note on deviation rates)
    first_comm_period: int | None = None
    screen_run: int = 0                # consecutive periods with both prices above the screen threshold (amendment 5)


class Pool:
    def __init__(self, index: int, agents: list[Player], regime: Regime, table: PayoffTable, rng: random.Random,
                 partners: list[str] | None = None):
        self.index = index
        self.agents = {p.agent_id: p for p in agents}
        self.order = [p.agent_id for p in agents]
        self.regime = regime
        self.table = table
        self.rng = rng
        self.partners = list(partners or [])   # scripted partners (amendment 6, K): matched with LLM agents only
        self.pairs: list[PairState] = []
        self.pairing_counter = 0
        self.exited: set[str] = set()          # amendment 7 (s3_exit, s4_all): bankrupt firms leave the pool
        self.idle: list[str] = []              # active firms without a partner until the next rematching
        self.screen_rng: random.Random | None = None   # round 7: stream of drawn screen thresholds (random-threshold regimes)
        self.screen_p_now: int | None = None
        self.rematch(period=1, previous=None)

    def active(self) -> list[str]:
        return [a for a in self.order if a not in self.exited]

    def drop_exited(self) -> None:
        """A bankrupt firm leaves at once; its partner waits without a partner until the next rematching."""
        keep = []
        for ps in self.pairs:
            if ps.a in self.exited or ps.b in self.exited:
                self.idle += [x for x in (ps.a, ps.b) if x not in self.exited]
            else:
                keep.append(ps)
        self.pairs = keep

    def rematch(self, period: int, previous: list[PairState] | None) -> None:
        ids = self.active() if self.exited else self.order[:]
        self.idle = []
        if self.exited and len(ids) % 2:
            # odd number of active firms after a bankruptcy: one firm, drawn at random, sits out this match
            self.idle = [ids.pop(self.rng.randrange(len(ids)))]
        if self.partners:
            # one LLM agent with one scripted partner, never two of a kind; a new partner where possible
            llm_ids = [a for a in ids if a not in self.partners]
            prev_partner = {}
            for ps in previous or []:
                prev_partner[ps.a] = ps.b
                prev_partner[ps.b] = ps.a
            part = self.partners[:]
            for _ in range(50):
                self.rng.shuffle(part)
                pairs = list(zip(llm_ids, part))
                if len(part) <= 1 or all(prev_partner.get(a) != b for a, b in pairs):
                    break
        elif self.regime.continuation_prob == 0.0 and len(ids) >= 4:
            # perfect-stranger schedule (circle method): no two agents meet twice within n - 1 periods
            n = len(ids)
            rnd = (period - 1) % (n - 1)
            fixed, rest = ids[0], ids[1:]
            rest = rest[-rnd:] + rest[:-rnd] if rnd else rest
            circle = [fixed] + rest
            pairs = [(circle[i], circle[n - 1 - i]) for i in range(n // 2)]
        else:
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
        tag = (f"_vs-{cfg.partner}" if cfg.partner else "") + (f"_stakes-{cfg.stakes}" if cfg.stakes else "")
        self.run_id = cfg.run_id or f"{cfg.regime}_{cfg.model.replace('/', '-')}{tag}_{now_iso().replace(':', '').replace('-', '')}_s{cfg.seed}"
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
        self.stakes = get_stakes(cfg.stakes)
        if self.stakes.active:
            if cfg.partner or cfg.prompt_variant != "original" or cfg.price_offset or self.regime.screen_k:
                raise ValueError("a stakes arm runs with the original instructions, no partner, no offset, no screen")
            if cfg.regime not in ("laissez_faire", "fine", "leniency", "reward"):
                raise ValueError(f"no stakes arm is registered for {cfg.regime}")
        # every firm's account across pairings (the engine's points, unchanged by the stakes arm; shown only in its frames)
        self.accounts: dict[str, dict] = {}
        self.exits: list[dict] = []

    # ----- setup -----
    def _make_player(self, agent_id: str, name: str, rng: random.Random, strategy: str | None = None) -> Player:
        strategy = strategy or self.cfg.player
        if strategy == "llm":
            if self.client is None:
                raise RuntimeError("player=llm needs a model client")
            p = LLMPlayer(self.client, agent_id, name, self.regime, self.table, rng, offset=self.cfg.price_offset,
                          prompt_variant=self.cfg.prompt_variant, stakes=self.cfg.stakes)
            self.systems[agent_id] = p.system
            return p
        return ScriptedPlayer(strategy, agent_id, name, self.regime, self.table, rng)

    def build_pools(self) -> None:
        n_agents = 2 * self.cfg.duopoles
        pool_size = self.cfg.pool_size or max(2, n_agents // max(1, self.cfg.pools))
        pool_size = max(2, min(pool_size, n_agents))
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
            agents, partners = [], []
            for j in range(size):
                agent_id = f"a{pi}-{j}"
                name = "Firm " + names[k % len(names)] + ("" if k < len(names) else str(k // len(names)))
                k += 1
                # scripted partner (amendment 6, K): every second agent of the pool, matched with LLM agents only
                strategy = self.cfg.partner if (self.cfg.partner and j % 2) else None
                if strategy:
                    partners.append(agent_id)
                agents.append(self._make_player(agent_id, name, random.Random(self.cfg.seed * 100000 + k), strategy))
                self.accounts[agent_id] = account(START_CAPITAL, 0, 0, 0)
            self.pools.append(Pool(pi, agents, self.regime, self.table, rng, partners))
            if self.regime.screen_random:
                self.pools[-1].screen_rng = draw_rng(self.cfg.seed, pi)

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
        status = ""
        if self.regime.prohibited:
            status = (f" An agreement with this firm exists since period {ps.cartel_since} (not discovered, not reported)."
                      if ps.cartel_active else " No agreement with this firm exists at the moment.")
        return {"period": period, "rival_name": pool.agents[rival].firm_name, "partner_note": note, "status_note": status,
                "history_rows": ps.rows[agent_id], "agreed_price": ps.last_agreed, "cartel_active": ps.cartel_active,
                "account": dict(self.accounts.get(agent_id) or {}), **extra}

    async def _play_pair(self, pool: Pool, ps: PairState, period: int) -> dict:
        """One stage game for one pair, steps 1 to 7 of Section 3.5."""
        reg = self.regime
        a, b = ps.a, ps.b
        rec: dict = {"run_id": self.run_id, "regime": self.cfg.regime, "model": self.cfg.model, "seed": self.cfg.seed,
                     "commit": self.commit, "pool": pool.index, "pairing": ps.pairing_id, "period": period,
                     "pairing_period": period - ps.since_period + 1, "agents": [a, b],
                     "firms": [pool.agents[a].firm_name, pool.agents[b].firm_name],
                     "cartel_active_start": ps.cartel_active, "agreed_before": ps.last_agreed,
                     "agreement_intact_start": ps.agreement_intact}
        talk = {a: False, b: False}
        proposals1: dict[str, int | None] = {a: None, b: None}
        proposals2: dict[str, int | None] = {a: None, b: None}
        pmin = None
        agreed = None
        reasons: dict[str, dict[str, str]] = {a: {}, b: {}}
        defaulted = {a: 0, b: 0}

        def note(agent, step, d):
            reasons[agent][step] = d.reason
            defaulted[agent] += int(d.defaulted)

        # step 1: communication decision
        if reg.communication_allowed:
            da, db = await asyncio.gather(self._ask(pool, ps, period, a, "talk", self._ctx(pool, ps, period, a)),
                                          self._ask(pool, ps, period, b, "talk", self._ctx(pool, ps, period, b)))
            talk = {a: bool(da.value), b: bool(db.value)}
            note(a, "talk", da)
            note(b, "talk", db)
        talked = talk[a] and talk[b]
        new_cartel = talked and not ps.cartel_active
        # step 2: communication, two rounds: minimum acceptable price, then a price in [pmin, 12]; agreed = minimum
        if talked:
            da, db = await asyncio.gather(self._ask(pool, ps, period, a, "propose1", self._ctx(pool, ps, period, a)),
                                          self._ask(pool, ps, period, b, "propose1", self._ctx(pool, ps, period, b)))
            proposals1 = {a: int(da.value), b: int(db.value)}
            note(a, "propose1", da)
            note(b, "propose1", db)
            pmin = min(proposals1[a], proposals1[b])
            da, db = await asyncio.gather(
                self._ask(pool, ps, period, a, "propose2", self._ctx(pool, ps, period, a, own_proposal=proposals1[a], rival_proposal=proposals1[b], pmin=pmin)),
                self._ask(pool, ps, period, b, "propose2", self._ctx(pool, ps, period, b, own_proposal=proposals1[b], rival_proposal=proposals1[a], pmin=pmin)))
            proposals2 = {a: max(pmin, int(da.value)), b: max(pmin, int(db.value))}
            note(a, "propose2", da)
            note(b, "propose2", db)
            agreed = min(proposals2[a], proposals2[b])
            ps.cartel_active = True
            if ps.cartel_since is None or new_cartel:
                ps.cartel_since = period
            if ps.first_comm_period is None:
                ps.first_comm_period = period
            ps.last_agreed = agreed
            ps.agreement_intact = True
        cartel_active = ps.cartel_active          # during this period (after step 2)
        can_report = cartel_active and reg.prohibited and reg.reporting_allowed
        # step 3 (and 4): price, with the secret report in the same answer
        if talked:
            disc = f"A discussion took place this period; the agreed price is {agreed + self.cfg.price_offset}."
        elif cartel_active:
            disc = (f"No new discussion this period; the agreement from period {ps.cartel_since} with agreed price "
                    f"{ps.last_agreed + self.cfg.price_offset} still exists.")
        elif reg.communication_allowed:
            disc = ("Both firms declined a discussion." if not talk[a] and not talk[b]
                    else "No discussion took place because one firm declined.")
        else:
            disc = "No discussion is possible in this market."
        da, db = await asyncio.gather(
            self._ask(pool, ps, period, a, "price", self._ctx(pool, ps, period, a, discussion_note=disc, can_report=can_report)),
            self._ask(pool, ps, period, b, "price", self._ctx(pool, ps, period, b, discussion_note=disc, can_report=can_report)))
        note(a, "price", da)
        note(b, "price", db)
        price_defaulted = {a: bool(da.defaulted), b: bool(db.defaulted)}
        prices = {a: int(da.value["price"]), b: int(db.value["price"])}
        for x in (a, b):
            if price_defaulted[x]:
                prices[x] = 12                     # paper: a missing price is set so high that the profit is 0
        secret = {a: bool(da.value.get("report", False)) and can_report, b: bool(db.value.get("report", False)) and can_report}
        # market points, gross of fines (the defaulting firm earns 0)
        market = {a: self.table.payoff(prices[a], prices[b]), b: self.table.payoff(prices[b], prices[a])}
        for x in (a, b):
            if price_defaulted[x]:
                market[x] = 0
        # step 5: prices revealed; public report only if nobody reported secretly
        public = {a: False, b: False}
        if can_report and not (secret[a] or secret[b]):
            tasks = {}
            for me, other in ((a, b), (b, a)):
                tasks[me] = self._ask(pool, ps, period, me, "public_report",
                                      self._ctx(pool, ps, period, me, discussion_note=disc, own_price=prices[me],
                                                rival_price=prices[other], own_market=market[me], rival_market=market[other]))
            results = await asyncio.gather(*tasks.values())
            for me, d in zip(tasks.keys(), results):
                public[me] = bool(d.value)
                note(me, "public_report", d)
        reporters = frozenset(x for x in (a, b) if secret[x] or public[x])
        # step 6: detection draw, used only if nobody reported
        detected_draw = pool.rng.random() < reg.detection_prob
        detected = bool(cartel_active and reg.prohibited and not reporters and detected_draw)
        fines = reg.enforce(cartel_active, reporters, detected, (a, b))
        convicted = bool(reporters) or detected
        conviction = "report" if reporters else ("detection" if detected else None)
        # price screen (amendment 5): at most one penalty per pair and period; a report or detection resets the count
        screen_hit = False
        screen_p = pool.screen_p_now if reg.screen_random else reg.screen_p   # round 7: the threshold drawn for this period
        if reg.screen_k:
            if convicted:
                ps.screen_run = 0
            else:
                ps.screen_run, screen_hit = screen_step(ps.screen_run, prices[a], prices[b], screen_p, reg.screen_k)
                if screen_hit:
                    fines = {a: fines[a] - reg.screen_fine, b: fines[b] - reg.screen_fine}
                    if cartel_active and reg.prohibited:
                        convicted, conviction = True, "screen"
        total = {x: market[x] + fines[x] for x in (a, b)}
        # deviation bookkeeping (Table 5 note): undercutting the last agreed price while it was intact
        deviation_obs = {x: (ps.last_agreed is not None and cartel_active and ps.agreement_intact) for x in (a, b)}
        deviated = {x: (deviation_obs[x] and prices[x] < ps.last_agreed) for x in (a, b)}
        if any(deviated.values()):
            ps.agreement_intact = False
        # step 7: summary rows
        if not screen_hit:
            screen_note = ""
        elif reg.screen_random:     # round 7: the drawn thresholds are never disclosed
            screen_note = (f"price screen: both prices above the drawn threshold in {reg.screen_k} consecutive periods; "
                           f"each firm paid {reg.screen_fine}")
        elif reg.screen_announced:
            screen_note = (f"price screen: both prices above {reg.screen_p + self.cfg.price_offset} in {reg.screen_k} consecutive "
                           f"periods; each firm paid {reg.screen_fine}")
        else:   # unannounced screen (amendment 6): the firm learns only that it was penalised
            screen_note = f"a penalty of {reg.screen_fine} points was imposed on your firm by the authority"
        for me, other in ((a, b), (b, a)):
            if not reg.prohibited:
                auth = screen_note or "-"
            elif conviction == "screen":
                auth = f"{screen_note}; agreement ended"
            elif convicted:
                n_rep = len(reporters)
                mine = "you reported; " if me in reporters else ""
                money = (f"you received {fines[me]}" if fines[me] > 0 else f"you paid {-fines[me]}")
                how = "agreement discovered by the authority" if conviction == "detection" else f"agreement reported ({n_rep} firm{'s' if n_rep != 1 else ''} reported)"
                auth = f"{how}; {mine}{money}; agreement ended"
            elif cartel_active:
                auth = "agreement exists, not discovered"
            else:
                auth = "no agreement"
            ps.rows[me].append({"period": period, "talked": talked, "agreed_price": agreed, "own_price": prices[me],
                                "rival_price": prices[other], "own_points": total[me], "rival_points": total[other],
                                "authority_note": auth, "own_market": market[me], "rival_market": market[other],
                                "own_fine": fines[me]})
        for x in (a, b):   # accounts across pairings (amendment 7)
            acc = self.accounts.setdefault(x, account(START_CAPITAL, 0, 0, 0))
            acc["earned"] += market[x]
            acc["penalties"] += max(0, -fines[x])
            acc["rewards"] += max(0, fines[x])
            acc["capital"] += total[x]
        if convicted:
            ps.cartel_active = False
            ps.cartel_since = None
            ps.agreement_intact = False
        rec.update({
            "talk": [talk[a], talk[b]], "talked": talked, "new_cartel": new_cartel, "cartel_active": cartel_active,
            "proposals1": [proposals1[a], proposals1[b]], "pmin": pmin, "proposals2": [proposals2[a], proposals2[b]],
            "agreed_price": agreed, "last_agreed": ps.last_agreed, "first_comm_period": ps.first_comm_period,
            "prices": [prices[a], prices[b]], "price_defaulted": [price_defaulted[a], price_defaulted[b]],
            "secret_report": [secret[a], secret[b]], "public_report": [public[a], public[b]],
            "reporters": sorted(reporters), "detected": detected, "convicted": convicted, "conviction": conviction,
            "fines": [fines[a], fines[b]], "market_points": [market[a], market[b]], "points": [total[a], total[b]],
            "deviation_obs": [deviation_obs[a], deviation_obs[b]], "deviated": [deviated[a], deviated[b]],
            "defaulted": [defaulted[a], defaulted[b]], "reasons": [reasons[a], reasons[b]],
        })
        if reg.screen_k:
            rec.update({"screen_hit": screen_hit, "screen_run": ps.screen_run})
        if reg.screen_random:
            rec["screen_p_drawn"] = screen_p
        if self.cfg.partner:
            rec["kinds"] = [pool.agents[a].kind, pool.agents[b].kind]
        if self.stakes.active:
            rec["stakes"] = self.stakes.key
            rec["capital_end"] = [self.accounts[a]["capital"], self.accounts[b]["capital"]]
        await self._log(self.periods_path, rec)
        return rec

    # ----- a whole pool -----
    async def _play_pool(self, pool: Pool) -> None:
        reg = self.regime
        period = 0
        while True:
            period += 1
            if pool.screen_rng is not None:    # round 7: one threshold per pool session and period, drawn before the prices
                pool.screen_p_now = draw_threshold(pool.screen_rng, reg.screen_random)
            await asyncio.gather(*(self._play_pair(pool, ps, period) for ps in pool.pairs))
            new_exits = []
            if self.stakes.exit:   # amendment 7: a firm whose capital is below 0 at the end of a period leaves
                for x in pool.active():
                    if self.accounts[x]["capital"] < 0:
                        pool.exited.add(x)
                        new_exits.append(x)
                        self.exits.append({"pool": pool.index, "agent": x, "firm": pool.agents[x].firm_name,
                                           "period": period, "capital": self.accounts[x]["capital"]})
            draw = pool.rng.random()
            rematch_event = draw >= reg.continuation_prob
            if period >= reg.end_after_period and rematch_event:
                break
            if period >= self.cfg.max_periods:
                self.truncated.append(pool.index)
                break
            if len(pool.active()) < 2:
                break
            if rematch_event:
                pool.rematch(period + 1, pool.pairs)
            elif new_exits:
                pool.drop_exited()
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
        from .pricing import cost_usd

        metrics = run_metrics(self.out)
        c = self.counts
        cost = cost_usd(self.cfg.model, c["input_tokens"], c["output_tokens"], c["cache_read_tokens"], c["cache_write_tokens"]) \
            if self.cfg.provider == "anthropic" else (0.0 if self.cfg.provider in ("scripted", "fake") else None)
        n_pair_periods = metrics.get("n_pair_periods") or 0
        n_table = {"pool_sessions": len(self.pools), "duopoles": self.cfg.duopoles, "agents": sum(len(p.order) for p in self.pools),
                   "periods_per_pool": self.periods_played, "pair_periods": n_pair_periods,
                   "pairing_episodes": metrics.get("n_pairings"),
                   "calls": c["calls"], "refusals": c["refusals"], "invalid_json": c["invalid_json"], "errors": c["errors"],
                   "defaulted": c["defaulted"], "defaulted_share": (c["defaulted"] / c["calls"]) if c["calls"] else 0.0,
                   "input_tokens": c["input_tokens"], "cache_read_tokens": c["cache_read_tokens"], "output_tokens": c["output_tokens"],
                   "cost_usd": cost, "cost_usd_per_duopoly": (cost / self.cfg.duopoles) if cost is not None else None,
                   "tokens_per_duopoly": ((c["input_tokens"] + c["cache_read_tokens"] + c["output_tokens"]) / self.cfg.duopoles),
                   "mean_latency_s": (c["latency_s"] / c["calls"]) if c["calls"] else 0.0}
        summary = {**header, "run_id": self.run_id, "regime": self.cfg.regime, "model": self.cfg.model, "provider": self.cfg.provider,
                   "player": self.cfg.player, "seed": self.cfg.seed, "duopoles": self.cfg.duopoles, "price_offset": self.cfg.price_offset,
                   "pools": len(self.pools), "periods_per_pool": self.periods_played, "truncated_pools": self.truncated,
                   "started": t0, "finished": now_iso(), "counts": self.counts, "n_table": n_table, "metrics": metrics}
        if self.stakes.active:
            caps = [acc["capital"] for acc in self.accounts.values()]
            summary["stakes"] = {"arm": self.stakes.key, "exits": self.exits, "n_exits": len(self.exits),
                                 "final_capital_min": min(caps), "final_capital_mean": sum(caps) / len(caps),
                                 "final_capital_max": max(caps),
                                 "penalty_points_total": sum(acc["penalties"] for acc in self.accounts.values()),
                                 "reward_points_total": sum(acc["rewards"] for acc in self.accounts.values())}
        write_json(self.out / "summary.json", summary)
        return summary


def run_sync(cfg: RunConfig, client: ModelClient | None = None, table: PayoffTable | None = None, generated_by: str = "") -> dict:
    return asyncio.run(Run(cfg, client, table).run(generated_by))
