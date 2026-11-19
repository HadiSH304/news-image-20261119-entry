# The World in One Day — Thursday 19 November 2026

A make.fun entry for
[news-image-20261119](https://make.fun/bounty/news-image-20261119):
one image that sums up 19 November 2026's world news.

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/HadiSH304/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/HadiSH304/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

## The image

A newspaper front page in one 1024×1024 image. The masthead names the day
— **THURSDAY 19 NOVEMBER 2026** — and 36 stories cover it:

- **Lead:** Trump, Xi and Putin hold their first three-way summit, Shenzhen
- **GTA VI arrives after a 13-year wait** — midnight rollout, 15.9m pre-orders
- **Anthropic debuts in the biggest IPO on record** — $81.3bn raised
- **World Court rules on Myanmar's Rohingya case** — first state found to have
  committed genocide
- **COP31 enters its final 48 hours** · **Cyclone Akvan bears down on Odisha**
  · **Crimean Bridge hit a third time** · **Israeli tanks cross the Gaza
  ceasefire line** · **Two tankers ablaze in the Strait of Hormuz** · and 23
  more stories, with a DATE CHECK box for what was first reported on
  Wednesday 18 November.

Every illustration is a flat drawing made for this page — no photographs, no
recognisable faces, no hands — and every word is real rendered text drawn by
`compose.py`, so the page stays legible at 300 px.

## How it runs

`main.py` (standard library only) copies `image.jpg` to
`/output/entry.png`. It writes identical bytes on every run and needs no
network. `python3 compose.py` rebuilds `image.jpg` from scratch with Pillow
(`python3 compose.py B` builds the navy-masthead variant instead).
