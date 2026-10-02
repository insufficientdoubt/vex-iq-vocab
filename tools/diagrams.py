#!/usr/bin/env python3
"""Draw the concept diagrams for vocab terms that aren't a single part.

Usage: python3 tools/diagrams.py        (writes images/<ID>.png for each diagram below)
Labels are English only, because images also appear in review materials. Needs Pillow.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
S = 1200                      # drawing size; saved at half size for smooth edges
PART, EDGE, HOLE = "#b9bec4", "#2b2f33", "#ffffff"
BLUE, ORANGE, TEXT, FAINT = "#0a6cc4", "#f07a10", "#1b1f24", "#c9ced4"


def font(size, bold=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    for d in ["/System/Library/Fonts/Supplemental/", "/Library/Fonts/"]:
        if Path(d + name).exists():
            return ImageFont.truetype(d + name, size)
    return ImageFont.load_default()


def canvas():
    im = Image.new("RGB", (S, S), "white")
    return im, ImageDraw.Draw(im)


def text(d, xy, s, size=56, bold=False, fill=TEXT, anchor="mm"):
    d.text(xy, s, font=font(size, bold), fill=fill, anchor=anchor)


def beam(d, x, y, cols, rows, p, fill=PART):
    """Beam/plate with a hole grid. Returns hole centers."""
    d.rounded_rectangle((x, y, x + cols * p, y + rows * p), radius=p * 0.45, fill=fill, outline=EDGE, width=6)
    centers = [(x + p / 2 + c * p, y + p / 2 + r * p) for r in range(rows) for c in range(cols)]
    for cx, cy in centers:
        rr = p * 0.3
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=HOLE, outline=EDGE, width=5)
    return centers


def dim(d, x1, y1, x2, y2, color=BLUE, w=7, head=26):
    """Double-headed dimension arrow."""
    d.line((x1, y1, x2, y2), fill=color, width=w)
    ang = math.atan2(y2 - y1, x2 - x1)
    for (px, py), a in [((x1, y1), ang), ((x2, y2), ang + math.pi)]:
        pts = [(px, py),
               (px + head * math.cos(a + 0.45), py + head * math.sin(a + 0.45)),
               (px + head * math.cos(a - 0.45), py + head * math.sin(a - 0.45))]
        d.polygon(pts, fill=color)


def dashed(d, x1, y1, x2, y2, color=BLUE, w=4, dash=16):
    n = int(math.hypot(x2 - x1, y2 - y1) // dash)
    for i in range(0, n, 2):
        a, b = i / n, min((i + 1) / n, 1)
        d.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a, x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=color, width=w)


def pitch():
    im, d = canvas()
    p = 180
    holes = beam(d, 150, 380, 5, 1, p)
    (ax, ay), (bx, _) = holes[0], holes[1]
    for x in (ax, bx):
        dashed(d, x, ay, x, 250)
    dim(d, ax, 270, bx, 270)
    text(d, (ax - 20, 200), "1 pitch = 12.7 mm", 60, True, BLUE, anchor="lm")
    text(d, (600, 640), "distance from one hole to the next", 44)
    # shaft measured in pitch
    x0, y = 150, 840
    d.rounded_rectangle((x0, y, x0 + 4 * p, y + 34), radius=8, fill="#d5d8dc", outline=EDGE, width=5)
    for i in range(5):
        d.line((x0 + i * p, y + 50, x0 + i * p, y + 80), fill=BLUE, width=6)
    for i in range(4):
        text(d, (x0 + i * p + p / 2, y + 105), str(i + 1), 44, True, BLUE)
    text(d, (x0 + 4 * p + 40, y + 17), "4x pitch", 50, True, anchor="lm")
    text(d, (x0 + 4 * p + 40, y + 77), "shaft", 50, True, anchor="lm")
    return im


def hole_count():
    im, d = canvas()
    p = 120
    x0, y0 = 120, 210
    holes = beam(d, x0, y0, 8, 1, p)
    for i, (cx, cy) in enumerate(holes):
        text(d, (cx, y0 - 45), str(i + 1), 44, True, BLUE)
    dim(d, x0, y0 + p + 45, x0 + 8 * p, y0 + p + 45)
    text(d, (x0 + 4 * p, y0 + p + 100), "8 holes long", 46, fill=BLUE)
    text(d, (x0 + 4 * p, 90), "1x8 beam", 64, True)
    # plate
    px, py = 200, 640
    beam(d, px, py, 4, 4, p, fill="#8e949b")
    dim(d, px, py - 40, px + 4 * p, py - 40)
    text(d, (px + 2 * p, py - 85), "4", 50, True, BLUE)
    dim(d, px - 40, py, px - 40, py + 4 * p)
    text(d, (px - 90, py + 2 * p), "4", 50, True, BLUE)
    text(d, (px + 4 * p + 60, py + 2 * p - 40), "4x4", 70, True, anchor="lm")
    text(d, (px + 4 * p + 60, py + 2 * p + 40), "plate", 70, True, anchor="lm")
    return im


def offset():
    im, d = canvas()
    p = 160
    xs = [120 + p / 2 + i * p for i in range(7)]
    text(d, (600, 120), "Holes line up with the grid", 50, True)
    beam(d, 120 + p, 330 - p / 2, 4, 1, p)
    text(d, (600, 560), "Offset: holes are shifted off the grid", 50, True, ORANGE)
    shift = p / 2
    holes = beam(d, 120 + p + shift, 760 - p / 2, 4, 1, p, fill="#f3b27a")
    gx = xs[1]
    dashed(d, gx, 760, gx, 900, ORANGE)
    dashed(d, holes[0][0], 760, holes[0][0], 900, ORANGE)
    dim(d, gx, 900, holes[0][0], 900, ORANGE)
    text(d, (600, 1010), "shifted", 46, fill=ORANGE)
    for gy in (330, 760):                       # grid dots on top, so they show inside the holes
        for x in xs:
            d.ellipse((x - 13, gy - 13, x + 13, gy + 13), fill=BLUE)
    return im


def travel():
    im, d = canvas()
    r = 130
    ground = 820
    circ = 2 * math.pi * r
    x1, x2 = 190, 190 + circ
    d.line((60, ground, S - 60, ground), fill=EDGE, width=6)
    for cx in (x1, x2):
        cy = ground - r
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#2b2f33")
        d.ellipse((cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62), fill=PART, outline=EDGE, width=4)
        d.rectangle((cx - 14, cy - 14, cx + 14, cy + 14), fill=HOLE, outline=EDGE, width=3)
        d.ellipse((cx - 20, ground - 40, cx + 20, ground), fill=ORANGE)   # mark on the tire
    # rotation arrow on first wheel
    cy = ground - r
    d.arc((x1 - r - 40, cy - r - 40, x1 + r + 40, cy + r + 40), start=200, end=330, fill=BLUE, width=8)
    a = math.radians(330)
    tip = (x1 + (r + 40) * math.cos(a), cy + (r + 40) * math.sin(a))
    d.polygon([tip, (tip[0] - 40, tip[1] - 6), (tip[0] - 14, tip[1] + 34)], fill=BLUE)
    text(d, (x2, ground - 2 * r - 60), "after 1 full turn", 44, fill=ORANGE)
    dashed(d, x1, ground, x1, ground + 110)
    dashed(d, x2, ground, x2, ground + 110)
    dim(d, x1, ground + 90, x2, ground + 90)
    text(d, ((x1 + x2) / 2, ground + 160), "travel", 64, True, BLUE)
    text(d, (600, 150), "How far a wheel rolls", 58, True)
    text(d, (600, 225), "in one full turn", 58, True)
    text(d, (600, 330), "A 200 mm travel wheel rolls 200 mm per turn.", 40)
    return im


def tooth_count():
    im, d = canvas()
    cx, cy, n = 600, 560, 12
    root, tip = 290, 360
    pts = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        step = 2 * math.pi / n
        for frac, rad in [(0.0, root), (0.18, tip), (0.42, tip), (0.6, root)]:
            a = a0 + step * frac - math.pi / 2
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill="#2f7fd0", outline=EDGE, width=6)
    d.ellipse((cx - 180, cy - 180, cx + 180, cy + 180), outline="#1d5ea3", width=6)
    d.rectangle((cx - 40, cy - 40, cx + 40, cy + 40), fill=HOLE, outline=EDGE, width=6)
    for i in range(n):
        a = 2 * math.pi * (i + 0.3) / n - math.pi / 2
        text(d, (cx + 430 * math.cos(a), cy + 430 * math.sin(a)), str(i + 1), 50, True, ORANGE)
    text(d, (600, 1110), "12 teeth = 12T", 70, True)
    return im


DIAGRAMS = {
    "pitch": pitch,
    "hole count (1x8, 2x4…)": hole_count,
    "offset": offset,
    "travel": travel,
    "tooth count": tooth_count,
}


def main():
    import csv
    ids = {r["term_en"]: r["id"] for r in csv.DictReader(open(ROOT / "data/vocab.csv", encoding="utf-8"))}
    for term, fn in DIAGRAMS.items():
        out = ROOT / "images" / f"{ids[term]}.png"
        fn().resize((S // 2, S // 2), Image.LANCZOS).quantize(colors=96, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
        print(f"{ids[term]}  {term}  → images/{out.name}")


if __name__ == "__main__":
    main()
