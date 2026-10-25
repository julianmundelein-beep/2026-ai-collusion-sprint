#!/usr/bin/env python3
"""Build the CartelBench explainer video from the repository.

Every frame is drawn with Pillow. Numbers come from paper/report.md and the
measurement files; where a machine-readable file exists in cartelbench/
evidence/ the value is read from it (round4 and provider2 scorecards,
round7/diagonal.json, round4/screen.json, risk_cards/risk_cards.json,
data/human_baseline.json). video/facts_used.md lists every number with its
source. Frames are piped into the ffmpeg binary of the PyPI package
imageio-ffmpeg.

    pip install pillow imageio-ffmpeg
    python3 video/build.py                 # render video/out/<name>.mp4 and video/stills/
    python3 video/build.py --timeline      # print the scene times and exit
    python3 video/build.py --stills-only   # only the PNG stills

Voice: if video/voice/01.mp3 ... 13.mp3 exist (one file per scene, see
narration.md), each scene lasts at least its file plus a pause and the files
are mixed under the video at the scene starts. Without them the scene length
follows the reading rule (3 s plus 0.35 s per word) and the timings in
narration.md.

Output: 1920x1080, 30 fps, H.264.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VIDEO_DIR = ROOT / "video"
OUT_DIR = VIDEO_DIR / "out"
STILLS_DIR = VIDEO_DIR / "stills"
VOICE_DIR = VIDEO_DIR / "voice"
OUT_NAME = "CartelBench_AI-Collusion-Research-Sprint_2026.mp4"
EVIDENCE = ROOT / "cartelbench" / "evidence"

W, H = 1920, 1080
FPS = 30
XFADE = 0.8        # seconds of cross-fade between scenes
VOICE_TAIL = 1.2   # seconds of silence after a voice file before the next scene
WPM = 150          # narration pace assumed without voice files

# Palette: one accent colour, warm paper background, near-black text.
BG = (250, 248, 244)
INK = (23, 32, 42)
MUTED = (107, 114, 128)
ACCENT = (46, 111, 214)
ACCENT_SOFT = (219, 230, 248)
RULE = (214, 211, 204)
HUMAN = (120, 120, 120)
GREEN = (36, 120, 70)
RED = (178, 48, 48)
GREEN_SOFT = (215, 236, 222)
RED_SOFT = (246, 218, 218)
GREY_SOFT = (232, 230, 225)

REGIMES = ["laissez_faire", "fine", "leniency", "reward"]
REGIME_LABEL = {"laissez_faire": "No authority", "fine": "Fine", "leniency": "Leniency", "reward": "Reward"}
MODEL_LABEL = {"haiku": "Claude Haiku 5.5", "sonnet": "Claude Sonnet 5.5", "qwen": "Qwen2.5-32B", "llama": "Llama-3.1-8B"}

# ----------------------------------------------------------------------------
# Numbers typed from paper/report.md (no JSON in the tree); ids in facts_used.md
# ----------------------------------------------------------------------------

R = {
    "human_price": {"laissez_faire": 4.92, "fine": 5.35, "leniency": 4.85, "reward": 3.97},  # Table 2 [F15]
    "deviation_haiku_lf": 0.015,   # Finding 1 [F13]
    "deviation_human_lf": 0.564,   # Finding 1 [F15]
    "payoff_cells": "169 of 169",  # contribution 1 [F08]
    "calls_total": 45286,          # Table A2 [F40]
    "sonnet_slope": "0.98",        # abstract [F85]
    "haiku_slope": "0.70",
    "qwen_slope": "0.68",
    "llama_slope": "0.31",
    "random_prices": [              # "Hiding the threshold" paragraph [F87]: (label, fixed at 4, random)
        ("Haiku 5.5", 4.16, 3.80), ("Sonnet 5.5", 4.00, 3.87), ("Qwen2.5-32B", 5.13, 5.55), ("Llama-3.1-8B", 4.55, 6.53),
    ],
    "random_p_haiku": "0.229",
    "random_share_drop": 0.54,     # share at 4 fell by 0.54 for Haiku and Sonnet [F87]
    "stakes_incidence": "0.093 to 0.164",  # Told or paid [F80, F81, F82]
    "fine_incidence_8pool": 0.401,
    "paraphrase_incidence": 0.018,  # [F50]
    "llama_training": ("-0.50", "-0.60", "0.222", "0.206"),  # [F91, F92]
    "scorecard_caveat": "Result 3 passes the bootstrap rule, not the permutation test (p 0.099); the first 4 pools give 2 of 7.",  # [F46]
}


def load_json(path: Path) -> dict:
    with open(path) as fh:
        return json.load(fh)


def evidence_numbers() -> dict:
    """Numbers read from the evidence files."""
    cards = {
        "haiku": load_json(EVIDENCE / "round4" / "scorecard_haiku_8pool" / "scorecard.json"),
        "sonnet": load_json(EVIDENCE / "round4" / "scorecard_sonnet_4pool" / "scorecard.json"),
        "qwen": load_json(EVIDENCE / "provider2" / "scorecard" / "scorecard.json"),
        "llama": load_json(EVIDENCE / "provider2" / "scorecard_llama-3.1-8b-instruct" / "scorecard.json"),
    }
    human = load_json(ROOT / "cartelbench" / "data" / "human_baseline.json")
    diagonal = load_json(EVIDENCE / "round7" / "diagonal.json")
    screen = load_json(EVIDENCE / "round4" / "screen.json")
    risk = load_json(EVIDENCE / "risk_cards" / "risk_cards.json")
    states = load_json(EVIDENCE / "round4" / "scorecards.json")["sets"]["haiku_8pool"]

    def row(card: dict, measure: str) -> dict:
        return next(r for r in card["rows"] if r["measure"] == measure)

    diag: dict = {}
    for r in diagonal["rows"]:
        diag.setdefault(r["model"], []).append((r["threshold"], r["avg_price"], r["share_at_threshold"], r["modal_price"]))
    fp = screen["false_positive_rate_max"]
    return {
        "human_incidence_lf": human["regimes"]["laissez_faire"]["cartel_incidence"],
        "price": {m: row(c, "avg_price")["llm"] for m, c in cards.items()},
        "incidence": {m: {k: c["metrics"][k]["cartel_incidence"] for k in REGIMES} for m, c in cards.items()},
        "scorecard": (cards["haiku"]["reproduced"], cards["haiku"]["tested"]),
        "scorecard_rows": [(r["n"], r["result"], states["states"][str(r["n"])]) for r in cards["haiku"]["rows"]],
        "diagonal": diag,
        "screen_fp": fp,
        "risk": risk,
    }


# ----------------------------------------------------------------------------
# Fonts and drawing helpers
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
    if key not in _font_cache:
        for name in FONT_FILES[weight]:
            for d in FONT_DIRS:
                if (d / name).is_file():
                    _font_cache[key] = ImageFont.truetype(str(d / name), size)
                    return _font_cache[key]
        _font_cache[key] = ImageFont.load_default(size)
    return _font_cache[key]


def ease(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def fade(t: float, t0: float, dur: float = 0.6) -> float:
    return ease((t - t0) / dur)


def pulse(t: float, t0: float, dur: float = 1.2) -> float:
    """0 to 1 to 0 around t0, for a short highlight ring."""
    x = (t - t0) / dur
    if x < 0 or x > 1:
        return 0.0
    return math.sin(x * math.pi)


def wrap(text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split(" "):
            cand = (cur + " " + w).strip()
            if fnt.getlength(cand) <= max_width or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(text: str, size: int, color=INK, weight: str = "regular", max_width: int = W - 240,
               align: str = "left", spacing: float = 1.3) -> Image.Image:
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
        x = (img.width - lw) / 2 if align == "center" else (img.width - lw if align == "right" else 0)
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


def shape_layer(canvas: Image.Image, draw_fn: Callable[[ImageDraw.ImageDraw], None], alpha: float = 1.0) -> None:
    if alpha <= 0:
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    if alpha < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(layer)


def rounded(canvas, box, fill, radius=24, outline=None, width=3, alpha=1.0) -> None:
    shape_layer(canvas, lambda d: d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width), alpha)


def line(canvas, a, b, color, width=4, alpha=1.0) -> None:
    shape_layer(canvas, lambda d: d.line([a, b], fill=color, width=width), alpha)


def dashed(canvas, a, b, color, width=4, dash=18, alpha=1.0) -> None:
    (x0, y0), (x1, y1) = a, b
    length = math.hypot(x1 - x0, y1 - y0)
    n = int(length // (dash * 2))

    def draw(d):
        for i in range(n + 1):
            s, e = i * 2 * dash / length, min(1.0, (i * 2 * dash + dash) / length)
            d.line([(x0 + (x1 - x0) * s, y0 + (y1 - y0) * s), (x0 + (x1 - x0) * e, y0 + (y1 - y0) * e)], fill=color, width=width)

    shape_layer(canvas, draw, alpha)


def circle(canvas, c, r, fill=None, outline=None, width=4, alpha=1.0) -> None:
    x, y = c
    shape_layer(canvas, lambda d: d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=width), alpha)


def new_canvas() -> Image.Image:
    return Image.new("RGBA", (W, H), BG + (255,))


def footer(canvas: Image.Image, label: str, alpha: float = 1.0) -> None:
    paste(canvas, text_block(label, 30, MUTED, max_width=W - 240), (120, H - 80), alpha, rise=0)


def header(canvas: Image.Image, kicker: str, title: str, t: float, t0: float = 0.0, size: int = 68) -> int:
    """Kicker plus scene title; returns the y where content may start."""
    paste(canvas, text_block(kicker.upper(), 34, ACCENT, "semibold"), (120, 90), fade(t, t0), rise=0)
    tb = text_block(title, size, INK, "bold", max_width=W - 240, spacing=1.15)
    paste(canvas, tb, (120, 140), fade(t, t0 + 0.15))
    return 140 + tb.height + 30


def count_up(t: float, t0: float, value: float, dur: float = 1.2) -> float:
    return value * ease((t - t0) / dur)


def fmt(x: float, nd: int = 2) -> str:
    return f"{x:.{nd}f}"


def bullet_list(c: Image.Image, items: list, y: int, t: float, t0: float, step: float, color=ACCENT, gap: int = 140,
                head_size: int = 46, body_size: int = 40) -> int:
    """Head and body lines appearing one after another; the newest item is full, earlier ones stay."""
    for i, (head, body) in enumerate(items):
        a = fade(t, t0 + i * step)
        rounded(c, (120, y + 14, 150, y + 44), color, 8, alpha=a)
        paste(c, text_block(head, head_size, INK, "semibold", max_width=W - 300), (180, y), a, rise=0)
        if body:
            paste(c, text_block(body, body_size, MUTED, max_width=W - 300), (180, y + head_size + 16), a, rise=0)
        y += gap
    return y


# ----------------------------------------------------------------------------
# Scenes
# ----------------------------------------------------------------------------


@dataclass
class Scene:
    name: str
    draw: Callable[[float], Image.Image]
    min_duration: float = 0.0   # the last element appears before this
    words: int = 0              # measured by count_words
    duration: float = 0.0       # set by plan_durations


def scene_00_intro(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        # two firms move together and agree on a price
        k = ease((t - 0.6) / 1.8)
        for i, name in enumerate(["Firm A", "Firm B"]):
            x0 = 420 if i == 0 else W - 420
            x1 = W // 2 - 300 if i == 0 else W // 2 + 300
            x = x0 + (x1 - x0) * k
            a = fade(t, 0.2)
            rounded(c, (x - 200, 300, x + 200, 420), ACCENT_SOFT, 28, alpha=a)
            paste(c, text_block(name, 50, ACCENT, "bold"), (x, 360), a, rise=0, anchor="mm")
        ag = fade(t, 2.4)
        line(c, (W // 2 - 100, 360), (W // 2 + 100, 360), ACCENT, 5, ag)
        paste(c, text_block("one price", 36, ACCENT, "semibold"), (W // 2, 330), ag, rise=0, anchor="mb")
        paste(c, text_block("When two companies quietly agree on a price instead of competing, customers pay more.", 54, INK, "semibold",
                            max_width=W - 300, align="center", spacing=1.25), (W // 2, 520), fade(t, 0.4), anchor="mt")
        paste(c, text_block("That is a cartel, and it is illegal almost everywhere.", 48, INK,
                            max_width=W - 300, align="center"), (W // 2, 710), fade(t, 4.6), anchor="mt")
        return c

    return Scene("01 Intro", draw, min_duration=6.0)


def scene_01_title(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        paste(c, text_block("CartelBench", 44, ACCENT, "semibold"), (W // 2, 150), fade(t, 0.2), anchor="mt")
        paste(c, text_block("Same Game, Different Players", 84, INK, "bold", max_width=W - 300, align="center", spacing=1.1),
              (W // 2, 215), fade(t, 0.5), anchor="mt")
        paste(c, text_block("A Human-Calibrated Testbed for Cartel Enforcement on LLM Pricing Agents", 42, MUTED,
                            max_width=W - 400, align="center"), (W // 2, 340), fade(t, 1.0), anchor="mt")
        # the three instruments, one after another
        for i, w in enumerate(["Fines", "Leniency", "Rewards"]):
            a = fade(t, 3.0 + i * 0.7)
            x = W // 2 + (i - 1) * 420
            rounded(c, (x - 170, 480, x + 170, 570), ACCENT_SOFT, 24, alpha=a)
            paste(c, text_block(w, 48, ACCENT, "bold"), (x, 525), a, rise=0, anchor="mm")
        paste(c, text_block("Three tools against cartels. All three were designed for people.", 44, INK, align="center",
                            max_width=W - 300), (W // 2, 610), fade(t, 5.6), anchor="mt")
        paste(c, text_block("Today, more and more prices are set by software, and language-model agents are starting to set them too.",
                            44, MUTED, align="center", max_width=W - 300), (W // 2, 690), fade(t, 8.4), anchor="mt")
        paste(c, text_block("Do the three tools work on them?", 60, INK, "semibold", align="center"),
              (W // 2, 820), fade(t, 11.5), anchor="mt")
        return c

    return Scene("02 Title", draw, min_duration=14.0)


def scene_02_game(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The game", "Two firms, one price each period", t)
        for i, name in enumerate(["Firm A", "Firm B"]):
            x = 420 + i * 1080
            a = fade(t, 0.8 + i * 0.3)
            rounded(c, (x - 220, y0, x + 220, y0 + 120), ACCENT_SOFT, 28, alpha=a)
            paste(c, text_block(name, 54, ACCENT, "bold"), (x, y0 + 60), a, rise=0, anchor="mm")
        paste(c, text_block("may talk about prices first\n(a talk forms a cartel)", 40, MUTED, align="center"),
              (W // 2, y0 + 60), fade(t, 2.0), anchor="mm")
        ay = y0 + 460
        ax0, ax1 = 260, W - 260
        a = fade(t, 3.2)
        line(c, (ax0, ay), (ax1, ay), INK, 5, a)
        for p in range(13):
            x = ax0 + (ax1 - ax0) * p / 12
            line(c, (x, ay - 14), (x, ay + 14), INK, 4, a)
            paste(c, text_block(str(p), 40, INK), (x, ay + 30), a, rise=0, anchor="mt")
        paste(c, text_block("Price set by each firm, 0 to 12", 40, MUTED), (W // 2, ay + 100), a, rise=0, anchor="mt")
        for p, label, t0, col in [(3, "3  Nash\ncompetitive price", 4.6, HUMAN), (9, "9  Joint optimum\ncartel price", 6.2, ACCENT)]:
            x = ax0 + (ax1 - ax0) * p / 12
            a = fade(t, t0)
            line(c, (x, ay - 40), (x, ay - 150), col, 6, a)
            circle(c, (x, ay), 22, fill=col, alpha=a)
            circle(c, (x, ay), 22 + 30 * pulse(t, t0 + 0.4), outline=col, width=5, alpha=pulse(t, t0 + 0.4))
            paste(c, text_block(label, 44, col, "semibold", align="center", spacing=1.2), (x, ay - 170), a, anchor="mb")
        paste(c, text_block("Profits follow the paper's payoff table. A pair stays together with probability 0.85.", 40, INK),
              (120, ay + 180), fade(t, 8.0))
        return c

    return Scene("03 Game", draw, min_duration=12.0)


def scene_03_humans(E: dict) -> Scene:
    cards = [
        ("No authority", "no rule, no fine"),
        ("Fine", "200 points per firm, detection 0.10 per period"),
        ("Leniency", "the sole reporter pays nothing"),
        ("Reward", "the reporter also receives the other firm's fine"),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The human experiment, Bigoni et al. (2012)", "Students played this game under four rules", t)
        cw, gap = 390, 30
        x0 = (W - (4 * cw + 3 * gap)) // 2
        top, bottom = y0 + 20, y0 + 470
        for i, (name, body) in enumerate(cards):
            a = fade(t, 1.4 + i * 1.3)
            x = x0 + i * (cw + gap)
            rounded(c, (x, top, x + cw, bottom), (255, 255, 255, 255), 28, outline=RULE, width=3, alpha=a)
            rounded(c, (x, top, x + cw, top + 16), ACCENT, 8, alpha=a)
            paste(c, text_block(name, 48, INK, "bold", max_width=cw - 60), (x + 30, top + 50), a, rise=0)
            paste(c, text_block(body, 38, INK, max_width=cw - 60, spacing=1.3), (x + 30, top + 130), a, rise=0)
            # students' average price, second beat
            k = REGIMES[i]
            b = fade(t, 7.6 + i * 0.5)
            paste(c, text_block("students' average price", 32, MUTED), (x + 30, bottom - 150), b, rise=0)
            hi = k == "reward"
            paste(c, text_block(fmt(R["human_price"][k]), 60, ACCENT if hi else INK, "bold"), (x + 30, bottom - 108), b, rise=0)
        paste(c, text_block("Only the reward pushed the students' prices toward the competitive price 3.",
                            40, INK, max_width=W - 240), (120, bottom + 40), fade(t, 10.5))
        return c

    return Scene("04 Humans", draw, min_duration=15.0)


def scene_04_testbed(E: dict) -> Scene:
    items = [
        ("Same rules, payoffs and instructions", f"{R['payoff_cells']} payoff cells match the paper"),
        ("Human data as the baseline", "each measure next to the student value"),
        ("Pre-registered", "rules committed before the first model call"),
        ("Four models, three families", "Claude Haiku 5.5, Claude Sonnet 5.5, Qwen2.5-32B, Llama-3.1-8B"),
        ("Complete record", None),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The testbed", "The human experiment, replayed with LLM sellers", t)
        y = bullet_list(c, items, y0 + 10, t, 1.2, 1.7)
        a = fade(t, 1.2 + 4 * 1.7)
        n = int(count_up(t, 1.2 + 4 * 1.7, R["calls_total"], 1.5))
        paste(c, text_block(f"{n:,} model calls, 0 refusals, every run hashed", 40, MUTED), (180, y - 140 + 62), a, rise=0)
        return c

    return Scene("05 Testbed", draw, min_duration=12.0)


def scene_05_table(E: dict) -> Scene:
    rows = [
        ("Human subjects", R["human_price"], HUMAN, False),
        ("Claude Haiku 5.5", E["price"]["haiku"], INK, True),
        ("Claude Sonnet 5.5", E["price"]["sonnet"], INK, True),
        ("Qwen2.5-32B", E["price"]["qwen"], INK, True),
        ("Llama-3.1-8B", E["price"]["llama"], INK, True),
    ]
    inc = E["incidence"]
    hi_lf, ai_lf = E["human_incidence_lf"], inc["haiku"]["laissez_faire"]
    T_ROW = [1.6, 3.0, 11.0, 13.0, 15.0]  # when each row appears
    T_B1, T_B2 = 5.0, 17.5                # callouts

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Finding 1 and 2", "Told rules remove the explicit cartels. The price stays.", t, size=64)
        col_x = [120, 760, 1030, 1300, 1570]
        col_w = 250
        hy = y0
        a = fade(t, 1.0)
        for j, lab in enumerate(["Average price", *[REGIME_LABEL[k] for k in REGIMES]]):
            pos = (col_x[j], hy) if j == 0 else (col_x[j] + col_w // 2, hy)
            paste(c, text_block(lab, 36, MUTED, "semibold"), pos, a, rise=0, anchor="lt" if j == 0 else "mt")
        line(c, (120, hy + 60), (W - 120, hy + 60), RULE, 3, a)
        rh = 86
        # column focus: first the no-authority column, then the three prohibited ones
        focus_lf = fade(t, T_B1) * (1 - fade(t, T_ROW[2] - 0.5, 0.5))
        focus_rules = fade(t, T_B2)
        for i, (name, vals, color, is_model) in enumerate(rows):
            y = hy + 80 + i * rh
            ar = fade(t, T_ROW[i])
            paste(c, text_block(name, 44, color, "semibold" if is_model else "regular"), (col_x[0], y + rh // 2), ar, rise=0, anchor="lm")
            for j, k in enumerate(REGIMES):
                v = vals[k]
                high = is_model and k != "laissez_faire" and v >= 5.5
                cx = col_x[j + 1] + col_w // 2
                if k == "laissez_faire" and focus_lf > 0:
                    rounded(c, (col_x[1] + 30, y + 8, col_x[1] + col_w - 30, y + rh - 8), ACCENT_SOFT, 14, alpha=focus_lf * ar)
                if high and focus_rules > 0:
                    rounded(c, (col_x[j + 1] + 30, y + 8, col_x[j + 1] + col_w - 30, y + rh - 8), ACCENT_SOFT, 14, alpha=focus_rules * ar)
                emph = (k == "laissez_faire" and focus_lf > 0.5) or (high and focus_rules > 0.5)
                paste(c, text_block(fmt(v), 46, ACCENT if emph else color, "bold" if emph else "regular"), (cx, y + rh // 2), ar, rise=0, anchor="mm")
            line(c, (120, y + rh), (W - 120, y + rh), RULE, 2, ar)
        ty = hy + 80 + len(rows) * rh + 20
        paste(c, text_block("Nash price 3, joint optimum 9.", 34, MUTED), (120, ty), fade(t, 1.0), rise=0)
        a1 = fade(t, T_B1) * (1 - fade(t, T_ROW[2] - 0.5, 0.5))
        b1 = text_block(
            f"No authority: cartels as often as the students (incidence {fmt(ai_lf, 3)} against {fmt(hi_lf, 3)}), "
            f"but students undercut in {fmt(R['deviation_human_lf'], 3)} of periods, Haiku in {fmt(R['deviation_haiku_lf'], 3)}. The price stays near 9.",
            40, INK, max_width=W - 240)
        paste(c, b1, (120, ty + 50), a1)
        a2 = fade(t, T_B2)
        b2 = text_block(
            f"Told rules: Sonnet and Qwen never form a cartel (incidence {fmt(inc['sonnet']['fine'], 3)}), yet three of four models "
            "keep prices at 5.7 to 7.3, almost without a word. Only Haiku falls near Nash.",
            40, INK, max_width=W - 240)
        paste(c, b2, (120, ty + 50), a2)
        return c

    return Scene("06 Table", draw, min_duration=T_B2 + 7)


def scene_06_line(E: dict) -> Scene:
    diag = E["diagonal"]
    series = [
        ("Sonnet 5.5", diag["Sonnet 5.5"], ACCENT, R["sonnet_slope"]),
        ("Haiku 5.5", diag["Haiku 5.5"], (214, 108, 46), R["haiku_slope"]),
        ("Qwen2.5-32B", diag["Qwen2.5-32B"], (36, 150, 110), R["qwen_slope"]),
        ("Llama-3.1-8B", diag["Llama-3.1-8B"], (120, 100, 200), R["llama_slope"]),
    ]
    T_RULE, T_AXES = 1.0, 3.0
    T_SONNET = [4.5, 5.7, 6.9, 8.1]
    T_SONNET_LABEL = 9.5
    T_HAIKU, T_QWEN, T_LLAMA = 13.0, 15.0, 18.0
    T_POINTE, T_READ = 22.5, 26.5
    # chart geometry
    cx0, cx1, cy0, cy1 = 260, 1180, 940, 420   # x: threshold 2.5..7.5; y: price 2.5..7.5
    fp = E["screen_fp"]

    def X(p):
        return cx0 + (cx1 - cx0) * (p - 2.5) / 5

    def Y(v):
        return cy0 + (cy1 - cy0) * (v - 2.5) / 5

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "The central finding", "The announced threshold becomes the price", t)
        paste(c, text_block("Screen rule: a fine when both prices exceed a threshold in two consecutive periods.", 38, INK, max_width=W - 240),
              (120, y0 - 10), fade(t, T_RULE))
        # axes
        a = fade(t, T_AXES)
        line(c, (cx0, cy0), (cx1, cy0), INK, 4, a)
        line(c, (cx0, cy0), (cx0, cy1), INK, 4, a)
        for p in range(3, 8):
            paste(c, text_block(str(p), 36, INK), (X(p), cy0 + 16), a, rise=0, anchor="mt")
            line(c, (X(p), cy0 - 8), (X(p), cy0 + 8), INK, 3, a)
            paste(c, text_block(str(p), 36, INK), (cx0 - 20, Y(p)), a, rise=0, anchor="rm")
            line(c, (cx0, Y(p)), (cx1, Y(p)), RULE, 2, a)
        paste(c, text_block("announced threshold", 36, MUTED), ((cx0 + cx1) // 2, cy0 + 64), a, rise=0, anchor="mt")
        paste(c, text_block("average price", 36, MUTED), (cx0 + 16, cy1 - 12), a, rise=0, anchor="lb")
        dashed(c, (X(2.6), Y(2.6)), (X(7.4), Y(7.4)), HUMAN, 4, alpha=fade(t, T_AXES + 0.6))
        paste(c, text_block("price = threshold", 34, HUMAN, "semibold"), (X(7.0) + 10, Y(7.0) - 50), fade(t, T_AXES + 0.6), rise=0, anchor="lb")
        # series
        starts = {"Sonnet 5.5": None, "Haiku 5.5": T_HAIKU, "Qwen2.5-32B": T_QWEN, "Llama-3.1-8B": T_LLAMA}
        for name, pts, col, slope in series:
            pts = sorted(pts)
            if name == "Sonnet 5.5":
                for i, (p, v, share, modal) in enumerate(pts):
                    ai = fade(t, T_SONNET[i])
                    if i > 0:
                        pp, vv = pts[i - 1][0], pts[i - 1][1]
                        line(c, (X(pp), Y(vv)), (X(p), Y(v)), col, 5, ai)
                    circle(c, (X(p), Y(v)), 14, fill=col, alpha=ai)
                    circle(c, (X(p), Y(v)), 14 + 36 * pulse(t, T_SONNET[i], 1.0), outline=col, width=5, alpha=pulse(t, T_SONNET[i], 1.0))
                    paste(c, text_block(fmt(v), 36, col, "bold"), (X(p) + 22, Y(v) - 10), ai, rise=0, anchor="lb")
            else:
                t0 = starts[name]
                dim = 0.85
                for i, (p, v, share, modal) in enumerate(pts):
                    ai = fade(t, t0 + i * 0.25) * dim
                    if i > 0:
                        line(c, (X(pts[i - 1][0]), Y(pts[i - 1][1])), (X(p), Y(v)), col, 4, ai)
                    if modal == p:
                        circle(c, (X(p), Y(v)), 11, fill=col, alpha=ai)
                    else:
                        circle(c, (X(p), Y(v)), 11, fill=BG + (255,), outline=col, width=4, alpha=ai)
        # legend / messages on the right
        rx = 1300
        msgs = [
            (T_SONNET_LABEL, f"Sonnet 5.5: slope {R['sonnet_slope']}, at least 93 percent of prices exactly on the line.", ACCENT, True),
            (T_HAIKU + 1.0, f"Haiku 5.5 ({R['haiku_slope']}) and Qwen2.5-32B ({R['qwen_slope']}): most frequent price always the threshold.", INK, False),
            (T_LLAMA + 1.0, f"Llama-3.1-8B ({R['llama_slope']}) does not follow (hollow: mode off the line).", MUTED, False),
        ]
        y = y0 + 150
        gone = 1 - fade(t, T_POINTE - 0.6, 0.5)  # the three notes make room for the pointe
        for t0, text, col, strong in msgs:
            a = fade(t, t0) * gone
            bb = text_block(text, 38, col, "semibold" if strong else "regular", max_width=W - rx - 120)
            rounded(c, (rx - 24, y - 4, rx - 10, y + bb.height - 18), col, 4, alpha=a)
            paste(c, bb, (rx, y), a, rise=0)
            y += bb.height + 22
        # the pointe: threshold 3
        ap = fade(t, T_POINTE)
        circle(c, (X(3), Y(3)), 14 + 40 * pulse(t, T_POINTE, 1.6), outline=ACCENT, width=6, alpha=pulse(t, T_POINTE, 1.6))
        y = y0 + 150
        pb = text_block("At threshold 3, the competitive price, every Sonnet price is exactly 3.", 44, ACCENT, "semibold", max_width=W - rx - 120)
        rounded(c, (rx - 24, y - 4, rx - 10, y + pb.height - 18), ACCENT, 4, alpha=ap)
        paste(c, pb, (rx, y), ap)
        rb = text_block("I read this as optimisation against the rule: the threshold is the most profitable price the rule allows.", 40, INK, max_width=W - rx - 120)
        paste(c, rb, (rx, y + pb.height + 30), fade(t, T_READ))
        return c

    return Scene("07 Line", draw, min_duration=T_READ + 6)


def scene_07_random(E: dict) -> Scene:
    arms = R["random_prices"]
    T_LEFT, T_RIGHT = 1.5, 8.0

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "An honest negative", "Hiding the threshold dissolves the bunching, not the price", t, size=62)
        # left: bunching at 4 (share of prices at 4, fixed vs random), Haiku and Sonnet
        paste(c, text_block("Threshold drawn at random from 3 to 6 each period and never disclosed", 38, INK, max_width=W - 240),
              (120, y0 - 10), fade(t, 0.8))
        lx = 120
        paste(c, text_block("Share of prices exactly at 4", 36, MUTED, "semibold"), (lx, y0 + 90), fade(t, T_LEFT), rise=0)
        bars = [("Haiku 5.5", 0.645, 0.105), ("Sonnet 5.5", 1.000, 0.465)]  # random.md, at-4 shares
        base_y, hgt = y0 + 500, 280
        for i, (name, fixed, rnd) in enumerate(bars):
            gx = lx + 60 + i * 330
            a1, a2 = fade(t, T_LEFT + 0.5 + i * 0.6, 0.8), fade(t, T_LEFT + 2.0 + i * 0.6, 0.8)
            h1, h2 = hgt * fixed * a1, hgt * rnd * a2
            if a1 > 0:
                rounded(c, (gx, base_y - h1, gx + 110, base_y), HUMAN, 8)
            if a2 > 0:
                rounded(c, (gx + 130, base_y - h2, gx + 240, base_y), ACCENT, 8)
            paste(c, text_block(fmt(fixed, 2), 36, HUMAN, "bold"), (gx + 55, base_y - h1 - 10), a1, rise=0, anchor="mb")
            paste(c, text_block(fmt(rnd, 2), 36, ACCENT, "bold"), (gx + 185, base_y - h2 - 10), a2, rise=0, anchor="mb")
            paste(c, text_block(name, 36, INK), (gx + 120, base_y + 16), fade(t, T_LEFT + 0.5), rise=0, anchor="mt")
        line(c, (lx, base_y), (lx + 760, base_y), INK, 3, fade(t, T_LEFT))
        paste(c, text_block("announced at 4", 32, HUMAN, "semibold"), (lx, base_y + 80), fade(t, T_LEFT), rise=0)
        paste(c, text_block("random, hidden", 32, ACCENT, "semibold"), (lx + 300, base_y + 80), fade(t, T_LEFT), rise=0)
        # right: average prices fixed vs random
        rx = 1000
        paste(c, text_block("Average price", 36, MUTED, "semibold"), (rx, y0 + 90), fade(t, T_RIGHT), rise=0)
        paste(c, text_block("announced at 4", 32, HUMAN, "semibold"), (rx + 360, y0 + 94), fade(t, T_RIGHT), rise=0)
        paste(c, text_block("random, hidden", 32, ACCENT, "semibold"), (rx + 640, y0 + 94), fade(t, T_RIGHT), rise=0)
        for i, (name, fixed, rnd) in enumerate(arms):
            y = y0 + 160 + i * 80
            a = fade(t, T_RIGHT + 0.6 + i * 0.7)
            paste(c, text_block(name, 40, INK), (rx, y), a, rise=0)
            paste(c, text_block(fmt(fixed), 40, HUMAN, "bold"), (rx + 360, y), a, rise=0)
            paste(c, text_block(fmt(rnd), 40, ACCENT, "bold"), (rx + 640, y), a, rise=0)
        paste(c, text_block(f"Haiku, Sonnet and Qwen within noise (Haiku p {R['random_p_haiku']}), Llama rose: no detectable price decrease.",
                            40, INK, max_width=W - rx - 120),
              (rx, y0 + 500), fade(t, T_RIGHT + 4.0))
        return c

    return Scene("08 Random", draw, min_duration=T_RIGHT + 9)


def scene_08_stakes(E: dict) -> Scene:
    lo, hi = R["stakes_incidence"].split(" to ")
    d1, d2, dist0, dist1 = R["llama_training"]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Told or paid", "Money, loss and bankruptcy: about as much as a rewording", t, size=56)
        frames = ["points as money", "loss from own capital", "risk of bankruptcy"]
        for i, f in enumerate(frames):
            a = fade(t, 1.2 + i * 0.6)
            x = 120 + i * 560
            rounded(c, (x, y0 + 10, x + 520, y0 + 100), ACCENT_SOFT, 20, alpha=a)
            paste(c, text_block(f, 40, ACCENT, "semibold"), (x + 260, y0 + 55), a, rise=0, anchor="mm")
        rows = [
            (3.6, "Haiku, fine regime, cartel incidence", f"{lo} to {hi}, against {fmt(R['fine_incidence_8pool'], 3)} original and {fmt(R['paraphrase_incidence'], 3)} with a rewording alone"),
            (7.0, "No loss aversion", "loss and gain frame equivalent within the margin"),
            (10.0, "Llama retrained after fines (exploratory)", f"prices {d1} and {d2} under leniency and reward; distance to the students {dist0} to {dist1}"),
        ]
        y = y0 + 150
        for t0, head, body in rows:
            a = fade(t, t0)
            rounded(c, (120, y + 14, 150, y + 44), ACCENT, 8, alpha=a)
            paste(c, text_block(head, 44, INK, "semibold", max_width=W - 300), (180, y), a, rise=0)
            bb = text_block(body, 40, MUTED, max_width=W - 300)
            paste(c, bb, (180, y + 60), a, rise=0)
            y += 60 + bb.height + 36
        return c

    return Scene("09 Stakes", draw, min_duration=16.0)


def scene_09_risk_card(E: dict) -> Scene:
    risk = E["risk"]
    card = risk["Sonnet 5.5"] if "Sonnet 5.5" in risk else None
    rows = [
        ("Laissez-faire incidence", "1.000", "students 0.961"),
        ("Fine: incidence drop", "+1.000", "students +0.378"),
        ("Reward price", "5.740", "students 3.973"),
        ("Silent price, no channel", "7.364", "Nash 3"),
        ("Against a Nash partner", "3.796", ""),
        ("Share at the announced threshold", "p3 1.00  p4 1.00  p5 0.98  p6 0.93", ""),
        ("Instructed to coordinate", "price 4.000, 0 penalties", ""),
        ("Cost", "0.245 USD per duopoly", ""),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Application", "A Cartel Risk Card per model, before deployment", t)
        paste(c, text_block("One page per model from the recorded runs. Example: Sonnet 5.5.", 40, INK,
                            max_width=W - 240), (120, y0 - 10), fade(t, 0.8))
        top = y0 + 80
        rounded(c, (120, top, W - 120, top + 70 + len(rows) * 66 + 20), (255, 255, 255, 255), 24, outline=RULE, width=3, alpha=fade(t, 1.4))
        paste(c, text_block("Cartel Risk Card: Claude Sonnet 5.5", 40, ACCENT, "bold"), (160, top + 20), fade(t, 1.4), rise=0)
        for i, (k, v, base) in enumerate(rows):
            y = top + 90 + i * 66
            a = fade(t, 2.4 + i * 0.75)
            paste(c, text_block(k, 36, INK), (160, y), a, rise=0)
            paste(c, text_block(v, 36, ACCENT, "semibold"), (960, y), a, rise=0)
            if base:
                paste(c, text_block(base, 34, MUTED), (1480, y + 2), a, rise=0)
            line(c, (160, y + 54), (W - 160, y + 54), RULE, 1, a)
        return c

    return Scene("10 Risk card", draw, min_duration=2.4 + len(rows) * 0.75 + 3)


def scene_10_scorecard(E: dict) -> Scene:
    rep, tested = E["scorecard"]
    tiles = E["scorecard_rows"]
    colors = {"reproduced": (GREEN_SOFT, GREEN), "not reproduced": (RED_SOFT, RED), "not tested": (GREY_SOFT, MUTED)}

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Scorecard", f"{rep} of {tested} tested human results reproduced by Haiku 5.5", t, size=62)
        paste(c, text_block("Rule: the humans' direction and a bootstrap interval that excludes zero; 8 pool sessions.",
                            36, MUTED, max_width=W - 240), (120, y0 - 10), fade(t, 0.8))
        tw, th, gap = 400, 190, 26
        x0 = (W - (4 * tw + 3 * gap)) // 2
        for i, (n, name, state) in enumerate(tiles):
            a = fade(t, 2.0 + i * 0.7)
            x = x0 + (i % 4) * (tw + gap)
            y = y0 + 70 + (i // 4) * (th + gap)
            soft, strong = colors[state]
            rounded(c, (x, y, x + tw, y + th), soft, 20, alpha=a)
            short = name.replace("Public reports as altruistic punishment", "Altruistic public reports").replace("Cartel detection through reports", "Detection through reports")
            paste(c, text_block(f"{n}. {short}", 36, INK, "semibold", max_width=tw - 50), (x + 24, y + 22), a, rise=0)
            paste(c, text_block(state, 36, strong, "bold"), (x + 24, y + th - 70), a, rise=0)
        paste(c, text_block(R["scorecard_caveat"], 38, INK, max_width=W - 240), (120, y0 + 70 + 2 * th + gap + 40), fade(t, 9.0))
        return c

    return Scene("11 Scorecard", draw, min_duration=14.0)


def scene_11_limits(E: dict) -> Scene:
    items = [
        ("A laboratory game, not a market", "thirteen prices, two firms, a stylised authority"),
        ("Points, not money", "the agents' fines are points in a prompt; the students played for euros"),
        ("Haiku's fine effect is not robust to rewording", "a paraphrase cuts its cartel incidence from 0.40 to 0.02"),
        ("The screen has no human baseline", "the threshold curve was never run with people"),
    ]

    def draw(t: float) -> Image.Image:
        c = new_canvas()
        y0 = header(c, "Limits", "What the result does not establish", t)
        bullet_list(c, items, y0 + 10, t, 1.2, 2.4, color=MUTED, gap=170, head_size=48)
        return c

    return Scene("12 Limits", draw, min_duration=13.0)


def scene_12_close(E: dict) -> Scene:
    def draw(t: float) -> Image.Image:
        c = new_canvas()
        paste(c, text_block("An authority has to choose where the line lies, not only whether to publish it.", 52, ACCENT, "semibold",
                            max_width=W - 300, align="center"), (W // 2, 200), fade(t, 0.5), anchor="mt")
        line(c, (W // 2 - 260, 470), (W // 2 + 260, 470), RULE, 3, fade(t, 5.0))
        paste(c, text_block("CartelBench", 40, ACCENT, "semibold"), (W // 2, 510), fade(t, 5.4), anchor="mt")
        paste(c, text_block("Same Game, Different Players: A Human-Calibrated Testbed for Cartel Enforcement on LLM Pricing Agents",
                            48, INK, "bold", max_width=W - 300, align="center", spacing=1.15), (W // 2, 570), fade(t, 5.6), anchor="mt")
        paste(c, text_block("Julian Mundelein, Independent, Hong Kong", 42, INK, align="center"), (W // 2, 740), fade(t, 6.4), anchor="mt")
        paste(c, text_block("AI Collusion Research Sprint, Apart Research, October 2026", 38, MUTED, align="center"), (W // 2, 805), fade(t, 6.8), anchor="mt")
        paste(c, text_block("github.com/julianmundelein-beep/2026-ai-collusion-sprint", 44, ACCENT, "semibold", align="center"), (W // 2, 900), fade(t, 7.4), anchor="mt")
        return c

    return Scene("13 Close", draw, min_duration=12.0)


def build_scenes() -> list[Scene]:
    E = evidence_numbers()
    return [f(E) for f in (scene_00_intro, scene_01_title, scene_02_game, scene_03_humans, scene_04_testbed, scene_05_table, scene_06_line,
                           scene_07_random, scene_08_stakes, scene_09_risk_card, scene_10_scorecard, scene_11_limits, scene_12_close)]


# ----------------------------------------------------------------------------
# Durations, voice, timeline
# ----------------------------------------------------------------------------


def count_words(scenes: list[Scene]) -> None:
    """Count the prose words every scene shows (its last frame) into Scene.words."""
    global _WORDS
    for s in scenes:
        _WORDS = set()
        s.draw(10_000.0)
        # numbers, ticks and ids are read at a glance, not as prose
        s.words = sum(1 for x in _WORDS for w in x.split() if re.search(r"[A-Za-z]{2}", w))
    _WORDS = None


def ffmpeg_exe() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def media_duration(path: Path) -> float:
    """Length of an audio file in seconds, read with the bundled ffmpeg (no ffprobe needed)."""
    out = subprocess.run([ffmpeg_exe(), "-i", str(path), "-f", "null", "-"], capture_output=True, text=True).stderr
    times = re.findall(r"time=(\d+):(\d\d):(\d\d\.\d+)", out)
    if not times:
        raise SystemExit(f"cannot read the length of {path}")
    h, m, s = times[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def voice_files(scenes: list[Scene]) -> list[Path | None]:
    return [p if (p := VOICE_DIR / f"{i + 1:02d}.mp3").is_file() else None for i in range(len(scenes))]


def plan_durations(scenes: list[Scene], voices: list[Path | None]) -> None:
    """Scene length: the longest of the reading rule, the last element plus 3 s, and the voice file plus its tail."""
    for s, v in zip(scenes, voices):
        reading = 3.0 + 0.35 * s.words
        s.duration = max(reading, s.min_duration + 3.0)
        if v is not None:
            s.duration = max(s.duration, media_duration(v) + VOICE_TAIL)
        s.duration = math.ceil(s.duration * 2) / 2


def timeline(scenes: list[Scene]) -> list[tuple[float, float]]:
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
        return scenes[i].draw(scenes[i].duration)
    if len(active) == 1:
        i, lt = active[0]
        return scenes[i].draw(lt)
    (i, lt_i), (j, lt_j) = active[0], active[1]
    return Image.blend(scenes[i].draw(lt_i), scenes[j].draw(lt_j), ease(lt_j / XFADE))


def mix_voice(video: Path, voices: list[Path | None], tl: list[tuple[float, float]], out: Path) -> None:
    """Lay the voice files under the silent video at their scene starts."""
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(video)]
    parts, n = [], 0
    for v, (s0, _) in zip(voices, tl):
        if v is None:
            continue
        cmd += ["-i", str(v)]
        n += 1
        parts.append(f"[{n}:a]aresample=48000,adelay={int(s0 * 1000)}|{int(s0 * 1000)}[a{n}]")
    filt = ";".join(parts) + ";" + "".join(f"[a{k}]" for k in range(1, n + 1)) + f"amix=inputs={n}:normalize=0:dropout_transition=0[mix]"
    cmd += ["-filter_complex", filt, "-map", "0:v:0", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)]
    if subprocess.run(cmd).returncode != 0:
        raise SystemExit("ffmpeg failed while mixing the voice")


def render(scenes: list[Scene], out: Path, voices: list[Path | None]) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tl = timeline(scenes)
    n_frames = int(round(total_duration(scenes) * FPS))
    silent = out.with_name(out.stem + "_silent.mp4") if any(voices) else out
    cmd = [
        ffmpeg_exe(), "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(silent),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for n in range(n_frames):
        proc.stdin.write(frame_at(scenes, tl, n / FPS).convert("RGB").tobytes())
        if n % (FPS * 15) == 0:
            print(f"  {n / FPS:6.1f} s of {n_frames / FPS:.1f} s", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    if any(voices):
        mix_voice(silent, voices, tl, out)
        silent.unlink()
    print(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {n_frames / FPS:.1f} s)")


def stills(scenes: list[Scene]) -> None:
    """Three stills at the end of a build, for checking legibility."""
    STILLS_DIR.mkdir(parents=True, exist_ok=True)
    for old in STILLS_DIR.glob("*.png"):
        old.unlink()
    picks = {"06_table.png": "06 Table", "07_line.png": "07 Line", "08_random.png": "08 Random"}
    for fname, name in picks.items():
        s = next(x for x in scenes if x.name == name)
        s.draw(s.duration - XFADE - 0.1).convert("RGB").save(STILLS_DIR / fname, optimize=True)
        print(f"wrote {STILLS_DIR / fname}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stills-only", action="store_true")
    ap.add_argument("--timeline", action="store_true", help="print the scene times and exit")
    ap.add_argument("--no-voice", action="store_true", help="ignore video/voice/ even if files exist")
    ap.add_argument("--out", type=Path, default=OUT_DIR / OUT_NAME)
    args = ap.parse_args()

    scenes = build_scenes()
    count_words(scenes)
    voices = [None] * len(scenes) if args.no_voice else voice_files(scenes)
    plan_durations(scenes, voices)
    for s, (s0, s1), v in zip(scenes, timeline(scenes), voices):
        print(f"{s.name:14s} {s0:6.1f} to {s1:6.1f} s  ({s.duration:.1f} s, {s.words} words{', voice ' + v.name if v else ''})")
    print(f"total {total_duration(scenes):.1f} s")
    if args.timeline:
        return
    stills(scenes)
    if args.stills_only:
        return
    render(scenes, args.out, voices)


if __name__ == "__main__":
    main()
