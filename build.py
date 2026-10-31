#!/usr/bin/env python3
"""Build the Phone Reset Day Pack printables.

Renders every HTML sheet in sheets/ to an unbranded PDF in printables/ using
WeasyPrint, entirely offline and local.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "sheets"
DEFAULT_OUT = ROOT / "printables"


def discover_sheets():
    return sorted(SHEETS_DIR.glob("*.html"))


def render_sheet(path):
    from weasyprint import HTML

    return HTML(filename=str(path)).render()


def pdf_bytes_are_valid(data):
    return (
        data.startswith(b"%PDF-")
        and b"%%EOF" in data[-256:]
        and len(data) > 2000
    )


def build_sheet(path, out_dir):
    doc = render_sheet(path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{path.stem}.pdf"
    doc.write_pdf(str(target))
    page_count = len(doc.pages)
    return page_count, target


def build_all(out_dir=None, only=None, quiet=False):
    out_dir = Path(out_dir) if out_dir else DEFAULT_OUT
    sheets = discover_sheets()
    if only:
        wanted = {name.removeprefix("sheets/").removesuffix(".html") for name in only}
        sheets = [s for s in sheets if s.stem in wanted]
    if not quiet:
        print(f"Phone Reset Day Pack: building {len(sheets)} sheet(s) -> {out_dir}")
    results = []
    failures = []
    for sheet in sheets:
        try:
            pages, target = build_sheet(sheet, out_dir)
            results.append((sheet.stem, pages, target))
            if not quiet:
                word = "page" if pages == 1 else "pages"
                print(f"  built {target.name} ({pages} {word})")
        except Exception as exc:
            failures.append((sheet, exc))
            if not quiet:
                print(f"  FAILED {sheet.name}: {exc}", file=sys.stderr)
    return results, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the Phone Reset Day Pack PDFs.")
    parser.add_argument(
        "--out",
        default=None,
        help=f"output directory (default: {DEFAULT_OUT.relative_to(ROOT)})",
    )
    parser.add_argument(
        "--sheet",
        action="append",
        default=[],
        help="build only these sheet names (repeatable, e.g. storage-sweep-checklist)",
    )
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    args = parser.parse_args(argv)

    results, failures = build_all(args.out, only=args.sheet or None, quiet=args.quiet)
    if failures:
        print(f"{len(failures)} sheet(s) failed.", file=sys.stderr)
        return 1
    if not results:
        print("No sheets matched. Sheets live in sheets/*.html", file=sys.stderr)
        return 1
    if not args.quiet:
        print("All done. Your printables are ready to print.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
