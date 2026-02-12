# modules\load_django.py

"""
Ініціалізація Django з папки modules
"""

import os
import sys
import django

# шлях до проєкту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScrapingCourse_project.settings')
django.setup()