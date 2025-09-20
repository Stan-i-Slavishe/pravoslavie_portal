# 🐳 Православный портал - Production Settings
import os
import dj_database_url
from .settings import *

# 🔒 Security Settings
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# 🔑 Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# 🗄️ Database Configuration
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 🚀 Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://redis:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
        }
    }
}

# 📧 Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@pravoslavie-portal.ru')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# 📁 Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# 🔒 Security Headers
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 🍪 Session & CSRF
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# 📊 Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'file', 'mail_admins'],
            'propagate': False,
        },
    },
}

# 🔄 Celery Configuration
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/2')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://redis:6379/3')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# 📊 Monitoring & Analytics
YANDEX_METRIKA_ID = os.environ.get('YANDEX_METRIKA_ID')
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')

# 🚨 Error Monitoring
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(auto_enabling_integrations=False),
            CeleryIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment='production',
    )

# 💳 Payment Configuration
YOOKASSA_SHOP_ID = os.environ.get('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = os.environ.get('YOOKASSA_SECRET_KEY')
YOOKASSA_TEST_MODE = os.environ.get('YOOKASSA_TEST_MODE', 'False').lower() == 'true'

# 🎬 YouTube API
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

# 🔍 Admin Configuration
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@pravoslavie-portal.ru')),
]
MANAGERS = ADMINS

# 🌐 CORS Configuration
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True

# 📱 PWA Configuration
PWA_APP_NAME = os.environ.get('PWA_APP_NAME', 'Православный портал')
PWA_APP_DESCRIPTION = os.environ.get('PWA_APP_DESCRIPTION', 'Духовные рассказы, книги и терапевтические сказки')
PWA_APP_THEME_COLOR = os.environ.get('PWA_APP_THEME_COLOR', '#2B5AA0')
PWA_APP_BACKGROUND_COLOR = os.environ.get('PWA_APP_BACKGROUND_COLOR', '#FEFEFE')

# 🎯 Feature Flags
ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'True').lower() == 'true'
ENABLE_PWA = os.environ.get('ENABLE_PWA', 'True').lower() == 'true'
ENABLE_NOTIFICATIONS = os.environ.get('ENABLE_NOTIFICATIONS', 'True').lower() == 'true'
ENABLE_YOOKASSA = os.environ.get('ENABLE_YOOKASSA', 'True').lower() == 'true'

# 📈 Performance Settings
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔧 Whitenoise Configuration
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# 📊 Database Optimization
CONN_MAX_AGE = 600
CONN_HEALTH_CHECKS = True

# 🎯 Production-specific middleware
MIDDLEWARE += [
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# 🔍 Search Configuration
if os.environ.get('ELASTICSEARCH_URL'):
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
            'URL': os.environ.get('ELASTICSEARCH_URL'),
            'INDEX_NAME': 'pravoslavie_portal',
        },
    }

# 📈 Performance Monitoring
if os.environ.get('ENABLE_PERFORMANCE_MONITORING', 'False').lower() == 'true':
    INSTALLED_APPS += ['silk']
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True

# ❤️ Health Check URL
HEALTH_CHECK_URL = '/health/'

# 🔐 Additional Security Settings
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# 🌍 Internationalization for Production
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'ru')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Moscow')

# 📧 Admin Email Settings
if EMAIL_HOST_USER:
    EMAIL_TIMEOUT = 10
    EMAIL_SSL_KEYFILE = None
    EMAIL_SSL_CERTFILE = None

# 📊 Импорт настроек мониторинга
try:
    from .monitoring_settings import *
except ImportError:
    print("⚠️ Настройки мониторинга не загружены")

# 🔧 Добавление middleware мониторинга
MIDDLEWARE += [
    'core.middleware.monitoring.PerformanceMonitoringMiddleware',
    'core.middleware.monitoring.SecurityMonitoringMiddleware', 
    'core.middleware.monitoring.HealthCheckMiddleware',
]

print("📊 Production настройки с мониторингом загружены")
