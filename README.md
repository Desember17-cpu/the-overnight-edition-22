[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Desember17-cpu/the-overnight-edition-22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The Overnight Edition — News Image 20261122




A one-page broadsheet for **Sunday 22 November 2026**, drawn as a 3D layered
page from the night desk: the stories run in the order the night happened.

The date itself is the masthead. Under it, a red numbers strip (2 Patriot
radars claimed in Bahrain · 05:42 WIB interception confirmation · M4.1 Myanmar
quake · 720/9 in Wellington · 50 laps in Las Vegas · a $4m LPGA prize · 11 NFL
games), a region tally bar whose seven segments sum to the page's 37 stories,
and an overnight spine — 02:40 WIB IRGC claim → 03:43 WIB Mecca sirens →
04:05 WIB Myanmar quake → 05:42 WIB coalition confirmation → 06:00 GMT COP31
plenary → 11:00 WIB Las Vegas lights out.

Round 3 keeps the overnight concept and fixes what round 2 lacked —
saturation and subject scale. The three lead scenes are now 125 px tall and
each is built around one giant bright colour field: a huge orange
interception burst over Bahrain, a golden burst over a lit Mecca dome, and a
fully coloured strata cross-section under Myanmar. Lead headlines run at
28 px serif. Ten more pictured cards follow — COP31's final text in Antalya,
India's record 720/9, the Las Vegas GP, Falcon 9 NROL-136, Liverpool v
Manchester United, the Alcaraz–Zverev Turin final, the LPGA finale, Kyushu
sumo's last day, the rain-moved RSM Classic and NFL Week 12 — each with a
50 px region-coloured band and a certainty chip (CONFIRMED · OFFICIAL ·
REPORTED · CLAIM, legend printed in DATE CHECK). Plus 24 numbered briefs, a
real-polygon world map with numbered pins in the bottom panel, and a
three-part DATE CHECK: seven stories left out as not 22 November, three
same-day items not yet finished (COP31 final adoption, Liverpool v Man Utd,
the ATP Turin final), and the contested claims (IRGC on the Patriot radars,
the Houthi interception claim).

37 stories, all from 22 November 2026, all from POOL22-BARU v3.

## Build

- `draw.py` — renders `entry.png` (1024×1024, PIL only) and `entry-300.png`.
- `main.py` — the hand-in entrypoint: copies the committed `entry.png` into
  `os.environ["MAKEFUN_OUTPUT_DIR"]`.
- `mapdata.py` — real country polygon data used for the map.
- `fonts/` — Playfair Display 900, Archivo Bold, Archivo Medium (OFL).

## License

MIT — see `LICENSE`.
