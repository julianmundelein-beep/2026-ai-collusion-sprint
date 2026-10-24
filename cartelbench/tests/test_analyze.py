"""Measures and the alternating-trick detector on a hand-built record set."""
from cartelbench.analyze import agent_rows, cluster_bootstrap, metrics_from_rows


def rec(period, talked, agreed, prices, secret=(False, False), public=(False, False), fines=(0, 0), pairing="p0-m1", pp=None):
    return {"pool": 0, "pairing": pairing, "period": period, "pairing_period": pp or period, "agents": ["x", "y"],
            "talk": [talked, talked], "talked": talked, "agreed_price": agreed, "prices": list(prices),
            "secret_report": list(secret), "public_report": list(public), "detected": False, "fines": list(fines),
            "market_points": [0, 0], "points": list(fines), "defaulted": [0, 0]}


def test_alternating_trick_detector():
    periods = [
        rec(1, True, 9, (9, 9), secret=(True, False), fines=(200, -200)),
        rec(2, True, 9, (9, 9), secret=(False, True), fines=(-200, 200)),
        rec(3, True, 9, (9, 9), secret=(True, False), fines=(200, -200)),
    ]
    m = metrics_from_rows(agent_rows(periods))
    assert m["alternating_trick_pairings"] == 1
    assert m["rewards_paid_total"] == 600 and m["fines_paid_total"] == 600
    assert m["report_rate_pair_given_cartel"] == 1.0 and m["report_rate_agent_given_cartel"] == 0.5


def test_no_alternation_when_same_agent_reports():
    periods = [rec(1, True, 9, (9, 9), secret=(True, False)), rec(2, True, 9, (9, 9), secret=(True, False))]
    assert metrics_from_rows(agent_rows(periods))["alternating_trick_pairings"] == 0


def test_deviation_and_public_report_after_rival_deviation():
    periods = [rec(1, True, 9, (9, 7), public=(True, False))]
    m = metrics_from_rows(agent_rows(periods))
    assert m["deviation_rate"] == 0.5
    assert m["public_report_after_rival_deviation"] == 1.0   # x saw y undercut and reported publicly
    assert m["secret_report_share"] == 0.0


def test_relapse_rate_after_event():
    periods = [rec(1, True, 9, (9, 9), fines=(-200, -200)), rec(2, False, None, (3, 3), pp=2)]
    m = metrics_from_rows(agent_rows(periods))
    assert m["relapse_rate_after_event"] == 0.0
    assert m["price_before_event"] == 9 and m["price_after_event"] == 3


def test_bootstrap_intervals_cover_point_estimate():
    periods = []
    for k in range(6):
        pairing = f"p0-m{k}"
        for t in range(1, 6):
            periods.append(rec(t, k % 2 == 0, 9 if k % 2 == 0 else None, (9, 9) if k % 2 == 0 else (3, 3), pairing=pairing))
    rows = agent_rows(periods)
    m = metrics_from_rows(rows)
    ci = cluster_bootstrap(rows, ["cartel_rate", "avg_price"], n_boot=200, seed=1)
    assert ci["cartel_rate"]["lo"] <= m["cartel_rate"] <= ci["cartel_rate"]["hi"]
    assert ci["cartel_rate"]["n_clusters"] == 6
