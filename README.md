[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Gobpox/news-image-24nov/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Gobpox/news-image-24nov/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Picture — Tuesday 24 November 2026

A make.fun `news-image-20261124` entry: one 1024×1024 image summing up
Tuesday 24 November 2026's world news — 3 heroes, 10 cards and a
21-line ALSO rail: exactly 34 stories, every story dated to the day,
with a date check naming what was excluded and a "not yet" line.
The strap count is computed from the story table, never hand-typed.

## The day

A US jury convicts Huawei on 10 of 12 counts. Iran says mines hit
3 tankers in Hormuz — carried as a claim, with the maritime centre's
"unconfirmed" in the deck, because a disputed claim shown as settled
fact is exactly what faithfulness framing exists to prevent.
Malaysia will repatriate 6,803 Myanmar nationals in December.
Nvidia slides about 7% a day after its 31.5% jump (that jump is
Monday's news, and sits in the date check, not the day's stories).

## Craft amendments (from the previous edition's verdict)

34 stories, locked. Decks are one line in every panel; ALSO
sub-lines carry only a core figure and a source, or nothing; the
last ALSO row carries no sub-line at all. Hero and card decks share
one size; all small captions share one size. The pictured layer is
unchanged (date, hero and card headlines, strips, rail numbers),
and it is confirmed-only: the day's single-outlet story (Solomon
Islands, reported) sits in ALSO with a REPORTED chip.

## Build

`draw.py` renders `entry.png` with Pillow from a single story data
table (strap, region tally and field tally are computed from that
table). Figures live in `figures.json`, the single registry every
panel draws its numbers from. `main.py` is the competition entry
point: it copies `entry.png` to the output directory, standard
library only, deterministic bytes.

## Gates

- `check_numbers.py` passes with no FAIL (exit 0).
- Seven ink-measured audits (text-vs-text, text-vs-line,
  text-vs-graphics, strip, masthead, rail, date-check) all report
  0 findings at a 3px minimum clearance.
- `gate_300.py` + checklist read by eye: date, heroes, card
  headlines and rail numbers stand on their own at 300px.
- Two runs of `draw.py` produce byte-identical PNGs.

SPDX-License-Identifier: MIT
