#!/usr/bin/env python3
"""Set the PDF metadata title and author of paper/report.pdf from paper/report.md (Pages writes the file name).

    python3 paper/set_pdf_title.py [--pdf paper/report.pdf] [--md paper/report.md]

Needs pypdf. Rewrites the PDF in place; page content and text layer are copied unchanged.
"""
import argparse
import pathlib
import re

from pypdf import PdfReader, PdfWriter


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", type=pathlib.Path, default=root / "paper/report.pdf")
    ap.add_argument("--md", type=pathlib.Path, default=root / "paper/report.md")
    args = ap.parse_args()
    md = args.md.read_text(encoding="utf8")
    title = re.search(r"^# (.+)$", md, re.M).group(1).strip()
    author = re.search(r"^AUTHOR: (.+)$", md, re.M).group(1).strip()
    writer = PdfWriter(clone_from=PdfReader(str(args.pdf)))
    writer.add_metadata({"/Title": title, "/Author": author})
    tmp = args.pdf.with_suffix(".tmp.pdf")
    with open(tmp, "wb") as f:
        writer.write(f)
    tmp.replace(args.pdf)
    print(f"title set: {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
