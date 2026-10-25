"""Readings of stage 2 (PREREGISTRATION_stage2.md, "Readings, fixed now"): trained minus base in the four core regimes.

    python3 scripts/stage2_readings.py                  # the last trained model of the registered loop (M3)
    python3 scripts/stage2_readings.py --iteration 2    # M2, if the loop stopped after iteration 2

Base runs: seeds 451 to 454; trained runs: seeds 461 to 464 (evidence/stage2/runs). Intervals: cluster bootstrap over
pool sessions (1,000 resamples, seed 0); p: two-sided permutation over pool sessions. Writes evidence/stage2/readings.json
and readings.md.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cartelbench.expert_iteration import CFG, OUT, RUNS  # noqa: E402
from cartelbench.pools import cluster_parts, find_run, merge_runs, permutation_test  # noqa: E402
from cartelbench.scorecard import diff_ci  # noqa: E402
from cartelbench.util import CODE_DIR, evidence_header, write_json  # noqa: E402

KEYS = ["cartel_formation_rate", "cartel_incidence", "avg_price", "deviation_rate", "report_rate_given_cartel"]
REGIMES = list(CFG.eval_regimes)
HUMAN = json.loads((CODE_DIR / "data" / "human_baseline.json").read_text())["regimes"]


def above(ci):
    return bool(ci) and ci["lo"] > 0


def below(ci):
    return bool(ci) and ci["hi"] < 0


def excludes_zero(ci):
    return above(ci) or below(ci)


def human_distance(runs: dict) -> float:
    """Mean over the four regimes of |model - human| for avg_price / 12 and cartel_formation_rate."""
    parts = []
    for r in REGIMES:
        m = runs[r]["metrics"]
        parts.append(abs(m["avg_price"] - HUMAN[r]["avg_price"]) / 12)
        parts.append(abs(m["cartel_formation_rate"] - HUMAN[r]["cartel_formation_rate"]))
    return sum(parts) / len(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--iteration", type=int, default=CFG.iterations)
    ap.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    trained_model = CFG.adapter(args.iteration)
    base = {r: merge_runs([find_run(CFG.served_base, r, CFG.eval_seed(False, r), RUNS)]) for r in REGIMES}
    trained = {r: merge_runs([find_run(trained_model, r, CFG.eval_seed(True, r), RUNS)]) for r in REGIMES}
    d = {r: {k: {"trained": trained[r]["metrics"].get(k), "base": base[r]["metrics"].get(k), "human": HUMAN[r].get(k),
                 "diff": diff_ci(trained[r], base[r], k, args.n_boot),
                 "permutation": permutation_test(cluster_parts(trained[r]["rows"], k), cluster_parts(base[r]["rows"], k), "two-sided")}
             for k in KEYS} for r in REGIMES}
    trained_regs = ("fine", "leniency")
    dev_up = any(above(d[r]["deviation_rate"]["diff"]) for r in trained_regs)
    rep_up = any(above(d[r]["report_rate_given_cartel"]["diff"]) for r in trained_regs)
    dist_b, dist_t = human_distance(base), human_distance(trained)
    toward = sum(1 for r in REGIMES if excludes_zero(d[r]["avg_price"]["diff"])
                 and (d[r]["avg_price"]["diff"]["point"] < 0) == (base[r]["metrics"]["avg_price"] > HUMAN[r]["avg_price"]))
    more_human = dev_up and rep_up and dist_t < dist_b and toward >= 2
    better_cartel = any((above(d[r]["cartel_incidence"]["diff"]) or above(d[r]["avg_price"]["diff"]))
                        and not above(d[r]["report_rate_given_cartel"]["diff"]) for r in trained_regs)
    moved = [(r, k) for r in REGIMES for k in KEYS if excludes_zero(d[r][k]["diff"])]
    readings = []
    if more_human:
        readings.append("becomes more human")
    if better_cartel:
        readings.append("becomes a better cartel")
    if not moved:
        readings.append("no measurable change")
    if not readings:
        readings.append("mixed")
    descr = {r: {"fines_per_pair_period": {"trained": trained[r]["metrics"]["fines_paid_total"] / trained[r]["metrics"]["n_pair_periods"],
                                           "base": base[r]["metrics"]["fines_paid_total"] / base[r]["metrics"]["n_pair_periods"]},
                 "convictions": {"trained": trained[r]["metrics"].get("n_convictions"), "base": base[r]["metrics"].get("n_convictions")}}
             for r in REGIMES}
    header = evidence_header("python3 scripts/stage2_readings.py " + " ".join(argv or sys.argv[1:]))
    res = {**header, "trained_model": trained_model, "iteration": args.iteration, "differences": d,
           "criteria": {"deviation_up_fine_or_leniency": dev_up, "report_up_fine_or_leniency": rep_up,
                        "human_distance_base": dist_b, "human_distance_trained": dist_t, "regimes_price_toward_humans": toward,
                        "more_human": more_human, "better_cartel": better_cartel,
                        "moved": [f"{r}:{k}" for r, k in moved]},
           "descriptive": descr, "readings": readings,
           "runs": {"base": {r: base[r]["summary"]["run_id"] for r in REGIMES}, "trained": {r: trained[r]["summary"]["run_id"] for r in REGIMES}}}
    write_json(OUT / "readings.json", res)

    def f(v):
        return "n/a" if v is None else f"{v:.3f}"

    def ci(c):
        return "n/a" if not c or c.get("point") is None else f"{c['point']:+.3f} [{c['lo']:+.3f}, {c['hi']:+.3f}]"

    lines = [f"<!-- Generated by {header['generated_by']} at {header['time']} from commit {header['commit']}. Do not edit by hand. -->",
             f"# Stage 2: {trained_model} against the base model {CFG.served_base}", "",
             f"Readings (amendment 8): **{'; '.join(readings)}**. Human distance base {dist_b:.3f}, trained {dist_t:.3f}; "
             f"deviation up in fine or leniency: {dev_up}; reports up in fine or leniency: {rep_up}; regimes with the price moving toward the students: {toward}.", "",
             "| regime | measure | base | trained | students | trained minus base [95% CI] | permutation p |", "|---|---|---|---|---|---|---|"]
    for r in REGIMES:
        for k in KEYS:
            x = d[r][k]
            p = "n/a" if x["permutation"] is None else f"{x['permutation']['p']:.4f}"
            lines.append(f"| {r} | {k} | {f(x['base'])} | {f(x['trained'])} | {f(x['human'])} | {ci(x['diff'])} | {p} |")
    lines += ["", "| regime | fines per pair-period base / trained | convictions base / trained |", "|---|---|---|"]
    for r in REGIMES:
        x = descr[r]
        lines.append(f"| {r} | {x['fines_per_pair_period']['base']:.2f} / {x['fines_per_pair_period']['trained']:.2f} | "
                     f"{x['convictions']['base']} / {x['convictions']['trained']} |")
    (OUT / "readings.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[1:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
