"""Small helpers: commit hash, timestamps, evidence headers."""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CODE_DIR = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = CODE_DIR / "evidence"


def git_commit() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        # dirty = uncommitted code or data; files written under evidence/ by runs and analyses do not count
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "cartelbench", ":!cartelbench/evidence"], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001
        return "unknown"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def command_line() -> str:
    return "python3 -m " + " ".join([sys.argv[0].rsplit("/", 1)[-1].replace(".py", "")] + sys.argv[1:]) \
        if sys.argv[0].endswith(".py") else "python3 " + " ".join(sys.argv)


def evidence_header(generated_by: str, commit: str | None = None) -> dict:
    return {"header": True, "generated_by": generated_by, "commit": commit or git_commit(), "time": now_iso(),
            "note": "Do not edit by hand."}


def write_json(path: pathlib.Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=False, default=str) + "\n")


def read_jsonl(path: pathlib.Path) -> list[dict]:
    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
