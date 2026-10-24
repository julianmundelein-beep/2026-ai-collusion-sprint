"""A1, A2: payoffs against the anchors of Table 1 and the structure of the stage game."""
from cartelbench.game import JOINT_OPTIMUM_PRICE, NASH_PRICE, PRICES, load_payoff_table


def test_anchor_cells():
    t = load_payoff_table()
    assert t.payoff(3, 3) == 100
    assert t.payoff(9, 9) == 180
    assert t.payoff(7, 9) == 296
    assert t.payoff(9, 7) == 20


def test_nash_price_is_unique_symmetric_equilibrium():
    t = load_payoff_table()
    nash = [p for p in PRICES if t.best_reply(p) == p
            and all(t.payoff(q, p) < t.payoff(p, p) for q in PRICES if q != p)]
    assert nash == [NASH_PRICE]


def test_joint_optimum_is_nine():
    t = load_payoff_table()
    assert max(PRICES, key=lambda p: t.payoff(p, p)) == JOINT_OPTIMUM_PRICE


def test_undercutting_nine_pays_more_than_keeping_it():
    t = load_payoff_table()
    assert t.best_reply(9) < 9
    assert t.payoff(t.best_reply(9), 9) > t.payoff(9, 9)


def test_table_scaling_and_provenance_are_recorded():
    t = load_payoff_table()
    assert "provenance" not in t.provenance.lower() or t.provenance
    s = t.scaled(2.0)
    assert s.payoff(3, 3) == 200 and s.payoff(9, 9) == 360
    assert "scaled by 2.0" in s.provenance
