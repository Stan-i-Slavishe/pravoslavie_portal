# Минимальные настройки без Redis для инициализации
from .settings import *

# Отключаем Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Сессии в базе данных
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Отключаем Celery
CELERY_TASK_ALWAYS_EAGER = True

# Простое логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
