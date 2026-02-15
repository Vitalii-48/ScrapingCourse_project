# parser_app/models.py

"""
Модель Product для збереження даних парсингу:
назва, посилання, посилання на картинку, ціна, опис, артикул (SKU), JSON-LD.
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
    source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['url', 'source'], name='unique_product_source_url')]

    def __str__(self):
        return f"{self.name} [{self.source}]"