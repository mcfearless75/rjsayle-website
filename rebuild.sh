#!/usr/bin/env bash
# Full rebuild from a clean clone. Run from /home/claude/rjsayle
set -e
rm -rf site && cp -r /root/rjsayle-website site
cp seo-fix.py geo-assets.py tailwind.config.js tailwind.input.css swap-tailwind.py fix-img.py site/ 2>/dev/null || true
cd site
python3 seo-fix.py > /dev/null
python3 geo-assets.py > /dev/null
python3 -c "
import cairosvg; cairosvg.svg2png(url='og-image.svg', write_to='og-image.png', output_width=1200, output_height=630)
from PIL import Image; Image.open('og-image.png').convert('RGB').save('og-image.jpg', quality=88)"
npx -y tailwindcss@3 -c tailwind.config.js -i tailwind.input.css -o assets/tailwind.css --minify 2>/dev/null
python3 swap-tailwind.py
python3 fix-img.py
rm -f seo-fix.py geo-assets.py swap-tailwind.py fix-img.py tailwind.input.css og-image.png
echo "rebuild complete"
