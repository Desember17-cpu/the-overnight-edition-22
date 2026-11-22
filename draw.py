#!/usr/bin/env python3
"""THE OVERNIGHT EDITION — one-page dark newspaper summing up
Sunday 22 November 2026: 40 stories, 13 pictured cards, a locator map,
27 briefs, a numbers strip and a date check.

Winner of the per-account duel test: Varian A (3D layered broadsheet).
It beat Varian B (2D flat — same facts, flatter hierarchy) and Varian C
(3D hero — the full-width hero strip wasted a band on empty space).
Draws entry.png (1024x1024) next to this file using only Pillow
primitives: flat vector-style shapes, no external images. Deterministic:
no randomness, no clocks, no network. All facts come from POOL22-BARU v3
(13 verified 22 Nov 2026 events); COP31 is in ANTALYA, Turkiye.
A source is named beside every story.
"""
import os
from PIL import Image, ImageDraw, ImageFont
from mapdata import WORLD

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16
CW = W - 2 * MX
BG = (14, 26, 43)
PANEL = (22, 40, 63)
PANEL_DK = (11, 21, 36)
CREAM = (242, 234, 216)
MUTED = (185, 196, 212)
GOLD = (232, 179, 60)
ALERT = (217, 95, 75)
HOOK = (146, 22, 40)
LINE = (58, 82, 112)
LAND = (201, 168, 106)
REGIONS = {
    "MIDEAST": (125, 60, 152), "EUROPE": (176, 58, 46), "ASIA": (29, 111, 184),
    "OCEANIA": (20, 143, 119), "AMERICAS": (202, 111, 30), "GLOBAL": (93, 109, 126),
}
_cache = {}
def F(name, size):
    k = (name, int(size))
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))
    return _cache[k]
PF, AB, AM = "PlayfairDisplay-900.ttf", "Archivo-Bold.ttf", "Archivo-Medium.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def fit(text, name, size, max_w, floor=8):
    s = size
    while s > floor and d.textlength(text, font=F(name, s)) > max_w:
        s -= 1
    return F(name, s)

def panel(x, y, w, h, fill=PANEL, outline=None):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline)

def shadow_panel(x, y, w, h, depth=6):
    d.rectangle([x + depth, y + depth, x + w - 1 + depth, y + h - 1 + depth], fill=(7, 13, 24))
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL, outline=LINE)

# --- 13 cards, every deck >=2 verified facts from POOL22-BARU v3 ---
CARDS = [
 dict(n=1, region="MIDEAST", topic="THE GULF", src="IRGC · BAHRAIN",
      head="GULF OVERNIGHT: 2 US RADARS HIT, IRGC CLAIMS",
      deck="IRGC statements at 02:40 & 03:37 WIB claim 2 Patriot radars hit in Bahrain; a civil site burned and a drone was downed in Kuwait.",
      scene="radar", chip="2 RADARS CLAIMED", cap="BAHRAIN · KUWAIT · THE GULF", pin=(50.6, 26.2)),
 dict(n=2, region="MIDEAST", topic="MAKKAH SKIES", src="ANADOLU",
      head="HOUTHI MISSILE FOR MAKKAH INTERCEPTED",
      deck="Civil-defence sirens sounded 03:43 WIB; the Saudi-led coalition confirmed the intercept at 05:42 WIB on Sunday.",
      scene="intercept", chip="05:42 WIB CONFIRMED", cap="MAKKAH REGION · SAUDI ARABIA", pin=(39.8, 21.4)),
 dict(n=3, region="EUROPE", topic="COP31", src="REUTERS",
      head="COP31 FINAL TEXT TABLED IN ANTALYA",
      deck="Objections closed at 03:00 GMT; the approval plenary is set for 06:00 GMT (13:00 WIB) in Antalya, Turkiye.",
      scene="summit", chip="06:00 GMT PLENARY", cap="ANTALYA · TURKIYE", pin=(30.7, 36.9)),
 dict(n=4, region="ASIA", topic="QUAKE", src="NCS · ANI",
      head="MYANMAR SHAKEN BY M4.1 QUAKE",
      deck="Recorded 04:05 WIB at 24.404N 94.616E; the epicentre was 95 km deep, the National Center for Seismology said.",
      scene="quake", chip="M4.1 · 95 KM DEEP", cap="MYANMAR · 24.404N 94.616E", pin=(94.6, 24.4)),
 dict(n=5, region="OCEANIA", topic="CRICKET", src="IANS · AFP",
      head="INDIA DECLARE ON 720/9, A RECORD",
      deck="Rahul 136 and Pant 128 powered 720/9; New Zealand made 368, leaving India 352 ahead on day four in Wellington.",
      scene="cricket", chip="720/9 · LEAD 352", cap="WELLINGTON · DAY 4", pin=(174.8, -41.3)),
 dict(n=6, region="AMERICAS", topic="FORMULA 1", src="FORMULA1.COM",
      head="LAS VEGAS GP RACES INTO THE NIGHT",
      deck="Lights out 11:00 WIB for 50 laps of the Strip Circuit — round 22 of the season, under the lights.",
      scene="race", chip="50 LAPS · 11:00 WIB", cap="LAS VEGAS · STRIP CIRCUIT", pin=(-115.2, 36.1)),
 dict(n=7, region="AMERICAS", topic="SPACE", src="VSFB · SPACEX",
      head="FALCON 9 LIFTS NROL-136 SATELLITES",
      deck="Launch window 19:16–19:46 WIB; booster B1097 flies the 15th NRO batch to Landing Zone 4.",
      scene="rocket", chip="19:16 WIB · B1097", cap="VANDENBERG · SLC-4E", pin=(-120.6, 34.7)),
 dict(n=8, region="EUROPE", topic="FOOTBALL", src="PREMIER LEAGUE",
      head="LIVERPOOL HOST MANCHESTER UNITED",
      deck="Kick-off 23:30 WIB in Matchweek 11; Hull host Brighton earlier at 21:00 WIB on Sunday.",
      scene="football", chip="23:30 WIB · MW11", cap="ANFIELD · LIVERPOOL", pin=(-2.96, 53.43)),
 dict(n=9, region="EUROPE", topic="TENNIS", src="ATP · REUTERS",
      head="ALCARAZ MEETS ZVEREV IN TURIN FINAL",
      deck="The final is played at 23:00 WIB in Turin; Alcaraz reached it after fighting back past Shelton.",
      scene="tennis", chip="23:00 WIB · TURIN", cap="TURIN · ATP FINALS", pin=(7.7, 45.07)),
 dict(n=10, region="AMERICAS", topic="GOLF", src="LPGA.COM",
      head="A LIM KIM LEADS AT -18 IN CME FINALE",
      deck="The leader is -18, one clear of Thitikul and Yoshida; the winner takes $4 million, the richest prize in women's golf.",
      scene="golf", chip="-18 · $4M PRIZE", cap="NAPLES, FLORIDA · TIBURON", pin=(-81.8, 26.1)),
 dict(n=11, region="ASIA", topic="SUMO", src="JAPAN SUMO ASSN",
      head="KYUSHU BASHO ENDS IN A TITLE FIGHT",
      deck="Final bouts at 16:00 WIB in Fukuoka; Onosato faces Hoshoryu and Wakamotoharu meets Atamifuji (11-3).",
      scene="sumo", chip="12-2 · 12-2", cap="FUKUOKA · SENSHURAKU", pin=(130.4, 33.6)),
 dict(n=12, region="AMERICAS", topic="GOLF", src="REUTERS · PGA TOUR",
      head="RAIN PUSHES RSM CLASSIC INTO SUNDAY",
      deck="Round three 21:10–23:00 WIB; Thorbjornsen, Penge, Neergaard-Petersen share -9.",
      scene="golf2", chip="3 SHARE -9", cap="SEA ISLAND · GEORGIA", pin=(-81.3, 31.2)),
 dict(n=13, region="AMERICAS", topic="NFL", src="ESPN · NFL",
      head="NFL WEEK 12 ENDS WITH VIKINGS AT 49ERS",
      deck="Eleven Sunday games in the US; the early window is 01:00 WIB Monday, Sunday night is Vikings at the 49ers.",
      scene="nfl", chip="SNF · VIKINGS @ 49ERS", cap="SANTA CLARA · SUNDAY NIGHT", pin=(-121.97, 37.4)),
]

BRIEFS = [
 ("14", "Bahrain demands UNSC enforce Resolution 2817."),
 ("15", "Drone downed at Ali Al Salem base — first since September."),
 ("16", "Gulf tanker attack: UKMTO reported Sat 11:27 UTC."),
 ("17", "Makkah sirens sounded 23:43 Riyadh time Saturday."),
 ("18", "COP31 draft recalls Dubai fossil deal; $120bn target fell."),
 ("19", "COP31 chaired by Murat Kurum; co-host Chris Bowen."),
 ("20", "India 720/9: highest Test total ever in New Zealand."),
 ("21", "Nicholls 175 for NZ; Bumrah took 4-92 in Wellington."),
 ("22", "Las Vegas: round 22, 50 laps on the Strip Circuit."),
 ("23", "NROL-136: 15th batch of the NRO spy constellation."),
 ("24", "Falcon 9 launch delayed from Saturday; window 30 min."),
 ("25", "Hull v Brighton kicks off 21:00 WIB, before Anfield."),
 ("26", "Alcaraz beat Shelton in a comeback to reach the final."),
 ("27", "Thitikul and Yoshida sit one shot back at -17."),
 ("28", "CME winner's $4m: biggest prize in women's golf."),
 ("29", "Atamifuji 11-3 into the final day in Fukuoka."),
 ("30", "RSM Classic final round moves to Monday."),
 ("31", "NFL early window 13:00 ET — 01:00 WIB Monday."),
 ("32", "Gulf radar claims are IRGC claims — unconfirmed."),
 ("33", "Myanmar quake: 02:35:57 IST, which is 04:05 WIB."),
 ("34", "COP31 plenary 06:00 GMT — 13:00 WIB Sunday."),
 ("35", "India declared after 166 overs; NZ trail by 352."),
 ("36", "LPGA leaders tee off about 23:35 WIB in Naples."),
 ("37", "Sumo final bouts 18:00 JST — 16:00 WIB Sunday."),
 ("38", "Three share the RSM lead at -9 after the rain."),
 ("39", "Sunday night football: Vikings at 49ers, 20:20 ET."),
 ("40", "One night spans Bahrain, Kuwait and Hormuz."),
]

TIMELINE = [
 ("02:40 WIB", "IRGC claim"), ("03:43 WIB", "Makkah sirens"),
 ("04:05 WIB", "Myanmar quake"), ("05:42 WIB", "Intercept confirmed"),
 ("06:00 GMT", "COP31 vote set"),
]

NUMBERS = [
 ("720/9", "India's record total"), ("352", "India's lead in runs"),
 ("50", "Laps in Las Vegas"), ("$4M", "LPGA winner's prize"),
 ("-18", "A Lim Kim's lead"), ("2", "Patriot radars claimed hit"),
]

DC_LINE = "Lviv strike 20 Nov · Riyadh missiles 21 Nov · CEPA signed 21 Nov · France march 82,500, 21 Nov · ICJ verdict 19 Nov · Kenya Ebola 11 Nov · Norway oil ruling 13 Nov · Davis Cup final 29 Nov (not yet)"

# --- data-carrying strips: every strip has a caption band + a data chip ---
def draw_scene(kind, x, y, w, h, col):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(26, 48, 74))
    if kind == "radar":
        for r in (18, 34, 50):
            d.arc([x + w // 2 - r, y + h - r, x + w // 2 + r, y + h + r], 180, 360, fill=GOLD, width=2)
        d.polygon([(x + 30, y + h - 8), (x + 46, y + 22), (x + 62, y + h - 8)], fill=ALERT)
        d.polygon([(x + w - 62, y + h - 8), (x + w - 46, y + 30), (x + w - 30, y + h - 8)], fill=ALERT)
        d.ellipse([x + w // 2 - 6, y + 14, x + w // 2 + 6, y + 26], fill=CREAM)
    elif kind == "intercept":
        for i in range(5):
            d.line([x + 12 + i * 26, y + h - 14, x + 30 + i * 26, y + 16], fill=GOLD, width=2)
        d.arc([x + w - 78, y + 6, x + w - 14, y + 58], 200, 340, fill=CREAM, width=3)
        d.ellipse([x + w - 52, y + 8, x + w - 40, y + 20], fill=ALERT)
    elif kind == "summit":
        d.rectangle([x + 18, y + h - 22, x + w - 18, y + h - 17], fill=(32, 58, 88))
        for i, c in enumerate([(217, 95, 75), (232, 179, 60), (29, 111, 184)]):
            d.rectangle([x + 34 + i * 44, y + 8, x + 62 + i * 44, y + h - 24], fill=c)
        d.ellipse([x + w // 2 - 7, y + 8, x + w // 2 + 7, y + h - 24], fill=CREAM)
    elif kind == "quake":
        for r in (12, 26, 40, 54):
            d.ellipse([x + w // 2 - r, y + h // 2 - r // 2, x + w // 2 + r, y + h // 2 + r // 2], outline=GOLD, width=2)
        d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5], fill=ALERT)
    elif kind == "cricket":
        d.rectangle([x, y + h - 26, x + w - 1, y + h - 1], fill=(30, 132, 73))
        d.rectangle([x + w // 2 - 14, y + 8, x + w // 2 + 14, y + h - 26], fill=(201, 168, 106))
        d.line([x + 24, y + 18, x + w - 40, y + h - 30], fill=CREAM, width=4)
        d.ellipse([x + w - 34, y + 10, x + w - 22, y + 22], fill=ALERT)
    elif kind == "race":
        d.ellipse([x + 10, y + 8, x + w - 10, y + h - 8], outline=CREAM, width=5)
        d.ellipse([x + 26, y + 18, x + w - 26, y + h - 18], outline=LINE, width=2)
        d.rectangle([x + w // 2 - 8, y + 10, x + w // 2 + 8, y + 22], fill=ALERT)
        d.rectangle([x + 30, y + h - 26, x + 46, y + h - 14], fill=GOLD)
    elif kind == "rocket":
        mid = y + max(20, h - 22)
        d.polygon([(x + w // 2, y + 4), (x + w // 2 - 9, mid), (x + w // 2 + 9, mid)], fill=CREAM)
        d.rectangle([x + w // 2 - 9, mid, x + w // 2 + 9, y + h - 17], fill=ALERT)
        d.polygon([(x + w // 2 - 4, y + h - 17), (x + w // 2, y + h - 5), (x + w // 2 + 4, y + h - 17)], fill=GOLD)
        for i in range(6):
            d.ellipse([x + 14 + i * 18, y + 12, x + 18 + i * 18, y + 16], fill=MUTED)
    elif kind == "football":
        d.rectangle([x, y + h - 24, x + w - 1, y + h - 1], fill=(30, 132, 73))
        d.line([x, y + h - 24, x + w, y + h - 24], fill=CREAM, width=2)
        d.ellipse([x + w // 2 - 12, y + h - 44, x + w // 2 + 12, y + h - 20], outline=CREAM, width=2)
        d.ellipse([x + 20, y + 10, x + 34, y + 24], fill=CREAM)
    elif kind == "tennis":
        d.rectangle([x + 20, y + 8, x + w - 20, y + h - 8], outline=CREAM, width=2)
        d.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=CREAM, width=2)
        d.ellipse([x + w - 40, y + 12, x + w - 28, y + 24], fill=GOLD)
        d.ellipse([x + 26, y + h - 26, x + 38, y + h - 14], fill=GOLD)
    elif kind == "golf":
        d.rectangle([x, y + h - 22, x + w - 1, y + h - 1], fill=(30, 132, 73))
        d.line([x + w // 2, y + 12, x + w // 2, y + h - 22], fill=CREAM, width=2)
        d.polygon([(x + w // 2, y + 12), (x + w // 2 + 18, y + 18), (x + w // 2, y + 24)], fill=ALERT)
        d.ellipse([x + 22, y + 12, x + 34, y + 24], fill=CREAM)
    elif kind == "golf2":
        d.rectangle([x, y + h - 22, x + w - 1, y + h - 1], fill=(20, 100, 60))
        for i, c in enumerate([GOLD, CREAM, (29, 111, 184)]):
            d.rectangle([x + 26 + i * 34, y + h - 44 - i * 6, x + 52 + i * 34, y + h - 22], fill=c)
        d.ellipse([x + w - 40, y + 10, x + w - 28, y + 22], fill=CREAM)
    elif kind == "sumo":
        d.ellipse([x + w // 2 - 34, y + 6, x + w // 2 + 34, y + h - 6], outline=GOLD, width=3)
        d.ellipse([x + w // 2 - 26, y + h // 2 - 8, x + w // 2 - 10, y + h // 2 + 8], fill=CREAM)
        d.ellipse([x + w // 2 + 10, y + h // 2 - 8, x + w // 2 + 26, y + h // 2 + 8], fill=ALERT)
    elif kind == "nfl":
        d.rectangle([x, y + h - 26, x + w - 1, y + h - 1], fill=(30, 110, 60))
        for i in range(5):
            d.line([x + 18 + i * 30, y + h - 26, x + 18 + i * 30, y + h - 8], fill=CREAM, width=1)
        d.ellipse([x + w - 36, y + 10, x + w - 22, y + 24], fill=(120, 70, 30))
    d.rectangle([x, y + h - 16, x + w - 1, y + h - 1], fill=PANEL_DK)

def draw_lead(c, x, y, w, h):
    shadow_panel(x, y, w, h)
    col = REGIONS[c["region"]]
    draw_scene(c["scene"], x + 6, y + 6, w - 12, 76, col)
    fw = d.textlength(c["chip"], font=F(AB, 10)) + 12
    d.rectangle([x + w - fw - 12, y + 10, x + w - 12, y + 28], fill=col)
    d.text((x + w - fw - 6, y + 12), c["chip"], font=F(AB, 10), fill=CREAM)
    d.text((x + 8, y + 86), "%d  %s · %s" % (c["n"], c["region"], c["topic"]), font=F(AB, 11), fill=GOLD)
    d.text((x + w - 8, y + 86), c["src"], font=F(AB, 9), fill=MUTED, anchor="ra")
    hy = y + 102
    for ln in wrap(c["head"], F(PF, 20), w - 16)[:2]:
        d.text((x + 8, hy), ln, font=F(PF, 20), fill=CREAM); hy += 22
    dy = hy + 2
    for ln in wrap(c["deck"], F(AM, 11), w - 16)[:3]:
        d.text((x + 8, dy), ln, font=F(AM, 11), fill=MUTED); dy += 14

def draw_small(c, x, y, w, h):
    shadow_panel(x, y, w, h)
    col = REGIONS[c["region"]]
    draw_scene(c["scene"], x + 5, y + 5, w - 10, 40, col)
    fw = d.textlength(c["chip"], font=F(AB, 9)) + 10
    d.rectangle([x + w - fw - 10, y + 8, x + w - 10, y + 24], fill=col)
    d.text((x + w - fw - 5, y + 10), c["chip"], font=F(AB, 9), fill=CREAM)
    d.text((x + 7, y + 48), "%d  %s · %s" % (c["n"], c["region"], c["topic"]), font=F(AB, 9), fill=GOLD)
    hy = y + 60
    for ln in wrap(c["head"], F(AB, 12), w - 14)[:2]:
        d.text((x + 7, hy), ln, font=F(AB, 12), fill=CREAM); hy += 13
    dy = hy + 1
    for ln in wrap(c["deck"], F(AM, 10), w - 14)[:3]:
        d.text((x + 7, dy), ln, font=F(AM, 10), fill=MUTED); dy += 11

# --- top block: gold kicker, Playfair masthead anchor, hook band, timeline, numbers ---
Y = 8
d.rectangle([MX, Y, MX + CW - 1, Y + 21], fill=GOLD)
d.text((MX + 8, Y + 4), "THE WORLD IN ONE DAY", font=F(AB, 12), fill=PANEL_DK)
d.text((MX + 300, Y + 4), "SUNDAY 22 NOVEMBER 2026", font=F(AB, 12), fill=PANEL_DK)
kr = "40 STORIES · 13 CARDS · EVERY ONE FROM SUNDAY 22 NOVEMBER"
d.text((MX + CW - 8, Y + 4), kr, font=fit(kr, AB, 11, 460), fill=PANEL_DK, anchor="ra")
Y = 34
mf = fit("THE OVERNIGHT EDITION", PF, 50, CW)
d.text((MX + CW // 2, Y), "THE OVERNIGHT EDITION", font=mf, fill=CREAM, anchor="ma")
Y += 58
HOOK_TEXT = "GULF OVERNIGHT: 2 US RADARS HIT — COP31 FINAL TEXT IN ANTALYA — INDIA 720/9"
d.rectangle([MX, Y, MX + CW - 1, Y + 28], fill=HOOK)
d.text((MX + CW // 2, Y + 7), HOOK_TEXT, font=fit(HOOK_TEXT, AB, 13, CW - 24), fill=CREAM, anchor="ma")
Y += 34
panel(MX, Y, CW, 30)
cell = CW / 5.0
for i, (lab, ev) in enumerate(TIMELINE):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 4, cx0, Y + 26], fill=LINE, width=1)
    d.text((cx0 + 8, Y + 4), lab.upper(), font=F(AB, 10), fill=GOLD)
    d.text((cx0 + 8, Y + 16), ev, font=F(AM, 10), fill=CREAM)
Y += 36
panel(MX, Y, CW, 54)
d.text((MX + 8, Y + 2), "THE DAY IN NUMBERS", font=F(AB, 8), fill=MUTED)
cell = CW / 6.0
for i, (num, cap) in enumerate(NUMBERS):
    cx0 = MX + int(i * cell)
    if i:
        d.line([cx0, Y + 8, cx0, Y + 52], fill=LINE, width=1)
    d.text((cx0 + 8, Y + 8), num, font=fit(num, PF, 23, cell - 14), fill=GOLD)
    for j, ln in enumerate(wrap(cap, F(AM, 9), cell - 14)[:2]):
        d.text((cx0 + 8, Y + 35 + j * 10), ln, font=F(AM, 9), fill=MUTED)
Y += 60

# --- lead row (cards 1-3) + feature grid (cards 4-13), all 3D raised ---
LEAD_Y = Y + 8
for i, c in enumerate(CARDS[:3]):
    draw_lead(c, MX + i * (325 + 8), LEAD_Y, 325, 196)
FEAT_Y = LEAD_Y + 196 + 8
for k, c in enumerate(CARDS[3:]):
    draw_small(c, MX + (k % 5) * (194 + 5), FEAT_Y + (k // 5) * (122 + 8), 194, 122)

# --- bottom: map + ALSO ON briefs (2 columns) ---
BOT_Y = FEAT_Y + 122 + 8 + 122 + 8
BOT_H = 265
MAP_W = 330
panel(MX, BOT_Y, MAP_W, BOT_H)
d.text((MX + 8, BOT_Y + 6), "WHERE IT HAPPENED", font=F(AB, 12), fill=GOLD)
map_x, map_y, mw, mh = MX + 8, BOT_Y + 28, MAP_W - 16, BOT_H - 62
d.rectangle([map_x, map_y, map_x + mw - 1, map_y + mh - 1], fill=PANEL_DK)
def proj(lon, lat):
    return (map_x + (lon + 180.0) / 360.0 * mw, map_y + (82.0 - lat) / 140.0 * mh)
for rings in WORLD.values():
    for ring in rings.split("|"):
        pts = []
        for pair in ring.split(","):
            try:
                lo, la = pair.split(":"); pts.append(proj(float(lo), float(la)))
            except ValueError:
                continue
        if len(pts) > 2:
            d.polygon(pts, fill=LAND)
PIN_OFF = {1: (17, -10), 2: (-14, 10), 3: (-5, -3), 5: (-16, -18), 6: (20, 6),
           8: (-21, 3), 9: (11, 7), 10: (-10, 10), 11: (11, -16)}
for c in CARDS:
    px, py = proj(c["pin"][0], c["pin"][1])
    ox, oy = PIN_OFF.get(c["n"], (0, 0)); px, py = px + ox, py + oy
    col = REGIONS[c["region"]]
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=col, outline=CREAM, width=1)
    d.text((px, py), str(c["n"]), font=F(AB, 10), fill=CREAM, anchor="mm")
ly = map_y + mh + 8
for ln in wrap("Numbered pins = the 13 pictured stories.", F(AM, 10), MAP_W - 16):
    d.text((MX + 8, ly), ln, font=F(AM, 10), fill=MUTED); ly += 12
AO_X = MX + MAP_W + 8
AO_W = W - MX - AO_X
panel(AO_X, BOT_Y, AO_W, BOT_H)
ao_title = "ALSO ON SUNDAY 22 NOVEMBER — 27 MORE STORIES"
d.text((AO_X + 8, BOT_Y + 6), ao_title, font=fit(ao_title, AB, 12, AO_W - 16), fill=GOLD)
bf, bnf = F(AM, 10), F(AB, 10)
col_w = (AO_W - 16 - 14) // 2
lines = []
for num, t in BRIEFS:
    nw = d.textlength(num + " ", font=bnf)
    lines.append((num, nw, wrap(t, bf, col_w - nw)))
total = sum(len(ls) for _, _, ls in lines)
half = (total + 1) // 2
cols, cur, cnt = [[], []], 0, 0
for item in lines:
    if cur == 0 and cnt + len(item[2]) > half and cnt > 0:
        cur = 1
    cols[cur].append(item)
    if cur == 0:
        cnt += len(item[2])
for ci, col in enumerate(cols):
    bx = AO_X + 8 + ci * (col_w + 14)
    by = BOT_Y + 24
    for num, nw, ls in col:
        d.text((bx, by), num, font=bnf, fill=GOLD)
        for ln in ls:
            d.text((bx + nw, by), ln, font=bf, fill=CREAM); by += 11
        by += 1

# --- DATE CHECK + footer ---
DC_Y = BOT_Y + BOT_H + 6
d.rectangle([MX, DC_Y, MX + CW - 1, DC_Y + 36], outline=ALERT, width=2)
d.text((MX + 8, DC_Y + 5), "DATE CHECK", font=F(AB, 10), fill=ALERT)
d.text((MX + 96, DC_Y + 5), DC_LINE, font=F(AM, 9), fill=MUTED)
d.text((MX + 8, DC_Y + 20), "Left out on purpose — these are NOT Sunday stories: see list in README.", font=F(AM, 9), fill=MUTED)
FY = DC_Y + 41
d.text((MX, FY), "Every story happened, or was first reported, on Sunday 22 November 2026. Contested claims are attributed.",
       font=F(AM, 9), fill=MUTED)
d.text((MX + CW, FY), "Sources: Reuters · Anadolu · AFP · IANS · NCS · Premier League · SpaceX · LPGA · PGA Tour · ESPN",
       font=F(AM, 9), fill=MUTED, anchor="ra")

img_q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
img_q.save(OUT, optimize=True)
print("saved", OUT, img.size)
