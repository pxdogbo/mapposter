#!/usr/bin/env python3
"""
Streamlit UI for visually tweaking map poster themes.

Usage:
  streamlit run streamlit_ui.py

The app opens in your browser. From there you can:
- Pick a city from the dropdown (country auto-selects), and set distance (meters)
- Pick an existing theme or start from scratch (terracotta base)
- Adjust colors for each theme key via color pickers
- See live color swatches for the current palette
- Click "Generate preview" for fast feedback (smaller radius, 6x8 in, PNG)
- Click "Generate full poster" for final output (12x16 in, 300 DPI)
- Click "Save theme" to write the current colors to a new JSON file in themes/
"""

import json
import math
import os
import re
import tempfile
from pathlib import Path

import streamlit as st

import create_map_poster
from font_management import load_fonts

# Telegraf: must have Telegraf-Regular.otf and Telegraf-UltraBold.otf in fonts/Telegraf/
TELEGRAF_FONTS = load_fonts("Telegraf")

# OKLCH → hex (for pasting from https://oklch.com)
try:
    import colour
    from colour.notation import RGB_to_HEX

    def oklch_to_hex(l: float, c: float, h_deg: float) -> str:
        """Convert OKLCH (L 0–1, C ~0–0.4, H 0–360°) to sRGB hex."""
        h_rad = math.radians(h_deg)
        a = c * math.cos(h_rad)
        b = c * math.sin(h_rad)
        oklab = [l, a, b]
        xyz = colour.Oklab_to_XYZ(oklab)
        rgb = colour.XYZ_to_sRGB(xyz)
        rgb_clipped = [max(0, min(1, x)) for x in rgb]
        return RGB_to_HEX(rgb_clipped).upper()

    HAS_OKLCH = True
except ImportError:
    HAS_OKLCH = False

    def oklch_to_hex(l: float, c: float, h_deg: float) -> str:
        return "#000000"


def parse_oklch_input(raw: str) -> tuple[float, float, float] | None:
    """
    Parse OKLCH from pasted text. Accepts:
    - 0.726,0.129,253.06,100 (oklch.com URL hash)
    - 0.726 0.129 253.06
    - oklch(0.726 0.129 253.06) or oklch(72.6% 0.129 253.06)
    Returns (L, C, H) with L in 0–1, C as-is, H in 0–360, or None if invalid.
    """
    if not raw or not raw.strip():
        return None
    raw = raw.strip()
    # Strip oklch(...) wrapper
    m = re.match(r"oklch\s*\(\s*(.+?)\s*\)", raw, re.I | re.DOTALL)
    if m:
        raw = m.group(1)
    # Split on comma or space
    parts = re.split(r"[\s,]+", raw.strip())
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) < 3:
        return None
    try:
        l_val = float(parts[0].replace("%", ""))
        if l_val > 1:
            l_val /= 100.0
        c_val = float(parts[1])
        h_val = float(parts[2])
        if not (0 <= l_val <= 1 and 0 <= c_val <= 0.5 and 0 <= h_val <= 360):
            return None
        return (l_val, c_val, h_val)
    except (ValueError, IndexError):
        return None


# Map label text (from pasted palettes) to theme keys (normalize dashes to "-")
def _norm(s: str) -> str:
    return s.strip().lower().replace("\u2013", "-").replace("–", "-").replace("  ", " ")

OKLCH_LABEL_TO_KEY = {
    "background": "bg",
    "text": "text",
    "gradient": "gradient_color",
    "water": "water",
    "parks": "parks",
    "road - motorway": "road_motorway",
    "road - primary": "road_primary",
    "road - secondary": "road_secondary",
    "road - tertiary": "road_tertiary",
    "road - residential": "road_residential",
    "road - default": "road_default",
    "road_motorway": "road_motorway",
    "road_primary": "road_primary",
    "road_secondary": "road_secondary",
    "road_tertiary": "road_tertiary",
    "road_residential": "road_residential",
    "road_default": "road_default",
}


def parse_oklch_palette_block(block: str) -> dict[str, str] | None:
    """
    Parse a block of lines like:
      Background: 0.1852, 0.0551, 282.82
      Text: 0.9295, 0.0339, 293.07
    Returns dict of theme_key -> hex, or None if nothing parsed.
    """
    if not block or not block.strip():
        return None
    result = {}
    for line in block.strip().splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        label, rest = line.split(":", 1)
        label = _norm(label)
        rest = rest.strip()
        parsed = parse_oklch_input(rest)
        if parsed is None:
            continue
        key = OKLCH_LABEL_TO_KEY.get(label)
        if key is None:
            key = OKLCH_LABEL_TO_KEY.get(label.replace("road - ", ""))
        if key and HAS_OKLCH:
            result[key] = oklch_to_hex(*parsed)
    return result if result else None


THEMES_DIR = "themes"
THEME_KEYS = [
    "bg",
    "text",
    "water",
    "parks",
    "gradient_color",
    "road_motorway",
    "road_primary",
    "road_secondary",
    "road_tertiary",
    "road_residential",
    "road_default",
]

DEFAULT_THEME = {
    "name": "Custom",
    "description": "Custom theme created in Streamlit UI",
    "bg": "#F5EDE4",
    "text": "#8B4513",
    "gradient_color": "#F5EDE4",
    "water": "#A8C4C4",
    "parks": "#E8E0D0",
    "road_motorway": "#A0522D",
    "road_primary": "#B8653A",
    "road_secondary": "#C9846A",
    "road_tertiary": "#D9A08A",
    "road_residential": "#E5C4B0",
    "road_default": "#D9A08A",
}


def load_theme_colors(theme_name: str) -> dict:
    """Load theme from file or return default if 'from scratch'."""
    if not theme_name or theme_name == "From scratch":
        return dict(DEFAULT_THEME)
    theme = create_map_poster.load_theme(theme_name)
    return {k: theme.get(k, DEFAULT_THEME.get(k, "#000000")) for k in THEME_KEYS}


def build_full_theme(colors: dict, name: str = "Custom", description: str = "") -> dict:
    """Build a complete theme dict with metadata."""
    return {
        "name": name,
        "description": description or "Custom theme created in Streamlit UI",
        **colors,
    }


# Main colors to show in theme palette preview (compact strip)
PALETTE_KEYS = ["bg", "road_primary", "road_secondary", "water", "parks", "text"]


def theme_palette_html(colors: dict) -> str:
    """HTML for a horizontal strip of color swatches that fill the container."""
    squares = "".join(
        f'<div style="flex:1;min-height:20px;background:{colors.get(k,"#666")};border-radius:3px"></div>'
        for k in PALETTE_KEYS
    )
    return f'<div style="display:flex;gap:2px;width:100%;min-height:20px">{squares}</div>'


def render_color_swatches(colors: dict) -> None:
    """Display live color swatches for the current palette in a grid."""
    st.caption("Current palette")
    grid_cols = st.columns(4)
    for i, (key, hex_val) in enumerate(colors.items()):
        with grid_cols[i % 4]:
            st.markdown(
                f'<div style="display:flex;flex-direction:column;gap:4px;margin-bottom:6px">'
                f'<div style="width:100%;aspect-ratio:1;background:{hex_val};border-radius:4px"></div>'
                f'<span style="font-size:11px">{key}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# Aspect ratio presets: (label, width_inches, height_inches)
ASPECT_RATIOS = [
    ("3:4 (portrait)", 9, 12),
    ("1:1 (square)", 12, 12),
    ("4:3 (landscape)", 12, 9),
    ("16:9 (wide)", 12, 6.75),
    ("9:16 (story)", 6.75, 12),
    ("12:16 (poster)", 12, 16),
]

# Fixed preset for live-updating preview (small so it regenerates quickly)
LIVE_PRESET_CITY = "Amsterdam"
LIVE_PRESET_COUNTRY = "Netherlands"
LIVE_PRESET_DIST = 5000
LIVE_PRESET_W, LIVE_PRESET_H = 5, 6

# City list: (city_name, country) — selecting a city auto-sets the country
CITIES = [
    ("Amsterdam", "Netherlands"),
    ("Barcelona", "Spain"),
    ("Budapest", "Hungary"),
    ("Cartagena", "Colombia"),
    ("Dubai", "UAE"),
    ("London", "UK"),
    ("Marrakech", "Morocco"),
    ("Medellín", "Colombia"),
    ("Moscow", "Russia"),
    ("Mumbai", "India"),
    ("New York", "USA"),
    ("Paris", "France"),
    ("Rio de Janeiro", "Brazil"),
    ("Rome", "Italy"),
    ("San Francisco", "USA"),
    ("Sydney", "Australia"),
    ("Tokyo", "Japan"),
    ("Venice", "Italy"),
]


def save_theme_to_file(theme: dict, filename: str) -> str:
    """Save theme to themes/ directory. Returns path or raises."""
    Path(THEMES_DIR).mkdir(exist_ok=True)
    path = os.path.join(THEMES_DIR, f"{filename}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)
    return path


def delete_theme_from_file(theme_id: str) -> bool:
    """Delete a theme JSON file from themes/ directory. Returns True if deleted."""
    if not theme_id or theme_id == "From scratch":
        return False
    path = Path(THEMES_DIR) / f"{theme_id}.json"
    if path.exists():
        path.unlink()
        return True
    return False


st.set_page_config(page_title="Map Poster Theme Editor", layout="wide")
if not TELEGRAF_FONTS:
    st.warning(
        "**Telegraf font not found.** Add `Telegraf-Regular.otf` and `Telegraf-UltraBold.otf` to `fonts/Telegraf/` "
        "(see README there). Using fallback font for now."
    )
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "generated_caption" not in st.session_state:
    st.session_state.generated_caption = None
if "live_preview_image" not in st.session_state:
    st.session_state.live_preview_image = None
if "last_live_preview_theme" not in st.session_state:
    st.session_state.last_live_preview_theme = None

# Two-column layout: controls left, preview right
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.title("Map Poster")
    st.caption("Theme Editor")

    # --- Location & map params ---
    st.subheader("Location & map")
    city_labels = [f"{c}, {co}" for c, co in CITIES]
    city_idx = st.selectbox(
        "City",
        range(len(CITIES)),
        format_func=lambda i: city_labels[i],
        key="city_select",
    )
    city, country = CITIES[city_idx]
    distance = st.number_input(
        "Distance (meters)",
        min_value=2000,
        max_value=50000,
        value=10000,
        step=1000,
        key="distance",
    )

    # --- Aspect ratio ---
    st.subheader("Aspect ratio")
    ratio_labels = [r[0] for r in ASPECT_RATIOS]
    ratio_choice = st.selectbox(
        "Output size",
        options=ratio_labels,
        key="aspect_ratio",
    )
    chosen_w, chosen_h = next((r[1], r[2]) for r in ASPECT_RATIOS if r[0] == ratio_choice)

    # --- Theme selection (grid with palette previews) ---
    st.subheader("Theme")
    available = ["From scratch"] + create_map_poster.get_available_themes()

    # Theme cards in 3-column grid — click the card to select; delete on saved themes
    theme_cols = st.columns(3)
    for i, theme_id in enumerate(available):
        with theme_cols[i % 3]:
            colors = load_theme_colors(theme_id)
            display_name = "From scratch (terracotta)" if theme_id == "From scratch" else theme_id.replace("_", " ").title()
            is_selected = st.session_state.get("theme_select") == theme_id
            border = "2px solid #1f77b4" if is_selected else "1px solid #ddd"
            st.markdown(
                f'<div style="padding:6px;margin-bottom:4px;border-radius:6px;border:{border};background:transparent">'
                f'{theme_palette_html(colors)}'
                f'</div>',
                unsafe_allow_html=True,
            )
            btn_col1, btn_col2 = st.columns([3, 1])
            with btn_col1:
                if st.button(display_name, key=f"theme_btn_{theme_id}", type="primary" if is_selected else "secondary", use_container_width=True):
                    st.session_state["theme_select"] = theme_id
                    st.rerun()
            if theme_id != "From scratch":
                with btn_col2:
                    if st.button("🗑", key=f"del_{theme_id}", help=f"Delete {display_name}", use_container_width=True):
                        if delete_theme_from_file(theme_id):
                            if st.session_state.get("theme_select") == theme_id:
                                st.session_state["theme_select"] = "From scratch"
                            st.rerun()

    selected_theme = st.session_state.get("theme_select", available[0])
    if selected_theme not in available:
        selected_theme = available[0]
        st.session_state["theme_select"] = selected_theme

    # Initialize session state for colors
    if "theme_colors" not in st.session_state:
        st.session_state.theme_colors = load_theme_colors(selected_theme)

    if st.session_state.get("last_theme") != selected_theme:
        st.session_state.theme_colors = load_theme_colors(selected_theme)
        st.session_state.last_theme = selected_theme
        st.session_state["palette_version"] = st.session_state.get("palette_version", 0) + 1

    # --- Color pickers in grid ---
    st.subheader("Theme colors")
    labels = {
        "bg": "Background",
        "text": "Text",
        "water": "Water",
        "parks": "Parks",
        "gradient_color": "Gradient",
        "road_motorway": "Motorway",
        "road_primary": "Primary",
        "road_secondary": "Secondary",
        "road_tertiary": "Tertiary",
        "road_residential": "Residential",
        "road_default": "Default",
    }

    # Paste OKLCH from https://oklch.com
    with st.expander("Paste OKLCH (from [oklch.com](https://oklch.com))"):
        if HAS_OKLCH:
            with st.expander("Copy this prompt to generate an OKLCH palette (e.g. with an AI)", expanded=False):
                st.caption("Paste the prompt below into an AI or use it as a brief. Then paste the model’s output into the box further down.")
                OKLCH_PROMPT_TEMPLATE = """Create an OKLCH palette for a map poster theme. For each of these 11 roles, output one line in this exact format: Label: L, C, H (Lightness 0–1, Chroma, Hue 0–360°). Use this order and these labels:

Background: L, C, H
Text: L, C, H
Gradient: L, C, H
Water: L, C, H
Parks: L, C, H
Road – motorway: L, C, H
Road – primary: L, C, H
Road – secondary: L, C, H
Road – tertiary: L, C, H
Road – residential: L, C, H
Road – default: L, C, H

Describe the mood or style you want (e.g. dark indigo, warm earth, high contrast). I will paste the output into a map theme editor that accepts OKLCH."""
                st.code(OKLCH_PROMPT_TEMPLATE, language=None)

            st.markdown("**Paste all 11 colors at once** — one line per key, no need to select an element.")
            oklch_placeholder = "\n".join(
                [
                    "Background: L, C, H",
                    "Text: L, C, H",
                    "Gradient: L, C, H",
                    "Water: L, C, H",
                    "Parks: L, C, H",
                    "Road – motorway: L, C, H",
                    "Road – primary: L, C, H",
                    "Road – secondary: L, C, H",
                    "Road – tertiary: L, C, H",
                    "Road – residential: L, C, H",
                    "Road – default: L, C, H",
                ]
            )
            oklch_palette_raw = st.text_area(
                "Paste your full palette here (one line per color)",
                placeholder=oklch_placeholder,
                key="oklch_palette_input",
                height=140,
                label_visibility="collapsed",
            )
            if st.button("Apply full palette", key="oklch_apply_all", type="primary"):
                applied = parse_oklch_palette_block(oklch_palette_raw)
                if applied:
                    for k, hex_val in applied.items():
                        st.session_state.theme_colors[k] = hex_val
                    # Force color pickers to re-initialize with new colors (they'd otherwise keep old state and overwrite)
                    st.session_state["palette_version"] = st.session_state.get("palette_version", 0) + 1
                    st.success(f"Applied {len(applied)} colors. No need to select anything — each line sets its own key.")
                    st.rerun()
                else:
                    st.error("Could not parse. Paste lines like: Background: 0.18, 0.05, 282.82")

            with st.expander("Or paste one color and apply to a single key"):
                oklch_raw = st.text_input(
                    "Single OKLCH value",
                    placeholder="e.g. 0.726, 0.129, 253.06",
                    key="oklch_input",
                )
                oklch_apply_key = st.selectbox(
                    "Apply to",
                    options=THEME_KEYS,
                    format_func=lambda k: labels.get(k, k),
                    key="oklch_apply_key",
                )
                if st.button("Apply OKLCH", key="oklch_apply"):
                    parsed = parse_oklch_input(oklch_raw)
                    if parsed is not None:
                        hex_val = oklch_to_hex(*parsed)
                        st.session_state.theme_colors[oklch_apply_key] = hex_val
                        st.success(f"Set {oklch_apply_key} to {hex_val}")
                        st.rerun()
                    else:
                        st.error("Could not parse OKLCH. Use: L, C, H (e.g. 0.726, 0.129, 253.06)")
        else:
            st.caption(
                "OKLCH needs the **colour** package. Install with the same Python that runs Streamlit, then restart:  \n"
                "`python3.11 -m pip install colour-science`  \n"
                "(If your Streamlit is under Python 3.11, use `python3.11`; otherwise use `python` or `python3`.)"
            )

    # Include palette_version so pickers re-init after "Apply full palette" (otherwise they overwrite with stale state)
    picker_key_suffix = st.session_state.get("palette_version", 0)
    picker_cols = st.columns(4)
    for i, key in enumerate(THEME_KEYS):
        with picker_cols[i % 4]:
            val = st.color_picker(
                labels.get(key, key),
                value=st.session_state.theme_colors.get(key, "#000000"),
                key=f"picker_{selected_theme}_{key}_{picker_key_suffix}",
            )
            st.session_state.theme_colors[key] = val

    render_color_swatches(st.session_state.theme_colors)

    # --- Actions ---
    st.subheader("Generate")
    add_border = st.checkbox(
        "Add border (uses theme text color)",
        value=True,
        key="add_border",
    )
    theme = build_full_theme(st.session_state.theme_colors)
    create_map_poster.THEME.clear()
    create_map_poster.THEME.update(theme)

    # Live preset map: regenerate when theme colors change (one fixed map, updates in real time)
    current_theme_key = tuple(sorted(st.session_state.theme_colors.items()))
    if current_theme_key != st.session_state.get("last_live_preview_theme"):
        try:
            coords = create_map_poster.get_coordinates(LIVE_PRESET_CITY, LIVE_PRESET_COUNTRY)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            with st.spinner("Updating live preview..."):
                create_map_poster.create_poster(
                    LIVE_PRESET_CITY,
                    LIVE_PRESET_COUNTRY,
                    coords,
                    LIVE_PRESET_DIST,
                    tmp_path,
                    "png",
                    width=LIVE_PRESET_W,
                    height=LIVE_PRESET_H,
                    fonts=TELEGRAF_FONTS or create_map_poster.FONTS,
                    pad_inches=0,
                    letter_spacing=20,
                )
            if add_border:
                create_map_poster.add_border_to_image(tmp_path, theme["text"], border_px=20)
            with open(tmp_path, "rb") as f:
                st.session_state.live_preview_image = f.read()
            os.unlink(tmp_path)
            st.session_state.last_live_preview_theme = current_theme_key
        except Exception as e:
            # Don't block the UI; live preview will retry next run
            st.session_state.last_live_preview_theme = current_theme_key

    if st.button("Generate preview", type="primary"):
        preview_dist = int(distance * 0.5)
        preview_w = chosen_w * 0.5
        preview_h = chosen_h * 0.5
        try:
            coords = create_map_poster.get_coordinates(city, country)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            with st.spinner("Generating..."):
                create_map_poster.create_poster(
                    city,
                    country,
                    coords,
                    preview_dist,
                    tmp_path,
                    "png",
                    width=preview_w,
                    height=preview_h,
                    fonts=TELEGRAF_FONTS or create_map_poster.FONTS,
                    pad_inches=0,
                    letter_spacing=20,
                )
            if add_border:
                create_map_poster.add_border_to_image(tmp_path, theme["text"], border_px=20)
            with open(tmp_path, "rb") as f:
                st.session_state.generated_image = f.read()
            st.session_state.generated_caption = f"Preview · {city}, {country}"
            os.unlink(tmp_path)
        except Exception as e:
            st.error(str(e))

    if st.button("Generate full poster"):
        try:
            coords = create_map_poster.get_coordinates(city, country)
            output_file = create_map_poster.generate_output_filename(
                city, "custom", "png", subdir="streamlit"
            )
            with st.spinner("Generating..."):
                create_map_poster.create_poster(
                    city,
                    country,
                    coords,
                    distance,
                    output_file,
                    "png",
                    width=chosen_w,
                    height=chosen_h,
                    fonts=TELEGRAF_FONTS or create_map_poster.FONTS,
                    pad_inches=0,
                    letter_spacing=20,
                )
            if add_border:
                create_map_poster.add_border_to_image(output_file, theme["text"], border_px=20)
            with open(output_file, "rb") as f:
                st.session_state.generated_image = f.read()
            st.session_state.generated_caption = f"Saved: {output_file}"
        except Exception as e:
            st.error(str(e))

    st.divider()
    st.subheader("Save palette")
    if selected_theme != "From scratch":
        if st.button("Update current theme", type="primary", key="update_theme_btn"):
            full_theme = build_full_theme(
                st.session_state.theme_colors,
                name=selected_theme.replace("_", " ").title(),
                description=f"Saved from Streamlit UI - {selected_theme}",
            )
            try:
                path = save_theme_to_file(full_theme, selected_theme)
                st.success(f"Updated **{selected_theme.replace('_', ' ').title()}**")
                st.rerun()
            except Exception as e:
                st.error(f"Update failed: {e}")
        st.caption("Or save as a new palette below.")
    theme_name = st.text_input("Save as new palette", value="my_theme", key="save_name")
    if st.button("Save as new"):
        full_theme = build_full_theme(
            st.session_state.theme_colors,
            name=theme_name.replace("_", " ").title(),
            description=f"Saved from Streamlit UI - {theme_name}",
        )
        try:
            path = save_theme_to_file(full_theme, theme_name)
            st.success(f"Theme **{theme_name}** saved to `{path}`")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

with col_right:
    st.subheader("Preview")
    # Live preset map — updates automatically when you change colors
    if st.session_state.live_preview_image:
        st.caption(f"**Live** · {LIVE_PRESET_CITY}, {LIVE_PRESET_COUNTRY} ({LIVE_PRESET_DIST//1000} km) — updates as you pick colors")
        st.image(
            st.session_state.live_preview_image,
            use_container_width=True,
        )
    else:
        st.info("Loading live preview… (preset map will update as you change colors)")

    # Last result from "Generate preview" / "Generate full poster"
    if st.session_state.generated_image:
        st.divider()
        st.caption("**Last generated**")
        st.image(
            st.session_state.generated_image,
            caption=st.session_state.generated_caption,
            use_container_width=True,
        )
