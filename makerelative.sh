#!/bin/bash

INPUT="index.html"
OUTPUT="index.preview.html"
DOMAIN="https://anandsreekumar.com"

cp "$INPUT" "$OUTPUT"

echo "[*] Rewriting absolute links to relative paths in $OUTPUT..."

# Convert anchor hrefs
sed -i '' "s|href=\"$DOMAIN|href=.|" "$OUTPUT"

# Convert og:url, twitter:url, etc. to GitHub Pages preview URL (optional)
sed -i '' "s|$DOMAIN|https://anandsreekumaras.github.io/anandsreekumar.com|g" "$OUTPUT"

echo "[+] Done. Preview version saved as $OUTPUT"
