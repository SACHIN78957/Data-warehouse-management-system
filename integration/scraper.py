
import requests
from bs4 import BeautifulSoup
import json
import csv
import os

def scrape_demo_site(url, json_out):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    items = soup.select(".product_pod")

    for i, prod in enumerate(items, 1):
        name = prod.select_one("h3 a")["title"]
        price = prod.select_one(".price_color").text.replace("£", "").strip()
        rating = prod.select_one(".star-rating")["class"][1]

        products.append({
            "product_id": i,
            "name": name,
            "price": price,
            "rating": rating,
            "category": "Books"
        })

    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)

    return json_out


def json_to_csv(json_file, csv_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    if not data:
        return None

    keys = data[0].keys()
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(data)

    return csv_file
