# ScrapingCourse_project\urls.py

"""
Файл конфігурації URL-ів (urls.py).
Містить маршрут до адмінки Django.
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]