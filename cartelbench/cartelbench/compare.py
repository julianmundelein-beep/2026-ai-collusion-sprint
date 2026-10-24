"""Difference of two runs with a cluster-bootstrap interval (clusters: pool sessions, resampled in each run).

    python3 -m cartelbench.compare <run_a> <run_b> [--keys cartel_incidence,avg_price] [--margins cartel_incidence=0.15,avg_price=1.0]

Used for the shifted-grid equivalence test (PREREGISTRATION.md, contamination (b): the interval of shifted minus
unshifted must lie within the margin) and for the placebo arm (placebo minus laissez-faire, placebo minus fine).
Writes <run_a>/compare_<run_b name>.json and prints one line per measure.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .scorecard import diff_ci, load_run
from .util import evidence_header, write_json

DEFAULT_KEYS = ["cartel_incidence", "cartel_formation_rate", "comm_attempt_rate", "avg_price", "cartel_price",
                "agreed_price", "deviation_rate", "report_rate_given_cartel", "late_avg_price"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_a")
    ap.add_argument("run_b")
    ap.add_argument("--keys", default=",".join(DEFAULT_KEYS))
    ap.add_argument("--margins", default="", help="equivalence margins per key, e.g. cartel_incidence=0.15,avg_price=1.0")
    ap.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    a, b = pathlib.Path(args.run_a), pathlib.Path(args.run_b)
    ra, rb = load_run(a), load_run(b)
    margins = {}
    for item in [x for x in args.margins.split(",") if x.strip()]:
        k, v = item.split("=")
        margins[k.strip()] = float(v)
    out = {**evidence_header("python3 -m cartelbench.compare " + " ".join(sys.argv[1:])),
           "run_a": a.name, "run_b": b.name, "model_a": ra["summary"].get("model"), "model_b": rb["summary"].get("model"),
           "clusters_a": ra["summary"]["n_table"].get("pool_sessions"), "clusters_b": rb["summary"]["n_table"].get("pool_sessions"),
           "differences": {}}
    print(f"{a.name} minus {b.name}")
    for k in [x.strip() for x in args.keys.split(",") if x.strip()]:
        ci = diff_ci(ra, rb, k, n_boot=args.n_boot)
        rec = {"a": ra["metrics"].get(k), "b": rb["metrics"].get(k), "diff": None if ci is None else ci}
        if ci is not None and k in margins:
            rec["margin"] = margins[k]
            rec["equivalent"] = (ci["lo"] >= -margins[k]) and (ci["hi"] <= margins[k])
        out["differences"][k] = rec
        if ci is None:
            print(f"  {k:40s} n/a")
        else:
            tag = ""
            if "equivalent" in rec:
                tag = f"  margin ±{rec['margin']}: {'equivalent' if rec['equivalent'] else 'NOT equivalent'}"
            print(f"  {k:40s} {rec['a']!s:>8} - {rec['b']!s:>8} = {ci['point']:+.3f}  [{ci['lo']:+.3f}, {ci['hi']:+.3f}]{tag}")
    path = a / f"compare_{b.name}.json"
    write_json(path, out)
    print(f"evidence: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
