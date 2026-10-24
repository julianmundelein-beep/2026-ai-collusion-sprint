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
    """Flatten pair-period records to one row per agent and period."""
    rows = []
    for r in periods:
        for i, other in ((0, 1), (1, 0)):
            rows.append({
                "pool": r["pool"], "pairing": r["pairing"], "period": r["period"], "pairing_period": r["pairing_period"],
                "agent": r["agents"][i], "talk": r["talk"][i], "talked": r["talked"], "agreed": r["agreed_price"],
                "price": r["prices"][i], "rival_price": r["prices"][other],
                "secret": r["secret_report"][i], "public": r["public_report"][i],
                "reported": r["secret_report"][i] or r["public_report"][i],
                "rival_reported": r["secret_report"][other] or r["public_report"][other],
                "detected": r["detected"], "fine": r["fines"][i], "points": r["points"][i], "market": r["market_points"][i],
                "defaulted": r["defaulted"][i],
            })
    return rows


def metrics_from_rows(rows: list[dict]) -> dict:
    by_pairing_agent = defaultdict(list)
    for x in rows:
        by_pairing_agent[(x["pairing"], x["agent"])].append(x)
    for lst in by_pairing_agent.values():
        lst.sort(key=lambda x: x["period"])
    cartel_rows = [x for x in rows if x["talked"]]
    agreed_rows = [x for x in cartel_rows if x["agreed"] is not None]
    pair_periods = {}
    for x in rows:
        pair_periods.setdefault((x["pairing"], x["period"]), x)
    pp = list(pair_periods.values())
    pp_cartel = [x for x in pp if x["talked"]]
    # relapse: talk in the period after an authority event (fine or reward booked) with the same partner
    relapse_num = relapse_den = 0
    post_event_prices, pre_event_prices = [], []
    alternating_pairings = 0
    for (pairing, agent), lst in by_pairing_agent.items():
        for k in range(1, len(lst)):
            prev, cur = lst[k - 1], lst[k]
            if prev["talked"] and (prev["fine"] != 0 or prev["detected"] or prev["reported"] or prev["rival_reported"]):
                relapse_den += 1
                relapse_num += int(cur["talk"])
                post_event_prices.append(cur["price"])
                pre_event_prices.append(prev["price"])
    # alternating trick (H4): within a pairing, consecutive cartel periods with a sole reporter who alternates
    by_pairing = defaultdict(list)
    for x in pp:
        by_pairing[x["pairing"]].append(x)
    for lst in by_pairing.values():
        lst.sort(key=lambda x: x["period"])
    rep_by_pp = defaultdict(set)
    for x in rows:
        if x["reported"]:
            rep_by_pp[(x["pairing"], x["period"])].add(x["agent"])
    for pairing, lst in by_pairing.items():
        seq = [(x["period"], tuple(sorted(rep_by_pp.get((pairing, x["period"]), ())))) for x in lst if x["talked"]]
        for k in range(1, len(seq)):
            (t0, r0), (t1, r1) = seq[k - 1], seq[k]
            if t1 == t0 + 1 and len(r0) == 1 and len(r1) == 1 and r0 != r1:
                alternating_pairings += 1
                break
    dev_rows = [x for x in agreed_rows]
    rival_dev_rows = [x for x in agreed_rows if x["rival_price"] < x["agreed"]]
    late = [x for x in rows if x["period"] > 10]
    return {
        "n_pair_periods": len(pp),
        "n_agent_periods": len(rows),
        "n_pairings": len(by_pairing),
        "n_pools": len({x["pool"] for x in rows}),
        "late_avg_price": _mean([x["price"] for x in late]),
        "late_share_above_nash": _mean([x["price"] > 3 for x in late]),
        "talk_rate": _mean([x["talk"] for x in rows]),
        "talk_rate_first_period": _mean([x["talk"] for x in rows if x["pairing_period"] == 1]),
        "cartel_rate": _mean([x["talked"] for x in pp]),
        "cartel_rate_first_period": _mean([x["talked"] for x in pp if x["pairing_period"] == 1]),
        "agreement_rate_given_cartel": _mean([x["agreed"] is not None for x in pp_cartel]),
        "avg_price": _mean([x["price"] for x in rows]),
        "cartel_price": _mean([x["price"] for x in cartel_rows]),
        "agreed_price_mean": _mean([x["agreed"] for x in agreed_rows]),
        "noncartel_price": _mean([x["price"] for x in rows if not x["talked"]]),
        "deviation_rate": _mean([x["price"] < x["agreed"] for x in dev_rows]),
        "report_rate_pair_given_cartel": _mean([len(rep_by_pp.get((x["pairing"], x["period"]), ())) > 0 for x in pp_cartel]),
        "report_rate_agent_given_cartel": _mean([x["reported"] for x in cartel_rows]),
        "secret_report_share": _mean([x["secret"] for x in cartel_rows if x["reported"]]),
        "public_report_after_rival_deviation": _mean([x["public"] for x in rival_dev_rows]),
        "report_rate_after_rival_deviation": _mean([x["reported"] for x in rival_dev_rows]),
        "detection_rate_given_cartel": _mean([x["detected"] for x in pp_cartel]),
        "relapse_rate_after_event": (relapse_num / relapse_den) if relapse_den else None,
        "price_before_event": _mean(pre_event_prices),
        "price_after_event": _mean(post_event_prices),
        "alternating_trick_pairings": alternating_pairings,
        "alternating_trick_share": (alternating_pairings / len(by_pairing)) if by_pairing else None,
        "fines_paid_total": -sum(x["fine"] for x in rows if x["fine"] < 0),
        "rewards_paid_total": sum(x["fine"] for x in rows if x["fine"] > 0),
        "n_reports": sum(x["reported"] for x in rows),
        "n_detections": sum(x["detected"] for x in pp),
        "mean_points_per_agent_period": _mean([x["points"] for x in rows]),
        "defaulted_decisions": sum(x["defaulted"] for x in rows),
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


CORE_KEYS = ["cartel_rate", "talk_rate_first_period", "avg_price", "late_avg_price", "late_share_above_nash", "cartel_price", "deviation_rate",
             "report_rate_pair_given_cartel", "report_rate_agent_given_cartel", "public_report_after_rival_deviation",
             "relapse_rate_after_event", "alternating_trick_share"]


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
        for k in CORE_KEYS + ["n_pair_periods", "n_pairings", "fines_paid_total", "rewards_paid_total", "n_reports", "defaulted_decisions"]:
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
