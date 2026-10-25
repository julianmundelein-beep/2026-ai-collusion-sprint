"""Checks that every relative link and image in the Markdown files of the repository points at an existing file
(Markdown links and images, and src or href attributes of inline HTML).

    python3 cartelbench/scripts/check_links.py [--root <repository root>]

Links with a scheme (https:, mailto:) and pure anchors (#section) are not checked. Exits 1 when a link is broken.
Evidence folders are skipped: their generated Markdown names files by convention, not by link.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|(?:src|href)=\"([^\"]+)\"")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
SKIP_PREFIXES = ("cartelbench/evidence/",)


def markdown_files(root: pathlib.Path):
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in p.parts) or rel.startswith(SKIP_PREFIXES):
            continue
        yield p


def check(root: pathlib.Path) -> list[str]:
    broken = []
    for md in markdown_files(root):
        text = md.read_text(encoding="utf-8")
        in_code = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for md_target, html_target in LINK.findall(line):
                target = md_target or html_target
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                if path.startswith("/"):
                    broken.append(f"{md.relative_to(root)}:{n}: absolute path {target}")
                    continue
                if not (md.parent / path).exists():
                    broken.append(f"{md.relative_to(root)}:{n}: missing {target}")
    return broken


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[2])
    args = ap.parse_args()
    broken = check(args.root)
    files = sum(1 for _ in markdown_files(args.root))
    for b in broken:
        print(b)
    print(f"{files} Markdown files checked, {len(broken)} broken links")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
