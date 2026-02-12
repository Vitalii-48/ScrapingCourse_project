# modules\1_get_listings.py

"""
Парсинг списку з сайту scrapingcourse.com. Збирає назви, посилання та картинки, заходить на сторінку кожного товару,
витягує деталі (ціна, опис, SKU, JSON-LD) і зберігає у модель Product.
"""

from load_django import *
from parser_app.models import Product
import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
}

url = "https://www.scrapingcourse.com/ecommerce/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 1. Збір списку товарів
products = soup.select(".product")

for product in products:
    title = product.select_one(".woocommerce-loop-product__title").get_text(strip=True)
    link = product.select_one("a")["href"]
    img_url = product.select_one("img.product-image").get("src")

    print("="*50)
    print("Назва:", title)
    print("Посилання:", link)
    print("Картинка:", img_url)

    # 2. Заходимо на сторінку товару
    r = requests.get(link, headers=headers)
    detail_soup = BeautifulSoup(r.text, "html.parser")

    # 3. Витягуємо деталі
    try:
        price = detail_soup.select_one("span.woocommerce-Price-amount bdi").get_text(strip=True)
    except AttributeError:
        price = None

    try:
        description = detail_soup.select_one("div#tab-description p").get_text(strip=True)
    except AttributeError:
        description = None

    try:
        sku_detail = detail_soup.select_one("span.sku").get_text(strip=True)
    except AttributeError:
        sku_detail = None

    # JSON-LD
    try:
        json_ld = detail_soup.find("script", type="application/ld+json")
        json_data = json.loads(json_ld.string) if json_ld else None
    except Exception:
        json_data = None

    print("Ціна:", price)
    print("Опис:", description)
    print("SKU (детально):", sku_detail)
    print("JSON-LD:", json_data)

    product = Product(
        name=title,
        url=link,
        image=img_url,
        price=float(price.replace("$", "")) if price else None,
        description=description,
        sku=sku_detail,
        json_ld=json_data
    )
    product.save()

    # невелика пауза, щоб не перевантажувати сайт
    time.sleep(1)
