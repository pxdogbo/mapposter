# Map Poster – Commands & Themes Reference

Quick reference for all CLI options and available themes.

---

## Commands (CLI Options)

### Required

| Option | Short | Description |
|--------|-------|-------------|
| `--city` | `-c` | City name (for geocoding) |
| `--country` | `-C` | Country name (for geocoding) |

### Optional

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--latitude` | `-lat` | Override center latitude (use with `--longitude`) | — |
| `--longitude` | `-long` | Override center longitude (use with `--latitude`) | — |
| `--country-label` | — | Override country text on poster | — |
| `--theme` | `-t` | Theme name | `terracotta` |
| `--distance` | `-d` | Map radius in meters | `18000` |
| `--width` | `-W` | Image width in inches | `12` (max 20) |
| `--height` | `-H` | Image height in inches | `16` (max 20) |
| `--list-themes` | — | List all themes | — |
| `--all-themes` | — | Generate one poster per theme | — |
| `--display-city` | `-dc` | Custom city label (e.g. "東京") | — |
| `--display-country` | `-dC` | Custom country label (e.g. "日本") | — |
| `--font-family` | — | Font: Google Fonts name or `Telegraf` (local) | Roboto/local |
| `--format` | `-f` | Output format: `png`, `svg`, or `pdf` | `png` |
| `--replicate` | `-r` | Post-process through Replicate AI (e.g. dream.district) | — |
| `--replicate-model` | — | Replicate model ID (with version) | `pxdogbo/dream.district:snedjsxd2xrmr0cwb3hag5kkxw` |
| `--replicate-prompt` | — | Prompt for AI model | default map poster description |
| `--replicate-schema` | — | Print model input schema (to check param names) | — |

### Run (pip/venv)

```bash
source .venv/bin/activate   # or: .venv\Scripts\activate on Windows
python create_map_poster.py -c "<city>" -C "<country>" [options]
```

### Run (uv)

```bash
uv run ./create_map_poster.py -c "<city>" -C "<country>" [options]
```

---

## Distance guide

| Distance (m) | Use case |
|--------------|----------|
| 4000–6000 | Small/dense areas (Venice, Amsterdam center) |
| 8000–12000 | Medium cities, downtown (Paris, Barcelona) |
| 15000–20000 | Large metros, full city (Tokyo, Mumbai) |

---

## Resolution (300 DPI)

| Target | Resolution (px) | Inches (`-W` / `-H`) |
|--------|------------------|------------------------|
| Instagram post | 1080 × 1080 | 3.6 × 3.6 |
| Mobile wallpaper | 1080 × 1920 | 3.6 × 6.4 |
| HD wallpaper | 1920 × 1080 | 6.4 × 3.6 |
| 4K wallpaper | 3840 × 2160 | 12.8 × 7.2 |
| A4 print | 2480 × 3508 | 8.3 × 11.7 |

---

## Themes (styles)

| Theme name | Display name | Description |
|------------|--------------|-------------|
| `autumn` | Autumn | Burnt oranges, deep reds, golden yellows – seasonal warmth |
| `blueprint` | Blueprint | Architectural blueprint – technical drawing look |
| `contrast_zones` | Contrast Zones | Strong contrast, urban density – darker center, lighter edges |
| `copper_patina` | Copper Patina | Oxidized copper – teal-green patina and copper accents |
| `dice_ai` | Dice AI | Dark indigo, purple gradient, lavender (custom app palette) |
| `dice_ai_2` | Dice AI 2 | UI/tray palette – tray gradients, header lavender, persona purple |
| `emerald` | Emerald City | Dark green with mint accents |
| `forest` | Forest | Deep greens and sage – botanical look |
| `gradient_roads` | Gradient Roads | Smooth gradient, dark center to light edges |
| `japanese_ink` | Japanese Ink | Ink wash style – minimal with subtle red accent |
| `midnight_blue` | Midnight Blue | Deep navy, gold/copper roads – atlas style |
| `monochrome_blue` | Monochrome Blue | Single blue family, varied saturation |
| `neon_amber` | Neon Amber | Dark with yellow/orange neon – warm night city |
| `neon_green` | Neon Green | Dark with green neon – cool night city |
| `neon_purple_green` | Neon Purple Green | Dark like Medellín, neon purple main lines, green secondary |
| `neon_purple_green_alt` | Neon Purple Green Alt | Dark like Medellín, brighter neon purple main, mint green secondary |
| `neon_cyberpunk` | Neon Cyberpunk | Dark with electric pink/cyan – night city |
| `noir` | Noir | Black background, white/gray roads – gallery style |
| `ocean` | Ocean | Blues and teals – coastal cities |
| `pastel_dream` | Pastel Dream | Soft pastels, dusty blues and mauves |
| `sunset` | Sunset | Warm oranges and pinks on peach – golden hour |
| `terracotta` | Terracotta | Mediterranean – burnt orange and clay on cream |
| `warm_beige` | Warm Beige | Warm neutrals, sepia – vintage map |

---

## Your city posters

Commands to regenerate your main posters (Telegraf font, same style as the ones you made):

```bash
# Medellín – Dice AI (purple)
python create_map_poster.py -c "Medellín" -C "Colombia" -t dice_ai --font-family Telegraf -d 12000

# Medellín – Dice AI 2 (UI/tray palette)
python create_map_poster.py -c "Medellín" -C "Colombia" -t dice_ai_2 --font-family Telegraf -d 12000

# Medellín – neon purple main + green secondary (2 variants)
python create_map_poster.py -c "Medellín" -C "Colombia" -t neon_purple_green --font-family Telegraf -d 12000
python create_map_poster.py -c "Medellín" -C "Colombia" -t neon_purple_green_alt --font-family Telegraf -d 12000

# Cartagena – neon amber (yellow/orange)
python create_map_poster.py -c "Cartagena" -C "Colombia" -t neon_amber --font-family Telegraf -d 8000

# Rio – neon green
python create_map_poster.py -c "Rio de Janeiro" -C "Brazil" -t neon_green --font-family Telegraf -d 14000

# Rio – neon amber (yellow/orange)
python create_map_poster.py -c "Rio de Janeiro" -C "Brazil" -t neon_amber --font-family Telegraf -d 14000
```

---

## Example commands

```bash
# Basic
python create_map_poster.py -c "Paris" -C "France"

# Theme + distance
python create_map_poster.py -c "New York" -C "USA" -t noir -d 12000

# Override center
python create_map_poster.py -c "New York" -C "USA" -lat 40.776676 -long -73.971321 -t noir

# i18n (e.g. Japanese)
python create_map_poster.py -c "Tokyo" -C "Japan" -dc "東京" -dC "日本" --font-family "Noto Sans JP" -t japanese_ink

# List themes
python create_map_poster.py --list-themes

# All themes for one city
python create_map_poster.py -c "Tokyo" -C "Japan" --all-themes

# Output format
python create_map_poster.py -c "Paris" -C "France" -f svg

# Replicate AI styling (requires REPLICATE_API_TOKEN, PNG output)
python create_map_poster.py -c "Medellín" -C "Colombia" -t dice_ai --font-family Telegraf -r

# Check Replicate model inputs (e.g. if param names differ)
python create_map_poster.py --replicate-schema
```

---

## Output

- **Directory:** `posters/`
- **Filename:** `{city}_{theme}_{YYYYMMDD_HHMMSS}.{png|svg|pdf}`  
  Example: `medellín_dice_ai_20260213_041507.png`

---

## Custom theme (JSON)

Add a `.json` file under `themes/` with:

```json
{
  "name": "My Theme",
  "description": "Short description",
  "bg": "#FFFFFF",
  "text": "#000000",
  "gradient_color": "#FFFFFF",
  "water": "#C0C0C0",
  "parks": "#F0F0F0",
  "road_motorway": "#0A0A0A",
  "road_primary": "#1A1A1A",
  "road_secondary": "#2A2A2A",
  "road_tertiary": "#3A3A3A",
  "road_residential": "#4A4A4A",
  "road_default": "#3A3A3A"
}
```

Use it with: `-t my_theme` (filename without `.json`).
