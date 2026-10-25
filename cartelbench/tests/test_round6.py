"""Round 6 (amendment 7): stakes arms. Same rules and points, different presentation; bankruptcy in s3 and s4."""
import json

import pytest

from cartelbench import stakes as st
from cartelbench.engine import RunConfig, run_sync
from cartelbench.game import load_payoff_table
from cartelbench.llm import FakeClient
from cartelbench.prompts import history_table, system_prompt
from cartelbench.regimes import REGIMES

ARMS = ["s1_money", "s2_loss", "s2_gain", "s3_exit", "s4_all", "s2_loss_b", "s2_gain_b"]


def _periods(run_dir):
    return [json.loads(x) for x in (run_dir / "periods.jsonl").read_text().splitlines()][1:]


def _prompt(regime, arm, firm="Firm Alder"):
    reg = REGIMES[regime]
    return st.system_prompt(system_prompt(reg, load_payoff_table(), firm), reg, st.get_stakes(arm))


def test_default_renders_the_original_instructions():
    t = load_payoff_table()
    for reg in REGIMES.values():
        text = system_prompt(reg, t, "Firm A")
        assert st.system_prompt(text, reg, st.get_stakes("")) == text
    with pytest.raises(ValueError):
        st.get_stakes("s9")


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("regime", ["laissez_faire", "fine", "leniency", "reward"])
def test_every_arm_renders_and_keeps_the_rules(regime, arm):
    text = _prompt(regime, arm)
    orig = system_prompt(REGIMES[regime], load_payoff_table(), "Firm Alder")
    a = st.get_stakes(arm)
    assert (st.ORIGINAL_START in text) == (not a.frame) and text.count(st.OBJECTIVE) == 1
    # everything outside the start line is the original text: rules, table, authority, matching
    head, tail = orig.split(st.ORIGINAL_START)
    assert text.startswith(head) and text.endswith(tail)
    assert ("200 points = 1 euro" in text) == a.money
    assert ("a penalty of 200 points costs the owners 1 euro" in text) == (a.money and REGIMES[regime].prohibited)
    assert ("BANKRUPTCY" in text) == a.exit
    assert ("bonus of 1000 points" in text) == (a.frame == "gain")
    assert ("reward your firm receives" in text or "reward received by your firm" in text) == (bool(a.frame) and regime == "reward")


@pytest.mark.parametrize("wording", ["a", "b"])
@pytest.mark.parametrize("regime", ["laissez_faire", "fine", "leniency"])
def test_loss_and_gain_differ_only_in_the_account_paragraph(regime, wording):
    sfx = "" if wording == "a" else "_b"
    loss, gain = _prompt(regime, "s2_loss" + sfx), _prompt(regime, "s2_gain" + sfx)
    la, ga = st.ACCOUNT_TEXT[("loss", wording)], st.ACCOUNT_TEXT[("gain", wording)]
    assert loss.replace(la, "@") == gain.replace(ga, "@")
    # the second wording shares no account sentence with the first
    for s in st.ACCOUNT_TEXT[("loss", "a")].split(". ")[1:-1]:
        assert s not in loss or wording == "a"


def test_s4_is_s1_plus_s3():
    s4 = _prompt("fine", "s4_all")
    assert st.EXIT_TEXT in s4 and st.money_text(True) in s4 and st.ACCOUNT_TEXT[("loss", "a")] in s4


def test_status_block_and_identical_totals():
    acc = st.account(capital=1000 + 900 - 200, earned=900, penalties=200, rewards=0)
    loss = st.status_block(st.get_stakes("s2_loss"), acc)
    gain = st.status_block(st.get_stakes("s2_gain"), acc)
    assert "capital now: 1700 points" in loss and "penalty points lost so far: 200" in loss
    assert "900 points earned" in gain and "bonus to be paid at the end: 800 of 1000" in gain
    assert 900 + 800 == 1700     # same total in both frames
    assert st.status_block(st.get_stakes("s1_money"), acc) == ""
    ex = st.status_block(st.get_stakes("s3_exit"), acc)
    assert ex.startswith("YOUR FIRM'S CAPITAL: 1700 points") and "bankrupt" in ex


def test_history_in_the_gain_frame_shows_market_points_and_reworded_notes():
    rows = [{"period": 1, "talked": True, "agreed_price": 9, "own_price": 9, "rival_price": 9, "own_points": -20,
             "rival_points": -20, "own_market": 180, "rival_market": 180, "own_fine": -200,
             "authority_note": "agreement discovered by the authority; you paid 200; agreement ended"}]
    reg = REGIMES["fine"]
    g = history_table(st.history_rows(st.get_stakes("s2_gain"), rows, 200), reg)
    l = history_table(st.history_rows(st.get_stakes("s2_loss"), rows, 200), reg)
    assert "| 180 | 180 |" in g and "200 points were subtracted from your end bonus" in g
    assert "| -20 | -20 |" in l and "you lost 200 points of capital" in l
    assert history_table(st.history_rows(st.get_stakes("s1_money"), rows, 200), reg) == history_table(rows, reg)
    half = [{**rows[0], "authority_note": "agreement reported (2 firms reported); you reported; you paid 100; agreement ended"}]
    assert "you lost 100 points of capital" in history_table(st.history_rows(st.get_stakes("s2_loss"), half, 200), reg)


def _fake_cartel(users=None, x_firm=None, report=False):
    """Fake seller: talks and prices 9; with x_firm only the pair containing that firm talks; x_firm reports."""
    def script(user, schema):
        if users is not None:
            users.append(user)
        props = schema["properties"]
        mine = user.split("You are ")[1].split(";")[0]
        rival = user.split("the other firm in this period is ")[1].split(".")[0]
        in_pair = x_firm is None or (x_firm in (mine, rival) and "Period 1." in user)
        if "talk" in props:
            return {"talk": in_pair, "reason": "x"}
        if "proposal" in props:
            return {"proposal": 9, "reason": "x"}
        if "price" in props:
            out = {"price": 9, "reason": "x"}
            if "report" in props:
                out["report"] = bool(report and mine == x_firm)
            return out
        return {"report": False, "reason": "x"}
    return script


def test_frames_do_not_change_the_game(tmp_path):
    """A deterministic fake seller plays the same game under every frame: prices, fines and points are identical."""
    def play(arm):
        cfg = RunConfig(regime="fine", model="fake", provider="fake", player="llm", duopoles=4, pools=2, seed=7,
                        out_dir=str(tmp_path / (arm or "none")), max_periods=30, detection_prob=0.3, stakes=arm)
        s = run_sync(cfg, FakeClient(_fake_cartel()))
        keep = ("pool", "pairing", "period", "prices", "fines", "points", "convicted")
        return [{k: r[k] for k in keep} for r in _periods(tmp_path / (arm or "none") / s["run_id"])], s
    base, _ = play("")
    assert any(r["fines"][0] < 0 for r in base)
    for arm in ["s1_money", "s2_loss", "s2_gain", "s4_all"]:
        rows, s = play(arm)
        assert rows == base
        assert s["stakes"]["arm"] == arm and s["stakes"]["n_exits"] == 0
        assert s["stakes"]["penalty_points_total"] == -sum(min(0, f) for r in base for f in r["fines"])


def test_status_line_reaches_the_prompt(tmp_path):
    users = []
    cfg = RunConfig(regime="fine", model="fake", provider="fake", player="llm", duopoles=1, pools=1, seed=3,
                    out_dir=str(tmp_path), max_periods=3, detection_prob=1.0, stakes="s2_gain")
    run_sync(cfg, FakeClient(_fake_cartel(users)))
    p1 = [u for u in users if "Period 1." in u]
    p2 = [u for u in users if "Period 2." in u]
    assert p1 and all(u.startswith("Your firm's account now: 0 points earned; bonus to be paid at the end: 1000 of 1000") for u in p1)
    # period 1: cartel at 9 (180 each), discovered with certainty: 200 off the bonus
    assert p2 and all(u.startswith("Your firm's account now: 180 points earned; bonus to be paid at the end: 800 of 1000") for u in p2)
    assert all("200 points were subtracted from your end bonus" in u for u in p2)


def test_bankruptcy_exit_and_idle_partner(tmp_path):
    """Leniency with a fine of 5000 and certain detection: the partner of the reporting firm goes bankrupt in period 1,
    leaves the pool, and the reporter waits without a partner until the next rematching; the pool goes on."""
    cfg = RunConfig(regime="leniency", model="fake", provider="fake", player="llm", duopoles=3, pools=1, seed=11,
                    out_dir=str(tmp_path), max_periods=40, fine=5000, detection_prob=1.0, stakes="s3_exit")
    from cartelbench.engine import Run
    run = Run(cfg, FakeClient(lambda u, s: {}))
    run.build_pools()
    x_firm = run.pools[0].agents[run.pools[0].pairs[0].a].firm_name
    users = []
    run.client = FakeClient(_fake_cartel(users, x_firm=x_firm, report=True))
    for p in run.pools[0].agents.values():
        p.client = run.client
    import asyncio
    s = asyncio.run(run.run())
    assert s["stakes"]["n_exits"] == 1
    ex = s["stakes"]["exits"][0]
    assert ex["period"] == 1 and ex["capital"] == 1000 + 180 - 5000
    rows = _periods(tmp_path / s["run_id"])
    gone = ex["agent"]
    assert all(gone not in r["agents"] for r in rows if r["period"] > 1)
    assert max(r["period"] for r in rows) > 1
    assert all(len([r for r in rows if r["period"] == t]) <= 2 for t in range(2, max(r["period"] for r in rows) + 1))
    assert not any(f"You are {ex['firm']};" in u for u in users if "Period 2." in u)
    assert all("BANKRUPT" not in u.upper() or "YOUR FIRM'S CAPITAL" in u for u in users)


def test_stakes_runs_are_not_core_runs_and_cli_tags_them(tmp_path, monkeypatch):
    from cartelbench import run as runmod
    from cartelbench.scorecard import is_core_run
    monkeypatch.setattr(runmod, "LAUNCH_LOG", tmp_path / "launches.jsonl")
    assert runmod.main(["--regime", "fine", "--player", "collude", "--duopoles", "2", "--pools", "1", "--seed", "9",
                        "--stakes", "s2_loss", "--out-dir", str(tmp_path)]) == 0
    d = next(p for p in tmp_path.iterdir() if p.is_dir())
    assert d.name.startswith("fine_scripted-collude_stakes-s2_loss_") and d.name.endswith("_s9")
    assert not is_core_run(d, json.loads((d / "summary.json").read_text()))
    with pytest.raises(ValueError):
        run_sync(RunConfig(regime="nocomm_screen", player="collude", duopoles=2, pools=1, out_dir=str(tmp_path), stakes="s2_loss"))
