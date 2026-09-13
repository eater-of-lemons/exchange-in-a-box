#!/usr/bin/env python3
"""validate repository documentation without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCS = ("README.md", "ROADMAP.md", "LEARNING.md")
REQUIRED_PHASES = range(9)

FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LINK_DESTINATION = re.compile(r"(\]\()[^)]*(\))")

# these forms contain uppercase letters by design. all-uppercase abbreviations of
# two or more characters are accepted separately below.
PRESERVED_CASE = (
    r"AddressSanitizer",
    r"UndefinedBehaviorSanitizer",
    r"GitHub Actions",
    r"GitHub",
    r"ROADMAP\.md",
    r"LEARNING\.md",
    r"README\.md",
    r"INVARIANTS\.md",
    r"SPEC\.md",
    r"C\+\+20",
    r"C\+\+",
    r"CMake",
    r"Linux",
    r"macOS",
    r"Python",
    r"Clang",
    r"GCC",
    r"IDs?",
    r"I/O",
    r"O\(1\)",
)
ALL_CAPS_ABBREVIATION = re.compile(r"\b[A-Z][A-Z0-9]{1,}(?:/[A-Z0-9]+)*\b")


def _mask_fenced_code(text: str) -> str:
    """remove fenced code while preserving line numbers."""

    return FENCED_CODE.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def uppercase_violations(text: str) -> list[tuple[int, str]]:
    """return prose lines containing uppercase text that is not exempt."""

    scrubbed = _mask_fenced_code(text)
    scrubbed = INLINE_CODE.sub("", scrubbed)
    scrubbed = LINK_DESTINATION.sub(r"\1\2", scrubbed)

    for pattern in PRESERVED_CASE:
        scrubbed = re.sub(pattern, "", scrubbed)
    scrubbed = ALL_CAPS_ABBREVIATION.sub("", scrubbed)

    return [
        (line_number, line.strip())
        for line_number, line in enumerate(scrubbed.splitlines(), start=1)
        if re.search(r"[A-Z]", line)
    ]


def markdown_targets(text: str) -> list[str]:
    """extract markdown link and image destinations."""

    targets: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1 : raw.index(">")]
        else:
            # ignore an optional quoted link title.
            raw = raw.split(maxsplit=1)[0]
        targets.append(raw)
    return targets


def broken_local_links(document: Path, root: Path = ROOT) -> list[str]:
    """return local markdown links that do not resolve."""

    broken: list[str] = []
    for target in markdown_targets(document.read_text(encoding="utf-8")):
        parsed = urlparse(target)
        if parsed.scheme or parsed.netloc or target.startswith("#"):
            continue

        relative_path = unquote(parsed.path)
        if not relative_path:
            continue

        destination = (document.parent / relative_path).resolve()
        try:
            destination.relative_to(root.resolve())
        except ValueError:
            broken.append(f"{target} (escapes repository root)")
            continue

        if not destination.exists():
            broken.append(target)
    return broken


def missing_roadmap_phases(text: str) -> list[int]:
    """return expected roadmap phases that are absent."""

    return [
        phase
        for phase in REQUIRED_PHASES
        if not re.search(rf"^## phase {phase}\b", text, flags=re.MULTILINE)
    ]


def validate(root: Path = ROOT) -> list[str]:
    """run all documentation checks and return human-readable errors."""

    errors: list[str] = []
    documents: list[Path] = []

    for filename in REQUIRED_DOCS:
        document = root / filename
        if not document.is_file():
            errors.append(f"missing required document: {filename}")
        else:
            documents.append(document)

    for document in documents:
        relative = document.relative_to(root)

        for line_number, line in uppercase_violations(
            document.read_text(encoding="utf-8")
        ):
            errors.append(
                f"{relative}:{line_number}: unexpected uppercase prose: {line}"
            )

        for target in broken_local_links(document, root):
            errors.append(f"{relative}: broken local link: {target}")

    roadmap = root / "ROADMAP.md"
    if roadmap.is_file():
        missing = missing_roadmap_phases(roadmap.read_text(encoding="utf-8"))
        if missing:
            errors.append(
                "ROADMAP.md: missing phases: " + ", ".join(map(str, missing))
            )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("docs check failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("docs check passed:")
    print(f"  - required files: {', '.join(REQUIRED_DOCS)}")
    print("  - local markdown links resolve")
    print("  - roadmap phases 0–8 are present")
    print("  - prose follows the lowercase style")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
