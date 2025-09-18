# Production Settings
import os
import dj_database_url

# Импортируем базовые настройки Django
from .settings_base import *
from decouple import config

# Production режим
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# Database для production
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Internationalization
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'ru')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Moscow')
USE_TZ = True

# Static files для production
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/pravoslavie_portal/staticfiles/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/pravoslavie_portal/media/'

# Security Headers для production
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Session cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

print("Production настройки загружены")

# Google OAuth настройки для автоматического входа
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True  # Автоматический вход при GET запросе
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_STORE_TOKENS = False
SOCIALACCOUNT_SIGNUP_FORM_CLASS = None

# Настройки редиректов
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Провайдеры (если есть настройки Google)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
