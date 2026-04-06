# scraper logic will go here
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import os

# =========================
# CREATE RESULTS FOLDER
# =========================
os.makedirs("results", exist_ok=True)

# =========================
# URL SETUP
# =========================
BASE_URL = "https://newyork.craigslist.org"
SEARCH_URL = "https://newyork.craigslist.org/search/fua"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# GET MAIN PAGE
# =========================
response = requests.get(SEARCH_URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# =========================
# FIND ALL LISTINGS
# =========================
items = soup.find_all("li", class_="cl-static-search-result")

rows = []

# =========================
# LOOP THROUGH LISTINGS
# =========================
for item in items[:30]:  # limit to 30 for safety
    title_tag = item.find("div", class_="title")
    price_tag = item.find("div", class_="price")
    location_tag = item.find("div", class_="location")
    link_tag = item.find("a")

    title = title_tag.get_text(strip=True) if title_tag else None
    price = price_tag.get_text(strip=True) if price_tag else None
    location = location_tag.get_text(strip=True) if location_tag else None

    url = urljoin(BASE_URL, link_tag["href"]) if link_tag and link_tag.get("href") else None

    description = None

    # =========================
    # OPEN EACH LISTING PAGE
    # =========================
    if url:
        try:
            listing_response = requests.get(url, headers=headers, timeout=30)
            listing_response.raise_for_status()

            listing_soup = BeautifulSoup(listing_response.text, "html.parser")

            desc_tag = listing_soup.find("section", id="postingbody")

            if desc_tag:
                description = desc_tag.get_text(" ", strip=True)

            # delay to avoid blocking
            time.sleep(1)

        except Exception:
            description = None

    # =========================
    # SAVE DATA
    # =========================
    rows.append({
        "title": title,
        "price_raw": price,
        "location_raw": location,
        "url": url,
        "description": description
    })

# =========================
# SAVE TO CSV
# ========================
df = pd.DataFrame(rows)

output_path = "results/raw_furniture_listings.csv"
df.to_csv(output_path, index=False)

print(f"Scraping completed. File saved at: {output_path}")
