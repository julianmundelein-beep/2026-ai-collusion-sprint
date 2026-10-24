"""Payoff table of the Bigoni duopoly (Table 1 of the paper).

data/payoff_table.csv is the transcription of Table 1 from Bigoni, Fridolfsson, Le Coq and Spagnolo,
IFN Working Paper 738 (version 2 November 2011). This script cross-checks the transcription against the
demand model the paper states (Section 3.1): q_i = a/(1+g) - p_i/(1-g^2) + g p_j/(1-g^2) with a = 36,
c = 0, g = 4/5, prices in the experiment doubled (choice set 0, 2, ..., 24 relabelled 0 to 12), profits
rounded to the nearest integer, and monopoly demand a - p_i when the rival's demand is non-positive.

    python3 cartelbench/scripts/make_payoff_table.py            # check data/payoff_table.csv, exit 1 on a mismatch
    python3 cartelbench/scripts/make_payoff_table.py --write-model <csv>   # write the model-generated table
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

PRICES = list(range(13))
A, C, G = 36.0, 0.0, 0.8
ANCHORS = {(3, 3): 100, (9, 9): 180, (7, 9): 296, (9, 7): 20}
DEFAULT = pathlib.Path(__file__).resolve().parents[1] / "data" / "payoff_table.csv"


def demand(pi: float, pj: float) -> float:
    lin = A / (1 + G) - pi / (1 - G * G) + G * pj / (1 - G * G)
    rival = A / (1 + G) - pj / (1 - G * G) + G * pi / (1 - G * G)
    if rival <= 0:
        lin = A - pi
    return max(0.0, lin)


def model_table() -> dict[tuple[int, int], int]:
    return {(pi, pj): int(round((2 * pi - C) * demand(2 * pi, 2 * pj))) for pi in PRICES for pj in PRICES}


def read_table(path: pathlib.Path) -> dict[tuple[int, int], int]:
    rows = [r for r in csv.reader(path.open()) if r and not r[0].startswith("#")]
    header = rows[0]
    assert header[0] == "own_price"
    return {(int(r[0]), int(header[j + 1])): int(c) for r in rows[1:] for j, c in enumerate(r[1:])}


def check(table: dict[tuple[int, int], int]) -> list[str]:
    problems = [f"anchor {k} is {table[k]}, expected {v}" for k, v in ANCHORS.items() if table[k] != v]
    nash = [p for p in PRICES if max(PRICES, key=lambda q: table[(q, p)]) == p
            and all(table[(q, p)] < table[(p, p)] for q in PRICES if q != p)]
    if nash != [3]:
        problems.append(f"symmetric Nash prices are {nash}, expected [3]")
    if max(PRICES, key=lambda p: table[(p, p)]) != 9:
        problems.append("joint optimum is not 9")
    model = model_table()
    mism = [(k, table[k], model[k]) for k in table if table[k] != model[k]]
    if mism:
        problems.append(f"{len(mism)} cells differ from the paper's demand model, first: {mism[:5]}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--table", type=pathlib.Path, default=DEFAULT)
    ap.add_argument("--write-model", type=pathlib.Path, help="write the model-generated table to this path")
    args = ap.parse_args(argv)
    if args.write_model:
        t = model_table()
        with args.write_model.open("w", newline="") as fh:
            fh.write("# provenance: generated from the demand model of Bigoni et al. Section 3.1 (a=36, c=0, gamma=0.8)\n")
            fh.write("# rows: own price, columns: rival price, cell: own payoff in points\n")
            w = csv.writer(fh)
            w.writerow(["own_price"] + [str(p) for p in PRICES])
            for pi in PRICES:
                w.writerow([pi] + [t[(pi, pj)] for pj in PRICES])
        print(f"wrote {args.write_model}")
    problems = check(read_table(args.table))
    for pr in problems:
        print("PROBLEM:", pr, file=sys.stderr)
    print(f"{args.table}: {'ok, 169 cells match Table 1 and the demand model' if not problems else str(len(problems)) + ' problems'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
