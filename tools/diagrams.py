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
}


def main():
    import csv
    ids = {r["term_en"]: r["id"] for r in csv.DictReader(open(ROOT / "data/vocab.csv", encoding="utf-8"))}
    for term, fn in DIAGRAMS.items():
        out = ROOT / "images" / f"{ids[term]}.png"
        im = fn()
        if ids[term].startswith(("CODE-", "ENG-", "EDP-", "COMP-")) and term != "sensor":
            im = fit(im)
        im.resize((S // 2, S // 2), Image.LANCZOS).quantize(colors=96, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
        print(f"{ids[term]}  {term}  → images/{out.name}")


if __name__ == "__main__":
    main()
