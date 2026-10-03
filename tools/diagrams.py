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


# ---------- engineering concept drawings ---------------------------------------------------
# Labels never name the term itself (or its aka), so the pictures work in quizzes.
DARK, LIGHTBLUE, LIGHTORANGE, GROUND = "#2b2f33", "#e7f1fb", "#fde3cc", "#8a9099"


def arrow(d, x1, y1, x2, y2, color=BLUE, w=10, head=34):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang)
    d.line((x1, y1, bx, by), fill=color, width=w)
    d.polygon([(x2, y2), (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45)),
               (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))], fill=color)


def spin(d, cx, cy, r, start, end, color=BLUE, w=8, head=30):
    """Curved arrow around (cx, cy) from angle start to end (degrees, clockwise if end > start)."""
    lo, hi = min(start, end), max(start, end)
    d.arc((cx - r, cy - r, cx + r, cy + r), start=lo, end=hi, fill=color, width=w)
    a = math.radians(end)
    tip = (cx + r * math.cos(a), cy + r * math.sin(a))
    sgn = 1 if end > start else -1
    tan = a + sgn * math.pi / 2
    back = (tip[0] - head * math.cos(tan), tip[1] - head * math.sin(tan))
    nx, ny = math.cos(a) * head * 0.45, math.sin(a) * head * 0.45
    d.polygon([tip, (back[0] + nx, back[1] + ny), (back[0] - nx, back[1] - ny)], fill=color)


def gear(d, cx, cy, r, n, fill="#2f7fd0", hole=True):
    pts, step = [], 2 * math.pi / n
    for i in range(n):
        for frac, rad in [(0.0, r - 22), (0.18, r + 18), (0.42, r + 18), (0.6, r - 22)]:
            a = step * (i + frac) - math.pi / 2
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=fill, outline=EDGE, width=5)
    if hole:
        d.rectangle((cx - 22, cy - 22, cx + 22, cy + 22), fill=HOLE, outline=EDGE, width=5)


def poly(d, pts, fill=PART, outline=EDGE, width=5):
    d.polygon(pts, fill=fill, outline=outline, width=width)


def rot_rect(cx, cy, w, h, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]


def bar(d, x1, y1, x2, y2, w=44, fill=PART):
    """A beam between two pivot points, with pivot holes at the ends."""
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = math.hypot(x2 - x1, y2 - y1)
    poly(d, rot_rect((x1 + x2) / 2, (y1 + y2) / 2, L + w, w, ang), fill)
    for x, y in ((x1, y1), (x2, y2)):
        d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=HOLE, outline=EDGE, width=4)


def wheel_side(d, cx, cy, r, tire=DARK):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=tire)
    d.ellipse((cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6), fill=PART, outline=EDGE, width=4)
    d.rectangle((cx - 10, cy - 10, cx + 10, cy + 10), fill=HOLE, outline=EDGE, width=3)


def ground(d, y, x1=80, x2=S - 80):
    d.line((x1, y, x2, y), fill=GROUND, width=8)
    for x in range(int(x1), int(x2), 50):
        d.line((x, y + 6, x - 24, y + 32), fill=GROUND, width=4)


def robot_side(d, x, y, w, h, r=70, wheels=2):
    """Side view: body box with its bottom at y, wheels below. Returns the ground line y."""
    d.rounded_rectangle((x, y - h, x + w, y), radius=16, fill=PART, outline=EDGE, width=6)
    gy = y + r * 0.35 + r
    xs = [x + r * 0.9, x + w - r * 0.9] if wheels == 2 else [x + w / 2]
    for cx in xs:
        wheel_side(d, cx, gy - r, r)
    return gy


def robot_top(d, cx, cy, w, h, fill=PART, front=True, outline=EDGE):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=18, fill=fill, outline=outline, width=6)
    if front:
        d.polygon([(cx, cy - h / 2 + 18), (cx - 30, cy - h / 2 + 62), (cx + 30, cy - h / 2 + 62)], fill=BLUE)


def omni_top(d, cx, cy, deg, w=50, h=150):
    poly(d, rot_rect(cx, cy, w, h, deg), DARK)
    a = math.radians(deg)
    for t in (-0.32, 0, 0.32):                     # rollers across the wheel
        px, py = cx - math.sin(a) * h * t, cy + math.cos(a) * h * t
        d.line((px - math.cos(a) * w * 0.42, py - math.sin(a) * w * 0.42,
                px + math.cos(a) * w * 0.42, py + math.sin(a) * w * 0.42), fill="#c9ced4", width=6)


def ball(d, cx, cy, r=45, color=ORANGE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color, outline=EDGE, width=5)


def field(d, x0, y0, n=6, cell=150):
    d.rectangle((x0, y0, x0 + n * cell, y0 + n * cell), fill="#f1f3f5", outline=EDGE, width=6)
    for i in range(1, n):
        d.line((x0 + i * cell, y0, x0 + i * cell, y0 + n * cell), fill="#d5d9de", width=3)
        d.line((x0, y0 + i * cell, x0 + n * cell, y0 + i * cell), fill="#d5d9de", width=3)


def controller_icon(d, cx, cy, k=1.0, fill="#4fb3e3"):
    w, h = 300 * k, 170 * k
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 3), radius=60 * k, fill=fill, outline=EDGE, width=5)
    for sx in (-1, 1):
        d.ellipse((cx + sx * 90 * k - 30 * k, cy - 30 * k, cx + sx * 90 * k + 30 * k, cy + 30 * k), fill="white", outline=EDGE, width=4)
        poly(d, [(cx + sx * 150 * k, cy), (cx + sx * 110 * k, cy + 95 * k), (cx + sx * 40 * k, cy + 40 * k)], fill, EDGE, 0)


def axes(d, x0, y0, x1, y1):
    arrow(d, x0, y0, x1 + 30, y0, DARK, 6, 26)
    arrow(d, x0, y0, x0, y1 - 30, DARK, 6, 26)


# --- drivetrains ---
def chassis():
    im, d = canvas()
    beam(d, 260, 260, 9, 1, 75)
    beam(d, 260, 860, 9, 1, 75)
    for x in (260, 860):
        beam(d, x, 335, 1, 7, 75)
    beam(d, 335, 560, 7, 1, 75, fill="#8e949b")
    for x in (200, 935):
        for y in (330, 720):
            d.rounded_rectangle((x, y, x + 65, y + 150), radius=14, fill=DARK)
    return im


def holonomic_drive():
    im, d = canvas()
    d.rounded_rectangle((380, 380, 820, 820), radius=30, fill=PART, outline=EDGE, width=6)
    for cx, cy, deg in [(600, 360, 90), (600, 840, 90), (360, 600, 0), (840, 600, 0)]:
        omni_top(d, cx, cy, deg)
    for k in range(8):
        a = math.radians(k * 45)
        arrow(d, 600 + 110 * math.cos(a), 600 + 110 * math.sin(a), 600 + 200 * math.cos(a), 600 + 200 * math.sin(a), ORANGE, 9, 30)
    return im


def omni_directional():
    im, d = canvas()
    for (x, y) in [(240, 320), (960, 320), (240, 880), (960, 880), (600, 220), (600, 980), (180, 600), (1020, 600)]:
        robot_top(d, x, y, 150, 150, fill="#eef0f2", outline=FAINT)
        dashed(d, 600, 600, x, y, ORANGE, 6)
    robot_top(d, 600, 600, 220, 220)
    return im


def footprint():
    im, d = canvas()
    poly(d, [(300, 300), (900, 300), (900, 900), (300, 900)], "#fde3cc", ORANGE, 6)
    d.rounded_rectangle((380, 380, 820, 820), radius=20, fill=PART, outline=EDGE, width=6)
    for x in (300, 900):
        for y in (300, 900):
            d.rounded_rectangle((x - 40, y - 85, x + 40, y + 85), radius=14, fill=DARK)
            d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=ORANGE)
    dim(d, 300, 1030, 900, 1030, ORANGE)
    dim(d, 1050, 300, 1050, 900, ORANGE)
    return im


def ground_clearance():
    im, d = canvas()
    d.rounded_rectangle((260, 380, 940, 640), radius=20, fill=PART, outline=EDGE, width=6)
    for cx in (360, 840):
        wheel_side(d, cx, 720, 150)
    ground(d, 870)
    dashed(d, 560, 640, 760, 640, ORANGE, 5)
    dim(d, 660, 650, 660, 862, ORANGE)
    return im


# --- manipulators ---
def shield():
    im, d = canvas()
    gy = robot_side(d, 330, 760, 520, 260, 80)
    ground(d, gy)
    poly(d, [(290, 430), (890, 430), (890, 470), (290, 470)], "#4fb3e3")
    for bx, by, ax, ay in [(470, 230, 380, 120), (720, 210, 820, 100)]:
        ball(d, bx, by, 50)
        arrow(d, bx, by + 70, bx, 400, DARK, 6, 26)
        arrow(d, bx, 400, ax, ay + 40, ORANGE, 8, 30)
    return im


def game_piece_slide():
    im, d = canvas()
    gy = robot_side(d, 140, 820, 420, 300, 80)
    ground(d, gy)
    poly(d, [(520, 470), (960, 690), (960, 730), (520, 510)], "#4fb3e3")
    d.rectangle((930, 730, 1110, gy), fill="#e9ecef", outline=EDGE, width=6)
    ball(d, 650, 470, 48)
    arrow(d, 720, 470, 880, 560, ORANGE, 8, 30)
    return im


def basket():
    im, d = canvas()
    gy = robot_side(d, 260, 840, 680, 220, 85)
    ground(d, gy)
    poly(d, [(330, 360), (870, 360), (830, 620), (370, 620)], "#dbe9f7", BLUE, 8)
    for x, y in [(470, 545), (600, 545), (730, 545), (535, 450), (665, 450)]:
        ball(d, x, y, 55)
    return im


def outtake():
    im, d = canvas()
    robot_top(d, 600, 860, 520, 360, front=False)
    for cx, s, e in [(420, 30, 330), (780, 150, 210)]:
        d.ellipse((cx - 85, 545, cx + 85, 715), fill=DARK)
        d.ellipse((cx - 40, 590, cx + 40, 670), fill=PART, outline=EDGE, width=4)
    spin(d, 420, 630, 125, 200, 320, ORANGE)
    spin(d, 780, 630, 125, 340, 220, ORANGE)
    ball(d, 600, 410, 80)
    arrow(d, 600, 300, 600, 110, ORANGE, 12, 44)
    return im


def conveyor():
    im, d = canvas()
    a = math.radians(-35)
    x1, y1, x2, y2 = 260, 900, 940, 900 + 680 * math.tan(a)
    for x, y in ((x1, y1), (x2, y2)):
        d.ellipse((x - 70, y - 70, x + 70, y + 70), fill=PART, outline=EDGE, width=6)
    nx, ny = -math.sin(a) * 70, math.cos(a) * 70
    d.line((x1 + nx, y1 - ny, x2 + nx, y2 - ny), fill=DARK, width=16)
    d.line((x1 - nx, y1 + ny, x2 - nx, y2 + ny), fill=DARK, width=16)
    for t in (0.2, 0.5, 0.8):
        px, py = x1 + (x2 - x1) * t + nx, y1 + (y2 - y1) * t - ny
        d.line((px, py, px + nx * 1.1, py - ny * 1.1), fill=ORANGE, width=14)
        ball(d, px + nx * 0.9 + 60 * math.cos(a), py - ny * 0.9 + 60 * math.sin(a) - 20, 42)
    arrow(d, 420, 640, 700, 640 + 280 * math.tan(a), BLUE, 10, 36)
    return im


def claw_jaws(d, pivots, angles, length=330, fill=PART):
    for (px, py), ang in zip(pivots, angles):
        a = math.radians(ang)
        bar(d, px, py, px + length * math.cos(a), py + length * math.sin(a), 46, fill)


def single_sided_claw():
    im, d = canvas()
    d.rectangle((300, 820, 900, 900), fill=PART, outline=EDGE, width=6)
    claw_jaws(d, [(420, 780)], [-90])                    # fixed side
    claw_jaws(d, [(780, 780)], [-112], fill="#f3b27a")    # moving side
    spin(d, 780, 780, 210, 248, 228, ORANGE)
    d.rectangle((480, 470, 620, 610), fill="#4fb3e3", outline=EDGE, width=6)
    return im


def double_sided_claw():
    im, d = canvas()
    gear(d, 510, 820, 90, 12, "#2f7fd0")
    gear(d, 690, 820, 90, 12, "#2f7fd0")
    claw_jaws(d, [(510, 820), (690, 820)], [-100, -80], 420, "#f3b27a")
    spin(d, 510, 820, 300, 262, 242, ORANGE)
    spin(d, 690, 820, 300, 278, 298, ORANGE)
    d.rectangle((530, 440, 670, 580), fill="#4fb3e3", outline=EDGE, width=6)
    return im


def roller_claw():
    im, d = canvas()
    for x in (330, 870):
        bar(d, x, 900, x, 420, 46)
    for cx, s, e in [(330, 160, 40), (870, 20, 140)]:
        d.ellipse((cx - 130, 290, cx + 130, 550), fill=DARK)
        d.ellipse((cx - 55, 365, cx + 55, 475), fill=PART, outline=EDGE, width=4)
    spin(d, 330, 420, 175, 140, 40, ORANGE)
    spin(d, 870, 420, 175, 40, 140, ORANGE)
    ball(d, 600, 330, 75, "#4fb3e3")
    arrow(d, 600, 440, 600, 760, BLUE, 12, 44)
    return im


def tower():
    im, d = canvas()
    gy = robot_side(d, 200, 860, 700, 140, 85)
    ground(d, gy)
    d.rectangle((420, 330, 520, 720), fill="#f3b27a", outline=ORANGE, width=8)
    bar(d, 470, 380, 980, 560, 44)
    gear(d, 470, 380, 60, 12, "#2f7fd0")
    return im


def linkage(d, base, length, ang_deg, gap=150, fill=PART):
    """Parallelogram arm: two parallel bars from a tower. Returns the far end points (top, bottom)."""
    bx, by = base
    a = math.radians(ang_deg)
    ends = []
    for dy in (0, gap):
        ex, ey = bx + length * math.cos(a), by + dy - length * math.sin(a)
        bar(d, bx, by + dy, ex, ey, 40, fill)
        ends.append((ex, ey))
    bar(d, ends[0][0], ends[0][1], ends[1][0], ends[1][1], 40, "#8e949b")
    return ends


def six_bar():
    im, d = canvas()
    d.rectangle((150, 560, 230, 1000), fill="#8e949b", outline=EDGE, width=6)
    (tx, ty), (bx, by) = linkage(d, (190, 700), 380, 35)
    linkage(d, (tx, ty - 150), 380, 35, gap=150, fill="#f3b27a")
    bar(d, tx, ty - 150, tx, ty, 40, "#8e949b")
    return im


def chain_bar():
    im, d = canvas()
    d.rectangle((210, 520, 290, 1000), fill="#8e949b", outline=EDGE, width=6)
    x1, y1, x2, y2 = 250, 640, 830, 360
    for x, y in ((x1, y1), (x2, y2)):
        gear(d, x, y, 80, 16, "#2f7fd0")
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a) * 95, math.cos(a) * 95
    for s in (1, -1):
        dashed(d, x1 + s * nx, y1 + s * ny, x2 + s * nx, y2 + s * ny, DARK, 12, 18)
    bar(d, x1, y1, x2, y2, 40, PART)
    d.rectangle((x2 - 30, y2 + 60, x2 + 160, y2 + 110), fill="#f3b27a", outline=EDGE, width=5)
    return im


def linear_slide():
    im, d = canvas()
    d.rectangle((480, 150, 560, 1000), fill=PART, outline=EDGE, width=6)
    for y in range(170, 990, 40):
        d.polygon([(560, y), (590, y + 10), (590, y + 25), (560, y + 35)], fill="#2f7fd0", outline=EDGE)
    d.rounded_rectangle((590, 420, 820, 640), radius=16, fill="#f3b27a", outline=EDGE, width=6)
    gear(d, 640, 530, 50, 10, "#2f7fd0")
    arrow(d, 900, 640, 900, 260, ORANGE, 12, 44)
    return im


def cascade_lift():
    im, d = canvas()
    for i, (x, top, fill) in enumerate([(360, 360, "#8e949b"), (440, 220, PART), (520, 90, "#f3b27a")]):
        d.rectangle((x, top, x + 300, 1000 - i * 60), fill=fill, outline=EDGE, width=6)
    for x in (400, 480):
        dashed(d, x + 40, 300, x + 40, 900, DARK, 10, 18)
    arrow(d, 960, 700, 960, 200, ORANGE, 12, 44)
    return im


def scissor_lift():
    im, d = canvas()
    xl, xr, h = 330, 870, 210
    y = 980
    for i in range(3):
        bar(d, xl, y, xr, y - h, 40)
        bar(d, xr, y, xl, y - h, 40, "#8e949b")
        y -= h
    d.rectangle((xl - 60, y - 50, xr + 60, y), fill="#f3b27a", outline=EDGE, width=6)
    d.rectangle((xl - 60, 980, xr + 60, 1030), fill=PART, outline=EDGE, width=6)
    arrow(d, 1030, 900, 1030, 300, ORANGE, 12, 44)
    return im


def flywheel_launcher():
    im, d = canvas()
    d.rectangle((150, 760, 880, 800), fill=PART, outline=EDGE, width=6)
    wheel_side(d, 700, 580, 160, "#c2255c")
    spin(d, 700, 580, 220, 200, 320, BLUE, 10, 36)
    ball(d, 470, 715, 45)
    arrow(d, 260, 715, 390, 715, DARK, 6, 24)
    ball(d, 990, 360, 45)
    for k in range(3):
        d.line((900 - k * 50, 450 + k * 30, 950 - k * 50, 410 + k * 30), fill=ORANGE, width=8)
    arrow(d, 1010, 330, 1110, 240, ORANGE, 10, 36)
    return im


# --- power transfer ---
def gear_pair(d, small_fill, big_fill, motor=True):
    gear(d, 400, 600, 110, 12, small_fill)
    gear(d, 740, 600, 240, 36, big_fill)
    if motor:
        d.rounded_rectangle((300, 150, 500, 420), radius=24, fill="#c9ced4", outline=EDGE, width=6)
        d.line((400, 420, 400, 580), fill=EDGE, width=14)
    spin(d, 400, 600, 175, 300, 360, DARK, 7, 26)
    spin(d, 740, 600, 300, 240, 180, DARK, 7, 26)


def driving_gear():
    im, d = canvas()
    gear_pair(d, ORANGE, "#c9ced4")
    return im


def driven_gear():
    im, d = canvas()
    gear_pair(d, "#c9ced4", ORANGE)
    bar(d, 740, 600, 1100, 300, 40, "#8e949b")
    return im


def gear_ratio():
    im, d = canvas()
    gear_pair(d, "#2f7fd0", "#2f7fd0")
    text(d, (400, 820), "12T", 56, True, ORANGE)
    text(d, (740, 920), "36T", 56, True, ORANGE)
    text(d, (600, 1080), "3 : 1", 96, True)
    return im


def mechanical_advantage():
    im, d = canvas()
    ground(d, 900)
    poly(d, [(420, 900), (360, 790), (480, 790)], "#8e949b")
    poly(d, rot_rect(600, 760, 900, 34, -10), "#f3b27a")
    d.rectangle((150, 640, 350, 790), fill=DARK)
    arrow(d, 1010, 520, 1010, 640, BLUE, 10, 36)
    arrow(d, 250, 760, 250, 480, ORANGE, 22, 64)
    return im


def compound_gear_ratio():
    im, d = canvas()
    gear(d, 240, 420, 80, 12)
    gear(d, 520, 420, 200, 36)
    gear(d, 520, 420, 80, 12, ORANGE, hole=True)
    gear(d, 520, 880, 80, 12, ORANGE)
    dashed(d, 520, 520, 520, 780, DARK, 6)
    gear(d, 860, 880, 260, 60)
    text(d, (380, 120), "3 : 1", 60, True, BLUE)
    text(d, (860, 540), "5 : 1", 60, True, BLUE)
    text(d, (220, 900), "15 : 1", 72, True)
    return im


def idler_gear():
    im, d = canvas()
    for cx, fill in [(250, "#2f7fd0"), (600, ORANGE), (950, "#2f7fd0")]:
        gear(d, cx, 600, 150, 18, fill)
    spin(d, 250, 600, 230, 200, 330, DARK, 7, 26)
    spin(d, 600, 600, 230, 150, 30, ORANGE, 8, 30)        # middle gear turns the other way (arrow below)
    spin(d, 950, 600, 230, 200, 330, DARK, 7, 26)
    return im


# --- forces ---
def force():
    im, d = canvas()
    ground(d, 900)
    d.rectangle((440, 650, 760, 900), fill="#4fb3e3", outline=EDGE, width=6)
    arrow(d, 120, 775, 420, 775, ORANGE, 16, 56)
    d.line((760, 700, 1000, 560), fill=DARK, width=6)
    arrow(d, 1000, 560, 1120, 490, BLUE, 16, 56)
    return im


def unbalanced_force():
    im, d = canvas()
    ground(d, 860)
    d.rectangle((470, 610, 730, 860), fill="#4fb3e3", outline=EDGE, width=6)
    arrow(d, 470, 735, 330, 735, BLUE, 14, 48)
    arrow(d, 730, 735, 1120, 735, ORANGE, 24, 72)
    dashed(d, 520, 1000, 900, 1000, ORANGE, 8)
    arrow(d, 880, 1000, 960, 1000, ORANGE, 10, 36)
    return im


def traction():
    im, d = canvas()
    ground(d, 900)
    wheel_side(d, 600, 640, 260)
    spin(d, 600, 640, 330, 200, 300, DARK, 9, 34)
    arrow(d, 600, 930, 340, 930, BLUE, 12, 44)
    arrow(d, 600, 640, 1000, 640, ORANGE, 16, 56)
    return im


def friction():
    im, d = canvas()
    d.line((80, 800, S - 80, 800), fill=GROUND, width=8)
    for x in range(100, S - 100, 40):
        d.line((x, 800, x + 20, 820), fill=GROUND, width=5)
    d.rectangle((420, 560, 780, 800), fill="#4fb3e3", outline=EDGE, width=6)
    arrow(d, 600, 680, 1020, 680, BLUE, 14, 48)
    arrow(d, 600, 790, 300, 790, ORANGE, 14, 48)
    return im


def mass():
    im, d = canvas()
    px, py, half, tilt = 600, 430, 430, math.radians(-12)        # beam dips toward the heavier side (left)
    ends = [(px - half * math.cos(tilt), py - half * math.sin(tilt)), (px + half * math.cos(tilt), py + half * math.sin(tilt))]
    poly(d, [(px, py), (px - 60, 960), (px + 60, 960)], "#8e949b")
    d.rectangle((px - 200, 960, px + 200, 1010), fill="#8e949b")
    poly(d, rot_rect(px, py, 2 * half + 60, 26, math.degrees(tilt)), DARK)
    for (ex, ey), size, fill in zip(ends, (240, 120), ("#4fb3e3", "#f3b27a")):
        d.rectangle((ex - size / 2, ey - 14 - size, ex + size / 2, ey - 14), fill=fill, outline=EDGE, width=6)
    return im


def center_of_mass():
    im, d = canvas()
    gy = robot_side(d, 240, 820, 720, 250, 85)
    ground(d, gy)
    bar(d, 760, 560, 1060, 360, 40)
    cx, cy, r = 560, 690, 50
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=DARK, width=6)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 270, fill=DARK)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 0, 90, fill=DARK)
    dashed(d, cx, cy + r, cx, gy, ORANGE, 6)
    return im


# --- control techniques ---
def autonomous():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    pts = [(300, 900), (300, 450), (750, 450), (750, 300), (900, 300)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dashed(d, x1, y1, x2, y2, BLUE, 10, 22)
    for i, (x, y) in enumerate(pts[1:], 1):
        d.ellipse((x - 32, y - 32, x + 32, y + 32), fill=BLUE)
        text(d, (x, y), str(i), 38, True, "white")
    robot_top(d, 300, 940, 130, 130)
    controller_icon(d, 900, 900, 0.7, "#c9ced4")
    d.line((780, 800, 1020, 1000), fill=RED, width=16)
    d.line((780, 1000, 1020, 800), fill=RED, width=16)
    return im


def starting_position():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    x, y = 300, 750
    for (cx, cy), (dx, dy) in [((x, y), (1, 1)), ((x + 300, y), (-1, 1)), ((x, y + 300), (1, -1)), ((x + 300, y + 300), (-1, -1))]:
        d.line((cx, cy, cx + dx * 80, cy), fill=ORANGE, width=14)
        d.line((cx, cy, cx, cy + dy * 80), fill=ORANGE, width=14)
    robot_top(d, x + 150, y + 150, 220, 220)
    dashed(d, x + 150, y - 40, x + 150, 300, BLUE, 8)
    return im


def graph_frame(d):
    axes(d, 150, 1000, 1080, 150)
    dashed(d, 150, 400, 1080, 400, ORANGE, 6)
    d.ellipse((1060, 380, 1100, 420), fill=ORANGE)


def bang_bang_control():
    im, d = canvas()
    graph_frame(d)
    pts = [(150, 1000), (480, 360)]
    x, up = 480, False
    while x < 1060:
        pts.append((x + 70, 450 if up else 350)); x += 70; up = not up
    d.line(pts, fill=BLUE, width=10, joint="curve")
    return im


def pid_control():
    im, d = canvas()
    graph_frame(d)
    pts = []
    for i in range(200):
        t = i / 199 * 6
        y = 1 - math.exp(-t) * (math.cos(1.6 * t) + 0.6 * math.sin(1.6 * t))
        pts.append((150 + i / 199 * 900, 1000 - 600 * y))
    d.line(pts, fill=BLUE, width=10, joint="curve")
    return im


def proportional_control():
    im, d = canvas()
    d.line((1000, 200, 1000, 1000), fill=ORANGE, width=10)
    poly(d, [(1000, 200), (1100, 240), (1000, 280)], ORANGE, ORANGE)
    for (x, y, L) in [(200, 330, 420), (540, 600, 240), (820, 870, 90)]:
        robot_top(d, x, y, 120, 120, front=False)
        arrow(d, x + 75, y, x + 75 + L, y, BLUE, 16 if L > 200 else 12, 56 if L > 200 else 40)
    return im


def number_line(d, robot_at, flag_hi):
    y = 700
    d.line((120, y, 1080, y), fill=DARK, width=8)
    for i, v in enumerate(range(0, 700, 100)):
        x = 150 + i * 150
        d.line((x, y - 20, x, y + 20), fill=DARK, width=5)
        text(d, (x, y + 60), str(v), 40)
    xr = 150 + robot_at / 100 * 150
    robot_top(d, xr, y - 110, 130, 130, front=False)
    xf = 150 + 5 * 150
    d.line((xf, y, xf, y - 300), fill=ORANGE if flag_hi else DARK, width=10)
    poly(d, [(xf, y - 300), (xf + 140, y - 255), (xf, y - 210)], ORANGE if flag_hi else "#c9ced4", EDGE, 4)
    return xr, xf, y


def setpoint():
    im, d = canvas()
    xr, xf, y = number_line(d, 200, True)
    d.ellipse((xf - 26, y - 26, xf + 26, y + 26), fill=ORANGE)
    text(d, (xf, y + 140), "500 mm", 56, True, ORANGE)
    return im


def error_control():
    im, d = canvas()
    xr, xf, y = number_line(d, 200, False)
    dim(d, xr, y + 150, xf, y + 150, ORANGE)
    text(d, ((xr + xf) / 2, y + 220), "300 mm", 56, True, ORANGE)
    return im


def odometry():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    arrow(d, 150, 1050, 1080, 1050, DARK, 6, 26)
    arrow(d, 150, 1050, 150, 120, DARK, 6, 26)
    pts = [(260, 980), (330, 820), (460, 700), (620, 640), (760, 520)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dashed(d, x1, y1, x2, y2, BLUE, 8, 18)
    x, y = pts[-1]
    dashed(d, x, y, x, 1050, ORANGE, 5)
    dashed(d, x, y, 150, y, ORANGE, 5)
    poly(d, rot_rect(x, y, 120, 120, 40), PART)
    arrow(d, x, y, x + 150 * math.cos(math.radians(-50)), y + 150 * math.sin(math.radians(-50)), BLUE, 10, 36)
    text(d, (x + 90, y + 120), "(x, y)", 56, True, ORANGE, anchor="lm")
    return im


# ---------- design process and competition drawings -----------------------------------------
SKIN, SHIRT, ADULT, NOTE = "#f1c9a5", "#4fb3e3", "#6b7280", "#fff3bf"


def person(d, x, y, k=1.0, shirt=SHIRT):
    """Simple figure standing with feet at (x, y)."""
    d.rounded_rectangle((x - 70 * k, y - 330 * k, x + 70 * k, y - 120 * k), radius=40 * k, fill=shirt, outline=EDGE, width=5)
    for dx in (-35, 35):
        d.rounded_rectangle((x + dx * k - 22 * k, y - 140 * k, x + dx * k + 22 * k, y), radius=14 * k, fill=DARK)
    d.ellipse((x - 55 * k, y - 450 * k, x + 55 * k, y - 340 * k), fill=SKIN, outline=EDGE, width=5)


def clipboard(d, x, y, k=1.0):
    d.rounded_rectangle((x - 70 * k, y - 95 * k, x + 70 * k, y + 95 * k), radius=10 * k, fill="#c69c6d", outline=EDGE, width=4)
    d.rectangle((x - 55 * k, y - 70 * k, x + 55 * k, y + 80 * k), fill="white")
    for i in range(4):
        d.line((x - 40 * k, y - 40 * k + i * 32 * k, x + 40 * k, y - 40 * k + i * 32 * k), fill=FAINT, width=4)
    d.rectangle((x - 30 * k, y - 105 * k, x + 30 * k, y - 80 * k), fill=DARK)


def mini_robot(d, x, y, k=1.0, fill=PART):
    """Small side-view robot with its wheels on y."""
    d.rounded_rectangle((x - 110 * k, y - 150 * k, x + 110 * k, y - 50 * k), radius=12 * k, fill=fill, outline=EDGE, width=5)
    for dx in (-65, 65):
        wheel_side(d, x + dx * k, y - 40 * k, 40 * k)


def plate(d, x, y, number, w=300, h=110, color="#e03131"):
    d.rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), radius=14, fill=color, outline=EDGE, width=5)
    text(d, (x, y), number, int(h * 0.62), True, "white")


def constraint():
    im, d = canvas()
    gy = robot_side(d, 330, 820, 520, 330, 80)
    ground(d, gy)
    d.rectangle((300, 380, 880, gy), outline=ORANGE, width=6)
    for x in range(300, 880, 40):
        d.line((x, 380, x + 20, 380), fill="white", width=8)
    dim(d, 300, 300, 880, 300, ORANGE)
    dim(d, 960, 380, 960, gy, ORANGE)
    text(d, (590, 240), "19 in", 56, True, ORANGE)
    text(d, (1060, (380 + gy) / 2), "15 in", 56, True, ORANGE)
    return im


def brainstorm():
    im, d = canvas()
    # light bulb
    d.ellipse((470, 380, 730, 640), fill="#ffe066", outline=EDGE, width=6)
    d.rectangle((540, 630, 660, 720), fill="#c9ced4", outline=EDGE, width=6)
    for a in range(0, 360, 45):
        r = math.radians(a)
        if 60 < a < 120:
            continue
        d.line((600 + 160 * math.cos(r), 510 + 160 * math.sin(r), 600 + 210 * math.cos(r), 510 + 210 * math.sin(r)), fill="#f0c419", width=10)
    notes = [(170, 220, -6), (1000, 230, 5), (150, 640, 4), (1040, 650, -5), (330, 950, -3), (860, 960, 6), (600, 160, 0)]
    for i, (x, y, deg) in enumerate(notes):
        poly(d, rot_rect(x, y, 200, 200, deg), NOTE, "#f0c419", 5)
        if i % 3 == 0:
            wheel_side(d, x, y, 50)
        elif i % 3 == 1:
            gear(d, x, y, 45, 10, "#2f7fd0", hole=False)
        else:
            claw_jaws(d, [(x - 30, y + 60), (x + 30, y + 60)], [-100, -80], 110)
    return im


def iterate():
    im, d = canvas()
    for i, (x, k) in enumerate([(220, 0.7), (600, 0.85), (980, 1.0)]):
        mini_robot(d, x, 640, k * 1.3, ["#dee2e6", "#c9ced4", PART][i])
        if i == 2:
            bar(d, x + 40, 470, x + 170, 380, 26)
        text(d, (x, 740), f"v{i + 1}", 60, True, BLUE)
        if i < 2:
            arrow(d, x + 120, 560, x + 250, 560, DARK, 8, 30)
    d.arc((180, 760, 1020, 1100), start=10, end=170, fill=ORANGE, width=10)
    poly(d, [(187, 880), (150, 950), (224, 950)], ORANGE, ORANGE)   # arc's left end (170°), pointing back up to v1
    return im


def scouting():
    im, d = canvas()
    mini_robot(d, 420, 760, 1.9, "#c9ced4")
    plate(d, 420, 560, "5678B", 260, 90)
    d.ellipse((470, 300, 830, 660), outline=DARK, width=26)
    d.line((800, 630, 960, 800), fill=DARK, width=40)
    clipboard(d, 990, 330, 1.3)
    return im


def pit():
    im, d = canvas()
    d.rectangle((120, 640, 1080, 690), fill="#a0785a", outline=EDGE, width=5)
    for x in (170, 1030):
        d.rectangle((x - 20, 690, x + 20, 1000), fill="#a0785a", outline=EDGE, width=4)
    mini_robot(d, 420, 640, 1.6)
    d.rounded_rectangle((720, 500, 980, 640), radius=10, fill="#e03131", outline=EDGE, width=5)
    d.rectangle((800, 470, 900, 510), outline=EDGE, width=8)
    d.rectangle((120, 230, 1080, 330), fill="#f1f3f5", outline=EDGE, width=5)
    text(d, (600, 280), "1234A", 70, True, DARK)
    for x in (300, 900):
        d.line((x, 330, x, 420), fill=EDGE, width=6)
    return im


def match_schedule():
    im, d = canvas()
    rows = [("Match", "Time", "Partner"), ("Q1", "9:00", "5678B"), ("Q7", "9:40", "2468C"), ("Q12", "10:15", "1357D"), ("Q18", "10:50", "9999E")]
    xs, y0, rh = [170, 450, 760, 1030], 220, 150
    d.rectangle((xs[0], y0 + 2 * rh, xs[-1], y0 + 3 * rh), fill="#ffe8cc")
    for i, row in enumerate(rows):
        y = y0 + i * rh
        if i == 0:
            d.rectangle((xs[0], y, xs[-1], y + rh), fill=BLUE)
        for j, cell in enumerate(row):
            text(d, ((xs[j] + xs[j + 1]) / 2, y + rh / 2), cell, 54, i == 0, "white" if i == 0 else TEXT)
    for i in range(len(rows) + 1):
        d.line((xs[0], y0 + i * rh, xs[-1], y0 + i * rh), fill=EDGE, width=4)
    for x in xs:
        d.line((x, y0, x, y0 + len(rows) * rh), fill=EDGE, width=4)
    return im


def queuing_area():
    im, d = canvas()
    d.rectangle((830, 380, 1130, 980), fill="#f1f3f5", outline=EDGE, width=6)
    for y in range(440, 980, 75):
        d.line((830, y, 1130, y), fill="#d5d9de", width=3)
    for x, shirt in [(170, "#f3b27a"), (360, "#f3b27a"), (560, SHIRT), (720, SHIRT)]:
        person(d, x, 980, 0.95, shirt)
    dashed(d, 90, 1030, 780, 1030, DARK, 6)
    arrow(d, 480, 1100, 800, 1100, ORANGE, 12, 44)
    return im


def driver():
    im, d = canvas()
    d.rectangle((640, 520, 1130, 1000), fill="#f1f3f5", outline=EDGE, width=6)
    poly(d, rot_rect(890, 760, 150, 150, 0), PART)
    d.polygon([(890, 700), (860, 745), (920, 745)], fill=BLUE)
    person(d, 330, 1000, 1.25, "#f3b27a")
    controller_icon(d, 360, 700, 0.75)
    for r in (70, 120, 170):
        d.arc((560 - r, 560 - r, 560 + r, 560 + r), start=-40, end=40, fill=ORANGE, width=8)
    return im


def coach():
    im, d = canvas()
    d.rectangle((650, 560, 1130, 1000), fill="#f1f3f5", outline=EDGE, width=6)
    for x in (700, 860):
        person(d, x, 990, 0.7)
    dashed(d, 560, 380, 560, 1060, ORANGE, 8)
    person(d, 280, 1000, 1.4, ADULT)
    clipboard(d, 400, 620, 1.2)
    return im


def trophy(d, x, y, k=1.0):
    gold = "#f0c419"
    d.pieslice((x - 120 * k, y - 160 * k, x + 120 * k, y + 80 * k), 0, 180, fill=gold, outline=EDGE, width=5)
    d.rectangle((x - 120 * k, y - 160 * k, x + 120 * k, y - 40 * k), fill=gold, outline=EDGE, width=5)
    for s in (-1, 1):
        d.arc((x + s * 120 * k - 60 * k, y - 140 * k, x + s * 120 * k + 60 * k, y - 20 * k), start=-90 if s > 0 else 90,
              end=90 if s > 0 else 270, fill=EDGE, width=int(12 * k))
    d.rectangle((x - 25 * k, y + 80 * k, x + 25 * k, y + 160 * k), fill=gold, outline=EDGE, width=5)
    d.rectangle((x - 90 * k, y + 160 * k, x + 90 * k, y + 210 * k), fill="#8e949b", outline=EDGE, width=5)


def judge():
    im, d = canvas()
    person(d, 360, 1040, 1.45, ADULT)
    clipboard(d, 520, 640, 1.4)
    trophy(d, 900, 520, 1.3)
    return im


def alliance_partner():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    for x, y, fill, num in [(400, 560, "#4fb3e3", "1234A"), (800, 560, "#f3b27a", "5678B")]:
        d.rounded_rectangle((x - 120, y - 120, x + 120, y + 120), radius=20, fill=fill, outline=EDGE, width=6)
        plate(d, x, y + 220, num, 260, 90)
    text(d, (600, 560), "+", 160, True, DARK)
    return im


def game_piece():
    im, d = canvas()
    ball(d, 280, 600, 150, "#f0c419")
    d.polygon([(500, 520), (640, 450), (780, 520), (640, 590)], fill="#74c0fc", outline=EDGE, width=5)
    d.polygon([(500, 520), (640, 590), (640, 770), (500, 700)], fill="#4fb3e3", outline=EDGE, width=5)
    d.polygon([(640, 590), (780, 520), (780, 700), (640, 770)], fill="#339af0", outline=EDGE, width=5)
    d.rounded_rectangle((900, 420, 1020, 780), radius=20, fill="#e03131", outline=EDGE, width=5)
    d.ellipse((900, 390, 1020, 450), fill="#ff6b6b", outline=EDGE, width=5)
    return im


def game_manual():
    im, d = canvas()
    poly(d, [(330, 170), (900, 170), (900, 1030), (330, 1030)], "white", EDGE, 6)
    d.rectangle((330, 170, 900, 330), fill=BLUE)
    d.rectangle((400, 225, 830, 275), fill="white")
    for i, code in enumerate(["<G1>", "<SG2>", "<R9>", "<T4>"]):
        y = 420 + i * 150
        text(d, (390, y), code, 46, True, ORANGE, anchor="lm")
        for j in range(2):
            d.line((560, y - 20 + j * 45, 840 - j * 80, y - 20 + j * 45), fill=FAINT, width=10)
    return im


def license_plate():
    im, d = canvas()
    gy = robot_side(d, 230, 760, 740, 330, 90)
    ground(d, gy)
    plate(d, 600, 590, "1234A", 420, 150)
    return im


# ---- award icons: one medal shape, a different color and symbol for each award ----

def star(d, cx, cy, r, fill, inner=0.45, outline=None, width=0):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline, width=width)


def medal(color, ribbon=None):
    """Medal on a ribbon. Returns (im, d, cx, cy, r) so the caller draws the symbol on the disc."""
    im, d = canvas()
    cx, cy, r = 600, 520, 330
    rb = ribbon or color
    for s in (-1, 1):
        x0 = cx + s * 120
        d.polygon([(x0 - 85, cy + 150), (x0 + 85, cy + 150), (x0 + 85 + s * 60, cy + 620),
                   (x0 + s * 60, cy + 560), (x0 - 85 + s * 60, cy + 620)], fill=rb, outline=EDGE)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color, outline=EDGE, width=8)
    d.ellipse((cx - r + 40, cy - r + 40, cx + r - 40, cy + r - 40), outline="white", width=10)
    return im, d, cx, cy, r


W = "white"


def excellence_award():
    im, d, cx, cy, r = medal("#f0b400", "#1c7ed6")
    star(d, cx, cy + 10, 200, W, outline=EDGE, width=4)
    for dx in (-150, 150):
        star(d, cx + dx, cy - 170, 45, W)
    return im


def design_award():
    im, d, cx, cy, r = medal("#1c7ed6")
    for s in (-1, 1):  # open notebook
        d.polygon([(cx, cy - 110), (cx + s * 190, cy - 140), (cx + s * 190, cy + 120), (cx, cy + 150)], fill=W, outline=EDGE, width=5)
        for i in range(4):
            y = cy - 80 + i * 50
            d.line((cx + s * 30, y + 5 * s * 0, cx + s * 160, y - 20), fill="#a5d8ff", width=8)
    d.line((cx + 30, cy + 170, cx + 230, cy - 60), fill=EDGE, width=38)  # pencil
    d.line((cx + 34, cy + 165, cx + 226, cy - 55), fill="#ffd43b", width=28)
    d.polygon([(cx + 18, cy + 190), (cx + 12, cy + 150), (cx + 50, cy + 175)], fill=EDGE)
    return im


def innovate_award():
    im, d, cx, cy, r = medal("#7048e8")
    d.ellipse((cx - 130, cy - 210, cx + 130, cy + 50), fill="#ffe066", outline=EDGE, width=6)  # bulb
    d.rectangle((cx - 60, cy + 30, cx + 60, cy + 120), fill="#ffe066", outline=EDGE, width=6)
    for i in range(3):
        d.rounded_rectangle((cx - 65, cy + 120 + i * 35, cx + 65, cy + 150 + i * 35), radius=12, fill="#ced4da", outline=EDGE, width=4)
    d.line((cx - 40, cy - 20, cx - 20, cy - 90, cx, cy - 30, cx + 20, cy - 90, cx + 40, cy - 20), fill="#f08c00", width=10)
    for a in (-150, -120, -90, -60, -30):
        t = math.radians(a)
        d.line((cx + 165 * math.cos(t), cy - 80 + 165 * math.sin(t), cx + 215 * math.cos(t), cy - 80 + 215 * math.sin(t)), fill=W, width=12)
    return im


def think_award():
    im, d, cx, cy, r = medal("#2f9e44")
    d.rounded_rectangle((cx - 210, cy - 150, cx + 210, cy + 150), radius=24, fill="#1b1f24", outline=W, width=8)
    text(d, (cx, cy), "</>", 170, True, "#8ce99a")
    return im


def amaze_award():
    im, d, cx, cy, r = medal("#1098ad")
    mini_robot(d, cx, cy + 150, 1.25, "#ced4da")
    d.rectangle((cx - 20, cy - 80, cx + 20, cy - 40), fill=EDGE)
    for x, y, rr in [(cx - 170, cy - 150, 55), (cx + 160, cy - 180, 70), (cx + 10, cy - 210, 40)]:
        star(d, x, y, rr, "#ffe066", inner=0.35)
    return im


def build_award():
    im, d, cx, cy, r = medal("#495057")
    ang = math.radians(-45)  # wrench along a diagonal
    ux, uy = math.cos(ang), math.sin(ang)
    p0, p1 = (cx - 170 * ux, cy - 170 * uy), (cx + 120 * ux, cy + 120 * uy)
    d.line((p0, p1), fill=EDGE, width=72)
    d.line((p0, p1), fill="#dee2e6", width=56)
    hx, hy = cx + 170 * ux, cy + 170 * uy
    d.ellipse((hx - 95, hy - 95, hx + 95, hy + 95), fill="#dee2e6", outline=EDGE, width=6)
    d.polygon([(hx + 20, hy - 120), (hx + 120, hy - 20), (hx + 50, hy + 50), (hx - 50, hy - 50)], fill="#495057")
    d.ellipse((p0[0] - 45, p0[1] - 45, p0[0] + 45, p0[1] + 45), fill="#dee2e6", outline=EDGE, width=6)
    d.ellipse((p0[0] - 18, p0[1] - 18, p0[0] + 18, p0[1] + 18), fill="#495057")
    return im


def create_award():
    im, d, cx, cy, r = medal("#d6336c")
    d.ellipse((cx - 210, cy - 160, cx + 190, cy + 170), fill="#f8f0e3", outline=EDGE, width=6)  # palette
    d.ellipse((cx + 60, cy + 40, cx + 140, cy + 120), fill="#d6336c", outline=EDGE, width=4)
    for (x, y), c in zip([(cx - 120, cy - 60), (cx - 30, cy - 110), (cx + 70, cy - 90), (cx - 130, cy + 50), (cx - 40, cy + 90)],
                         ["#e03131", "#ffd43b", "#1c7ed6", "#2f9e44", "#7048e8"]):
        d.ellipse((x - 38, y - 38, x + 38, y + 38), fill=c, outline=EDGE, width=4)
    return im


def judges_award():
    im, d, cx, cy, r = medal("#a0522d")
    star(d, cx - 30, cy - 30, 120, "#ffe066", outline=EDGE, width=4)
    d.ellipse((cx - 190, cy - 190, cx + 130, cy + 130), outline=W, width=26)  # magnifier
    d.line((cx + 90, cy + 90, cx + 210, cy + 210), fill=W, width=44)
    return im


def inspire_award():
    im, d, cx, cy, r = medal("#f76707")
    d.polygon([(cx, cy - 230), (cx + 70, cy - 110), (cx + 150, cy - 160), (cx + 170, cy + 40), (cx + 110, cy + 170),
               (cx - 110, cy + 170), (cx - 170, cy + 40), (cx - 130, cy - 120), (cx - 60, cy - 60)], fill="#ffe066", outline=EDGE, width=6)
    d.polygon([(cx, cy - 40), (cx + 80, cy + 60), (cx + 50, cy + 170), (cx - 50, cy + 170), (cx - 80, cy + 60)], fill="#ff922b")
    return im


def sportsmanship_award():
    im, d, cx, cy, r = medal("#e03131")
    k = 12.5  # classic heart curve
    pts = [(cx + k * 16 * math.sin(t) ** 3,
            cy - 10 - k * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)))
           for t in [i * 2 * math.pi / 200 for i in range(200)]]
    d.polygon(pts, fill=W)
    return im


def energy_award():
    im, d, cx, cy, r = medal("#74b816")
    d.polygon([(cx + 40, cy - 240), (cx - 150, cy + 30), (cx - 10, cy + 30), (cx - 60, cy + 240), (cx + 150, cy - 50), (cx + 10, cy - 50)],
              fill="#ffe066", outline=EDGE, width=6)
    return im


def big_trophy(d, cx, cy, k=1.0):
    trophy(d, cx, cy, k)
    star(d, cx, cy - 70 * k, 55 * k, W)


def teamwork_champions():
    im, d = canvas()
    big_trophy(d, 600, 430, 1.9)
    mini_robot(d, 330, 1060, 1.0, "#4fb3e3")
    mini_robot(d, 870, 1060, 1.0, "#f3b27a")
    text(d, (600, 990), "+", 120, True, DARK)
    return im


def robot_skills_champion():
    im, d = canvas()
    big_trophy(d, 600, 430, 1.9)
    mini_robot(d, 600, 1060, 1.1, "#4fb3e3")
    return im


def small_medal(d, cx, cy, color, k=1.0):
    for s in (-1, 1):
        d.polygon([(cx + s * 30 * k - 30 * k, cy - 210 * k), (cx + s * 30 * k + 30 * k, cy - 210 * k), (cx + s * 15 * k, cy - 60 * k)], fill="#1c7ed6", outline=EDGE)
    d.ellipse((cx - 100 * k, cy - 100 * k, cx + 100 * k, cy + 100 * k), fill=color, outline=EDGE, width=6)
    star(d, cx, cy, 60 * k, W)


def judged_award():
    im, d = canvas()
    person(d, 330, 1040, 1.45, ADULT)
    clipboard(d, 500, 640, 1.4)
    small_medal(d, 880, 600, "#f0b400", 1.5)
    return im


def performance_award():
    im, d = canvas()
    d.rounded_rectangle((120, 320, 640, 640), radius=24, fill="#1b1f24", outline=EDGE, width=6)  # scoreboard
    text(d, (380, 480), "54", 200, True, "#ffe066")
    mini_robot(d, 380, 900, 1.3, "#4fb3e3")
    small_medal(d, 900, 600, "#f0b400", 1.5)
    return im


def nominated_award():
    im, d = canvas()
    for i, x in enumerate((230, 470)):
        person(d, x, 1040, 1.25, ["#69db7c", "#ffa94d"][i])
    d.line((520, 760, 560, 560), fill="#ffa94d", width=44)  # raised arm
    d.ellipse((520, 470, 610, 580), fill=SKIN, outline=EDGE, width=5)
    small_medal(d, 900, 600, "#e03131", 1.5)
    return im


# ---- competition: tiers, matches, roles, rules ----
YELLOW, LIME, PINK = "#ffd43b", "#74b816", "#f783ac"


def check(d, x, y, s=60, color=GREEN, w=16):
    d.line((x - s, y, x - s * 0.3, y + s * 0.7, x + s, y - s * 0.8), fill=color, width=w, joint="curve")


def cross(d, x, y, s=50, color="#e03131", w=16):
    d.line((x - s, y - s, x + s, y + s), fill=color, width=w)
    d.line((x - s, y + s, x + s, y - s), fill=color, width=w)


def page(d, x0, y0, x1, y1, lines=5, fill="white"):
    d.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=fill, outline=EDGE, width=6)
    gap = (y1 - y0 - 80) / max(lines, 1)
    for i in range(lines):
        y = y0 + 60 + i * gap
        d.line((x0 + 40, y, x1 - 40, y), fill=FAINT, width=8)


def stopwatch(d, cx, cy, r, s="1:00", color="#e03131"):
    d.rectangle((cx - 22, cy - r - 45, cx + 22, cy - r + 5), fill=EDGE)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=color, width=int(r * 0.12))
    if s:
        text(d, (cx, cy), s, int(r * 0.55), True, DARK)


def school(d, cx, by, k=1.0, fill="#ffe8cc"):
    d.rectangle((cx - 170 * k, by - 220 * k, cx + 170 * k, by), fill=fill, outline=EDGE, width=6)
    d.polygon([(cx - 200 * k, by - 220 * k), (cx, by - 360 * k), (cx + 200 * k, by - 220 * k)], fill="#e8590c", outline=EDGE)
    d.rectangle((cx - 40 * k, by - 110 * k, cx + 40 * k, by), fill="#a0522d", outline=EDGE, width=4)
    for dx in (-110, 110):
        d.rectangle((cx + dx * k - 35 * k, by - 180 * k, cx + dx * k + 35 * k, by - 120 * k), fill="#a5d8ff", outline=EDGE, width=4)
    d.line((cx, by - 360 * k, cx, by - 460 * k), fill=EDGE, width=6)
    d.polygon([(cx, by - 460 * k), (cx + 80 * k, by - 435 * k), (cx, by - 410 * k)], fill="#e03131")


def globe(d, cx, cy, r, fill="#4dabf7"):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=EDGE, width=6)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline="white", width=6)
    d.line((cx, cy - r, cx, cy + r), fill="white", width=6)
    for t in (-0.5, 0, 0.5):
        w = r * math.sqrt(1 - t * t)
        d.line((cx - w, cy + t * r, cx + w, cy + t * r), fill="white", width=6)


STEP = [(130, 900, 470, 1080), (470, 680, 810, 1080), (810, 460, 1150, 1080)]


def ladder(hi=None, faded=False):
    """Three steps: local qualifying event → Championship Event → World Championship."""
    im, d = canvas()
    for i, box in enumerate(STEP):
        d.rectangle(box, fill=(YELLOW if i == hi else "#e9ecef"), outline=EDGE, width=6)
    for i in range(2):
        arrow(d, STEP[i][0] + 170, STEP[i][1] - 40, STEP[i + 1][0] + 120, STEP[i + 1][1] - 70, DARK, 10, 40)
    globe(d, 980, 340, 90, "#4dabf7" if hi == 2 else "#ced4da")
    return im, d


def qualifying_event():
    im, d = ladder(0)
    mini_robot(d, 300, 890, 0.9, "#4fb3e3")
    return im


def championship_event():
    im, d = ladder(1)
    mini_robot(d, 640, 670, 0.9, "#4fb3e3")
    big_trophy(d, 640, 380, 0.9)
    return im


def world_championship():
    im, d = ladder(2)
    mini_robot(d, 980, 450, 0.9, "#4fb3e3")
    return im


def signature_event():
    im, d = ladder(None)
    d.rounded_rectangle((80, 260, 420, 520), radius=20, fill="#7048e8", outline=EDGE, width=6)
    star(d, 250, 390, 90, YELLOW)
    d.line((420, 330, 860, 330), fill="#7048e8", width=14)
    arrow(d, 860, 330, 890, 340, "#7048e8", 14, 50)
    return im


def spotlight_event():
    im, d = canvas()
    d.polygon([(600, 120), (300, 900), (900, 900)], fill="#fff3bf")
    d.ellipse((520, 60, 680, 180), fill=DARK)
    d.ellipse((300, 860, 900, 960), fill="#ffe066", outline=EDGE, width=5)
    mini_robot(d, 600, 900, 1.3, "#4fb3e3")
    for x, y in [(180, 300), (1020, 300), (160, 700), (1040, 700)]:
        star(d, x, y, 50, YELLOW, outline=EDGE, width=3)
    return im


def scrimmage():
    im, d = canvas()
    field(d, 200, 330, 4, 200)
    mini_robot(d, 420, 900, 1.0, "#4fb3e3")
    mini_robot(d, 780, 900, 1.0, "#f3b27a")
    trophy(d, 1030, 220, 0.6)
    d.line((900, 80, 1160, 380), fill="#e03131", width=20)
    return im


def in_school_competition():
    im, d = canvas()
    school(d, 600, 760, 1.6, "#fff4e6")
    mini_robot(d, 470, 760, 0.6, "#4fb3e3")
    mini_robot(d, 730, 760, 0.6, "#f3b27a")
    ground(d, 770)
    return im


def school_based_event():
    im, d = canvas()
    for i, x in enumerate((230, 600, 970)):
        school(d, x, 640, 0.75)
        mini_robot(d, x, 900, 0.8, ["#4fb3e3", "#f3b27a", "#69db7c"][i])
    d.line((140, 990, 1060, 990), fill=GROUND, width=8)
    return im


def skills_only_event():
    im, d = canvas()
    field(d, 140, 360, 4, 180)
    mini_robot(d, 500, 900, 1.2, "#4fb3e3")
    stopwatch(d, 980, 330, 170, "1:00")
    return im


def qualifying_spot():
    im, d = canvas()
    d.rounded_rectangle((180, 380, 1020, 820), radius=40, fill="#ffe066", outline=EDGE, width=8)  # ticket
    for y in (480, 600, 720):
        d.ellipse((150, y - 30, 210, y + 30), fill="white")
        d.ellipse((990, y - 30, 1050, y + 30), fill="white")
    d.line((380, 400, 380, 800), fill=EDGE, width=5)
    star(d, 280, 600, 60, "#f08c00")
    arrow(d, 560, 750, 560, 450, "#2f9e44", 40, 110)
    arrow(d, 800, 750, 800, 450, "#2f9e44", 40, 110)
    return im


def qualifying_award():
    im, d = canvas()
    small_medal(d, 380, 640, "#f0b400", 2.0)
    d.rounded_rectangle((680, 520, 1120, 760), radius=30, fill="#ffe066", outline=EDGE, width=6)
    arrow(d, 900, 720, 900, 560, "#2f9e44", 30, 80)
    text(d, (600, 640), "+", 140, True, DARK)
    return im


def world_skills_standings():
    im, d = canvas()
    globe(d, 300, 360, 170)
    for i, (n, w) in enumerate([("1", 520), ("2", 440), ("3", 380), ("4", 320)]):
        y = 640 + i * 130
        d.rounded_rectangle((180, y, 180 + 100, y + 100), radius=16, fill=YELLOW if i == 0 else "#e9ecef", outline=EDGE, width=5)
        text(d, (230, y + 50), n, 64, True, DARK)
        d.rounded_rectangle((310, y + 15, 310 + w, y + 85), radius=12, fill="#4fb3e3", outline=EDGE, width=4)
    stopwatch(d, 870, 380, 150, "")
    return im


def level_es_ms():
    im, d = canvas()
    person(d, 400, 1060, 1.15, "#69db7c")
    person(d, 800, 1060, 1.65, "#4fb3e3")
    return im


def schedule(d, x0, y0, rows, hi=None, prefix="Q"):
    w = 760
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 100 + len(rows) * 120), radius=20, fill="white", outline=EDGE, width=6)
    d.rectangle((x0, y0, x0 + w, y0 + 100), fill="#1c7ed6")
    for i, (m, a, b) in enumerate(rows):
        y = y0 + 100 + i * 120
        if i == hi:
            d.rectangle((x0 + 6, y, x0 + w - 6, y + 120), fill="#fff3bf")
        text(d, (x0 + 110, y + 60), m, 60, True, DARK)
        plate(d, x0 + 360, y + 60, a, 230, 80, "#4dabf7")
        plate(d, x0 + 620, y + 60, b, 230, 80, "#ff8787")


def qualification_match():
    im, d = canvas()
    schedule(d, 220, 230, [("Q22", "1234A", "5678B"), ("Q23", "1234A", "2468C"), ("Q24", "9012D", "1234A"), ("Q25", "1357E", "8642F")], 1)
    return im


def finals_match():
    im, d = canvas()
    big_trophy(d, 600, 330, 1.2)
    for i, (m, a, b) in enumerate([("F1", "1", "2"), ("F2", "3", "4"), ("F3", "5", "6")]):
        y = 680 + i * 150
        text(d, (300, y), m, 70, True, DARK)
        for j, n in enumerate((a, b)):
            d.rounded_rectangle((440 + j * 260, y - 55, 660 + j * 260, y + 55), radius=16, fill="#e7f1fb", outline=EDGE, width=5)
            text(d, (550 + j * 260, y), "#" + n, 60, True, DARK)
    return im


def robot_skills_challenge():
    im, d = canvas()
    field(d, 330, 330, 4, 140)
    mini_robot(d, 610, 720, 1.0, "#4fb3e3")
    controller_icon(d, 230, 950, 0.7)
    d.rounded_rectangle((830, 860, 1110, 1040), radius=16, fill="#1b1f24", outline=EDGE, width=5)
    text(d, (970, 950), "</>", 90, True, "#8ce99a")
    text(d, (600, 950), "+", 110, True, DARK)
    return im


def driving_skills():
    im, d = canvas()
    controller_icon(d, 330, 500, 1.3)
    mini_robot(d, 850, 640, 1.4, "#4fb3e3")
    for r in (60, 110, 160):
        d.arc((560 - r, 480 - r, 560 + r, 480 + r), start=-40, end=40, fill=ORANGE, width=10)
    stopwatch(d, 600, 930, 130, "1:00")
    return im


def autonomous_skills():
    im, d = canvas()
    d.rounded_rectangle((110, 330, 560, 640), radius=20, fill="#1b1f24", outline=EDGE, width=6)
    text(d, (335, 485), "</>", 150, True, "#8ce99a")
    mini_robot(d, 850, 640, 1.4, "#4fb3e3")
    arrow(d, 580, 480, 720, 480, DARK, 14, 46)
    stopwatch(d, 600, 930, 130, "1:00")
    return im


def skills_stop_time():
    im, d = canvas()
    stopwatch(d, 600, 440, 280, "0:12")
    controller_icon(d, 600, 960, 0.9)
    ground(d, 1040, 300, 900)
    return im


def ranking():
    im, d = canvas()
    for i, (team, c) in enumerate([("1234A", YELLOW), ("5678B", "#dee2e6"), ("2468C", "#ffc078"), ("9012D", "white")]):
        y = 230 + i * 200
        d.rounded_rectangle((200, y, 1000, y + 160), radius=20, fill=c, outline=EDGE, width=6)
        text(d, (300, y + 80), str(i + 1), 90, True, DARK)
        plate(d, 640, y + 80, team, 340, 110)
    return im


def scoreboard(d, x0, y0, x1, y1, s, color="#ffe066"):
    d.rounded_rectangle((x0, y0, x1, y1), radius=24, fill="#1b1f24", outline=EDGE, width=6)
    text(d, ((x0 + x1) / 2, (y0 + y1) / 2), s, int((y1 - y0) * 0.6), True, color)


def practice_match():
    im, d = canvas()
    field(d, 200, 520, 4, 140)
    mini_robot(d, 420, 980, 0.9, "#4fb3e3")
    mini_robot(d, 700, 980, 0.9, "#f3b27a")
    scoreboard(d, 330, 150, 870, 420, "- -", "#868e96")
    return im


def no_show():
    im, d = canvas()
    field(d, 150, 300, 4, 180)
    mini_robot(d, 400, 900, 1.0, "#4fb3e3")
    d.rounded_rectangle((620, 760, 880, 920), radius=16, outline="#e03131", width=8)
    text(d, (750, 840), "?", 110, True, "#e03131")
    stopwatch(d, 1000, 250, 130, "")
    return im


def referee_person(d, x, y, k=1.0):
    person(d, x, y, k, "white")
    for i in range(5):  # black stripes on the shirt
        sx = x - 55 * k + i * 27 * k
        d.rectangle((sx, y - 325 * k, sx + 12 * k, y - 125 * k), fill=DARK)


def event_partner():
    im, d = canvas()
    person(d, 330, 1060, 1.5, "#7048e8")
    clipboard(d, 500, 650, 1.2)
    field(d, 680, 520, 3, 140)
    for i, x in enumerate((720, 880, 1040)):
        person(d, x, 460, 0.55, ["#4fb3e3", "#69db7c", "#ffa94d"][i])
    return im


def head_referee():
    im, d = canvas()
    referee_person(d, 420, 1070, 1.6)
    d.ellipse((620, 380, 700, 460), fill=SKIN, outline=EDGE, width=4)  # raised hand
    d.line((560, 600, 650, 440), fill="white", width=40)
    d.line((560, 600, 650, 440), fill=EDGE, width=4)
    field(d, 760, 600, 2, 180)
    return im


def scorekeeper_referee():
    im, d = canvas()
    referee_person(d, 400, 1070, 1.5)
    d.rounded_rectangle((560, 520, 860, 900), radius=20, fill="#1b1f24", outline=EDGE, width=6)  # tablet
    text(d, (710, 650), "36", 110, True, "#ffe066")
    d.rectangle((600, 760, 820, 840), fill="#4dabf7")
    return im


def judge_advisor():
    im, d = canvas()
    person(d, 600, 760, 1.25, "#a0522d")
    clipboard(d, 760, 470, 0.8)
    for x in (230, 970):
        person(d, x, 1100, 0.9, ADULT)
    d.rounded_rectangle((120, 800, 1080, 880), radius=10, fill="#c69c6d", outline=EDGE, width=5)  # table
    return im


def emcee():
    im, d = canvas()
    person(d, 450, 1060, 1.6, "#d6336c")
    d.line((600, 560, 680, 420), fill=DARK, width=24)  # mic
    d.ellipse((640, 330, 740, 430), fill="#495057", outline=EDGE, width=5)
    for r in (90, 140, 190):
        d.arc((690 - r, 380 - r, 690 + r, 380 + r), start=-50, end=30, fill=ORANGE, width=10)
    return im


def volunteer():
    im, d = canvas()
    for i, (x, c) in enumerate([(270, "#69db7c"), (600, "#69db7c"), (930, "#69db7c")]):
        person(d, x, 1000, 1.25, c)
        d.rectangle((x - 25, 600, x + 25, 650), fill="white")
    k = 4.0
    pts = [(600 + k * 16 * math.sin(t) ** 3, 250 - k * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)))
           for t in [i * 2 * math.pi / 120 for i in range(120)]]
    d.polygon(pts, fill="#e03131")
    return im


def code_of_conduct():
    im, d = canvas()
    page(d, 300, 160, 900, 1040, 7)
    k = 4.5
    pts = [(600 + k * 16 * math.sin(t) ** 3, 820 - k * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)))
           for t in [i * 2 * math.pi / 120 for i in range(120)]]
    d.polygon(pts, fill="#e03131")
    return im


def student_centered_policy():
    im, d = canvas()
    person(d, 330, 1060, 1.15, "#4fb3e3")  # student builds
    mini_robot(d, 560, 1060, 1.0)
    d.line((390, 700, 470, 900), fill="#4fb3e3", width=36)
    person(d, 930, 1060, 1.6, ADULT)  # adult stands back and explains
    d.ellipse((560, 170, 1100, 480), fill="white", outline=EDGE, width=6)
    d.polygon([(820, 470), (900, 470), (900, 560)], fill="white", outline=EDGE)
    text(d, (830, 325), "Why?", 110, True, BLUE)
    return im


def official_qa():
    im, d = canvas()
    d.rounded_rectangle((120, 200, 620, 560), radius=40, fill="#e7f1fb", outline=EDGE, width=6)
    text(d, (370, 380), "?", 220, True, BLUE)
    d.rounded_rectangle((560, 600, 1080, 960), radius=40, fill="#ebfbee", outline=EDGE, width=6)
    page(d, 650, 660, 990, 900, 4)
    check(d, 940, 720, 50)
    return im


def team_number():
    im, d = canvas()
    for i, letter in enumerate("ABC"):
        plate(d, 600, 330 + i * 270, "12345" + letter, 760, 200, ["#e03131", "#1c7ed6", "#2f9e44"][i])
    return im


def student_centered_review():
    im, d = canvas()
    for i, x in enumerate((200, 400)):
        person(d, x, 1060, 1.05, ["#4fb3e3", "#69db7c"][i])
    mini_robot(d, 600, 1060, 0.9)
    person(d, 960, 1060, 1.5, ADULT)
    clipboard(d, 800, 650, 1.0)
    d.ellipse((150, 200, 560, 470), fill="white", outline=EDGE, width=6)
    text(d, (355, 335), "We built...", 60, True, BLUE)
    return im


def bean(d, cx, cy, color="#fcc419", w=110, h=80, ang=0):
    poly(d, rot_rect(cx, cy, w, h, ang), color)


def kid_with(d, x, k=1.15, shirt="#4fb3e3"):
    person(d, x, 1060, k, shirt)


def drive_team():
    im, d = canvas()
    for i, (x, c) in enumerate([(230, "#4fb3e3"), (520, "#69db7c"), (810, "#ffa94d")]):
        person(d, x, 1060, 1.3, c)
    controller_icon(d, 230, 700, 0.55)
    bean(d, 810, 680, "#fcc419", 150, 110)
    d.rectangle((90, 1080, 1110, 1100), fill="#e03131")
    return im


def driver_switch():
    im, d = canvas()
    person(d, 300, 1060, 1.4, "#4fb3e3")
    person(d, 900, 1060, 1.4, "#69db7c")
    controller_icon(d, 600, 640, 0.7)
    arrow(d, 430, 520, 760, 520, ORANGE, 14, 50)
    stopwatch(d, 600, 250, 120, "0:30")
    return im


def robot_reset():
    im, d = canvas()
    field(d, 150, 150, 4, 160)
    poly(d, rot_rect(550, 420, 230, 160, 35), PART)  # tipped robot
    for dx, dy in ((-60, 70), (70, -20)):
        d.ellipse((550 + dx - 40, 420 + dy - 40, 550 + dx + 40, 420 + dy + 40), fill=DARK)
    controller_icon(d, 330, 1000, 0.7)
    ground(d, 1080, 120, 600)
    d.rounded_rectangle((800, 840, 1050, 1000), radius=16, outline=GREEN, width=8)
    arrow(d, 640, 520, 900, 820, GREEN, 12, 44)
    return im


def match_stop_time():
    im, d = canvas()
    stopwatch(d, 600, 420, 250, "0:12")
    big_trophy(d, 600, 860, 0.8)
    for x in (300, 900):
        d.rounded_rectangle((x - 120, 850, x + 120, 970), radius=16, fill="#e7f1fb", outline=EDGE, width=5)
        text(d, (x, 910), "40", 70, True, DARK)
    return im


def alliance_score():
    im, d = canvas()
    scoreboard(d, 330, 160, 870, 460, "36")
    mini_robot(d, 380, 900, 1.2, "#4fb3e3")
    mini_robot(d, 820, 900, 1.2, "#f3b27a")
    arrow(d, 520, 480, 400, 700, DARK, 10, 40)
    arrow(d, 680, 480, 800, 700, DARK, 10, 40)
    return im


def possession():
    im, d = canvas()
    robot_top(d, 600, 640, 300, 360, PART)
    d.rectangle((470, 380, 500, 460), fill=EDGE)
    d.rectangle((700, 380, 730, 460), fill=EDGE)
    bean(d, 600, 410, "#fcc419", 150, 100)
    for a in (90, 180, 270):
        spin(d, 600, 640, 330, a - 40, a - 5, GREEN, 10, 34)
    return im


def plowing():
    im, d = canvas()
    robot_top(d, 380, 620, 300, 300, PART, front=False)
    bean(d, 640, 620, "#fcc419", 110, 150, 0)
    arrow(d, 760, 620, 1080, 620, ORANGE, 18, 60)
    for y in (540, 700):
        d.line((180, y, 230, y), fill=FAINT, width=10)
    return im


def preload():
    im, d = canvas()
    field(d, 200, 200, 4, 200)
    robot_top(d, 400, 900, 260, 260, "#4fb3e3")
    bean(d, 400, 900, "#fcc419", 120, 90)
    d.line((660, 1000, 660, 820), fill=EDGE, width=8)
    d.polygon([(660, 820), (780, 860), (660, 900)], fill=GREEN)
    return im


def field_perimeter():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    d.rectangle((150, 150, 1050, 1050), outline=ORANGE, width=40)
    return im


def ref_flag(d, x, y, color, k=1.0):
    d.line((x, y, x, y - 420 * k), fill=DARK, width=int(14 * k))
    d.polygon([(x, y - 420 * k), (x + 280 * k, y - 340 * k), (x, y - 260 * k)], fill=color, outline=EDGE)


def violation():
    im, d = canvas()
    page(d, 120, 260, 560, 900, 6)
    ref_flag(d, 760, 1000, "#ffd43b", 1.5)
    return im


def minor_violation():
    im, d = canvas()
    ref_flag(d, 420, 1000, "#ffd43b", 1.4)
    d.ellipse((690, 300, 1100, 620), fill="white", outline=EDGE, width=6)
    text(d, (895, 460), "careful!", 70, True, ORANGE)
    return im


def major_violation():
    im, d = canvas()
    ref_flag(d, 380, 1000, "#e03131", 1.5)
    scoreboard(d, 680, 380, 1080, 680, "0", "#ff6b6b")
    return im


def score_affecting():
    im, d = canvas()
    scoreboard(d, 140, 380, 640, 700, "36")
    arrow(d, 760, 900, 760, 330, "#e03131", 30, 90)
    ref_flag(d, 980, 1000, "#e03131", 1.0)
    return im


def disqualification():
    im, d = canvas()
    scoreboard(d, 240, 220, 960, 640, "0", "#ff6b6b")
    d.rounded_rectangle((470, 720, 730, 1060), radius=20, fill="#e03131", outline=EDGE, width=6)  # red card
    return im


def disablement():
    im, d = canvas()
    controller_icon(d, 600, 900, 1.2)
    ground(d, 1030, 200, 1000)
    d.regular_polygon((600, 400, 230), 8, rotation=22.5, fill="#e03131", outline=EDGE)
    d.rectangle((470, 370, 730, 430), fill="white")
    return im


def match_replay():
    im, d = canvas()
    field(d, 330, 330, 3, 180)
    spin(d, 600, 600, 420, -60, 240, BLUE, 26, 70)
    return im


def appeal():
    im, d = canvas()
    person(d, 330, 1060, 1.3, "#4fb3e3")
    d.line((390, 700, 470, 470), fill="#4fb3e3", width=40)
    d.ellipse((430, 400, 520, 490), fill=SKIN, outline=EDGE, width=4)
    referee_person(d, 880, 1060, 1.45)
    d.ellipse((170, 120, 560, 380), fill="white", outline=EDGE, width=6)
    text(d, (365, 250), "Q14?", 100, True, BLUE)
    return im


def game_design_committee():
    im, d = canvas()
    for i, x in enumerate((250, 600, 950)):
        person(d, x, 1080, 1.05, ["#868e96", "#495057", "#adb5bd"][i])
    page(d, 380, 140, 820, 560, 5, "#fff9db")
    star(d, 600, 230, 50, ORANGE)
    return im


def legal_parts():
    im, d = canvas()
    beam(d, 130, 330, 6, 1, 90)
    d.rounded_rectangle((180, 520, 520, 620), radius=40, fill="#4fb3e3", outline=EDGE, width=6)
    check(d, 360, 820, 90)
    d.polygon([(760, 380), (1060, 380), (1000, 620), (820, 620)], fill="#adb5bd", outline=EDGE, width=6)  # odd non-VEX part
    d.line((840, 450, 980, 560), fill=EDGE, width=6)
    cross(d, 910, 830, 70)
    d.line((600, 280, 600, 960), fill=FAINT, width=6)
    return im


def role_kid(shirt, prop):
    im, d = canvas()
    person(d, 360, 1080, 1.55, shirt)
    prop(d)
    return im


def designer():
    def p(d):
        page(d, 640, 280, 1080, 760, 0, "#e7f1fb")
        d.rounded_rectangle((720, 450, 1000, 560), radius=14, outline=BLUE, width=8)
        for x in (770, 950):
            d.ellipse((x - 40, 540, x + 40, 620), outline=BLUE, width=8)
        d.line((640, 900, 820, 680), fill=EDGE, width=26)
        d.line((644, 896, 816, 684), fill=YELLOW, width=18)
    return role_kid("#7048e8", p)


def builder():
    def p(d):
        mini_robot(d, 860, 1060, 1.4, PART)
        d.line((600, 760, 760, 600), fill="#adb5bd", width=40)
        d.ellipse((730, 540, 830, 640), fill="#adb5bd", outline=EDGE, width=5)
    return role_kid("#e8590c", p)


def coder():
    def p(d):
        d.rounded_rectangle((620, 480, 1100, 820), radius=20, fill="#1b1f24", outline=EDGE, width=6)
        text(d, (860, 650), "</>", 150, True, "#8ce99a")
        d.polygon([(580, 820), (1140, 820), (1180, 880), (540, 880)], fill="#adb5bd", outline=EDGE, width=5)
    return role_kid("#2f9e44", p)


def strategist():
    def p(d):
        d.rounded_rectangle((620, 260, 1120, 760), radius=16, fill="white", outline=EDGE, width=8)
        for x, y in ((720, 360), (720, 640)):
            d.ellipse((x - 30, y - 30, x + 30, y + 30), outline=BLUE, width=8)
        cross(d, 1000, 380, 30, "#e03131", 10)
        arrow(d, 760, 380, 960, 480, BLUE, 10, 34)
        arrow(d, 760, 620, 980, 560, BLUE, 10, 34)
    return role_kid("#1c7ed6", p)


def notebooker():
    def p(d):
        page(d, 640, 380, 1080, 960, 6, "#fff9db")
        d.line((560, 900, 760, 640), fill=EDGE, width=26)
        d.line((564, 896, 756, 644), fill=YELLOW, width=18)
    return role_kid("#d6336c", p)


# ---- design process, outside ideas, notebook ----

def bulb(d, cx, cy, k=1.0, fill="#ffe066"):
    d.ellipse((cx - 90 * k, cy - 110 * k, cx + 90 * k, cy + 70 * k), fill=fill, outline=EDGE, width=6)
    d.rectangle((cx - 40 * k, cy + 55 * k, cx + 40 * k, cy + 115 * k), fill="#ced4da", outline=EDGE, width=5)


def notebook(d, x0, y0, x1, y1, fill="#fff9db", lines=6):
    page(d, x0, y0, x1, y1, lines, fill)
    for y in range(int(y0) + 40, int(y1) - 20, 70):
        d.ellipse((x0 - 18, y - 12, x0 + 18, y + 12), fill="white", outline=EDGE, width=4)


def magnifier(d, cx, cy, r, color=DARK):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=int(r * 0.18))
    d.line((cx + r * 0.7, cy + r * 0.7, cx + r * 1.6, cy + r * 1.6), fill=color, width=int(r * 0.3))


def video(d, x0, y0, x1, y1):
    d.rounded_rectangle((x0, y0, x1, y1), radius=24, fill="#1b1f24", outline=EDGE, width=6)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill="#e03131")
    d.polygon([(cx - 22, cy - 38), (cx - 22, cy + 38), (cx + 42, cy)], fill="white")
    d.rectangle((x0 + 30, y1 - 40, x1 - 30, y1 - 28), fill="#868e96")
    d.rectangle((x0 + 30, y1 - 40, x0 + (x1 - x0) * 0.45, y1 - 28), fill="#e03131")


def define_the_problem():
    im, d = canvas()
    d.ellipse((380, 120, 820, 520), fill="#e7f1fb", outline=EDGE, width=6)
    text(d, (600, 320), "?", 280, True, BLUE)
    page(d, 300, 620, 900, 1060, 4)
    return im


def criteria():
    im, d = canvas()
    page(d, 250, 160, 950, 1060, 0)
    for i in range(4):
        y = 300 + i * 200
        d.rounded_rectangle((330, y - 50, 430, y + 50), radius=10, outline=EDGE, width=6)
        check(d, 385, y, 45, GREEN, 14)
        d.line((480, y, 860, y), fill=FAINT, width=14)
    return im


def proto(d, cx, cy, k, kind):
    if kind == 0:
        d.rectangle((cx - 90 * k, cy - 50 * k, cx + 90 * k, cy + 50 * k), outline=BLUE, width=8)
    elif kind == 1:
        d.rounded_rectangle((cx - 90 * k, cy - 50 * k, cx + 90 * k, cy + 50 * k), radius=30 * k, outline=BLUE, width=8)
        d.line((cx + 90 * k, cy, cx + 150 * k, cy - 60 * k), fill=BLUE, width=8)
    else:
        d.rounded_rectangle((cx - 90 * k, cy - 50 * k, cx + 90 * k, cy + 50 * k), radius=30 * k, fill="#d0ebff", outline=BLUE, width=8)
        d.line((cx + 90 * k, cy, cx + 150 * k, cy - 60 * k), fill=BLUE, width=8)
        d.line((cx + 150 * k, cy - 60 * k, cx + 200 * k, cy - 20 * k), fill=BLUE, width=8)
    for dx in (-55, 55):
        d.ellipse((cx + dx * k - 30 * k, cy + 40 * k, cx + dx * k + 30 * k, cy + 100 * k), outline=BLUE, width=8)


def develop_solutions():
    im, d = canvas()
    for i, x in enumerate((220, 600, 980)):
        page(d, x - 170, 380, x + 170, 760, 0)
        proto(d, x - 20, 550, 0.9, i)
    for x in (390, 770):
        arrow(d, x + 10, 570, x + 40, 570, ORANGE, 12, 40)
    stopwatch(d, 600, 960, 110, "")
    return im


def optimize():
    im, d = canvas()
    d.line((200, 1000, 1000, 1000), fill=EDGE, width=8)
    d.line((200, 1000, 200, 250), fill=EDGE, width=8)
    pts = [(260, 900), (420, 780), (580, 720), (740, 520), (920, 330)]
    d.line(pts, fill=GREEN, width=14)
    for x, y in pts:
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=GREEN, outline=EDGE, width=4)
    return im


def test_procedure():
    im, d = canvas()
    page(d, 220, 140, 980, 1060, 0)
    for i in range(4):
        y = 300 + i * 200
        d.ellipse((290, y - 55, 400, y + 55), fill=BLUE)
        text(d, (345, y), str(i + 1), 70, True, "white")
        d.line((450, y, 880, y), fill=FAINT, width=14)
    return im


def table(d, x0, y0, cols, rows, cw, rh, head=None, cells=None):
    for r in range(rows):
        for c in range(cols):
            fill = "#e7f1fb" if r == 0 else "white"
            d.rectangle((x0 + c * cw, y0 + r * rh, x0 + (c + 1) * cw, y0 + (r + 1) * rh), fill=fill, outline=EDGE, width=5)
            if cells and cells[r][c]:
                text(d, (x0 + c * cw + cw / 2, y0 + r * rh + rh / 2), cells[r][c], int(rh * 0.42), r == 0, DARK)


def trial():
    im, d = canvas()
    table(d, 180, 260, 2, 5, 420, 140, cells=[["#", "Points"], ["1", "8"], ["2", "12"], ["3", "11"], ["4", "12"]])
    return im


def quantitative_data():
    im, d = canvas()
    d.line((200, 1000, 1000, 1000), fill=EDGE, width=8)
    for i, (h, v) in enumerate([(300, "8"), (480, "12"), (430, "11"), (560, "14")]):
        x = 260 + i * 190
        d.rectangle((x, 1000 - h, x + 130, 1000), fill="#4dabf7", outline=EDGE, width=5)
        text(d, (x + 65, 1000 - h - 50), v, 70, True, DARK)
    return im


def qualitative_data():
    im, d = canvas()
    notebook(d, 220, 160, 980, 1060)
    for i, (txt, c) in enumerate([("claw slips", "#e03131"), ("wobbly arm", "#e03131"), ("smooth turns", GREEN)]):
        text(d, (600, 380 + i * 200), txt, 72, True, c)
    return im


def tradeoff():
    im, d = canvas()
    d.polygon([(560, 1000), (640, 1000), (600, 520)], fill=DARK)
    d.line((220, 440, 980, 600), fill=DARK, width=16)
    for x, y, c, sym in [(260, 450, "#ffa94d", "fast"), (940, 610, "#4dabf7", "strong")]:
        d.line((x, y, x, y + 140), fill=DARK, width=6)
        d.rounded_rectangle((x - 150, y + 140, x + 150, y + 320), radius=20, fill=c, outline=EDGE, width=6)
        text(d, (x, y + 230), sym, 64, True, DARK)
    return im


def reflection():
    im, d = canvas()
    person(d, 330, 1080, 1.5, "#4fb3e3")
    d.ellipse((560, 120, 1100, 600), fill="white", outline=EDGE, width=6)
    for x, y, r in ((520, 640, 30), (470, 720, 20)):
        d.ellipse((x - r, y - r, x + r, y + r), fill="white", outline=EDGE, width=5)
    spin(d, 830, 360, 150, -60, 230, BLUE, 18, 50)
    check(d, 830, 360, 60, GREEN, 18)
    return im


def research():
    im, d = canvas()
    video(d, 140, 230, 760, 680)
    mini_robot(d, 450, 560, 0.9, "#f3b27a")
    magnifier(d, 820, 720, 170)
    return im


def team_circle(d):
    d.ellipse((240, 320, 960, 1040), fill="#f1f3f5", outline=EDGE, width=6)
    for i, x in enumerate((420, 600, 780)):
        person(d, x, 920, 0.75, ["#4fb3e3", "#69db7c", "#ffa94d"][i])


def outside_idea():
    im, d = canvas()
    team_circle(d)
    bulb(d, 1040, 200, 1.0)
    arrow(d, 960, 300, 760, 500, ORANGE, 16, 54)
    return im


def reveal_video():
    im, d = canvas()
    video(d, 120, 230, 1080, 900)
    mini_robot(d, 600, 760, 1.6, "#4fb3e3")
    for x, y in ((300, 380), (900, 380)):
        star(d, x, y, 50, YELLOW)
    return im


def inspired_adaptation():
    im, d = canvas()
    mini_robot(d, 300, 640, 1.3, "#f3b27a")
    d.rectangle((240, 360, 270, 470), fill=EDGE)
    arrow(d, 480, 560, 700, 560, GREEN, 16, 56)
    mini_robot(d, 900, 640, 1.3, "#4fb3e3")
    d.rectangle((840, 360, 870, 470), fill=EDGE)
    d.line((870, 365, 1010, 365), fill=EDGE, width=26)  # added arm
    star(d, 1060, 300, 60, YELLOW, outline=EDGE, width=3)
    bulb(d, 300, 220, 0.7)
    return im


def direct_copying():
    im, d = canvas()
    for x in (300, 900):
        mini_robot(d, x, 640, 1.3, "#f3b27a")
        d.rectangle((x - 60, 360, x - 30, 470), fill=EDGE)
    text(d, (600, 560), "=", 200, True, "#e03131")
    cross(d, 600, 860, 80)
    return im


def ownership_check():
    im, d = canvas()
    boxes = [(330, 330), (870, 330), (330, 870), (870, 870)]
    for x, y in boxes:
        d.rounded_rectangle((x - 230, y - 230, x + 230, y + 230), radius=30, fill="#f1f3f5", outline=EDGE, width=6)
    # adapt: wrench, test: stopwatch, understand: bulb, credit: tag
    d.line((230, 430, 420, 240), fill="#868e96", width=44)
    d.ellipse((380, 190, 470, 280), fill="#868e96", outline=EDGE, width=5)
    stopwatch(d, 870, 360, 140, "")
    bulb(d, 330, 880, 1.2)
    d.polygon([(720, 800), (950, 800), (1040, 880), (950, 960), (720, 960)], fill=YELLOW, outline=EDGE)
    d.ellipse((940, 860, 980, 900), fill="white", outline=EDGE, width=4)
    return im


def help_check():
    im, d = canvas()
    person(d, 300, 1080, 1.5, ADULT)
    d.rounded_rectangle((470, 160, 1100, 560), radius=16, fill="white", outline=EDGE, width=8)  # whiteboard
    for cx, cy, r in ((640, 360, 110), (900, 360, 60)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLUE, width=8)
    person(d, 800, 1080, 1.05, "#4fb3e3")
    mini_robot(d, 1010, 1080, 0.8)
    return im


def design_convergence():
    im, d = canvas()
    for x, y, c in ((220, 260, "#f3b27a"), (980, 260, "#69db7c"), (220, 960, "#ffd43b"), (980, 960, "#b197fc")):
        mini_robot(d, x, y + 60, 0.75, c)
        arrow(d, x + (120 if x < 600 else -120), y + (60 if y < 600 else -60), 600 + (-150 if x < 600 else 150), 600 + (-90 if y < 600 else 90), DARK, 10, 36)
    mini_robot(d, 600, 680, 1.3, "#4fb3e3")
    return im


def starting_point():
    im, d = canvas()
    mini_robot(d, 330, 760, 1.4, "#adb5bd")
    d.line((330, 560, 330, 360), fill=EDGE, width=8)
    d.polygon([(330, 360), (470, 400), (330, 440)], fill=GREEN)
    arrow(d, 560, 680, 760, 680, ORANGE, 14, 50)
    mini_robot(d, 960, 760, 1.4, "#4fb3e3")
    d.rectangle((900, 470, 930, 610), fill=EDGE)
    d.line((930, 475, 1080, 430), fill=EDGE, width=24)
    return im


def notebook_entry():
    im, d = canvas()
    notebook(d, 240, 140, 960, 1060, lines=0)
    d.rounded_rectangle((300, 200, 640, 290), radius=12, fill="#e7f1fb", outline=EDGE, width=4)
    text(d, (470, 245), "Oct 3", 56, True, DARK)
    for i in range(5):
        d.line((310, 380 + i * 100, 890, 380 + i * 100), fill=FAINT, width=12)
    d.ellipse((700, 880, 900, 1000), outline=BLUE, width=6)
    text(d, (800, 940), "AL", 64, True, BLUE)
    return im


def table_of_contents():
    im, d = canvas()
    page(d, 220, 140, 980, 1060, 0)
    for i in range(6):
        y = 260 + i * 130
        d.line((300, y, 680, y), fill="#adb5bd", width=14)
        for x in range(700, 830, 30):
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#adb5bd")
        text(d, (880, y), str(1 + i * 7), 60, True, DARK)
    return im


def appendix():
    im, d = canvas()
    for i in range(5):
        x = 300 + i * 22
        d.rounded_rectangle((x, 200 + i * 10, x + 560, 1000 + i * 10), radius=14, fill="white", outline=EDGE, width=5)
    d.rounded_rectangle((950, 760, 1060, 880), radius=10, fill=ORANGE, outline=EDGE, width=5)
    return im


def credit():
    im, d = canvas()
    bulb(d, 330, 500, 1.6)
    d.polygon([(560, 640), (1000, 640), (1100, 760), (1000, 880), (560, 880)], fill=YELLOW, outline=EDGE, width=6)
    d.ellipse((990, 735, 1040, 785), fill="white", outline=EDGE, width=4)
    text(d, (780, 760), "1234A", 80, True, DARK)
    d.line((330, 650, 560, 760), fill=EDGE, width=6)
    return im


def season_summary():
    im, d = canvas()
    page(d, 140, 180, 600, 1020, 0, "#e7f1fb")
    for i in range(4):
        star(d, 220, 300 + i * 190, 36, ORANGE)
        d.line((280, 300 + i * 190, 540, 300 + i * 190), fill="#74c0fc", width=14)
        arrow(d, 600, 300 + i * 190, 760, 300 + i * 190, DARK, 8, 30)
    notebook(d, 800, 200, 1080, 1000)
    return im


def code_summary():
    im, d = canvas()
    page(d, 220, 140, 980, 1060, 0, "#ebfbee")
    for i, (w, c) in enumerate([(300, "#ffd43b"), (360, "#4dabf7"), (300, "#4dabf7"), (240, "#69db7c")]):
        y = 280 + i * 200
        d.rounded_rectangle((600 - w / 2, y - 55, 600 + w / 2, y + 55), radius=26, fill=c, outline=EDGE, width=5)
        if i < 3:
            arrow(d, 600, y + 60, 600, y + 140, DARK, 8, 30)
    return im


def credit_summary():
    im, d = canvas()
    page(d, 220, 140, 980, 1060, 0)
    for i in range(5):
        y = 280 + i * 160
        d.polygon([(300, y - 40), (400, y - 40), (440, y), (400, y + 40), (300, y + 40)], fill=YELLOW, outline=EDGE, width=4)
        d.line((480, y, 880, y), fill=FAINT, width=14)
    return im


def fully_developed_notebook():
    im, d = canvas()
    for i in range(8):
        d.rectangle((330 + i * 8, 250 + i * 14, 830 + i * 8, 980 + i * 14), fill="#fff9db" if i == 7 else "white", outline=EDGE, width=4)
    spin(d, 640, 690, 180, -80, 240, GREEN, 20, 56)
    return im


def digital_notebook():
    im, d = canvas()
    d.rounded_rectangle((180, 220, 1020, 780), radius=24, fill="#1b1f24", outline=EDGE, width=6)
    page(d, 300, 280, 900, 740, 5, "#fff9db")
    d.polygon([(100, 800), (1100, 800), (1160, 900), (40, 900)], fill="#adb5bd", outline=EDGE, width=6)
    return im


def annotate():
    im, d = canvas()
    d.rectangle((300, 300, 900, 900), fill="#f1f3f5", outline=EDGE, width=5)
    mini_robot(d, 600, 760, 1.6, PART)
    for (x, y), (tx, ty), s in [((480, 600), (200, 200), "gear"), ((720, 720), (1000, 1050), "wheel")]:
        d.line((x, y, tx, ty + (40 if ty < 600 else -40)), fill=ORANGE, width=8)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=ORANGE)
        text(d, (tx, ty), s, 70, True, ORANGE)
    return im


# ---- season game: Level Up (2026-27) ----
RED_BAG, BLUE_BAG, YEL_BAG = "#e03131", "#1c7ed6", "#fcc419"


def pyramid(hi):
    """Side view of a Pyramid Goal with one level (0 = L1, 1 = L2, 2 = L3) highlighted."""
    im, d = canvas()
    for i, (w, y) in enumerate([(900, 980), (640, 760), (380, 540)]):
        top = y - 200
        d.rectangle((600 - w / 2, top, 600 + w / 2, y), fill="#c92a2a", outline=EDGE, width=6)
        d.rectangle((600 - w / 2, top - 30, 600 + w / 2, top), fill=YELLOW if i == hi else "#495057", outline=EDGE, width=6)
    ground(d, 990, 80, 1120)
    levels = [(900, 980), (640, 760), (380, 540)]
    w, y = levels[hi]
    surface = y - 230
    inner = levels[hi + 1][0] if hi < 2 else 0          # the next level up covers the middle
    xs = [600 - (w + inner) / 4, 600 + (w + inner) / 4] if hi < 2 else [540, 660]
    for x in xs:
        bean(d, x, surface - 38, RED_BAG, 100 if hi < 2 else 110, 70)
    return im


def l1_goal(): return pyramid(0)
def l2_goal(): return pyramid(1)
def l3_goal(): return pyramid(2)


def match_load():
    im, d = canvas()
    field(d, 420, 220, 4, 180)
    d.rectangle((420, 220, 600, 940), fill="#ffc9c9", outline=EDGE, width=6)  # load zone strip
    d.rounded_rectangle((60, 220, 360, 940), radius=20, outline="#e03131", width=10)  # driver station
    for i in range(8):
        bean(d, 150 + (i % 2) * 120, 290 + (i // 2) * 160, RED_BAG, 100, 72)
    arrow(d, 300, 1040, 520, 1040, DARK, 12, 44)
    return im


def loader():
    im, d = canvas()
    d.rectangle((640, 640, 1150, 1080), fill="#f1f3f5", outline=EDGE, width=6)
    d.rectangle((640, 640, 820, 1080), fill="#ffc9c9", outline=EDGE, width=5)
    person(d, 330, 1080, 1.4, "#ffa94d")
    d.line((410, 720, 650, 760), fill="#ffa94d", width=40)
    bean(d, 730, 790, RED_BAG, 120, 86)
    for i in range(3):
        bean(d, 160 + i * 20, 1050 - i * 40, RED_BAG, 110, 70)
    return im


def shortcut():
    im, d = canvas()
    field(d, 150, 150, 6, 150)
    d.rectangle((150, 520, 690, 620), fill="#495057")  # walls with a narrow gap
    d.rectangle((790, 520, 1050, 620), fill="#495057")
    robot_top(d, 740, 900, 90, 120, "#4fb3e3")
    arrow(d, 740, 820, 740, 330, GREEN, 14, 50)
    robot_top(d, 360, 900, 220, 220, "#f3b27a")
    d.line((360, 780, 360, 680, 160, 680), fill=ORANGE, width=10)
    return im


def color_match():
    im, d = canvas()
    for x, gc in ((330, "#ffc9c9"), (870, "#d0ebff")):
        d.rounded_rectangle((x - 230, 380, x + 230, 900), radius=20, fill=gc, outline=EDGE, width=6)
    bean(d, 330, 640, RED_BAG, 180, 130)
    check(d, 330, 260, 70)
    bean(d, 870, 640, RED_BAG, 180, 130)
    cross(d, 870, 260, 60)
    return im


def one_bag_limit():
    im, d = canvas()
    for x, n in ((320, 1), (880, 2)):
        robot_top(d, x, 640, 280, 320, PART, front=False)
        for i in range(n):
            bean(d, x - (0 if n == 1 else 70) + i * 140, 440, YEL_BAG if i == 0 else BLUE_BAG, 130, 90)
    check(d, 320, 950, 70)
    cross(d, 880, 950, 60)
    d.line((600, 200, 600, 1050), fill=FAINT, width=6)
    return im


def out_of_the_field():
    im, d = canvas()
    field(d, 150, 300, 4, 180)
    bean(d, 1000, 300, BLUE_BAG, 130, 95, 25)
    arrow(d, 760, 520, 940, 340, ORANGE, 12, 44)
    cross(d, 1000, 300, 90, "#e03131", 14)
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
    # engineering
    "chassis": chassis,
    "holonomic drive": holonomic_drive,
    "omni-directional": omni_directional,
    "footprint": footprint,
    "ground clearance": ground_clearance,
    "shield": shield,
    "game piece slide": game_piece_slide,
    "basket": basket,
    "outtake": outtake,
    "conveyor": conveyor,
    "single-sided claw": single_sided_claw,
    "double-sided claw": double_sided_claw,
    "roller claw": roller_claw,
    "tower": tower,
    "6-bar": six_bar,
    "chain-bar": chain_bar,
    "linear slide": linear_slide,
    "cascade lift": cascade_lift,
    "scissor lift": scissor_lift,
    "flywheel launcher": flywheel_launcher,
    "driving gear": driving_gear,
    "driven gear": driven_gear,
    "gear ratio": gear_ratio,
    "mechanical advantage": mechanical_advantage,
    "compound gear ratio": compound_gear_ratio,
    "idler gear": idler_gear,
    "force": force,
    "unbalanced force": unbalanced_force,
    "traction": traction,
    "friction": friction,
    "mass": mass,
    "center of mass": center_of_mass,
    "autonomous": autonomous,
    "starting position": starting_position,
    "bang-bang control": bang_bang_control,
    "PID control": pid_control,
    "proportional control": proportional_control,
    "setpoint": setpoint,
    "error (control)": error_control,
    "odometry": odometry,
    # design process and competition
    "constraint": constraint,
    "brainstorm": brainstorm,
    "iterate": iterate,
    "scouting": scouting,
    "pit": pit,
    "match schedule": match_schedule,
    "queuing area": queuing_area,
    "driver": driver,
    "coach": coach,
    "judge": judge,
    "alliance partner": alliance_partner,
    "game piece": game_piece,
    "game manual": game_manual,
    "license plate": license_plate,
    "Excellence Award": excellence_award,
    "Design Award": design_award,
    "Innovate Award": innovate_award,
    "Think Award": think_award,
    "Amaze Award": amaze_award,
    "Build Award": build_award,
    "Create Award": create_award,
    "Judges Award": judges_award,
    "Inspire Award": inspire_award,
    "Sportsmanship Award": sportsmanship_award,
    "Energy Award": energy_award,
    "Teamwork Champions": teamwork_champions,
    "Robot Skills Champion": robot_skills_champion,
    "judged award": judged_award,
    "performance award": performance_award,
    "nominated award": nominated_award,
    "scrimmage": scrimmage,
    "in-school competition": in_school_competition,
    "qualifying event": qualifying_event,
    "school-based event": school_based_event,
    "Robot Skills-Only Event": skills_only_event,
    "Championship Event": championship_event,
    "Spotlight Event": spotlight_event,
    "Signature Event": signature_event,
    "VEX Robotics World Championship": world_championship,
    "qualifying spot": qualifying_spot,
    "qualifying award": qualifying_award,
    "World Skills Standings": world_skills_standings,
    "level (Elementary / Middle School)": level_es_ms,
    "qualification match": qualification_match,
    "finals match": finals_match,
    "Robot Skills Challenge": robot_skills_challenge,
    "Driving Skills match": driving_skills,
    "Autonomous Coding Skills match": autonomous_skills,
    "Skills Stop Time": skills_stop_time,
    "ranking": ranking,
    "practice match": practice_match,
    "no-show": no_show,
    "Event Partner": event_partner,
    "head referee": head_referee,
    "scorekeeper referee": scorekeeper_referee,
    "Judge Advisor": judge_advisor,
    "emcee": emcee,
    "volunteer": volunteer,
    "Code of Conduct": code_of_conduct,
    "Student-Centered Policy": student_centered_policy,
    "official Q&A": official_qa,
    "team number": team_number,
    "Student-Centered Review": student_centered_review,
    "drive team": drive_team,
    "driver switch": driver_switch,
    "robot reset": robot_reset,
    "Match Stop Time": match_stop_time,
    "Alliance Score": alliance_score,
    "possession": possession,
    "plowing": plowing,
    "preload": preload,
    "field perimeter": field_perimeter,
    "violation": violation,
    "Minor Violation": minor_violation,
    "Major Violation": major_violation,
    "Score Affecting": score_affecting,
    "Disqualification": disqualification,
    "Disablement": disablement,
    "match replay": match_replay,
    "appeal": appeal,
    "Game Design Committee": game_design_committee,
    "legal parts": legal_parts,
    "designer": designer,
    "builder": builder,
    "coder": coder,
    "strategist": strategist,
    "notebooker": notebooker,
    "define the problem": define_the_problem,
    "criteria": criteria,
    "develop solutions": develop_solutions,
    "optimize": optimize,
    "test procedure": test_procedure,
    "trial": trial,
    "quantitative data": quantitative_data,
    "qualitative data": qualitative_data,
    "tradeoff": tradeoff,
    "reflection": reflection,
    "research": research,
    "outside idea": outside_idea,
    "reveal video": reveal_video,
    "inspired adaptation": inspired_adaptation,
    "direct copying": direct_copying,
    "Ownership Check": ownership_check,
    "Help Check": help_check,
    "design convergence": design_convergence,
    "starting point": starting_point,
    "notebook entry": notebook_entry,
    "table of contents": table_of_contents,
    "appendix": appendix,
    "credit": credit,
    "Season Summary": season_summary,
    "Code Summary": code_summary,
    "Credit Summary": credit_summary,
    "fully developed notebook": fully_developed_notebook,
    "digital engineering notebook": digital_notebook,
    "annotate": annotate,
    "Match Load": match_load,
    "L1 Goal": l1_goal,
    "L2 Goal": l2_goal,
    "L3 Goal": l3_goal,
    "loader": loader,
    "shortcut": shortcut,
    "color match": color_match,
    "one-bag limit": one_bag_limit,
    "out of the field": out_of_the_field,
}


def main():
    import csv
    ids = {r["term_en"]: r["id"] for r in csv.DictReader(open(ROOT / "data/vocab.csv", encoding="utf-8"))}
    for term, fn in DIAGRAMS.items():
        out = ROOT / "images" / f"{ids[term]}.png"
        im = fn()
        if ids[term].startswith(("CODE-", "ENG-", "EDP-", "COMP-", "SEASON-")) and term != "sensor":
            im = fit(im)
        im.resize((S // 2, S // 2), Image.LANCZOS).quantize(colors=96, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
        print(f"{ids[term]}  {term}  → images/{out.name}")


if __name__ == "__main__":
    main()
