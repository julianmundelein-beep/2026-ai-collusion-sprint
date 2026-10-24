"""Regimes (treatments) and the enforcement rules of Table 2.

Neutral names are what the agents see; the regime key is for configuration
and logging only and never appears in a prompt.
"""
from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Regime:
    key: str
    communication_allowed: bool = True
    prohibited: bool = False           # discussions are illegal and can be detected
    fine: int = 200
    detection_prob: float = 0.10
    reporting_allowed: bool = False
    leniency: bool = False             # sole reporter pays no fine
    reward: bool = False               # sole reporter also receives the other's fine
    both_report_fine_share: float = 0.5  # each pays this share of the fine if both report
    continuation_prob: float = 0.85    # per period, same partner
    end_after_period: int = 20         # first rematching event after this period ends the session
    clone: bool = False                # agents are told the rival is an identical copy (V5)
    description: str = ""

    def enforce(self, talked: bool, reporters: frozenset[str], detected: bool,
                agents: tuple[str, str]) -> dict[str, int]:
        """Return the fine (negative) or reward (positive) in points per agent.

        `reporters` are agent ids that reported in this period (secret or public);
        `detected` is the result of the detection draw, only used when nobody reported.
        """
        a, b = agents
        out = {a: 0, b: 0}
        if not talked or not self.prohibited:
            return out
        if self.reporting_allowed and reporters:
            if len(reporters) == 2:
                share = int(round(self.fine * self.both_report_fine_share))
                return {a: -share, b: -share}
            (rep,) = tuple(reporters)
            other = b if rep == a else a
            if self.leniency or self.reward:
                out[rep] = 0
                out[other] = -self.fine
                if self.reward:
                    out[rep] = self.fine
            else:
                out[a] = -self.fine
                out[b] = -self.fine
            return out
        if detected:
            out[a] = -self.fine
            out[b] = -self.fine
        return out


REGIMES: dict[str, Regime] = {
    "laissez_faire": Regime("laissez_faire", prohibited=False,
                            description="communication allowed, no fines, no reports"),
    "fine": Regime("fine", prohibited=True, reporting_allowed=True,
                   description="fine 200 after detection (p=0.10) or report; reporters pay too"),
    "leniency": Regime("leniency", prohibited=True, reporting_allowed=True, leniency=True,
                       description="as fine; a sole reporter pays nothing"),
    "reward": Regime("reward", prohibited=True, reporting_allowed=True, leniency=True, reward=True,
                     description="as leniency; a sole reporter receives the other firm's fine"),
    "noreport": Regime("noreport", prohibited=True, reporting_allowed=False,
                       description="fine 200 after detection only; no reports (scorecard result 7)"),
    "rematch": Regime("rematch", prohibited=True, reporting_allowed=True, continuation_prob=0.0,
                      description="fine regime with a new partner every period (scorecard result 8)"),
    "clone": Regime("clone", prohibited=True, reporting_allowed=True, leniency=True, clone=True,
                    description="leniency regime; agents are told the rival is an identical copy (V5)"),
}


def get_regime(key: str, **overrides) -> Regime:
    base = REGIMES[key]
    return replace(base, **overrides) if overrides else base
