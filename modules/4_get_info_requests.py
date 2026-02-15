# modules\4_get_info_requests.py

"""
Перегляд даних із моделі Product.
Виводить ID, назву, ціну, SKU та JSON-LD для кожного товару.
"""
from load_django import *
from parser_app.models import Product

for item in Product.objects.all().order_by("id"):
    print("ID -", item.id, "Product:", item.name, "| Ціна:", item.price, "| SKU:", item.sku, end='')
    print("json-ld:", item.json_ld)
