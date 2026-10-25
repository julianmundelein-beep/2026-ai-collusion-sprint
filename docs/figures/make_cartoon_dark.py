"""Dark-mode variant of the README cartoon (docs/figures/cartoon_dark.svg) from the hand-drawn cartoon.svg.

    python3 docs/figures/make_cartoon_dark.py

Swaps the paper, ink and wood colours of cartoon.svg for GitHub's dark theme and leaves shapes, text and the
animation untouched; the four model colours are the dark-mode hues of model_overview_dark.png, checked for contrast on the dark surface.
"""
from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC, OUT = HERE / "cartoon.svg", HERE / "cartoon_dark.svg"

# light -> dark; the order matters where one colour is a prefix of none (hex codes are distinct)
COLOURS = {
    "#fcfcfb": "#161b22",  # paper and white fills
    "#111": "#e6edf3",     # ink: outlines, eyes, text
    "#52514e": "#8b949e",  # posts, antennae, the authority's coat
    "#e8e6df": "#30363d",  # counters
    "#fff6cf": "#4a3f12",  # price boards
    "#dcefff": "#1f3a5a",  # the magnifying glass
    "#eb6834": "#e66b38",  # Haiku; the four model hues are those of model_overview_dark.png
    "#2a78d6": "#4489de",  # Sonnet
    "#16996a": "#21a06d",  # Qwen
    "#6250d6": "#8c7ce8",  # Llama
}


def main() -> None:
    svg = SRC.read_text(encoding="utf-8")
    for light, dark in COLOURS.items():
        svg = svg.replace(f'"{light}"', f'"{dark}"').replace(f":{light}", f":{dark}")
    # the picture's own background is the page's dark surface; the badge text stays light on the model hues
    svg = svg.replace('<rect width="1200" height="430" rx="6" fill="#161b22"/>', '<rect width="1200" height="430" rx="6" fill="#0d1117"/>')
    svg = svg.replace("fill:#161b22;text-anchor:middle;font-weight:bold", "fill:#e6edf3;text-anchor:middle;font-weight:bold")
    svg = svg.replace("<!-- Hand-drawn SVG", "<!-- Dark-mode variant written by docs/figures/make_cartoon_dark.py from cartoon.svg. Hand-drawn SVG")
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
