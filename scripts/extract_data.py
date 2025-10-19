import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_LAKE_DIR = os.path.join(BASE_DIR, "../data_lake")
os.makedirs(DATA_LAKE_DIR, exist_ok=True)

WEBSITES = {
    "laptops": "https://webscraper.io/test-sites/e-commerce/static/computers/laptops",
    "phones": "https://webscraper.io/test-sites/e-commerce/static/phones/touch",
    "tablets": "https://webscraper.io/test-sites/e-commerce/static/computers/tablets",
    "cameras": "https://webscraper.io/test-sites/e-commerce/static/phones/touch",
}

def extract_data(category_name, url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f" Failed to fetch {category_name} page")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    products, prices, ratings = [], [], []
    for product in soup.select(".thumbnail"):
        name = product.select_one(".title")
        price = product.select_one(".price")
        rating_count = len(product.select(".glyphicon-star"))
        name = name.text.strip() if name else "N/A"
        price = price.text.strip() if price else "N/A"
        rating = rating_count if rating_count > 0 else None
        products.append(name)
        prices.append(price)
        ratings.append(rating)

    df = pd.DataFrame({"Product": products, "Price": prices, "Rating": ratings})
    csv_path = os.path.join(DATA_LAKE_DIR, f"{category_name}_raw.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f" {category_name.capitalize()} raw data saved to {csv_path}")

for site_name, site_url in WEBSITES.items():
    extract_data(site_name, site_url)
