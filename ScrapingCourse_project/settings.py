# ScrapingCourse_project\settings.py

"""
Файл налаштувань Django для проєкту ScrapingCourse_project.
Містить конфігурацію безпеки, бази даних, додатків, middleware,
шаблонів, локалізації та інші базові параметри.
"""

import environ
import os
from pathlib import Path

# Базова директорія проєкту
BASE_DIR = Path(__file__).resolve().parent.parent

# Ініціалізація
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Використання
SECRET_KEY = env("SC_SECRET_KEY")
PASSWORD_BD = env("SC_PASSWORD_BD")

# Режим розробки
DEBUG = True

ALLOWED_HOSTS = []

# Додатки Django + твій додаток parser_app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parser_app',   # твій додаток
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ScrapingCourse_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Підключення до PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scraping_db',   # назва твоєї бази
        'USER': 'postgres',      # користувач Postgres
        'PASSWORD': PASSWORD_BD,    # пароль користувача
        'HOST': 'localhost',     #   локальна база
        'PORT': '5432',          # стандартний порт Postgres
    }
}

# Статичні файли
STATIC_URL = '/static/'

# Мова та час
LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'Europe/Kiev'

USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'