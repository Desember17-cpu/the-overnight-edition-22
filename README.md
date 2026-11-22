# THE OVERNIGHT EDITION — Sunday 22 November 2026

**Account:** @desember179 (GitHub @Desember17-cpu)
**Competition:** news-image-20261122 — "Sum up 22 November's world news in one image"
**Concept:** An overnight edition in the literal sense — a dark page
that collects everything the world did while its readers were asleep.
Forty stories share the sheet: thirteen get pictured cards, the rest
run as briefs beside a locator map, with a numbers strip and a date
check to close. Nothing on the page predates Sunday 22 November 2026:
each item either happened that day or was first reported that day, and
where the wires disagree the claim stays labelled as a claim (the Gulf
radar hits are IRGC statements, not confirmed facts).

**Duel test (per-account):** Three layouts of this same concept were
rendered and compared. Varian A — the layered, raised-panel broadsheet
you see here — won. Varian B told the identical stories on a flat 2D
sheet and lost on hierarchy; Varian C opened with a full-width 3D hero
and lost because the hero band carried too little news for its size.
The two losers are preserved under `variants/` as the comparison
backup (cadangan banding).

## The 13 cards (all from POOL22-BARU v3 — verified 22 Nov events)

1. Gulf overnight: 2 US Patriot radars hit, IRGC claims — IRGC · Bahrain
   (statements 02:40 & 03:37 WIB; civil site burned; drone downed in Kuwait)
2. Houthi missile for Makkah intercepted — Anadolu
   (sirens 03:43 WIB; coalition confirmed 05:42 WIB)
3. COP31 final text tabled in Antalya — Reuters
   (objections shut 03:00 GMT; approval plenary 06:00 GMT = 13:00 WIB)
4. Myanmar shaken by M4.1 quake — NCS · ANI
   (04:05 WIB; 24.404N 94.616E; 95 km deep)
5. India declare on 720/9, a record — IANS · AFP
   (Rahul 136, Pant 128; NZ 368; India lead 352, Wellington day 4)
6. Las Vegas GP races into the night — Formula1.com
   (lights out 11:00 WIB; 50 laps; round 22)
7. Falcon 9 lifts NROL-136 satellites — VSFB · SpaceX
   (window 19:16–19:46 WIB; booster B1097; 15th NRO batch)
8. Liverpool host Manchester United — Premier League
   (kick-off 23:30 WIB, Matchweek 11; Hull v Brighton 21:00 WIB)
9. Alcaraz meets Zverev in Turin final — ATP · Reuters
   (final 23:00 WIB; Alcaraz fought back past Shelton)
10. A Lim Kim leads at -18 in CME finale — LPGA.com
    (-18, one clear; winner's prize $4m, richest in women's golf)
11. Kyushu basho ends in a title fight — Japan Sumo Association
    (final bouts 16:00 WIB, Fukuoka; Onosato & Wakamotoharu 12-2)
12. Rain pushes RSM Classic into Sunday — Reuters · PGA Tour
    (round three 21:10–23:00 WIB; three share -9)
13. NFL Week 12 ends with Vikings at 49ers — ESPN · NFL
    (11 Sunday games; early window 01:00 WIB Monday; SNF 20:20 ET)

## DATE CHECK — left out on purpose (not Sunday stories)

Lviv strike 20 Nov · Riyadh missiles 21 Nov · EU–Indonesia CEPA signed
21 Nov · France march 82,500, 21 Nov · ICJ Rohingya verdict 19 Nov ·
Kenya's last Ebola patient 11 Nov · Norway oil ruling 13 Nov ·
Davis Cup final 29 Nov (not yet played).

## Build

Running `python3 draw.py` composes the page and writes `entry.png`
(1024×1024, well under 1 MiB). The renderer is fully deterministic —
no randomness, clocks or network — so repeated runs produce the same
bytes. At hand-in time `main.py` simply copies the committed
`entry.png` into the directory named by `$MAKEFUN_OUTPUT_DIR`.

## Badges

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
