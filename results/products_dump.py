# results/products_dump.py

from modules.load_django import *
from parser_app.models import Product
from django.core.serializers.json import DjangoJSONEncoder
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def dump_products_to_json():
    """
    Експортує всі товари з моделі Product у JSON-файл.

    - Виконує запит до бази даних (Product.objects.all().values()),
      отримуючи всі поля моделі у вигляді словників.
    - Створює файл results/products_dump.json та записує дані у форматі JSON.
    - Використовує DjangoJSONEncoder для серіалізації складних типів
      (Decimal, DateTime, dict, list), щоб уникнути помилок.
    - Дані зберігаються у UTF-8 кодуванні з відступами (indent=4)
      для зручності читання.

    Результат:
    - JSON-файл з усіма полями моделі Product.

        """

    products = Product.objects.all().values()
    filename = os.path.join(BASE_DIR, "products_dump.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list(products), f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
    print(f"Дамп БД збережено у {filename}")

if __name__ == "__main__":
    dump_products_to_json()