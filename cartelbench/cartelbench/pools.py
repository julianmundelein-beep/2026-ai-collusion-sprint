"""Pool sessions across runs (pre-registration amendment 4): merge runs of one regime into one sample, split a
sample into its pool sessions, and the permutation test over pool sessions.

Every measure the scorecard uses is a ratio of sums over pool sessions (pairing episodes never cross pools), so
the measure of any set of pool sessions is sum(num) / sum(den) of its parts; `ratio_parts` gives these parts and
a test checks them against `analyze.metrics_from_rows`.
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import random
from collections import defaultdict

from .analyze import metrics_from_rows
from .scorecard import load_run
from .util import EVIDENCE_DIR

RUNS_DIR = EVIDENCE_DIR / "runs"


def run_variant(run_dir: pathlib.Path) -> str:
    try:
        cfg = json.loads((run_dir / "config.json").read_text()).get("config") or {}
    except (OSError, ValueError):
        return "original"
    return cfg.get("prompt_variant") or "original"


def find_run(model: str, regime: str, seed: int, runs_dir: pathlib.Path = RUNS_DIR) -> pathlib.Path:
    """The one complete run of this model, regime and seed (seeds are unique per model and regime)."""
    hits = []
    for d in sorted(runs_dir.iterdir()):
        p = d / "summary.json"
        if not p.exists():
            continue
        s = json.loads(p.read_text())
        if s.get("model") == model and s.get("regime") == regime and s.get("seed") == seed:
            hits.append(d)
    if len(hits) != 1:
        raise LookupError(f"{len(hits)} complete runs for {model} {regime} seed {seed}")
    return hits[0]


def merge_runs(dirs: list[pathlib.Path]) -> dict:
    """One sample from several runs of one regime: pool sessions and pairing episodes keep their run identity."""
    loaded = [load_run(pathlib.Path(d)) for d in dirs]
    if len(loaded) == 1:
        return loaded[0]
    regimes = {r["summary"]["regime"] for r in loaded}
    if len(regimes) != 1:
        raise ValueError(f"cannot merge different regimes: {sorted(regimes)}")
    rows = []
    periods, counts, n_table = {}, defaultdict(float), defaultdict(float)
    for r in loaded:
        s = r["summary"]
        tag = f"s{s['seed']}"
        for x in r["rows"]:
            y = dict(x)
            y["pool"] = f"{tag}:{x['pool']}"
            y["pairing"] = f"{tag}:{x['pairing']}"
            rows.append(y)
        for k, v in (s.get("periods_per_pool") or {}).items():
            periods[f"{tag}:{k}"] = v
        for k, v in (s.get("counts") or {}).items():
            counts[k] += v or 0
        for k in ("calls", "refusals", "invalid_json", "errors", "defaulted", "cost_usd", "duopoles", "pool_sessions"):
            n_table[k] += (s.get("n_table") or {}).get(k) or 0
    first = loaded[0]["summary"]
    summary = {**first, "run_id": " + ".join(r["summary"]["run_id"] for r in loaded),
               "run_ids": [r["summary"]["run_id"] for r in loaded], "seed": [r["summary"]["seed"] for r in loaded],
               "pools": int(n_table["pool_sessions"]), "duopoles": int(n_table["duopoles"]), "periods_per_pool": periods,
               "counts": {k: (int(v) if float(v).is_integer() else v) for k, v in counts.items()},
               "n_table": {**{k: int(v) for k, v in n_table.items() if k != "cost_usd"}, "cost_usd": n_table["cost_usd"]}}
    return {"dir": [str(d) for d in dirs], "summary": summary, "rows": rows, "metrics": metrics_from_rows(rows)}


def pool_sessions(rows: list[dict]) -> dict[str, list[dict]]:
    out = defaultdict(list)
    for x in rows:
        out[x["pool"]].append(x)
    return dict(out)


def _pair_periods(rows: list[dict]) -> list[dict]:
    pp = {}
    for x in rows:
        pp.setdefault((x["pairing"], x["period"]), x)
    return list(pp.values())


def ratio_parts(rows: list[dict], key: str) -> tuple[float, int]:
    """(numerator, denominator) of a measure, following analyze.metrics_from_rows."""
    pp = _pair_periods(rows)
    if key == "cartel_formation_rate":
        sel = [x for x in pp if not x["cartel_start"]]
        return float(sum(x["new_cartel"] for x in sel)), len(sel)
    if key == "cartel_incidence":
        return float(sum(x["cartel"] for x in pp)), len(pp)
    if key == "avg_price":
        return float(sum(x["pair_price"] for x in pp)), len(pp)
    if key == "late_avg_price":
        sel = [x for x in pp if x["period"] > 10]
        return float(sum(x["pair_price"] for x in sel)), len(sel)
    if key == "cartel_price":
        sel = [x for x in pp if x["cartel"]]
        return float(sum(x["pair_price"] for x in sel)), len(sel)
    if key == "share_above_nash":
        return float(sum(x["price"] > 3 for x in rows)), len(rows)
    # amendment 6
    if key in ("share_at_4", "share_at_5", "share_above_4"):
        q = {"share_at_4": lambda p: p == 4, "share_at_5": lambda p: p == 5, "share_above_4": lambda p: p > 4}[key]
        return float(sum(q(x["price"]) for x in rows)), len(rows)
    if key == "mean_points_per_agent_period":
        return float(sum(x["points"] for x in rows)), len(rows)
    if key.startswith("llm_"):
        sel = [x for x in rows if x["kind"] == "llm"]
        if key == "llm_late_avg_price":
            sel = [x for x in sel if x["period"] > 10]
        f = {"llm_avg_price": lambda x: x["price"], "llm_late_avg_price": lambda x: x["price"],
             "llm_share_above_nash": lambda x: x["price"] > 3, "llm_points_per_agent_period": lambda x: x["points"]}[key]
        return float(sum(f(x) for x in sel)), len(sel)
    if key == "both_above_4":
        return float(sum(x["both_above_4"] for x in pp)), len(pp)
    if key == "asymmetric_above_4":
        return float(sum((x["price"] > 4) != (x["rival_price"] > 4) for x in pp)), len(pp)
    if key == "alternation_share":
        by_pairing = defaultdict(list)
        for x in pp:
            by_pairing[x["pairing"]].append(x)
        num = den = 0
        for lst in by_pairing.values():
            lst.sort(key=lambda x: x["period"])
            for k in range(1, len(lst)):
                den += 1
                num += int(lst[k]["both_above_4"] != lst[k - 1]["both_above_4"])
        return float(num), den
    if key == "late_share_above_nash":
        sel = [x for x in rows if x["period"] > 10]
        return float(sum(x["price"] > 3 for x in sel)), len(sel)
    if key == "report_rate_given_cartel":
        reported = {(x["pairing"], x["period"]) for x in rows if x["reported"]}
        sel = [x for x in pp if x["cartel"]]
        return float(sum((x["pairing"], x["period"]) in reported for x in sel)), len(sel)
    if key == "deviation_rate":
        sel = [x for x in rows if x["deviation_obs"]]
        return float(sum(x["deviated"] for x in sel)), len(sel)
    if key == "public_report_rate_given_only_rival_deviated":
        sel = [x for x in rows if x["deviation_obs"] and x["rival_deviated"] and not x["deviated"] and not x["rival_secret"]]
        return float(sum(x["public"] for x in sel)), len(sel)
    if key == "relapse_rate_next_period":
        by_pairing = defaultdict(list)
        for x in pp:
            by_pairing[x["pairing"]].append(x)
        num = den = 0
        for lst in by_pairing.values():
            lst.sort(key=lambda x: x["period"])
            for k, x in enumerate(lst):
                if x["convicted"] and k + 1 < len(lst):
                    den += 1
                    num += int(lst[k + 1]["talked"])
        return float(num), den
    raise KeyError(key)


def cluster_parts(rows: list[dict], key: str) -> list[tuple[float, int]]:
    return [ratio_parts(c, key) for _, c in sorted(pool_sessions(rows).items())]


def _ratio(parts) -> float | None:
    den = sum(d for _, d in parts)
    return None if den == 0 else sum(n for n, _ in parts) / den


def permutation_test(parts_a: list[tuple[float, int]], parts_b: list[tuple[float, int]], alternative: str = "greater",
                     n_max: int = 10_000, seed: int = 0) -> dict | None:
    """Relabel pool sessions between two samples (group sizes kept). Statistic: measure(A) minus measure(B).

    greater: p = share of relabellings with a statistic >= the observed one; two-sided: |statistic| >= |observed|.
    Exact enumeration when there are at most n_max distinct relabellings, else n_max random draws with
    random.Random(seed) and p = (1 + count) / (1 + n_max). Relabellings with an undefined measure never count.
    """
    obs_a, obs_b = _ratio(parts_a), _ratio(parts_b)
    if obs_a is None or obs_b is None:
        return None
    obs = obs_a - obs_b
    allp = list(parts_a) + list(parts_b)
    n, k = len(allp), len(parts_a)
    total = math.comb(n, k)
    eps = 1e-12

    def stat(idx: tuple[int, ...]) -> float | None:
        s = set(idx)
        a = _ratio([allp[i] for i in idx])
        b = _ratio([allp[i] for i in range(n) if i not in s])
        return None if a is None or b is None else a - b

    def hit(v: float) -> bool:
        return (v >= obs - eps) if alternative == "greater" else (abs(v) >= abs(obs) - eps)

    count = undefined = 0
    if total <= n_max:
        draws = itertools.combinations(range(n), k)
        exact = True
    else:
        rng = random.Random(seed)
        draws = (tuple(sorted(rng.sample(range(n), k))) for _ in range(n_max))
        exact = False
    m = 0
    for idx in draws:
        m += 1
        v = stat(idx)
        if v is None:
            undefined += 1
        elif hit(v):
            count += 1
    p = count / m if exact else (1 + count) / (1 + m)
    return {"observed": obs, "p": p, "alternative": alternative, "exact": exact, "relabellings": m,
            "distinct_relabellings": total, "count_at_least_observed": count, "undefined": undefined,
            "clusters_a": len(parts_a), "clusters_b": len(parts_b), "seed": None if exact else seed}


# scorecard differences (rows 1 to 7 of scorecard.evaluate), oriented in the humans' direction: A minus B > 0
SCORECARD_TESTS = [
    (1, "lf_minus_fine", "laissez_faire", "fine", "cartel_formation_rate"),
    (1, "fine_minus_leniency", "fine", "leniency", "cartel_formation_rate"),
    (2, "leniency_minus_fine", "leniency", "fine", "report_rate_given_cartel"),
    (3, "fine_minus_leniency", "fine", "leniency", "relapse_rate_next_period"),
    (4, "fine_minus_lf", "fine", "laissez_faire", "avg_price"),
    (4, "lf_minus_leniency_reported_only", "laissez_faire", "leniency", "avg_price"),   # humans 4.917 against 4.845
    (5, "fine_minus_lf", "fine", "laissez_faire", "cartel_price"),
    (5, "leniency_minus_lf", "leniency", "laissez_faire", "cartel_price"),
    (6, "lf_minus_fine", "laissez_faire", "fine", "deviation_rate"),
    (6, "lf_minus_leniency", "laissez_faire", "leniency", "deviation_rate"),
    (7, "fine_minus_noreport", "fine", "noreport", "cartel_price"),
]


def scorecard_permutations(runs: dict[str, dict], n_max: int = 10_000, seed: int = 0) -> list[dict]:
    out = []
    for row, name, a, b, key in SCORECARD_TESTS:
        ra, rb = runs.get(a), runs.get(b)
        res = None
        if ra is not None and rb is not None:
            res = permutation_test(cluster_parts(ra["rows"], key), cluster_parts(rb["rows"], key), "greater", n_max, seed)
        out.append({"row": row, "test": name, "a": a, "b": b, "measure": key, "permutation": res})
    return out
