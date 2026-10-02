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


# ---------- coding concept cards ----------------------------------------------------------
GREEN, RED, CODEBG, KEYWORD = "#2f9e44", "#d6336c", "#f4f6f8", "#7048e8"


def mono(size, bold=False):
    for f, i in [("/System/Library/Fonts/Menlo.ttc", 1 if bold else 0),
                 ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 0)]:
        if Path(f).exists():
            return ImageFont.truetype(f, size, index=i)
    return ImageFont.load_default()


def code_card(d, lines, top=330, size=50, marks=(), keywords=()):
    """Draw Python lines in an editor-style panel. marks = [(line, col_from, col_to, color)] highlights."""
    f = mono(size)
    cw, lh = f.getlength("M"), size * 1.55
    width = max(len(l) for l in lines) * cw + 120
    x0 = (S - width) / 2
    d.rounded_rectangle((x0, top, x0 + width, top + len(lines) * lh + 70), radius=24, fill=CODEBG, outline=FAINT, width=4)
    x, y = x0 + 60, top + 35
    for (ln, a, b, color) in marks:
        d.rounded_rectangle((x + a * cw - 6, y + ln * lh - 6, x + b * cw + 6, y + ln * lh + size + 10), radius=10, fill=color)
    for i, line in enumerate(lines):
        d.text((x, y + i * lh), line, font=f, fill=TEXT)
        for kw in keywords:                                  # recolor keywords
            j = line.find(kw)
            if j >= 0 and (j == 0 or not line[j - 1].isalnum()):
                d.text((x + j * cw, y + i * lh), kw, font=mono(size, True), fill=KEYWORD)
    return x, y, cw, lh


def title(d, s, sub=None):
    """Deliberately draws nothing: an image that names its own term would give away quiz answers."""


def fit(im, margin=70):
    """Crop to the drawing and scale it to fill the square, so small drawings are readable on cards."""
    box = Image.eval(im.convert("L"), lambda v: 255 - v).getbbox()
    if not box:
        return im
    part = im.crop(box)
    k = min((S - 2 * margin) / part.width, (S - 2 * margin) / part.height, 1.6)
    part = part.resize((int(part.width * k), int(part.height * k)), Image.LANCZOS)
    out = Image.new("RGB", (S, S), "white")
    out.paste(part, ((S - part.width) // 2, (S - part.height) // 2))
    return out


def while_loop():
    im, d = canvas()
    title(d, "while", "repeats as long as the condition is True")
    code_card(d, ["while bumper_1.pressing():", "    intake.spin(FORWARD)", "intake.stop()"], top=380,
              marks=[(0, 6, 25, "#d3f9d8")], keywords=["while"])
    text(d, (600, 850), "green part = the condition", 42, fill=GREEN)
    text(d, (600, 920), "the indented line repeats", 42)
    return im


def indentation():
    im, d = canvas()
    title(d, "indentation", "spaces that show what is inside")
    x, y, cw, lh = code_card(d, ["while True:", "    drivetrain.drive(FORWARD)", "    wait(1, SECONDS)", "brain.screen.print(\"done\")"],
                             top=380, marks=[(1, 0, 4, "#ffd8a8"), (2, 0, 4, "#ffd8a8")], keywords=["while", "True"])
    text(d, (600, 930), "orange = 4 spaces → inside the loop", 42, fill=ORANGE)
    return im


def colon():
    im, d = canvas()
    title(d, "colon  :", "ends the first line of a loop, if or function")
    code_card(d, ["if bumper_1.pressing():", "    drivetrain.stop()", "", "while True:", "", "def drive_square():"], top=330,
              marks=[(0, 22, 23, "#ffc9c9"), (3, 10, 11, "#ffc9c9"), (5, 18, 19, "#ffc9c9")], keywords=["if", "while", "True", "def"])
    return im


def import_():
    im, d = canvas()
    title(d, "import", "load extra code into your program")
    code_card(d, ["from vex import *", "import random", "", "n = random.randint(1, 3)"], top=380,
              marks=[(0, 9, 15, "#e5dbff"), (1, 0, 6, "#e5dbff")], keywords=["from", "import"])
    text(d, (600, 960), "VEXcode adds the first line for you", 42)
    return im


def string():
    im, d = canvas()
    title(d, "string", "text, written inside quotes")
    code_card(d, ["name = \"Ready!\"", "brain.screen.print(\"Score: \")"], top=420,
              marks=[(0, 7, 15, "#d3f9d8"), (1, 19, 28, "#d3f9d8")])
    text(d, (600, 800), "\"5\" is text     5 is a number", 46, True, BLUE)
    return im


def int_float():
    im, d = canvas()
    title(d, "integer / float", "two kinds of numbers")
    code_card(d, ["count = 3", "distance = 3.5"], top=400, size=60, marks=[(0, 8, 9, "#d0ebff"), (1, 11, 14, "#ffd8a8")])
    text(d, (420, 780), "integer", 56, True, BLUE)
    text(d, (420, 845), "whole number", 40, fill=BLUE)
    text(d, (800, 780), "float", 56, True, ORANGE)
    text(d, (800, 845), "has a decimal point", 40, fill=ORANGE)
    return im


def true_false():
    im, d = canvas()
    title(d, "True / False", "the only two Boolean values")
    for cx, word, color in [(330, "True", GREEN), (870, "False", RED)]:
        d.rounded_rectangle((cx - 220, 420, cx + 220, 820), radius=40, fill=color)
        if word == "True":
            d.line([(cx - 70, 560), (cx - 15, 615), (cx + 85, 500)], fill="white", width=26, joint="curve")
        else:
            d.line((cx - 65, 495, cx + 65, 625), fill="white", width=26)
            d.line((cx - 65, 625, cx + 65, 495), fill="white", width=26)
        text(d, (cx, 730), word, 80, True, "white")
    text(d, (600, 960), "Is the bumper pressed?  →  True or False", 44)
    return im


def boxes_flow(d, steps, top=330, h=120, color=BLUE):
    for i, s in enumerate(steps):
        y = top + i * (h + 60)
        d.rounded_rectangle((260, y, 940, y + h), radius=28, fill="#e7f1fb", outline=color, width=6)
        text(d, (330, y + h / 2), str(i + 1), 60, True, color)
        text(d, (390, y + h / 2), s, 50, anchor="lm")
        if i < len(steps) - 1:
            d.line((600, y + h, 600, y + h + 50), fill=color, width=8)
            d.polygon([(580, y + h + 30), (620, y + h + 30), (600, y + h + 56)], fill=color)


def algorithm():
    im, d = canvas()
    title(d, "algorithm", "a step-by-step plan")
    boxes_flow(d, ["Find the ball", "Drive to it", "Close the claw", "Score it"], top=320)
    return im


def pseudocode():
    im, d = canvas()
    title(d, "pseudocode", "a plan in plain words, not real code")
    d.rounded_rectangle((180, 330, 1020, 900), radius=24, fill="#fff9db", outline="#f0c419", width=5)
    for i in range(7):
        d.line((210, 430 + i * 72, 990, 430 + i * 72), fill="#f3e3a1", width=3)
    for i, (indent, line) in enumerate([(0, "repeat 4 times:"), (1, "drive forward 300 mm"), (1, "turn right 90°"),
                                         (0, "if I see a ball:"), (1, "close the claw"), (0, "go home")]):
        text(d, (240 + indent * 70, 405 + i * 72), line, 46, anchor="lm")
    return im


def bug():
    im, d = canvas()
    title(d, "bug", "a mistake that makes the robot do the wrong thing")
    code_card(d, ["drivetrain.drive_for(FORWARD, 300, MM)", "drivetrain.turn_for(LEFT, 90, DEGREES)", "drivetrain.drive_for(FORWARD, 300, MM)"],
              top=340, size=36, marks=[(1, 20, 24, "#ffc9c9")])
    text(d, (600, 610), "should be RIGHT!", 50, True, RED)
    # plan vs. what happened
    sx, sy = 600, 1050
    d.line((sx, sy, sx, 830), fill=GREEN, width=10)
    dashed(d, sx, 830, sx + 220, 830, GREEN, w=10, dash=22)
    d.line((sx, 830, sx - 220, 830), fill=RED, width=10)
    d.polygon([(sx + 250, 830), (sx + 215, 810), (sx + 215, 850)], fill=GREEN)
    d.polygon([(sx - 250, 830), (sx - 215, 810), (sx - 215, 850)], fill=RED)
    text(d, (sx + 230, 780), "planned", 40, True, GREEN)
    text(d, (sx - 230, 780), "actual", 40, True, RED)
    return im


def sensor():
    """2x2 grid of the sensor part photos already in images/."""
    im, _ = canvas()
    for i, pid in enumerate(["BLD-013", "BLD-014", "BLD-015", "BLD-016"]):
        p = ROOT / "images" / f"{pid}.png"
        part = Image.open(p).convert("RGB").resize((560, 560))
        im.paste(part, (20 + (i % 2) * 600, 20 + (i // 2) * 600))
    return im


DIAGRAMS = {
    "pitch": pitch,
    "hole count (1x8, 2x4…)": hole_count,
    "offset": offset,
    "travel": travel,
    "tooth count": tooth_count,
    "while": while_loop,
    "indentation": indentation,
    "colon": colon,
    "import": import_,
    "string": string,
    "integer / float": int_float,
    "True / False": true_false,
    "algorithm": algorithm,
    "pseudocode": pseudocode,
    "bug": bug,
    "sensor": sensor,
}


def main():
    import csv
    ids = {r["term_en"]: r["id"] for r in csv.DictReader(open(ROOT / "data/vocab.csv", encoding="utf-8"))}
    for term, fn in DIAGRAMS.items():
        out = ROOT / "images" / f"{ids[term]}.png"
        im = fn()
        if ids[term].startswith("CODE-") and term != "sensor":
            im = fit(im)
        im.resize((S // 2, S // 2), Image.LANCZOS).quantize(colors=96, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
        print(f"{ids[term]}  {term}  → images/{out.name}")


if __name__ == "__main__":
    main()
