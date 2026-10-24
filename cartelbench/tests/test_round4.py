"""Round 4 (amendment 4): launch log of the run ledger."""
import json

from cartelbench import run as run_mod


def test_launch_log_lists_start_and_end(tmp_path, monkeypatch):
    log = tmp_path / "launches.jsonl"
    monkeypatch.setattr(run_mod, "LAUNCH_LOG", log)
    rc = run_mod.main(["--regime", "fine", "--player", "nash", "--duopoles", "2", "--pools", "1", "--seed", "3",
                       "--out-dir", str(tmp_path / "runs")])
    assert rc == 0
    rows = [json.loads(x) for x in log.read_text().splitlines()]
    assert [r["event"] for r in rows] == ["start", "end"]
    assert rows[0]["run_id"] == rows[1]["run_id"] and rows[1]["status"] == "complete"
    assert (tmp_path / "runs" / rows[0]["run_id"] / "summary.json").exists()


def _scripted(tmp_path, regime, player, seed, duopoles=6, pools=3):
    from cartelbench.engine import RunConfig, run_sync
    cfg = RunConfig(regime=regime, model=f"scripted-{player}", provider="scripted", player=player, duopoles=duopoles,
                    pools=pools, seed=seed, out_dir=str(tmp_path))
    s = run_sync(cfg)
    return tmp_path / s["run_id"]


KEYS = ["cartel_formation_rate", "cartel_incidence", "avg_price", "late_avg_price", "cartel_price", "late_share_above_nash",
        "report_rate_given_cartel", "deviation_rate", "public_report_rate_given_only_rival_deviated", "relapse_rate_next_period"]


def test_ratio_parts_match_metrics_and_merge_keeps_pools(tmp_path):
    from cartelbench.analyze import metrics_from_rows
    from cartelbench.pools import _ratio, cluster_parts, merge_runs
    a = _scripted(tmp_path, "fine", "random", 1)
    b = _scripted(tmp_path, "fine", "random", 2)
    m = merge_runs([a, b])
    assert m["summary"]["pools"] == 6 and len({x["pool"] for x in m["rows"]}) == 6
    assert m["summary"]["duopoles"] == 12
    full = metrics_from_rows(m["rows"])
    for k in KEYS:
        got = _ratio(cluster_parts(m["rows"], k))
        assert (got is None and full[k] is None) or abs(got - full[k]) < 1e-9, k


def test_permutation_exact_and_sampled():
    from cartelbench.pools import permutation_test
    a = [(9.0, 1)] * 4
    b = [(1.0, 1)] * 4
    r = permutation_test(a, b, "greater")
    assert r["exact"] and r["relabellings"] == 70 and abs(r["p"] - 1 / 70) < 1e-12
    r2 = permutation_test(a, b, "two-sided")
    assert abs(r2["p"] - 2 / 70) < 1e-12
    big = permutation_test([(9.0, 1)] * 8, [(1.0, 1)] * 8, "greater", n_max=10_000, seed=0)
    assert not big["exact"] and big["relabellings"] == 10_000 and big["p"] < 0.01


def test_scorecard_picks_first_registered_run(tmp_path):
    from cartelbench.scorecard import pick_runs
    a = _scripted(tmp_path, "fine", "nash", 1, duopoles=2, pools=1)
    _scripted(tmp_path, "fine", "nash", 2, duopoles=2, pools=1)
    runs = pick_runs(tmp_path, "scripted-nash")
    assert runs["fine"]["summary"]["run_id"] == a.name


def _prompts_of(run_dir):
    rows = [json.loads(x) for x in (run_dir / "calls.jsonl").read_text().splitlines()][1:]
    return [r["user"] for r in rows]


def _fake_run(tmp_path, regime, variant, seed=3):
    import random as _r

    from cartelbench.engine import RunConfig, run_sync
    from cartelbench.llm import FakeClient
    rng = _r.Random(seed)

    def script(user, schema):
        props = schema["properties"]
        if "talk" in props:
            return {"talk": rng.random() < 0.7, "reason": "x"}
        if "proposal" in props:
            return {"proposal": max(props["proposal"]["minimum"], 9), "reason": "x"}
        if "price" in props:
            out = {"price": rng.choice([3, 7, 9]), "reason": "x"}
            if "report" in props:
                out["report"] = rng.random() < 0.3
            return out
        return {"report": rng.random() < 0.3, "reason": "x"}

    cfg = RunConfig(regime=regime, model="fake", provider="fake", player="llm", duopoles=4, pools=2, seed=seed,
                    out_dir=str(tmp_path / variant), prompt_variant=variant)
    s = run_sync(cfg, FakeClient(script))
    return tmp_path / variant / s["run_id"]


def test_paraphrase_keeps_numbers_and_schemas_and_rewords_every_note(tmp_path):
    import re

    from cartelbench import prompts, prompts_paraphrase as pp
    from cartelbench.game import load_payoff_table
    from cartelbench.regimes import REGIMES
    t = load_payoff_table()
    for reg in ["laissez_faire", "fine", "leniency", "reward"]:
        for off in (0, 5):
            a = prompts.system_prompt(REGIMES[reg], t, "Firm Alder", off)
            b = pp.system_prompt(REGIMES[reg], t, "Firm Alder", off)
            assert sorted(re.findall(r"\d+", a)) == sorted(re.findall(r"\d+", b)), (reg, off)
            assert a != b
    ctx = {"period": 4, "firm_name": "Firm A", "rival_name": "Firm B", "partner_note": "This is the first period.",
           "status_note": "", "history": "", "pmin": 4, "own_proposal": 9, "rival_proposal": 4, "discussion_note": "Both firms declined a discussion.",
           "can_report": True, "own_price": 3, "rival_price": 9, "own_market": 100, "rival_market": 20}
    for step in ["talk", "propose1", "propose2", "price", "public_report"]:
        assert prompts.question(step, ctx)[1] == pp.question(step, ctx)[1], step
    for reg in ["fine", "leniency", "reward", "laissez_faire"]:
        run = _fake_run(tmp_path, reg, "paraphrase")
        users = _prompts_of(run)
        assert users
        for u in users:
            for w in ("discussion", "agreement", "authority", "agreed"):
                assert w not in u, (reg, w, u[:300])
        system = json.loads((run / "prompts.json").read_text())["system_prompts"]
        assert all("COMPETITION OFFICE" in v for v in system.values()) == (reg != "laissez_faire")


def test_original_variant_unchanged_against_recorded_runs():
    import pathlib

    from cartelbench import prompts
    from cartelbench.game import load_payoff_table
    from cartelbench.regimes import REGIMES
    runs = pathlib.Path(__file__).resolve().parents[1] / "evidence" / "runs"
    t = load_payoff_table()
    checked = 0
    for reg, seed in [("laissez_faire", 1), ("fine", 2), ("leniency", 3), ("reward", 4)]:
        for d in runs.glob(f"{reg}_claude-haiku-5-5_*_s{seed}"):
            rec = json.loads((d / "prompts.json").read_text())["system_prompts"]
            cfg = json.loads((d / "config.json").read_text())
            names = {a["id"]: a["firm"] for p in cfg["pools"] for a in p["agents"]}
            for agent, text in rec.items():
                assert prompts.system_prompt(REGIMES[reg], t, names[agent], 0) == text
                checked += 1
    assert checked == 160
