from .settings_base import *
from decouple import Config, RepositoryEnv
import os

# STAGING - точная копия продакшена для безопасного тестирования

# Настройка decouple для чтения .env.staging
STAGING_ENV_FILE = BASE_DIR / '.env.staging'
if STAGING_ENV_FILE.exists():
    staging_config = Config(RepositoryEnv(str(STAGING_ENV_FILE)))
else:
    # Fallback на обычный config если .env.staging не найден
    from decouple import config
    staging_config = config

DEBUG = staging_config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = staging_config(
    'ALLOWED_HOSTS', 
    default='staging.dobrist.com,www.staging.dobrist.com',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Database для staging (ОТДЕЛЬНАЯ от продакшена!)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': staging_config('DB_NAME'),
        'USER': staging_config('DB_USER'),
        'PASSWORD': staging_config('DB_PASSWORD'),
        'HOST': staging_config('DB_HOST', default='localhost'),
        'PORT': staging_config('DB_PORT', default='5432'),
        # PostgreSQL не использует charset в OPTIONS
    }
}

# Static files для staging
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/staging.dobrist.com/staticfiles/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files для staging
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/staging.dobrist.com/media/'

# Email settings (те же что продакшн для тестирования)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = staging_config('EMAIL_HOST', default='smtp.yandex.ru')
EMAIL_PORT = staging_config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = staging_config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = staging_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = staging_config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = staging_config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Security settings (как на продакшене для точного тестирования)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings (мягче чем продакшн)
SECURE_HSTS_SECONDS = 3600  # 1 час вместо года
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

# Cache для staging (Redis, но другой канал)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': staging_config('REDIS_URL', default='redis://127.0.0.1:6379/2'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'pravoslavie_staging',
        'TIMEOUT': 300,
    }
}

# Session в Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Celery configuration для staging
CELERY_BROKER_URL = staging_config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = staging_config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')

# YooKassa настройки (ТЕСТОВЫЕ!)
YOOKASSA_SHOP_ID = staging_config('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = staging_config('YOOKASSA_SECRET_KEY')
YOOKASSA_TEST_MODE = staging_config('YOOKASSA_TEST_MODE', default=True, cast=bool)

# YouTube API (тестовый ключ)
YOUTUBE_API_KEY = staging_config('YOUTUBE_API_KEY')

# Push-уведомления
VAPID_PRIVATE_KEY = staging_config('VAPID_PRIVATE_KEY', default='')
VAPID_PUBLIC_KEY = staging_config('VAPID_PUBLIC_KEY', default='')
VAPID_EMAIL = staging_config('VAPID_EMAIL', default='admin@staging.dobrist.com')

# Полная конфигурация шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.cart_context',
                'core.context_processors.site_context',
            ],
        },
    },
]

# Logging для staging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] STAGING {levelname} {name}: {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/dobrist/staging_django.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'shop': {
            'handlers': ['file'],
            'level': 'INFO', 
            'propagate': False,
        },
    },
}

# Создать папки для логов (локально не сработает, но на сервере нужно)
try:
    os.makedirs('/var/log/dobrist', exist_ok=True)
except PermissionError:
    pass  # Локально может не быть прав

# Админы
ADMINS = [
    ('Staging Admin', staging_config('ADMIN_EMAIL', default='admin@staging.dobrist.com')),
]
MANAGERS = ADMINS

# Идентификация окружения
ENVIRONMENT_NAME = 'STAGING'
print("🧪 STAGING ОКРУЖЕНИЕ (settings_staging.py) - исправленная версия с правильным чтением .env.staging")
