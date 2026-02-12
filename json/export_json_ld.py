# json/export_json_ld.py

"""
Експорт JSON-LD з моделі Product у окремі файли в папці json
"""

from modules.load_django import *
from parser_app.models import Product
import os
import json


def safe_filename(name):
    """
        Допоміжна функція:
        Перетворює назву товару у безпечну назву файлу (нижній регістр, заміна пробілів).
        """
    return name.replace(' ', '_').lower()

def export_json_ld():
    """
        Основна функція:
        Експортує товари з моделі Product у окремі JSON-файли в папці json/.
        """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    products = Product.objects.only("name", "json_ld")
    for product in products:
        if product.json_ld:
            filename = os.path.join(BASE_DIR, f"{safe_filename(product.name)}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(product.json_ld, f, ensure_ascii=False, indent=4)
            print(f"Збережено: {filename}")

if __name__ == "__main__":
    export_json_ld()