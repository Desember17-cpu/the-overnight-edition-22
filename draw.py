#!/usr/bin/env python3
"""The Overnight Edition — round 3 REVISED build for @desember179 (NI22).

Revision driven by BEDAH-TOP1.md (pixel-measured dissection of the actual
#1 entry, irvan-motion 989.306), which overrides BEDAH-R3 where they
conflict. What changed versus the first r3 build:

- Certainty chips REMOVED from every card (#1 has zero). Replaced by D1
  slug bars: a region-coloured bar on EVERY pictured card (leads 20 px,
  minis 15 px), white bold caps = PLACE/TOPIC + the card's biggest fact.
- Lead headlines back to ~18 px serif bold (pitch 19); mini headlines
  ~13 px serif bold, 2 lines, NO deck (D9 / D2).
- Lead scenes ~110 px (D7) with the dominant subject >=70% of scene
  height; the saturated fields stay (orange burst, lit dome, coloured
  strata), rescaled.
- 21 pictured cards (D2): 3 leads + 18 deck-less minis; briefs drop to
  16, total stays 37 stories (POOL22-BARU v3 only).
- Numbered badge (diameter ~17 px) on EVERY scene, bottom-right (D3);
  map pins numbered for ALL 37 stories, briefs included (D3).
- Subdeck (D4): italic serif ~19 px under the date = the 3 lead
  headlines joined with " . ".
- Briefs rebuilt to D5: coloured region number badge + bold coloured
  region caps label + ONE line + (source); pitch 13 px, font 11 px.
- Tally (D10): 16 px, labels INSIDE segments, widths tightly
  proportional, sum == 37 (cards + briefs per region).
- Scenes (D12): flat vector, one sky gradient, max 3 large elements,
  in-scene labels only >=14 px, region colours mid-tone.
- Lead captions (D11): numbered coloured captions under lead scenes.
- DATE CHECK keeps its three-part content from the first r3 build
  (LEFT OUT / NOT YET / UNCONFIRMED) — deeper than #1's, no new space.

PIL only. Canvas 1024x1024. Writes entry.png + entry-300.png beside itself.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from mapdata import WORLD  # noqa: E402  (committed data asset)

PAGE_W = 1024
CREAM = (246, 240, 221)
FACE = (255, 253, 246)
INKC = (24, 36, 58)
NAVYC = (22, 40, 63)
REDC = (193, 39, 45)
GREYC = (110, 104, 90)
SHADC = (198, 190, 168)
BACKC = (232, 225, 203)
WHITE = (255, 255, 255)

FONT_DIR = os.path.join(BASE, "fonts")
SERIF = os.path.join(FONT_DIR, "PlayfairDisplay-900.ttf")
BOLD = os.path.join(FONT_DIR, "Archivo-Bold.ttf")
MED = os.path.join(FONT_DIR, "Archivo-Medium.ttf")

canvas = Image.new("RGB", (PAGE_W, PAGE_W), CREAM)
pen = ImageDraw.Draw(canvas, "RGBA")


def F(kind, size):
    return ImageFont.truetype(kind, size)


def tw(fnt, s):
    return pen.textlength(s, font=fnt)


def wrap_to(fnt, s, limit):
    out, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(fnt, trial) <= limit:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def spaced(x, y, s, fnt, colour, gap=1):
    cx = x
    for ch in s:
        pen.text((cx, y), ch, font=fnt, fill=colour)
        cx += tw(fnt, ch) + gap
    return cx


def sheet(x, y, w, h):
    pen.rectangle([x - 4, y - 4, x + w - 4, y + h - 4], fill=BACKC)
    pen.rectangle([x + 6, y + 7, x + w + 6, y + h + 7], fill=SHADC)
    pen.rectangle([x, y, x + w, y + h], fill=FACE, outline=INKC, width=1)


def gradient(x, y, w, h, top, bottom, steps=22):
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        pen.rectangle([x, y + h * i / steps, x + w, y + h * (i + 1) / steps + 1], fill=c)


def lighten(col, f=0.45):
    return tuple(int(c + (255 - c) * f) for c in col)


def starfield(x, y, w, h, n, seed):
    rnd = random.Random(seed)
    for _ in range(n):
        sx = x + rnd.uniform(4, w - 4)
        sy = y + rnd.uniform(3, h * 0.45)
        r = rnd.choice([1, 1, 2])
        pen.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 238, 210))


def burst(cx, cy, rings):
    """Concentric saturated burst — dominant subject of a lead scene."""
    r_out = rings[0][0]
    for r, col in rings:
        pen.ellipse([cx - r, cy - r * 0.82, cx + r, cy + r * 0.82], fill=col)
    for a in range(0, 360, 24):
        x2 = cx + r_out * math.cos(math.radians(a))
        y2 = cy + r_out * 0.82 * math.sin(math.radians(a))
        pen.line([cx, cy, x2, y2], fill=rings[1][1], width=3)
    pen.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(255, 246, 214))


def badge(x_right, y_bottom, n, col, d=17):
    """D3: numbered badge, bottom-right of a scene."""
    r = d / 2
    cx, cy = x_right - r - 3, y_bottom - r - 3
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=WHITE, width=2)
    f = F(BOLD, 10 if n < 10 else 9)
    s = str(n)
    pen.text((cx - tw(f, s) / 2, cy - f.size / 2 - 1), s, font=f, fill=WHITE)


# Region scheme of this paper (mid-tone colours, D12).
REGIONS = {
    "GULF": (45, 88, 146),
    "ARABIA": (176, 110, 20),
    "ASIA": (17, 107, 88),
    "CLIMATE": (54, 143, 145),
    "OCEANIA": (181, 83, 39),
    "EUROPE": (78, 128, 45),
    "AMERICAS": (156, 46, 90),
}

# ============================================================ masthead zone
fbar = F(BOLD, 15)
fbar2 = F(BOLD, 11)
pen.text((14, 10), "THE OVERNIGHT EDITION", font=fbar, fill=NAVYC)
pen.text((14 + tw(fbar, "THE OVERNIGHT EDITION") + 10, 13),
         "· THE NIGHT DESK · EST. TONIGHT", font=fbar2, fill=GREYC)
mast_r = "37 STORIES · 7 REGIONS · EVERY ONE FROM ONE NIGHT"
pen.text((PAGE_W - 14 - tw(fbar2, mast_r), 13), mast_r, font=fbar2, fill=GREYC)
pen.line([(14, 33), (PAGE_W - 14, 33)], fill=INKC, width=2)

# The date IS the masthead: render huge, crop, scale into a 952x88 box.
DATE_TXT = "SUNDAY 22 NOVEMBER 2026"
huge = F(SERIF, 345)
layer = Image.new("RGBA", (5200, 430), (0, 0, 0, 0))
ImageDraw.Draw(layer).text((10, 0), DATE_TXT, font=huge, fill=NAVYC + (255,))
layer = layer.crop(layer.getbbox()).resize((952, 82), Image.LANCZOS)
canvas.paste(layer, (36, 37), layer)
pen = ImageDraw.Draw(canvas, "RGBA")
DATE_CAP_PX = 82

# ============================================================ D4 subdeck
# Italic serif ~19 px: the 3 lead headlines joined with " . ".
LEAD_HEADS = [
    "IRGC claims two Patriot radars hit in Bahrain",
    "Missile downed bound for the Mecca region",
    "Deep M4.1 quake under Myanmar",
]
SUBDECK = " · ".join(LEAD_HEADS)
sub_f = F(SERIF, 19)
sub_layer = Image.new("RGBA", (2400, 30), (0, 0, 0, 0))
ImageDraw.Draw(sub_layer).text((10, 0), SUBDECK, font=sub_f, fill=(70, 62, 48, 255))
sub_layer = sub_layer.crop(sub_layer.getbbox())
# fake italic: shear the layer so the top leans right
w0, h0 = sub_layer.size
sheared = sub_layer.transform((w0 + 8, h0), Image.AFFINE, (1, -0.28, 0.28 * h0, 0, 1, 0))
if sheared.size[0] > 996:
    sheared = sheared.resize((996, h0), Image.LANCZOS)
canvas.paste(sheared, ((PAGE_W - sheared.size[0]) // 2, 124), sheared)
pen = ImageDraw.Draw(canvas, "RGBA")
SUBDECK_PX = 19

# ============================================================ numbers strip
NUMBERS = [
    ("2", "PATRIOT RADARS · BAHRAIN"),
    ("05:42", "WIB · COALITION CONFIRMS"),
    ("M4.1", "MYANMAR · 95 KM DEEP"),
    ("720/9", "INDIA TEST TOTAL"),
    ("50", "LAPS · LAS VEGAS GP"),
    ("$4m", "LPGA RECORD PRIZE"),
    ("11", "NFL SUNDAY GAMES"),
]
pen.line([(14, 149), (PAGE_W - 14, 149)], fill=REDC, width=3)
fnum = F(BOLD, 34)
fcap = F(BOLD, 8)
cell = (PAGE_W - 28) / 7.0
for i, (num, cap) in enumerate(NUMBERS):
    cx = 14 + i * cell
    pen.text((cx + (cell - tw(fnum, num)) / 2, 152), num, font=fnum, fill=REDC)
    pen.text((cx + (cell - tw(fcap, cap)) / 2, 188), cap, font=fcap, fill=INKC)
    if i:
        pen.line([(cx, 154), (cx, 196)], fill=(214, 206, 184), width=1)
DIGIT_PX = 34

# ============================================================ D10 tally
# Counts per region across ALL 37 stories (pictured cards + briefs).
TALLY = [
    ("GULF", 5), ("ARABIA", 2), ("ASIA", 5), ("CLIMATE", 4),
    ("OCEANIA", 5), ("EUROPE", 4), ("AMERICAS", 12),
]
TALLY_TOTAL = sum(n for _n, n in TALLY)
TALLY_Y, TALLY_H = 199, 16
tx = 14.0
ftally = F(BOLD, 9)
for name, n in TALLY:
    segw = (PAGE_W - 28) * n / TALLY_TOTAL
    pen.rectangle([tx, TALLY_Y, tx + segw, TALLY_Y + TALLY_H], fill=REGIONS[name])
    label = f"{name} {n}"
    pen.text((tx + (segw - tw(ftally, label)) / 2, TALLY_Y + 3), label,
             font=ftally, fill=WHITE)
    tx += segw

# ============================================================ lead scenes
# D7/D12: ~110 px, flat vector, one gradient, max 3 large elements,
# dominant subject >=70% of scene height. No in-scene text labels.

def lead_gulf(x, y, w, h):
    gradient(x, y, w, h, (14, 30, 62), (30, 74, 110))
    starfield(x, y, w, h, 14, 4)
    sea_y = y + h - 26
    pen.rectangle([x, sea_y, x + w, y + h], fill=(10, 130, 150))
    # element 1: GIANT orange burst, ~79 px tall = 72% of scene
    burst(x + 222, y + 50, [(48, (216, 62, 10)), (37, (240, 110, 20)),
                            (26, (248, 158, 32)), (15, (252, 200, 70))])
    # element 2: burning plant silhouette under the burst
    px = x + 176
    pen.rectangle([px, sea_y - 14, px + 88, sea_y], fill=(8, 12, 20))
    pen.rectangle([px + 10, sea_y - 23, px + 17, sea_y - 14], fill=(8, 12, 20))
    # element 3: big radar dish, left foreground (74 px across, ~66 tall)
    rx, ry = x + 52, sea_y - 2
    pen.line([rx, ry, rx - 12, sea_y + 12], fill=(225, 228, 210), width=4)
    pen.line([rx, ry, rx + 14, sea_y + 12], fill=(225, 228, 210), width=4)
    pen.arc([rx - 37, ry - 52, rx + 37, ry + 22], start=300, end=130,
            fill=(235, 238, 220), width=5)
    pen.line([rx, ry - 14, rx + 28, ry - 36], fill=(235, 238, 220), width=3)
    pen.ellipse([rx + 25, ry - 39, rx + 32, ry - 32], fill=(255, 214, 120))


def lead_mecca(x, y, w, h):
    gradient(x, y, w, h, (12, 24, 52), (36, 58, 98))
    starfield(x, y, w, h, 12, 9)
    ground = y + h - 14
    pen.rectangle([x, ground, x + w, y + h], fill=(10, 16, 28))
    # element 1: GIANT golden burst, ~75 px tall = 68-72% of scene
    burst(x + 200, y + 42, [(46, (198, 128, 16)), (35, (232, 168, 30)),
                            (24, (250, 205, 80)), (13, (255, 232, 150))])
    # missile trail into the burst (part of the burst element)
    pts = [(x + 16 + i * 10, y + 80 - i * 4.4) for i in range(11)]
    for i in range(0, len(pts) - 1, 2):
        pen.line([pts[i], pts[i + 1]], fill=(240, 130, 90), width=3)
    # element 2: BIG lit dome, ~80 px tall = 73% of scene
    bx = x + 42
    pen.rectangle([bx, ground - 24, bx + 118, ground], fill=(146, 96, 26))
    pen.pieslice([bx + 8, ground - 80, bx + 110, ground - 20], 180, 360, fill=(226, 156, 44))
    pen.pieslice([bx + 22, ground - 72, bx + 96, ground - 24], 180, 360, fill=(248, 196, 84))
    pen.rectangle([bx + 55, ground - 90, bx + 63, ground - 76], fill=(226, 156, 44))
    pen.ellipse([bx + 54, ground - 97, bx + 64, ground - 87], fill=(255, 240, 190))
    for wx_ in range(4):
        pen.rectangle([bx + 14 + wx_ * 26, ground - 17, bx + 22 + wx_ * 26, ground - 7],
                      fill=(255, 226, 140))
    # element 3: tall minaret, right
    mx_ = x + 282
    pen.rectangle([mx_, ground - 72, mx_ + 11, ground], fill=(16, 24, 40))
    pen.polygon([(mx_ - 4, ground - 72), (mx_ + 15, ground - 72), (mx_ + 5, ground - 88)],
                fill=(16, 24, 40))
    pen.rectangle([mx_ - 5, ground - 55, mx_ + 16, ground - 50], fill=(255, 226, 140))


def lead_quake(x, y, w, h):
    # element 1: dusk sky band + surface town
    gradient(x, y, w, 20, (240, 130, 40), (250, 180, 70))
    pen.rectangle([x, y + 20, x + w, y + 27], fill=(52, 130, 60))
    for bx, bw, bh in [(x + 26, 30, 13), (x + 64, 20, 9), (x + 226, 34, 14), (x + 268, 22, 10)]:
        pen.rectangle([bx, y + 20 - bh, bx + bw, y + 20], fill=(20, 30, 44))
        pen.rectangle([bx + 4, y + 20 - bh + 3, bx + 9, y + 20 - bh + 7], fill=(255, 232, 150))
    # element 2: COLOURED STRATA filling the underground (90 px = 82%)
    strata = [(206, 106, 30), (168, 52, 138), (22, 138, 164), (86, 164, 56), (186, 52, 48)]
    sy = y + 27
    for i, c in enumerate(strata):
        pen.rectangle([x, sy + i * 17, x + w, sy + (i + 1) * 17], fill=c)
    # element 3: epicentre rings + hypocentre star + depth line
    cx = x + 138
    for r in (8, 16, 25):
        pen.ellipse([cx - r, y + 23 - r // 2, cx + r, y + 23 + r // 2],
                    outline=(255, 246, 200), width=2)
    hx, hy = cx, y + h - 13
    for a in range(0, 360, 45):
        pen.line([hx, hy, hx + 11 * math.cos(math.radians(a)), hy + 11 * math.sin(math.radians(a))],
                 fill=(255, 240, 170), width=3)
    pen.line([cx, y + 27, hx, hy - 9], fill=(255, 246, 200), width=2)
    gx = x + w - 36
    pen.rectangle([gx, y + 29, gx + 9, y + h - 5], fill=(240, 236, 214), outline=INKC, width=1)
    pen.rectangle([gx, y + h - 20, gx + 9, y + h - 5], fill=REDC)


LEADS = [
    dict(n=1, reg="GULF", scene=lead_gulf,
         slug="BAHRAIN: 2 PATRIOT RADARS CLAIMED",
         caption="1 · BAHRAIN · GULF",
         head=LEAD_HEADS[0],
         deck="Tehran says it hit 2 Patriot sites (Al-Riffa, Awali); a Bahrain "
              "plant burned and a drone fell over Kuwait.",
         source="IRGC · Bahrain ministry", facts=4,
         subject_pct=72),
    dict(n=2, reg="ARABIA", scene=lead_mecca,
         slug="MECCA REGION: MISSILE INTERCEPTED",
         caption="2 · MECCA REGION · ARABIA",
         head=LEAD_HEADS[1],
         deck="Sirens sounded at 03:43 WIB; at 05:42 WIB the coalition "
              "confirmed the Houthi missile was intercepted.",
         source="Anadolu · coalition", facts=3,
         subject_pct=73),
    dict(n=3, reg="ASIA", scene=lead_quake,
         slug="MYANMAR: M4.1 AT 95 KM DEEP",
         caption="3 · MYANMAR · ASIA",
         head=LEAD_HEADS[2],
         deck="NCS logged it at 04:05 WIB — 24.404N, 94.616E, 95 km down: "
              "deep enough to pass almost unfelt.",
         source="NCS India · ANI", facts=4,
         subject_pct=82),
]

LEAD_Y, LEAD_SLUG_H, LEAD_SCENE_H, LEAD_W, LEAD_CARD_H = 219, 20, 110, 324, 220
fslug_lead = F(BOLD, 12)
for L, lx in zip(LEADS, [14, 350, 686]):
    col = REGIONS[L["reg"]]
    sheet(lx, LEAD_Y, LEAD_W, LEAD_CARD_H)
    # D1 slug bar (20 px), region colour, white bold caps
    pen.rectangle([lx + 1, LEAD_Y + 1, lx + LEAD_W - 1, LEAD_Y + 1 + LEAD_SLUG_H], fill=col)
    pen.text((lx + 9, LEAD_Y + 5), L["slug"], font=fslug_lead, fill=WHITE)
    sy = LEAD_Y + 1 + LEAD_SLUG_H
    L["scene"](lx + 1, sy, LEAD_W - 2, LEAD_SCENE_H)
    badge(lx + LEAD_W - 1, sy + LEAD_SCENE_H, L["n"], col)
    # D11 numbered coloured caption under the scene; source right-aligned
    # on the same line (plain source tag, no chip).
    cap_y = sy + LEAD_SCENE_H + 4
    pen.text((lx + 10, cap_y), L["caption"], font=F(BOLD, 10), fill=col)
    fs = F(MED, 9)
    pen.text((lx + LEAD_W - 10 - tw(fs, L["source"]), cap_y + 1), L["source"],
             font=fs, fill=GREYC)
    fh = F(SERIF, 18)
    hy = sy + LEAD_SCENE_H + 17
    for line in wrap_to(fh, L["head"], LEAD_W - 20)[:2]:
        pen.text((lx + 10, hy), line, font=fh, fill=INKC)
        hy += 19
    fd = F(MED, 11)
    for line in wrap_to(fd, L["deck"], LEAD_W - 20)[:2]:
        pen.text((lx + 10, hy + 2), line, font=fd, fill=(52, 48, 40))
        hy += 13

# ============================================================ mini scenes
# D2/D12: full-bleed coloured field edge-to-edge, ±45 px, flat vector,
# max 3 large elements, in-scene labels only >=14 px.

def sc_screen(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.25), col)
    pen.rectangle([x + 8, y + 5, x + 92, y + h - 5], fill=(8, 40, 52))
    pen.rectangle([x + 12, y + 9, x + 88, y + h - 9], fill=(120, 235, 245))
    pen.rectangle([x + 18, y + 15, x + 58, y + 20], fill=(8, 90, 110))
    pen.rectangle([x + 18, y + 25, x + 74, y + 30], fill=(8, 90, 110))
    cx, cy, r = x + 128, y + h // 2, 17
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVYC, width=2)
    pen.line([cx, cy, cx, cy - 11], fill=INKC, width=2)
    pen.line([cx, cy, cx + 8, cy + 4], fill=REDC, width=2)


def sc_score(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    pen.rectangle([x + 8, y + 7, x + 118, y + 17], fill=(255, 240, 200))
    pen.rectangle([x + 8, y + 27, x + 66, y + 37], fill=(60, 60, 60))
    pen.text((x + 122, y + 4), "720", font=F(BOLD, 15), fill=WHITE)


def sc_circuit(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.25), col)
    pts = [(x + 12 + i * 13, y + h // 2 + int(13 * math.sin(i * 1.55))) for i in range(8)]
    pen.line(pts, fill=(255, 240, 170), width=4)
    pen.text((x + 116, y + 4), "50", font=F(BOLD, 16), fill=WHITE)


def sc_rocket(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.15), col)
    starfield(x, y, w, h, 7, 31)
    rx = x + 36
    pen.polygon([(rx, y + 2), (rx + 8, y + 11), (rx + 8, y + 29), (rx - 8, y + 29),
                 (rx - 8, y + 11)], fill=(240, 240, 234))
    pen.polygon([(rx - 8, y + 29), (rx - 15, y + 37), (rx - 8, y + 37)], fill=REDC)
    pen.polygon([(rx + 8, y + 29), (rx + 15, y + 37), (rx + 8, y + 37)], fill=REDC)
    pen.polygon([(rx - 4, y + 37), (rx + 4, y + 37), (rx, y + 45)], fill=(250, 170, 60))
    pen.text((x + 62, y + 27), "GO", font=F(BOLD, 15), fill=WHITE)


def sc_pitch(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    pen.rectangle([x + 7, y + 4, x + 104, y + h - 4], outline=WHITE, width=2)
    pen.line([x + 55, y + 4, x + 55, y + h - 4], fill=WHITE, width=2)
    pen.ellipse([x + 43, y + h // 2 - 12, x + 67, y + h // 2 + 12], outline=WHITE, width=2)


def sc_court(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    pen.rectangle([x + 7, y + 4, x + 100, y + h - 4], outline=WHITE, width=2)
    pen.line([x + 53, y + 4, x + 53, y + h - 4], fill=WHITE, width=2)
    pen.line([x + 7, y + h // 2, x + 100, y + h // 2], fill=WHITE, width=2)
    pen.ellipse([x + 112, y + 24, x + 130, y + 42], fill=(215, 235, 90), outline=INKC, width=1)


def sc_board(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    pen.text((x + 8, y + 4), "KIM -18", font=F(BOLD, 14), fill=WHITE)
    pen.rectangle([x + 8, y + 26, x + 96, y + 34], fill=(255, 240, 190))
    pen.rectangle([x + 8, y + 38, x + 88, y + 44], fill=(255, 240, 190))
    pen.text((x + 104, y + 25), "-17", font=F(BOLD, 14), fill=WHITE)


def sc_ring(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    cx, cy = x + 48, y + h // 2
    pen.ellipse([cx - 34, cy - 19, cx + 34, cy + 19], fill=(238, 220, 178),
                outline=(120, 88, 40), width=3)
    pen.line([cx - 14, cy, cx + 14, cy], fill=(120, 88, 40), width=3)
    pen.text((x + 92, y + 26), "12-2", font=F(BOLD, 14), fill=WHITE)


def sc_rain(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.25), col)
    for i in range(9):
        rx = x + 10 + i * 11
        pen.line([rx, y + 5, rx - 4, y + 18], fill=(210, 235, 255), width=3)
        pen.line([rx, y + 26, rx - 4, y + 39], fill=(210, 235, 255), width=3)
    pen.text((x + 112, y + 26), "-9", font=F(BOLD, 15), fill=WHITE)


def sc_dots(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    for r in range(2):
        for c in range(6):
            if r * 6 + c < 11:
                cx, cy = x + 18 + c * 15, y + 12 + r * 21
                pen.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(250, 236, 170))
    pen.text((x + 116, y + 26), "11", font=F(BOLD, 15), fill=WHITE)


def sc_flames(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.15), col)
    pen.rectangle([x + 14, y + 28, x + 120, y + h], fill=(10, 16, 26))
    pen.rectangle([x + 26, y + 18, x + 34, y + 28], fill=(10, 16, 26))
    for fx, fh_ in [(30, 20), (58, 27), (88, 18)]:
        pen.polygon([(x + fx - 9, y + 30), (x + fx, y + 30 - fh_), (x + fx + 9, y + 30)],
                    fill=(245, 130, 30))
        pen.polygon([(x + fx - 4, y + 30), (x + fx, y + 30 - fh_ + 8), (x + fx + 4, y + 30)],
                    fill=(252, 200, 70))


def sc_un(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.25), col)
    pen.rectangle([x + 30, y + 12, x + 130, y + h], fill=(235, 232, 220))
    pen.rectangle([x + 22, y + 6, x + 138, y + 12], fill=(200, 196, 182))
    for i in range(5):
        pen.rectangle([x + 40 + i * 18, y + 18, x + 48 + i * 18, y + h - 4], fill=col)


def sc_drone(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    cx, cy = x + 62, y + h // 2
    pen.line([cx - 26, cy - 12, cx + 26, cy + 12], fill=WHITE, width=4)
    pen.line([cx - 26, cy + 12, cx + 26, cy - 12], fill=WHITE, width=4)
    for dx, dy in [(-26, -12), (26, 12), (-26, 12), (26, -12)]:
        pen.ellipse([cx + dx - 8, cy + dy - 5, cx + dx + 8, cy + dy + 5], outline=WHITE, width=3)
    pen.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=REDC)


def sc_tanker(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.25), col)
    pen.rectangle([x, y + h - 12, x + w, y + h], fill=(12, 90, 130))
    pen.polygon([(x + 18, y + 26), (x + 128, y + 26), (x + 118, y + 36), (x + 28, y + 36)],
                fill=(30, 34, 44))
    pen.rectangle([x + 34, y + 18, x + 104, y + 26], fill=(196, 60, 40))
    pen.rectangle([x + 112, y + 10, x + 122, y + 26], fill=(30, 34, 44))


def sc_sirens(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.1), col)
    pen.ellipse([x + 14, y + 6, x + 44, y + 36], fill=(250, 240, 200))
    pen.ellipse([x + 24, y + 4, x + 52, y + 34], fill=lighten(col, 0.1))
    for r in (14, 22, 30):
        pen.arc([x + 108 - r, y + h // 2 - r, x + 108 + r, y + h // 2 + r],
                start=300, end=60, fill=(255, 220, 120), width=4)


def sc_clock(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    cx, cy, r = x + 40, y + h // 2, 19
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVYC, width=2)
    pen.line([cx, cy, cx, cy - 13], fill=INKC, width=3)
    pen.line([cx, cy, cx + 10, cy + 6], fill=REDC, width=3)
    pen.text((x + 70, y + 25), "02:35", font=F(BOLD, 14), fill=WHITE)


def sc_target(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    pen.rectangle([x + 12, y + 30, x + 60, y + 38], fill=(255, 240, 190))
    pen.rectangle([x + 12, y + 16, x + 88, y + 24], fill=(255, 240, 190))
    pen.text((x + 96, y + 4), "$120bn", font=F(BOLD, 14), fill=WHITE)


def sc_bars(x, y, w, h, col):
    gradient(x, y, w, h, lighten(col, 0.2), col)
    for i, (lab, bw) in enumerate([("98", 96), ("85", 82), ("80", 76)]):
        yy = y + 5 + i * 14
        pen.rectangle([x + 8, yy, x + 8 + bw, yy + 9], fill=(255, 240, 190))
        pen.text((x + 12 + bw, yy - 2), lab, font=F(BOLD, 14), fill=WHITE)


MINIS = [
    dict(n=4, reg="CLIMATE", dev=sc_screen, slug="ANTALYA · 06:00 PLENARY",
         head="COP31 text tabled; plenary 06:00 GMT",
         source="CLIMATE · Reuters", facts=3),
    dict(n=5, reg="OCEANIA", dev=sc_score, slug="WELLINGTON: 720/9 RECORD",
         head="India declare 720/9; Rahul 136, Pant 128",
         source="OCEANIA · IANS · AFP", facts=4),
    dict(n=6, reg="AMERICAS", dev=sc_circuit, slug="LAS VEGAS: 50 LAPS",
         head="Vegas GP lights out 11:00 WIB, round 22",
         source="AMERICAS · F1", facts=3),
    dict(n=7, reg="AMERICAS", dev=sc_rocket, slug="VANDENBERG: GO 12:16",
         head="Falcon 9 NROL-136 GO; B1097 to LZ4",
         source="AMERICAS · VSFB", facts=3),
    dict(n=8, reg="EUROPE", dev=sc_pitch, slug="ANFIELD: 16:30 UTC",
         head="Liverpool host Man United, week 11",
         source="EUROPE · Premier League", facts=2),
    dict(n=9, reg="EUROPE", dev=sc_court, slug="TURIN: FINAL TONIGHT",
         head="Alcaraz v Zverev final ~16:00 UTC",
         source="EUROPE · Reuters", facts=2),
    dict(n=10, reg="AMERICAS", dev=sc_board, slug="FLORIDA: $4M PRIZE",
         head="Kim -18 leads CME; Thitikul -17",
         source="AMERICAS · LPGA · AP", facts=3),
    dict(n=11, reg="ASIA", dev=sc_ring, slug="FUKUOKA: 12-2 LEADERS",
         head="Final day: Onosato, Wakamotoharu 12-2",
         source="ASIA · JSA", facts=3),
    dict(n=12, reg="AMERICAS", dev=sc_rain, slug="RSM: THREE TIED -9",
         head="Rain pushes RSM finish to Monday",
         source="AMERICAS · Reuters", facts=2),
    dict(n=13, reg="AMERICAS", dev=sc_dots, slug="NFL: 11 SUNDAY GAMES",
         head="Week 12: 11 games, Vikings @ 49ers late",
         source="AMERICAS · ESPN · NFL", facts=3),
    dict(n=14, reg="GULF", dev=sc_flames, slug="BAHRAIN: FIRES 23:25",
         head="Fires reported 23:25 local, ministry says",
         source="GULF · Bahrain ministry", facts=2),
    dict(n=15, reg="GULF", dev=sc_un, slug="BAHRAIN: UN 2817",
         head="Bahrain asks UN to enforce Res. 2817",
         source="GULF · UN Council", facts=2),
    dict(n=16, reg="GULF", dev=sc_drone, slug="KUWAIT: DRONE DOWN",
         head="Drone at Ali Al Salem, first since Sept",
         source="GULF · Kuwait reports", facts=2),
    dict(n=17, reg="GULF", dev=sc_tanker, slug="HORMUZ: TANKER HIT",
         head="Tanker hit Sat 11:27 UTC, UKMTO says",
         source="GULF · UKMTO", facts=2),
    dict(n=18, reg="ARABIA", dev=sc_sirens, slug="MECCA: SIRENS 23:43",
         head="Sirens 23:43 Riyadh time, Saturday",
         source="ARABIA · Riyadh reports", facts=2),
    dict(n=19, reg="ASIA", dev=sc_clock, slug="MYANMAR: 02:35 IST",
         head="NCS clocks M4.1 shock at 02:35:57 IST",
         source="ASIA · NCS India", facts=2),
    dict(n=20, reg="CLIMATE", dev=sc_target, slug="COP31: $120BN FELL",
         head="$120bn target fell in Antalya talks Thu",
         source="CLIMATE · COP31 talks", facts=2),
    dict(n=21, reg="OCEANIA", dev=sc_bars, slug="WELLINGTON: GILL 98",
         head="Gill 98, Jaiswal 85, Padikkal 80",
         source="OCEANIA · Scorecard", facts=3),
]

pen.text((14, 445), "MORE FROM THE NIGHT · STORIES 4–21", font=F(BOLD, 11), fill=REDC)
MINI_W, MINI_H, MINI_SLUG_H, MINI_SCENE_H = 159, 103, 15, 45
MINI_Y, MINI_PITCH = 457, 103
fslug_mini = F(BOLD, 10)
for idx, M in enumerate(MINIS):
    mx = 14 + (idx % 6) * 167
    my = MINI_Y + (idx // 6) * MINI_PITCH
    col = REGIONS[M["reg"]]
    sheet(mx, my, MINI_W, MINI_H)
    pen.rectangle([mx + 1, my + 1, mx + MINI_W - 1, my + 1 + MINI_SLUG_H], fill=col)
    pen.text((mx + 6, my + 4), M["slug"], font=fslug_mini, fill=WHITE)
    sy = my + 1 + MINI_SLUG_H
    M["dev"](mx + 1, sy, MINI_W - 2, MINI_SCENE_H, col)
    badge(mx + MINI_W - 1, sy + MINI_SCENE_H, M["n"], col)
    fh = F(SERIF, 13)
    hy = sy + MINI_SCENE_H + 1
    for line in wrap_to(fh, M["head"], MINI_W - 14)[:2]:
        pen.text((mx + 7, hy), line, font=fh, fill=INKC)
        hy += 12
    pen.text((mx + 7, my + MINI_H - 10), M["source"], font=F(MED, 9), fill=GREYC)

# ============================================================ bottom zone
BOT_HDR_Y = 772
ftitle = F(BOLD, 11)
pen.text((14, BOT_HDR_Y), "WHERE IT HAPPENED · ALL 37 STORIES, PINNED BY NUMBER",
         font=ftitle, fill=NAVYC)
pen.text((530, BOT_HDR_Y), "ALSO ON THE NIGHT · STORIES 22–37", font=ftitle, fill=NAVYC)

BRIEF_REGIONS = {
    22: "ASIA", 23: "ASIA", 24: "CLIMATE", 25: "CLIMATE", 26: "OCEANIA",
    27: "OCEANIA", 28: "OCEANIA", 29: "EUROPE", 30: "EUROPE",
    31: "AMERICAS", 32: "AMERICAS", 33: "AMERICAS", 34: "AMERICAS",
    35: "AMERICAS", 36: "AMERICAS", 37: "AMERICAS",
}

MAP_BOX = (14, 786, 500, 198)
mx0, my0, mw, mh = MAP_BOX
pen.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(205, 225, 235), outline=INKC, width=1)


def project(lon, lat):
    return (mx0 + (lon + 180) / 360 * mw, my0 + (76 - lat) / 132 * mh)


for _name, rings in WORLD.items():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            lo, la = pair.split(":")
            pts.append(project(float(lo), float(la)))
        if len(pts) > 2:
            pen.polygon(pts, fill=(222, 205, 180))

PIN_LATLON = {
    1: (50.5, 26.2), 2: (39.8, 21.4), 3: (94.6, 24.4), 4: (30.7, 36.9),
    5: (174.8, -41.3), 6: (-115.1, 36.1), 7: (-120.6, 34.7), 8: (-2.96, 53.4),
    9: (7.7, 45.1), 10: (-81.8, 26.1), 11: (130.4, 33.6), 12: (-81.4, 31.1),
    13: (-122.4, 37.8), 14: (51.4, 26.7), 15: (49.7, 25.7), 16: (47.4, 29.3),
    17: (56.3, 26.6), 18: (40.4, 20.9), 19: (95.4, 23.8), 20: (31.5, 37.4),
    21: (175.6, -40.7), 22: (131.2, 33.1), 23: (129.6, 34.1), 24: (29.9, 36.4),
    25: (149.1, -35.3), 26: (174.1, -42.0), 27: (176.3, -41.0), 28: (173.4, -40.2),
    29: (-0.33, 53.74), 30: (8.5, 44.6), 31: (-114.3, 35.6), 32: (-121.4, 35.2),
    33: (-77.4, 38.9), 34: (-82.6, 25.6), 35: (-80.6, 31.6), 36: (-82.2, 30.6),
    37: (-81.9, 32.1),
}
fpin = F(BOLD, 8)
for n in range(1, 38):
    lo, la = PIN_LATLON[n]
    px, py = project(lo, la)
    reg = None
    for card in LEADS + MINIS:
        if card["n"] == n:
            reg = card["reg"]
    if reg is None:
        reg = BRIEF_REGIONS[n]
    col = REGIONS[reg]
    pen.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=WHITE, width=1)
    s = str(n)
    pen.text((px - tw(fpin, s) / 2, py - 4), s, font=fpin, fill=WHITE)

# D5 briefs: 16 left after 8 briefs were converted to minis (14–21).
# (region, one-line text, source) — text never wraps.
BRIEF_DATA = [
    (22, "ASIA", "Wakamotoharu v Atamifuji helps decide yusho", "JSA"),
    (23, "ASIA", "Atamifuji 11-3 still chases the Kyushu cup", "JSA"),
    (24, "CLIMATE", "COP31 objections were closed at 03:00 GMT", "Reuters"),
    (25, "CLIMATE", "Chris Bowen co-hosts COP31 for Australia", "COP31 hosts"),
    (26, "OCEANIA", "Nicholls 175 anchors New Zealand's 368", "AFP"),
    (27, "OCEANIA", "Bumrah takes 4-92 in New Zealand's innings", "AFP"),
    (28, "OCEANIA", "India's 720/9 came in 166 overs at Wellington", "IANS"),
    (29, "EUROPE", "Hull v Brighton kicks off 14:00 UTC", "PL"),
    (30, "EUROPE", "Alcaraz fought back past Shelton in semi", "Reuters"),
    (31, "AMERICAS", "Las Vegas is round 22 of the F1 season", "F1"),
    (32, "AMERICAS", "Booster B1097 returns to Landing Zone 4", "VSFB"),
    (33, "AMERICAS", "NROL-136 built with Northrop Grumman", "VSFB"),
    (34, "AMERICAS", "Thitikul & Yoshida one back at -17", "LPGA"),
    (35, "AMERICAS", "Penge shares the RSM lead at -9", "Reuters"),
    (36, "AMERICAS", "Neergaard-Petersen shares RSM lead -9", "Reuters"),
    (37, "AMERICAS", "RSM Classic final round moves to Monday", "Reuters"),
]
fbrief = F(MED, 11)
fbrief_reg = F(BOLD, 11)
for i, (n, reg, text, src) in enumerate(BRIEF_DATA):
    col = REGIONS[reg]
    yy = 786 + i * 13
    bx = 530
    # coloured region number badge
    pen.ellipse([bx, yy + 1, bx + 11, yy + 12], fill=col)
    fn = F(BOLD, 7 if n >= 10 else 8)
    s = str(n)
    pen.text((bx + 5.5 - tw(fn, s) / 2, yy + 3), s, font=fn, fill=WHITE)
    x = bx + 15
    pen.text((x, yy), reg, font=fbrief_reg, fill=col)
    x += tw(fbrief_reg, reg) + 5
    pen.text((x, yy), text, font=fbrief, fill=INKC)
    x += tw(fbrief, text) + 5
    pen.text((x, yy), f"({src})", font=fbrief, fill=GREYC)

TOTAL_STORIES = len(LEADS) + len(MINIS) + len(BRIEF_DATA)
assert TOTAL_STORIES == 37, TOTAL_STORIES
assert TOTAL_STORIES == TALLY_TOTAL, (TOTAL_STORIES, TALLY_TOTAL)
assert len(PIN_LATLON) == TOTAL_STORIES

# ============================================================ DATE CHECK
# Three-part content kept from the first r3 build (no new space).
DC_Y = 994
pen.rectangle([14, DC_Y, PAGE_W - 14, DC_Y + 29], outline=REDC, width=2)
pen.text((22, DC_Y + 4), "DATE CHECK", font=F(BOLD, 10), fill=REDC)
fdc = F(MED, 9)
dc_lines = [
    "LEFT OUT (not 22 Nov): Lviv strikes (20 Nov) · Peru M6.9 quake (20/21 Nov) · 400-drone barrage (19-20 Nov) · "
    "ICJ ruling (19 Nov) · Berlin Coalition talks (19 Nov) · Geneva killer-robot deal (21 Nov).",
    "NOT YET (same day, unfinished): COP31 final adoption · Liverpool v Man Utd result · ATP Turin final result. "
    "UNCONFIRMED / CONTESTED: IRGC claim of 2 Patriot radars destroyed · Houthi interception claim.",
    "HOW WE CHECKED: CONFIRMED = 2+ major outlets · OFFICIAL = on the record · REPORTED = 1 major outlet · "
    "CLAIM = one-sided claim. Every story above happened, or was first reported, on Sunday 22 November 2026.",
]
for i, line in enumerate(dc_lines):
    pen.text((112, DC_Y + 1 + i * 9), line, font=fdc, fill=INKC)

# ============================================================ save
tmp = os.path.join(BASE, "_full.png")
canvas.save(tmp)
chosen = None
for colours in (256, 224, 192, 160):
    q = canvas.quantize(colors=colours, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
    q.save(os.path.join(BASE, "entry.png"), optimize=True)
    chosen = os.path.getsize(os.path.join(BASE, "entry.png"))
    print(f"palette={colours} entry bytes={chosen}")
    if chosen <= 170_000:
        break
canvas.resize((300, 300), Image.LANCZOS).save(os.path.join(BASE, "entry-300.png"))
os.remove(tmp)
print("entry bytes:", chosen, "| date cap px:", DATE_CAP_PX, "| digit px:", DIGIT_PX)
print("subdeck px:", SUBDECK_PX, "| lead scene px:", LEAD_SCENE_H, "| mini scene px:", MINI_SCENE_H)
print("pictured:", len(LEADS) + len(MINIS), "= 3 leads +", len(MINIS), "minis")
print("stories:", TOTAL_STORIES, "=", len(LEADS) + len(MINIS), "cards +", len(BRIEF_DATA),
      "briefs | tally sum:", TALLY_TOTAL)
print("badges:", len(LEADS) + len(MINIS), "/", len(LEADS) + len(MINIS),
      "| pins:", len(PIN_LATLON), "/", TOTAL_STORIES)
print("avg facts/card:", sum(c["facts"] for c in LEADS + MINIS) / (len(LEADS) + len(MINIS)))
