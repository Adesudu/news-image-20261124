#!/usr/bin/env python3
"""Render the news-image-20261124 entry: a one-page newspaper front page.

Draws a 1024x1024 newspaper front page, "THE WORLD - TUESDAY 24 NOVEMBER
2026", summing up the world news of Tuesday 24 November 2026, and writes
entry.png beside this script. Uses Pillow (build-time only); the graded
program main.py only copies the finished PNG.

Layout notes (all geometry in pixels, canvas 1024x1024):
- masthead 0-153, lead story 192-428, grid rows 440-664 and 676-900,
  ALSO TODAY strip 912-1012.
- Every illustration is drawn on its own layer and pasted, so no drawing
  can spill outside its band; headlines and bodies auto-shrink until they
  fit their panel (max 2 lines each).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# --- palette ---------------------------------------------------------------
CREAM = (246, 241, 227)      # newsprint paper
PAPER = (255, 253, 246)      # panel paper
NAVY = (22, 35, 63)          # masthead band
NAVY_SOFT = (38, 56, 92)
RED = (176, 42, 48)          # kicker red
GOLD = (201, 162, 39)        # masthead rule
INK = (24, 24, 24)           # body text
GREY = (96, 96, 88)
RULE = (185, 174, 148)       # panel borders
SKY = (220, 233, 245)        # illustration sky
SEA = (205, 226, 238)        # illustration sea

W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, size, max_w, max_lines):
    """Largest font size (stepping down from `size`) whose wrap fits."""
    while size >= 14:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    return font(path, 14), wrap(draw, text, font(path, 14), max_w)


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def draw_tracked(draw, cx, y, text, fnt, fill, tracking=4):
    """Draw text with extra letter spacing, centred on cx."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + tracking


# --- illustrations (Pillow primitives only; all coords inside the box) ------

def draw_awacs(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # missile arcs (red) arcing in from the left
    draw.arc([x0 + 8, y0 + 6, x0 + w * 0.45, y0 + h * 0.56], 200, 340,
             fill=RED, width=4)
    draw.arc([x0 + w * 0.09, y0 + h * 0.17, x0 + w * 0.58, y0 + h * 0.73],
             200, 340, fill=RED, width=3)
    draw.ellipse([x0 + w * 0.42, y0 + h * 0.41, x0 + w * 0.45, y0 + h * 0.44],
                 fill=RED)
    draw.ellipse([x0 + w * 0.53, y0 + h * 0.55, x0 + w * 0.56, y0 + h * 0.58],
                 fill=RED)
    # AWACS plane: fuselage, wings, radar dome on top
    cx, cy = x0 + w * 0.58, y0 + h * 0.52
    draw.polygon([(cx - 130, cy + 6), (cx - 60, cy - 14), (cx + 90, cy - 14),
                  (cx + 150, cy + 2), (cx + 90, cy + 14), (cx - 60, cy + 14)],
                 fill=(240, 240, 238), outline=NAVY, width=3)
    draw.polygon([(cx - 20, cy - 12), (cx + 10, cy - 62), (cx + 46, cy - 62),
                  (cx + 30, cy - 12)], fill=(200, 208, 220), outline=NAVY, width=2)
    draw.polygon([(cx - 20, cy + 12), (cx + 10, cy + 52), (cx + 46, cy + 52),
                  (cx + 30, cy + 12)], fill=(200, 208, 220), outline=NAVY, width=2)
    draw.polygon([(cx + 96, cy - 12), (cx + 138, cy - 44), (cx + 146, cy - 12)],
                 fill=(200, 208, 220), outline=NAVY, width=2)
    draw.line([(cx - 6, cy - 14), (cx - 6, cy - 46)], fill=NAVY, width=4)
    draw.ellipse([cx - 26, cy - 78, cx + 14, cy - 38], fill=(226, 232, 240),
                 outline=NAVY, width=3)
    draw.ellipse([cx + 96, cy - 8, cx + 116, cy + 8], fill=(120, 130, 145),
                 outline=NAVY, width=2)
    for r in (34, 48):
        draw.arc([cx - 6 - r, cy - 58 - r, cx - 6 + r, cy - 58 + r],
                 200, 340, fill=NAVY_SOFT, width=3)
    for bx, by in ((x0 + w * 0.05, y0 + h * 0.56), (x1 - w * 0.36, y1 - h * 0.20)):
        draw.ellipse([bx, by, bx + 70, by + 22], fill=(255, 255, 255))
        draw.ellipse([bx + 18, by - 12, bx + 78, by + 12], fill=(255, 255, 255))


def draw_warship(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    mid = y0 + h * 0.60
    # explosion starburst where the drone hit
    ex, ey = x0 + w * 0.26, y0 + h * 0.20
    for ang in range(0, 360, 30):
        dx = math.cos(math.radians(ang)) * h * 0.24
        dy = math.sin(math.radians(ang)) * h * 0.24
        draw.line([(ex, ey), (ex + dx, ey + dy)], fill=(232, 120, 30), width=4)
    draw.ellipse([ex - h * 0.16, ey - h * 0.16, ex + h * 0.16, ey + h * 0.16],
                 fill=(245, 178, 60))
    draw.ellipse([ex - h * 0.08, ey - h * 0.08, ex + h * 0.08, ey + h * 0.08],
                 fill=(255, 226, 120))
    # smoke, kept inside the band
    for bx, by, r in ((x0 + w * 0.30, y0 + h * 0.10, h * 0.09),
                      (x0 + w * 0.38, y0 + h * 0.05, h * 0.11)):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=(120, 120, 118))
    # hull, listing after the hit
    draw.polygon([(x0 + w * 0.13, mid), (x1 - w * 0.10, mid - 2),
                  (x1 - w * 0.23, mid + h * 0.20), (x0 + w * 0.20, mid + h * 0.20)],
                 fill=(70, 76, 88), outline=NAVY, width=2)
    draw.rectangle([x0 + w * 0.40, mid - h * 0.24, x0 + w * 0.63, mid - 1],
                   fill=(96, 104, 116), outline=NAVY, width=2)
    draw.line([(x0 + w * 0.52, mid - h * 0.24), (x0 + w * 0.52, mid - h * 0.38)],
              fill=NAVY, width=3)
    draw.line([(x0 + w * 0.66, mid - 1), (x0 + w * 0.71, mid - h * 0.22)],
              fill=NAVY, width=3)
    # waves, inside the band
    for wy in (y0 + h * 0.86, y0 + h * 0.95):
        for wx in range(int(x0 + 4), int(x1 - 20), 36):
            draw.arc([wx, wy, wx + 32, wy + 10], 180, 360, fill=NAVY_SOFT, width=2)


def draw_tanker(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    mid = y0 + h * 0.58
    # flames on deck
    for fx in (x0 + w * 0.32, x0 + w * 0.50, x0 + w * 0.68):
        draw.polygon([(fx - h * 0.10, mid - 2), (fx, mid - h * 0.36),
                      (fx + h * 0.10, mid - 2)], fill=(232, 120, 30))
        draw.polygon([(fx - h * 0.05, mid - 2), (fx, mid - h * 0.22),
                      (fx + h * 0.05, mid - 2)], fill=(245, 200, 60))
    # long hull
    draw.rectangle([x0 + w * 0.08, mid - 2, x1 - w * 0.08, mid + h * 0.20],
                   fill=(122, 52, 44), outline=NAVY, width=2)
    draw.rectangle([x0 + w * 0.08, mid + h * 0.12, x1 - w * 0.08, mid + h * 0.20],
                   fill=(70, 40, 36))
    # deck tanks
    for tx in (x0 + w * 0.20, x0 + w * 0.39, x0 + w * 0.58):
        draw.ellipse([tx, mid - h * 0.20, tx + w * 0.14, mid - 2],
                     fill=(226, 226, 220), outline=NAVY, width=2)
    # bridge tower
    draw.rectangle([x1 - w * 0.20, mid - h * 0.40, x1 - w * 0.10, mid - 2],
                   fill=(240, 240, 238), outline=NAVY, width=2)
    draw.rectangle([x1 - w * 0.22, mid - h * 0.46, x1 - w * 0.08, mid - h * 0.40],
                   fill=NAVY)
    # smoke
    for bx, by, r in ((x0 + w * 0.32, y0 + h * 0.06, h * 0.09),
                      (x0 + w * 0.42, y0 + h * 0.02, h * 0.11)):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=(110, 110, 108))
    # naval mine in the water
    mx, my = x1 - w * 0.30, y0 + h * 0.90
    draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(40, 40, 40))
    for dx, dy in ((-10, 0), (10, 0), (0, -10), (0, 10)):
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(40, 40, 40), width=2)
    for wy in (y0 + h * 0.86,):
        for wx in range(int(x0 + 4), int(x1 - 20), 36):
            draw.arc([wx, wy, wx + 32, wy + 10], 180, 360, fill=NAVY_SOFT, width=2)


def draw_globe(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(232, 240, 244))
    cx, cy = x0 + w * 0.38, y0 + h * 0.50
    r = h * 0.42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(127, 179, 213),
                 outline=NAVY, width=2)
    draw.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.05, cy + r * 0.10, cx + r * 0.70, cy + r * 0.65],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.25, cy - r * 0.70, cx + r * 0.65, cy - r * 0.30],
                 fill=(120, 175, 105))
    draw.arc([cx - r, cy - r * 0.42, cx + r, cy + r * 0.42], 0, 360,
             fill=(255, 255, 255), width=2)
    draw.ellipse([cx - r * 0.42, cy - r, cx + r * 0.42, cy + r],
                 outline=(255, 255, 255), width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    # hot sun: the talks failed
    sx, sy = x1 - w * 0.20, y0 + h * 0.28
    sr = h * 0.16
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(245, 178, 60),
                 outline=(200, 120, 20), width=2)
    for ang in range(0, 360, 45):
        dx = math.cos(math.radians(ang)) * sr * 1.5
        dy = math.sin(math.radians(ang)) * sr * 1.5
        draw.line([(sx + dx * 0.75, sy + dy * 0.75), (sx + dx, sy + dy)],
                  fill=(245, 178, 60), width=2)
    draw.text((x1 - w * 0.34, y1 - h * 0.24), "NO DEAL",
              font=font(SANS_B, 16), fill=RED)


def draw_jet(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    cx, cy = x0 + w * 0.50, y0 + h * 0.52
    for oy in (-h * 0.13, 0, h * 0.13):
        draw.line([(x0 + 4, cy + oy), (cx - w * 0.40, cy + oy)],
                  fill=(255, 255, 255), width=3)
    draw.polygon([(cx - w * 0.43, cy), (cx - w * 0.13, cy - h * 0.09),
                  (cx + w * 0.36, cy - h * 0.05), (cx + w * 0.48, cy),
                  (cx + w * 0.36, cy + h * 0.05), (cx - w * 0.13, cy + h * 0.09)],
                 fill=(150, 158, 170), outline=NAVY, width=2)
    draw.polygon([(cx - w * 0.10, cy - h * 0.08), (cx + w * 0.07, cy - h * 0.40),
                  (cx + w * 0.17, cy - h * 0.40), (cx + w * 0.12, cy - h * 0.08)],
                 fill=(120, 130, 145), outline=NAVY, width=2)
    draw.polygon([(cx - w * 0.10, cy + h * 0.08), (cx + w * 0.07, cy + h * 0.36),
                  (cx + w * 0.17, cy + h * 0.36), (cx + w * 0.12, cy + h * 0.08)],
                 fill=(120, 130, 145), outline=NAVY, width=2)
    draw.polygon([(cx - w * 0.39, cy - h * 0.06), (cx - w * 0.32, cy - h * 0.28),
                  (cx - w * 0.27, cy - h * 0.06)],
                 fill=(120, 130, 145), outline=NAVY, width=2)
    draw.ellipse([cx + w * 0.20, cy - h * 0.07, cx + w * 0.35, cy + h * 0.02],
                 fill=(180, 210, 235), outline=NAVY, width=2)
    draw.polygon([(cx - w * 0.43, cy - h * 0.03), (cx - w * 0.47, cy),
                  (cx - w * 0.43, cy + h * 0.03)], fill=(232, 120, 30))
    # warning triangle
    tx, ty = x1 - w * 0.16, y0 + h * 0.24
    draw.polygon([(tx, ty - 13), (tx - 13, ty + 10), (tx + 13, ty + 10)],
                 fill=(245, 200, 60), outline=NAVY, width=2)
    draw.text((tx - 3, ty - 8), "!", font=font(SANS_B, 15), fill=NAVY)


def draw_tennis(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(238, 244, 226))
    cx, cy = x0 + w * 0.30, y0 + h * 0.50
    r = h * 0.36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(204, 224, 80),
                 outline=(120, 140, 40), width=2)
    draw.arc([cx - r, cy - r, cx, cy + r], 250, 110, fill=(255, 255, 255), width=4)
    draw.arc([cx, cy - r, cx + r, cy + r], 70, 290, fill=(255, 255, 255), width=4)
    # trophy
    tx = x1 - w * 0.24
    draw.polygon([(tx - w * 0.11, y0 + h * 0.10), (tx + w * 0.11, y0 + h * 0.10),
                  (tx + w * 0.07, y0 + h * 0.58), (tx - w * 0.07, y0 + h * 0.58)],
                 fill=(212, 175, 55), outline=(140, 105, 20), width=2)
    draw.arc([tx - w * 0.19, y0 + h * 0.14, tx - w * 0.07, y0 + h * 0.50],
             90, 270, fill=(212, 175, 55), width=5)
    draw.arc([tx + w * 0.07, y0 + h * 0.14, tx + w * 0.19, y0 + h * 0.50],
             270, 90, fill=(212, 175, 55), width=5)
    draw.rectangle([tx - 4, y0 + h * 0.58, tx + 4, y0 + h * 0.76],
                   fill=(212, 175, 55), outline=(140, 105, 20), width=2)
    draw.rectangle([tx - w * 0.08, y0 + h * 0.76, tx + w * 0.08, y0 + h * 0.88],
                   fill=(212, 175, 55), outline=(140, 105, 20), width=2)


def draw_chess(draw, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(240, 236, 224))
    cx = x0 + w * 0.42
    base = y0 + h * 0.90
    # king piece, scaled to the band
    draw.ellipse([cx - w * 0.14, base - h * 0.08, cx + w * 0.14, base + h * 0.02],
                 fill=(40, 40, 40))
    draw.polygon([(cx - w * 0.11, base - h * 0.06), (cx - w * 0.07, base - h * 0.52),
                  (cx + w * 0.07, base - h * 0.52), (cx + w * 0.11, base - h * 0.06)],
                 fill=(40, 40, 40))
    draw.rectangle([cx - w * 0.09, base - h * 0.62, cx + w * 0.09, base - h * 0.52],
                   fill=(40, 40, 40))
    draw.polygon([(cx - w * 0.07, base - h * 0.62), (cx - w * 0.09, base - h * 0.78),
                  (cx - w * 0.03, base - h * 0.68), (cx, base - h * 0.82),
                  (cx + w * 0.03, base - h * 0.68), (cx + w * 0.09, base - h * 0.78),
                  (cx + w * 0.07, base - h * 0.62)], fill=(40, 40, 40))
    draw.rectangle([cx - 2, base - h * 0.96, cx + 2, base - h * 0.80],
                   fill=(40, 40, 40))
    draw.rectangle([cx - 7, base - h * 0.92, cx + 7, base - h * 0.87],
                   fill=(40, 40, 40))
    # white pawn beside it
    px = cx + w * 0.30
    draw.ellipse([px - w * 0.05, base - h * 0.06, px + w * 0.05, base + h * 0.02],
                 fill=(255, 255, 255), outline=NAVY, width=2)
    draw.polygon([(px - w * 0.04, base - h * 0.04), (px - w * 0.02, base - h * 0.34),
                  (px + w * 0.02, base - h * 0.34), (px + w * 0.04, base - h * 0.04)],
                 fill=(255, 255, 255), outline=NAVY, width=2)
    draw.ellipse([px - w * 0.03, base - h * 0.44, px + w * 0.03, base - h * 0.32],
                 fill=(255, 255, 255), outline=NAVY, width=2)


# --- page ------------------------------------------------------------------

def story_panel(img, draw, x, y, w, h, kicker, headline, body, illu):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=RULE, width=2)
    ih = 70  # illustration band height
    # illustration on its own layer: nothing can spill into the text below
    layer = Image.new("RGB", (w - 4, ih), PAPER)
    illu(ImageDraw.Draw(layer), 0, 0, w - 4, ih)
    img.paste(layer, (x + 2, y + 2))
    draw.line([(x, y + ih), (x + w, y + ih)], fill=RULE, width=2)
    ty = y + ih + 8
    draw.text((x + 14, ty), kicker, font=font(SANS_B, 17), fill=RED)
    ty += 24
    hfnt, hlines = fit_lines(draw, headline, SERIF_B, 25, w - 28, 2)
    for line in hlines:
        draw.text((x + 14, ty), line, font=hfnt, fill=INK)
        ty += 30
    ty += 4
    bfnt, blines = fit_lines(draw, body, SANS, 18, w - 28, 2)
    for line in blines:
        draw.text((x + 14, ty), line, font=bfnt, fill=(60, 60, 58))
        ty += 22


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw_centered(draw, W // 2, 12, "THE WORLD", font(SERIF_B, 92), (250, 246, 232))
    draw_tracked(draw, W // 2, 116, "TUESDAY 24 NOVEMBER 2026",
                 font(SANS_B, 27), (201, 162, 39), tracking=5)
    draw.rectangle([0, 148, W, 153], fill=GOLD)
    draw_centered(draw, W // 2, 162, "THE DAY'S WORLD NEWS — IN ONE PAGE",
                  font(SANS_B, 19), GREY)

    # --- lead story ---
    lx, ly, lw, lh = 36, 192, 952, 236
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=PAPER, outline=NAVY, width=3)
    ix0, iy0, ix1, iy1 = lx + lw - 330, ly + 2, lx + lw - 2, ly + lh - 2
    layer = Image.new("RGB", (ix1 - ix0, iy1 - iy0), SKY)
    draw_awacs(ImageDraw.Draw(layer), 0, 0, ix1 - ix0, iy1 - iy0)
    img.paste(layer, (ix0, iy0))
    draw.line([(ix0, ly), (ix0, ly + lh)], fill=RULE, width=2)
    tx = lx + 24
    draw.text((tx, ly + 16), "POLAND  •  NATO RESPONDS", font=font(SANS_B, 22), fill=RED)
    hy = ly + 48
    for line in ("MISSILES LAND", "IN POLAND"):
        draw.text((tx, hy), line, font=font(SERIF_B, 58), fill=INK)
        hy += 64
    # body text wrapped to the text column only (never under the illustration)
    bfnt, blines = fit_lines(
        draw,
        "Three Russian Kh-101 missiles landed in Poland on Friday. "
        "NATO will deploy an AWACS early-warning aircraft in response.",
        SANS, 20, ix0 - tx - 16, 2)
    by = ly + 182
    for line in blines:
        draw.text((tx, by), line, font=bfnt, fill=(60, 60, 58))
        by += 25

    # --- story grid: 3 columns x 2 rows ---
    panels = [
        ("LIBYA", "WARSHIP SUNK OFF LIBYA",
         "Sea drones hit the corvette Merkury at Benghazi; it capsized.",
         draw_warship),
        ("STRAIT OF HORMUZ", "TANKERS HIT BY MINES",
         "Three tankers hit mines and caught fire in the Strait.",
         draw_tanker),
        ("CLIMATE", "COP31 ENDS IN FAILURE",
         "No fossil-fuel deal; backlash in Australia, Pacific despair.",
         draw_globe),
        ("SOUTH KOREA", "RUSSIAN JET INCURSION",
         "Brief evacuation alert for Ulleung island after the incursion.",
         draw_jet),
        ("SPORT", "ALCARAZ WINS ATP FINALS",
         "Alcaraz beats Zverev for his first ATP Finals title.",
         draw_tennis),
        ("CHESS & CRICKET", "GUKESH DEFENDS CROWN",
         "Title defence begins vs Sindarov in Geneva; India–NZ draw.",
         draw_chess),
    ]
    pw, ph, gap = 306, 224, 17
    gx, gy = 36, 440
    for i, (kicker, headline, body, illu) in enumerate(panels):
        px = gx + (i % 3) * (pw + gap)
        py = gy + (i // 3) * (ph + 12)
        story_panel(img, draw, px, py, pw, ph, kicker, headline, body, illu)

    # --- ALSO TODAY strip ---
    sx, sy, sw, sh = 36, 912, 952, 100
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=PAPER, outline=NAVY, width=2)
    draw.text((sx + 16, sy + 9), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    items = ("Mexico captures drug lord 'Chapo Isidro' (Fausto Isidro Meza Flores)"
             "  •  Jensen Huang returns as Nvidia CEO — stock surges 31%"
             "  •  Cikande candy factory fire kills 24 in Indonesia"
             "  •  Chinese official sentenced to death for leaking state secrets")
    sfnt, slines = fit_lines(draw, items, SANS, 19, sw - 32, 3)
    ly = sy + 36
    for line in slines:
        draw.text((sx + 16, ly), line, font=sfnt, fill=INK)
        ly += 21

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
