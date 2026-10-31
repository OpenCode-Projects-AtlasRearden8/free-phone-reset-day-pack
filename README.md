# Free Phone Reset Day Pack

Nine printable sheets for a monthly phone reset ritual: about an hour total,
broken into snack-sized steps with friendly pacing notes on every sheet.
Print them, check boxes, feel calmer. No apps, no signups, no accounts.

Published by [Asdale Dynamics, LLC](https://dylanasdale.github.io) as a free,
open-source printable. Explained like a friend would: plain English, step by
step, never condescending.

## What is in the pack

| # | Sheet | What it does |
|---|-------|--------------|
| 1 | Storage Sweep | Find what is eating your space and clear it |
| 2 | App Purge Decision Card | Four questions and a Keep/Hold/Delete ladder |
| 3 | Camera Roll Album Rules | Four albums and five rules that run themselves |
| 4 | Duplicate Photo Triage | Bursts, twins, and blurs, in easy rounds |
| 5 | Notification Trims | One rule: sound is for people |
| 6 | Subscription Hunt | Where recurring charges hide, and what to do about them |
| 7 | Backup Happiness Check | Five checks and a 1-5 soup-proof meter |
| 8 | Contacts Tidy | Three 5-minute passes, safety net first |
| 9 | The Reward List | Small treat per sheet, big treat for the pack |

## How to build the PDFs

Everything is local: HTML/CSS in `sheets/`, one build script, no network calls.

```
pip install -r requirements.txt   # if WeasyPrint is not already installed
python3 build.py
```

PDFs land in `printables/`, ready to print on US Letter. Build a single sheet
with `python3 build.py --sheet reward-list`; send output elsewhere with
`--out DIR`.

## How to run the tests

```
python3 -m unittest discover -s tests -v
```

The tests rebuild every sheet in a temp directory and verify each one produces
a valid, non-truncated PDF, plus checks that the sheets stay unbranded and
keep their pacing notes.

## Design notes

- Each sheet has a **Pacing** box: how long it takes, and permission to stop
  halfway. Built for low-energy days and ADHD-friendly dabbing.
- Checkboxes are drawn with CSS, so they print crisp at any size.
- The PDFs are deliberately unbranded - just you, checkboxes, and your phone.
- Letter size with generous margins; it degrades gracefully to A4 on request
  (edit `size: Letter` in `sheets/style.css`).

## Relationship to the Phone Comfort Guide

This pack is for the monthly *sweep*: clearing, trimming, backing up, and
claiming the reward. If what you want is help *choosing and using* a phone in
the first place, that is the separate phone-comfort-guide project. They
complement each other; neither requires the other.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC - see [LICENSE](LICENSE).
