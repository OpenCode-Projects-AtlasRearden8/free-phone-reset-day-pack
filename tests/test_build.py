import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build

EXPECTED_SHEETS = [
    "app-purge-decision-card",
    "backup-happiness-check",
    "camera-roll-album-rules",
    "contacts-tidy-split",
    "duplicate-photo-triage",
    "notification-trims-one-pager",
    "reward-list",
    "storage-sweep-checklist",
    "subscription-hunt-sheet",
]


def read_pdf(path):
    data = path.read_bytes()
    assert data.startswith(b"%PDF-"), f"{path.name} lacks %PDF header"
    assert b"%%EOF" in data[-256:], f"{path.name} is truncated"
    assert len(data) > 2000, f"{path.name} is implausibly small"
    return data


class TestSheets(unittest.TestCase):
    def test_all_nine_sheets_exist(self):
        self.assertEqual([s.stem for s in build.discover_sheets()], EXPECTED_SHEETS)

    def test_every_sheet_renders_a_valid_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            results, failures = build.build_all(out, quiet=True)
            self.assertEqual(failures, [])
            self.assertEqual(len(results), 9)
            for sheet_name, pages, target in results:
                with self.subTest(sheet=sheet_name):
                    self.assertGreaterEqual(pages, 1)
                    self.assertEqual(target.name, f"{sheet_name}.pdf")
                    read_pdf(target)

    def test_cli_builds_every_sheet(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "build.py"), "--out", tmp],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            pdfs = sorted(Path(tmp).glob("*.pdf"))
            self.assertEqual([p.stem for p in pdfs], EXPECTED_SHEETS)
            for pdf in pdfs:
                read_pdf(pdf)

    def test_cli_single_sheet_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "build.py"),
                    "--out",
                    tmp,
                    "--sheet",
                    "reward-list",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertEqual([p.stem for p in Path(tmp).glob("*.pdf")], ["reward-list"])

    def test_sheets_have_friendly_pacing_notes(self):
        for sheet in build.discover_sheets():
            with self.subTest(sheet=sheet.stem):
                html = sheet.read_text(encoding="utf-8")
                self.assertIn('class="pacing"', html)
                self.assertIn("Pacing", html)

    def test_pdfs_are_unbranded(self):
        for sheet in build.discover_sheets():
            html = sheet.read_text(encoding="utf-8").lower()
            with self.subTest(sheet=sheet.stem):
                for brand in ("asdale", "dylan", "llc", "massive ai manual"):
                    self.assertNotIn(brand, html)

    def test_shared_stylesheet_exists(self):
        css = ROOT / "sheets" / "style.css"
        self.assertTrue(css.exists())
        self.assertIn("@page", css.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
