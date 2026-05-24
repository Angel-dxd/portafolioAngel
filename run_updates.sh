#!/bin/bash
cd /Users/angelxavier/portafolioAngel

echo "Generando CV..."
python3 cv/generate_cv.py

echo "Convirtiendo imágenes a WebP..."
sips -s format webp -z 180 180 img/foto_clean.png --out img/foto_clean.webp
sips -s format webp img/boutique-login.jpeg --out img/boutique-login.webp
sips -s format webp img/boutique-dashboard.jpeg --out img/boutique-dashboard.webp
sips -s format webp img/boutique-market.jpeg --out img/boutique-market.webp

echo "¡Hecho!"
