from .settings import *

# Временно отключаем Redis для проверки дизайна
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
