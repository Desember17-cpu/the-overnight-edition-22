#!/usr/bin/env python3
"""THE OVERNIGHT EDITION — renderer.

Composes a single 1024x1024 front page that sums up Sunday
22 November 2026: thirteen pictured story cards over a locator map,
twenty-seven one-line briefs, a five-slot timeline, a six-figure
numbers strip and an explicit date-check box. Everything is drawn
with Pillow primitives only — no photographs, no network, no clock,
no randomness — so two runs always produce the same file.

All editorial content comes from POOL22-BARU v3 (thirteen events
verified against 22 November 2026 wires). COP31 sits in Antalya,
Turkiye; the Turin singles final is listed without a winner because
none had been decided when the page was composed. Claims that are
contested on the wires (the Gulf radar hits) are labelled as claims
and carry their source next to the story.
"""
import os

from PIL import Image, ImageDraw, ImageFont

from mapdata import WORLD

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE, "fonts")
TARGET = os.path.join(BASE, "entry.png")

# ---------------------------------------------------------------- palette
SIDE = 16                      # page margin
PAGE = 1024                    # square canvas
SPAN = PAGE - 2 * SIDE         # usable width

NIGHT = (14, 26, 43)           # page background
CARD_BG = (22, 40, 63)         # raised panel fill
CARD_DEEP = (11, 21, 36)       # caption band / map sea
INK = (242, 234, 216)          # main text
SOFT = (185, 196, 212)         # secondary text
GILT = (232, 179, 60)          # gold accents
BRICK = (217, 95, 75)          # alert accents
BANNER = (146, 22, 40)         # hook band
RULE = (58, 82, 112)           # hairlines / panel outline
SHADOW = (7, 13, 24)           # drop shadow
SCENE_BG = (26, 48, 74)        # picture tile background
CONTINENT = (201, 168, 106)    # map landmass

REGION_TINT = {
    "MIDEAST": (125, 60, 152),
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "OCEANIA": (20, 143, 119),
    "AMERICAS": (202, 111, 30),
    "GLOBAL": (93, 109, 126),
}

SERIF = "PlayfairDisplay-900.ttf"
SANS_B = "Archivo-Bold.ttf"
SANS_M = "Archivo-Medium.ttf"

# ------------------------------------------------------------------- data
# Story table columns:
#   (number, region, topic, source, headline, deck, scene, chip,
#    caption, pin longitude, pin latitude)
STORIES = [
    (1, "MIDEAST", "THE GULF", "IRGC · BAHRAIN",
     "GULF OVERNIGHT: 2 US RADARS HIT, IRGC CLAIMS",
     "IRGC statements at 02:40 & 03:37 WIB claim 2 Patriot radars hit in Bahrain; a civil site burned and a drone was downed in Kuwait.",
     "radar", "2 RADARS CLAIMED", "BAHRAIN · KUWAIT · THE GULF", 50.6, 26.2),
    (2, "MIDEAST", "MAKKAH SKIES", "ANADOLU",
     "HOUTHI MISSILE FOR MAKKAH INTERCEPTED",
     "Civil-defence sirens sounded 03:43 WIB; the Saudi-led coalition confirmed the intercept at 05:42 WIB on Sunday.",
     "intercept", "05:42 WIB CONFIRMED", "MAKKAH REGION · SAUDI ARABIA", 39.8, 21.4),
    (3, "EUROPE", "COP31", "REUTERS",
     "COP31 FINAL TEXT TABLED IN ANTALYA",
     "Objections closed at 03:00 GMT; the approval plenary is set for 06:00 GMT (13:00 WIB) in Antalya, Turkiye.",
     "summit", "06:00 GMT PLENARY", "ANTALYA · TURKIYE", 30.7, 36.9),
    (4, "ASIA", "QUAKE", "NCS · ANI",
     "MYANMAR SHAKEN BY M4.1 QUAKE",
     "Recorded 04:05 WIB at 24.404N 94.616E; the epicentre was 95 km deep, the National Center for Seismology said.",
     "quake", "M4.1 · 95 KM DEEP", "MYANMAR · 24.404N 94.616E", 94.6, 24.4),
    (5, "OCEANIA", "CRICKET", "IANS · AFP",
     "INDIA DECLARE ON 720/9, A RECORD",
     "Rahul 136 and Pant 128 powered 720/9; New Zealand made 368, leaving India 352 ahead on day four in Wellington.",
     "cricket", "720/9 · LEAD 352", "WELLINGTON · DAY 4", 174.8, -41.3),
    (6, "AMERICAS", "FORMULA 1", "FORMULA1.COM",
     "LAS VEGAS GP RACES INTO THE NIGHT",
     "Lights out 11:00 WIB for 50 laps of the Strip Circuit — round 22 of the season, under the lights.",
     "race", "50 LAPS · 11:00 WIB", "LAS VEGAS · STRIP CIRCUIT", -115.2, 36.1),
    (7, "AMERICAS", "SPACE", "VSFB · SPACEX",
     "FALCON 9 LIFTS NROL-136 SATELLITES",
     "Launch window 19:16–19:46 WIB; booster B1097 flies the 15th NRO batch to Landing Zone 4.",
     "rocket", "19:16 WIB · B1097", "VANDENBERG · SLC-4E", -120.6, 34.7),
    (8, "EUROPE", "FOOTBALL", "PREMIER LEAGUE",
     "LIVERPOOL HOST MANCHESTER UNITED",
     "Kick-off 23:30 WIB in Matchweek 11; Hull host Brighton earlier at 21:00 WIB on Sunday.",
     "football", "23:30 WIB · MW11", "ANFIELD · LIVERPOOL", -2.96, 53.43),
    (9, "EUROPE", "TENNIS", "ATP · REUTERS",
     "ALCARAZ MEETS ZVEREV IN TURIN FINAL",
     "The final is played at 23:00 WIB in Turin; Alcaraz reached it after fighting back past Shelton.",
     "tennis", "23:00 WIB · TURIN", "TURIN · ATP FINALS", 7.7, 45.07),
    (10, "AMERICAS", "GOLF", "LPGA.COM",
     "A LIM KIM LEADS AT -18 IN CME FINALE",
     "The leader is -18, one clear of Thitikul and Yoshida; the winner takes $4 million, the richest prize in women's golf.",
     "golf", "-18 · $4M PRIZE", "NAPLES, FLORIDA · TIBURON", -81.8, 26.1),
    (11, "ASIA", "SUMO", "JAPAN SUMO ASSN",
     "KYUSHU BASHO ENDS IN A TITLE FIGHT",
     "Final bouts at 16:00 WIB in Fukuoka; Onosato faces Hoshoryu and Wakamotoharu meets Atamifuji (11-3).",
     "sumo", "12-2 · 12-2", "FUKUOKA · SENSHURAKU", 130.4, 33.6),
    (12, "AMERICAS", "GOLF", "REUTERS · PGA TOUR",
     "RAIN PUSHES RSM CLASSIC INTO SUNDAY",
     "Round three 21:10–23:00 WIB; Thorbjornsen, Penge, Neergaard-Petersen share -9.",
     "golf2", "3 SHARE -9", "SEA ISLAND · GEORGIA", -81.3, 31.2),
    (13, "AMERICAS", "NFL", "ESPN · NFL",
     "NFL WEEK 12 ENDS WITH VIKINGS AT 49ERS",
     "Eleven Sunday games in the US; the early window is 01:00 WIB Monday, Sunday night is Vikings at the 49ers.",
     "nfl", "SNF · VIKINGS @ 49ERS", "SANTA CLARA · SUNDAY NIGHT", -121.97, 37.4),
]
(N_NUM, N_REGION, N_TOPIC, N_SRC, N_HEAD, N_DECK,
 N_SCENE, N_CHIP, N_CAP, N_LON, N_LAT) = range(11)

SHORTS = [
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

CLOCK = [
    ("02:40 WIB", "IRGC claim"),
    ("03:43 WIB", "Makkah sirens"),
    ("04:05 WIB", "Myanmar quake"),
    ("05:42 WIB", "Intercept confirmed"),
    ("06:00 GMT", "COP31 vote set"),
]

FIGURES = [
    ("720/9", "India's record total"),
    ("352", "India's lead in runs"),
    ("50", "Laps in Las Vegas"),
    ("$4M", "LPGA winner's prize"),
    ("-18", "A Lim Kim's lead"),
    ("2", "Patriot radars claimed hit"),
]

EXCLUDED = ("Lviv strike 20 Nov · Riyadh missiles 21 Nov · CEPA signed 21 Nov · "
            "France march 82,500, 21 Nov · ICJ verdict 19 Nov · Kenya Ebola 11 Nov · "
            "Norway oil ruling 13 Nov · Davis Cup final 29 Nov (not yet)")

# Per-pin nudges so numbered markers never sit on top of each other.
PIN_NUDGE = {1: (17, -10), 2: (-14, 10), 3: (-5, -3), 5: (-16, -18),
             6: (20, 6), 8: (-21, 3), 9: (11, 7), 10: (-10, 10), 11: (11, -16)}


# ------------------------------------------------------------------ fonts
class TypeCase:
    """Memoised truetype loader bound to the bundled fonts folder."""

    def __init__(self, folder):
        self._folder = folder
        self._loaded = {}

    def get(self, name, size):
        key = (name, int(size))
        if key not in self._loaded:
            path = os.path.join(self._folder, name)
            self._loaded[key] = ImageFont.truetype(path, int(size))
        return self._loaded[key]


# ------------------------------------------------------------------- page
class Page:
    """Owns the canvas and every drawing helper used to fill it."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE, PAGE), NIGHT)
        self.pen = ImageDraw.Draw(self.image)
        self.type = TypeCase(FONT_PATH)

    # -- measuring ------------------------------------------------------
    def width_of(self, text, font):
        return self.pen.textlength(text, font=font)

    def shrink_to_fit(self, text, name, size, max_w, floor=8):
        s = size
        while s > floor and self.width_of(text, self.type.get(name, s)) > max_w:
            s -= 1
        return self.type.get(name, s)

    def fold(self, text, font, max_w):
        """Greedy word wrap against this page's own text metrics."""
        done, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.width_of(trial, font) <= max_w or not current:
                current = trial
            else:
                done.append(current)
                current = word
        if current:
            done.append(current)
        return done

    # -- shapes ---------------------------------------------------------
    def box(self, x, y, w, h, fill=CARD_BG, outline=None):
        self.pen.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline)

    def raised(self, x, y, w, h, depth=6):
        self.pen.rectangle([x + depth, y + depth,
                            x + w - 1 + depth, y + h - 1 + depth], fill=SHADOW)
        self.pen.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD_BG, outline=RULE)

    def say(self, xy, text, font, fill, anchor=None):
        self.pen.text(xy, text, font=font, fill=fill, anchor=anchor)


# ----------------------------------------------------------------- scenes
# Each painter receives the page plus the tile's top-left corner and size,
# draws its little vector vignette, and finishes with the caption band.
def scene_radar(pg, x, y, w, h):
    d = pg.pen
    for r in (18, 34, 50):
        d.arc([x + w // 2 - r, y + h - r, x + w // 2 + r, y + h + r], 180, 360, fill=GILT, width=2)
    d.polygon([(x + 30, y + h - 8), (x + 46, y + 22), (x + 62, y + h - 8)], fill=BRICK)
    d.polygon([(x + w - 62, y + h - 8), (x + w - 46, y + 30), (x + w - 30, y + h - 8)], fill=BRICK)
    d.ellipse([x + w // 2 - 6, y + 14, x + w // 2 + 6, y + 26], fill=INK)


def scene_intercept(pg, x, y, w, h):
    d = pg.pen
    for i in range(5):
        d.line([x + 12 + i * 26, y + h - 14, x + 30 + i * 26, y + 16], fill=GILT, width=2)
    d.arc([x + w - 78, y + 6, x + w - 14, y + 58], 200, 340, fill=INK, width=3)
    d.ellipse([x + w - 52, y + 8, x + w - 40, y + 20], fill=BRICK)


def scene_summit(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x + 18, y + h - 22, x + w - 18, y + h - 17], fill=(32, 58, 88))
    for i, c in enumerate([(217, 95, 75), (232, 179, 60), (29, 111, 184)]):
        d.rectangle([x + 34 + i * 44, y + 8, x + 62 + i * 44, y + h - 24], fill=c)
    d.ellipse([x + w // 2 - 7, y + 8, x + w // 2 + 7, y + h - 24], fill=INK)


def scene_quake(pg, x, y, w, h):
    d = pg.pen
    for r in (12, 26, 40, 54):
        d.ellipse([x + w // 2 - r, y + h // 2 - r // 2, x + w // 2 + r, y + h // 2 + r // 2], outline=GILT, width=2)
    d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5], fill=BRICK)


def scene_cricket(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x, y + h - 26, x + w - 1, y + h - 1], fill=(30, 132, 73))
    d.rectangle([x + w // 2 - 14, y + 8, x + w // 2 + 14, y + h - 26], fill=(201, 168, 106))
    d.line([x + 24, y + 18, x + w - 40, y + h - 30], fill=INK, width=4)
    d.ellipse([x + w - 34, y + 10, x + w - 22, y + 22], fill=BRICK)


def scene_race(pg, x, y, w, h):
    d = pg.pen
    d.ellipse([x + 10, y + 8, x + w - 10, y + h - 8], outline=INK, width=5)
    d.ellipse([x + 26, y + 18, x + w - 26, y + h - 18], outline=RULE, width=2)
    d.rectangle([x + w // 2 - 8, y + 10, x + w // 2 + 8, y + 22], fill=BRICK)
    d.rectangle([x + 30, y + h - 26, x + 46, y + h - 14], fill=GILT)


def scene_rocket(pg, x, y, w, h):
    d = pg.pen
    mid = y + max(20, h - 22)
    d.polygon([(x + w // 2, y + 4), (x + w // 2 - 9, mid), (x + w // 2 + 9, mid)], fill=INK)
    d.rectangle([x + w // 2 - 9, mid, x + w // 2 + 9, y + h - 17], fill=BRICK)
    d.polygon([(x + w // 2 - 4, y + h - 17), (x + w // 2, y + h - 5), (x + w // 2 + 4, y + h - 17)], fill=GILT)
    for i in range(6):
        d.ellipse([x + 14 + i * 18, y + 12, x + 18 + i * 18, y + 16], fill=SOFT)


def scene_football(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x, y + h - 24, x + w - 1, y + h - 1], fill=(30, 132, 73))
    d.line([x, y + h - 24, x + w, y + h - 24], fill=INK, width=2)
    d.ellipse([x + w // 2 - 12, y + h - 44, x + w // 2 + 12, y + h - 20], outline=INK, width=2)
    d.ellipse([x + 20, y + 10, x + 34, y + 24], fill=INK)


def scene_tennis(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x + 20, y + 8, x + w - 20, y + h - 8], outline=INK, width=2)
    d.line([x + w // 2, y + 8, x + w // 2, y + h - 8], fill=INK, width=2)
    d.ellipse([x + w - 40, y + 12, x + w - 28, y + 24], fill=GILT)
    d.ellipse([x + 26, y + h - 26, x + 38, y + h - 14], fill=GILT)


def scene_golf(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x, y + h - 22, x + w - 1, y + h - 1], fill=(30, 132, 73))
    d.line([x + w // 2, y + 12, x + w // 2, y + h - 22], fill=INK, width=2)
    d.polygon([(x + w // 2, y + 12), (x + w // 2 + 18, y + 18), (x + w // 2, y + 24)], fill=BRICK)
    d.ellipse([x + 22, y + 12, x + 34, y + 24], fill=INK)


def scene_golf_rain(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x, y + h - 22, x + w - 1, y + h - 1], fill=(20, 100, 60))
    for i, c in enumerate([GILT, INK, (29, 111, 184)]):
        d.rectangle([x + 26 + i * 34, y + h - 44 - i * 6, x + 52 + i * 34, y + h - 22], fill=c)
    d.ellipse([x + w - 40, y + 10, x + w - 28, y + 22], fill=INK)


def scene_sumo(pg, x, y, w, h):
    d = pg.pen
    d.ellipse([x + w // 2 - 34, y + 6, x + w // 2 + 34, y + h - 6], outline=GILT, width=3)
    d.ellipse([x + w // 2 - 26, y + h // 2 - 8, x + w // 2 - 10, y + h // 2 + 8], fill=INK)
    d.ellipse([x + w // 2 + 10, y + h // 2 - 8, x + w // 2 + 26, y + h // 2 + 8], fill=BRICK)


def scene_nfl(pg, x, y, w, h):
    d = pg.pen
    d.rectangle([x, y + h - 26, x + w - 1, y + h - 1], fill=(30, 110, 60))
    for i in range(5):
        d.line([x + 18 + i * 30, y + h - 26, x + 18 + i * 30, y + h - 8], fill=INK, width=1)
    d.ellipse([x + w - 36, y + 10, x + w - 22, y + 24], fill=(120, 70, 30))


SCENE_PAINT = {
    "radar": scene_radar, "intercept": scene_intercept, "summit": scene_summit,
    "quake": scene_quake, "cricket": scene_cricket, "race": scene_race,
    "rocket": scene_rocket, "football": scene_football, "tennis": scene_tennis,
    "golf": scene_golf, "golf2": scene_golf_rain, "sumo": scene_sumo,
    "nfl": scene_nfl,
}


def paint_tile(pg, story, x, y, w, h):
    """Scene background, vignette, then the dark caption strip."""
    pg.pen.rectangle([x, y, x + w - 1, y + h - 1], fill=SCENE_BG)
    SCENE_PAINT[story[N_SCENE]](pg, x, y, w, h)
    pg.pen.rectangle([x, y + h - 16, x + w - 1, y + h - 1], fill=CARD_DEEP)


# ------------------------------------------------------------------ cards
def lead_card(pg, story, x, y, w, h):
    pg.raised(x, y, w, h)
    tint = REGION_TINT[story[N_REGION]]
    paint_tile(pg, story, x + 6, y + 6, w - 12, 76)
    chip_w = pg.width_of(story[N_CHIP], pg.type.get(SANS_B, 10)) + 12
    pg.pen.rectangle([x + w - chip_w - 12, y + 10, x + w - 12, y + 28], fill=tint)
    pg.say((x + w - chip_w - 6, y + 12), story[N_CHIP], pg.type.get(SANS_B, 10), INK)
    pg.say((x + 8, y + 86), "%d  %s · %s" % (story[N_NUM], story[N_REGION], story[N_TOPIC]),
           pg.type.get(SANS_B, 11), GILT)
    pg.say((x + w - 8, y + 86), story[N_SRC], pg.type.get(SANS_B, 9), SOFT, anchor="ra")
    cursor = y + 102
    for line in pg.fold(story[N_HEAD], pg.type.get(SERIF, 20), w - 16)[:2]:
        pg.say((x + 8, cursor), line, pg.type.get(SERIF, 20), INK)
        cursor += 22
    cursor += 2
    for line in pg.fold(story[N_DECK], pg.type.get(SANS_M, 11), w - 16)[:3]:
        pg.say((x + 8, cursor), line, pg.type.get(SANS_M, 11), SOFT)
        cursor += 14


def mini_card(pg, story, x, y, w, h):
    pg.raised(x, y, w, h)
    tint = REGION_TINT[story[N_REGION]]
    paint_tile(pg, story, x + 5, y + 5, w - 10, 40)
    chip_w = pg.width_of(story[N_CHIP], pg.type.get(SANS_B, 9)) + 10
    pg.pen.rectangle([x + w - chip_w - 10, y + 8, x + w - 10, y + 24], fill=tint)
    pg.say((x + w - chip_w - 5, y + 10), story[N_CHIP], pg.type.get(SANS_B, 9), INK)
    pg.say((x + 7, y + 48), "%d  %s · %s" % (story[N_NUM], story[N_REGION], story[N_TOPIC]),
           pg.type.get(SANS_B, 9), GILT)
    cursor = y + 60
    for line in pg.fold(story[N_HEAD], pg.type.get(SANS_B, 12), w - 14)[:2]:
        pg.say((x + 7, cursor), line, pg.type.get(SANS_B, 12), INK)
        cursor += 13
    cursor += 1
    for line in pg.fold(story[N_DECK], pg.type.get(SANS_M, 10), w - 14)[:3]:
        pg.say((x + 7, cursor), line, pg.type.get(SANS_M, 10), SOFT)
        cursor += 11


# --------------------------------------------------------------- sections
def header_block(pg):
    """Gold kicker, masthead, hook band, timeline and numbers strip."""
    y = 8
    pg.pen.rectangle([SIDE, y, SIDE + SPAN - 1, y + 21], fill=GILT)
    pg.say((SIDE + 8, y + 4), "THE WORLD IN ONE DAY", pg.type.get(SANS_B, 12), CARD_DEEP)
    pg.say((SIDE + 300, y + 4), "SUNDAY 22 NOVEMBER 2026", pg.type.get(SANS_B, 12), CARD_DEEP)
    strap = "40 STORIES · 13 CARDS · EVERY ONE FROM SUNDAY 22 NOVEMBER"
    pg.say((SIDE + SPAN - 8, y + 4), strap,
           pg.shrink_to_fit(strap, SANS_B, 11, 460), CARD_DEEP, anchor="ra")

    y = 34
    masthead = pg.shrink_to_fit("THE OVERNIGHT EDITION", SERIF, 50, SPAN)
    pg.say((SIDE + SPAN // 2, y), "THE OVERNIGHT EDITION", masthead, INK, anchor="ma")
    y += 58

    hook = "GULF OVERNIGHT: 2 US RADARS HIT — COP31 FINAL TEXT IN ANTALYA — INDIA 720/9"
    pg.pen.rectangle([SIDE, y, SIDE + SPAN - 1, y + 28], fill=BANNER)
    pg.say((SIDE + SPAN // 2, y + 7), hook,
           pg.shrink_to_fit(hook, SANS_B, 13, SPAN - 24), INK, anchor="ma")
    y += 34

    pg.box(SIDE, y, SPAN, 30)
    slot = SPAN / 5.0
    for i, (stamp, event) in enumerate(CLOCK):
        left = SIDE + int(i * slot)
        if i:
            pg.pen.line([left, y + 4, left, y + 26], fill=RULE, width=1)
        pg.say((left + 8, y + 4), stamp.upper(), pg.type.get(SANS_B, 10), GILT)
        pg.say((left + 8, y + 16), event, pg.type.get(SANS_M, 10), INK)
    y += 36

    pg.box(SIDE, y, SPAN, 54)
    pg.say((SIDE + 8, y + 2), "THE DAY IN NUMBERS", pg.type.get(SANS_B, 8), SOFT)
    slot = SPAN / 6.0
    for i, (figure, caption) in enumerate(FIGURES):
        left = SIDE + int(i * slot)
        if i:
            pg.pen.line([left, y + 8, left, y + 52], fill=RULE, width=1)
        pg.say((left + 8, y + 8), figure,
               pg.shrink_to_fit(figure, SERIF, 23, slot - 14), GILT)
        for j, line in enumerate(pg.fold(caption, pg.type.get(SANS_M, 9), slot - 14)[:2]):
            pg.say((left + 8, y + 35 + j * 10), line, pg.type.get(SANS_M, 9), SOFT)
    return y + 60


def card_rows(pg, top):
    lead_y = top + 8
    for i, story in enumerate(STORIES[:3]):
        lead_card(pg, story, SIDE + i * (325 + 8), lead_y, 325, 196)
    feat_y = lead_y + 196 + 8
    for k, story in enumerate(STORIES[3:]):
        mini_card(pg, story,
                  SIDE + (k % 5) * (194 + 5), feat_y + (k // 5) * (122 + 8), 194, 122)
    return feat_y + 122 + 8 + 122 + 8


def map_panel(pg, x, y, w, h):
    pg.box(x, y, w, h)
    pg.say((x + 8, y + 6), "WHERE IT HAPPENED", pg.type.get(SANS_B, 12), GILT)
    mx, my, mw, mh = x + 8, y + 28, w - 16, h - 62
    pg.pen.rectangle([mx, my, mx + mw - 1, my + mh - 1], fill=CARD_DEEP)

    def place(lon, lat):
        return (mx + (lon + 180.0) / 360.0 * mw, my + (82.0 - lat) / 140.0 * mh)

    for rings in WORLD.values():
        for ring in rings.split("|"):
            points = []
            for pair in ring.split(","):
                try:
                    lo, la = pair.split(":")
                    points.append(place(float(lo), float(la)))
                except ValueError:
                    continue
            if len(points) > 2:
                pg.pen.polygon(points, fill=CONTINENT)

    def drop_pin(story):
        px, py = place(story[N_LON], story[N_LAT])
        dx, dy = PIN_NUDGE.get(story[N_NUM], (0, 0))
        px, py = px + dx, py + dy
        pg.pen.ellipse([px - 9, py - 9, px + 9, py + 9],
                       fill=REGION_TINT[story[N_REGION]], outline=INK, width=1)
        pg.say((px, py), str(story[N_NUM]), pg.type.get(SANS_B, 10), INK, anchor="mm")

    for story in STORIES:
        drop_pin(story)

    note_y = my + mh + 8
    for line in pg.fold("Numbered pins = the 13 pictured stories.",
                        pg.type.get(SANS_M, 10), w - 16):
        pg.say((x + 8, note_y), line, pg.type.get(SANS_M, 10), SOFT)
        note_y += 12


def split_into_columns(wrapped):
    """Balance pre-wrapped briefs across two columns by line count.

    Walks the items in order, filling column one until adding the next
    item would pass the halfway line count, then spills the rest into
    column two. Returns the pair of columns.
    """
    total = sum(len(lines) for _, _, lines in wrapped)
    half = (total + 1) // 2
    columns, current, count = [[], []], 0, 0
    for item in wrapped:
        if current == 0 and count + len(item[2]) > half and count > 0:
            current = 1
        columns[current].append(item)
        if current == 0:
            count += len(item[2])
    return columns


def briefs_panel(pg, x, y, w, h):
    pg.box(x, y, w, h)
    heading = "ALSO ON SUNDAY 22 NOVEMBER — 27 MORE STORIES"
    pg.say((x + 8, y + 6), heading,
           pg.shrink_to_fit(heading, SANS_B, 12, w - 16), GILT)
    body = pg.type.get(SANS_M, 10)
    bold = pg.type.get(SANS_B, 10)
    col_w = (w - 16 - 14) // 2

    wrapped = []
    for num, text in SHORTS:
        num_w = pg.width_of(num + " ", bold)
        wrapped.append((num, num_w, pg.fold(text, body, col_w - num_w)))

    for ci, column in enumerate(split_into_columns(wrapped)):
        bx = x + 8 + ci * (col_w + 14)
        by = y + 24
        for num, num_w, lines in column:
            pg.say((bx, by), num, bold, GILT)
            for line in lines:
                pg.say((bx + num_w, by), line, body, INK)
                by += 11
            by += 1


def footer_block(pg, y):
    pg.pen.rectangle([SIDE, y, SIDE + SPAN - 1, y + 36], outline=BRICK, width=2)
    pg.say((SIDE + 8, y + 5), "DATE CHECK", pg.type.get(SANS_B, 10), BRICK)
    pg.say((SIDE + 96, y + 5), EXCLUDED, pg.type.get(SANS_M, 9), SOFT)
    pg.say((SIDE + 8, y + 20),
           "Left out on purpose — these are NOT Sunday stories: see list in README.",
           pg.type.get(SANS_M, 9), SOFT)
    foot_y = y + 41
    pg.say((SIDE, foot_y),
           "Every story happened, or was first reported, on Sunday 22 November 2026. Contested claims are attributed.",
           pg.type.get(SANS_M, 9), SOFT)
    pg.say((SIDE + SPAN, foot_y),
           "Sources: Reuters · Anadolu · AFP · IANS · NCS · Premier League · SpaceX · LPGA · PGA Tour · ESPN",
           pg.type.get(SANS_M, 9), SOFT, anchor="ra")


def compose():
    pg = Page()
    top = header_block(pg)
    bottom_y = card_rows(pg, top)
    bottom_h = 265
    map_w = 330
    map_panel(pg, SIDE, bottom_y, map_w, bottom_h)
    briefs_panel(pg, SIDE + map_w + 8, bottom_y,
                 PAGE - SIDE - (SIDE + map_w + 8), bottom_h)
    footer_block(pg, bottom_y + bottom_h + 6)
    return pg.image


def render():
    page = compose()
    squeezed = page.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    squeezed.save(TARGET, optimize=True)
    print("saved", TARGET, page.size)


if __name__ == "__main__":
    render()
