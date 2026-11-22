# The Overnight Edition — News Image 20261122

![News Image 20261122](https://make.fun/badge/news-image-20261122.svg)
![Rank](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/rank.svg)
![Reward](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/reward.svg)

A one-page broadsheet for **Sunday 22 November 2026**, drawn as a 3D layered
page from the night desk: the stories run in the order the night happened.

The date itself is the masthead. Under it, a red numbers strip (2 Patriot
radars claimed in Bahrain · 05:42 WIB interception confirmation · M4.1 Myanmar
quake · 720/9 in Wellington · 50 laps in Las Vegas · a $4m LPGA prize · 11 NFL
games) and an overnight spine — 02:40 WIB IRGC claim → 03:43 WIB Mecca sirens →
04:05 WIB Myanmar quake → 05:42 WIB coalition confirmation → 06:00 GMT COP31
plenary → 11:00 WIB Las Vegas lights out.

Three pictorial lead scenes carry the night: the Gulf complex (IRGC claims on
two Patriot radars in Bahrain, a drone over Kuwait, a tanker near Hormuz —
claims tagged as claims), the Houthi missile intercepted toward the Mecca
region, and Myanmar's deep M4.1 quake drawn as a cross-section with its 95 km
depth gauge. Ten more pictured cards follow — COP31's final text in Antalya,
India's record 720/9, the Las Vegas GP, Falcon 9 NROL-136, Liverpool v
Manchester United, the Alcaraz–Zverev Turin final, the LPGA finale, Kyushu
sumo's last day, the rain-moved RSM Classic and NFL Week 12 — plus 27 numbered
briefs, a real-polygon world map with numbered pins in the bottom panel, and a
DATE CHECK naming seven stories deliberately left out as not 22 November (and
one not yet: the Davis Cup final, 29 Nov).

Every card carries a data strip and a source/certainty tag; contested claims
are attributed on the card itself. 40 stories, all from 22 November 2026.

## Build

- `draw.py` — renders `entry.png` (1024×1024, PIL only) and `entry-300.png`.
- `main.py` — the hand-in entrypoint: copies the committed `entry.png` into
  `os.environ["MAKEFUN_OUTPUT_DIR"]`.
- `mapdata.py` — real country polygon data used for the map.
- `fonts/` — Playfair Display 900, Archivo Bold, Archivo Medium (OFL).

## License

MIT — see `LICENSE`.
