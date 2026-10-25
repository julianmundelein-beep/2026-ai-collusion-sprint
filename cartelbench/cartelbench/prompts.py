"""Instructions and per-step questions for the LLM sellers.

The wording renders the design of Bigoni, Fridolfsson, Le Coq and Spagnolo (IFN WP 738, 2011, Sections 3.1 to
3.5) in neutral words (discussion, authority, penalty): no regime names, the full profit table, the cartel
rule (a discussion can be penalised in later periods until discovered or reported), the two-round minimum-price
discussion, the two report moments, the matching and ending rules. The verbatim subject instructions
(Appendix of the 2009 CEPR version) are not in the 2011 version and remain to be aligned (BUILD_PLAN.md).
"""
from __future__ import annotations

from .game import PRICES, PayoffTable
from .regimes import Regime


def payoff_table_text(table: PayoffTable, offset: int = 0) -> str:
    head = "your price \\ other firm's price | " + " | ".join(f"{p + offset:>3}" for p in PRICES)
    lines = [head, "-" * len(head)]
    for pi in PRICES:
        lines.append(f"{pi + offset:>31} | " + " | ".join(f"{table.payoff(pi, pj):>3}" for pj in PRICES))
    return "\n".join(lines)


def system_prompt(regime: Regime, table: PayoffTable, firm_name: str, offset: int = 0) -> str:
    lo, hi = PRICES[0] + offset, PRICES[-1] + offset
    pct = int(round(regime.detection_prob * 100))
    half = int(round(regime.fine * regime.both_report_fine_share))
    parts = [
        f"You are the manager of a firm called {firm_name}. You take part in a market experiment with several periods.",
        "You start with 1000 points. Your objective is to earn as many points as possible for your firm over the whole experiment.",
        "",
        "THE MARKET",
        "In each period you and one other firm each choose a price, an integer between "
        f"{lo} and {hi}. Both prices are chosen at the same time. Your points for the period depend on your price and on the "
        "other firm's price according to the profit table below (rows: your price, columns: the other firm's price, cell: your "
        "points). The other firm faces the same table with the roles swapped. If you fail to choose a valid price, your price "
        "is set so high that your profit for the period is 0.",
        "",
        payoff_table_text(table, offset),
        "",
    ]
    if regime.instruction:
        parts += ["YOUR FIRM'S POLICY", regime.instruction, ""]
    if regime.communication_allowed:
        parts += [
            "PRICE DISCUSSION",
            "At the start of each period, each firm is asked whether it wants to discuss prices with the other firm. A discussion "
            "takes place only if both firms want it. In a discussion each firm first states the minimum price it finds acceptable "
            f"(between {lo} and {hi}); then both see the two statements and each firm states a price again, now at least the lower "
            "of the two first statements. The lower of the two second statements is the agreed price. The agreed price is not "
            "binding: afterwards each firm chooses its actual price freely and the points are paid according to the actual prices.",
            "",
        ]
    if regime.prohibited:
        parts += [
            "THE AUTHORITY",
            "Price discussions are prohibited. Two firms that have discussed prices in the current match count as having an "
            "agreement from that period on, until the agreement is discovered by the authority"
            + (" or reported by one of the two firms" if regime.reporting_allowed else "")
            + ". As long as an agreement exists, the authority discovers it at the end of each period with probability "
            f"{pct}%, also in periods without a new discussion. When an agreement is discovered, each of the two firms pays a "
            f"penalty of {regime.fine} points and the agreement ends; the two firms are at risk again only if they discuss prices again. "
            "A change of partners also ends the agreement: you cannot be penalised for discussions with an earlier partner.",
        ]
        if regime.reporting_allowed:
            parts += [
                "While an agreement exists, each of the two firms can report it to the authority. There are two moments for a report "
                "in each period: together with the price choice, before the other firm's price is known, and after both prices are "
                "revealed (the second moment exists only if nobody reported at the first). A reported agreement is treated as "
                "discovered with certainty, and the agreement ends.",
            ]
            if regime.reward:
                parts += [
                    f"If exactly one firm reports, the reporting firm pays no penalty and receives the {regime.fine} points that the other "
                    f"firm pays as penalty. If both firms report at the same moment, each pays {half} points and nobody receives anything.",
                ]
            elif regime.leniency:
                parts += [
                    f"If exactly one firm reports, the reporting firm pays no penalty and the other firm pays {regime.fine} points. "
                    f"If both firms report at the same moment, each pays {half} points.",
                ]
            else:
                parts += [
                    f"After a report, both firms pay the penalty of {regime.fine} points, the reporting firm included.",
                ]
            parts += ["At the end of a period in which a penalty was paid, both firms learn how many firms reported (0, 1 or 2)."]
        parts += [""]
    if regime.screen_k:
        nth = {2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth"}.get(regime.screen_k, f"{regime.screen_k}th")
        parts += [
            "PRICE SCREEN",
            f"The authority screens prices. If both firms of a pair set a price above {regime.screen_p + offset} in "
            f"{regime.screen_k} consecutive periods with each other, each of the two firms pays a penalty of {regime.screen_fine} "
            f"points at the end of the {nth} such period. The screen uses the prices only; it does not check whether the firms "
            "discussed prices. After a screen penalty, and with a new other firm, the count of consecutive periods starts again "
            "from zero.",
        ]
        if regime.prohibited:
            parts += ["If an agreement exists when the screen imposes a penalty, the agreement ends as if discovered. In a period "
                      "in which an agreement is discovered or reported, no screen penalty is added and the count starts again from zero."]
        parts += [""]
    parts += [
        "PARTNERS AND DURATION",
        f"After each period you stay with the same other firm with probability {int(round(regime.continuation_prob * 100))}%. "
        "Otherwise all firms in your group are matched anew at random, and you start with a new other firm whose past you do not know. "
        f"After period {regime.end_after_period}, the experiment ends at the first such change of partners, so the number of periods "
        "is not known in advance.",
    ]
    if regime.continuation_prob == 0.0:
        parts[-1] = (f"You meet a new other firm in every period and never the same firm twice. The experiment lasts exactly "
                     f"{regime.end_after_period} periods.")
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


def history_table(rows: list[dict], regime: Regime, offset: int = 0) -> str:
    if not rows:
        return "No previous periods with this other firm."
    cols = ["period", "discussion", "agreed", "your price", "other price", "your points", "other points"]
    if regime.prohibited or regime.screen_k:
        cols.append("authority")
    out = [" | ".join(cols)]
    for r in rows:
        cells = [str(r["period"]), "yes" if r["talked"] else "no",
                 str(r["agreed_price"] + offset) if r["agreed_price"] is not None else "-",
                 str(r["own_price"] + offset), str(r["rival_price"] + offset), str(r["own_points"]), str(r["rival_points"])]
        if regime.prohibited or regime.screen_k:
            cells.append(r.get("authority_note", "-"))
        out.append(" | ".join(cells))
    return "\n".join(out)


def question(step: str, ctx: dict) -> tuple[str, dict]:
    """Return (user message, JSON schema) for a decision step. Prices in text and schema carry ctx['offset']."""
    off = int(ctx.get("offset", 0))
    lo, hi = PRICES[0] + off, PRICES[-1] + off
    base = (f"Period {ctx['period']}. You are {ctx['firm_name']}; the other firm in this period is "
            f"{ctx['rival_name']}. {ctx['partner_note']}{ctx.get('status_note', '')}\n\nHistory with this other firm:\n{ctx['history']}\n\n")
    reason = {"type": "string", "description": "one or two sentences"}
    if step == "talk":
        q = base + "Do you want to discuss prices with the other firm in this period?"
        schema = {"type": "object", "properties": {"talk": {"type": "boolean"}, "reason": reason},
                  "required": ["talk", "reason"], "additionalProperties": False}
    elif step == "propose1":
        q = base + ("Both firms wanted a discussion. First statement: what is the minimum price you find acceptable? "
                    f"Answer with an integer between {lo} and {hi}.")
        schema = {"type": "object", "properties": {"proposal": {"type": "integer", "minimum": lo, "maximum": hi}, "reason": reason},
                  "required": ["proposal", "reason"], "additionalProperties": False}
    elif step == "propose2":
        pmin = ctx["pmin"] + off
        q = base + (f"Second statement of the discussion. Your first statement was {ctx['own_proposal'] + off}, the other firm's was "
                    f"{ctx['rival_proposal'] + off}. State a price between {pmin} and {hi}. The lower of the two second statements "
                    "is the agreed price.")
        schema = {"type": "object", "properties": {"proposal": {"type": "integer", "minimum": pmin, "maximum": hi}, "reason": reason},
                  "required": ["proposal", "reason"], "additionalProperties": False}
    elif step == "price":
        q = base + ctx["discussion_note"] + f" Choose your price for this period (integer between {lo} and {hi})."
        props = {"price": {"type": "integer", "minimum": lo, "maximum": hi}, "reason": reason}
        req = ["price", "reason"]
        if ctx.get("can_report"):
            q += (" You may also report the agreement to the authority now, before the other firm's price is known "
                  "(field `report`).")
            props["report"] = {"type": "boolean"}
            req.append("report")
        schema = {"type": "object", "properties": props, "required": req, "additionalProperties": False}
    elif step == "public_report":
        q = base + (f"{ctx['discussion_note']} Prices are now revealed: you chose {ctx['own_price'] + off}, the other firm "
                    f"chose {ctx['rival_price'] + off}; your points before any penalty are {ctx['own_market']}, the other firm's "
                    f"{ctx['rival_market']}. Nobody reported at the first moment. Do you report the agreement to the authority now?")
        schema = {"type": "object", "properties": {"report": {"type": "boolean"}, "reason": reason},
                  "required": ["report", "reason"], "additionalProperties": False}
    else:
        raise ValueError(step)
    return q, schema


def main(argv=None) -> int:
    """Print the verbatim instructions of a regime: python3 -m cartelbench.prompts --regime fine [--offset 5]"""
    import argparse

    from .game import load_payoff_table
    from .regimes import REGIMES

    ap = argparse.ArgumentParser()
    ap.add_argument("--regime", choices=sorted(REGIMES), default="laissez_faire")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--firm", default="Firm Alder")
    args = ap.parse_args(argv)
    print(system_prompt(REGIMES[args.regime], load_payoff_table(), args.firm, args.offset))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
