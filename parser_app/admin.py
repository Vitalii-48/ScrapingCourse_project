# parser_app\admin.py

"""
Налаштування Django Admin для моделі Product.
Додає відображення основних полів, пошук та фільтри.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Product

# ---- Адмінка для Product ----
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "name", "url", "price", "sku", "description", "source")
    search_fields = ("name", "sku", "source")
    list_filter = ("sku", "source",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image)
        return "-"

    image_tag.short_description = "Зображення"

