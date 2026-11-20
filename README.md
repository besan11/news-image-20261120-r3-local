# news-image-20261120-r3-local — The World in One Day

[![competition](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/besan11/news-image-20261120-r3-local/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/besan11/news-image-20261120-r3-local/reward.svg)](https://make.fun/bounty/news-image-20261120)

Bounty: [Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120)

- Owner: besan11
- Repo: news-image-20261120-r3-local
- Description: A cream-paper newspaper front page summing up the world's
  news of Friday 20 November 2026 in one image: a giant serif date, a
  stats ticker of six big round numbers, a coloured region-count strip
  (45 stories), a UTC timeline rail, three illustrated leads (Cyclone
  Akvan comes ashore in India, Kyiv hit by an overnight ballistic
  barrage, COP31 reaches its final day), ten numbered secondary panels
  with solid colour-block mini-scenes, a numbered navy world map, 32
  numbered briefs, a DATE CHECK box listing the 19 November stories left
  out on purpose, and a freshness footer with named sources. Every lead
  and panel carries a source tag with a UTC stamp.
- Run: `python3 render.py` to draw `entry.png`, then
  `MAKEFUN_OUTPUT_DIR=out python3 main.py` to copy it to the output
  directory.
- Referral code: jpgk45b3

The image is drawn by `render.py` (Python + Pillow, DejaVu fonts shipped
in `fonts/`); `main.py` copies `entry.png` to the output directory and
verifies the PNG magic bytes.
