"""Two questions of jury round R05 answered from recorded data, no new run (to-do items 6 and 10).

    python3 cartelbench/scripts/jury_answers.py

(a) Which permutation test gave p 0.029 for 4 against 4 pool sessions and p 0.002 for 8 against 4 (screen arms,
    M72; prohibition against no channel, M67): reads the recorded test records and recounts the relabellings.
(b) How 5 formations in 247 pair-periods (F66) fit 10 cartels formed and 9 convictions (F16): recounts the
    leniency run (Haiku 5.5, seed 3) from periods.jsonl.
Writes evidence/round5/jury_answers.json.
"""
from __future__ import annotations

import json
import pathlib
import sys
from collections import defaultdict
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cartelbench.pools import find_run  # noqa: E402
from cartelbench.util import EVIDENCE_DIR, evidence_header, read_jsonl, write_json  # noqa: E402


def permutation_records() -> list[dict]:
    out = []
    screen = json.loads((EVIDENCE_DIR / "round4" / "screen.json").read_text())
    for arm in screen["arms"]:
        p = arm["differences"]["avg_price"]["permutation"]
        out.append({"source": "M72 screen arms (amendment 5)", "comparison": arm["label"] + ", avg_price screen minus no screen", **_rec(p)})
    nocomm = json.loads((EVIDENCE_DIR / "round4" / "nocomm_comparison.json").read_text())
    for model in ("sonnet", "haiku"):
        for reg, d in nocomm[model]["comparisons"].items():
            p = d["avg_price"]["permutation"]
            out.append({"source": "M67/M68 prohibition against no channel (amendment 4 (b))",
                        "comparison": f"{nocomm[model]['model']} {reg} minus nocomm, avg_price", **_rec(p)})
    sc = json.loads((EVIDENCE_DIR / "round4" / "scorecard_haiku_8pool" / "scorecard.json").read_text())
    for t in sc["permutation_tests"][:2]:
        out.append({"source": "M64 scorecard rows (amendment 4 (a))", "comparison": f"row {t['row']} {t['test']} {t['measure']}", **_rec(t["permutation"])})
    return out


def _rec(p: dict) -> dict:
    return {"alternative": p["alternative"], "p": p["p"], "count": p["count_at_least_observed"], "relabellings": p["relabellings"],
            "exact": p["exact"], "clusters": [p["clusters_a"], p["clusters_b"]], "as_fraction": f"{p['count_at_least_observed']}/{p['relabellings']}",
            "minimum_two_sided": (2 if p["clusters_a"] == p["clusters_b"] else 1) / p["relabellings"] if p["exact"] else None,
            "minimum_one_sided": 1 / p["relabellings"] if p["exact"] else None}


def leniency_counts() -> dict:
    d = find_run("claude-haiku-5-5", "leniency", 3)
    rows = [r for r in read_jsonl(d / "periods.jsonl") if not r.get("header")]
    by = defaultdict(list)
    for r in rows:
        by[r["pairing"]].append(r)
    formations, ends = [], []
    for r in rows:
        if not r["new_cartel"]:
            continue
        seq = sorted((x for x in by[r["pairing"]] if x["period"] >= r["period"]), key=lambda x: x["period"])
        end = next((x for x in seq if x["convicted"]), None)
        formations.append({"pairing": r["pairing"], "formed": r["period"]})
        ends.append({"pairing": r["pairing"], "formed": r["period"],
                     "end": (end["period"], end["conviction"], len(end["reporters"])) if end else ("episode ended", seq[-1]["period"])})
    conv = [r for r in rows if r["convicted"]]
    n_form, n_free = len(formations), sum(1 for r in rows if not r["cartel_active_start"])
    frac = Fraction(n_form, n_free)
    return {"run": d.name, "pair_periods": len(rows), "cartel_pair_periods": sum(1 for r in rows if r["cartel_active"]),
            "pair_periods_without_running_cartel": n_free, "cartels_formed": n_form,
            "formation_rate": n_form / n_free, "formation_rate_reduced_fraction": f"{frac.numerator}/{frac.denominator}",
            "convictions": len(conv), "by_detection": sum(r["conviction"] == "detection" for r in conv),
            "report_events": sum(r["conviction"] == "report" for r in conv), "reporters": sum(len(r["reporters"]) for r in conv),
            "cartels_not_convicted": [e for e in ends if e["end"][0] == "episode ended"], "cartel_ends": ends}


def main() -> int:
    perms = permutation_records()
    len_ = leniency_counts()
    answers = {
        "a": ("The screen comparisons (M72) and the prohibition-against-no-channel comparisons (M67, M68) use the two-sided "
              "permutation test registered in amendments 5 and 4 (b): p is the share of relabellings of the pool sessions with "
              "|statistic| at least the observed one. With 4 against 4 pool sessions and complete separation, the observed "
              "relabelling and its mirror image both reach it: p = 2/70 = 0.029. With 8 against 4 pool sessions (fine_screen "
              "against the 8-pool fine sample) the groups differ in size, so no mirror relabelling exists and only the observed "
              "one reaches it: p = 1/495 = 0.002, the same as the one-sided minimum. The scorecard rows (M64) are one-sided in "
              "the humans' direction (amendment 4 (a)): minimum 1/70 = 0.014 for 4 against 4. No add-one correction is applied "
              "to exact tests."),
        "a_methods_sentence": ("Permutation p-values relabel pool sessions between the two arms (exact enumeration up to 10,000 "
                               "relabellings); they are one-sided in the humans' direction for the scorecard rows and two-sided for "
                               "the comparisons without a human direction (prohibition against no channel, screen against no screen). "
                               "Under complete separation the smallest attainable p is 1/70 = 0.014 (one-sided) or 2/70 = 0.029 "
                               "(two-sided) for 4 against 4 pool sessions and 1/495 = 0.002 for 8 against 4, where unequal group "
                               "sizes leave no mirror relabelling."),
        "b": (f"The leniency run formed {len_['cartels_formed']} cartels in {len_['pair_periods_without_running_cartel']} pair-periods "
              f"without a running cartel at the start of the period (formation rate {len_['formation_rate']:.4f}); F66's "
              f"\"5 of 247\" is this ratio reduced to lowest terms, not a count. {len_['convictions']} of the {len_['cartels_formed']} "
              f"cartels were convicted ({len_['by_detection']} by detection, {len_['report_events']} by report events with "
              f"{len_['reporters']} reporters, one event with two); the tenth formed in the last period of its pairing episode "
              f"and ended with the rematch, unconvicted."),
        "b_note_clause": (f"10 formations in 494 pair-periods without a running cartel, 0.020; 9 of the 10 cartels were convicted "
                          f"and one ended with a rematch in its first period"),
    }
    out = {**evidence_header("python3 cartelbench/scripts/jury_answers.py"), "answers": answers, "permutation_records": perms,
           "leniency_counts": len_}
    write_json(EVIDENCE_DIR / "round5" / "jury_answers.json", out)
    for p in perms:
        print(f"{p['source']:55s} {p['comparison']:70s} {p['alternative']:9s} p {p['p']:.4f} = {p['as_fraction']}, pools {p['clusters']}")
    print(json.dumps({k: v for k, v in len_.items() if k != "cartel_ends"}, indent=1))
    print("\n(a)", answers["a"], "\n\n(b)", answers["b"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
