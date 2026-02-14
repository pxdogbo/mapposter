#!/usr/bin/env python3
"""
Add an 80px border to each poster using the theme's text color.
Creates new files with _bordered before .png (e.g. poster_bordered.png).
"""

import json
import os
import re
from pathlib import Path

from PIL import Image

POSTERS_DIR = Path("posters")
THEMES_DIR = Path("themes")
BORDER_PX = 80


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert #RRGGBB to (r, g, b)."""
    hex_str = hex_str.lstrip("#")
    return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))


def get_theme_names() -> list[str]:
    """Return theme names (without .json) sorted by length descending for longest match."""
    names = []
    for f in THEMES_DIR.glob("*.json"):
        names.append(f.stem)
    return sorted(names, key=len, reverse=True)


def theme_from_filename(basename: str, theme_names: list[str]) -> str | None:
    """Extract theme name from poster filename: city_theme_YYYYMMDD_HHMMSS."""
    # Remove .png
    base = basename.replace(".png", "").replace(".PNG", "")
    # Remove timestamp suffix _YYYYMMDD_HHMMSS
    m = re.search(r"_\d{8}_\d{6}$", base)
    if not m:
        return None
    base = base[: m.start()]
    for theme in theme_names:
        if base.endswith("_" + theme) or base == theme:
            return theme
    return None


def load_theme_text_color(theme_name: str) -> tuple[int, int, int]:
    """Load theme JSON and return text color as RGB."""
    path = THEMES_DIR / f"{theme_name}.json"
    if not path.exists():
        return (255, 255, 255)  # fallback white
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    hex_color = data.get("text", "#FFFFFF")
    return hex_to_rgb(hex_color)


def add_border(image_path: Path, border_rgb: tuple[int, int, int]) -> Path:
    """Add 4px border around image; save as *_bordered.png. Returns output path."""
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    out_w, out_h = w + 2 * BORDER_PX, h + 2 * BORDER_PX
    out = Image.new("RGB", (out_w, out_h), border_rgb)
    out.paste(img, (BORDER_PX, BORDER_PX))
    stem = image_path.stem
    out_name = f"{stem}_bordered.png"
    out_path = image_path.parent / out_name
    out.save(out_path, "PNG")
    return out_path


def main():
    POSTERS_DIR.mkdir(exist_ok=True)
    theme_names = get_theme_names()

    for path in sorted(POSTERS_DIR.glob("*.png")):
        if "_bordered" in path.stem:
            continue
        basename = path.name
        theme = theme_from_filename(basename, theme_names)
        if theme is None:
            print(f"  Skip (no theme): {basename}")
            continue
        rgb = load_theme_text_color(theme)
        out_path = add_border(path, rgb)
        print(f"  {basename} (theme {theme}, text color) -> {out_path.name}")


if __name__ == "__main__":
    print("Adding 80px border (theme text color) to posters...")
    main()
    print("Done.")
