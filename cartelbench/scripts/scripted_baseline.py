"""Naive baseline: scripted players through the full pipeline, no API.

    python3 cartelbench/scripts/scripted_baseline.py

Runs collude, deviate and nash players in the four core regimes (5 duopoles, seed 1), writes the runs to
evidence/scripted/runs/ and the table of measures to evidence/scripted/baseline_table.json and .md.
The expected values are the acceptance criteria A5 and A6 of BUILD_PLAN.md.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cartelbench.engine import RunConfig, run_sync  # noqa: E402
from cartelbench.util import EVIDENCE_DIR, evidence_header, write_json  # noqa: E402

OUT = EVIDENCE_DIR / "scripted"
KEYS = ["cartel_rate", "avg_price", "cartel_price", "deviation_rate", "report_rate_pair_given_cartel",
        "n_detections", "fines_paid_total", "rewards_paid_total", "mean_points_per_agent_period", "n_pair_periods"]


def main() -> int:
    cmd = "python3 cartelbench/scripts/scripted_baseline.py"
    rows = []
    for player in ("collude", "deviate", "nash"):
        for regime in ("laissez_faire", "fine", "leniency", "reward"):
            cfg = RunConfig(regime=regime, model=f"scripted-{player}", provider="scripted", player=player, duopoles=5,
                            pool_size=10, seed=1, out_dir=str(OUT / "runs"), run_id=f"{regime}_{player}_s1")
            s = run_sync(cfg, generated_by=cmd)
            rows.append({"player": player, "regime": regime, "run_id": s["run_id"], **{k: s["metrics"][k] for k in KEYS}})
    header = evidence_header(cmd)
    write_json(OUT / "baseline_table.json", {**header, "rows": rows})
    md = [f"<!-- {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
          "# Scripted baseline (no API)", "",
          "| player | regime | cartel_rate | avg_price | cartel_price | deviation_rate | report_rate | detections | fines | rewards | points per agent-period | pair-periods |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        f = lambda v: "n/a" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))  # noqa: E731
        md.append(f"| {r['player']} | {r['regime']} | " + " | ".join(f(r[k]) for k in KEYS) + " |")
    (OUT / "baseline_table.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
