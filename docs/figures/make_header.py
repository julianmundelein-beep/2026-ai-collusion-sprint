"""Builds the README header banner (docs/figures/header.svg) in the typeface of the report.

    python3 docs/figures/make_header.py [--out docs/figures/header.svg] [--dark-out docs/figures/header_dark.svg]

The report's template embeds Old Standard TT (SIL Open Font License 1.1) in paper/report.docx. This script takes
the regular, bold and italic faces from there, subsets each to the characters the banner uses (fontTools) and
inlines them as data URIs, so the SVG renders in the same face on GitHub without loading anything external.
"""
from __future__ import annotations

import argparse
import base64
import io
import pathlib
import zipfile

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCX = ROOT / "paper/report.docx"

TITLE = "CartelBench"
SUBTITLE = ["Same Game, Different Players: A Human-Calibrated Testbed", "for Cartel Enforcement on LLM Pricing Agents"]
AUTHOR = "Julian Mündelein"
AFFILIATION = "Independent, Hong Kong"
SPRINT = "Submitted to the AI Collusion Research Sprint, Apart Research, October 2026"
INK, RULE, PAPER = "#111111", "#111111", "#fcfcfb"
DARK_INK = "#e6edf3"  # GitHub's dark-mode foreground; the dark variant has no background of its own


def face(name: str, text: str) -> str:
    """Subset one embedded face to `text` and return it as a base64 WOFF data URI."""
    with zipfile.ZipFile(DOCX) as z:
        raw = z.read(f"word/fonts/OldStandardTT-{name}.ttf")
    font = TTFont(io.BytesIO(raw))
    opts = subset.Options()
    opts.flavor = "woff"
    opts.desubroutinize = True
    opts.name_IDs = [0, 1, 2, 13, 14]  # copyright, family, style, licence text and URL stay in the subset
    s = subset.Subsetter(opts)
    s.populate(text=text)
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff"
    font.save(buf)
    return "data:font/woff;base64," + base64.b64encode(buf.getvalue()).decode()


def build(dark: bool = False) -> str:
    ink = rule = DARK_INK if dark else INK
    paper = "none" if dark else PAPER
    bold_text = TITLE + "".join(SUBTITLE) + AUTHOR
    regular_text = AFFILIATION
    italic_text = SPRINT
    fonts = {"bold": face("bold", bold_text), "regular": face("regular", regular_text), "italic": face("italic", italic_text)}
    w, h = 1200, 400
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="t d">',
        f"<title id=\"t\">{TITLE}: {' '.join(SUBTITLE)}</title>",
        f'<desc id="d">{AUTHOR}, {AFFILIATION}. {SPRINT}.</desc>',
        "<!-- Typeface: Old Standard TT, Copyright 2011 The Old Standard Project Authors, SIL Open Font License 1.1 "
        "(http://scripts.sil.org/OFL); subsets embedded from the report template by docs/figures/make_header.py. -->",
        "<defs><style>",
        f"@font-face{{font-family:'OSB';src:url({fonts['bold']}) format('woff');font-weight:bold}}",
        f"@font-face{{font-family:'OSR';src:url({fonts['regular']}) format('woff')}}",
        f"@font-face{{font-family:'OSI';src:url({fonts['italic']}) format('woff');font-style:italic}}",
        f".b{{font-family:'OSB','Old Standard TT',Georgia,serif;font-weight:bold;fill:{ink}}}",
        f".r{{font-family:'OSR','Old Standard TT',Georgia,serif;fill:{ink}}}",
        f".i{{font-family:'OSI','Old Standard TT',Georgia,serif;font-style:italic;fill:{ink}}}",
        "</style></defs>",
        f'<rect width="{w}" height="{h}" rx="6" fill="{paper}"/>',
        f'<rect x="80" y="40" width="{w - 160}" height="5" fill="{rule}"/>',
        f'<text class="b" x="{w / 2}" y="128" font-size="72" text-anchor="middle">{TITLE}</text>',
        f'<text class="b" x="{w / 2}" y="186" font-size="30" text-anchor="middle">{SUBTITLE[0]}</text>',
        f'<text class="b" x="{w / 2}" y="224" font-size="30" text-anchor="middle">{SUBTITLE[1]}</text>',
        f'<rect x="80" y="252" width="{w - 160}" height="1.5" fill="{rule}"/>',
        f'<text class="b" x="{w / 2}" y="300" font-size="26" text-anchor="middle">{AUTHOR}</text>',
        f'<text class="r" x="{w / 2}" y="332" font-size="23" text-anchor="middle">{AFFILIATION}</text>',
        f'<text class="i" x="{w / 2}" y="372" font-size="21" text-anchor="middle">{SPRINT}</text>',
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "docs/figures/header.svg")
    ap.add_argument("--dark-out", type=pathlib.Path, default=ROOT / "docs/figures/header_dark.svg",
                    help="the dark-mode variant: light ink on a transparent background")
    args = ap.parse_args()
    for out, dark in ((args.out, False), (args.dark_out, True)):
        out.write_text(build(dark), encoding="utf-8")
        print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
