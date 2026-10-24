"""Stage game: prices 0 to 12 and the payoff table (Table 1 of the paper)."""
from __future__ import annotations

import csv
import pathlib
from dataclasses import dataclass

PRICES = tuple(range(13))
NASH_PRICE = 3
JOINT_OPTIMUM_PRICE = 9
DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"
DEFAULT_TABLE = DATA_DIR / "payoff_table.csv"


@dataclass(frozen=True)
class PayoffTable:
    cells: dict[tuple[int, int], int]
    provenance: str
    scale: float = 1.0

    def payoff(self, own: int, rival: int) -> int:
        """Own points for own price against the rival's price."""
        if own not in PRICES or rival not in PRICES:
            raise ValueError(f"price out of range: {own}, {rival}")
        return int(round(self.cells[(own, rival)] * self.scale))

    def best_reply(self, rival: int) -> int:
        return max(PRICES, key=lambda p: (self.payoff(p, rival), -p))

    def scaled(self, factor: float) -> "PayoffTable":
        return PayoffTable(self.cells, self.provenance + f"; scaled by {factor}", factor)

    def as_rows(self) -> list[list[int]]:
        return [[self.payoff(pi, pj) for pj in PRICES] for pi in PRICES]


def load_payoff_table(path: pathlib.Path | str = DEFAULT_TABLE) -> PayoffTable:
    path = pathlib.Path(path)
    provenance = "unknown"
    rows = []
    with path.open() as fh:
        for line in fh:
            if line.startswith("# provenance:"):
                provenance = line.split(":", 1)[1].strip()
            if line.startswith("#"):
                continue
            rows.append(line.rstrip("\n"))
    reader = list(csv.reader(rows))
    header = reader[0]
    if header[0] != "own_price":
        raise ValueError("payoff table must start with an own_price header row")
    cells = {}
    for row in reader[1:]:
        own = int(row[0])
        for j, cell in enumerate(row[1:]):
            cells[(own, int(header[j + 1]))] = int(cell)
    if len(cells) != len(PRICES) ** 2:
        raise ValueError(f"payoff table has {len(cells)} cells, expected {len(PRICES) ** 2}")
    return PayoffTable(cells, provenance)
