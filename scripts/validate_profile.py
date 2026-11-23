#!/usr/bin/env python3
"""Validate the profile README and the SVG cards it actually uses."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GALLERY = ROOT / "profile-summary-card-output"
ASSETS = ROOT / "assets"

# Only the theme referenced by the root README must be complete.
USED_THEME = "tokyonight"
USED_CARDS = (
    "0-profile-details.svg",
    "1-repos-per-language.svg",
    "2-most-commit-language.svg",
    "3-stats.svg",
)

IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LOCAL_RAW = re.compile(
    r"raw\.githubusercontent\.com/master-bry/master-bry/main/([^\s\"')]+)"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_query(target: str) -> str:
    return target.split("?", 1)[0]


def check_svg(path: Path, errors: list[str]) -> None:
    """Report an error if the file is not well-formed XML."""
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid SVG ({exc})")


def check_used_theme(errors: list[str]) -> None:
    """The theme used by README.md must contain every card it references."""
    theme = GALLERY / USED_THEME
    if not theme.is_dir():
        errors.append(f"{theme.relative_to(ROOT)}: theme folder missing")
        return
    for card in USED_CARDS:
        if not (theme / card).is_file():
            errors.append(f"{theme.relative_to(ROOT)}: missing {card}")


def check_root_readme(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        errors.append("README.md: file missing")
        return

    content = read(readme)

    # Every image served from this repo must exist in the working tree.
    for raw_path in LOCAL_RAW.findall(content):
        target = ROOT / strip_query(raw_path)
        if not target.is_file():
            errors.append(f"README.md: broken local asset {raw_path}")

    # Markdown images need non-empty alt text.
    for alt, target in IMAGE.findall(content):
        if not alt.strip():
            errors.append(f"README.md: empty alt text for {target}")


def check_all_svgs(errors: list[str]) -> None:
    """Parse every SVG that exists; generated files may change daily."""
    svgs = list(ASSETS.glob("*.svg")) if ASSETS.is_dir() else []
    if GALLERY.is_dir():
        svgs += list(GALLERY.glob("*/*.svg"))
    for svg in svgs:
        check_svg(svg, errors)


def main() -> int:
    errors: list[str] = []

    check_used_theme(errors)
    check_root_readme(errors)
    check_all_svgs(errors)

    if errors:
        print(f"Validation failed with {len(errors)} problem(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    card_count = len(list(GALLERY.glob("*/*.svg"))) if GALLERY.is_dir() else 0
    print(f"Validated README.md, assets/ and {card_count} generated cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
