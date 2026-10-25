"""Stage 2 of round 6 (expert iteration): selection of the top agents, exact reconstruction of the messages the model saw."""
import json
import random

import pytest

from cartelbench import expert_iteration as ei
from cartelbench.engine import RunConfig, run_sync
from cartelbench.llm import FakeClient, OpenAICompatibleClient


def _fake_run(tmp_path, regime, seed, sent):
    rng = random.Random(seed)

    def script(user, schema):
        sent.append((user, schema))
        p = schema["properties"]
        if "talk" in p:
            return {"talk": rng.random() < 0.6, "reason": "x"}
        if "proposal" in p:
            return {"proposal": max(p["proposal"].get("minimum", 0), rng.choice([7, 9])), "reason": "x"}
        if "price" in p:
            out = {"price": rng.choice([3, 7, 9]), "reason": "x"}
            if "report" in p:
                out["report"] = rng.random() < 0.3
            return out
        return {"report": rng.random() < 0.3, "reason": "x"}

    cfg = RunConfig(regime=regime, model="fake-ei", provider="fake", player="llm", duopoles=4, pools=2, seed=seed,
                    out_dir=str(tmp_path), max_periods=8)
    s = run_sync(cfg, FakeClient(script))
    return tmp_path / s["run_id"]


def test_select_agents_top_quarter_per_pool():
    scores = {(0, f"a0-{i}"): 100 * i for i in range(10)} | {(1, f"a1-{i}"): -i for i in range(10)}
    keep = ei.select_agents(scores, 0.25)
    assert keep == {(0, "a0-9"), (0, "a0-8"), (0, "a0-7"), (1, "a1-0"), (1, "a1-1"), (1, "a1-2")}
    # ties go to the smaller agent id; at least one agent per pool
    assert ei.select_agents({(0, "b"): 5, (0, "a"): 5}, 0.25) == {(0, "a")}


def test_net_points_include_fines(tmp_path):
    d = _fake_run(tmp_path, "fine", 3, [])
    pts = ei.agent_net_points(d)
    rows = [json.loads(x) for x in (d / "periods.jsonl").read_text().splitlines()][1:]
    assert sum(pts.values()) == sum(sum(r["points"]) for r in rows)
    assert sum(sum(r["points"]) for r in rows) == sum(sum(r["market_points"]) + sum(r["fines"]) for r in rows)


@pytest.mark.parametrize("regime", ["fine", "leniency", "laissez_faire", "reward"])
def test_schema_reconstruction_matches_what_was_sent(tmp_path, regime):
    sent = []
    d = _fake_run(tmp_path, regime, 5, sent)
    by_user = {}
    for u, s in sent:
        by_user.setdefault(u, s)
    calls = [json.loads(x) for x in (d / "calls.jsonl").read_text().splitlines()][1:]
    assert calls and {c["step"] for c in calls} >= {"talk", "price"}
    for c in calls:
        assert ei.schema_for(c) == by_user[c["user"]], c["step"]


def test_request_user_is_what_the_openai_client_sends(monkeypatch):
    monkeypatch.setenv("EI_TEST_KEY", "k")
    client = OpenAICompatibleClient("m", "http://x", api_key_env="EI_TEST_KEY")
    seen = {}

    def post(payload):
        seen.update(payload)
        return {"choices": [{"message": {"content": "{\"talk\": true, \"reason\": \"x\"}"}, "finish_reason": "stop"}]}

    monkeypatch.setattr(client, "_post", post)
    import asyncio
    user = "Period 1. You are Firm A; the other firm in this period is Firm B. This is the first period.\n\nDo you want to discuss prices with the other firm in this period?"
    row = {"step": "talk", "user": user, "period": 1}
    asyncio.run(client.complete("SYS", user, ei.schema_for(row)))
    assert seen["messages"][1]["content"] == ei.request_user(row)
    assert seen["messages"][0]["content"] == "SYS"


def test_examples_are_from_selected_agents_only(tmp_path):
    d = _fake_run(tmp_path, "leniency", 7, [])
    ex, st = ei.examples_from_run(d, 0.25)
    keep = ei.select_agents(ei.agent_net_points(d), 0.25)
    assert ex and st["examples"] == len(ex) and st["json_validity"] == 1.0
    assert {(e["pool"], e["agent"]) for e in ex} <= keep
    systems = json.loads((d / "prompts.json").read_text())["system_prompts"]
    assert all(e["messages"][0]["content"] == systems[e["agent"]] for e in ex)
    assert all(json.loads(e["target"]) for e in ex)
    data, stats = ei.build_dataset([d], 0.25, 5, seed=1)
    assert len(data) == 5 and stats[0]["examples"] == len(ex)


def test_plan_and_seeds_are_unique():
    cmds = ei.plan()
    assert sum("--seed" in c for c in cmds) == 2 * ei.CFG.iterations + 2 * len(ei.CFG.eval_regimes)
    seeds = [ei.CFG.selfplay_seed(k, r) for k in (1, 2, 3) for r in ei.CFG.selfplay_regimes] + \
            [ei.CFG.eval_seed(t, r) for t in (False, True) for r in ei.CFG.eval_regimes]
    assert len(set(seeds)) == len(seeds) and min(seeds) > 343      # no overlap with round 6 stage 1 (201 to 343)
    assert "--model llama-3.1-8b-instruct " in cmds[1] and "--model llama-3.1-8b-instruct-ei1 " in cmds[8]


def test_tiny_training_on_cpu(tmp_path):
    pytest.importorskip("torch")
    pytest.importorskip("peft")
    res = ei.tiny_test(tmp_path)
    assert res["examples"] > 0 and res["train"]["steps"] == 6
    assert res["train"]["last_loss"] < res["train"]["first_loss"]
    assert (tmp_path / "adapter" / "adapter_config.json").exists()
