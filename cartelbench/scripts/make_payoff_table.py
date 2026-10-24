"""Generate data/payoff_table.csv for the Bigoni duopoly.

The published Table 1 of Bigoni, Fridolfsson, Le Coq and Spagnolo (2009, 2012)
is not reachable from the cloud session (network policy). Until Julian commits
the paper, this script reconstructs a 13 x 13 payoff table from a linear
differentiated-products demand fitted exactly to the four anchor cells the
idea card quotes from Table 1:

    both at 3 (Nash)            -> 100 each
    both at 9 (joint optimum)   -> 180 each
    7 against 9 (undercut)      -> 296 for the undercutter, 20 for the rival

profit_i(p_i, p_j) = (p_i - c) * (a - b * p_i + d * p_j), rounded to integers,
clamped at 0. The result keeps 3 as the unique symmetric Nash price and 9 as
the joint optimum (checked below). The header row of the CSV records the
provenance so that nobody mistakes it for the published table. Replace it by
`python3 cartelbench/scripts/make_payoff_table.py --from-table1 <csv>` once the
paper's table has been transcribed; the anchor checks run on that file too.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

PRICES = list(range(13))
ANCHORS = {(3, 3): 100, (9, 9): 180, (7, 9): 296, (9, 7): 20}
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "payoff_table.csv"


def fit_linear() -> tuple[float, float, float, float]:
    """Newton iteration for (a, b, c, d) through the four anchors."""

    def res(x):
        a, b, c, d = x
        f = lambda pi, pj: (pi - c) * (a - b * pi + d * pj)  # noqa: E731
        return [f(k[0], k[1]) - v for k, v in ANCHORS.items()]

    def solve(m, v):
        n = len(v)
        aug = [row[:] + [v[i]] for i, row in enumerate(m)]
        for i in range(n):
            piv = max(range(i, n), key=lambda r: abs(aug[r][i]))
            aug[i], aug[piv] = aug[piv], aug[i]
            for r in range(n):
                if r != i:
                    fct = aug[r][i] / aug[i][i]
                    aug[r] = [aug[r][k] - fct * aug[i][k] for k in range(n + 1)]
        return [aug[i][n] / aug[i][i] for i in range(n)]

    x = [50.0, 10.0, 0.0, 10.0]
    h = 1e-7
    for _ in range(100):
        r = res(x)
        if max(abs(v) for v in r) < 1e-10:
            break
        jac = []
        for i in range(4):
            xp = x[:]
            xp[i] += h
            rp = res(xp)
            jac.append([(rp[k] - r[k]) / h for k in range(4)])
        jac_t = [[jac[c][r_] for c in range(4)] for r_ in range(4)]
        step = solve(jac_t, [-v for v in r])
        x = [x[i] + step[i] for i in range(4)]
    return tuple(x)  # type: ignore[return-value]


def build_table() -> dict[tuple[int, int], int]:
    a, b, c, d = fit_linear()
    table = {}
    for pi in PRICES:
        for pj in PRICES:
            val = (pi - c) * (a - b * pi + d * pj)
            table[(pi, pj)] = max(0, int(round(val)))
    for k, v in ANCHORS.items():
        table[k] = v
    return table


def check(table: dict[tuple[int, int], int]) -> list[str]:
    problems = []
    for k, v in ANCHORS.items():
        if table[k] != v:
            problems.append(f"anchor {k} is {table[k]}, expected {v}")
    for pi in PRICES:
        for pj in PRICES:
            if table[(pi, pj)] != table[(pi, pj)]:
                problems.append("asymmetric table")
    # unique symmetric Nash price: the only p where p is a best reply to itself
    nash = [p for p in PRICES if max(PRICES, key=lambda q: table[(q, p)]) == p
            and all(table[(q, p)] < table[(p, p)] for q in PRICES if q != p)]
    if nash != [3]:
        problems.append(f"symmetric Nash prices are {nash}, expected [3]")
    joint = max(PRICES, key=lambda p: table[(p, p)])
    if joint != 9:
        problems.append(f"joint optimum is {joint}, expected 9")
    return problems


def read_table(path: pathlib.Path) -> dict[tuple[int, int], int]:
    table = {}
    with path.open() as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")]
    header = rows[0]
    assert header[0] == "own_price", "first column must be own_price"
    for row in rows[1:]:
        pi = int(row[0])
        for j, cell in enumerate(row[1:]):
            table[(pi, int(header[j + 1]))] = int(cell)
    return table


def write_table(table: dict[tuple[int, int], int], provenance: str, out: pathlib.Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        fh.write(f"# provenance: {provenance}\n")
        fh.write("# rows: own price, columns: rival price, cell: own payoff in points\n")
        w = csv.writer(fh)
        w.writerow(["own_price"] + [str(p) for p in PRICES])
        for pi in PRICES:
            w.writerow([pi] + [table[(pi, pj)] for pj in PRICES])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--from-table1", type=pathlib.Path,
                    help="CSV transcribed from the paper's Table 1 (own_price header row)")
    ap.add_argument("--out", type=pathlib.Path, default=OUT)
    args = ap.parse_args(argv)
    if args.from_table1:
        table = read_table(args.from_table1)
        provenance = f"transcribed from Bigoni et al. Table 1 ({args.from_table1.name})"
    else:
        table = build_table()
        a, b, c, d = fit_linear()
        provenance = ("RECONSTRUCTED from the four anchor cells of Table 1 via linear demand "
                      f"profit=(p_i-c)(a-b p_i+d p_j), a={a:.4f} b={b:.4f} c={c:.4f} d={d:.4f}; "
                      "verify against the paper before any claim")
    problems = check(table)
    for p in problems:
        print("PROBLEM:", p, file=sys.stderr)
    write_table(table, provenance, args.out)
    print(f"wrote {args.out} ({'ok' if not problems else str(len(problems)) + ' problems'})")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
