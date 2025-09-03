# Настройки для быстрого тестирования с SQLite
from .settings import *
import os

# SQLite база данных для быстрого тестирования
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# Простое кеширование в памяти
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Отладка включена
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email в консоль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print("=== ТЕСТОВЫЕ НАСТРОЙКИ SQLite ===")
print("База данных: SQLite (db_test.sqlite3)")
print("Кеш: В памяти")
print("Debug: Включен")
