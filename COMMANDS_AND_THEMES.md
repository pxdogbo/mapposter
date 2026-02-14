# Map Poster Originals — Commands and Themes

Reference for the original city/theme/distance combinations that showcase iconic urban patterns.

## Iconic grid patterns

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| New York | USA | noir | 12000 | Manhattan grid |
| Barcelona | Spain | warm_beige | 8000 | Eixample district grid |

## Waterfront & canals

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| Venice | Italy | blueprint | 4000 | Canal network |
| Amsterdam | Netherlands | ocean | 6000 | Concentric canals |
| Dubai | UAE | midnight_blue | 15000 | Palm & coastline |

## Radial patterns

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| Paris | France | pastel_dream | 10000 | Haussmann boulevards |
| Moscow | Russia | noir | 12000 | Ring roads |

## Organic old cities

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| Tokyo | Japan | japanese_ink | 15000 | Dense organic streets |
| Marrakech | Morocco | neon_amber | 5000 | Medina maze |
| Rome | Italy | warm_beige | 8000 | Ancient street layout |

## Coastal cities

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| San Francisco | USA | sunset | 10000 | Peninsula grid |
| Sydney | Australia | ocean | 12000 | Harbor city |
| Mumbai | India | contrast_zones | 18000 | Coastal peninsula |

## River cities

| City | Country | Theme | Distance | Notes |
|------|---------|-------|----------|-------|
| London | UK | noir | 15000 | Thames curves |
| Budapest | Hungary | copper_patina | 8000 | Danube split |

---

## Batch commands (one per line)

```bash
# Iconic grid patterns
python create_map_poster.py -c "New York" -C "USA" -t noir -d 12000
python create_map_poster.py -c "Barcelona" -C "Spain" -t warm_beige -d 8000

# Waterfront & canals
python create_map_poster.py -c "Venice" -C "Italy" -t blueprint -d 4000
python create_map_poster.py -c "Amsterdam" -C "Netherlands" -t ocean -d 6000
python create_map_poster.py -c "Dubai" -C "UAE" -t midnight_blue -d 15000

# Radial patterns
python create_map_poster.py -c "Paris" -C "France" -t pastel_dream -d 10000
python create_map_poster.py -c "Moscow" -C "Russia" -t noir -d 12000

# Organic old cities
python create_map_poster.py -c "Tokyo" -C "Japan" -t japanese_ink -d 15000
python create_map_poster.py -c "Marrakech" -C "Morocco" -t neon_amber -d 5000
python create_map_poster.py -c "Rome" -C "Italy" -t warm_beige -d 8000

# Coastal cities
python create_map_poster.py -c "San Francisco" -C "USA" -t sunset -d 10000
python create_map_poster.py -c "Sydney" -C "Australia" -t ocean -d 12000
python create_map_poster.py -c "Mumbai" -C "India" -t contrast_zones -d 18000

# River cities
python create_map_poster.py -c "London" -C "UK" -t noir -d 15000
python create_map_poster.py -c "Budapest" -C "Hungary" -t copper_patina -d 8000
```

---

## Distance guide

- **4000–6000 m** — Small/dense cities (Venice, Amsterdam old center)
- **8000–12000 m** — Medium cities, focused downtown (Paris, Barcelona)
- **15000–20000 m** — Large metros, full city view (Tokyo, Mumbai)
