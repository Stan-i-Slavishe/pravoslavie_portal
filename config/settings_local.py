from .settings_base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '0.0.0.0',
    'testserver'
]

# === ГИБКИЙ ВЫБОР БАЗЫ ДАННЫХ ===
# Проверяем переменную USE_SQLITE из .env файла
use_sqlite = config('USE_SQLITE', default=True, cast=bool)

if use_sqlite:
    # SQLite для простоты разработки
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("🔧 Локальная разработка: SQLite база данных")
else:
    # PostgreSQL для тестирования как на продакшене
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='pravoslavie_portal_dev'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            # PostgreSQL не использует charset в OPTIONS
            # Кодировка задается при создании БД
        }
    }
    print("🔧 Локальная разработка: PostgreSQL база данных")

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email backend для разработки (письма в консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Отключить HTTPS редирект в разработке
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Cache для разработки
cache_backend = config('CACHE_BACKEND', default='dummy')
if cache_backend == 'dummy':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    # Использовать Redis если нужно тестировать кеширование
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        }
    }

# Простые настройки для разработки
try:
    import corsheaders
    CORS_ALLOW_ALL_ORIGINS = True
except ImportError:
    pass

# Настройки для тестирования платежей
YOOKASSA_SHOP_ID = config('YOOKASSA_SHOP_ID', default='test-shop-id')
YOOKASSA_SECRET_KEY = config('YOOKASSA_SECRET_KEY', default='test-secret-key')
YOOKASSA_TEST_MODE = True

# YouTube API для тестирования
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY', default='your-youtube-api-key')

# Push-уведомления (из переменных окружения)
VAPID_PRIVATE_KEY = config('VAPID_PRIVATE_KEY', default='')
VAPID_PUBLIC_KEY = config('VAPID_PUBLIC_KEY', default='')
VAPID_EMAIL = config('VAPID_EMAIL', default='admin@localhost')

# Упрощенные шаблоны для разработки
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

print("🔧 ЛОКАЛЬНАЯ РАЗРАБОТКА (settings_local.py) - улучшенная версия")


# Настройки для локальной разработки
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Локальные домены для CSRF
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Для локальной разработки можно отключить строгие настройки безопасности
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
