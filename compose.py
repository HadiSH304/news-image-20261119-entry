"""Compose the news front page for make.fun news-image-20261119.

36-story flat-illustration newspaper front page, drawn entirely with PIL
(no generated photos, no faces, no hands — the winners' grammar from the
news18 extreme analysis). Two candidates: A (cream masthead) and B (navy
masthead + UTC timeline strip). Run: python3 compose.py A|B
Saves candidate-a.jpg / candidate-b.jpg next to this file, 1024x1024 JPEG.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# Palette (winners' family: cream paper, navy, red accents)
CREAM = (247, 243, 232)
PAPER = (250, 246, 236)
NAVY = (14, 30, 58)
NAVY2 = (20, 42, 78)
RED = (178, 34, 34)
DARK_RED = (139, 21, 21)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
GREY = (90, 90, 90)
TAN = (217, 201, 163)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (176, 208, 224)
SKY = (214, 232, 240)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

REGION_COLORS = {
    "EUROPE": (31, 93, 168),
    "THE AMERICAS": (34, 139, 90),
    "ASIA-PACIFIC": (168, 52, 52),
    "MIDEAST": (186, 124, 31),
    "AFRICA": (122, 90, 168),
    "OCEANIA": (31, 139, 139),
    "WORLD": (96, 96, 96),
}


def fb(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, font, fill):
    draw.text(xy, s, font=font, fill=fill)


def centered(draw, cx, y, s, font, fill):
    w = draw.textlength(s, font=font)
    draw.text((cx - w / 2, y), s, font=font, fill=fill)


def draw_flag(draw, x, y, w, h, country):
    """Flat mini flag, no text."""
    if country == "US":
        for i in range(7):
            draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                           fill=(178, 34, 34) if i % 2 == 0 else WHITE)
        draw.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 60, 120))
        for r in range(3):
            for c in range(4):
                draw.ellipse([x + 3 + c * 5, y + 3 + r * 4,
                              x + 5 + c * 5, y + 5 + r * 4], fill=WHITE)
    elif country == "CN":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.polygon([(x + 3, y + 3), (x + 5, y + 7), (x + 8, y + 7),
                      (x + 6, y + 9), (x + 7, y + 12), (x + 3, y + 10),
                      (x - 1, y + 12), (x, y + 9), (x - 2, y + 7),
                      (x + 1, y + 7)], fill=(255, 222, 0))
    elif country == "RU":
        draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 60, 160))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 30, 30))


def skyline(draw, x, y, w, h, color, seed=0):
    """Flat building silhouettes along the bottom of a box."""
    import random
    rnd = random.Random(seed)
    bx = x
    while bx < x + w - 8:
        bw = rnd.randint(14, 34)
        bh = rnd.randint(int(h * 0.3), int(h * 0.95))
        draw.rectangle([bx, y + h - bh, min(bx + bw, x + w), y + h], fill=color)
        if rnd.random() < 0.5:
            draw.rectangle([bx + bw // 3, y + h - bh - 6, bx + 2 * bw // 3,
                            y + h - bh], fill=color)
        bx += bw + rnd.randint(2, 8)


# ---------------- flat illustrations (each draws inside box x,y,w,h) -----
def ill_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 196, 138))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(90, 60, 80))
    skyline(d, x, y + 8, w, int(h * 0.55), (70, 60, 90), seed=3)
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(240, 200, 90))
    # round table with three flags
    d.ellipse([x + w * 0.18, y + h * 0.62, x + w * 0.82, y + h * 0.78],
              fill=(120, 70, 60))
    d.rectangle([x + w * 0.18, y + h * 0.70, x + w * 0.82, y + h * 0.78],
                fill=(100, 55, 50))
    for i, c in enumerate(["US", "CN", "RU"]):
        fx = x + w * (0.28 + 0.22 * i)
        d.line([fx + 12, y + h * 0.30, fx + 12, y + h * 0.66], fill=(60, 40, 30),
               width=2)
        draw_flag(d, fx, y + h * 0.30, 26, 17, c)


def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 32, 92))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(120, 50, 110))
    d.ellipse([x + w * 0.62, y + 8, x + w * 0.86, y + 8 + w * 0.24],
              fill=(250, 190, 80))
    skyline(d, x, y + int(h * 0.35), w, int(h * 0.65), (30, 18, 55), seed=7)
    # palm silhouettes (kept inside the panel)
    for px in (x + 36, x + w - 36):
        d.line([px, y + h * 0.55, px, y + h * 0.85], fill=(20, 12, 40), width=3)
        for a in (-20, -7, 7, 20):
            d.line([px, y + h * 0.55, px + a, y + h * 0.55 - 12],
                   fill=(20, 12, 40), width=2)
    # controller
    cx, cy = x + w // 2, y + int(h * 0.62)
    d.rounded_rectangle([cx - 34, cy - 14, cx + 34, cy + 14], radius=12,
                        fill=(20, 20, 30))
    d.ellipse([cx - 24, cy - 5, cx - 14, cy + 5], fill=(250, 250, 250))
    for ox, oy, col in ((18, -6, (240, 200, 60)), (24, 2, (220, 60, 60)),
                        (12, 4, (60, 180, 90)), (20, 8, (70, 120, 230))):
        d.ellipse([cx + ox - 3, cy + oy - 3, cx + ox + 3, cy + oy + 3], fill=col)
    d.rounded_rectangle([x + w // 2 - 44, y + 6, x + w // 2 + 44, y + 20],
                        radius=7, fill=(178, 34, 34))
    centered(d, x + w // 2, y + 8, "OUT TODAY", fb(SANS_B, 10), WHITE)


def ill_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 70, 52))
    pts = [(x + 12 + i * (w - 24) / 7, y + h - 20 - i * (h * 0.52) / 7)
           for i in range(8)]
    for i in range(7):
        d.line([pts[i], pts[i + 1]], fill=(120, 220, 140), width=3)
    for i, (px, py) in enumerate(pts):
        col = (60, 200, 110) if i % 2 == 0 else (230, 80, 80)
        d.rectangle([px - 4, py - 10, px + 4, py + 10], fill=col)
        d.line([px, py - 14, px, py + 14], fill=col, width=2)
    text(d, (x + 10, y + 6), "ANT", fb(SANS_B, 20), WHITE)
    text(d, (x + w - 58, y + 6), "$83", fb(SANS_B, 20), (255, 210, 60))
    text(d, (x + 10, y + h - 18), "NASDAQ · FIRST TRADE TODAY",
         fb(SANS_B, 9), (170, 220, 190))


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    d.polygon([(x + w * 0.08, y + h * 0.42), (x + w * 0.5, y + h * 0.10),
               (x + w * 0.92, y + h * 0.42)], fill=(240, 236, 224))
    d.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.90, y + h * 0.48],
                fill=(200, 192, 172))
    for i in range(4):
        cx = x + w * (0.18 + 0.21 * i)
        d.rectangle([cx - 5, y + h * 0.48, cx + 5, y + h * 0.86],
                    fill=(245, 242, 232))
    d.rectangle([x + w * 0.08, y + h * 0.86, x + w * 0.92, y + h * 0.92],
                fill=(200, 192, 172))
    # scales of justice, tiny
    sx, sy = x + w - 26, y + h - 22
    d.line([sx, sy - 12, sx, sy], fill=(60, 60, 60), width=2)
    d.line([sx - 8, sy - 12, sx + 8, sy - 12], fill=(60, 60, 60), width=2)
    d.polygon([(sx - 10, sy - 6), (sx - 6, sy - 6), (sx - 8, sy - 2)],
              fill=(178, 34, 34))
    d.polygon([(sx + 6, sy - 6), (sx + 10, sy - 6), (sx + 8, sy - 2)],
              fill=(178, 34, 34))


def ill_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 214))
    d.ellipse([x + 8, y + 6, x + 8 + h * 0.62, y + 6 + h * 0.62],
              fill=(70, 130, 180))
    d.ellipse([x + 16, y + 14, x + 30, y + 26], fill=(120, 190, 110))
    d.ellipse([x + 30, y + 30, x + 48, y + 40], fill=(120, 190, 110))
    # thermometer
    tx = x + w - 22
    d.rounded_rectangle([tx, y + 8, tx + 10, y + h - 14], radius=5,
                        fill=WHITE)
    d.ellipse([tx - 4, y + h - 22, tx + 14, y + h - 4], fill=(200, 40, 40))
    d.rectangle([tx + 3, y + h * 0.45, tx + 7, y + h - 12], fill=(200, 40, 40))
    d.ellipse([x + w - 52, y + 8, x + w - 34, y + 26], fill=(240, 190, 60))
    text(d, (x + 8, y + h - 16), "FINAL 48 HOURS", fb(SANS_B, 9),
         (90, 40, 40))


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(180, 205, 225))
    cx, cy = x + w // 2, y + h // 2 + 2
    for r in range(6, 34, 5):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + r * 8,
              end=300 + r * 8, fill=WHITE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(178, 34, 34))
    d.rounded_rectangle([x + 6, y + 5, x + 74, y + 19], radius=6,
                        fill=(178, 34, 34))
    centered(d, x + 40, y + 7, "RED ALERT", fb(SANS_B, 9), WHITE)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 160, 120))


def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 130, 170))
    for tx in (x + w * 0.22, x + w * 0.72):
        d.rectangle([tx - 3, y + h * 0.18, tx + 3, y + h * 0.62],
                    fill=(70, 70, 80))
    d.rectangle([x, y + h * 0.55, x + w, y + h * 0.62], fill=(60, 60, 70))
    for i in range(6):
        d.line([(x + w * 0.22, y + h * 0.20),
                (x + w * (0.05 + 0.15 * i), y + h * 0.55)], fill=(120, 120, 130),
               width=1)
    # explosion starburst
    ex, ey = x + w * 0.48, y + h * 0.30
    for ang in range(0, 360, 30):
        import math
        r = 12
        x2 = ex + r * math.cos(math.radians(ang))
        y2 = ey + r * math.sin(math.radians(ang))
        d.line([ex, ey, x2, y2], fill=(240, 140, 30), width=3)
    d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(250, 200, 40))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(190, 165, 110))
    # dashed yellow line
    lx = x + w * 0.62
    for yy in range(y + 6, y + h - 4, 10):
        d.line([lx, yy, lx, yy + 5], fill=(230, 200, 40), width=3)
    # tank silhouette
    tx, ty = x + w * 0.16, y + h * 0.55
    d.rounded_rectangle([tx, ty, tx + 52, ty + 16], radius=5, fill=(70, 75, 60))
    d.rectangle([tx + 12, ty - 10, tx + 34, ty + 2], fill=(70, 75, 60))
    d.line([tx + 34, ty - 6, tx + 58, ty - 10], fill=(70, 75, 60), width=4)
    d.ellipse([tx + 6, ty + 16, tx + 14, ty + 22], fill=(50, 52, 42))
    d.ellipse([tx + 38, ty + 16, tx + 46, ty + 22], fill=(50, 52, 42))
    # buildings
    d.rectangle([x + w - 40, y + 10, x + w - 8, y + h * 0.55], fill=(150, 130, 100))
    d.rectangle([x + w - 58, y + 24, x + w - 42, y + h * 0.55],
                fill=(170, 150, 118))


def ill_florida(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 175, 195))
    for cx, cy, s in ((0.25, 0.30, 26), (0.55, 0.22, 30), (0.80, 0.34, 22)):
        px, py = x + w * cx, y + h * cy
        d.ellipse([px - s, py - s * 0.6, px + s, py + s * 0.6], fill=(70, 85, 105))
        d.ellipse([px - s * 0.6, py - s * 0.8, px + s * 0.7, py + s * 0.4],
                  fill=(70, 85, 105))
    for i in range(14):
        rx = x + 6 + i * (w - 12) / 14
        d.line([rx, y + h * 0.55, rx - 6, y + h * 0.75], fill=(90, 120, 150),
               width=2)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 130, 170))
    d.rounded_rectangle([x + w - 80, y + 5, x + w - 4, y + 19], radius=6,
                        fill=(178, 34, 34))
    centered(d, x + w - 42, y + 7, "300+ RESCUES", fb(SANS_B, 9), WHITE)


def ill_suneung(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.rectangle([x + 10, y + h * 0.55, x + w - 10, y + h * 0.62],
                fill=(150, 110, 70))
    d.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.62, y + h * 0.55],
                fill=WHITE)
    for i in range(4):
        d.line([x + w * 0.33, y + h * (0.36 + 0.05 * i),
                x + w * 0.59, y + h * (0.36 + 0.05 * i)], fill=(150, 150, 150),
               width=1)
    # clock
    cx, cy = x + w - 26, y + 24
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=WHITE)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=(40, 40, 40), width=2)
    d.line([cx, cy, cx, cy - 9], fill=(40, 40, 40), width=2)
    d.line([cx, cy, cx + 7, cy + 3], fill=(40, 40, 40), width=2)
    text(d, (x + 8, y + 6), "08:40–17:45", fb(SANS_B, 9), (90, 40, 40))


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 195))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(60, 100, 140))
    # tanker hull
    d.polygon([(x + 12, y + h * 0.55), (x + w - 12, y + h * 0.55),
               (x + w - 26, y + h * 0.72), (x + 24, y + h * 0.72)],
              fill=(60, 60, 70))
    for i in range(4):
        d.rectangle([x + 22 + i * 30, y + h * 0.38, x + 46 + i * 30,
                     y + h * 0.55], fill=(200, 80, 50) if i % 2 else (230, 200, 90))
    d.rectangle([x + w - 46, y + h * 0.30, x + w - 16, y + h * 0.55],
                fill=(240, 240, 235))
    # flames + smoke
    for fx, fy, s, col in ((0.30, 0.30, 12, (250, 140, 30)),
                           (0.55, 0.26, 15, (240, 90, 20)),
                           (0.78, 0.32, 10, (250, 170, 40))):
        px, py = x + w * fx, y + h * fy
        d.polygon([(px - s, py + s), (px, py - s), (px + s, py + s)],
                  fill=col)
    d.ellipse([x + w * 0.42, y + 4, x + w * 0.52, y + 16], fill=(90, 90, 95))
    d.ellipse([x + w * 0.55, y + 2, x + w * 0.68, y + 14], fill=(110, 110, 115))


def ill_colombia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    for i, col in enumerate(((178, 34, 34), (31, 93, 168), (34, 139, 90))):
        sx = x + 18 + i * 52
        d.rectangle([sx, y + 10, sx + 40, y + 30], fill=col)
        d.line([sx + 20, y + 30, sx + 20, y + h - 8], fill=(90, 70, 50),
               width=3)
    for i in range(6):
        px = x + 14 + i * 26
        d.ellipse([px - 5, y + h - 16, px + 5, y + h - 6], fill=(80, 70, 60))
        d.rectangle([px - 3, y + h - 24, px + 3, y + h - 14], fill=(80, 70, 60))


def ill_benghazi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    for i, (bx, by, bw, bh) in enumerate(((14, 30, 44, 22), (62, 30, 44, 22),
                                          (110, 30, 44, 22), (38, 8, 44, 22),
                                          (86, 8, 44, 22))):
        d.rectangle([x + bx, y + by, x + bx + bw, y + by + bh],
                    fill=(190, 165, 120))
        d.rectangle([x + bx, y + by, x + bx + bw, y + by + bh],
                    outline=(120, 95, 60), width=2)
        d.line([x + bx, y + by + bh / 2, x + bx + bw, y + by + bh / 2],
               fill=(120, 95, 60), width=1)
    d.polygon([(x + 60, y + h - 26), (x + w - 60, y + h - 26),
               (x + w - 52, y + h - 12), (x + 52, y + h - 12)],
              fill=(178, 34, 34))
    centered(d, x + w // 2, y + h - 24, "SEIZED", fb(SANS_B, 11), WHITE)


ILL = {
    "summit": ill_summit, "gta": ill_gta, "ipo": ill_ipo, "court": ill_court,
    "cop": ill_cop, "cyclone": ill_cyclone, "bridge": ill_bridge,
    "gaza": ill_gaza, "florida": ill_florida, "suneung": ill_suneung,
    "hormuz": ill_hormuz, "colombia": ill_colombia, "benghazi": ill_benghazi,
}


# ---------------- world map ----------------------------------------------
CONTINENTS = {
    "NA": [(-168, 66), (-155, 71), (-140, 70), (-125, 71), (-120, 60),
           (-110, 55), (-95, 58), (-85, 66), (-80, 73), (-75, 62),
           (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
           (-80, 30), (-85, 29), (-90, 21), (-95, 18), (-100, 16),
           (-105, 20), (-115, 28), (-125, 40), (-125, 48), (-135, 58),
           (-150, 60), (-165, 60)],
    "GL": [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-68, 76), (-68, 70)],
    "SA": [(-80, 10), (-75, 8), (-70, 11), (-62, 10), (-55, 6), (-50, 0),
           (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35),
           (-65, -40), (-70, -50), (-73, -53), (-70, -40), (-72, -20),
           (-80, -5), (-81, 0)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53),
           (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60),
           (30, 62), (32, 70), (40, 68), (50, 69), (60, 69), (68, 66),
           (60, 60), (50, 55), (45, 50), (40, 47), (35, 45), (30, 44),
           (28, 41), (23, 40), (22, 37), (19, 42), (12, 44), (8, 44),
           (3, 42), (0, 39), (-2, 37), (-6, 36)],
    "AF": [(-17, 15), (-15, 20), (-10, 30), (-5, 35), (0, 36), (10, 37),
           (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 18),
           (43, 11), (48, 11), (51, 10), (46, 5), (42, 0), (40, -5),
           (38, -10), (35, -18), (32, -25), (28, -32), (20, -35),
           (15, -30), (12, -18), (10, -5), (8, 4), (4, 6), (-8, 5),
           (-13, 8), (-17, 12)],
    "AS": [(32, 36), (36, 36), (42, 38), (45, 40), (50, 42), (55, 45),
           (60, 48), (65, 50), (70, 55), (75, 60), (80, 65), (85, 68),
           (90, 70), (100, 72), (110, 73), (120, 72), (130, 71), (140, 72),
           (150, 70), (160, 68), (170, 66), (178, 65), (170, 60),
           (162, 58), (158, 52), (150, 45), (142, 42), (140, 38),
           (135, 35), (130, 32), (127, 35), (122, 38), (120, 32),
           (115, 25), (110, 20), (108, 12), (105, 8), (100, 8), (98, 12),
           (95, 16), (92, 20), (90, 22), (88, 22), (85, 20), (82, 17),
           (80, 13), (78, 8), (76, 10), (74, 20), (72, 20), (70, 25),
           (66, 25), (62, 25), (58, 26), (55, 27), (52, 28), (50, 29),
           (48, 30), (44, 29), (40, 31), (36, 36)],
    "AU": [(114, -22), (114, -30), (115, -35), (120, -34), (125, -32),
           (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
           (142, -11), (137, -12), (135, -12), (132, -12), (130, -13),
           (126, -14), (122, -17), (118, -20)],
}
# story number -> (lon, lat) for map pins (stories 1-13)
PINS = {1: (114, 22), 2: (175, -41), 3: (-74, 40), 4: (4, 52), 5: (30, 37),
        6: (85, 20), 7: (36, 45), 8: (34, 31), 9: (-80, 26), 10: (127, 37),
        11: (56, 26), 12: (-74, 5), 13: (20, 32)}


def draw_map(d, x, y, w, h, bg, land, pin_fill=RED):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    # graticule
    for gx in range(1, 6):
        d.line([x + w * gx / 6, y, x + w * gx / 6, y + h], fill=(255, 255, 255),
               width=1) if bg == NAVY else None
    def proj(lon, lat):
        px = x + (lon + 180) / 360 * w
        py = y + (75 - lat) / 135 * h
        return (px, py)
    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=land)
    # Indonesia dots
    for lon, lat in ((100, 0), (110, -7), (120, -9), (130, -3), (140, -5),
                     (105, 2), (118, -2)):
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 2, px + 3, py + 2], fill=land)
    for num, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=pin_fill,
                  outline=WHITE, width=1)
        centered(d, px, py - 6, str(num), fb(SANS_B, 9), WHITE)


# ---------------- story data (36 stories) -------------------------------
LEADS = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT", region="ASIA-PACIFIC",
         art="summit", src="REUTERS · AP",
         head="Trump, Xi and Putin hold first three-way summit",
         deck="The three nuclear powers meet at APEC in Shenzhen; arms "
              "control and the Iran war top the agenda. No deal expected."),
    dict(n=2, place="WORLDWIDE", topic="GAMES", region="WORLD",
         art="gta", src="REUTERS",
         head="GTA VI arrives after a 13-year wait",
         deck="Rockstar's sequel unlocks at midnight in each country, New "
              "Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and "
              "Xbox, no PC yet."),
    dict(n=3, place="NASDAQ", topic="MARKETS", region="THE AMERICAS",
         art="ipo", src="REUTERS · BLOOMBERG",
         head="Anthropic debuts in the biggest IPO on record",
         deck="Priced at $83, above its range, the Claude maker raised "
              "$81.3bn and is valued near $1.5tn. First trades set the "
              "real price."),
]

CARDS = [
    dict(n=4, place="THE HAGUE", topic="LAW", region="EUROPE",
         art="court", src="ICJ · AP",
         head="World Court rules on Myanmar's Rohingya case",
         deck="The ICJ reads its judgment in The Gambia's case over the "
              "2017 campaign. Final, with no appeal."),
    dict(n=5, place="ANTALYA", topic="CLIMATE", region="EUROPE",
         art="cop", src="UNFCCC",
         head="COP31 enters its final 48 hours",
         deck="Ministers take over the text in Antalya; \u201cphase out\u201d "
              "and the $120bn adaptation fund are still open."),
    dict(n=6, place="ODISHA", topic="STORM", region="ASIA-PACIFIC",
         art="cyclone", src="IMD",
         head="Akvan bears down as 200,000 flee the coast",
         deck="Red alerts in 11 districts, schools shut. Landfall near "
              "Puri due Friday."),
    dict(n=7, place="KERCH", topic="WAR", region="EUROPE",
         art="bridge", src="BBC · KYIV",
         head="Crimean Bridge hit a third time in a week",
         deck="Traffic halted after a fresh attack, a Russian official "
              "says."),
    dict(n=8, place="GAZA", topic="WAR", region="MIDEAST",
         art="gaza", src="REUTERS",
         head="Israeli tanks cross the Gaza ceasefire line",
         deck="A rare ground raid beyond the Yellow Line; Hamas calls it a "
              "truce breach."),
    dict(n=9, place="FLORIDA", topic="WEATHER", region="THE AMERICAS",
         art="florida", src="AP · NWS",
         head="Flooded Florida braces for still more rain",
         deck="A foot of rain in hours in Hollywood; 300 rescue calls in "
              "a night. Schools shut Thursday."),
    dict(n=10, place="SEOUL", topic="EDUCATION", region="ASIA-PACIFIC",
         art="suneung", src="YONHAP",
         head="Half a million sit Korea's Suneung exam",
         deck="551,864 take the college exam; flights pause for the "
              "listening test."),
    dict(n=11, place="HORMUZ", topic="GULF", region="MIDEAST",
         art="hormuz", src="IRIB · CLAIM",
         head="Two tankers ablaze after mine strikes",
         deck="Iran says the ships hit mines while sailing illegally; 4m "
              "barrels aboard. Strait traffic at 42%."),
    dict(n=12, place="BOGOT\u00c1", topic="LABOUR", region="THE AMERICAS",
         art="colombia", src="AFP",
         head="Colombia's unions strike nationwide",
         deck="Workers and teachers march against the government's tax "
              "and fiscal bill."),
    dict(n=13, place="BENGHAZI", topic="CRIME", region="AFRICA",
         art="benghazi", src="AFP",
         head="Cocaine and millions of pills seized in eastern Libya",
         deck="Officials display one of the country's biggest drug hauls, "
              "seized in the east."),
]

BRIEFS = [
    (14, "MEXICO CITY", "Banxico cuts rates to 6.25%."),
    (15, "CANBERRA", "Australia's jobless rate hits 4.9%."),
    (16, "MOGADISHU", "Somalia accuses UAE of secret bases."),
    (17, "NEW DELHI", "Modi meets the Prince and Princess of Wales."),
    (18, "TOKYO", "India and Japan review defence ties."),
    (19, "BENGALURU", "Amazon pledges $7bn for India renewables."),
    (20, "BAGHDAD", "Six French ISIL members jailed for life."),
    (21, "NAIROBI", "Kenya floods kill six; Ruto addresses nation."),
    (22, "CARACAS", "Hegseth signs a US–Venezuela military deal."),
    (23, "MANAMA", "Bapco refinery back on its feet."),
    (24, "RIYADH", "Gulf leaders urge Trump not to strike Iran."),
    (25, "WASHINGTON", "Vance: no \u201cforever war\u201d in the Gulf."),
    (26, "OTTAWA", "Carney rethinks China ties."),
    (27, "VIENNA", "IAEA: North Korea expanded uranium enrichment."),
    (28, "LA PAZ", "Bolivia declares an El Ni\u00f1o emergency."),
    (29, "MADRID", "Police clash with strikers across Spain."),
    (30, "SYDNEY", "Duckett's 133 puts England on top in ODI."),
    (31, "SACRAMENTO", "California braces for an atmospheric river."),
    (32, "THIMPHU", "A glacial lake burst floods Bhutan's hot springs."),
    (33, "DHAKA", "Bangladesh in turmoil: violence in 28 districts."),
    (34, "DAKAR", "Migrant boat capsizes; dozens missing."),
    (35, "SHENZHEN", "APEC leaders adopt the Shenzhen Declaration."),
    (36, "BERLIN", "Coalition of the Willing backs Ukraine."),
]

REGIONS = [("EUROPE", 6), ("THE AMERICAS", 9), ("ASIA-PACIFIC", 9),
           ("MIDEAST", 5), ("AFRICA", 4), ("OCEANIA", 2), ("WORLD", 1)]

NUMBERS = [
    ("$81.3bn", "raised by Anthropic — the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "evacuated ahead of Cyclone Akvan"),
    ("$120bn", "a year of adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017 — the ICJ case"),
    ("551,864", "sit South Korea's college entrance exam"),
]

DATE_CHECK = ("DATE CHECK — FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON THIS "
    "PAGE AS NEWS: the Iranian drone interceptions over Kuwait and Bahrain · "
    "the EU's proposed \u20ac45bn loan for Ukraine · the House Democrats' "
    "251–11 vote nominating Hakeem Jeffries · Voyager 1 crossing one "
    "light-day, at 10:16 GMT Wednesday · Van Gogh's record $190.4m sale · "
    "Peltola's Alaska win · Pew's projection that Islam becomes the largest "
    "religion by 2035 · Nvidia's $115.8bn quarter · the US strike on Qeshm "
    "(Tue 17 Nov).  NOT YET: Akvan's landfall (Fri) · COP31's final text (Fri).")

FOOTER = ("Every story here happened, or was first reported, on Thursday 19 "
    "November 2026. Disputed claims are attributed, not stated as fact. "
    "Sources: Reuters, AP, AFP, BBC, Al Jazeera, The Hindu, IMD, NASA, ICJ, "
    "IAEA. Original drawings.")


def rule(d, x, y, w, color=INK, width=2):
    d.rectangle([x, y, x + w, y + width - 1], fill=color)


def region_bar(d, x, y, w, h):
    total = sum(c for _, c in REGIONS)
    cx = x
    for name, count in REGIONS:
        seg = w * count / total
        d.rectangle([cx, y, cx + seg, y + h], fill=REGION_COLORS[name])
        label = f"{name} {count}"
        fnt = fb(SANS_B, 10)
        tw = d.textlength(label, font=fnt)
        if tw <= seg - 6:
            d.text((cx + (seg - tw) / 2, y + 4), label, font=fnt, fill=WHITE)
        elif d.textlength(str(count), font=fnt) <= seg - 4:
            d.text((cx + (seg - d.textlength(str(count), font=fnt)) / 2,
                    y + 4), str(count), font=fnt, fill=WHITE)
        cx += seg


def numbers_strip(d, x, y, w, h, dark=False):
    cw = w / len(NUMBERS)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = x + i * cw
        if i:
            d.line([cx, y + 6, cx, y + h - 6], fill=(180, 170, 150), width=1)
        nf = fb(SERIF, 21)
        tw = d.textlength(num, font=nf)
        while tw > cw - 10 and nf.size > 15:
            nf = fb(SERIF, nf.size - 1)
            tw = d.textlength(num, font=nf)
        d.text((cx + (cw - tw) / 2, y + 2), num, font=nf,
               fill=RED if not dark else GOLD)
        cf = fb(SANS, 10)
        lines = wrap(d, cap, cf, cw - 10)
        ly = y + 24
        for ln in lines[:2]:
            centered(d, cx + cw / 2, ly, ln, cf, INK if not dark else WHITE)
            ly += 11


def lead_card(d, s, x, y, w, ill_h, head_size=21, deck_size=12):
    ILL[s["art"]](d, x, y, w, ill_h)
    ty = y + ill_h + 6
    d.text((x, ty), f"{s['n']} · {s['place']} · {s['topic']}",
           font=fb(SANS_B, 11), fill=RED)
    sw = d.textlength(s["src"], font=fb(SANS, 10))
    d.text((x + w - sw, ty), s["src"], font=fb(SANS, 10), fill=GREY)
    ty += 16
    hf = fb(SERIF, head_size)
    lines = wrap(d, s["head"], hf, w)
    for ln in lines[:2]:
        d.text((x, ty), ln, font=hf, fill=INK)
        ty += head_size + 4
    df = fb(SANS, deck_size)
    for ln in wrap(d, s["deck"], df, w)[:3]:
        d.text((x, ty), ln, font=df, fill=(60, 60, 60))
        ty += deck_size + 3
    return ty


def small_card(d, s, x, y, w, ill_h):
    ILL[s["art"]](d, x, y, w, ill_h)
    ty = y + ill_h + 5
    d.text((x, ty), f"{s['n']} · {s['place']} · {s['topic']}",
           font=fb(SANS_B, 10), fill=RED)
    ty += 14
    hf = fb(SERIF, 14)
    lines = wrap(d, s["head"], hf, w)
    for ln in lines[:3]:
        d.text((x, ty), ln, font=hf, fill=INK)
        ty += 17
    df = fb(SANS, 10)
    for ln in wrap(d, s["deck"], df, w)[:3]:
        d.text((x, ty), ln, font=df, fill=(60, 60, 60))
        ty += 12
    return ty


def briefs_block(d, x, y, w, h):
    d.text((x, y), "ALSO ON THURSDAY 19 NOVEMBER — 23 MORE STORIES",
           font=fb(SANS_B, 12), fill=RED)
    y += 18
    col_w = (w - 16) / 2
    fnt = fb(SANS, 10)
    bf = fb(SANS_B, 10)
    per_col = 12
    bottom = y
    for ci in range(2):
        cx = x + ci * (col_w + 16)
        cy = y
        for n, place, txt in BRIEFS[ci * per_col:(ci + 1) * per_col]:
            head = f"{n} {place} — "
            lines = wrap(d, head + txt, fnt, col_w)
            # wrap() collapses whitespace, so the first line starts with
            # "<n> <PLACE> — ..."; draw the number bold, then the rest.
            first = lines[0]
            rest = first[len(str(n)) + 1:]
            d.text((cx, cy), str(n), font=bf, fill=RED)
            d.text((cx + d.textlength(str(n) + " ", font=bf), cy),
                   rest, font=fnt, fill=INK)
            cy += 13
            for ln in lines[1:]:
                d.text((cx, cy), ln, font=fnt, fill=INK)
                cy += 13
        bottom = max(bottom, cy)
    return bottom


def date_check_box(d, x, y, w):
    fnt = fb(SANS, 10)
    lines = wrap(d, DATE_CHECK, fnt, w - 16)
    h = 6 + 12 * len(lines) + 4
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    ly = y + 4
    for ln in lines:
        d.text((x + 8, ly), ln, font=fnt, fill=INK)
        ly += 12
    return y + h


def build_a():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16
    y = 8
    d.text((M, y), "THE WORLD IN ONE DAY", font=fb(SANS_B, 13), fill=RED)
    right = "THURSDAY'S NEWS · ONE PAGE · 36 STORIES"
    d.text((W - M - d.textlength(right, font=fb(SANS_B, 13)), y), right,
           font=fb(SANS_B, 13), fill=INK)
    y += 20
    rule(d, M, y, W - 2 * M, width=3)
    y += 6
    centered(d, W // 2, y, "Thursday 19 November 2026", fb(SERIF, 50), INK)
    y += 60
    centered(d, W // 2, y,
             "Three leaders meet in Shenzhen · A court rules on Myanmar · "
             "The biggest IPO ever debuts",
             fb(SERIF_IT, 16), RED)
    y += 22
    region_bar(d, M, y, W - 2 * M, 20)
    y += 24
    numbers_strip(d, M, y, W - 2 * M, 44)
    y += 48
    rule(d, M, y, W - 2 * M, width=1)
    y += 5
    # leads row
    lw = (W - 2 * M - 32) // 3
    lead_bottom = y
    for i, s in enumerate(LEADS):
        lx = M + i * (lw + 16)
        b = lead_card(d, s, lx, y, lw, 84)
        lead_bottom = max(lead_bottom, b)
    y = lead_bottom + 6
    rule(d, M, y, W - 2 * M, width=1)
    y += 5
    # cards rows
    cw = (W - 2 * M - 32) // 5
    for row in range(2):
        row_bottom = y
        for i in range(5):
            s = CARDS[row * 5 + i]
            cx = M + i * (cw + 8)
            b = small_card(d, s, cx, y, cw, 46)
            row_bottom = max(row_bottom, b)
        y = row_bottom + 5
        if row == 0:
            rule(d, M, y, W - 2 * M, width=1)
            y += 4
    rule(d, M, y, W - 2 * M, width=1)
    y += 5
    # bottom: map + briefs
    d.text((M, y), "WHERE IT HAPPENED", font=fb(SANS_B, 12), fill=RED)
    map_y = y + 18
    draw_map(d, M, map_y, 330, 140, NAVY, TAN)
    d.text((M, map_y + 144),
           "Red numbers mark stories 1–13. Positions are approximate.",
           font=fb(SANS, 10), fill=GREY)
    bx = M + 346
    briefs_bottom = briefs_block(d, bx, y, W - M - bx, 200)
    y = max(map_y + 162, briefs_bottom) + 6
    y = date_check_box(d, M, y, W - 2 * M)
    y += 6
    for ln in wrap(d, FOOTER, fb(SANS, 10), W - 2 * M):
        d.text((M, y), ln, font=fb(SANS, 10), fill=GREY)
        y += 12
    print("candidate A bottom y =", y)
    return img


def build_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16
    # navy masthead band
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((M, 10), "THE WORLD IN ONE DAY", font=fb(SANS_B, 13), fill=GOLD)
    right = "36 STORIES · ONE DAY · EVERY CONTINENT"
    d.text((W - M - d.textlength(right, font=fb(SANS_B, 13)), 10), right,
           font=fb(SANS_B, 13), fill=GOLD)
    centered(d, W // 2, 26, "Thursday 19 November 2026", fb(SERIF, 48), WHITE)
    centered(d, W // 2, 84,
             "Three leaders meet in Shenzhen · A court rules on Myanmar · "
             "The biggest IPO ever debuts",
             fb(SERIF_IT, 15), (220, 210, 180))
    y = 116
    # UTC timeline strip (one line)
    d.text((M, y), "THE DAY BY HOURS · UTC", font=fb(SANS_B, 11), fill=RED)
    tl = ("00:00 GTA VI unlocks in NZ  ·  MORNING Shenzhen summit opens  ·  "
          "10:00 World Court reads Rohingya judgment  ·  14:30 Anthropic's "
          "first trades  ·  EVENING COP31 ministers take over")
    d.text((M, y + 14), tl, font=fb(SANS, 10), fill=INK)
    y += 28
    rule(d, M, y, W - 2 * M, width=1)
    y += 5
    # leads row
    lw = (W - 2 * M - 32) // 3
    lead_bottom = y
    for i, s in enumerate(LEADS):
        lx = M + i * (lw + 16)
        b = lead_card(d, s, lx, y, lw, 84)
        lead_bottom = max(lead_bottom, b)
    y = lead_bottom + 6
    # navy numbers band
    d.rectangle([M, y, W - M, y + 44], fill=NAVY)
    numbers_strip(d, M, y, W - 2 * M, 44, dark=True)
    y += 50
    region_bar(d, M, y, W - 2 * M, 20)
    y += 24
    # cards rows
    cw = (W - 2 * M - 32) // 5
    for row in range(2):
        row_bottom = y
        for i in range(5):
            s = CARDS[row * 5 + i]
            cx = M + i * (cw + 8)
            b = small_card(d, s, cx, y, cw, 46)
            row_bottom = max(row_bottom, b)
        y = row_bottom + 5
        if row == 0:
            rule(d, M, y, W - 2 * M, width=1)
            y += 4
    rule(d, M, y, W - 2 * M, width=1)
    y += 5
    # bottom: map + briefs
    d.text((M, y), "WHERE IT HAPPENED", font=fb(SANS_B, 12), fill=RED)
    map_y = y + 18
    draw_map(d, M, map_y, 330, 140, NAVY, TAN)
    d.text((M, map_y + 144),
           "Red numbers mark stories 1–13. Positions are approximate.",
           font=fb(SANS, 10), fill=GREY)
    bx = M + 346
    briefs_bottom = briefs_block(d, bx, y, W - M - bx, 200)
    y = max(map_y + 162, briefs_bottom) + 6
    y = date_check_box(d, M, y, W - 2 * M)
    y += 6
    for ln in wrap(d, FOOTER, fb(SANS, 10), W - 2 * M):
        d.text((M, y), ln, font=fb(SANS, 10), fill=GREY)
        y += 12
    print("candidate B bottom y =", y)
    return img




# ================= v2: LATE FINAL EDITION (44 stories) ===============
# v1 (36-story, build_a/build_b) is kept above for reference; the
# default build is now the v2 late final edition (D1, 44 stories).
# `python3 compose.py` rebuilds image.jpg byte-identically;
# `python3 compose.py D2` builds the 36-story variant instead.

# ---------------- new flat illustrations ---------------------------------
def ill_tower(d, x, y, w, h):
    """PIF Tower, Riyadh — tall skyscraper at dusk, broken windows."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
    d.ellipse([x + w - 40, y + 8, x + w - 16, y + 32], fill=(240, 200, 90))
    # tower: slightly tapered, lit windows
    tx, tw = x + w * 0.30, w * 0.40
    d.polygon([(tx, y + h), (tx + 6, y + 8), (tx + tw - 6, y + 8),
               (tx + tw, y + h)], fill=(120, 140, 175))
    for r in range(5):
        for c in range(3):
            wx = tx + 10 + c * 14
            wy = y + 16 + r * 11
            d.rectangle([wx, wy, wx + 7, wy + 5], fill=(250, 210, 110))
    # broken windows: dark panes + red crack zigzag near the top
    for wx, wy in ((tx + 10, y + 16), (tx + 38, y + 27), (tx + 24, y + 38)):
        d.rectangle([wx, wy, wx + 7, wy + 5], fill=(30, 30, 40))
    cx, cy = tx + tw * 0.62, y + 22
    for dx, dy in ((0, 0), (8, 6), (-4, 10), (6, 16)):
        d.line([cx + dx, cy + dy, cx + dx + 6, cy + dy + 5],
               fill=(220, 60, 40), width=2)
    # neighbouring low blocks + debris dots
    d.rectangle([x + 8, y + h - 26, x + 30, y + h], fill=(70, 80, 110))
    d.rectangle([x + w - 32, y + h - 20, x + w - 8, y + h], fill=(70, 80, 110))
    for px, py in ((0.55, 0.55), (0.68, 0.62), (0.48, 0.70)):
        d.ellipse([x + w * px - 2, y + h * py - 2, x + w * px + 2,
                   y + h * py + 2], fill=(200, 200, 210))


def ill_greenland(d, x, y, w, h):
    """Greenland + Golden Dome: white ice island, radar dome, two flags."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 225))
    # island silhouette (white ice, green coast)
    d.polygon([(x + 12, y + h * 0.62), (x + 34, y + h * 0.30),
               (x + 70, y + h * 0.18), (x + 108, y + h * 0.26),
               (x + 138, y + h * 0.48), (x + 128, y + h * 0.72),
               (x + 90, y + h * 0.86), (x + 40, y + h * 0.82)],
              fill=(245, 248, 250))
    d.polygon([(x + 12, y + h * 0.62), (x + 40, y + h * 0.82),
               (x + 90, y + h * 0.86), (x + 128, y + h * 0.72),
               (x + 128, y + h * 0.86), (x + 12, y + h * 0.86)],
              fill=(120, 170, 120))
    # radar dome arc over the island
    d.arc([x + w * 0.28, y + h * 0.05, x + w * 0.78, y + h * 0.75],
          start=180, end=360, fill=(255, 255, 255), width=3)
    d.line([x + w * 0.53, y + h * 0.05, x + w * 0.53, y + h * 0.22],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.50, y + h * 0.02, x + w * 0.56, y + h * 0.08],
              fill=(255, 255, 255))
    # two small flags: Denmark (red/white cross) + US (stripes)
    for i, kind in enumerate(("DK", "US")):
        fx = x + 16 + i * 30
        d.line([fx + 8, y + h - 34, fx + 8, y + h - 12], fill=(60, 40, 30),
               width=2)
        if kind == "DK":
            d.rectangle([fx + 8, y + h - 34, fx + 26, y + h - 22],
                        fill=(200, 30, 40))
            d.rectangle([fx + 13, y + h - 34, fx + 16, y + h - 22],
                        fill=WHITE)
            d.rectangle([fx + 8, y + h - 29, fx + 26, y + h - 27],
                        fill=WHITE)
        else:
            for s in range(4):
                d.rectangle([fx + 8, y + h - 34 + s * 3, fx + 26,
                             y + h - 31 + s * 3],
                            fill=(178, 34, 34) if s % 2 == 0 else WHITE)
            d.rectangle([fx + 8, y + h - 34, fx + 16, y + h - 28],
                        fill=(30, 60, 120))


ILL["tower"] = ill_tower
ILL["greenland"] = ill_greenland
PINS.update({14: (46.7, 24.7), 15: (12.5, 55.7)})

# ---------------- v2 story data ------------------------------------------
LEADS2 = [
    dict(n=1, place="SHENZHEN", topic="SUMMIT", region="ASIA-PACIFIC",
         art="summit", src="REUTERS · BBC",
         head="Three leaders issue a peace declaration",
         deck="The first trilateral of the US, Chinese and Russian leaders "
              "ends with a four-point peace declaration. No Ukraine "
              "breakthrough."),
    dict(n=2, place="WORLDWIDE", topic="GAMES", region="WORLD",
         art="gta", src="REUTERS",
         head="GTA VI arrives after a 13-year wait",
         deck="Rockstar's sequel unlocks at midnight in each country, New "
              "Zealand first; 15.9m pre-orders banked. $79.99 on PS5 and "
              "Xbox, no PC yet."),
    dict(n=3, place="NASDAQ", topic="MARKETS", region="THE AMERICAS",
         art="ipo", src="REUTERS · BLOOMBERG",
         head="Anthropic debuts in the biggest IPO on record",
         deck="Priced at $83, above its range, the Claude maker raised "
              "$81.3bn and is valued near $1.5tn. First trades set the "
              "real price."),
]

CARDS2 = [
    dict(n=4, place="THE HAGUE", topic="LAW", region="EUROPE",
         art="court", src="ICJ · AP",
         head="World Court rules on Myanmar's Rohingya case",
         deck="The Gambia's case: final judgment, no appeal."),
    dict(n=5, place="ANTALYA", topic="CLIMATE", region="EUROPE",
         art="cop", src="UNFCCC",
         head="COP31 enters its final 48 hours",
         deck="Ministers take over the text; fund still open."),
    dict(n=6, place="ODISHA", topic="STORM", region="ASIA-PACIFIC",
         art="cyclone", src="IMD",
         head="Akvan bears down as 200,000 flee the coast",
         deck="Red alerts in 11 districts; landfall Friday."),
    dict(n=7, place="KERCH", topic="WAR", region="EUROPE",
         art="bridge", src="BBC · KYIV",
         head="Crimean Bridge hit a third time in a week",
         deck="Traffic halted after a fresh attack, officials say."),
    dict(n=8, place="GAZA", topic="WAR", region="MIDEAST",
         art="gaza", src="REUTERS",
         head="Israeli tanks cross the Gaza ceasefire line",
         deck="Raid beyond the Yellow Line; Hamas calls it a breach."),
    dict(n=9, place="FLORIDA", topic="WEATHER", region="THE AMERICAS",
         art="florida", src="AP · NWS",
         head="Flooded Florida braces for still more rain",
         deck="A foot of rain in hours; 300 rescue calls in a night."),
    dict(n=10, place="SEOUL", topic="EDUCATION", region="ASIA-PACIFIC",
         art="suneung", src="YONHAP",
         head="Half a million sit Korea's Suneung exam",
         deck="551,864 take the exam; flights pause for listening."),
    dict(n=11, place="HORMUZ", topic="GULF", region="MIDEAST",
         art="hormuz", src="REUTERS · CLAIM",
         head="Three tankers ablaze after mine strikes",
         deck="Iran's navy says the ships hit mines; traffic at 42%."),
    dict(n=12, place="BOGOTÁ", topic="LABOUR", region="THE AMERICAS",
         art="colombia", src="AFP",
         head="Colombia's unions strike nationwide",
         deck="Workers and teachers march against the tax bill."),
    dict(n=13, place="BENGHAZI", topic="CRIME", region="AFRICA",
         art="benghazi", src="AFP",
         head="Cocaine and millions of pills seized in Libya",
         deck="Officials display a record drug haul."),
    dict(n=14, place="RIYADH", topic="GULF", region="MIDEAST",
         art="tower", src="REUTERS · JPOST",
         head="Houthi missile hits Riyadh's tallest tower",
         deck="Windows blown out across 7–8 floors; the facade bent."),
    dict(n=15, place="COPENHAGEN", topic="ARCTIC", region="EUROPE",
         art="greenland", src="CNBC · GUARDIAN",
         head="Denmark ratifies US deal on Greenland",
         deck="Unanimous; expands the US role, incl. a missile shield."),
]

BRIEFS_D2 = [
    (16, "MEXICO CITY", "Banxico cuts rates to 6.25%."),
    (17, "CANBERRA", "Australia's jobless rate hits 4.9%."),
    (18, "MOGADISHU", "Somalia accuses UAE of secret bases."),
    (19, "NEW DELHI", "Modi meets the Prince and Princess of Wales."),
    (20, "TOKYO", "India and Japan review defence ties."),
    (21, "BENGALURU", "Amazon pledges $7bn for India renewables."),
    (22, "BAGHDAD", "Six French ISIL members jailed for life."),
    (23, "NAIROBI", "Kenya floods kill six; Ruto addresses nation."),
    (24, "CARACAS", "Hegseth signs a US–Venezuela military deal."),
    (25, "RIYADH", "Gulf leaders urge Trump not to strike Iran."),
    (26, "WASHINGTON", "Vance: no \u201cforever war\u201d in the Gulf."),
    (27, "OTTAWA", "Carney rethinks China ties."),
    (28, "VIENNA", "IAEA: North Korea expanded uranium enrichment."),
    (29, "LA PAZ", "Bolivia declares an El Ni\u00f1o emergency."),
    (30, "MADRID", "Police clash with strikers across Spain."),
    (31, "SYDNEY", "Duckett's 133 puts England on top in ODI."),
    (32, "DHAKA", "Bangladesh in turmoil: violence in 28 districts."),
    (33, "DAKAR", "Migrant boat capsizes; dozens missing."),
    (34, "SHENZHEN", "APEC leaders adopt the Shenzhen Declaration."),
    (35, "BERLIN", "Coalition of the Willing backs Ukraine."),
    (36, "JAKARTA", "Indonesia passes asset-seizure law."),
]

BRIEFS_D1_EXTRA = [
    (37, "AUCKLAND", "New Zealanders first into GTA VI at midnight."),
    (38, "WASHINGTON", "Trump: \u201cWe\u2019re not going to let Iran have a "
     "nuclear weapon.\u201d"),
    (39, "KYIV", "Zelenskyy: no decisions about Ukraine without Ukraine."),
    (40, "SACRAMENTO", "California braces for an atmospheric river."),
    (41, "THIMPHU", "A glacial lake burst floods Bhutan's hot springs."),
    (42, "MANAMA", "Bapco refinery back on its feet."),
    (43, "SANA'A", "Saudi air strikes hit Houthi targets, Houthi media report."),
    (44, "NEW YORK", "Take-Two shares rise 6% as GTA VI launches."),
]

REGIONS_D2 = [("EUROPE", 7), ("THE AMERICAS", 8), ("ASIA-PACIFIC", 9),
              ("MIDEAST", 5), ("AFRICA", 4), ("OCEANIA", 2), ("WORLD", 1)]
REGIONS_D1 = [("EUROPE", 8), ("THE AMERICAS", 11), ("ASIA-PACIFIC", 10),
              ("MIDEAST", 7), ("AFRICA", 4), ("OCEANIA", 3), ("WORLD", 1)]

NUMBERS2 = [
    ("$81.3bn", "raised by Anthropic, largest IPO ever"),
    ("15.9m", "GTA VI pre-orders banked"),
    ("200,000", "evacuated ahead of Akvan"),
    ("$120bn", "adaptation finance open at COP31"),
    ("730,000", "Rohingya who fled in 2017"),
    ("551,864", "sit Korea's college exam"),
    ("4.9%", "Australian jobless, 5-year high"),
    ("48 hrs", "left at COP31 in Antalya"),
]

TIMELINE = ("00:00 AUCKLAND GTA VI unlocks \u00b7 08:40 SEOUL exam begins "
            "\u00b7 04:42 RIYADH sirens \u00b7 09:30 JAKARTA law passed "
            "\u00b7 P.M. SHENZHEN declaration \u00b7 10:00 THE HAGUE "
            "ruling \u00b7 14:30 NEW YORK trades")

DATE_CHECK2 = ("DATE CHECK \u2014 FIRST REPORTED WEDNESDAY 18 NOV, SO NOT ON "
    "THIS PAGE AS NEWS: the Iranian drone interceptions over Kuwait and "
    "Bahrain \u00b7 the EU's proposed \u20ac45bn loan for Ukraine \u00b7 the "
    "House Democrats' 251\u201311 vote nominating Hakeem Jeffries \u00b7 "
    "Voyager 1 crossing one light-day, at 10:16 GMT Wednesday \u00b7 Van "
    "Gogh's record $190.4m sale \u00b7 Peltola's Alaska win \u00b7 Pew's "
    "projection that Islam becomes the largest religion by 2035 \u00b7 "
    "Nvidia's $115.8bn quarter \u00b7 Anthropic's $83 IPO pricing (Wed 18) "
    "\u00b7 the Canada\u2013China tariff deal (Wed 18) \u00b7 the US strike on "
    "Qeshm (Tue 17 Nov).  NOT YET: Akvan's landfall (Fri) \u00b7 COP31's "
    "final text (Fri) \u00b7 Anthropic's first-day close (Fri).")

FOOTER2 = ("Every story here happened, or was first reported, on Thursday 19 "
    "November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera, The Hindu, "
    "IMD, NASA, ICJ, IAEA. Original drawings.")

LEGEND = ("HOW SURE ARE WE?   REPORTED = on the record  \u00b7  CLAIM = one "
          "side's account  \u00b7  FORECAST = official prediction")


# ---------------- layout ---------------------------------------------------
def region_strip(d, x, y, w, total_label, regions):
    """#1-style text strip: every region label visible (fixes v1's G3).
    Shrinks the font until the whole line fits the page width."""
    sep = "  \u00b7  "
    parts = [(total_label, INK)]
    for name, count in regions:
        parts.append((f"{name} {count}", REGION_COLORS[name]))
    size = 11
    while size > 8:
        fnt = fb(SANS_B, size)
        total_w = sum(d.textlength(t, font=fnt) for t, _ in parts)
        total_w += (len(parts) - 1) * d.textlength(sep, font=fnt)
        if total_w <= w - 8:
            break
        size -= 1
    fnt = fb(SANS_B, size)
    total_w = sum(d.textlength(t, font=fnt) for t, _ in parts)
    total_w += (len(parts) - 1) * d.textlength(sep, font=fnt)
    cx = x + (w - total_w) / 2
    for i, (txt, col) in enumerate(parts):
        if i:
            d.text((cx, y), sep, font=fnt, fill=GREY)
            cx += d.textlength(sep, font=fnt)
        d.text((cx, y), txt, font=fnt, fill=col)
        cx += d.textlength(txt, font=fnt)


def timeline_strip(d, x, y, w):
    d.text((x, y), "THE DAY BY HOURS \u2014 LOCAL TIME, IN ORDER",
           font=fb(SANS_B, 11), fill=RED)
    d.text((x, y + 14), TIMELINE, font=fb(SANS, 10), fill=INK)
    return y + 28


def small_card_v2(d, s, x, y, w, ill_h):
    """6-column card: smaller head, deck capped at 2 lines."""
    ILL[s["art"]](d, x, y, w, ill_h)
    ty = y + ill_h + 5
    d.text((x, ty), f"{s['n']} \u00b7 {s['place']} \u00b7 {s['topic']}",
           font=fb(SANS_B, 9), fill=RED)
    ty += 13
    hf = fb(SERIF, 13)
    for ln in wrap(d, s["head"], hf, w)[:3]:
        d.text((x, ty), ln, font=hf, fill=INK)
        ty += 16
    df = fb(SANS, 10)
    for ln in wrap(d, s["deck"], df, w)[:2]:
        d.text((x, ty), ln, font=df, fill=(60, 60, 60))
        ty += 12
    return ty


def briefs_block_v2(d, x, y, w, briefs, header, row_h=12):
    d.text((x, y), header, font=fb(SANS_B, 12), fill=RED)
    y += 18
    col_w = (w - 16) / 2
    fnt = fb(SANS, 10)
    bf = fb(SANS_B, 10)
    per_col = (len(briefs) + 1) // 2
    bottom = y
    for ci in range(2):
        cx = x + ci * (col_w + 16)
        cy = y
        for n, place, txt in briefs[ci * per_col:(ci + 1) * per_col]:
            lines = wrap(d, f"{n} {place} \u2014 {txt}", fnt, col_w)
            first = lines[0]
            rest = first[len(str(n)) + 1:]
            d.text((cx, cy), str(n), font=bf, fill=RED)
            d.text((cx + d.textlength(str(n) + " ", font=bf), cy),
                   rest, font=fnt, fill=INK)
            cy += row_h
            for ln in lines[1:]:
                d.text((cx, cy), ln, font=fnt, fill=INK)
                cy += row_h
        bottom = max(bottom, cy)
    return bottom


def verdict_box(d, x, y, w, h=52):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.text((x + 8, y + 5), "THE VERDICT \u2014 THE HAGUE \u00b7 10:00",
           font=fb(SANS_B, 10), fill=GOLD)
    vf = fb(SANS, 10)
    ly = y + 20
    for ln in wrap(d, "Myanmar committed genocide, 9\u20136. First state "
                     "held liable. Must allow return, make reparations.",
                     vf, w - 16):
        d.text((x + 8, ly), ln, font=vf, fill=WHITE)
        ly += 12
    return y + h


def date_check_box_v2(d, x, y, w, font_size=9):
    fnt = fb(SANS, font_size)
    lines = wrap(d, DATE_CHECK2, fnt, w - 16)
    h = 6 + (font_size + 2) * len(lines) + 4
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    ly = y + 4
    for ln in lines:
        d.text((x + 8, ly), ln, font=fnt, fill=INK)
        ly += font_size + 2
    return y + h


CFG = {
    "D2": dict(lead_ill=82, map_h=120, brief_row=12, numbers_h=44,
               verdict_h=52),
    "D1": dict(lead_ill=68, map_h=96, brief_row=11, numbers_h=44,
               verdict_h=47),
}


def build_v2(which):
    if which == "D1":
        briefs = BRIEFS_D2 + BRIEFS_D1_EXTRA
        regions = REGIONS_D1
        total_label = "44 STORIES FROM 7 REGIONS"
        header = "ALSO ON THURSDAY 19 NOVEMBER \u2014 29 MORE STORIES"
        out = os.path.join(HERE, "image.jpg")
    else:
        briefs = BRIEFS_D2
        regions = REGIONS_D2
        total_label = "36 STORIES FROM 7 REGIONS"
        header = "ALSO ON THURSDAY 19 NOVEMBER \u2014 21 MORE STORIES"
        out = os.path.join(HERE, "candidate-d2.jpg")
    n_total = 3 + len(CARDS2) + len(briefs)
    assert n_total == (44 if which == "D1" else 36), n_total
    assert sum(c for _, c in regions) == n_total
    cfg = CFG[which]

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16
    y = 8
    d.text((M, y), "THE WORLD IN ONE DAY", font=fb(SANS_B, 13), fill=RED)
    right = f"LATE FINAL EDITION \u00b7 {n_total} STORIES"
    d.text((W - M - d.textlength(right, font=fb(SANS_B, 13)), y), right,
           font=fb(SANS_B, 13), fill=INK)
    y += 20
    rule(d, M, y, W - 2 * M, width=3)
    y += 6
    centered(d, W // 2, y, "Thursday 19 November 2026", fb(SERIF, 48), INK)
    y += 58
    centered(d, W // 2, y,
               "Three leaders issue a peace declaration \u00b7 A court rules "
               "on Myanmar \u00b7 The biggest IPO ever debuts",
               fb(SERIF_IT, 15), RED)
    y += 21
    y = timeline_strip(d, M, y, W - 2 * M)
    y += 2
    region_strip(d, M, y, W - 2 * M, total_label, regions)
    y += 18
    global NUMBERS
    NUMBERS = NUMBERS2
    numbers_strip(d, M, y, W - 2 * M, cfg["numbers_h"])
    y += cfg["numbers_h"] + 4
    rule(d, M, y, W - 2 * M, width=1)
    y += 4
    # leads row
    lw = (W - 2 * M - 32) // 3
    lead_bottom = y
    for i, s in enumerate(LEADS2):
        lx = M + i * (lw + 16)
        b = lead_card(d, s, lx, y, lw, cfg["lead_ill"])
        lead_bottom = max(lead_bottom, b)
    y = lead_bottom + 3
    rule(d, M, y, W - 2 * M, width=1)
    y += 3
    # cards rows: 2 rows of 6
    cw = (W - 2 * M - 40) // 6
    for row in range(2):
        row_bottom = y
        for i in range(6):
            s = CARDS2[row * 6 + i]
            cx = M + i * (cw + 8)
            b = small_card_v2(d, s, cx, y, cw, 46)
            row_bottom = max(row_bottom, b)
        y = row_bottom + 3
        if row == 0:
            rule(d, M, y, W - 2 * M, width=1)
            y += 2
    rule(d, M, y, W - 2 * M, width=1)
    y += 3
    # bottom: map + verdict | briefs
    d.text((M, y), "WHERE IT HAPPENED", font=fb(SANS_B, 12), fill=RED)
    map_y = y + 18
    draw_map(d, M, map_y, 330, cfg["map_h"], NAVY, (217, 201, 163))
    cap_y = map_y + cfg["map_h"] + 4
    d.text((M, cap_y),
           "Red numbers mark stories 1\u201315. Positions are approximate.",
           font=fb(SANS, 10), fill=GREY)
    verdict_box(d, M, cap_y + 16, 330, cfg["verdict_h"])
    bx = M + 346
    briefs_bottom = briefs_block_v2(d, bx, y, W - M - bx, briefs, header,
                                    cfg["brief_row"])
    y = max(cap_y + 16 + cfg["verdict_h"], briefs_bottom) + 4
    # legend line, full width
    lf = fb(SANS, 9)
    tw = d.textlength(LEGEND, font=lf)
    d.text(((W - tw) / 2, y), LEGEND, font=lf, fill=GREY)
    y += 12
    # date check
    y = date_check_box_v2(d, M, y, W - 2 * M, font_size=9)
    y += 4
    for ln in wrap(d, FOOTER2, fb(SANS, 10), W - 2 * M):
        d.text((M, y), ln, font=fb(SANS, 10), fill=GREY)
        y += 12
    print(f"candidate {which} bottom y =", y)
    return img, out


def main():
    which = sys.argv[1].upper() if len(sys.argv) > 1 else "D1"
    # verify the timeline line fits the page (regression: first D2 build
    # ran it off the right edge)
    probe = Image.new("RGB", (W, H), PAPER)
    pd = ImageDraw.Draw(probe)
    tw = pd.textlength(TIMELINE, font=fb(SANS, 10))
    print(f"timeline width = {tw:.0f}px (page inner width {W - 32})")
    assert tw <= W - 32, "timeline too wide"
    img, out = build_v2(which)
    img.save(out, "JPEG", quality=88)
    size = os.path.getsize(out)
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}, {size} bytes "
          f"(limit 1048576) {'OK' if size <= 1048576 else 'TOO BIG'}")


if __name__ == "__main__":
    main()
