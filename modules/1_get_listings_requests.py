# modules\1_get_listings_requests.py

"""
Парсинг списку з сайту scrapingcourse.com. Збирає назви, посилання та картинки, заходить на сторінку кожного товару,
витягує деталі (ціна, опис, SKU, JSON-LD) і зберігає у модель Product.
"""


from load_django import *
from parser_app.models import Product
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import json
import re
import time


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com',
}

def get_product_details(link):
    """ Функція для парсингу сторінки окремого товару """
    r = requests.get(link, headers=HEADERS)
    detail_soup = BeautifulSoup(r.text, "html.parser")

    # 3. Витягуємо деталі товару
    try:
        price_text = detail_soup.select_one("span.woocommerce-Price-amount bdi").get_text(strip=True)
        match = re.search(r"[\d\.]+", price_text.replace(",", "."))
        price = Decimal(match.group()) if match else None
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

    try:
        json_ld = detail_soup.find("script", type="application/ld+json")
        json_data = json.loads(json_ld.string) if json_ld else None
    except Exception:
        json_data = None

    return {
        'price': price,
        'description': description,
        'sku': sku_detail,
        'json_ld': json_data
    }

def run_parser():
    """Основна функція запуску (Логіка №1 та збереження)"""
    url = "https://www.scrapingcourse.com/ecommerce/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # 1. Збір списку товарів
    products = soup.select(".product")

    for product in products:
        title = product.select_one(".woocommerce-loop-product__title").get_text(strip=True)
        link = product.select_one("a")["href"]
        img_url = product.select_one("img.product-image").get("src")

        print("="*50)
        print(f"Парсимо: {title}")

        # 2. Заходимо на сторінку товару, викликаючи функцію деталей
        details = get_product_details(link)

        # 4. Збереження даних товару в БД
        Product.objects.update_or_create(
            url=link,
            defaults={
                'name': title,
                'image': img_url,
                'price': details['price'],
                'description': details['description'],
                'sku': details['sku'],
                'json_ld': details['json_ld'],
                'source': "requests"
            }
        )

        # невелика пауза, щоб не перевантажувати сайт
        time.sleep(1)

if __name__ == "__main__":
    run_parser()

