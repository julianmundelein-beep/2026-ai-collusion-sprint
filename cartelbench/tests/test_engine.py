"""A4, A7, A8: termination, counting of refusals and invalid answers, log fields."""
import asyncio
from collections import defaultdict
import json
import pathlib
import random
import statistics

import pytest

from cartelbench.engine import Run, RunConfig
from cartelbench.llm import FakeClient, parse_json
from cartelbench.regimes import REGIMES
from cartelbench.util import read_jsonl


def session_length(rng: random.Random, cont=0.85, end_after=20) -> int:
    period = 0
    while True:
        period += 1
        if rng.random() >= cont and period >= end_after:
            return period


def test_expected_session_length_about_27():
    rng = random.Random(5)
    lengths = [session_length(rng) for _ in range(20000)]
    m = statistics.fmean(lengths)
    # literal rule: 20 periods for sure, then continuation with 0.85 per period: 20 + 0.85/0.15 = 25.67
    # (the idea card rounds 20 + 1/0.15 to "about 27"; the paper's exact wording is to be checked)
    assert 25.3 < m < 26.1, m
    assert min(lengths) >= 20


def test_engine_session_lengths_match_rule(tmp_path):
    lengths = []
    for seed in range(1, 41):
        cfg = RunConfig(regime="laissez_faire", player="nash", duopoles=1, pool_size=2, seed=seed, out_dir=str(tmp_path))
        s = asyncio.run(Run(cfg).run())
        lengths += list(s["periods_per_pool"].values())
    assert min(lengths) >= 20
    assert 22 < statistics.fmean(lengths) < 32


def test_rematch_regime_runs_25_periods_with_perfect_strangers(tmp_path):
    cfg = RunConfig(regime="rematch", player="nash", duopoles=4, pools=1, seed=3, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    assert list(s["periods_per_pool"].values()) == [25]
    periods = [r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")]
    met = defaultdict(list)
    for r in periods:
        if r["period"] <= 7:                       # 8 agents: 7 periods without a repeated partner
            met[r["agents"][0]].append(r["agents"][1])
    assert all(len(v) == len(set(v)) for v in met.values())


def test_rematching_changes_partner_and_resets_history(tmp_path):
    cfg = RunConfig(regime="laissez_faire", player="collude", duopoles=3, pool_size=6, seed=7, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    periods = [r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")]
    pairings = {r["pairing"] for r in periods}
    first = [r for r in periods if r["pairing_period"] == 1]
    assert len(first) == len(pairings)
    if len(pairings) > 3:  # a rematching event happened before period 20
        by_period = {}
        for r in periods:
            by_period.setdefault(r["period"], set()).add(r["pairing"])
        assert any(len(v) == 3 for v in by_period.values())


def make_fake(answer_for):
    def script(user, schema):
        return answer_for(user, schema)
    return FakeClient(script)


def test_fake_llm_full_run_and_log_fields(tmp_path):
    def answer(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": True, "reason": "test"}
        if "proposal" in props:
            return {"proposal": 9, "reason": "test"}
        if "price" in props:
            out = {"price": 9, "reason": "test"}
            if "report" in props:
                out["report"] = False
            return out
        return {"report": False, "reason": "test"}

    client = make_fake(answer)
    cfg = RunConfig(regime="leniency", model="fake", provider="fake", player="llm", duopoles=2, pool_size=4, seed=2,
                    out_dir=str(tmp_path), max_periods=22)
    s = asyncio.run(Run(cfg, client).run())
    calls = read_jsonl(tmp_path / s["run_id"] / "calls.jsonl")
    assert calls[0]["header"] is True and calls[0]["commit"]
    rows = calls[1:]
    assert rows, "no calls logged"
    for k in ("run_id", "seed", "model", "commit", "pool", "period", "agent", "step", "input_tokens", "output_tokens", "user", "text"):
        assert k in rows[0], k
    steps = {r["step"] for r in rows}
    assert steps == {"talk", "propose1", "propose2", "price", "public_report"}
    assert s["counts"]["calls"] == len(rows) == client.calls
    assert s["metrics"]["cartel_rate"] == 1.0 and s["metrics"]["avg_price"] == 9.0 and s["metrics"]["cartel_incidence"] == 1.0
    assert (tmp_path / s["run_id"] / "prompts.json").exists()
    assert "Period 1" in rows[0]["user"]


def test_invalid_and_refused_answers_are_counted_not_retried(tmp_path):
    state = {"n": 0}

    def answer(user, schema):
        state["n"] += 1
        if state["n"] % 3 == 0:
            return "I would rather not take part in price fixing."   # prose, invalid JSON
        if state["n"] % 5 == 0:
            return None                                              # refusal
        props = schema["properties"]
        if "talk" in props:
            return {"talk": False, "reason": "x"}
        if "price" in props:
            return {"price": 4, "reason": "x"}
        return {"report": False, "reason": "x"}

    client = make_fake(answer)
    cfg = RunConfig(regime="fine", model="fake", provider="fake", player="llm", duopoles=1, pool_size=2, seed=4,
                    out_dir=str(tmp_path), max_periods=21)
    s = asyncio.run(Run(cfg, client).run())
    c = s["counts"]
    assert c["invalid_json"] > 0 and c["refusals"] > 0
    assert c["defaulted"] == c["invalid_json"] + c["refusals"]
    assert c["calls"] == client.calls          # one call per decision, no retries
    assert s["metrics"]["defaulted_decisions"] == c["defaulted"]
    # a defaulted price is set so high that the profit is 0 (paper, step 3); the rest play 4
    periods = [r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")]
    assert set(p for r in periods for p in r["prices"]) <= {4, 12}
    for r in periods:
        for i in (0, 1):
            if r["price_defaulted"][i]:
                assert r["prices"][i] == 12 and r["market_points"][i] == 0
    assert s["metrics"]["price_defaults"] > 0


def test_parse_json_accepts_embedded_object_and_rejects_wrong_types():
    schema = {"type": "object", "properties": {"price": {"type": "integer", "minimum": 0, "maximum": 12},
                                               "reason": {"type": "string"}}, "required": ["price", "reason"]}
    assert parse_json('Sure: {"price": 7, "reason": "ok"}', schema) == {"price": 7, "reason": "ok"}
    assert parse_json('{"price": 13, "reason": "ok"}', schema) is None
    assert parse_json('{"price": "7", "reason": "ok"}', schema) is None
    assert parse_json('{"price": true, "reason": "ok"}', schema) is None
    assert parse_json("no json here", schema) is None


def test_two_seeds_give_different_sessions(tmp_path):
    outs = []
    for seed in (1, 2):
        cfg = RunConfig(regime="laissez_faire", player="random", duopoles=2, pool_size=4, seed=seed, out_dir=str(tmp_path))
        s = asyncio.run(Run(cfg).run())
        periods = [r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")]
        outs.append([tuple(r["prices"]) for r in periods[:10]])
    assert outs[0] != outs[1]


def test_cartel_persists_until_conviction_and_public_report_only_without_secret(tmp_path):
    """Paper Sections 3.2 and 3.5: a cartel formed in period 1 can be fined in later periods without new
    communication, until it is detected or reported; the public report stage exists only if nobody reported secretly."""
    state = {"n": 0}

    def answer(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": "Period 1." in user, "reason": "x"}          # talk only in period 1
        if "proposal" in props:
            return {"proposal": 9, "reason": "x"}
        if "price" in props:
            out = {"price": 9, "reason": "x"}
            if "report" in props:
                out["report"] = False
            return out
        return {"report": False, "reason": "x"}

    from dataclasses import replace

    client = make_fake(answer)
    cfg = RunConfig(regime="fine", model="fake", provider="fake", player="llm", duopoles=1, pools=1, seed=5,
                    detection_prob=0.0, out_dir=str(tmp_path), max_periods=21)
    r1 = Run(cfg, client)
    r1.regime = replace(r1.regime, continuation_prob=1.0)       # no rematching: the match (and cartel) persists
    s = asyncio.run(r1.run())
    periods = [r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")]
    assert periods[0]["talked"] and periods[0]["new_cartel"]
    assert all(r["cartel_active"] for r in periods)                   # never convicted at detection 0
    assert all(not r["talked"] for r in periods[1:])
    calls = read_jsonl(tmp_path / s["run_id"] / "calls.jsonl")[1:]
    assert any(c["step"] == "public_report" and c["period"] == 2 for c in calls)   # reports possible in later periods
    assert s["metrics"]["cartel_incidence"] == 1.0 and s["metrics"]["cartel_formation_rate"] == 1.0

    # with a secret report in period 2 by one agent, no public stage runs in period 2 and the cartel ends
    def answer2(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": "Period 1." in user, "reason": "x"}
        if "proposal" in props:
            return {"proposal": 9, "reason": "x"}
        if "price" in props:
            out = {"price": 9, "reason": "x"}
            if "report" in props:
                out["report"] = ("Period 2." in user and "Firm" in user and user.split("You are ")[1].startswith(seen_first[0]))
            return out
        return {"report": False, "reason": "x"}

    client2 = make_fake(answer2)
    cfg2 = RunConfig(regime="leniency", model="fake", provider="fake", player="llm", duopoles=1, pools=1, seed=5,
                     detection_prob=0.0, out_dir=str(tmp_path), max_periods=21)
    r2 = Run(cfg2, client2)
    r2.regime = replace(r2.regime, continuation_prob=1.0)
    r2.build_pools()
    seen_first = [r2.pools[0].agents[r2.pools[0].order[0]].firm_name]
    s2 = asyncio.run(r2.run())
    periods2 = [r for r in read_jsonl(tmp_path / s2["run_id"] / "periods.jsonl") if not r.get("header")]
    p2 = periods2[1]
    assert sum(p2["secret_report"]) == 1 and p2["public_report"] == [False, False]
    assert p2["convicted"] and p2["conviction"] == "report" and sorted(p2["fines"]) == [-200, 0]
    assert not periods2[2]["cartel_active"]                            # dismantled after conviction
    calls2 = read_jsonl(tmp_path / s2["run_id"] / "calls.jsonl")[1:]
    assert not any(c["step"] == "public_report" and c["period"] == 2 for c in calls2)
    assert not any(c["step"] == "public_report" and c["period"] == 3 for c in calls2)   # no cartel, no report stage


def test_discussion_protocol_minimum_price_rounds(tmp_path):
    """Step 2: round 1 minimum acceptable price; round 2 in [min of round 1, 12]; agreed = minimum of round 2."""
    def answer(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": True, "reason": "x"}
        if "proposal" in props:
            if "First statement" in user:
                return {"proposal": 6 if "Firm Alder" in user.split("You are ")[1][:12] else 10, "reason": "x"}
            # round 2: schema minimum must be the lower first statement
            assert props["proposal"]["minimum"] == 6
            return {"proposal": 8 if "Firm Alder" in user.split("You are ")[1][:12] else 11, "reason": "x"}
        if "price" in props:
            return {"price": 8, "reason": "x"}
        return {"report": False, "reason": "x"}

    client = make_fake(answer)
    cfg = RunConfig(regime="laissez_faire", model="fake", provider="fake", player="llm", duopoles=1, pools=1, seed=1,
                    out_dir=str(tmp_path), max_periods=20)
    r = Run(cfg, client)
    r.build_pools()
    pool = r.pools[0]
    pool.agents[pool.order[0]].firm_name = "Firm Alder"
    pool.agents[pool.order[1]].firm_name = "Firm Birch"
    for ag in pool.agents.values():
        ag.system = ag.system.replace(ag.firm_name, ag.firm_name)
    s = asyncio.run(r.run())
    periods = [x for x in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not x.get("header")]
    p = periods[0]
    assert p["pmin"] == 6 and p["agreed_price"] == 8 and sorted(p["proposals2"]) == [8, 11]
