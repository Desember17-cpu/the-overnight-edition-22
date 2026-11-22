#!/usr/bin/env python3
"""The Overnight Edition — NI22 challenger for @desember179.

A 3D layered broadsheet that tells Sunday 22 November 2026 in the order the
night happened: the date is the masthead, an overnight UTC/WIB spine runs
under the numbers strip, three pictorial lead scenes carry the night, and
every one of the 13 cards carries a data strip and a source tag.
All story facts come only from POOL22-BARU (13 verified 22 Nov events).
PIL only, stdlib only. Renders entry.png (1024x1024) next to this file.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402  (data asset: real country polygons)

W = H = 1024
PAPER = (246, 240, 221)
CARD = (255, 253, 246)
INK = (24, 36, 58)
NAVY = (22, 40, 63)
RED = (193, 39, 45)
GREY = (110, 104, 90)
SHADOW = (198, 190, 168)
SHEET = (232, 225, 203)

FDIR = os.path.join(HERE, "fonts")
PF = os.path.join(FDIR, "PlayfairDisplay-900.ttf")
AB = os.path.join(FDIR, "Archivo-Bold.ttf")
AM = os.path.join(FDIR, "Archivo-Medium.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")


def text_w(f, s):
    return d.textlength(s, font=f)


def wrap(f, s, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(f, t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def tracked(x, y, s, f, fill, spacing=1):
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += text_w(f, ch) + spacing
    return x


def tracked_w(f, s, spacing=1):
    return sum(text_w(f, c) for c in s) + spacing * (len(s) - 1)


# ---------------------------------------------------------------- masthead
fb_bar = font(AB, 15)
fb_bar_r = font(AB, 11)
d.text((14, 13), "THE OVERNIGHT EDITION", font=fb_bar, fill=NAVY)
d.text((14 + text_w(fb_bar, "THE OVERNIGHT EDITION") + 10, 16),
       "· THE NIGHT DESK · EST. TONIGHT", font=fb_bar_r, fill=GREY)
right = "40 STORIES · 7 REGIONS · EVERY ONE FROM ONE NIGHT"
d.text((W - 14 - text_w(fb_bar_r, right), 16), right, font=fb_bar_r, fill=GREY)
d.line([(14, 38), (W - 14, 38)], fill=INK, width=2)

# Date as its own layer: render big, then scale to a 952x88 glyph box.
DATE = "SUNDAY 22 NOVEMBER 2026"
big = font(PF, 345)
layer = Image.new("RGBA", (5000, 420), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
ld.text((10, 0), DATE, font=big, fill=NAVY + (255,))
bbox = layer.getbbox()
layer = layer.crop(bbox)
layer = layer.resize((952, 88), Image.LANCZOS)
img.paste(layer, (36, 44), layer)
d = ImageDraw.Draw(img, "RGBA")
DATE_BOX = (952, 88)

fk = font(AM, 11)
kick = ("The night desk's page, in the order it happened: Gulf claims, a missile over the "
        "Mecca region, a deep Myanmar quake — then the day's sport.")
kw = text_w(fk, kick)
d.text(((W - kw) / 2, 140), kick, font=fk, fill=(70, 62, 48))

# ------------------------------------------------------- numbers strip
NUMS = [
    ("2", "PATRIOT RADARS\nCLAIMED HIT · BAHRAIN", 1),
    ("05:42", "WIB — COALITION\nCONFIRMS INTERCEPTION", 2),
    ("M4.1", "MYANMAR QUAKE\n95 KM DEEP", 3),
    ("720/9", "INDIA'S RECORD TEST\nTOTAL · WELLINGTON", 5),
    ("50", "LAPS UNDER LIGHTS\nLAS VEGAS GP", 6),
    ("$4m", "LPGA WINNER'S PRIZE\nWOMEN'S GOLF RECORD", 10),
    ("11", "NFL GAMES SUNDAY\nWEEK 12 SLATE", 13),
]
d.line([(14, 158), (W - 14, 158)], fill=RED, width=3)
fnum = font(AB, 34)
fcap = font(AB, 9)
cellw = (W - 28) / 7.0
for i, (num, cap, _card) in enumerate(NUMS):
    cx = 14 + i * cellw
    nw = text_w(fnum, num)
    d.text((cx + (cellw - nw) / 2, 162), num, font=fnum, fill=RED)
    for j, line in enumerate(cap.split("\n")):
        lw = text_w(fcap, line)
        d.text((cx + (cellw - lw) / 2, 200 + j * 11), line, font=fcap, fill=INK)
    if i:
        d.line([(cx, 164), (cx, 218)], fill=(214, 206, 184), width=1)
NUM_DIGIT_PX = 34

# ------------------------------------------------- overnight timeline spine
SLOTS = [
    ("02:40 WIB", "IRGC claim · Bahrain"),
    ("03:43 WIB", "Sirens · Mecca region"),
    ("04:05 WIB", "Myanmar quake M4.1"),
    ("05:42 WIB", "Interception confirmed"),
    ("06:00 GMT", "COP31 plenary · Antalya"),
    ("11:00 WIB", "Vegas GP lights out"),
]
ty = 244
d.line([(30, ty), (W - 30, ty)], fill=NAVY, width=2)
ft = font(AB, 11)
fl = font(AM, 9)
slotw = (W - 60) / 6.0
for i, (tm, lab) in enumerate(SLOTS):
    cx = 30 + slotw * i + slotw / 2
    d.ellipse([cx - 5, ty - 5, cx + 5, ty + 5], fill=RED, outline=NAVY, width=1)
    tw = text_w(ft, tm)
    d.text((cx - tw / 2, ty - 18), tm, font=ft, fill=RED)
    lw = text_w(fl, lab)
    d.text((cx - lw / 2, ty + 9), lab, font=fl, fill=INK)

# ------------------------------------------------------------------- cards
REGION_COL = {
    "GULF": (51, 86, 110), "ARABIA": (122, 84, 40), "ASIA": (46, 110, 84),
    "CLIMATE": (38, 110, 120), "CRICKET": (140, 90, 30), "MOTORSPORT": (90, 60, 130),
    "SPACE": (40, 70, 140), "FOOTBALL": (30, 120, 60), "TENNIS": (170, 90, 40),
    "GOLF": (60, 130, 70), "SUMO": (150, 60, 60), "NFL": (70, 70, 150),
}


def card_frame(x, y, w, h):
    """3D layered sheet: back sheet + drop shadow + face."""
    d.rectangle([x - 4, y - 4, x + w - 4, y + h - 4], fill=SHEET)
    d.rectangle([x + 6, y + 7, x + w + 6, y + h + 7], fill=SHADOW)
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)


def chip(x, y, s, f, bg, fg=(255, 255, 255), pad=5):
    w = int(text_w(f, s)) + pad * 2
    h = f.size + 7
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    d.text((x + pad, y + 3), s, font=f, fill=fg)
    return w, h


def caption_band(x, y, w, s, tag):
    """Navy band at strip foot: place left, source/certainty tag right."""
    d.rectangle([x, y, x + w, y + 16], fill=NAVY)
    tracked(x + 6, y + 3, s, font(AB, 10), (255, 255, 255), 1)
    tf = font(AB, 9)
    tw = tracked_w(tf, tag, 1)
    tracked(x + w - tw - 6, y + 3, tag, tf, (255, 214, 120), 1)


def scene_base(x, y, w, h, top, bottom):
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + h * i / steps, x + w, y + h * (i + 1) / steps + 1], fill=c)


def stars(x, y, w, h, n=26, seed=7):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        sx, sy = x + rnd.uniform(4, w - 4), y + rnd.uniform(3, h * 0.55)
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 238, 210))


# ------------------------------------------------------------- lead scenes
def scene_gulf(x, y, w, h):
    scene_base(x, y, w, h, (16, 30, 54), (38, 66, 92))
    stars(x, y, w, h, 22, 3)
    sea = y + h - 26
    d.rectangle([x, sea, x + w, y + h], fill=(24, 52, 74))
    for i in range(5):
        d.line([x + 12 + i * 62, sea + 6 + (i % 2) * 7, x + 44 + i * 62, sea + 6 + (i % 2) * 7],
               fill=(90, 140, 170), width=2)
    # tanker silhouette (foreground, right)
    tx, ty = x + w - 118, sea - 12
    d.polygon([(tx, ty + 8), (tx + 96, ty + 8), (tx + 84, ty + 16), (tx + 10, ty + 16)], fill=(8, 12, 20))
    d.rectangle([tx + 16, ty, tx + 30, ty + 8], fill=(8, 12, 20))
    d.rectangle([tx + 58, ty - 4, tx + 68, ty + 8], fill=(8, 12, 20))
    # industrial plant with fire (midground, centre)
    px = x + 128
    d.rectangle([px, sea - 22, px + 58, sea], fill=(10, 16, 26))
    d.rectangle([px + 8, sea - 34, px + 14, sea - 22], fill=(10, 16, 26))
    for fx, fh in [(px + 30, 16), (px + 40, 11)]:
        d.polygon([(fx, sea - 22), (fx + 5, sea - 22 - fh), (fx + 10, sea - 22)], fill=(232, 120, 40))
        d.polygon([(fx + 2, sea - 22), (fx + 5, sea - 22 - fh + 5), (fx + 8, sea - 22)], fill=(245, 197, 24))
    # radar dish (foreground, left)
    rx, ry = x + 44, sea - 6
    d.line([rx, ry, rx - 8, sea + 8], fill=(210, 214, 200), width=3)
    d.line([rx, ry, rx + 10, sea + 8], fill=(210, 214, 200), width=3)
    d.arc([rx - 26, ry - 34, rx + 26, ry + 14], start=300, end=130, fill=(225, 228, 210), width=4)
    d.line([rx, ry - 10, rx + 20, ry - 26], fill=(225, 228, 210), width=2)
    # missile arcs (dashed red) falling toward the radar
    for k, off in enumerate((0, 26)):
        pts = []
        for t in range(21):
            u = t / 20
            mx = x + 16 + off + u * 62
            my = y + 6 + (u ** 1.6) * 44
            pts.append((mx, my))
        for i in range(0, len(pts) - 1, 2):
            d.line([pts[i], pts[i + 1]], fill=(235, 90, 80), width=2)
    for a in range(0, 360, 45):
        d.line([x + 80, y + 48, x + 80 + 9 * math.cos(math.radians(a)),
                y + 48 + 9 * math.sin(math.radians(a))], fill=(245, 197, 24), width=2)
    f = font(AB, 10)
    chip(x + 8, y + 7, "2 RADARS CLAIMED", f, RED)
    chip(x + 8, y + 29, "02:40 WIB", f, NAVY)


def scene_mecca(x, y, w, h):
    scene_base(x, y, w, h, (14, 26, 50), (44, 62, 96))
    stars(x, y, w, h, 20, 11)
    # crescent moon
    mx, my = x + w - 52, y + 16
    d.ellipse([mx, my, mx + 30, my + 30], fill=(240, 230, 180))
    d.ellipse([mx + 10, my - 2, mx + 38, my + 28], fill=(20, 34, 58))
    ground = y + h - 18
    d.rectangle([x, ground, x + w, y + h], fill=(10, 16, 28))
    # dome + minaret silhouette (foreground left-centre)
    bx = x + 96
    d.rectangle([bx, ground - 20, bx + 92, ground], fill=(8, 12, 22))
    d.pieslice([bx + 16, ground - 44, bx + 76, ground - 8], 180, 360, fill=(8, 12, 22))
    d.rectangle([bx + 43, ground - 52, bx + 49, ground - 40], fill=(8, 12, 22))
    d.ellipse([bx + 42, ground - 57, bx + 50, ground - 49], fill=(240, 230, 180))
    tx = x + 216
    d.rectangle([tx, ground - 58, tx + 9, ground], fill=(8, 12, 22))
    d.polygon([(tx - 3, ground - 58), (tx + 12, ground - 58), (tx + 4, ground - 70)], fill=(8, 12, 22))
    d.rectangle([tx - 4, ground - 44, tx + 13, ground - 40], fill=(8, 12, 22))
    # incoming missile + interception burst
    pts = [(x + 18 + i * 9, y + 52 - i * 3.4) for i in range(12)]
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(235, 120, 90), width=2)
    ex, ey = pts[-1]
    for a in range(0, 360, 30):
        d.line([ex, ey, ex + 13 * math.cos(math.radians(a)), ey + 13 * math.sin(math.radians(a))],
               fill=(245, 197, 24), width=2)
    d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 240, 190))
    # siren arcs over the city
    for r in (10, 17, 24):
        d.arc([bx + 130 - r, ground - 34 - r, bx + 130 + r, ground - 34 + r], 200, 320,
              fill=(120, 180, 220), width=2)
    f = font(AB, 10)
    chip(x + 8, y + 7, "03:43 WIB SIRENS", f, NAVY)
    chip(x + 8, y + 29, "05:42 WIB CONFIRMED", f, RED)


def scene_quake(x, y, w, h):
    # sky + surface
    d.rectangle([x, y, x + w, y + 26], fill=(30, 52, 84))
    stars(x, y, w, 26, 12, 5)
    d.rectangle([x, y + 26, x + w, y + 34], fill=(96, 128, 74))
    # rock strata below
    strata = [(120, 96, 70), (100, 78, 58), (82, 62, 48), (64, 48, 40)]
    for i, c in enumerate(strata):
        d.rectangle([x, y + 34 + i * 15, x + w, y + 34 + (i + 1) * 15], fill=c)
    # surface town silhouette
    for bx, bw, bh in [(x + 30, 26, 12), (x + 62, 18, 9), (x + 210, 30, 13), (x + 248, 20, 10)]:
        d.rectangle([bx, y + 26 - bh, bx + bw, y + 26], fill=(14, 22, 34))
    # epicentre rings on surface + hypocentre star at depth
    cx, cy = x + 140, y + 30
    for r in (8, 16, 25):
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=(245, 197, 24), width=2)
    hx, hy = x + 140, y + h - 28
    for a in range(0, 360, 45):
        d.line([hx, hy, hx + 10 * math.cos(math.radians(a)), hy + 10 * math.sin(math.radians(a))],
               fill=(245, 120, 60), width=2)
    d.line([cx, cy + 4, hx, hy - 8], fill=(245, 197, 24), width=2)
    # depth gauge (right)
    gx = x + w - 40
    d.rectangle([gx, y + 36, gx + 8, y + h - 8], fill=(230, 226, 205), outline=INK, width=1)
    d.rectangle([gx, y + h - 20, gx + 8, y + h - 8], fill=RED)
    f = font(AB, 10)
    chip(x + 8, y + 6, "M4.1 · 04:05 WIB", f, RED)
    chip(x + w - 92, y + 6, "95 KM DEEP", f, NAVY)


LEADS = [
    dict(n=1, reg="GULF · OVERNIGHT STRIKES", col=REGION_COL["GULF"], scene=scene_gulf,
         band="BAHRAIN · KUWAIT · THE GULF", tag="CLAIM · IRGC",
         head="IRGC claims two Patriot radars hit in Bahrain",
         deck="Tehran says a joint missile-and-drone strike hit 2 US Patriot radar sites "
              "(Al-Riffa, Awali); a civil site burned in Bahrain, a drone fell over Kuwait.",
         facts=3),
    dict(n=2, reg="ARABIA · AIR DEFENCE", col=REGION_COL["ARABIA"], scene=scene_mecca,
         band="MECCA · SAUDI ARABIA", tag="CONFIRMED · ANADOLU",
         head="Houthi missile intercepted bound for Mecca region",
         deck="Sirens sounded across the Mecca region at 03:43 WIB; at 05:42 WIB the "
              "Saudi-led coalition confirmed the Houthi missile was intercepted.",
         facts=3),
    dict(n=3, reg="ASIA · EARTHQUAKE", col=REGION_COL["ASIA"], scene=scene_quake,
         band="MYANMAR · 24.404N 94.616E", tag="NCS · ANI",
         head="Deep M4.1 quake strikes Myanmar before dawn",
         deck="India's NCS logged it at 04:05 WIB: magnitude 4.1, 95 km down, at "
              "24.404N, 94.616E — a deep, quiet shock under Myanmar's north-west.",
         facts=4),
]

LEAD_Y, LEAD_H, SCENE_H = 268, 212, 98
lead_xs = [14, 350, 686]
for L, lx in zip(LEADS, lead_xs):
    lw_ = 324
    card_frame(lx, LEAD_Y, lw_, LEAD_H)
    L["scene"](lx + 1, LEAD_Y + 1, lw_ - 2, SCENE_H)
    caption_band(lx + 1, LEAD_Y + SCENE_H - 15, lw_ - 2, L["band"], L["tag"])
    d.line([(lx, LEAD_Y + SCENE_H + 1), (lx + lw_, LEAD_Y + SCENE_H + 1)], fill=L["col"], width=3)
    tracked(lx + 10, LEAD_Y + SCENE_H + 8, f"{L['n']}  {L['reg']}", font(AB, 10), L["col"], 1)
    fh = font(PF, 19)
    hy = LEAD_Y + SCENE_H + 24
    for line in wrap(fh, L["head"], lw_ - 20):
        d.text((lx + 10, hy), line, font=fh, fill=INK)
        hy += 23
    fd = font(AM, 12)
    for line in wrap(fd, L["deck"], lw_ - 20)[:3]:
        d.text((lx + 10, hy + 2), line, font=fd, fill=(52, 48, 40))
        hy += 15


# -------------------------------------------------------------- mini cards
def dev_clock(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 230))
    cx, cy, r = x + 26, y + h // 2, 13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=NAVY, width=2)
    d.line([cx, cy, cx, cy - 9], fill=INK, width=2)
    d.line([cx, cy, cx + 7, cy + 3], fill=RED, width=2)
    chip(x + 48, y + 8, "06:00 GMT PLENARY", font(AB, 9), NAVY)


def dev_bars720(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.rectangle([x + 10, y + 6, x + 118, y + 13], fill=(140, 90, 30))
    d.rectangle([x + 10, y + 20, x + 66, y + 27], fill=(90, 90, 90))
    d.text((x + 122, y + 2), "720", font=font(AB, 11), fill=INK)
    d.text((x + 70, y + 16), "368", font=font(AB, 11), fill=INK)


def dev_track(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    pts = [(x + 14 + 15 * math.sin(i * 0.9) + i * 8, y + 17 + 9 * math.sin(i * 1.7)) for i in range(11)]
    d.line(pts, fill=(240, 230, 170), width=2)
    for px, py in [(x + 16, y + 10), (x + 16, y + 24)]:
        d.ellipse([px, py, px + 5, py + 5], fill=RED)
    chip(x + 118, y + 8, "50 LAPS", font(AB, 9), RED)


def dev_rocket(x, y, w, h):
    scene_base(x, y, w, h, (18, 34, 66), (52, 84, 128))
    stars(x, y, w, h, 10, 21)
    rx = x + 30
    d.polygon([(rx, y + 4), (rx + 7, y + 12), (rx + 7, y + 24), (rx - 7, y + 24), (rx - 7, y + 12)],
              fill=(235, 235, 228))
    d.polygon([(rx - 7, y + 24), (rx - 12, y + 30), (rx - 7, y + 30)], fill=RED)
    d.polygon([(rx + 7, y + 24), (rx + 12, y + 30), (rx + 7, y + 30)], fill=RED)
    d.polygon([(rx - 3, y + 30), (rx + 3, y + 30), (rx, y + 36)], fill=(245, 160, 60))
    chip(x + 56, y + 8, "GO · 12:16 UTC", font(AB, 9), (30, 120, 60))


def dev_pitch(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 128, 74))
    d.rectangle([x + 6, y + 4, x + 86, y + h - 4], outline=(255, 255, 255), width=1)
    d.line([x + 46, y + 4, x + 46, y + h - 4], fill=(255, 255, 255), width=1)
    d.ellipse([x + 38, y + h // 2 - 8, x + 54, y + h // 2 + 8], outline=(255, 255, 255), width=1)
    chip(x + 96, y + 8, "16:30 UTC", font(AB, 9), NAVY)


def dev_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 92, 150))
    d.rectangle([x + 8, y + 5, x + 78, y + h - 5], outline=(255, 255, 255), width=1)
    d.line([x + 43, y + 5, x + 43, y + h - 5], fill=(255, 255, 255), width=1)
    d.line([x + 8, y + h // 2, x + 78, y + h // 2], fill=(255, 255, 255), width=1)
    chip(x + 88, y + 8, "FINAL · TURIN", font(AB, 9), NAVY)


def dev_leaderboard(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 224))
    for i, (nm, sc, bw) in enumerate([("KIM", "-18", 104), ("THITIKUL", "-17", 88), ("YOSHIDA", "-17", 88)]):
        yy = y + 4 + i * 11
        d.text((x + 6, yy), nm, font=font(AB, 9), fill=INK)
        d.rectangle([x + 52, yy + 1, x + 52 + bw // 2, yy + 8], fill=(60, 130, 70))
        d.text((x + 160, yy), sc, font=font(AB, 9), fill=RED)


def dev_dohyo(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 208, 178))
    cx, cy = x + 34, y + h // 2
    d.ellipse([cx - 16, cy - 13, cx + 16, cy + 13], fill=(214, 192, 150), outline=(120, 90, 50), width=2)
    d.line([cx - 8, cy, cx + 8, cy], fill=(120, 90, 50), width=2)
    chip(x + 62, y + 5, "12-2 ×2 LEAD", font(AB, 9), NAVY)


def dev_rain(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    for i in range(9):
        rx = x + 8 + i * 10
        d.line([rx, y + 4, rx - 3, y + 13], fill=(70, 110, 150), width=2)
    chip(x + 6, y + 17, "-9 ×3 CO-LEAD", font(AB, 9), NAVY)
    d.text((x + 104, y + 5), "SAT RAINED OUT", font=font(AB, 9), fill=INK)


def dev_nfl(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(36, 44, 84))
    for r in range(2):
        for c in range(6):
            if r * 6 + c < 11:
                cx, cy = x + 12 + c * 13, y + 9 + r * 13
                d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 230, 170))
    chip(x + 100, y + 8, "11 GAMES", font(AB, 9), RED)


MINIS = [
    dict(n=4, reg="GLOBAL · CLIMATE", col=REGION_COL["CLIMATE"], dev=dev_clock, tag="REUTERS",
         head="COP31 final text tabled, Antalya",
         deck="Kurum tables the final package late; objections close 03:00 GMT, approval set 06:00 GMT.", facts=3),
    dict(n=5, reg="OCEANIA · CRICKET", col=REGION_COL["CRICKET"], dev=dev_bars720, tag="IANS · AFP",
         head="India declare on 720/9, a NZ record",
         deck="Rahul 136, Pant 128; NZ made 368 (Nicholls 175) — India lead by 352.", facts=4),
    dict(n=6, reg="AMERICAS · F1", col=REGION_COL["MOTORSPORT"], dev=dev_track, tag="FORMULA1.COM",
         head="Las Vegas GP: lights out 11:00 WIB",
         deck="Round 22 on the Strip Circuit: 50 laps from 04:00 UTC Sunday.", facts=3),
    dict(n=7, reg="AMERICAS · SPACE", col=REGION_COL["SPACE"], dev=dev_rocket, tag="OFFICIAL · VSFB",
         head="Falcon 9 NROL-136 set for Vandenberg",
         deck="Window 12:16–12:46 UTC, status GO; 15th NRO batch, booster B1097 lands LZ4.", facts=3),
    dict(n=8, reg="EUROPE · FOOTBALL", col=REGION_COL["FOOTBALL"], dev=dev_pitch, tag="PREMIERLEAGUE.COM",
         head="Liverpool host Man United, Anfield",
         deck="Matchweek 11: Anfield 16:30 UTC (23:30 WIB); Hull v Brighton 14:00 UTC.", facts=3),
    dict(n=9, reg="EUROPE · TENNIS", col=REGION_COL["TENNIS"], dev=dev_court, tag="ATP · REUTERS",
         head="Alcaraz v Zverev: Turin final tonight",
         deck="Final ~16:00 UTC Sunday; Alcaraz came back past Shelton to reach it.", facts=2),
    dict(n=10, reg="AMERICAS · GOLF", col=REGION_COL["GOLF"], dev=dev_leaderboard, tag="LPGA · AP",
         head="Kim leads CME finale by one, Naples",
         deck="A Lim Kim -18 at Tiburón; winner takes $4m, women's golf's biggest prize.", facts=3),
    dict(n=11, reg="ASIA · SUMO", col=REGION_COL["SUMO"], dev=dev_dohyo, tag="JSA · DAY 14",
         head="Kyushu basho: final day in Fukuoka",
         deck="Onosato & Wakamotoharu 12-2, Atamifuji 11-3; last bout ~09:00 UTC.", facts=3),
    dict(n=12, reg="AMERICAS · GOLF", col=REGION_COL["GOLF"], dev=dev_rain, tag="REUTERS",
         head="RSM round 3 washed into Sunday",
         deck="Three share -9: Thorbjornsen, Penge, Neergaard-Petersen; final now Monday.", facts=3),
    dict(n=13, reg="AMERICAS · NFL", col=REGION_COL["NFL"], dev=dev_nfl, tag="ESPN · NFL",
         head="NFL Week 12: 11 Sunday games",
         deck="Early window 18:00 UTC; night game Vikings @ 49ers, 20:20 ET.", facts=3),
]

MINI_W, MINI_H, STRIP_H = 191, 132, 36
mini_pos = []
for r in range(2):
    for c in range(5):
        mini_pos.append((14 + c * 201, 488 + r * 140))
fhtag = font(AB, 9)
for M, (mx, my) in zip(MINIS, mini_pos):
    card_frame(mx, my, MINI_W, MINI_H)
    M["dev"](mx + 1, my + 1, MINI_W - 2, STRIP_H)
    tf = fhtag
    tw = tracked_w(tf, M["tag"], 1)
    d.rectangle([mx + MINI_W - tw - 12, my + STRIP_H - 13, mx + MINI_W - 3, my + STRIP_H - 1], fill=NAVY)
    tracked(mx + MINI_W - tw - 9, my + STRIP_H - 11, M["tag"], tf, (255, 255, 255), 1)
    tracked(mx + 8, my + STRIP_H + 5, f"{M['n']}  {M['reg']}", font(AB, 9), M["col"], 1)
    fh = font(AB, 14)
    hy = my + STRIP_H + 19
    for line in wrap(fh, M["head"], MINI_W - 16)[:2]:
        d.text((mx + 8, hy), line, font=fh, fill=INK)
        hy += 17
    fd = font(AM, 12)
    for line in wrap(fd, M["deck"], MINI_W - 16)[:3]:
        d.text((mx + 8, hy + 1), line, font=fd, fill=(52, 48, 40))
        hy += 14

# ------------------------------------------------------------- bottom zone
BOT_Y = 768
d.line([(14, BOT_Y - 6), (W - 14, BOT_Y - 6)], fill=INK, width=2)
ftitle = font(AB, 11)
d.text((14, BOT_Y), "WHERE IT HAPPENED — THE OVERNIGHT MAP", font=ftitle, fill=NAVY)
d.text((486, BOT_Y), "ALSO ON THE NIGHT — 27 MORE STORIES", font=ftitle, fill=NAVY)

MAP = (14, BOT_Y + 18, 456, 148)
mx0, my0, mw, mh = MAP
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(24, 44, 40), outline=INK, width=1)


def proj(lon, lat):
    return (mx0 + (lon + 180) / 360 * mw, my0 + (76 - lat) / 132 * mh)


for _name, rings in WORLD.items():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(proj(float(lo), float(la)))
        if len(pts) > 2:
            d.polygon(pts, fill=(96, 138, 96))

PINS = {1: (50.5, 26.2), 2: (39.8, 21.4), 3: (94.6, 24.4), 4: (30.7, 36.9),
        5: (174.8, -41.3), 6: (-115.1, 36.1), 7: (-120.6, 34.7), 8: (-2.96, 53.4),
        9: (7.7, 45.1), 10: (-81.8, 26.1), 11: (130.4, 33.6), 12: (-81.4, 31.1),
        13: (-122.4, 37.8)}
fpin = font(AB, 10)
for n, (lo, la) in PINS.items():
    px, py = proj(lo, la)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
    s = str(n)
    d.text((px - text_w(fpin, s) / 2, py - 6), s, font=fpin, fill=(255, 255, 255))
for lo, la in [(51.5, 26.0), (39.0, 21.5), (95.5, 24.0), (31.5, 36.5), (174.0, -41.0),
               (-81.0, 26.5), (131.0, 33.0), (-122.0, 37.0)]:
    px, py = proj(lo, la)
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 230, 170))
fleg = font(AM, 9)
d.text((14, my0 + mh + 5),
       "Numbered pins = the 13 pictured cards · small dots = the briefs listed beside the map",
       font=fleg, fill=INK)

BRIEFS = [
    "Bahrain ministry reported fires 23:25 local, Sat",
    "Bahrain asks UN Council to enforce Resolution 2817",
    "Kuwait drone grab: first at Ali Al Salem since September",
    "Hormuz tanker hit Sat 11:27 UTC (UKMTO)",
    "Mecca sirens first sounded 23:43 Riyadh time, Sat",
    "NCS clocked the quake at 02:35:57 IST",
    "COP31 objections were closed at 03:00 GMT",
    "COP31's $120bn adaptation target fell on Thursday",
    "Chris Bowen co-hosts COP31 for Australia",
    "COP31 draft recalls the Dubai fossil-fuel deal",
    "Rahul 136 tops India's card at Wellington",
    "Pant 128 in India's 720/9 declaration",
    "Gill 98 · Jaiswal 85 · Padikkal 80 for India",
    "Nicholls 175 anchors New Zealand's 368",
    "Bumrah 4-92 in New Zealand's innings",
    "Las Vegas is round 22 of the F1 season",
    "Booster B1097 returns to Landing Zone 4",
    "NROL-136 built with Northrop Grumman",
    "Hull v Brighton kicks off 14:00 UTC",
    "Anfield clash is Premier League Matchweek 11",
    "Alcaraz fought back past Shelton in the semi",
    "Thitikul & Yoshida sit one back at -17",
    "Wakamotoharu v Atamifuji decides the yusho",
    "Atamifuji 11-3 still chases the Kyushu cup",
    "Penge shares the RSM lead at -9",
    "Neergaard-Petersen shares the RSM lead at -9",
    "RSM Classic final round moves to Monday",
]
fb = font(AM, 10)
fn = font(AB, 10)
cols = [(486, BRIEFS[:14]), (756, BRIEFS[14:])]
for cx, items in cols:
    for i, b in enumerate(items):
        yy = BOT_Y + 20 + i * 12.6
        num = str(14 + BRIEFS.index(b)) if False else None
        idx = BRIEFS.index(b)
        d.text((cx, yy), f"{14 + idx}", font=fn, fill=RED)
        d.text((cx + 20, yy), b, font=fb, fill=INK)

# -------------------------------------------------------------- DATE CHECK
DC_Y = 966
d.rectangle([14, DC_Y, W - 14, DC_Y + 30], outline=RED, width=2)
d.text((22, DC_Y + 4), "DATE CHECK", font=font(AB, 10), fill=RED)
dc = ("Left out as not 22 Nov: Lviv strikes (20 Nov) · Peru M6.9 quake (20/21 Nov) · 400-drone barrage (19–20 Nov) · "
      "ICJ ruling (19 Nov) · Berlin Coalition talks (19 Nov) · Geneva killer-robot deal (21 Nov). Not yet: Davis Cup final, 29 Nov.")
fdc = font(AM, 9)
for i, line in enumerate(wrap(fdc, dc, W - 130)):
    d.text((112, DC_Y + 4 + i * 11), line, font=fdc, fill=INK)

d.text((14, 1002),
       "Every story happened, or was first reported, on Sunday 22 November 2026. Contested claims are attributed.",
       font=font(AM, 9), fill=GREY)
foot_r = "Sources named on each card · Original drawings"
d.text((W - 14 - text_w(font(AM, 9), foot_r), 1002), foot_r, font=font(AM, 9), fill=GREY)

# ------------------------------------------------------------------- save
raw = os.path.join(HERE, "_entry_full.png")
img.save(raw)
best = None
for colors in (256, 224, 192):
    q = img.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    out = os.path.join(HERE, "entry.png")
    q.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"colors={colors} bytes={size}")
    if size <= 160_000:
        best = size
        break
    best = size
img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "entry-300.png"))
os.remove(raw)
print("entry bytes:", best, "date box:", DATE_BOX, "digit px:", NUM_DIGIT_PX)
print("cards>=2 facts:", sum(1 for c in LEADS + MINIS if c["facts"] >= 2), "/13",
      "avg facts:", sum(c["facts"] for c in LEADS + MINIS) / 13)
print("stories total:", 13 + len(BRIEFS), "briefs:", len(BRIEFS), "timeline slots:", len(SLOTS),
      "numbers:", len(NUMS))
