# results/products_csv.py

from modules.load_django import *
from parser_app.models import Product
import os, csv, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def export_products_to_csv():
    """
        Експортує всі товари з моделі Product у CSV-файл.

        - Виконує запит до бази даних (Product.objects.all().values()),
          отримуючи всі поля моделі у вигляді словників.
        - Автоматично визначає назви колонок (fieldnames) з ключів першого запису.
        - Створює файл results/products.csv та записує дані у табличному форматі.
        - Для складних типів (dict, list, Decimal) значення перетворюються у рядки
          або JSON-рядки, щоб уникнути помилок при серіалізації.

        Результат:
        - CSV-файл з усіма полями моделі Product.
        """
    products = Product.objects.all().values()
    filename = os.path.join(BASE_DIR, "products.csv")
    filenames = products[0].keys() if products else []
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=filenames)
        writer.writeheader()
        for p in products:
            row = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)) for k, v in p.items()}
            writer.writerow(row)


if __name__ == "__main__":
    export_products_to_csv()

