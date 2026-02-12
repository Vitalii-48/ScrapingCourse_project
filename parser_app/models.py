# parser_app/models.py

"""
Модель Product для збереження даних парсингу:
назва, посилання, картинка, ціна, опис, артикул (SKU), JSON-LD.
"""

from django.db import models

# Модель Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    image = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    json_ld = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name