import os
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests

BASE_URL = "https://anandsreekumar.com"
OUTPUT_FILE = "sitemap.xml"
STATIC_DIRS = [".", "writeups"]

urls = []

# Collect URLs excluding 404
for directory in STATIC_DIRS:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                if "404.html" in rel_path:
                    continue
                url = BASE_URL + "/" + rel_path.replace("index.html", "").lstrip("./").rstrip("/")
                urls.append(url)

# Build sitemap XML
sitemap = BeautifulSoup(features="xml")
urlset = sitemap.new_tag("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
sitemap.append(urlset)

for url in sorted(set(urls)):
    url_tag = sitemap.new_tag("url")
    loc = sitemap.new_tag("loc")
    loc.string = url
    lastmod = sitemap.new_tag("lastmod")
    lastmod.string = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url_tag.append(loc)
    url_tag.append(lastmod)
    urlset.append(url_tag)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(sitemap.prettify())

print(f"[+] sitemap.xml generated with {len(urls)} URLs (404.html excluded)")

# Ping Google
def ping_google():
    sitemap_url = f"{BASE_URL}/sitemap.xml"
    try:
        res = requests.get(f"https://www.google.com/ping?sitemap={sitemap_url}", timeout=10)
        if res.status_code == 200:
            print("[+] Pinged Google successfully.")
        else:
            print(f"[!] Google ping failed: HTTP {res.status_code}")
    except Exception as e:
        print(f"[!] Error pinging Google: {e}")

ping_google()
