#!/usr/bin/env python3
"""Build the CartelBench explainer video from the repository.

Every frame is drawn with Pillow; the figure in scene 8 is paper/figures/
figure1_landscape.png; every number comes from hackathon/FACTS.md (ids in
video/facts_used.md) and is read, where a machine-readable file exists, from
cartelbench/evidence/. The frames are piped into the ffmpeg binary shipped by
the PyPI package imageio-ffmpeg.

    pip install pillow imageio-ffmpeg
    python3 video/build.py                 # writes video/out/<name>.mp4 and video/stills/
    python3 video/build.py --stills-only   # only the three PNG stills
    python3 video/build.py --timeline      # print scene start and end times

Output: 1920x1080, 30 fps, H.264, no audio.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "video" / "out"
STILLS_DIR = ROOT / "video" / "stills"
OUT_NAME = "CartelBench_AI-Collusion-Research-Sprint_2026.mp4"
FIGURE = ROOT / "paper" / "figures" / "figure1_landscape.png"
EVIDENCE = ROOT / "cartelbench" / "evidence"

W, H = 1920, 1080
FPS = 30
XFADE = 0.8  # seconds of cross-fade between scenes

# Palette: one accent colour, warm paper background, near-black text.
BG = (250, 248, 244)
INK = (23, 32, 42)
MUTED = (107, 114, 128)
ACCENT = (46, 111, 214)
ACCENT_SOFT = (219, 230, 248)
RULE = (214, 211, 204)
HUMAN = (120, 120, 120)

# ----------------------------------------------------------------------------
# Numbers read from the evidence files (every one also listed in FACTS.md)
# ----------------------------------------------------------------------------


def load_json(path: Path) -> dict:
    with open(path) as fh:
        return json.load(fh)


def evidence_numbers() -> dict:
    """Read the numbers that exist as machine-readable evidence."""
    haiku = load_json(EVIDENCE / "round4" / "scorecard_haiku_8pool" / "scorecard.json")
    sonnet = load_json(EVIDENCE / "round4" / "scorecard_sonnet_4pool" / "scorecard.json")
    qwen = load_json(EVIDENCE / "provider2" / "scorecard" / "scorecard.json")
    llama = load_json(EVIDENCE / "provider2" / "scorecard_llama-3.1-8b-instruct" / "scorecard.json")
    screen = load_json(EVIDENCE / "round4" / "screen.json")
    human = load_json(ROOT / "cartelbench" / "data" / "human_baseline.json")

    def row(card: dict, measure: str) -> dict:
        for r in card["rows"]:
            if r["measure"] == measure:
                return r
        raise KeyError(measure)

    def prices(card: dict) -> dict:
        return row(card, "avg_price")["llm"]

    def incidence(card: dict) -> dict:
        return {k: card["metrics"][k]["cartel_incidence"] for k in REGIMES}

    arms = {a["label"]: a["differences"]["avg_price"] for a in screen["arms"]}
    return {
        "human_price": {k: human["regimes"][k]["avg_price"] for k in REGIMES},
        "human_incidence": {k: human["regimes"][k]["cartel_incidence"] for k in REGIMES},
        "price": {
            "haiku": prices(haiku),
            "sonnet": prices(sonnet),
            "qwen": prices(qwen),
            "llama": prices(llama),
        },
        "incidence": {
            "haiku": incidence(haiku),
            "sonnet": incidence(sonnet),
            "qwen": incidence(qwen),
            "llama": incidence(llama),
        },
        "scorecard": (haiku["reproduced"], haiku["tested"]),
        "screen": {
            "sonnet_nocomm": (arms["Sonnet 5.5, no channel"]["no_screen"], arms["Sonnet 5.5, no channel"]["screen"]),
            "haiku_nocomm": (arms["Haiku 5.5, no channel"]["no_screen"], arms["Haiku 5.5, no channel"]["screen"]),
            "haiku_fine": (arms["Haiku 5.5, fine regime"]["no_screen"], arms["Haiku 5.5, fine regime"]["screen"]),
        },
        "screen_fp": screen["false_positive_rate_max"],
    }


REGIMES = ["laissez_faire", "fine", "leniency", "reward"]
REGIME_LABEL = {"laissez_faire": "No authority", "fine": "Fine", "leniency": "Leniency", "reward": "Reward"}

# Numbers that exist only in FACTS.md and the report (no JSON in the tree).
# Each id is listed in video/facts_used.md.
F = {
    "deviation_haiku_lf": 0.015,   # F13
    "deviation_human_lf": 0.564,   # F15
    "payoff_cells": "169 of 169",  # F08
    "calls_total": "45,286",       # F40
    "refusals": 0,                 # F40
    "sonnet_no_channel_prices_at_4": 1.000,  # F53: every price exactly at 4
    "haiku_fine_screen_incidence": (0.401, 0.008),  # F53
}

# ----------------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------------

FONT_DIRS = [
    Path(os.environ.get("VIDEO_FONT_DIR", "")),
    Path("/usr/share/fonts/opentype/inter"),
    Path("/usr/share/fonts/truetype/inter"),
    Path.home() / "Library" / "Fonts",
    Path("/Library/Fonts"),
    Path("/usr/share/fonts/truetype/dejavu"),
]
FONT_FILES = {
    "regular": ["Inter-Regular.otf", "Inter-Regular.ttf", "DejaVuSans.ttf"],
    "semibold": ["Inter-SemiBold.otf", "Inter-SemiBold.ttf", "DejaVuSans-Bold.ttf"],
    "bold": ["InterDisplay-Bold.otf", "Inter-Bold.otf", "Inter-Bold.ttf", "DejaVuSans-Bold.ttf"],
}
_font_cache: dict = {}
_WORDS: set | None = None  # when a set, text_block records every string drawn


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    key = (size, weight)
    if key in _font_cache:
        return _font_cache[key]
    for name in FONT_FILES[weight]:
        for d in FONT_DIRS:
            p = d / name
            if p.is_file():
                f = ImageFont.truetype(str(p), size)
                _font_cache[key] = f
                return f
    f = ImageFont.load_default(size)
    _font_cache[key] = f
    return f


# ----------------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------------


def ease(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def fade(t: float, t0: float, dur: float = 0.6) -> float:
    return ease((t - t0) / dur)


def wrap(text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            cand = (cur + " " + w).strip()
            if fnt.getlength(cand) <= max_width or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(
    text: str,
    size: int,
    color=INK,
    weight: str = "regular",
    max_width: int = W - 240,
    align: str = "left",
    spacing: float = 1.3,
) -> Image.Image:
    """Render wrapped text onto a transparent layer sized to its content."""
    if _WORDS is not None:
        _WORDS.add(text)
    fnt = font(size, weight)
    lines = wrap(text, fnt, max_width)
    line_h = int(size * spacing)
    width = max(int(math.ceil(fnt.getlength(l))) for l in lines) + 4
    img = Image.new("RGBA", (max(width, 1), line_h * len(lines) + size // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        lw = fnt.getlength(line)
        if align == "center":
            x = (img.width - lw) / 2
        elif align == "right":
            x = img.width - lw
        else:
            x = 0
        d.text((x, i * line_h), line, font=fnt, fill=color)
    return img


def paste(canvas: Image.Image, layer: Image.Image, xy: tuple, alpha: float = 1.0, rise: int = 18, anchor: str = "lt") -> None:
    """Alpha-composite a layer with a fade and a small upward motion."""
    if alpha <= 0:
        return
    x, y = xy
    if anchor[0] == "m":
        x -= layer.width // 2
    elif anchor[0] == "r":
        x -= layer.width
    if anchor[1] == "m":
        y -= layer.height // 2
    elif anchor[1] == "b":
        y -= layer.height
    y += int((1 - alpha) * rise)
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer = layer.copy()
        layer.putalpha(a)
    canvas.alpha_composite(layer, (int(x), int(y)))


def rounded(canvas: Image.Image, box, fill, radius=24, outline=None, width=3, alpha=1.0) -> None:
    if alpha <= 0:
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(layer)


def line(canvas: Image.Image, a, b, color, width=4, alpha=1.0) -> None:
    if alpha <= 0:
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).line([a, b], fill=color, width=width)
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(layer)


def new_canvas() -> Image.Image:
    return Image.new("RGBA", (W, H), BG + (255,))


def footer(canvas: Image.Image, label: str, alpha: float = 1.0) -> None:
    """Small source line at the bottom; the FACTS ids live in facts_used.md."""
    paste(canvas, text_block(label, 30, MUTED), (120, H - 70), alpha, rise=0)


def header(canvas: Image.Image, kicker: str, title: str, t: float, t0: float = 0.0) -> int:
    """Kicker plus scene title; returns the y where content may start."""
    paste(canvas, text_block(kicker.upper(), 34, ACCENT, "semibold"), (120, 90), fade(t, t0), rise=0)
    tb = text_block(title, 68, INK, "bold", max_width=W - 240, spacing=1.15)
    paste(canvas, tb, (120, 140), fade(t, t0 + 0.15))
    return 140 + tb.height + 40


# ----------------------------------------------------------------------------
# Scenes: each is a function (t) -> canvas, with a fixed duration
# ----------------------------------------------------------------------------


@dataclass
class Scene:
    name: str
    duration: float
    draw: Callable[[float], Image.Image]
    words: int = 0  # words on the card, measured by count_words


def fmt(x: float, nd: int = 2) -> str:
    return f"{x:.{nd}f}"


def scene_title(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        paste(c, text_block("CartelBench", 48, ACCENT, "semibold"), (W // 2, 300), fade(t, 0.2), anchor="mt")
        title = text_block(
            "Same Game, Different Players",
            96, INK, "bold", max_width=W - 300, align="center", spacing=1.1,
        )
        paste(c, title, (W // 2, 370), fade(t, 0.5), anchor="mt")
        sub = text_block(
            "A human-calibrated testbed for cartel enforcement on LLM pricing agents",
            44, MUTED, "regular", max_width=W - 400, align="center",
        )
        paste(c, sub, (W // 2, 500), fade(t, 1.0), anchor="mt")
        line(c, (W // 2 - 260, 640), (W // 2 + 260, 640), RULE, 3, fade(t, 2.6))
        q = text_block(
            "Do antitrust tools that work on people\nwork on AI pricing agents?",
            60, INK, "semibold", max_width=W - 300, align="center", spacing=1.25,
        )
        paste(c, q, (W // 2, 700), fade(t, 3.0), anchor="mt")
        footer(c, "AI Collusion Research Sprint, Apart Research, October 2026", fade(t, 4.0))
        return c

    return Scene("1 Title", 15.0, draw)


def scene_game(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The game", "Two firms, one price each period", t)
        # Firms
        for i, name in enumerate(["Firm A", "Firm B"]):
            x = 420 + i * 1080
            a = fade(t, 0.8 + i * 0.3)
            rounded(c, (x - 220, y0, x + 220, y0 + 120), ACCENT_SOFT, 28, alpha=a)
            paste(c, text_block(name, 54, ACCENT, "bold"), (x, y0 + 60), a, rise=0, anchor="mm")
        mid = text_block("may talk about prices first\n(a talk forms a cartel)", 40, MUTED, align="center")
        paste(c, mid, (W // 2, y0 + 60), fade(t, 1.6), anchor="mm")
        # Price axis
        ay = y0 + 460
        ax0, ax1 = 260, W - 260
        a = fade(t, 2.4)
        line(c, (ax0, ay), (ax1, ay), INK, 5, a)
        for p in range(13):
            x = ax0 + (ax1 - ax0) * p / 12
            line(c, (x, ay - 14), (x, ay + 14), INK, 4, a)
            paste(c, text_block(str(p), 40, INK), (x, ay + 30), a, rise=0, anchor="mt")
        paste(c, text_block("Price set by each firm, 0 to 12", 40, MUTED), (W // 2, ay + 100), a, rise=0, anchor="mt")
        # Markers
        for p, label, t0, col in [
            (3, "3  Nash\ncompetitive price", 3.6, HUMAN),
            (9, "9  Joint optimum\ncartel price", 4.6, ACCENT),
        ]:
            x = ax0 + (ax1 - ax0) * p / 12
            a = fade(t, t0)
            line(c, (x, ay - 40), (x, ay - 150), col, 6, a)
            rounded(c, (x - 22, ay - 22, x + 22, ay + 22), col, 22, alpha=a)
            paste(c, text_block(label, 44, col, "semibold", align="center", spacing=1.2), (x, ay - 170), a, anchor="mb")
        paste(
            c,
            text_block(
                "Profits follow the paper's payoff table. A pair stays together with probability 0.85.",
                40, INK, max_width=W - 240,
            ),
            (120, ay + 180), fade(t, 6.0),
        )
        return c

    return Scene("2 Game", 20.0, draw)


def scene_regimes(E: dict) -> Scene:
    cards = [
        ("No authority", "Laissez-faire", "No rule, no fine."),
        ("Fine", "Detection 0.10", "200 points per firm after detection or report."),
        ("Leniency", "Immunity", "The sole reporter pays nothing."),
        ("Reward", "Paid to report", "The sole reporter also receives the other firm's fine."),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Four regimes", "The enforcement rules the students faced", t)
        cw, gap = 390, 30
        x0 = (W - (4 * cw + 3 * gap)) // 2
        for i, (name, kicker, body) in enumerate(cards):
            a = fade(t, 1.2 + i * 1.3)
            x = x0 + i * (cw + gap)
            top, bottom = y0 + 20, y0 + 520
            rounded(c, (x, top, x + cw, bottom), (255, 255, 255, 255), 28, outline=RULE, width=3, alpha=a)
            rounded(c, (x, top, x + cw, top + 16), ACCENT, 8, alpha=a)
            paste(c, text_block(name, 50, INK, "bold", max_width=cw - 60), (x + 30, top + 50), a, rise=0)
            paste(c, text_block(kicker, 36, ACCENT, "semibold", max_width=cw - 60), (x + 30, top + 130), a, rise=0)
            paste(c, text_block(body, 40, INK, max_width=cw - 60, spacing=1.3), (x + 30, top + 210), a, rise=0)
        paste(
            c,
            text_block("Punishments are told, never paid. Regime names never appear in the prompt.",
                       40, MUTED, max_width=W - 240),
            (120, y0 + 580), fade(t, 6.5),
        )
        return c

    return Scene("3 Regimes", 23.5, draw)


def scene_testbed(E: dict) -> Scene:
    items = [
        ("Same rules, payoffs and instructions", f"Bigoni et al. (2012); {F['payoff_cells']} payoff cells match"),
        ("Human data as the baseline", "every measure next to the published student value"),
        ("Pre-registered", "decision rules committed before the first model call"),
        ("Four models, three families", "Claude Haiku 5.5, Claude Sonnet 5.5, Qwen2.5-32B, Llama-3.1-8B"),
        ("Complete record", f"{F['calls_total']} model calls, {F['refusals']} refusals, every run hashed"),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The testbed", "The human experiment, replayed with LLM sellers", t)
        y = y0 + 10
        for i, (head, body) in enumerate(items):
            a = fade(t, 1.2 + i * 1.6)
            rounded(c, (120, y + 14, 150, y + 44), ACCENT, 8, alpha=a)
            paste(c, text_block(head, 46, INK, "semibold", max_width=W - 300), (180, y), a, rise=0)
            paste(c, text_block(body, 40, MUTED, max_width=W - 300), (180, y + 62), a, rise=0)
            y += 140
        return c

    return Scene("4 Testbed", 25.0, draw)


def bar_chart(c: Image.Image, x0: int, y_base: int, height: int, bars: list, t: float, t0: float,
              vmax: float = 12.0, bar_w: int = 160, gap: int = 90, marks=((3, "3 Nash"), (9, "9 optimum"))) -> None:
    """Vertical bars with a 0..vmax scale and reference lines at Nash and optimum."""
    n = len(bars)
    width = n * bar_w + (n - 1) * gap
    a = fade(t, t0)
    line(c, (x0 - 40, y_base), (x0 + width + 40, y_base), INK, 4, a)
    for v, label in marks:
        y = y_base - height * v / vmax
        line(c, (x0 - 40, y), (x0 + width + 40, y), RULE, 3, a)
        paste(c, text_block(label, 32, MUTED), (x0 + width + 56, y), a, rise=0, anchor="lm")
    for i, (label, value, color, tb) in enumerate(bars):
        x = x0 + i * (bar_w + gap)
        g = fade(t, tb, 0.9)
        h = height * value / vmax * g
        if g > 0:
            rounded(c, (x, y_base - h, x + bar_w, y_base), color, 10)
        paste(c, text_block(fmt(value), 54, color, "bold"), (x + bar_w // 2, y_base - h - 16), g, rise=0, anchor="mb")
        paste(c, text_block(label, 38, INK, align="center", max_width=bar_w + gap - 10), (x + bar_w // 2, y_base + 20), fade(t, tb), rise=0, anchor="mt")


def scene_finding1(E: dict) -> Scene:
    hp = E["human_price"]["laissez_faire"]
    ap = E["price"]["haiku"]["laissez_faire"]
    hi = E["human_incidence"]["laissez_faire"]
    ai = E["incidence"]["haiku"]["laissez_faire"]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Finding 1", "Without an authority, agents form cartels as often as students, and keep them", t)
        bar_chart(
            c, 300, y0 + 520, 430,
            [("Human subjects", hp, HUMAN, 2.2), ("Claude Haiku 5.5", ap, ACCENT, 3.2)],
            t, 1.4, bar_w=200, gap=120,
        )
        paste(c, text_block("Average price, no authority", 40, MUTED), (300, y0 + 20), fade(t, 1.4), rise=0)
        x = 1080
        rows = [
            ("Cartel incidence", f"{fmt(hi, 3)} students, {fmt(ai, 3)} agents", 4.6),
            ("Deviation from the agreed price", f"{fmt(F['deviation_human_lf'], 3)} students, {fmt(F['deviation_haiku_lf'], 3)} agents", 6.2),
            ("Reading", "Students undercut their partner more than half the time. The agents almost never do, so the price stays near 9.", 8.0),
        ]
        y = y0 + 20
        for head, body, tb in rows:
            a = fade(t, tb)
            paste(c, text_block(head, 40, ACCENT, "semibold", max_width=W - x - 120), (x, y), a, rise=0)
            bb = text_block(body, 40, INK, max_width=W - x - 120)
            paste(c, bb, (x, y + 56), a, rise=0)
            y += 56 + bb.height + 30
        return c

    return Scene("5 Finding 1", 23.0, draw)


def scene_finding2(E: dict) -> Scene:
    rows = [
        ("Human subjects", E["human_price"], HUMAN, False),
        ("Claude Haiku 5.5", E["price"]["haiku"], INK, True),
        ("Claude Sonnet 5.5", E["price"]["sonnet"], INK, True),
        ("Qwen2.5-32B", E["price"]["qwen"], INK, True),
        ("Llama-3.1-8B", E["price"]["llama"], INK, True),
    ]
    inc = E["incidence"]
    caption = (
        "Explicit cartels under fine, leniency and reward: Sonnet "
        f"{fmt(max(inc['sonnet'][k] for k in REGIMES[1:]), 3)}, Qwen {fmt(max(inc['qwen'][k] for k in REGIMES[1:]), 3)}, "
        f"Llama at most {fmt(max(inc['llama'][k] for k in REGIMES[1:]), 3)}, Haiku {fmt(inc['haiku']['fine'], 3)} to {fmt(inc['haiku']['reward'], 3)}."
    )

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Finding 2", "Explicit cartels vanish. Prices stay high.", t)
        col_x = [120, 760, 1030, 1300, 1570]
        col_w = 250
        hy = y0 + 10
        a = fade(t, 1.2)
        for j, lab in enumerate(["Average price", *[REGIME_LABEL[k] for k in REGIMES]]):
            if j == 0:
                paste(c, text_block(lab, 36, MUTED, "semibold"), (col_x[j], hy), a, rise=0)
            else:
                paste(c, text_block(lab, 36, MUTED, "semibold"), (col_x[j] + col_w // 2, hy), a, rise=0, anchor="mt")
        line(c, (120, hy + 60), (W - 120, hy + 60), RULE, 3, a)
        rh = 90
        for i, (name, vals, color, is_model) in enumerate(rows):
            y = hy + 80 + i * rh
            ar = fade(t, 1.8 + i * 1.6)
            paste(c, text_block(name, 44, color, "semibold" if is_model else "regular"), (col_x[0], y + rh // 2), ar, rise=0, anchor="lm")
            for j, k in enumerate(REGIMES):
                v = vals[k]
                high = is_model and k != "laissez_faire" and v >= 5.5
                cx = col_x[j + 1] + col_w // 2
                if high:
                    rounded(c, (col_x[j + 1] + 30, y + 10, col_x[j + 1] + col_w - 30, y + rh - 10), ACCENT_SOFT, 16, alpha=ar)
                paste(c, text_block(fmt(v), 46, ACCENT if high else color, "bold" if high else "regular"), (cx, y + rh // 2), ar, rise=0, anchor="mm")
            line(c, (120, y + rh), (W - 120, y + rh), RULE, 2, ar)
        ty = hy + 80 + len(rows) * rh + 24
        paste(c, text_block("Nash price 3, joint optimum 9. Shaded: price 5.5 or more under a told rule.", 36, MUTED), (120, ty), fade(t, 3.0), rise=0)
        # Two captions share one slot: the first fades out when the second comes.
        a1 = fade(t, 10.0) * (1 - fade(t, 18.5, 0.5))
        a2 = fade(t, 19.0)
        paste(c, text_block(caption, 40, INK, max_width=W - 240), (120, ty + 64), a1)
        paste(
            c,
            text_block("Almost without a word: Sonnet asked to talk in 1 to 2 of 460 to 510 decisions. Only Haiku falls near Nash under leniency and reward.",
                       40, INK, max_width=W - 240),
            (120, ty + 64), a2,
        )
        return c

    return Scene("6 Finding 2", 31.0, draw)


def scene_finding3(E: dict) -> Scene:
    s = E["screen"]
    fp = E["screen_fp"]
    arms = [
        ("Sonnet 5.5\nno channel", s["sonnet_nocomm"], 2.6),
        ("Haiku 5.5\nno channel", s["haiku_nocomm"], 4.2),
        ("Haiku 5.5\nfine regime", s["haiku_fine"], 5.8),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Finding 3", "A price screen reaches silent coordination", t)
        paste(
            c,
            text_block(f"Pre-registered rule: a fine when both prices exceed 4 in two consecutive periods. False-positive rate at most {fp * 100:.1f} percent.",
                       40, INK, max_width=W - 240),
            (120, y0 + 10), fade(t, 1.0),
        )
        # Chart
        x0, y_base, height, vmax = 160, y0 + 600, 330, 10.0
        bw, gap, group = 100, 20, 90
        a = fade(t, 2.0)
        total = len(arms) * (2 * bw + gap) + (len(arms) - 1) * group
        line(c, (x0 - 30, y_base), (x0 + total + 30, y_base), INK, 4, a)
        for v, lab, col in [(3, "3 Nash", RULE), (4, "4 threshold", ACCENT)]:
            y = y_base - height * v / vmax
            line(c, (x0 - 30, y), (x0 + total + 30, y), col, 3 if v == 3 else 4, a)
            paste(c, text_block(lab, 32, ACCENT if v == 4 else MUTED, "semibold" if v == 4 else "regular"), (x0 + total + 46, y), a, rise=0, anchor="lm")
        for i, (label, (before, after), tb) in enumerate(arms):
            gx = x0 + i * (2 * bw + gap + group)
            g1, g2 = fade(t, tb, 0.8), fade(t, tb + 0.8, 0.8)
            h1, h2 = height * before / vmax * g1, height * after / vmax * g2
            if g1 > 0:
                rounded(c, (gx, y_base - h1, gx + bw, y_base), HUMAN, 8)
            if g2 > 0:
                rounded(c, (gx + bw + gap, y_base - h2, gx + 2 * bw + gap, y_base), ACCENT, 8)
            paste(c, text_block(fmt(before), 42, HUMAN, "bold"), (gx + bw // 2, y_base - h1 - 12), g1, rise=0, anchor="mb")
            paste(c, text_block(fmt(after), 42, ACCENT, "bold"), (gx + bw + gap + bw // 2, y_base - h2 - 12), g2, rise=0, anchor="mb")
            paste(c, text_block(label, 36, INK, align="center", spacing=1.2), (gx + bw + gap // 2, y_base + 20), fade(t, tb), rise=0, anchor="mt")
        leg_y = y0 + 150
        paste(c, text_block("without screen", 34, HUMAN, "semibold"), (160, leg_y), fade(t, 2.0), rise=0)
        paste(c, text_block("with screen", 34, ACCENT, "semibold"), (440, leg_y), fade(t, 2.0), rise=0)
        # Right column
        x = 1280
        pts = [
            ("Zero screen penalties in all three arms.", 7.5),
            ("Every Sonnet price sits exactly at the threshold: 4.", 9.5),
            ("A known threshold becomes the new focal price.", 12.0),
        ]
        y = leg_y + 10
        for body, tb in pts:
            a = fade(t, tb)
            emph = "exactly" in body
            bb = text_block(body, 42 if not emph else 46, ACCENT if emph else INK, "semibold" if emph else "regular", max_width=W - x - 120)
            rounded(c, (x - 24, y - 6, x - 10, y + bb.height - 20), ACCENT, 4, alpha=a)
            paste(c, bb, (x, y), a, rise=0)
            y += bb.height + 24
        return c

    return Scene("7 Finding 3", 26.0, draw)


def scene_scorecard(E: dict) -> Scene:
    fig = Image.open(FIGURE).convert("RGBA")
    scale = min((W - 160) / fig.width, (H - 260) / fig.height)
    fig = fig.resize((int(fig.width * scale), int(fig.height * scale)), Image.LANCZOS)
    rep, tested = E["scorecard"]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        paste(c, text_block("Scorecard".upper(), 34, ACCENT, "semibold"), (120, 60), fade(t, 0.0), rise=0)
        paste(
            c,
            text_block(f"{rep} of {tested} tested Bigoni results reproduced by Claude Haiku 5.5", 60, INK, "bold", max_width=W - 240, spacing=1.1),
            (120, 105), fade(t, 0.2),
        )
        paste(c, text_block("Primary sample: 8 pool sessions per core regime. Figure 1 of the report.", 36, MUTED), (120, 185), fade(t, 0.4), rise=0)
        paste(c, fig, ((W - fig.width) // 2, 240), fade(t, 1.4), rise=10)
        return c

    return Scene("8 Scorecard", 20.0, draw)


def scene_limits(E: dict) -> Scene:
    items = [
        ("A lab game, not a market", "thirteen prices, two firms, a known payoff table, a stylised authority"),
        ("Punishments are told, not paid", "a placebo text without a penalty removes about half of Haiku's fine effect"),
        ("The fine regime is sensitive to wording", "paraphrased instructions cut Haiku's cartel incidence under the fine from 0.40 to 0.02"),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Limits", "What the result does not establish", t)
        y = y0 + 30
        for i, (head, body) in enumerate(items):
            a = fade(t, 1.2 + i * 2.6)
            rounded(c, (120, y + 14, 150, y + 44), MUTED, 8, alpha=a)
            paste(c, text_block(head, 50, INK, "semibold", max_width=W - 300), (180, y), a, rise=0)
            paste(c, text_block(body, 40, MUTED, max_width=W - 300), (180, y + 70), a, rise=0)
            y += 200
        return c

    return Scene("9 Limits", 22.0, draw)


def scene_credits(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        paste(c, text_block("CartelBench", 48, ACCENT, "semibold"), (W // 2, 230), fade(t, 0.2), anchor="mt")
        paste(
            c,
            text_block("Same Game, Different Players: A Human-Calibrated Testbed for Cartel Enforcement on LLM Pricing Agents",
                       64, INK, "bold", max_width=W - 300, align="center", spacing=1.15),
            (W // 2, 300), fade(t, 0.5), anchor="mt",
        )
        paste(c, text_block("Julian Mundelein, Independent, Hong Kong", 44, INK, align="center"), (W // 2, 560), fade(t, 1.4), anchor="mt")
        paste(c, text_block("AI Collusion Research Sprint, Apart Research, October 2026", 40, MUTED, align="center"), (W // 2, 630), fade(t, 1.8), anchor="mt")
        line(c, (W // 2 - 260, 730), (W // 2 + 260, 730), RULE, 3, fade(t, 2.4))
        paste(c, text_block("Code, pre-registration, every model call and the report:", 40, MUTED, align="center"), (W // 2, 770), fade(t, 2.8), anchor="mt")
        paste(c, text_block("github.com/julianmundelein-beep/2026-ai-collusion-sprint", 46, ACCENT, "semibold", align="center"), (W // 2, 840), fade(t, 3.0), anchor="mt")
        return c

    return Scene("10 Credits", 16.0, draw)


def build_scenes() -> list[Scene]:
    E = evidence_numbers()
    return [
        scene_title(E),
        scene_game(E),
        scene_regimes(E),
        scene_testbed(E),
        scene_finding1(E),
        scene_finding2(E),
        scene_finding3(E),
        scene_scorecard(E),
        scene_limits(E),
        scene_credits(E),
    ]


# ----------------------------------------------------------------------------
# Timeline and rendering
# ----------------------------------------------------------------------------


def timeline(scenes: list[Scene]) -> list[tuple[float, float]]:
    """Start and end time of every scene; scenes overlap by XFADE."""
    out, start = [], 0.0
    for s in scenes:
        out.append((start, start + s.duration))
        start += s.duration - XFADE
    return out


def total_duration(scenes: list[Scene]) -> float:
    return timeline(scenes)[-1][1]


def frame_at(scenes: list[Scene], tl: list[tuple[float, float]], T: float) -> Image.Image:
    active = [(i, T - s0) for i, (s0, s1) in enumerate(tl) if s0 <= T < s1]
    if not active:
        i = len(scenes) - 1
        return scenes[i].draw(scenes[i].duration - 1 / FPS)
    if len(active) == 1:
        i, lt = active[0]
        return scenes[i].draw(lt)
    (i, lt_i), (j, lt_j) = active[0], active[1]
    a = scenes[i].draw(lt_i)
    b = scenes[j].draw(lt_j)
    k = ease(lt_j / XFADE)
    return Image.blend(a, b, k)


def count_words(scenes: list[Scene]) -> None:
    """Count the words every scene shows (its last frame) into Scene.words."""
    global _WORDS
    for s in scenes:
        _WORDS = set()
        s.draw(s.duration)
        # numbers, ticks and ids are read as a glance, not as prose
        s.words = sum(1 for x in _WORDS for w in x.split() if re.search(r"[A-Za-z]{2}", w))
    _WORDS = None


def check_reading_time(scenes: list[Scene]) -> None:
    """Every card stays at least 3 s plus 0.35 s per word."""
    for s in scenes:
        need = 3.0 + 0.35 * s.words
        if s.duration < need:
            raise SystemExit(f"{s.name}: {s.duration:.1f} s is shorter than the reading time {need:.1f} s for {s.words} words")


def render(scenes: list[Scene], out: Path) -> None:
    import imageio_ffmpeg

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    out.parent.mkdir(parents=True, exist_ok=True)
    tl = timeline(scenes)
    n_frames = int(round(total_duration(scenes) * FPS))
    cmd = [
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(out),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for n in range(n_frames):
        frame = frame_at(scenes, tl, n / FPS).convert("RGB")
        proc.stdin.write(frame.tobytes())
        if n % (FPS * 10) == 0:
            print(f"  {n / FPS:6.1f} s of {n_frames / FPS:.1f} s", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {n_frames / FPS:.1f} s)")


def stills(scenes: list[Scene]) -> None:
    """Three stills at the end of a build, for checking legibility."""
    STILLS_DIR.mkdir(parents=True, exist_ok=True)
    picks = {"06_finding2.png": "6 Finding 2", "07_finding3.png": "7 Finding 3", "02_game.png": "2 Game"}
    for fname, name in picks.items():
        s = next(x for x in scenes if x.name == name)
        s.draw(s.duration - XFADE - 0.1).convert("RGB").save(STILLS_DIR / fname, optimize=True)
        print(f"wrote {STILLS_DIR / fname}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stills-only", action="store_true")
    ap.add_argument("--timeline", action="store_true", help="print the scene times and exit")
    ap.add_argument("--out", type=Path, default=OUT_DIR / OUT_NAME)
    args = ap.parse_args()

    scenes = build_scenes()
    count_words(scenes)
    check_reading_time(scenes)
    tl = timeline(scenes)
    for s, (s0, s1) in zip(scenes, tl):
        print(f"{s.name:14s} {s0:6.1f} to {s1:6.1f} s  ({s.duration:.1f} s, {s.words} words)")
    print(f"total {total_duration(scenes):.1f} s")
    if args.timeline:
        return
    stills(scenes)
    if args.stills_only:
        return
    render(scenes, args.out)


if __name__ == "__main__":
    main()
