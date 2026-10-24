"""R01 design notes: independent pool sessions, validation arms, shifted price grid."""
import asyncio

from cartelbench.analyze import agent_rows, cluster_bootstrap, cluster_key
from cartelbench.engine import Run, RunConfig
from cartelbench.game import load_payoff_table
from cartelbench.llm import FakeClient, parse_json
from cartelbench.prompts import question, system_prompt
from cartelbench.regimes import REGIMES
from cartelbench.util import read_jsonl


def test_default_is_four_independent_pools_of_ten(tmp_path):
    cfg = RunConfig(regime="laissez_faire", player="nash", duopoles=20, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    assert s["pools"] == 4 and s["n_table"]["agents"] == 40 and s["n_table"]["pool_sessions"] == 4
    rows = agent_rows([r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")])
    assert cluster_key(rows) == "pool"
    ci = cluster_bootstrap(rows, ["avg_price"], n_boot=50)
    assert ci["avg_price"]["cluster"] == "pool" and ci["avg_price"]["n_clusters"] == 4


def test_single_pool_falls_back_to_pairing_clusters(tmp_path):
    cfg = RunConfig(regime="laissez_faire", player="nash", duopoles=3, pools=1, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    rows = agent_rows([r for r in read_jsonl(tmp_path / s["run_id"] / "periods.jsonl") if not r.get("header")])
    assert s["pools"] == 1 and cluster_key(rows) == "pairing"


def test_nocomm_arm_never_talks(tmp_path):
    cfg = RunConfig(regime="nocomm", player="collude", duopoles=2, pools=1, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    assert s["metrics"]["cartel_rate"] == 0.0 and s["metrics"]["talk_rate"] == 0.0


def test_fine_certain_arm_fines_every_discussion(tmp_path):
    cfg = RunConfig(regime="fine_certain", player="collude", duopoles=2, pools=1, out_dir=str(tmp_path))
    s = asyncio.run(Run(cfg).run())
    m = s["metrics"]
    assert m["detection_rate_given_cartel"] == 1.0 and m["fines_paid_total"] == 400 * m["n_pair_periods"]


def test_instructed_cartel_has_instruction_in_prompt_and_no_regime_words():
    t = load_payoff_table()
    text = system_prompt(REGIMES["instructed_cartel"], t, "Firm X")
    assert "YOUR FIRM'S POLICY" in text and "propose the price 9" in text
    assert "cartel" not in text.lower()


def test_price_offset_shifts_labels_only(tmp_path):
    seen = {"max_label": 0}

    def answer(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": True, "reason": "x"}
        if "proposal" in props:
            seen["max_label"] = max(seen["max_label"], props["proposal"]["maximum"])
            return {"proposal": 14, "reason": "x"}          # label 14 = internal price 9 with offset 5
        if "price" in props:
            out = {"price": 14, "reason": "x"}
            if "report" in props:
                out["report"] = False
            return out
        return {"report": False, "reason": "x"}

    client = FakeClient(answer)
    cfg = RunConfig(regime="laissez_faire", model="fake", provider="fake", player="llm", duopoles=1, pools=1, seed=1,
                    price_offset=5, out_dir=str(tmp_path), max_periods=21)
    s = asyncio.run(Run(cfg, client).run())
    assert seen["max_label"] == 17
    assert s["metrics"]["avg_price"] == 9.0 and s["metrics"]["agreed_price"] == 9.0
    prompts = read_jsonl(tmp_path / s["run_id"] / "calls.jsonl")[1:]
    assert "between 5 and 17" in prompts[0]["user"] or "between 5 and 17" in next(p["user"] for p in prompts if p["step"] == "price")
    sys_text = system_prompt(REGIMES["laissez_faire"], load_payoff_table(), "Firm X", 5)
    assert "between 5 and 17" in sys_text and "|  17" in sys_text


def test_cost_in_n_table_for_anthropic_models():
    from cartelbench.pricing import cost_usd
    assert abs(cost_usd("claude-haiku-5-5", 1_000_000, 0) - 0.10) < 1e-9
    assert abs(cost_usd("claude-haiku-5-5", 0, 1_000_000) - 0.50) < 1e-9
    assert abs(cost_usd("claude-haiku-5-5", 0, 0, cache_read=1_000_000) - 0.01) < 1e-9
    assert cost_usd("unknown-model", 10, 10) is None
