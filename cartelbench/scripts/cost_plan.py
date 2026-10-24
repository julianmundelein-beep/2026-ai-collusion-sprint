"""Round 4 cost plan (amendment 4, budget): expected and upper-bound cost from the measured cost per duopoly.

    python3 cartelbench/scripts/cost_plan.py

Reads cost_usd_per_duopoly from the summary.json of the recorded runs and writes evidence/round4/cost_plan.json.
Expected: the arm's own measured cost per duopoly (for a new arm: the closest measured arm, scaled as stated);
upper bound: the highest measured cost per duopoly of that model.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cartelbench.util import EVIDENCE_DIR, evidence_header, write_json  # noqa: E402

CAP_USD = 50.0


def per_duopoly() -> dict[tuple[str, str], float]:
    out = {}
    for d in sorted((EVIDENCE_DIR / "runs").iterdir()):
        p = d / "summary.json"
        if not p.exists():
            continue
        s = json.loads(p.read_text())
        c = (s.get("n_table") or {}).get("cost_usd_per_duopoly")
        if c is None or s.get("price_offset"):
            continue
        cfg = json.loads((d / "config.json").read_text()).get("config", {})
        if cfg.get("detection_prob") is not None or cfg.get("fine") is not None:
            continue
        out.setdefault((s["model"], s["regime"]), c)   # first (registered) run per model and regime
    return out


def main() -> int:
    c = per_duopoly()
    H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
    hmax = max(v for (m, _), v in c.items() if m == H)
    smax = max(v for (m, _), v in c.items() if m == S)
    nocomm_ratio = c[(H, "nocomm")] / c[(H, "fine")]       # a no-channel arm makes fewer calls per period
    core = ["laissez_faire", "fine", "leniency", "reward"]
    items = []
    for r in core:
        items.append({"block": "K1", "arm": f"Haiku {r}", "duopoles": 20, "per_duopoly": c[(H, r)], "upper_per_duopoly": hmax})
    for r in core:
        items.append({"block": "K2", "arm": f"Sonnet {r}", "duopoles": 10, "per_duopoly": c[(S, r)], "upper_per_duopoly": smax})
    items.append({"block": "K2", "arm": "Sonnet nocomm", "duopoles": 20, "per_duopoly": c[(S, "fine")] * nocomm_ratio,
                  "upper_per_duopoly": smax, "note": "Sonnet fine cost times the Haiku nocomm/fine ratio"})
    for r in core:
        items.append({"block": "C", "arm": f"Haiku {r} paraphrase", "duopoles": 20, "per_duopoly": c[(H, r)], "upper_per_duopoly": hmax})
    items.append({"block": "K3", "arm": "Sonnet nocomm + screen", "duopoles": 20, "per_duopoly": c[(S, "fine")] * nocomm_ratio, "upper_per_duopoly": smax})
    items.append({"block": "K3", "arm": "Haiku nocomm + screen", "duopoles": 20, "per_duopoly": c[(H, "nocomm")], "upper_per_duopoly": hmax})
    items.append({"block": "K3", "arm": "Haiku fine + screen", "duopoles": 20, "per_duopoly": c[(H, "fine")], "upper_per_duopoly": hmax})
    blocks = {}
    for it in items:
        it["expected_usd"] = round(it["duopoles"] * it["per_duopoly"], 3)
        it["upper_usd"] = round(it["duopoles"] * it["upper_per_duopoly"], 3)
        b = blocks.setdefault(it["block"], {"expected_usd": 0.0, "upper_usd": 0.0})
        b["expected_usd"] = round(b["expected_usd"] + it["expected_usd"], 3)
        b["upper_usd"] = round(b["upper_usd"] + it["upper_usd"], 3)
    total = {"expected_usd": round(sum(b["expected_usd"] for b in blocks.values()), 2),
             "upper_usd": round(sum(b["upper_usd"] for b in blocks.values()), 2), "cap_usd": CAP_USD}
    out = {**evidence_header("python3 cartelbench/scripts/cost_plan.py"), "items": items, "blocks": blocks, "total": total,
           "measured_per_duopoly": {f"{m} {r}": v for (m, r), v in c.items()}}
    write_json(EVIDENCE_DIR / "round4" / "cost_plan.json", out)
    for k, b in blocks.items():
        print(f"{k:3s} expected {b['expected_usd']:6.2f} USD, upper {b['upper_usd']:6.2f} USD")
    print(f"all expected {total['expected_usd']:.2f} USD, upper {total['upper_usd']:.2f} USD, cap {CAP_USD:.0f} USD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
