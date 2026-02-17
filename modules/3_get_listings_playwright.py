# modules\3_get_listings_playwright.py

"""
Парсинг списку товарів зі сторінки ScrapingCourse (Infinite Scroll / JS Rendering)
за допомогою Playwright. Збирає назви, посилання, картинку, заходить на сторінку
кожного товару і витягує деталі (ціна, опис, SKU, JSON-LD).
"""

from load_django import *
from parser_app.models import Product
from asgiref.sync import sync_to_async
import asyncio
import json
import re
from playwright.async_api import async_playwright
from decimal import Decimal

async def scrape_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.scrapingcourse.com/infinite-scrolling")

        # Скролимо кілька разів, щоб підвантажити товари
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

        product_elements = page.locator(".product-item")
        count = await product_elements.count()

        product_links = []
        for i in range(count):
            url_href = await product_elements.nth(i).locator("a").first.get_attribute("href")
            if url_href:
                product_links.append(url_href)


        for link in product_links:
            try:
                # Заходимо на сторінку товару
                detail_page = await browser.new_page()
                await detail_page.goto(link)
                await asyncio.sleep(0.5)

                title = await detail_page.locator("h1.product_title.entry-title").inner_text()

                try:
                    price_text = await detail_page.locator("p.price span.woocommerce-Price-amount bdi").inner_text()
                    match = re.search(r"[\d\.]+", price_text)
                    price = Decimal(match.group()) if match else None
                except:
                    price = None
                    print(price, "exept")

                try:
                    img_url = await detail_page.locator("img.product-image").first.get_attribute("src")
                except:
                    img_url = None

                try:
                    desc_el = await detail_page.query_selector("div#tab-description p")
                    description = await desc_el.inner_text() if desc_el else None
                except:
                    description = None

                try:
                    sku_el = await detail_page.query_selector("span.sku")
                    sku_detail = await sku_el.inner_text() if sku_el else None
                except:
                    sku_detail = None

                try:
                    json_ld_el = await detail_page.query_selector("script[type='application/ld+json']")
                    json_ld_text = await json_ld_el.inner_text() if json_ld_el else None
                    json_data = json.loads(json_ld_text) if json_ld_text else None
                except:
                    json_data = None

                # Запис у БД
                await sync_to_async(Product.objects.update_or_create)(
                    url=link,
                    defaults={
                        'name': title,
                        'image': img_url,
                        'price': price,
                        'description': description,
                        'sku': sku_detail,
                        'json_ld': json_data,
                        'source': "playwright"
                    }
                )

                await detail_page.close()
            except Exception as e:
                print(f"Помилка при обробці продукту: {e}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_products())