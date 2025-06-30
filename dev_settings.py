# Упрощенные настройки для локальной разработки
# Добавьте в конец settings.py или создайте local_settings.py

# Принудительно отключаем Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Сессии в базе данных
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400

# Отключаем Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

print("🔧 Применены упрощенные настройки для разработки")
