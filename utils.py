# utils.py

import requests
from bs4 import BeautifulSoup
from config import PRODUCT_URL, HEADERS

def scrape_price():
    try:
        r = requests.get(PRODUCT_URL, headers=HEADERS)
        soup = BeautifulSoup(r.text, "lxml")

        title_tag = soup.find("span", class_="VU-ZEz")
        title = title_tag.text.strip() if title_tag else "Unknown Product"

        price_tag = soup.find("div", class_="Nx9bqj CxhGGd")
        if not price_tag:
            return title, None

        price_text = price_tag.text.strip().replace("₹", "").replace(",", "")
        price = int(price_text)

        return title, price

    except:
        return "Unknown Product", None

print(scrape_price())
