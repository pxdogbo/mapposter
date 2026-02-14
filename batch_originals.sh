#!/bin/bash
# Batch generate the original map poster set (15 city/theme pairs)
# Run from project root: ./batch_originals.sh

set -e
cd "$(dirname "$0")"

echo "========================================"
echo "Map Poster Originals — Batch Generation"
echo "========================================"
echo ""

# Iconic grid patterns
echo "[1/15] New York — Manhattan grid (noir)"
python create_map_poster.py -c "New York" -C "USA" -t noir -d 12000

echo "[2/15] Barcelona — Eixample district grid (warm_beige)"
python create_map_poster.py -c "Barcelona" -C "Spain" -t warm_beige -d 8000

# Waterfront & canals
echo "[3/15] Venice — Canal network (blueprint)"
python create_map_poster.py -c "Venice" -C "Italy" -t blueprint -d 4000

echo "[4/15] Amsterdam — Concentric canals (ocean)"
python create_map_poster.py -c "Amsterdam" -C "Netherlands" -t ocean -d 6000

echo "[5/15] Dubai — Palm & coastline (midnight_blue)"
python create_map_poster.py -c "Dubai" -C "UAE" -t midnight_blue -d 15000

# Radial patterns
echo "[6/15] Paris — Haussmann boulevards (pastel_dream)"
python create_map_poster.py -c "Paris" -C "France" -t pastel_dream -d 10000

echo "[7/15] Moscow — Ring roads (noir)"
python create_map_poster.py -c "Moscow" -C "Russia" -t noir -d 12000

# Organic old cities
echo "[8/15] Tokyo — Dense organic streets (japanese_ink)"
python create_map_poster.py -c "Tokyo" -C "Japan" -t japanese_ink -d 15000

echo "[9/15] Marrakech — Medina maze (neon_amber)"
python create_map_poster.py -c "Marrakech" -C "Morocco" -t neon_amber -d 5000

echo "[10/15] Rome — Ancient street layout (warm_beige)"
python create_map_poster.py -c "Rome" -C "Italy" -t warm_beige -d 8000

# Coastal cities
echo "[11/15] San Francisco — Peninsula grid (sunset)"
python create_map_poster.py -c "San Francisco" -C "USA" -t sunset -d 10000

echo "[12/15] Sydney — Harbor city (ocean)"
python create_map_poster.py -c "Sydney" -C "Australia" -t ocean -d 12000

echo "[13/15] Mumbai — Coastal peninsula (contrast_zones)"
python create_map_poster.py -c "Mumbai" -C "India" -t contrast_zones -d 18000

# River cities
echo "[14/15] London — Thames curves (noir)"
python create_map_poster.py -c "London" -C "UK" -t noir -d 15000

echo "[15/15] Budapest — Danube split (copper_patina)"
python create_map_poster.py -c "Budapest" -C "Hungary" -t copper_patina -d 8000

echo ""
echo "========================================"
echo "✓ Batch complete — 15 originals generated"
echo "========================================"
