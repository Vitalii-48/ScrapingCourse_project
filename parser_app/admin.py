# parser_app\admin.py

"""
Налаштування Django Admin для моделі Product.
Додає відображення основних полів, пошук та фільтри.
"""

from django.contrib import admin
from .models import Product

# ---- Адмінка для Product ----
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "price", "sku", "description")
    search_fields = ("name", "url", "sku")
    list_filter = ("sku",)
