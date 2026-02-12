# results/products_dump.py

from modules.load_django import *
from parser_app.models import Product
from django.core.serializers.json import DjangoJSONEncoder
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def dump_products_to_json():
    products = Product.objects.all().values()
    filename = os.path.join(BASE_DIR, "products_dump.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(list(products), f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
    print(f"Дамп БД збережено у {filename}")

if __name__ == "__main__":
    dump_products_to_json()