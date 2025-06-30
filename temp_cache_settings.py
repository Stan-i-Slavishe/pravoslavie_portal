# Временные настройки кеширования без Redis
# Заменяет настройки в settings.py для локальной разработки

# Кеширование в памяти (вместо Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Сессии в базе данных (вместо Redis)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = None

# Отключаем Celery для локальной разработки
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

print("✅ Настройки кеширования изменены: используется локальная память вместо Redis")
