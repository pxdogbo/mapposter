# Map Poster

TEST CHANGE: Generate minimalist map posters for any city using OpenStreetMap data. Pick a city, choose a theme, and export print-ready images.

## Quick start

```bash
# Install (uv)
uv sync

# Run the theme editor (recommended)
streamlit run streamlit_ui.py
```

In the app you can pick a city, tweak colors, and generate previews or full posters (PNG, 300 DPI).

## Command line

```bash
# Single poster: city, country, theme, radius in meters
python create_map_poster.py -c "Amsterdam" -C "Netherlands" -t ocean -d 6000

# List themes
python create_map_poster.py --list-themes
```

## Optional

- **Fonts**: Place `Telegraf-Regular.otf` and `Telegraf-UltraBold.otf` in `fonts/Telegraf/` for the intended look (see that folder’s README).
- **Replicate styling**: For AI-style post-processing, set `REPLICATE_API_TOKEN` and use `replicate_style.py` (see script docstring).

## License

MIT.
