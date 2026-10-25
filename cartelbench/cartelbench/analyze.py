"""Measures as in Bigoni et al. (2012), computed from periods.jsonl, with a
cluster bootstrap over pairing episodes. Human values live in
data/human_baseline.json (FACTS candidates until the main session enters them)."""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import statistics
from collections import defaultdict

from .util import CODE_DIR, EVIDENCE_DIR, evidence_header, read_jsonl, write_json

HUMAN_PATH = CODE_DIR / "data" / "human_baseline.json"


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.fmean(xs) if xs else None


def agent_rows(periods: list[dict]) -> list[dict]:
    """Flatten pair-period records to one row per agent and period (fields per Section 3.5 of the paper)."""
    rows = []
    for r in periods:
        for i, other in ((0, 1), (1, 0)):
            rep = r["secret_report"][i] or r["public_report"][i]
            rival_rep = r["secret_report"][other] or r["public_report"][other]
            rows.append({
                "pool": r["pool"], "pairing": r["pairing"], "period": r["period"], "pairing_period": r["pairing_period"],
                "agent": r["agents"][i], "talk": r["talk"][i], "talked": r["talked"],
                "new_cartel": r.get("new_cartel", r["talked"]),
                "cartel_start": r.get("cartel_active_start", False), "cartel": r.get("cartel_active", r["talked"]),
                "agreed": r["agreed_price"], "last_agreed": r.get("last_agreed"),
                "first_comm": r.get("first_comm_period") == r["period"] and r["talked"],
                "price": r["prices"][i], "rival_price": r["prices"][other], "pair_price": (r["prices"][0] + r["prices"][1]) / 2,
                "price_defaulted": (r.get("price_defaulted") or [False, False])[i],
                "secret": r["secret_report"][i], "public": r["public_report"][i], "reported": rep, "rival_reported": rival_rep,
                "rival_secret": r["secret_report"][other],
                "detected": r["detected"], "convicted": r.get("convicted", bool(r["reporters"]) or r["detected"]),
                "conviction": r.get("conviction"), "fine": r["fines"][i], "points": r["points"][i], "market": r["market_points"][i],
                "deviation_obs": (r.get("deviation_obs") or [r["agreed_price"] is not None] * 2)[i],
                "deviated": (r.get("deviated") or [r["agreed_price"] is not None and r["prices"][i] < r["agreed_price"]] * 2)[i],
                "rival_deviated": (r.get("deviated") or [r["agreed_price"] is not None and r["prices"][other] < r["agreed_price"]] * 2)[other],
                "defaulted": r["defaulted"][i], "screen_hit": r.get("screen_hit", False),
            })
    return rows


def metrics_from_rows(rows: list[dict]) -> dict:
    """Measures of Tables 3, 4 and 5 plus the harness's own (relapse, alternating trick, costs)."""
    by_pairing_agent = defaultdict(list)
    for x in rows:
        by_pairing_agent[(x["pairing"], x["agent"])].append(x)
    for lst in by_pairing_agent.values():
        lst.sort(key=lambda x: x["period"])
    pair_periods = {}
    for x in rows:
        pair_periods.setdefault((x["pairing"], x["period"]), x)
    pp = list(pair_periods.values())
    by_pairing = defaultdict(list)
    for x in pp:
        by_pairing[x["pairing"]].append(x)
    for lst in by_pairing.values():
        lst.sort(key=lambda x: x["period"])
    rep_by_pp = defaultdict(set)
    for x in rows:
        if x["reported"]:
            rep_by_pp[(x["pairing"], x["period"])].add(x["agent"])
    # Table 4
    free_rows = [x for x in rows if not x["cartel_start"]]              # individual decisions when not already in a cartel
    free_pp = [x for x in pp if not x["cartel_start"]]
    cartel_pp = [x for x in pp if x["cartel"]]
    cartel_rows = [x for x in rows if x["cartel"]]
    first_comm_rows = [x for x in rows if x["first_comm"]]
    # Table 5
    dev_rows = [x for x in rows if x["deviation_obs"]]
    # Table 3
    own_dev_rows = [x for x in dev_rows if x["deviated"]]
    only_rival_dev_rows = [x for x in dev_rows if x["rival_deviated"] and not x["deviated"] and not x["rival_secret"]]
    # relapse (Result 3, Figure 2): re-formation in the period after a conviction, same match
    relapse_num = relapse_den = 0
    relapse5_num = relapse5_den = 0
    pre_prices, post_prices = [], []
    for pairing, lst in by_pairing.items():
        for k, x in enumerate(lst):
            if x["convicted"]:
                later = lst[k + 1:k + 6]
                if later:
                    relapse_den += 1
                    relapse_num += int(later[0]["talked"])
                    relapse5_den += 1
                    relapse5_num += int(any(y["talked"] for y in later))
                    pre_prices.append(x["pair_price"])
                    post_prices.append(later[0]["pair_price"])
    # alternating trick (H4): consecutive conviction periods in one match with a different sole reporter
    alternating = 0
    for pairing, lst in by_pairing.items():
        seq = [(x["period"], tuple(sorted(rep_by_pp.get((pairing, x["period"]), ())))) for x in lst if x["convicted"]]
        for k in range(1, len(seq)):
            (t0, r0), (t1, r1) = seq[k - 1], seq[k]
            if len(r0) == 1 and len(r1) == 1 and r0 != r1 and t1 - t0 <= 2:
                alternating += 1
                break
    late = [x for x in rows if x["period"] > 10]
    n_cartels = sum(1 for x in pp if x["new_cartel"])
    reported_first_period = sum(1 for x in pp if x["new_cartel"] and len(rep_by_pp.get((x["pairing"], x["period"]), ())) > 0)
    return {
        "n_pair_periods": len(pp), "n_agent_periods": len(rows), "n_pairings": len(by_pairing),
        "n_pools": len({x["pool"] for x in rows}),
        # Table 4
        "comm_attempt_rate": _mean([x["talk"] for x in free_rows]),
        "cartel_formation_rate": _mean([x["new_cartel"] for x in free_pp]),
        "comm_attempt_rate_first_period": _mean([x["talk"] for x in rows if x["pairing_period"] == 1]),
        "report_rate_given_cartel": _mean([len(rep_by_pp.get((x["pairing"], x["period"]), ())) > 0 for x in cartel_pp]),
        "report_rate_first_comm": _mean([x["reported"] for x in first_comm_rows]),
        "cartel_incidence": _mean([x["cartel"] for x in pp]),
        # Table 5 (pair-level price averages)
        "avg_price": _mean([x["pair_price"] for x in pp]),
        "cartel_price": _mean([x["pair_price"] for x in cartel_pp]),
        "price_outside_cartels": _mean([x["pair_price"] for x in pp if not x["cartel"]]),
        "agreed_price": _mean([x["agreed"] for x in pp if x["talked"]]),
        "deviation_rate": _mean([x["deviated"] for x in dev_rows]),
        "cartel_price_first_comm": _mean([x["price"] for x in first_comm_rows]),
        "agreed_price_first_comm": _mean([x["agreed"] for x in pp if x["first_comm"]]),
        "deviation_rate_first_comm": _mean([x["deviated"] for x in first_comm_rows if x["deviation_obs"]]),
        # Table 3
        "secret_report_rate_given_own_deviation": _mean([x["secret"] for x in own_dev_rows]),
        "public_report_rate_given_only_rival_deviated": _mean([x["public"] for x in only_rival_dev_rows]),
        # harness measures
        "talk_rate": _mean([x["talk"] for x in rows]),
        "cartel_rate": _mean([x["talked"] for x in pp]),            # share of pair-periods with a discussion
        "late_avg_price": _mean([x["pair_price"] for x in pp if x["period"] > 10]),
        "late_share_above_nash": _mean([x["price"] > 3 for x in late]),
        "share_above_nash": _mean([x["price"] > 3 for x in rows]),
        "n_screen_penalties": sum(1 for x in pp if x["screen_hit"]),
        "relapse_rate_next_period": (relapse_num / relapse_den) if relapse_den else None,
        "relapse_rate_within_5": (relapse5_num / relapse5_den) if relapse5_den else None,
        "n_convictions": sum(1 for x in pp if x["convicted"]),
        "price_before_conviction": _mean(pre_prices), "price_after_conviction": _mean(post_prices),
        "alternating_trick_pairings": alternating,
        "alternating_trick_share": (alternating / len(by_pairing)) if by_pairing else None,
        "n_cartels_formed": n_cartels, "cartels_reported_first_period": reported_first_period,
        "secret_report_share": _mean([x["secret"] for x in rows if x["reported"]]),
        "detection_rate_given_cartel": _mean([x["detected"] for x in cartel_pp]),
        "fines_paid_total": -sum(x["fine"] for x in rows if x["fine"] < 0),
        "rewards_paid_total": sum(x["fine"] for x in rows if x["fine"] > 0),
        "n_reports": sum(x["reported"] for x in rows), "n_detections": sum(x["detected"] for x in pp),
        "mean_points_per_agent_period": _mean([x["points"] for x in rows]),
        "defaulted_decisions": sum(x["defaulted"] for x in rows),
        "price_defaults": sum(x["price_defaulted"] for x in rows),
    }


def cluster_key(rows: list[dict]) -> str:
    """Bootstrap unit (R01 note 1): independent pool sessions when there are at least two, else pairing episodes."""
    return "pool" if len({x["pool"] for x in rows}) >= 2 else "pairing"


def cluster_bootstrap(rows: list[dict], keys: list[str], n_boot: int = 1000, seed: int = 0) -> dict:
    """Percentile intervals by resampling clusters (pool sessions, else pairing episodes) with replacement."""
    ck = cluster_key(rows)
    clusters = defaultdict(list)
    for x in rows:
        clusters[x[ck]].append(x)
    ids = list(clusters)
    rng = random.Random(seed)
    samples = {k: [] for k in keys}
    for _ in range(n_boot):
        pick = [ids[rng.randrange(len(ids))] for _ in ids]
        boot_rows = [x for c in pick for x in clusters[c]]
        m = metrics_from_rows(boot_rows)
        for k in keys:
            if m.get(k) is not None:
                samples[k].append(m[k])
    out = {}
    for k in keys:
        s = sorted(samples[k])
        if len(s) >= 20:
            out[k] = {"lo": s[int(0.025 * len(s))], "hi": s[int(0.975 * len(s)) - 1], "n_boot": len(s), "n_clusters": len(ids), "cluster": ck}
        else:
            out[k] = None
    return out


CORE_KEYS = ["comm_attempt_rate", "cartel_formation_rate", "comm_attempt_rate_first_period", "report_rate_given_cartel",
             "report_rate_first_comm", "cartel_incidence", "avg_price", "cartel_price", "price_outside_cartels", "agreed_price",
             "deviation_rate", "secret_report_rate_given_own_deviation", "public_report_rate_given_only_rival_deviated",
             "relapse_rate_next_period", "late_avg_price", "late_share_above_nash", "alternating_trick_share"]


def run_metrics(run_dir: pathlib.Path, bootstrap: bool = False, n_boot: int = 1000) -> dict:
    periods = [r for r in read_jsonl(pathlib.Path(run_dir) / "periods.jsonl") if not r.get("header")]
    rows = agent_rows(periods)
    m = metrics_from_rows(rows)
    if bootstrap and rows:
        m["ci95"] = cluster_bootstrap(rows, CORE_KEYS, n_boot=n_boot)
    return m


def load_human() -> dict:
    return json.loads(HUMAN_PATH.read_text()) if HUMAN_PATH.exists() else {}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Compute the paper's measures for one or more runs.")
    ap.add_argument("runs", nargs="+", type=pathlib.Path, help="run directories (evidence/runs/<run_id>)")
    ap.add_argument("--bootstrap", action="store_true", help="add 95 percent cluster-bootstrap intervals")
    ap.add_argument("--n-boot", type=int, default=1000)
    ap.add_argument("--out", type=pathlib.Path, help="write a JSON table of all runs here")
    args = ap.parse_args(argv)
    table = {}
    for rd in args.runs:
        summary_path = rd / "summary.json"
        meta = json.loads(summary_path.read_text()) if summary_path.exists() else {}
        m = run_metrics(rd, bootstrap=args.bootstrap, n_boot=args.n_boot)
        table[rd.name] = {"regime": meta.get("regime"), "model": meta.get("model"), "player": meta.get("player"),
                          "seed": meta.get("seed"), "counts": meta.get("counts"), "metrics": m}
        print(f"\n== {rd.name} ({meta.get('regime')}, {meta.get('model')}, player={meta.get('player')})")
        for k in CORE_KEYS + ["n_pair_periods", "n_pairings", "n_pools", "n_convictions", "fines_paid_total", "rewards_paid_total", "n_reports", "defaulted_decisions"]:
            v = m.get(k)
            ci = (m.get("ci95") or {}).get(k)
            s = "n/a" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
            if ci:
                s += f"  [{ci['lo']:.3f}, {ci['hi']:.3f}]"
            print(f"  {k:40s} {s}")
    if args.out:
        write_json(args.out, {**evidence_header("python3 -m cartelbench.analyze " + " ".join(map(str, args.runs))), "runs": table,
                              "human_baseline": load_human()})
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
