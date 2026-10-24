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
