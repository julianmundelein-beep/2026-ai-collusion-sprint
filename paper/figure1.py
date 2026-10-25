#!/usr/bin/env python3
"""Figure 1 of the report in landscape: the scorecard per Bigoni result, humans against the LLM, 2 by 4 panels.

    python3 paper/figure1.py --scorecard <scorecard.json> --bootstrap <analyze_core_bootstrap.txt>
                             [--out paper/figures/figure1_landscape.png]

Inputs are the measurement files of F19 in the backend branch (`cartelbench/evidence/scorecard/`): scorecard.json
(rows per result with human and LLM values and the tested regime differences with intervals) and
analyze_core_bootstrap.txt (per-regime 95 percent cluster-bootstrap intervals over pool sessions). Panels of results
that were not tested carry no data. No title inside the image; the caption lives in the report.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

LABEL = {"laissez_faire": "LF", "fine": "Fi", "leniency": "Le", "reward": "Re",
         "noreport": "NoRep", "rematch": "ReMatch"}
SHORT = {1: "Deterrence", 2: "Detection by reports", 3: "Recidivism", 4: "Average prices", 5: "Cartel prices",
         6: "Price deviations", 7: "Reports as punishment", 8: "Altruistic reports"}
YLABEL = {"cartel_formation_rate": "formation rate", "report_rate_given_cartel": "report rate",
          "relapse_rate_next_period": "relapse rate", "avg_price": "average price",
          "cartel_price": "cartel price", "deviation_rate": "deviation rate",
          "public_report_rate_given_only_rival_deviated": "public reports"}
TEST_LABEL = {"lf_minus_fine": "LF-Fine", "fine_minus_leniency": "Fine-Len.", "fine_minus_noreport": "Fine-NoRep.",
              "leniency_minus_fine": "Len.-Fine", "fine_minus_lf": "Fine-LF",
              "leniency_minus_lf": "Len.-LF", "lf_minus_leniency": "LF-Len."}
HUMAN = "#6b6a66"
LLM = "#2a78d6"
GREEN, RED, GREY = "#1b7f3b", "#b3261e", "#8a8984"


def read_bootstrap(path: pathlib.Path, runs: dict[str, str]) -> dict[str, dict[str, tuple[float, float]]]:
    """Per-regime intervals, taken from the run that the scorecard picked for that regime."""
    by_run: dict[str, dict[str, tuple[float, float]]] = {}
    run_id = None
    for line in path.read_text().splitlines():
        m = re.match(r"== (\S+) \(", line)
        if m:
            run_id = m.group(1)
            by_run[run_id] = {}
            continue
        m = re.match(r"\s+(\w+)\s+([\d.]+)\s+\[([\d.]+), ([\d.]+)\]", line)
        if m and run_id:
            by_run[run_id][m.group(1)] = (float(m.group(3)), float(m.group(4)))
    return {regime: by_run.get(rid, {}) for regime, rid in runs.items()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scorecard", type=pathlib.Path, required=True)
    ap.add_argument("--bootstrap", type=pathlib.Path, default=None)
    ap.add_argument("--pools", default="8")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("paper/figures/figure1_landscape.png"))
    args = ap.parse_args(argv)
    sc = json.loads(args.scorecard.read_text())
    ci = read_bootstrap(args.bootstrap, sc.get("runs", {})) if args.bootstrap else {}
    perm = {(t["row"], t["test"]): t["permutation"]["p"] for t in sc.get("permutation_tests", []) if t.get("permutation")}
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8})
    fig, axes = plt.subplots(2, 4, figsize=(6.5, 3.0))
    for ax, row in zip(axes.flat, sc["rows"]):
        state = row.get("replicated")
        verdict, color = ("reproduced", GREEN) if state else (("not testable", GREY) if state is None else ("not reproduced", RED))
        ax.set_title(f"{row['n']}. {SHORT[row['n']]}\n{verdict}", loc="left", color=color, fontsize=8)
        key = row["measure"]
        if state is not None:
            ax.set_ylabel(YLABEL.get(key, key), fontsize=8)
        regimes = [r for r in row["human"] if r in LABEL]
        if state is None:
            ax.set_xticks([]); ax.set_yticks([])
            for side in ax.spines.values():
                side.set_color("#d9d8d2")
            ax.text(0.5, 0.5, "no cartel\nin ReMatch:\nno public\nreport occurs", ha="center", va="center",
                    fontsize=8, color=GREY, transform=ax.transAxes)
            continue
        xs = list(range(len(regimes)))
        for x, r in zip(xs, regimes):
            h = row["human"].get(r)
            v = row["llm"].get(r)
            if h is not None:
                ax.plot([x - 0.14], [h], marker="o", ms=5.5, mfc="white", mec=HUMAN, mew=1.2, ls="none", zorder=3)
            if v is not None:
                lo, hi = ci.get(r, {}).get(key, (None, None))
                if lo is not None:
                    ax.plot([x + 0.14, x + 0.14], [lo, hi], color=LLM, lw=1.4, solid_capstyle="round", zorder=2)
                ax.plot([x + 0.14], [v], marker="s", ms=5, color=LLM, ls="none", zorder=4)
        ax.set_xticks(xs)
        ax.set_xticklabels([LABEL[r] for r in regimes], fontsize=8)
        ax.set_xlim(-0.6, len(regimes) - 0.4)
        ax.grid(axis="y", color="#e6e5df", lw=0.6)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis="y", labelsize=8)
        if key in ("avg_price", "cartel_price"):
            ax.set_ylim(2.5, 9.6)
        else:
            ax.set_ylim(-0.04, 1.06)
        # the tested regime difference with its interval
        lines = []
        for tkey, t in (row.get("tests") or {}).items():
            if t and t.get("point") is not None and "reported_only" not in tkey:
                pv = perm.get((row["n"], tkey))
                ptxt = f", p {pv:.3f}" if pv is not None else ""
                lines.append(f"{TEST_LABEL.get(tkey, tkey)}: {t['point']:+.3f} [{t['lo']:+.3f}, {t['hi']:+.3f}]{ptxt}")
        # differences, intervals and permutation p are reported in the scorecard table of the report
    handles = [plt.Line2D([], [], marker="o", ms=5.5, mfc="white", mec=HUMAN, mew=1.2, ls="none", label="Humans (Bigoni et al.), pooled"),
               plt.Line2D([], [], marker="s", ms=5, color=LLM, ls="none", label=f"Claude Haiku 5.5, {args.pools} pool sessions per core regime")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(h_pad=1.2, w_pad=1.0, rect=(0, 0.07, 1, 1))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=300)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
