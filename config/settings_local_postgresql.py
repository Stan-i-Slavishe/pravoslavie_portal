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

# === ПРИНУДИТЕЛЬНО POSTGRESQL ===
# Убрана условная логика - всегда используем PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='pravoslavie_portal_db'),
        'USER': config('DB_USER', default='pravoslavie_user'),
        'PASSWORD': config('DB_PASSWORD', default='local_strong_password_2024'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        # PostgreSQL не использует charset в OPTIONS
        # Кодировка задается при создании БД
    }
}

print("Локальная разработка: PostgreSQL база данных (принудительно)")

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

# reCAPTCHA настройки для локальной разработки (тестовые ключи)
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
RECAPTCHA_REQUIRED_SCORE = 0.85

# Отключаем предупреждение о тестовых ключах для локальной разработки
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']
# CSRF Settings for HTTPS
CSRF_TRUSTED_ORIGINS = ['https://dobrist.com', 'https://www.dobrist.com']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Настройки для социальной аутентификации Google
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# Автоматическое перенаправление на провайдера
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'VERIFIED_EMAIL': True,
    }
}
