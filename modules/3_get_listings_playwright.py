# modules\3_get_listings_playwright.py

"""
Парсинг списку товарів зі сторінки ScrapingCourse (Infinite Scroll / JS Rendering)
за допомогою Playwright. Збирає назви, посилання, картинку, заходить на сторінку
кожного товару і витягує деталі (ціна, опис, SKU, JSON-LD).
"""

from load_django import *
from parser_app.models import Product

import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.scrapingcourse.com/infinitescroll/")

        # Скролимо кілька разів, щоб підвантажити товари
        for _ in range(5):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

        products = await page.query_selector_all(".product")

        for product in products:
            try:
                title = await product.query_selector(".woocommerce-loop-product__title")
                url = await product.query_selector("a")
                img = await product.query_selector("img")

                title_text = await title.inner_text() if title else None
                url_href = await url.get_attribute("href") if url else None
                img_url = await img.get_attribute("src") if img else None

                # Заходимо на сторінку товару
                detail_page = await browser.new_page()
                await detail_page.goto(url_href)
                await asyncio.sleep(1)

                try:
                    price_el = await detail_page.query_selector("span.woocommerce-Price-amount bdi")
                    price = await price_el.inner_text() if price_el else None
                except:
                    price = None

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

                if price:
                    clean_price = price.replace("$", "").replace(",", "").strip()
                    try:
                        clean_price = float(clean_price)
                    except:
                        clean_price = None
                else:
                    clean_price = None

                # Запис у БД
                Product.objects.update_or_create(
                    url=url_href,
                    defaults={
                        'name': title_text,
                        'image': img_url,
                        'price': clean_price,
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