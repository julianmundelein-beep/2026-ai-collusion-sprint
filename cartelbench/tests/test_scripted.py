"""A5, A6: scripted players reproduce the expected rates; the naive baseline of the harness."""
import asyncio

import pytest

from cartelbench.engine import Run, RunConfig


def run(regime, player, seed=1, duopoles=4, **kw):
    cfg = RunConfig(regime=regime, player=player, duopoles=duopoles, pool_size=2 * duopoles, seed=seed, **kw)
    return asyncio.run(Run(cfg).run())


@pytest.mark.parametrize("regime", ["laissez_faire", "fine", "leniency", "reward"])
def test_always_collude(tmp_path, regime):
    s = run(regime, "collude", out_dir=str(tmp_path))
    m = s["metrics"]
    assert m["cartel_rate"] == 1.0
    assert m["avg_price"] == 9.0 and m["cartel_price"] == 9.0
    assert m["deviation_rate"] == 0.0
    assert m["n_reports"] == 0
    if regime == "laissez_faire":
        assert m["fines_paid_total"] == 0 and m["n_detections"] == 0
    else:
        # detection with p = 0.10 per cartel period: expect some fines over about 4 pairs x 27 periods
        assert m["n_detections"] > 0
        assert m["fines_paid_total"] == 400 * m["n_detections"]
        assert m["mean_points_per_agent_period"] < 180


def test_always_deviate_and_report_leniency(tmp_path):
    s = run("leniency", "deviate", out_dir=str(tmp_path))
    m = s["metrics"]
    assert m["cartel_rate"] == 1.0
    assert m["deviation_rate"] == 1.0
    assert m["report_rate_pair_given_cartel"] == 1.0
    assert m["report_rate_agent_given_cartel"] == 1.0
    assert m["secret_report_share"] == 1.0
    assert m["n_detections"] == 0                 # reports pre-empt detection
    # both report every period: each pays 100 per period under leniency
    assert m["fines_paid_total"] == 200 * m["n_pair_periods"]
    from cartelbench.game import load_payoff_table
    assert m["cartel_price"] == load_payoff_table().best_reply(9)   # the undercut price


def test_always_deviate_and_report_fine_regime(tmp_path):
    s = run("fine", "deviate", out_dir=str(tmp_path))
    m = s["metrics"]
    assert m["fines_paid_total"] == 200 * m["n_pair_periods"]   # both report: 100 each


def test_deviate_versus_collude_mixed_pool_reward(tmp_path):
    """One deviator per pair in the reward regime: sole reporter receives 200 every period."""
    from cartelbench.engine import Run as R
    cfg = RunConfig(regime="reward", player="collude", duopoles=1, pool_size=2, seed=9, out_dir=str(tmp_path))
    r = R(cfg)
    r.build_pools()
    pool = r.pools[0]
    a_id = pool.order[0]
    pool.agents[a_id].strategy = "deviate"
    s = asyncio.run(r.run())
    m = s["metrics"]
    assert m["rewards_paid_total"] == 200 * m["n_pair_periods"]
    assert m["fines_paid_total"] == 200 * m["n_pair_periods"]
    assert m["report_rate_agent_given_cartel"] == 0.5
    assert m["deviation_rate"] == 0.5
    assert m["public_report_after_rival_deviation"] == 0.0   # the colluder never reports


def test_nash_players(tmp_path):
    s = run("fine", "nash", out_dir=str(tmp_path))
    m = s["metrics"]
    assert m["cartel_rate"] == 0.0 and m["talk_rate"] == 0.0
    assert m["avg_price"] == 3.0 and m["mean_points_per_agent_period"] == 100
    assert m["cartel_price"] is None


def test_payoff_scale_changes_points_not_behaviour(tmp_path):
    s1 = run("laissez_faire", "tit", seed=3, out_dir=str(tmp_path), payoff_scale=1.0)
    s2 = run("laissez_faire", "tit", seed=3, out_dir=str(tmp_path), payoff_scale=2.0)
    assert s1["metrics"]["avg_price"] == s2["metrics"]["avg_price"]
    assert s2["metrics"]["mean_points_per_agent_period"] == 2 * s1["metrics"]["mean_points_per_agent_period"]
