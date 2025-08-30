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

# Database для локальной разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# Cache для разработки (dummy cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Простая конфигурация для разработки
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

# Дополнительные настройки для разработки
ALLOWED_HOSTS = ['*']  # В разработке разрешаем все хосты

# Переопределение шаблонов для упрощения разработки
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
                # Убираем проблемные контекстные процессоры
                # 'core.context_processors.cart_context',
                # 'core.context_processors.analytics_context',
            ],
        },
    },
]

print("Запущена УПРОЩЕННАЯ локальная разработка (settings_local.py)")
