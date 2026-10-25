"""Round 7 analyses for the open models only (PREREGISTRATION_round7.md section (c), PREREGISTRATION_provider2.md amendment 3).

    python3 scripts/provider2_round7.py      # curve, random threshold and diagonal-figure data for Qwen and Llama

Runs the unchanged `cartelbench.round7_analysis` (curve, slope, readings, random-threshold comparisons, diagonal
figure) restricted to Qwen2.5-32B and Llama-3.1-8B, with every output in evidence/provider2/round7/ instead of
evidence/round7/; the calibration (false-positive rates, risk-neutral benchmark) is read from evidence/round7/.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cartelbench import round7_analysis as ra  # noqa: E402
from cartelbench.util import EVIDENCE_DIR  # noqa: E402

Q, L = "qwen2.5-32b-instruct", "llama-3.1-8b-instruct"
R7 = EVIDENCE_DIR / "round7"


class _Out(type(pathlib.Path())):
    """evidence/provider2/round7, except that the shared calibration file is read from evidence/round7."""

    def __truediv__(self, key):
        return R7 / key if key == "calibration.json" else pathlib.Path(super().__truediv__(key))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n-boot", type=int, default=ra.N_BOOT)
    args = ap.parse_args(argv)
    out = _Out(EVIDENCE_DIR / "provider2" / "round7")
    pathlib.Path(out).mkdir(parents=True, exist_ok=True)
    ra.OUT, ra.MODELS, ra.FIG_MODELS = out, [Q, L], [Q, L]
    for cmd in (ra.cmd_curve, ra.cmd_random, ra.cmd_figure):
        cmd(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
