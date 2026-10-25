#!/usr/bin/env python3
"""YouTube thumbnail for the CartelBench video, drawn with the helpers of build.py.

    python3 video/thumbnail.py    # writes video/thumbnail.png (1280x720)

Left: title and question in the video's type; right: the central finding as a
small chart, the Sonnet prices of round7/diagonal.json on the line price = threshold.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

OUT = build.VIDEO_DIR / "thumbnail.png"


def main() -> None:
    E = build.evidence_numbers()
    c = build.new_canvas()  # 1920x1080, scaled to 1280x720 at the end
    W, H = build.W, build.H
    # left column
    build.paste(c, build.text_block("CartelBench", 52, build.ACCENT, "semibold"), (120, 150), rise=0)
    build.paste(c, build.text_block("Same Game,\nDifferent Players", 120, build.INK, "bold", max_width=1160, spacing=1.05), (120, 230), rise=0)
    build.paste(c, build.text_block("Do antitrust tools built for people\nwork on AI pricing agents?", 54, build.MUTED, max_width=1100, spacing=1.25),
                (120, 560), rise=0)
    build.paste(c, build.text_block("AI Collusion Research Sprint, Apart Research 2026", 36, build.MUTED), (120, 940), rise=0)
    # right: the line
    cx0, cx1, cy0, cy1 = 1300, 1800, 900, 300
    pts = sorted(E["diagonal"]["Sonnet 5.5"])

    def X(p):
        return cx0 + (cx1 - cx0) * (p - 2.5) / 4.5

    def Y(v):
        return cy0 + (cy1 - cy0) * (v - 2.5) / 4.5

    build.rounded(c, (cx0 - 90, cy1 - 90, cx1 + 60, cy0 + 150), (255, 255, 255, 255), 36, outline=build.RULE, width=3)
    build.line(c, (cx0, cy0), (cx1, cy0), build.INK, 5)
    build.line(c, (cx0, cy0), (cx0, cy1), build.INK, 5)
    build.dashed(c, (X(2.7), Y(2.7)), (X(6.8), Y(6.8)), build.HUMAN, 5, dash=22)
    for i in range(len(pts) - 1):
        build.line(c, (X(pts[i][0]), Y(pts[i][1])), (X(pts[i + 1][0]), Y(pts[i + 1][1])), build.ACCENT, 8)
    for p, v, share, modal in pts:
        build.circle(c, (X(p), Y(v)), 22, fill=build.ACCENT)
    build.paste(c, build.text_block("announced threshold", 34, build.MUTED), ((cx0 + cx1) // 2, cy0 + 30), rise=0, anchor="mt")
    build.paste(c, build.text_block("price", 34, build.MUTED), (cx0 - 20, cy1 - 10), rise=0, anchor="rb")
    build.paste(c, build.text_block("the threshold becomes the price", 38, build.ACCENT, "semibold", align="center"),
                ((cx0 + cx1) // 2 - 15, cy0 + 98), rise=0, anchor="mt")
    img = c.convert("RGB").resize((1280, 720), Image.LANCZOS)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
