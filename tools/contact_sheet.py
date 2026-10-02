#!/usr/bin/env python3
"""Make a contact sheet of every vocab image, labeled with ID and term, for checking.

Usage: python3 tools/contact_sheet.py [DOMAIN]     e.g.  python3 tools/contact_sheet.py BLD
Writes build/contact-sheet[-DOMAIN].png (build/ is not committed). Needs Pillow.
"""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
COLS, CELL, LABEL = 6, 260, 44


def font(size):
    for f in ["/System/Library/Fonts/Supplemental/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def main():
    domain = sys.argv[1] if len(sys.argv) > 1 else None
    rows = [r for r in csv.DictReader(open(ROOT / "data/vocab.csv", encoding="utf-8"))
            if r["image"] and (domain is None or r["domain"] == domain)]
    if not rows:
        sys.exit("no rows with images")
    nrows = (len(rows) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL, nrows * (CELL + LABEL)), "white")
    draw, f_id, f_term = ImageDraw.Draw(sheet), font(15), font(17)
    for i, r in enumerate(rows):
        x, y = (i % COLS) * CELL, (i // COLS) * (CELL + LABEL)
        im = Image.open(ROOT / "images" / r["image"]).convert("RGB")
        im.thumbnail((CELL - 20, CELL - 20))
        sheet.paste(im, (x + (CELL - im.width) // 2, y + 10 + (CELL - 20 - im.height) // 2))
        draw.text((x + 10, y + CELL - 4), r["id"], fill="#888", font=f_id)
        draw.text((x + 10, y + CELL + 14), r["term_en"], fill="black", font=f_term)
        draw.rectangle((x, y, x + CELL - 1, y + CELL + LABEL - 1), outline="#ddd")
    out = ROOT / "build" / f"contact-sheet{'-' + domain if domain else ''}.png"
    out.parent.mkdir(exist_ok=True)
    sheet.save(out)
    print(f"{len(rows)} images → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
