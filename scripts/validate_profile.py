#!/usr/bin/env python3
"""Validate the profile README, theme gallery and generated SVG cards."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GALLERY = ROOT / "profile-summary-card-output"
CARDS = (
    "0-profile-details.svg",
    "1-repos-per-language.svg",
    "2-most-commit-language.svg",
    "3-stats.svg",
    "4-productive-time.svg",
)
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LOCAL_RAW = re.compile(r"raw\.githubusercontent\.com/master-bry/master-bry/main/([^\s\"')]+)")
THEME_LINK = re.compile(r"\]\(\./([^/)]+)/README\.md\)")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def image_targets(content: str) -> list[tuple[str, str]]:
    return [(alt, target) for alt, target in IMAGE.findall(content)]


def strip_query(target: str) -> str:
    return target.split("?", 1)[0]


def check_svg(path: Path, errors: list[str]) -> None:
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid SVG ({exc})")


def check_theme(theme: Path, errors: list[str]) -> None:
    for card in CARDS:
        path = theme / card
        if not path.is_file():
            errors.append(f"{theme.relative_to(ROOT)}: missing {card}")
        else:
            check_svg(path, errors)

    readme = theme / "README.md"
    if not readme.is_file():
        errors.append(f"{theme.relative_to(ROOT)}: missing README.md")
        return

    content = read(readme)
    targets = [strip_query(target) for _, target in image_targets(content)]
    names = {Path(target).name for target in targets}
    for target in targets:
        if target.startswith("./") and not (theme / target[2:]).is_file():
            errors.append(f"{readme.relative_to(ROOT)}: broken image {target}")

    for card in CARDS:
        if card not in names:
            errors.append(f"{readme.relative_to(ROOT)}: does not showcase {card}")

    for alt, target in image_targets(content):
        if not alt.strip():
            errors.append(f"{readme.relative_to(ROOT)}: empty alt text for {target}")


def check_root_readme(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    content = read(readme)
    for raw_path in LOCAL_RAW.findall(content):
        target = ROOT / strip_query(raw_path)
        if not target.is_file():
            errors.append(f"README.md: broken local asset {raw_path}")

    for alt, target in image_targets(content):
        if not alt.strip():
            errors.append(f"README.md: empty alt text for {target}")


def check_gallery(themes: list[Path], errors: list[str]) -> None:
    gallery_readme = GALLERY / "README.md"
    index = GALLERY / "INDEX.md"
    if not index.is_file():
        errors.append("profile-summary-card-output/INDEX.md: missing theme index")
    gallery_content = read(gallery_readme) if gallery_readme.is_file() else ""
    index_content = read(index) if index.is_file() else ""
    linked = set(THEME_LINK.findall(gallery_content)) | set(THEME_LINK.findall(index_content))

    for theme in themes:
        if theme.name not in linked:
            errors.append(f"{theme.relative_to(ROOT)}: absent from gallery index")


def main() -> int:
    themes = sorted(path for path in GALLERY.iterdir() if path.is_dir())
    errors: list[str] = []

    if not themes:
        errors.append("profile-summary-card-output: no themes found")

    for theme in themes:
        check_theme(theme, errors)

    check_root_readme(errors)
    check_gallery(themes, errors)

    for asset in (ROOT / "assets").glob("*.svg"):
        check_svg(asset, errors)

    if errors:
        print(f"Validation failed with {len(errors)} problem(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(themes)} themes, {len(list(GALLERY.glob('*/*.svg')))} cards and README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
