#!/usr/bin/env python3
"""The Overnight Edition - NI22 round 4 for @desember179.

FALLER HYBRID: the round-2 page (13 pictured cards + 27 briefs, cream
field, date-as-masthead, red numbers strip, overnight timeline spine)
kept as the base, with five measured additions and nothing else:
  (a) a 16 px region tally bar under the numbers strip, segment widths
      proportional to story counts, labels inside the segments, and the
      segment counts summing exactly to the page's story total;
  (b) a fact-bearing slug bar on every pictured card (place/topic plus
      the card's biggest fact);
  (c) an italic subdeck under the date joining the three lead headlines;
  (d) a numbered badge on every pictured scene and numbered map pins
      for every story on the page, briefs included;
  (e) the round-2 DATE CHECK kept at full depth.
Written fresh for round 4. PIL + stdlib only. Renders entry.png and
entry-300.png next to this file.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # data asset: country polygons as lon:lat strings

W = H = 1024
MX = 14                      # page margin
CW = W - 2 * MX              # content width = 996
PAPER = (246, 240, 221)
CARD_BG = (255, 253, 246)
INK = (24, 36, 58)
NAVY = (22, 40, 63)
RED = (193, 39, 45)
GREY = (110, 104, 90)
SHADOW = (198, 190, 168)
SHEET = (232, 225, 203)
WHITE = (255, 255, 255)

REGIONS = {
    "GULF": (38, 92, 120),
    "ARABIA": (150, 96, 36),
    "ASIA": (44, 116, 84),
    "CLIMATE": (30, 122, 128),
    "OCEANIA": (146, 92, 32),
    "EUROPE": (52, 110, 62),
    "AMERICAS": (104, 74, 148),
}

FONT_DIR = os.path.join(HERE, "fonts")
SERIF = os.path.join(FONT_DIR, "PlayfairDisplay-900.ttf")
SANS_B = os.path.join(FONT_DIR, "Archivo-Bold.ttf")
SANS = os.path.join(FONT_DIR, "Archivo-Medium.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img, "RGBA")


def tw(f, s):
    return dr.textlength(s, font=f)


def wrap(f, s, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(f, trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(x, y, s, f, fill, gap=1):
    for ch in s:
        dr.text((x, y), ch, font=f, fill=fill)
        x += tw(f, ch) + gap
    return x


def spaced_w(f, s, gap=1):
    return sum(tw(f, c) for c in s) + gap * (len(s) - 1)


def pill(x, y, s, f, bg, fg=WHITE, pad=5):
    w = int(tw(f, s)) + 2 * pad
    h = f.size + 7
    dr.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    dr.text((x + pad, y + 3), s, font=f, fill=fg)
    return w


def badge(cx, cy, n, col, dia=17):
    r = dia / 2
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
               outline=WHITE, width=2)
    f = F(SANS_B, 10 if n < 10 else 9)
    s = str(n)
    dr.text((cx - tw(f, s) / 2, cy - f.size / 2 - 1), s, font=f, fill=WHITE)


def gradient(x, y, w, h, top, bottom, steps=24):
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        dr.rectangle([x, y + h * i / steps, x + w, y + h * (i + 1) / steps + 1],
                     fill=c)


def starfield(x, y, w, h, n, seed):
    rnd = random.Random(seed)
    for _ in range(n):
        sx = x + rnd.uniform(4, w - 4)
        sy = y + rnd.uniform(3, h * 0.55)
        r = rnd.choice([1, 1, 2])
        dr.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 238, 210))


def burst(cx, cy, r, col, spokes=8, width=2):
    for a in range(0, 360, 360 // spokes):
        dr.line([cx, cy, cx + r * math.cos(math.radians(a)),
                 cy + r * math.sin(math.radians(a))], fill=col, width=width)
    dr.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 240, 190))


# ------------------------------------------------------------- masthead
f_name = F(SANS_B, 15)
f_claim = F(SANS_B, 11)
dr.text((MX, 12), "THE OVERNIGHT EDITION", font=f_name, fill=NAVY)
dr.text((MX + tw(f_name, "THE OVERNIGHT EDITION") + 10, 15),
        "· THE NIGHT DESK · EST. TONIGHT", font=f_claim, fill=GREY)
claim = "40 STORIES · 7 REGIONS · EVERY ONE FROM ONE NIGHT"
dr.text((W - MX - tw(f_claim, claim), 15), claim, font=f_claim, fill=GREY)
dr.line([(MX, 36), (W - MX, 36)], fill=INK, width=2)

# Date as masthead: draw large on its own layer, scale into a 952x84 box.
DATE_TEXT = "SUNDAY 22 NOVEMBER 2026"
layer = Image.new("RGBA", (5200, 430), (0, 0, 0, 0))
ImageDraw.Draw(layer).text((10, 0), DATE_TEXT, font=F(SERIF, 345),
                           fill=NAVY + (255,))
layer = layer.crop(layer.getbbox()).resize((952, 84), Image.LANCZOS)
img.paste(layer, (36, 42), layer)
dr = ImageDraw.Draw(img, "RGBA")

# (c) Italic subdeck: the three lead headlines joined, sheared serif,
# fitted to a single line under the date.
LEAD_HEADS = [
    "IRGC claims two Patriot radars hit in Bahrain",
    "Houthi missile intercepted bound for Mecca region",
    "Deep M4.1 quake strikes Myanmar before dawn",
]
sub_text = " · ".join(LEAD_HEADS)
sub = Image.new("RGBA", (4200, 90), (0, 0, 0, 0))
ImageDraw.Draw(sub).text((6, 4), sub_text, font=F(SERIF, 40),
                         fill=(70, 62, 48, 255))
sub = sub.crop(sub.getbbox())
sub = sub.transform(sub.size, Image.AFFINE, (1, 0.30, -0.30 * 10, 0, 1, 0),
                    resample=Image.BICUBIC)
sub = sub.crop(sub.getbbox())
fit_w = min(CW - 8, sub.width)
fit_h = round(sub.height * fit_w / sub.width)
sub = sub.resize((fit_w, fit_h), Image.LANCZOS)
img.paste(sub, ((W - fit_w) // 2, 131), sub)
dr = ImageDraw.Draw(img, "RGBA")

# ------------------------------------------------------- numbers strip
NUMS = [
    ("2", "PATRIOT RADARS\nCLAIMED HIT · BAHRAIN"),
    ("05:42", "WIB - COALITION\nCONFIRMS INTERCEPTION"),
    ("M4.1", "MYANMAR QUAKE\n95 KM DEEP"),
    ("720/9", "INDIA'S RECORD TEST\nTOTAL · WELLINGTON"),
    ("50", "LAPS UNDER LIGHTS\nLAS VEGAS GP"),
    ("$4m", "LPGA WINNER'S PRIZE\nWOMEN'S GOLF RECORD"),
    ("11", "NFL GAMES SUNDAY\nWEEK 12 SLATE"),
]
dr.line([(MX, 160), (W - MX, 160)], fill=RED, width=3)
f_num = F(SANS_B, 34)
f_cap = F(SANS_B, 9)
cell = CW / 7.0
for i, (num, cap) in enumerate(NUMS):
    cx = MX + i * cell
    dr.text((cx + (cell - tw(f_num, num)) / 2, 164), num, font=f_num, fill=RED)
    for j, line in enumerate(cap.split("\n")):
        dr.text((cx + (cell - tw(f_cap, line)) / 2, 202 + j * 11), line,
                font=f_cap, fill=INK)
    if i:
        dr.line([(cx, 166), (cx, 220)], fill=(214, 206, 184), width=1)

# (a) Region tally bar: 16 px, labels inside, widths proportional.
TALLY = [("GULF", 5), ("ARABIA", 2), ("ASIA", 5), ("CLIMATE", 4),
         ("OCEANIA", 7), ("EUROPE", 5), ("AMERICAS", 12)]
TALLY_Y = 230
tx = float(MX)
for name, count in TALLY:
    seg_w = CW * count / 40.0
    dr.rectangle([tx, TALLY_Y, tx + seg_w - 1, TALLY_Y + 16],
                 fill=REGIONS[name])
    label = f"{name} {count}"
    lf = F(SANS_B, 10)
    if tw(lf, label) > seg_w - 6:
        lf = F(SANS_B, 8)
    dr.text((tx + (seg_w - tw(lf, label)) / 2, TALLY_Y + 3), label,
            font=lf, fill=WHITE)
    tx += seg_w

# ------------------------------------------------- overnight timeline
SLOTS = [
    ("02:40 WIB", "IRGC claim · Bahrain"),
    ("03:43 WIB", "Sirens · Mecca region"),
    ("04:05 WIB", "Myanmar quake M4.1"),
    ("05:42 WIB", "Interception confirmed"),
    ("06:00 GMT", "COP31 plenary · Antalya"),
    ("11:00 WIB", "Vegas GP lights out"),
]
TY = 272
dr.line([(30, TY), (W - 30, TY)], fill=NAVY, width=2)
f_slot = F(SANS_B, 11)
f_slotlab = F(SANS, 9)
slot_w = (W - 60) / 6.0
for i, (tm, lab) in enumerate(SLOTS):
    cx = 30 + slot_w * i + slot_w / 2
    dr.ellipse([cx - 5, TY - 5, cx + 5, TY + 5], fill=RED, outline=NAVY, width=1)
    dr.text((cx - tw(f_slot, tm) / 2, TY - 19), tm, font=f_slot, fill=RED)
    dr.text((cx - tw(f_slotlab, lab) / 2, TY + 9), lab, font=f_slotlab, fill=INK)


# ---------------------------------------------------------------- scenes
def frame(x, y, w, h):
    dr.rectangle([x - 4, y - 4, x + w - 4, y + h - 4], fill=SHEET)
    dr.rectangle([x + 6, y + 7, x + w + 6, y + h + 7], fill=SHADOW)
    dr.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=INK, width=1)


def slug_bar(x, y, w, text, col, size=10):
    dr.rectangle([x, y, x + w, y + 16], fill=col)
    f = F(SANS_B, size)
    while tw(f, text) > w - 14 and f.size > 7:
        f = F(SANS_B, f.size - 1)
    dr.text((x + 7, y + 3), text, font=f, fill=WHITE)


def sc_gulf(x, y, w, h):
    gradient(x, y, w, h, (16, 30, 54), (38, 66, 92))
    starfield(x, y, w, h, 20, 3)
    sea = y + h - 24
    dr.rectangle([x, sea, x + w, y + h], fill=(24, 52, 74))
    for i in range(5):
        yy = sea + 6 + (i % 2) * 7
        dr.line([x + 12 + i * 62, yy, x + 44 + i * 62, yy],
                fill=(90, 140, 170), width=2)
    # tanker, right foreground
    tx0, ty0 = x + w - 116, sea - 11
    dr.polygon([(tx0, ty0 + 7), (tx0 + 96, ty0 + 7), (tx0 + 84, ty0 + 15),
                (tx0 + 10, ty0 + 15)], fill=(8, 12, 20))
    dr.rectangle([tx0 + 16, ty0, tx0 + 30, ty0 + 7], fill=(8, 12, 20))
    dr.rectangle([tx0 + 58, ty0 - 4, tx0 + 68, ty0 + 7], fill=(8, 12, 20))
    # burning plant, centre
    px = x + 128
    dr.rectangle([px, sea - 20, px + 56, sea], fill=(10, 16, 26))
    dr.rectangle([px + 8, sea - 31, px + 14, sea - 20], fill=(10, 16, 26))
    for fx, fh in [(px + 28, 15), (px + 38, 10)]:
        dr.polygon([(fx, sea - 20), (fx + 5, sea - 20 - fh), (fx + 10, sea - 20)],
                   fill=(232, 120, 40))
        dr.polygon([(fx + 2, sea - 20), (fx + 5, sea - 20 - fh + 5),
                    (fx + 8, sea - 20)], fill=(245, 197, 24))
    # radar dish, left foreground
    rx, ry = x + 42, sea - 5
    dr.line([rx, ry, rx - 8, sea + 7], fill=(210, 214, 200), width=3)
    dr.line([rx, ry, rx + 10, sea + 7], fill=(210, 214, 200), width=3)
    dr.arc([rx - 25, ry - 32, rx + 25, ry + 13], start=300, end=130,
           fill=(225, 228, 210), width=4)
    dr.line([rx, ry - 9, rx + 19, ry - 24], fill=(225, 228, 210), width=2)
    # dashed missile arcs
    for off in (0, 26):
        pts = [(x + 14 + off + (t / 20) * 60, y + 5 + (t / 20) ** 1.6 * 42)
               for t in range(21)]
        for i in range(0, 20, 2):
            dr.line([pts[i], pts[i + 1]], fill=(235, 90, 80), width=2)
    burst(x + 78, y + 44, 9, (245, 197, 24))
    f = F(SANS_B, 10)
    pill(x + 8, y + 7, "2 RADARS CLAIMED", f, RED)
    pill(x + 8, y + 29, "02:40 WIB", f, NAVY)


def sc_mecca(x, y, w, h):
    gradient(x, y, w, h, (14, 26, 50), (44, 62, 96))
    starfield(x, y, w, h, 18, 11)
    mx0, my0 = x + w - 54, y + 14
    dr.ellipse([mx0, my0, mx0 + 30, my0 + 30], fill=(240, 230, 180))
    dr.ellipse([mx0 + 10, my0 - 2, mx0 + 38, my0 + 28], fill=(22, 36, 60))
    ground = y + h - 16
    dr.rectangle([x, ground, x + w, y + h], fill=(10, 16, 28))
    bx = x + 92
    dr.rectangle([bx, ground - 18, bx + 92, ground], fill=(8, 12, 22))
    dr.pieslice([bx + 16, ground - 40, bx + 76, ground - 6], 180, 360,
                fill=(8, 12, 22))
    dr.rectangle([bx + 43, ground - 48, bx + 49, ground - 36], fill=(8, 12, 22))
    dr.ellipse([bx + 42, ground - 53, bx + 50, ground - 45], fill=(240, 230, 180))
    tx0 = x + 214
    dr.rectangle([tx0, ground - 54, tx0 + 9, ground], fill=(8, 12, 22))
    dr.polygon([(tx0 - 3, ground - 54), (tx0 + 12, ground - 54),
                (tx0 + 4, ground - 66)], fill=(8, 12, 22))
    pts = [(x + 16 + i * 9, y + 50 - i * 3.2) for i in range(12)]
    for i in range(0, 11, 2):
        dr.line([pts[i], pts[i + 1]], fill=(235, 120, 90), width=2)
    burst(pts[-1][0], pts[-1][1], 13, (245, 197, 24), spokes=12)
    for r in (10, 17, 24):
        dr.arc([bx + 132 - r, ground - 32 - r, bx + 132 + r, ground - 32 + r],
               200, 320, fill=(120, 180, 220), width=2)
    f = F(SANS_B, 10)
    pill(x + 8, y + 7, "03:43 WIB SIRENS", f, NAVY)
    pill(x + 8, y + 29, "05:42 WIB CONFIRMED", f, RED)


def sc_quake(x, y, w, h):
    dr.rectangle([x, y, x + w, y + 24], fill=(30, 52, 84))
    starfield(x, y, w, 24, 10, 5)
    dr.rectangle([x, y + 24, x + w, y + 32], fill=(96, 128, 74))
    strata = [(146, 102, 64), (122, 84, 56), (96, 66, 48), (74, 52, 42)]
    for i, c in enumerate(strata):
        dr.rectangle([x, y + 32 + i * 16, x + w, y + 32 + (i + 1) * 16], fill=c)
    for bx, bw, bh in [(x + 28, 26, 11), (x + 60, 18, 8), (x + 208, 30, 12),
                       (x + 246, 20, 9)]:
        dr.rectangle([bx, y + 24 - bh, bx + bw, y + 24], fill=(14, 22, 34))
    cx, cy = x + 138, y + 28
    for r in (8, 16, 25):
        dr.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                   outline=(245, 197, 24), width=2)
    hx, hy = x + 138, y + h - 24
    burst(hx, hy, 10, (245, 150, 60), spokes=8)
    dr.line([cx, cy + 4, hx, hy - 9], fill=(245, 197, 24), width=2)
    gx = x + w - 38
    dr.rectangle([gx, y + 34, gx + 8, y + h - 6], fill=(230, 226, 205),
                 outline=INK, width=1)
    dr.rectangle([gx, y + h - 18, gx + 8, y + h - 6], fill=RED)
    f = F(SANS_B, 10)
    pill(x + 8, y + 5, "M4.1 · 04:05 WIB", f, RED)
    pill(x + w - 94, y + 5, "95 KM DEEP", f, NAVY)


# ------------------------------------------------------------- lead cards
LEADS = [
    dict(n=1, region="GULF", scene=sc_gulf,
         slug="BAHRAIN: 2 RADARS CLAIMED",
         caption="1 · BAHRAIN · GULF", tag="CLAIM · IRGC",
         head=LEAD_HEADS[0],
         deck="Tehran says its missile-and-drone strike hit 2 US Patriot "
              "radar sites (Al-Riffa, Awali); a drone fell over Kuwait."),
    dict(n=2, region="ARABIA", scene=sc_mecca,
         slug="MECCA REGION: MISSILE INTERCEPTED",
         caption="2 · MECCA REGION · ARABIA", tag="CONFIRMED · ANADOLU",
         head=LEAD_HEADS[1],
         deck="Sirens sounded across the Mecca region at 03:43 WIB; at "
              "05:42 WIB the coalition confirmed the Houthi missile "
              "was intercepted."),
    dict(n=3, region="ASIA", scene=sc_quake,
         slug="MYANMAR: M4.1 · 95 KM DEEP",
         caption="3 · MYANMAR · ASIA", tag="NCS · ANI",
         head=LEAD_HEADS[2],
         deck="India's NCS logged it at 04:05 WIB: magnitude 4.1, 95 km "
              "down, at 24.404N, 94.616E - a deep shock under Myanmar's "
              "north-west."),
]
LEAD_Y, LEAD_H, LEAD_SCENE = 300, 224, 98
for L, lx in zip(LEADS, [14, 350, 686]):
    lw_ = 324
    col = REGIONS[L["region"]]
    frame(lx, LEAD_Y, lw_, LEAD_H)
    slug_bar(lx + 1, LEAD_Y + 1, lw_ - 2, L["slug"], col, size=11)
    L["scene"](lx + 1, LEAD_Y + 17, lw_ - 2, LEAD_SCENE)
    badge(lx + lw_ - 16, LEAD_Y + 17 + LEAD_SCENE - 14, L["n"], col)
    cy = LEAD_Y + 17 + LEAD_SCENE + 3
    spaced(lx + 10, cy, L["caption"], F(SANS_B, 10), col, 1)
    tf = F(SANS_B, 9)
    spaced(lx + lw_ - spaced_w(tf, L["tag"], 1) - 10, cy, L["tag"], tf, GREY, 1)
    fh = F(SERIF, 19)
    hy = cy + 17
    for line in wrap(fh, L["head"], lw_ - 20)[:2]:
        dr.text((lx + 10, hy), line, font=fh, fill=INK)
        hy += 22
    fd = F(SANS, 12)
    for line in wrap(fd, L["deck"], lw_ - 20)[:3]:
        dr.text((lx + 10, hy + 2), line, font=fd, fill=(52, 48, 40))
        hy += 14


# ------------------------------------------------------------ mini strips
def st_clock(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(30, 122, 128))
    cx, cy, r = x + 24, y + h // 2, 12
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=2)
    dr.line([cx, cy, cx, cy - 8], fill=INK, width=2)
    dr.line([cx, cy, cx + 6, cy + 3], fill=RED, width=2)
    dr.text((x + 46, y + 10), "06:00 GMT PLENARY", font=F(SANS_B, 11), fill=WHITE)


def st_bars(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    dr.rectangle([x + 10, y + 6, x + 116, y + 13], fill=(146, 92, 32))
    dr.rectangle([x + 10, y + 20, x + 64, y + 27], fill=(90, 90, 90))
    dr.text((x + 120, y + 2), "720", font=F(SANS_B, 11), fill=INK)
    dr.text((x + 68, y + 16), "368", font=F(SANS_B, 11), fill=INK)


def st_track(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    pts = [(x + 14 + 15 * math.sin(i * 0.9) + i * 8, y + 16 + 9 * math.sin(i * 1.7))
           for i in range(11)]
    dr.line(pts, fill=(240, 230, 170), width=2)
    dr.text((x + 112, y + 9), "50 LAPS", font=F(SANS_B, 11), fill=(245, 197, 24))


def st_rocket(x, y, w, h):
    gradient(x, y, w, h, (18, 34, 66), (52, 84, 128))
    starfield(x, y, w, h, 9, 21)
    rx = x + 28
    dr.polygon([(rx, y + 3), (rx + 7, y + 11), (rx + 7, y + 22),
                (rx - 7, y + 22), (rx - 7, y + 11)], fill=(235, 235, 228))
    dr.polygon([(rx - 7, y + 22), (rx - 12, y + 28), (rx - 7, y + 28)], fill=RED)
    dr.polygon([(rx + 7, y + 22), (rx + 12, y + 28), (rx + 7, y + 28)], fill=RED)
    dr.polygon([(rx - 3, y + 28), (rx + 3, y + 28), (rx, y + 34)],
               fill=(245, 160, 60))
    dr.text((x + 52, y + 9), "GO · 12:16 UTC", font=F(SANS_B, 11), fill=WHITE)


def st_pitch(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(52, 128, 74))
    dr.rectangle([x + 6, y + 4, x + 84, y + h - 4], outline=WHITE, width=1)
    dr.line([x + 45, y + 4, x + 45, y + h - 4], fill=WHITE, width=1)
    dr.ellipse([x + 37, y + h // 2 - 8, x + 53, y + h // 2 + 8], outline=WHITE, width=1)
    dr.text((x + 94, y + 9), "16:30 UTC", font=F(SANS_B, 11), fill=WHITE)


def st_court(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(52, 92, 150))
    dr.rectangle([x + 8, y + 5, x + 76, y + h - 5], outline=WHITE, width=1)
    dr.line([x + 42, y + 5, x + 42, y + h - 5], fill=WHITE, width=1)
    dr.line([x + 8, y + h // 2, x + 76, y + h // 2], fill=WHITE, width=1)
    dr.text((x + 86, y + 9), "FINAL · TURIN", font=F(SANS_B, 11), fill=WHITE)


def st_board(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(224, 238, 224))
    rows = [("KIM", "-18", 60), ("THITIKUL", "-17", 48), ("YOSHIDA", "-17", 48)]
    for i, (nm, sc, bw) in enumerate(rows):
        yy = y + 4 + i * 10
        dr.text((x + 26, yy), nm, font=F(SANS_B, 8), fill=INK)
        bx = x + 74
        dr.rectangle([bx, yy + 1, bx + bw // 2, yy + 7], fill=(60, 130, 70))
        dr.text((bx + bw // 2 + 5, yy), sc, font=F(SANS_B, 8), fill=RED)


def st_dohyo(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(226, 208, 178))
    cx, cy = x + 32, y + h // 2
    dr.ellipse([cx - 16, cy - 12, cx + 16, cy + 12], fill=(214, 192, 150),
               outline=(120, 90, 50), width=2)
    dr.line([cx - 8, cy, cx + 8, cy], fill=(120, 90, 50), width=2)
    dr.text((x + 58, y + 9), "12-2 x2 LEAD", font=F(SANS_B, 11), fill=INK)


def st_rain(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    for i in range(9):
        rx = x + 8 + i * 10
        dr.line([rx, y + 4, rx - 3, y + 13], fill=(70, 110, 150), width=2)
    dr.text((x + 6, y + 18), "-9 x3 CO-LEAD", font=F(SANS_B, 9), fill=NAVY)
    dr.text((x + 104, y + 5), "SAT RAINED OUT", font=F(SANS_B, 9), fill=INK)


def st_nfl(x, y, w, h):
    dr.rectangle([x, y, x + w, y + h], fill=(36, 44, 84))
    for r in range(2):
        for c in range(6):
            if r * 6 + c < 11:
                cx, cy = x + 12 + c * 13, y + 9 + r * 13
                dr.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 230, 170))
    dr.text((x + 100, y + 9), "11 GAMES", font=F(SANS_B, 11), fill=(245, 197, 24))


MINIS = [
    dict(n=4, region="CLIMATE", strip=st_clock, tag="REUTERS",
         slug="ANTALYA COP31: FINAL TEXT TABLED",
         head="COP31 final text tabled, Antalya",
         deck="Kurum tables the final package late; objections close "
              "03:00 GMT, approval set 06:00 GMT."),
    dict(n=5, region="OCEANIA", strip=st_bars, tag="IANS · AFP",
         slug="WELLINGTON: INDIA 720/9",
         head="India declare on 720/9, a NZ record",
         deck="Rahul 136, Pant 128; NZ made 368 (Nicholls 175) - "
              "India lead by 352."),
    dict(n=6, region="AMERICAS", strip=st_track, tag="FORMULA1.COM",
         slug="LAS VEGAS GP: 50 LAPS",
         head="Las Vegas GP: lights out 11:00 WIB",
         deck="Round 22 on the Strip Circuit: 50 laps from 04:00 UTC Sunday."),
    dict(n=7, region="AMERICAS", strip=st_rocket, tag="OFFICIAL · VSFB",
         slug="VANDENBERG: FALCON 9 · 12:16 UTC",
         head="Falcon 9 NROL-136 set for Vandenberg",
         deck="Window 12:16-12:46 UTC, status GO; 15th NRO batch, "
              "booster B1097 lands LZ4."),
    dict(n=8, region="EUROPE", strip=st_pitch, tag="PREMIERLEAGUE.COM",
         slug="ANFIELD: LIVERPOOL v MAN UTD",
         head="Liverpool host Man United, Anfield",
         deck="Matchweek 11: Anfield 16:30 UTC (23:30 WIB); Hull v "
              "Brighton 14:00 UTC."),
    dict(n=9, region="EUROPE", strip=st_court, tag="ATP · REUTERS",
         slug="TURIN FINAL: ALCARAZ v ZVEREV",
         head="Alcaraz v Zverev: Turin final tonight",
         deck="Final ~16:00 UTC Sunday; Alcaraz came back past Shelton "
              "to reach it."),
    dict(n=10, region="AMERICAS", strip=st_board, tag="LPGA · AP",
         slug="NAPLES LPGA: $4M PRIZE",
         head="Kim leads CME finale by one, Naples",
         deck="A Lim Kim -18 at Tiburon; winner takes $4m, women's "
              "golf's biggest prize."),
    dict(n=11, region="ASIA", strip=st_dohyo, tag="JSA · DAY 14",
         slug="FUKUOKA SUMO: 12-2 LEADERS",
         head="Kyushu basho: final day in Fukuoka",
         deck="Onosato & Wakamotoharu 12-2, Atamifuji 11-3; last bout "
              "~09:00 UTC."),
    dict(n=12, region="AMERICAS", strip=st_rain, tag="REUTERS",
         slug="RSM CLASSIC: -9 CO-LEADERS",
         head="RSM round 3 washed into Sunday",
         deck="Three share -9: Thorbjornsen, Penge, Neergaard-Petersen; "
              "final now Monday."),
    dict(n=13, region="AMERICAS", strip=st_nfl, tag="ESPN · NFL",
         slug="NFL WEEK 12: 11 GAMES",
         head="NFL Week 12: 11 Sunday games",
         deck="Early window 18:00 UTC; night game Vikings @ 49ers, "
              "20:20 ET."),
]
MINI_W, MINI_H, STRIP_H = 191, 132, 34
f_tag = F(SANS_B, 8)
for idx, M in enumerate(MINIS):
    mx = 14 + (idx % 5) * 201
    my = 530 + (idx // 5) * 138
    col = REGIONS[M["region"]]
    frame(mx, my, MINI_W, MINI_H)
    slug_bar(mx + 1, my + 1, MINI_W - 2, M["slug"], col, size=9)
    M["strip"](mx + 1, my + 17, MINI_W - 2, STRIP_H)
    badge(mx + 13, my + 17 + STRIP_H - 11, M["n"], col, dia=15)
    tag_w = int(tw(f_tag, M["tag"])) + 8
    dr.rectangle([mx + MINI_W - tag_w - 3, my + 17 + STRIP_H - 13,
                  mx + MINI_W - 3, my + 17 + STRIP_H - 1], fill=NAVY)
    dr.text((mx + MINI_W - tag_w + 1, my + 17 + STRIP_H - 11), M["tag"],
            font=f_tag, fill=WHITE)
    fh = F(SANS_B, 13)
    hy = my + 17 + STRIP_H + 6
    for line in wrap(fh, M["head"], MINI_W - 16)[:2]:
        dr.text((mx + 8, hy), line, font=fh, fill=INK)
        hy += 16
    fd = F(SANS, 11)
    for line in wrap(fd, M["deck"], MINI_W - 16)[:3]:
        dr.text((mx + 8, hy + 1), line, font=fd, fill=(52, 48, 40))
        hy += 13


# ------------------------------------------------------------- bottom zone
BOT_Y = 806
dr.line([(MX, BOT_Y), (W - MX, BOT_Y)], fill=INK, width=2)
f_sec = F(SANS_B, 11)
dr.text((MX, BOT_Y + 6), "WHERE IT HAPPENED - THE OVERNIGHT MAP", font=f_sec, fill=NAVY)
dr.text((486, BOT_Y + 6), "ALSO ON THE NIGHT - 27 MORE STORIES", font=f_sec, fill=NAVY)

MAP_X, MAP_Y, MAP_W, MAP_H = 14, 828, 456, 118
dr.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
             fill=(24, 44, 40), outline=INK, width=1)


def proj(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W,
            MAP_Y + (76 - lat) / 132 * MAP_H)


for _name, rings in WORLD.items():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(proj(float(lo), float(la)))
        if len(pts) > 2:
            dr.polygon(pts, fill=(96, 138, 96))

# (text, region, lon, lat) for the 27 briefs, stories 14-40.
BRIEFS = [
    ("Bahrain ministry reported fires 23:25 local, Sat", "GULF", 50.6, 26.0),
    ("Bahrain asks UN Council to enforce Resolution 2817", "GULF", 50.4, 26.4),
    ("Kuwait drone grab: first at Ali Al Salem since September", "GULF", 47.9, 29.3),
    ("Hormuz tanker hit Sat 11:27 UTC (UKMTO)", "GULF", 56.3, 26.6),
    ("Mecca sirens first sounded 23:43 Riyadh time, Sat", "ARABIA", 39.7, 21.3),
    ("NCS clocked the quake at 02:35:57 IST", "ASIA", 94.7, 24.5),
    ("COP31 objections were closed at 03:00 GMT", "CLIMATE", 30.8, 36.8),
    ("COP31's $120bn adaptation target fell on Thursday", "CLIMATE", 30.6, 37.0),
    ("Chris Bowen co-hosts COP31 for Australia", "OCEANIA", 149.1, -35.3),
    ("COP31 draft recalls the Dubai fossil-fuel deal", "CLIMATE", 55.3, 25.2),
    ("Rahul 136 tops India's card at Wellington", "OCEANIA", 174.7, -41.2),
    ("Pant 128 in India's 720/9 declaration", "OCEANIA", 174.9, -41.4),
    ("Gill 98 · Jaiswal 85 · Padikkal 80 for India", "OCEANIA", 174.5, -41.0),
    ("Nicholls 175 anchors New Zealand's 368", "OCEANIA", 175.1, -41.3),
    ("Bumrah 4-92 in New Zealand's innings", "OCEANIA", 174.6, -41.5),
    ("Las Vegas is round 22 of the F1 season", "AMERICAS", -115.2, 36.0),
    ("Booster B1097 returns to Landing Zone 4", "AMERICAS", -120.5, 34.6),
    ("NROL-136 built with Northrop Grumman", "AMERICAS", -120.7, 34.8),
    ("Hull v Brighton kicks off 14:00 UTC", "EUROPE", -0.3, 53.7),
    ("Anfield clash is Premier League Matchweek 11", "EUROPE", -3.1, 53.5),
    ("Alcaraz fought back past Shelton in the semi", "EUROPE", 7.6, 45.0),
    ("Thitikul & Yoshida sit one back at -17", "AMERICAS", -81.7, 26.2),
    ("Wakamotoharu v Atamifuji decides the yusho", "ASIA", 130.3, 33.5),
    ("Atamifuji 11-3 still chases the Kyushu cup", "ASIA", 130.5, 33.7),
    ("Penge shares the RSM lead at -9", "AMERICAS", -81.5, 31.2),
    ("Neergaard-Petersen shares the RSM lead at -9", "AMERICAS", -81.3, 31.0),
    ("RSM Classic final round moves to Monday", "AMERICAS", -81.6, 31.4),
]
CARD_PINS = {1: (50.5, 26.2), 2: (39.8, 21.4), 3: (94.6, 24.4), 4: (30.7, 36.9),
             5: (174.8, -41.3), 6: (-115.1, 36.1), 7: (-120.6, 34.7),
             8: (-2.96, 53.4), 9: (7.7, 45.1), 10: (-81.8, 26.1),
             11: (130.4, 33.6), 12: (-81.4, 31.1), 13: (-122.4, 37.8)}
CARD_REGIONS = {1: "GULF", 2: "ARABIA", 3: "ASIA", 4: "CLIMATE", 5: "OCEANIA",
                6: "AMERICAS", 7: "AMERICAS", 8: "EUROPE", 9: "EUROPE",
                10: "AMERICAS", 11: "ASIA", 12: "AMERICAS", 13: "AMERICAS"}

# (d) Numbered pins for ALL 40 stories.
ALL_PINS = [(n, CARD_REGIONS[n], CARD_PINS[n][0], CARD_PINS[n][1])
            for n in range(1, 14)]
ALL_PINS += [(14 + i, b[1], b[2], b[3]) for i, b in enumerate(BRIEFS)]
f_pin = F(SANS_B, 8)
for n, region, lo, la in ALL_PINS:
    px, py = proj(lo, la)
    dr.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=REGIONS[region],
               outline=WHITE, width=1)
    s = str(n)
    dr.text((px - tw(f_pin, s) / 2, py - 4.5), s, font=f_pin, fill=WHITE)
dr.text((MX, MAP_Y + MAP_H + 4),
        "Numbered pins = all 40 stories: 1-13 pictured cards, 14-40 the briefs beside the map",
        font=F(SANS, 9), fill=INK)

f_brief = F(SANS, 9)
f_briefn = F(SANS_B, 9)
for col_i, items in enumerate([BRIEFS[:14], BRIEFS[14:]]):
    cx = 486 + col_i * 270
    for i, (text, region, _lo, _la) in enumerate(items):
        yy = 828 + i * 9.6
        n = 14 + col_i * 14 + i
        dr.text((cx, yy), str(n), font=f_briefn, fill=REGIONS[region])
        dr.text((cx + 19, yy), text, font=f_brief, fill=INK)

# -------------------------------------------------------------- DATE CHECK
DC_Y = 972
dr.rectangle([MX, DC_Y, W - MX, DC_Y + 28], outline=RED, width=2)
dr.text((22, DC_Y + 5), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
dc_text = ("Left out as not 22 Nov: Lviv strikes (20 Nov) · Peru M6.9 quake (20/21 Nov) · "
           "400-drone barrage (19-20 Nov) · ICJ ruling (19 Nov) · Berlin Coalition talks "
           "(19 Nov) · Geneva killer-robot deal (21 Nov). Not yet: Davis Cup final, 29 Nov.")
f_dc = F(SANS, 9)
for i, line in enumerate(wrap(f_dc, dc_text, W - 130)[:2]):
    dr.text((112, DC_Y + 4 + i * 11), line, font=f_dc, fill=INK)
dr.text((MX, 1006),
        "Every story happened, or was first reported, on Sunday 22 November 2026. "
        "Contested claims are attributed.",
        font=F(SANS, 9), fill=GREY)
foot_r = "Sources named on each card · Original drawings"
dr.text((W - MX - tw(F(SANS, 9), foot_r), 1006), foot_r, font=F(SANS, 9), fill=GREY)

# ------------------------------------------------------------------- save
assert sum(c for _n, c in TALLY) == 13 + len(BRIEFS) == 40
img.save(os.path.join(HERE, "_full.png"))
best = None
for colors in (256, 224, 192):
    q = img.quantize(colors=colors, method=Image.MEDIANCUT,
                     dither=Image.FLOYDSTEINBERG)
    out = os.path.join(HERE, "entry.png")
    q.save(out, optimize=True)
    best = os.path.getsize(out)
    print(f"colors={colors} bytes={best}")
    if best <= 160_000:
        break
os.remove(os.path.join(HERE, "_full.png"))
img.resize((300, 300), Image.LANCZOS).save(os.path.join(HERE, "entry-300.png"))
print("entry bytes:", best, "| pictured cards: 13 | stories: 40 |",
      "tally:", TALLY, "sum:", sum(c for _n, c in TALLY))
