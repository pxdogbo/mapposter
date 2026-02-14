#!/bin/bash
# Batch generate Medellín, Cartagena, Rio de Janeiro (first South America batch)
# Run from project root: ./batch_colombia_rio.sh

set -e
cd "$(dirname "$0")"

echo "========================================"
echo "Map Posters — Medellín, Cartagena, Rio"
echo "========================================"
echo ""

echo "[1/3] Medellín — Valley city (neon_purple_green_alt)"
uv run python create_map_poster.py -c "Medellín" -C "Colombia" -t neon_purple_green_alt -d 8000 --font-family Telegraf

echo "[2/3] Cartagena — Walled city (multicolor_cartagena)"
uv run python create_map_poster.py -c "Cartagena" -C "Colombia" -t multicolor_cartagena -d 6000 --font-family Telegraf

echo "[3/3] Rio de Janeiro — Coastal city (neon_amber_blue_water)"
uv run python create_map_poster.py -c "Rio de Janeiro" -C "Brazil" -t neon_amber_blue_water -d 12000 --font-family Telegraf

echo ""
echo "========================================"
echo "✓ Batch complete — 3 posters generated"
echo "========================================"
