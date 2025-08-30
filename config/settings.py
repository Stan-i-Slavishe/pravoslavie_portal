"""
Django settings для проекта Православный портал

Автоматический выбор окружения на основе переменной DJANGO_ENV:
- local: для локальной разработки (по умолчанию)
- production: для продакшен сервера
- staging: для тестового сервера (опционально)
"""

import os
from decouple import config

# Определяем окружение
ENVIRONMENT = config('DJANGO_ENV', default='local')

print(f"Загружается окружение: {ENVIRONMENT.upper()}")

# Импортируем настройки в зависимости от окружения
if ENVIRONMENT == 'production':
    from .settings_production import *
elif ENVIRONMENT == 'staging':
    try:
        from .settings_staging import *
    except ImportError:
        print("⚠️ settings_staging.py не найден, использую settings_production.py")
        from .settings_production import *
else:
    # По умолчанию используем локальные настройки
    from .settings_local import *

# Дополнительные настройки, которые могут переопределяться через .env
if config('SECRET_KEY', default=None):
    SECRET_KEY = config('SECRET_KEY')

# Возможность переопределить DEBUG через переменную окружения
if config('DEBUG', default=None) is not None:
    DEBUG = config('DEBUG', cast=bool)

# Переопределение ALLOWED_HOSTS через переменную окружения
allowed_hosts_env = config('ALLOWED_HOSTS', default=None)
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')]

print(f"Настройки загружены для {ENVIRONMENT.upper()} окружения")
print(f"   DEBUG: {DEBUG}")
print(f"   ALLOWED_HOSTS: {ALLOWED_HOSTS}")
