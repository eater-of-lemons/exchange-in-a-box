from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_docs import (
    broken_local_links,
    missing_roadmap_phases,
    uppercase_violations,
)


class LowercaseStyleTests(unittest.TestCase):
    def test_accepts_lowercase_prose_and_required_technical_casing(self) -> None:
        text = (
            "# docs\n\n"
            "C++ uses GTC and IOC orders with unique IDs on Linux.\n"
            "see [`ROADMAP.md`](ROADMAP.md).\n"
        )

        self.assertEqual(uppercase_violations(text), [])

    def test_rejects_unexpected_uppercase_prose(self) -> None:
        violations = uppercase_violations("# Docs\n\nThis should be lowercase.\n")

        self.assertEqual(violations, [(1, "# Docs"), (3, "This should be lowercase.")])

    def test_ignores_code_blocks_inline_code_and_link_destinations(self) -> None:
        text = (
            "read `TypeName` in the docs.\n"
            "[repository](https://GitHub.com/Example/Project)\n"
            "```C++\n"
            "class MatchingEngine {};\n"
            "```\n"
        )

        self.assertEqual(uppercase_violations(text), [])


class MarkdownLinkTests(unittest.TestCase):
    def test_accepts_existing_local_file_and_heading_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "ROADMAP.md"
            target.write_text("# roadmap\n", encoding="utf-8")
            document = root / "README.md"
            document.write_text(
                "[roadmap](ROADMAP.md)\n[section](#section)\n",
                encoding="utf-8",
            )

            self.assertEqual(broken_local_links(document, root), [])

    def test_reports_missing_file_and_repository_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "README.md"
            document.write_text(
                "[missing](MISSING.md)\n[outside](../outside.md)\n",
                encoding="utf-8",
            )

            self.assertEqual(
                broken_local_links(document, root),
                ["MISSING.md", "../outside.md (escapes repository root)"],
            )


class RoadmapStructureTests(unittest.TestCase):
    def test_accepts_all_phases(self) -> None:
        roadmap = "\n".join(f"## phase {phase} — work" for phase in range(9))

        self.assertEqual(missing_roadmap_phases(roadmap), [])

    def test_reports_missing_phases(self) -> None:
        roadmap = "## phase 0 — start\n## phase 8 — finish\n"

        self.assertEqual(missing_roadmap_phases(roadmap), list(range(1, 8)))


if __name__ == "__main__":
    unittest.main()
