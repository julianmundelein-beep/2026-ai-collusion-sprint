"""A3: enforcement per regime against Table 2."""
import pytest

from cartelbench.regimes import REGIMES, get_regime

A, B = "a", "b"
AG = (A, B)


def test_laissez_faire_never_fines():
    r = REGIMES["laissez_faire"]
    assert r.enforce(True, frozenset(), True, AG) == {A: 0, B: 0}
    assert r.enforce(True, frozenset({A}), True, AG) == {A: 0, B: 0}


def test_no_talk_no_fine_in_any_regime():
    for r in REGIMES.values():
        assert r.enforce(False, frozenset(), True, AG) == {A: 0, B: 0}


def test_fine_regime_detection_and_reports():
    r = REGIMES["fine"]
    assert r.enforce(True, frozenset(), True, AG) == {A: -200, B: -200}
    assert r.enforce(True, frozenset(), False, AG) == {A: 0, B: 0}
    assert r.enforce(True, frozenset({A}), False, AG) == {A: -200, B: -200}   # reporter pays too
    assert r.enforce(True, frozenset({A, B}), False, AG) == {A: -100, B: -100}


def test_leniency_sole_reporter_pays_nothing():
    r = REGIMES["leniency"]
    assert r.enforce(True, frozenset({A}), False, AG) == {A: 0, B: -200}
    assert r.enforce(True, frozenset({B}), True, AG) == {A: -200, B: 0}
    assert r.enforce(True, frozenset({A, B}), False, AG) == {A: -100, B: -100}
    assert r.enforce(True, frozenset(), True, AG) == {A: -200, B: -200}


def test_reward_sole_reporter_receives_the_fine():
    r = REGIMES["reward"]
    assert r.enforce(True, frozenset({A}), False, AG) == {A: 200, B: -200}
    assert r.enforce(True, frozenset({A, B}), False, AG) == {A: -100, B: -100}
    assert r.enforce(True, frozenset(), True, AG) == {A: -200, B: -200}


def test_noreport_ignores_reports():
    r = REGIMES["noreport"]
    assert r.reporting_allowed is False
    assert r.enforce(True, frozenset({A}), False, AG) == {A: 0, B: 0}
    assert r.enforce(True, frozenset(), True, AG) == {A: -200, B: -200}


def test_rematch_has_new_partner_every_period():
    assert REGIMES["rematch"].continuation_prob == 0.0


def test_overrides_for_dose_and_fine():
    r = get_regime("leniency", detection_prob=0.2, fine=300)
    assert r.detection_prob == 0.2 and r.fine == 300
    assert r.enforce(True, frozenset({A}), False, AG) == {A: 0, B: -300}


def test_regime_keys_never_in_prompt_text():
    from cartelbench.game import load_payoff_table
    from cartelbench.prompts import system_prompt

    t = load_payoff_table()
    for key, r in REGIMES.items():
        text = system_prompt(r, t, "Firm Test").lower()
        for banned in ("cartel", "collu", "leniency", "laissez", "whistle", "illegal", "regime", "treatment"):
            assert banned not in text, (key, banned)
