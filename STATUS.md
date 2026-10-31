# STATUS - Free Phone Reset Day Pack

Date: 2026-10-31
Owner: Asdale Dynamics, LLC

## What was built

Nine printable sheets for a monthly phone reset ritual (~1 hour total,
snack-sized steps, friendly pacing note on every sheet):

1. Storage Sweep - storage-sweep-checklist.pdf (2 pages)
2. App Purge Decision Card - app-purge-decision-card.pdf (2 pages)
3. Camera Roll Album Rules - camera-roll-album-rules.pdf (2 pages)
4. Duplicate Photo Triage - duplicate-photo-triage.pdf (2 pages)
5. Notification Trims, One Page - notification-trims-one-pager.pdf (2 pages)
6. The Subscription Hunt - subscription-hunt-sheet.pdf (1 page)
7. The Backup Happiness Check - backup-happiness-check.pdf (1 page)
8. The Contacts Tidy - contacts-tidy-split.pdf (2 pages)
9. The Reward List - reward-list.pdf (2 pages)

Structure:
- `sheets/` - 9 HTML sources + shared `style.css` (US Letter, CSS-drawn
  checkboxes, pacing boxes, print-friendly page rules)
- `build.py` - one local build script (WeasyPrint), supports `--out DIR`,
  `--sheet NAME` (repeatable), `--quiet`
- `printables/` - the generated, deliberately unbranded PDFs
- `tests/` - unittest suite, no external deps beyond build.py's
- `requirements.txt`, `.gitignore`, MIT `LICENSE`, `README.md`

Distinct from phone-comfort-guide: this pack is the monthly sweep/ritual,
not choosing-and-using advice. Noted in the README so future contributors
keep the split.

## How to run it

```
pip install -r requirements.txt    # only if WeasyPrint is missing
python3 build.py                   # builds all 9 PDFs into printables/
python3 build.py --sheet reward-list
python3 -m unittest discover -s tests -v
```

Zero signups, zero network calls; everything happens locally.

## Verification results

- `python3 build.py`: all 9 sheets build, exit code 0, no warnings.
- `python3 -m unittest discover -s tests`: 7/7 tests pass.
  - every sheet renders a valid, non-truncated `%PDF` (header + %%EOF + size
    sanity), page counts as listed above
  - CLI end-to-end build produces exactly the 9 expected PDFs
  - single-sheet `--sheet` filter works
  - every sheet contains its Pacing note
  - "unbranded" check passes (no Asdale/LLC/name strings in sheet HTML)
  - shared stylesheet present and print-defined
- Visual spot-check via `pdftoppm` previews (storage, notifications,
  subscription, reward sheets): layout, checkboxes, write-in lines, tables,
  and meter render correctly on Letter.

## Known gaps / possible next steps

- Page setup is US Letter only; A4 means editing one line in
  `sheets/style.css` (documented in README).
- Pacing notes are per sheet, not per section; a future version could add
  mid-sheet breathing points.
- No fill-in-preserved interactive PDF form fields (by design: these are
  meant to be printed and scribbled on).
- App-store subscription-table suggestion counts are deliberately generic so
  the sheets stay unbranded and evergreen.
- Not yet wired into dylanasdale.github.io; it is a standalone local-first
  pack ready to be linked from there.
