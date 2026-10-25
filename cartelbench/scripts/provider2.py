"""Pilot and contamination check for the second provider, written to evidence/provider2/ instead of evidence/.

    python3 scripts/provider2.py pilot --models qwen2.5-32b-instruct --provider openai --base-url <url>/v1 --api-key-env P2_KEY
    python3 scripts/provider2.py contamination --model qwen2.5-32b-instruct --provider openai --base-url <url>/v1 --api-key-env P2_KEY

Runs the unchanged `cartelbench.pilot` and `cartelbench.contamination` (same threshold, same probes) with their
evidence directory pointed at evidence/provider2/, so the Claude pilot files are never touched.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from cartelbench import contamination, pilot  # noqa: E402
from cartelbench.util import EVIDENCE_DIR  # noqa: E402

P2_DIR = EVIDENCE_DIR / "provider2"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in {"pilot", "contamination"}:
        print(__doc__, file=sys.stderr)
        return 2
    cmd, argv = sys.argv[1], sys.argv[2:]
    sys.argv = [f"cartelbench.{cmd}", *argv]  # evidence headers name the module that ran
    module = pilot if cmd == "pilot" else contamination
    module.EVIDENCE_DIR = P2_DIR
    return module.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
