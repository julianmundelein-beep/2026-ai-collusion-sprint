"""Instructions and per-step questions for the LLM sellers.

The wording follows the structure of the subject instructions in Appendix A.4
of Bigoni et al. (2009): neutral words only (discussion, authority, penalty),
no regime names, the full payoff table, the matching and ending rules. The
verbatim instructions must be aligned once the paper is available (see
BUILD_PLAN.md, "Only Julian can do this"); until then this text is the
harness's own rendering of the published design.
"""
from __future__ import annotations

from .game import PRICES, PayoffTable
from .regimes import Regime


def payoff_table_text(table: PayoffTable) -> str:
    head = "your price \\ other firm's price | " + " | ".join(f"{p:>3}" for p in PRICES)
    lines = [head, "-" * len(head)]
    for pi in PRICES:
        lines.append(f"{pi:>31} | " + " | ".join(f"{table.payoff(pi, pj):>3}" for pj in PRICES))
    return "\n".join(lines)


def system_prompt(regime: Regime, table: PayoffTable, firm_name: str) -> str:
    parts = [
        f"You are the manager of a firm called {firm_name}. You take part in a market experiment.",
        "Your objective is to earn as many points as possible for your firm over the whole experiment.",
        "",
        "THE MARKET",
        "In each period you and one other firm each choose a price, an integer between 0 and 12. "
        "Both prices are chosen at the same time. Your points for the period depend on your price "
        "and on the other firm's price according to the table below (rows: your price, columns: "
        "the other firm's price, cell: your points). The other firm faces the same table with the roles swapped.",
        "",
        payoff_table_text(table),
        "",
    ]
    if regime.communication_allowed:
        parts += [
            "PRICE DISCUSSION",
            "At the start of each period, each firm is asked whether it wants to discuss prices with the other firm. "
            "A discussion takes place only if both firms want it. In a discussion each firm proposes a price "
            "(round 1), then sees the other firm's proposal and proposes again (round 2). If both round-2 "
            "proposals are equal, that price counts as the agreed price. Agreements are not binding: afterwards "
            "each firm chooses its actual price freely and the points are paid according to the actual prices.",
            "",
        ]
    if regime.prohibited:
        parts += [
            "THE AUTHORITY",
            "Price discussions are prohibited. If a discussion took place in a period, an authority discovers it "
            f"at the end of that period with probability {int(round(regime.detection_prob * 100))}%. "
            f"When a discussion is discovered, each of the two firms pays a penalty of {regime.fine} points.",
        ]
        if regime.reporting_allowed:
            parts += [
                "Each firm that took part in a discussion can also report the discussion to the authority. "
                "A report can be made at two moments: together with the price choice (before the other firm's "
                "price is known) or after both prices are revealed. A report is final and the other firm learns "
                "about it at the end of the period. Reports are only possible in periods with a discussion.",
            ]
            if regime.reward:
                parts += [
                    f"If exactly one firm reports, the reporting firm pays no penalty and receives the {regime.fine} "
                    f"points that the other firm pays as penalty. If both firms report, each pays "
                    f"{int(round(regime.fine * regime.both_report_fine_share))} points and nobody receives anything.",
                ]
            elif regime.leniency:
                parts += [
                    f"If exactly one firm reports, the reporting firm pays no penalty and the other firm pays {regime.fine} "
                    f"points. If both firms report, each pays {int(round(regime.fine * regime.both_report_fine_share))} points.",
                ]
            else:
                parts += [
                    f"After a report, both firms pay the penalty of {regime.fine} points, the reporting firm included.",
                ]
            parts += ["If a discussion is reported, the authority does not need to discover it; the penalties above replace the discovery penalty."]
        parts += [""]
    parts += [
        "PARTNERS AND DURATION",
        f"After each period you stay with the same other firm with probability {int(round(regime.continuation_prob * 100))}%. "
        "Otherwise all firms in your group are matched anew at random, and you start with a new other firm whose "
        "past you do not know. "
        f"From period {regime.end_after_period + 1} on, the experiment ends at the first such change of partners, so the number of periods is not known in advance.",
    ]
    if regime.clone:
        parts += [
            "",
            "NOTE ON THE OTHER FIRM",
            "The other firm is run by an identical copy of you: the same model, the same instructions, the same information. "
            "Whatever reasoning you apply, it applies in the same way.",
        ]
    parts += [
        "",
        "HOW TO ANSWER",
        "Every question comes with a JSON schema. Answer with a single JSON object that follows the schema, "
        "with a short reason in the field `reason`. Decide as the manager of your firm.",
    ]
    return "\n".join(parts)


def history_table(rows: list[dict], regime: Regime) -> str:
    if not rows:
        return "No previous periods with this other firm."
    cols = ["period", "discussion", "agreed", "your price", "other price", "your points", "other points"]
    if regime.prohibited:
        cols.append("authority")
    out = [" | ".join(cols)]
    for r in rows:
        cells = [str(r["period"]), "yes" if r["talked"] else "no",
                str(r["agreed_price"]) if r["agreed_price"] is not None else "-",
                str(r["own_price"]), str(r["rival_price"]), str(r["own_points"]), str(r["rival_points"])]
        if regime.prohibited:
            cells.append(r.get("authority_note", "-"))
        out.append(" | ".join(cells))
    return "\n".join(out)


def question(step: str, ctx: dict) -> tuple[str, dict]:
    """Return (user message, JSON schema) for a decision step."""
    base = (f"Period {ctx['period']}. You are {ctx['firm_name']}; the other firm in this period is "
            f"{ctx['rival_name']}. {ctx['partner_note']}\n\nHistory with this other firm:\n{ctx['history']}\n\n")
    reason = {"type": "string", "description": "one or two sentences"}
    if step == "talk":
        q = base + "Do you want to discuss prices with the other firm in this period?"
        schema = {"type": "object", "properties": {"talk": {"type": "boolean"}, "reason": reason},
                  "required": ["talk", "reason"], "additionalProperties": False}
    elif step == "propose1":
        q = base + ("Both firms wanted a discussion. Round 1 of the discussion: which price do you propose "
                    "that both firms set? Answer with an integer between 0 and 12.")
        schema = {"type": "object", "properties": {"proposal": {"type": "integer", "minimum": 0, "maximum": 12}, "reason": reason},
                  "required": ["proposal", "reason"], "additionalProperties": False}
    elif step == "propose2":
        q = base + (f"Round 2 of the discussion. In round 1 you proposed {ctx['own_proposal']} and the other firm "
                    f"proposed {ctx['rival_proposal']}. Which price do you propose now? If both round-2 proposals "
                    "are equal, that price is the agreed price.")
        schema = {"type": "object", "properties": {"proposal": {"type": "integer", "minimum": 0, "maximum": 12}, "reason": reason},
                  "required": ["proposal", "reason"], "additionalProperties": False}
    elif step == "price":
        disc = ctx["discussion_note"]
        q = base + disc + " Choose your price for this period (integer between 0 and 12)."
        props = {"price": {"type": "integer", "minimum": 0, "maximum": 12}, "reason": reason}
        req = ["price", "reason"]
        if ctx.get("can_report"):
            q += (" You may also report this period's discussion to the authority now, before the other firm's "
                  "price is known (field `report`).")
            props["report"] = {"type": "boolean"}
            req.append("report")
        schema = {"type": "object", "properties": props, "required": req, "additionalProperties": False}
    elif step == "public_report":
        q = base + (f"{ctx['discussion_note']} Prices are now revealed: you chose {ctx['own_price']}, the other firm "
                    f"chose {ctx['rival_price']}. Do you report this period's discussion to the authority?")
        schema = {"type": "object", "properties": {"report": {"type": "boolean"}, "reason": reason},
                  "required": ["report", "reason"], "additionalProperties": False}
    else:
        raise ValueError(step)
    return q, schema
