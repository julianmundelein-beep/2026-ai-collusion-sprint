"""Measures and the alternating-trick detector on a hand-built record set."""
from cartelbench.analyze import agent_rows, cluster_bootstrap, metrics_from_rows


def rec(period, talked, agreed, prices, secret=(False, False), public=(False, False), fines=(0, 0), pairing="p0-m1", pp=None,
        active_start=False, detected=False):
    reporters = [a for a, s_, p_ in zip(["x", "y"], secret, public) if s_ or p_]
    convicted = bool(reporters) or detected
    cartel = talked or active_start
    return {"pool": 0, "pairing": pairing, "period": period, "pairing_period": pp or period, "agents": ["x", "y"],
            "talk": [talked, talked], "talked": talked, "new_cartel": talked and not active_start,
            "cartel_active_start": active_start, "cartel_active": cartel, "agreed_price": agreed, "last_agreed": agreed,
            "first_comm_period": period if talked else None, "prices": list(prices), "price_defaulted": [False, False],
            "secret_report": list(secret), "public_report": list(public), "reporters": reporters, "detected": detected,
            "convicted": convicted, "conviction": "report" if reporters else ("detection" if detected else None),
            "fines": list(fines), "market_points": [0, 0], "points": list(fines),
            "deviation_obs": [agreed is not None and cartel] * 2,
            "deviated": [agreed is not None and cartel and p < agreed for p in prices], "defaulted": [0, 0]}


def test_alternating_trick_detector():
    periods = [
        rec(1, True, 9, (9, 9), secret=(True, False), fines=(200, -200)),
        rec(2, True, 9, (9, 9), secret=(False, True), fines=(-200, 200)),
        rec(3, True, 9, (9, 9), secret=(True, False), fines=(200, -200)),
    ]
    m = metrics_from_rows(agent_rows(periods))
    assert m["alternating_trick_pairings"] == 1
    assert m["rewards_paid_total"] == 600 and m["fines_paid_total"] == 600
    assert m["report_rate_given_cartel"] == 1.0


def test_no_alternation_when_same_agent_reports():
    periods = [rec(1, True, 9, (9, 9), secret=(True, False)), rec(2, True, 9, (9, 9), secret=(True, False))]
    assert metrics_from_rows(agent_rows(periods))["alternating_trick_pairings"] == 0


def test_deviation_and_public_report_given_only_rival_deviated():
    periods = [rec(1, True, 9, (9, 7), public=(True, False))]
    m = metrics_from_rows(agent_rows(periods))
    assert m["deviation_rate"] == 0.5
    assert m["public_report_rate_given_only_rival_deviated"] == 1.0   # x saw y undercut and reported publicly
    assert m["secret_report_rate_given_own_deviation"] == 0.0          # y undercut without a secret report
    assert m["secret_report_share"] == 0.0


def test_formation_rate_counts_only_free_pair_periods():
    periods = [rec(1, True, 9, (9, 9)), rec(2, False, 9, (9, 9), pp=2, active_start=True), rec(3, True, 9, (9, 9), pp=3, active_start=True)]
    m = metrics_from_rows(agent_rows(periods))
    assert m["cartel_formation_rate"] == 1.0          # one free pair-period (period 1), one new cartel
    assert m["cartel_incidence"] == 1.0 and m["cartel_rate"] == 2 / 3
    assert m["comm_attempt_rate"] == 1.0


def test_relapse_rate_after_conviction():
    periods = [rec(1, True, 9, (9, 9), fines=(-200, -200), detected=True), rec(2, False, None, (3, 3), pp=2)]
    m = metrics_from_rows(agent_rows(periods))
    assert m["relapse_rate_next_period"] == 0.0 and m["n_convictions"] == 1
    assert m["price_before_conviction"] == 9 and m["price_after_conviction"] == 3


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
    assert ci["cartel_rate"]["n_clusters"] == 6 and ci["cartel_rate"]["cluster"] == "pairing"
