# modules/2_get_listings_selenium.py

"""
Парсинг списку товарів зі сторінки ScrapingCourse (Load More / Pagination)
за допомогою Selenium. Збирає назви, посилання, картинку, заходить на сторінку
кожного товару і витягує деталі (ціна, опис, SKU, JSON-LD).
"""

from load_django import *
from parser_app.models import Product

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal
import time
import json
import re

def scrape_products():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(), options=options)
    wait = WebDriverWait(driver, 3)

    try:
        driver.get("https://www.scrapingcourse.com/button-click")

        # --- Натискання кнопки Load More ---
        for _ in range(2):
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.ID, "load-more-btn")))
                load_more_button.click()
                time.sleep(1)
            except:
                break

        # --- Збір посилань на товари ---
        product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-item")
        product_links = [p.find_element(By.TAG_NAME, "a").get_attribute("href") for p in product_elements if p]
        print(f"Знайдено товарів: {len(product_links)}")

        # --- Парсинг кожного товару ---
        for url in product_links[:20]: # беремо тільки перші 20 товарів

            try:
                driver.get(url)

                title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_title"))).text
                price_text = driver.find_element(By.CSS_SELECTOR, "span.woocommerce-Price-amount bdi").text
                match = re.search(r"[\d\.]+", price_text)
                price = Decimal(match.group()) if match else None
                img_url = driver.find_element(By.CSS_SELECTOR, ".woocommerce-product-gallery__image img").get_attribute("src")


                try:
                    description = driver.find_element(By.CSS_SELECTOR, "#tab-description p").text
                except:
                    description = None

                try:
                    sku_detail = driver.find_element(By.CLASS_NAME, "sku").text
                except:
                    sku_detail = None

                try:
                    json_ld = driver.find_element(By.XPATH, "//script[@type='application/ld+json']").get_attribute("textContent")
                    json_data = json.loads(json_ld)
                except:
                    json_data = None

                # --- Запис у БД ---
                Product.objects.update_or_create(
                    url=url,
                    defaults={
                        'name': title,
                        'image': img_url,
                        'price': price,
                        'description': description,
                        'sku': sku_detail,
                        'json_ld': json_data,
                        'source': "selenium"
                    }
                )
                print(f"Збережено: {title}")

            except Exception as e:
                print(f"Помилка на сторінці {url}: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_products()