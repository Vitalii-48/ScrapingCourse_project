# tests/test_requests_parser.py
import pytest

from decimal import Decimal
from unittest.mock import Mock
import importlib
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.modules["load_django"] = Mock()
sys.modules["parser_app"] = Mock()
sys.modules["parser_app.models"] = Mock()
parser = importlib.import_module("modules.1_get_listings_requests")

def test_get_product_details(monkeypatch):
    # HTML для сторінки товару
    detail_html = """
    <span class="woocommerce-Price-amount"><bdi>$19.99</bdi></span>
    <div id="tab-description"><p>Test description</p></div>
    <span class="sku">SKU123</span>
    <script type="application/ld+json">
        {"@context":"https://schema.org","@type":"Product","name":"Test Product"}
    </script>
    """

    # Мокаємо requests.get, щоб він повертав наш HTML

    def fake_get(url, headers=None):
        return Mock(text=detail_html)

    # підміняємо requests.get на нашу фейкову функцію
    monkeypatch.setattr(parser.requests, "get", fake_get)

    # Викликаємо функцію
    details = parser.get_product_details("https://example.com/product1")

    # Перевіряємо результат
    assert details["price"] == Decimal("19.99")
    assert details["description"] == "Test description"
    assert details["sku"] == "SKU123"
    assert details["json_ld"]["@type"] == "Product"