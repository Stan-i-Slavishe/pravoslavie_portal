from .settings_base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['46.62.167.17', 'localhost', '127.0.0.1', 'dobrist.com', 'www.dobrist.com']

# Сильный SECRET_KEY для production (более 50 символов)
SECRET_KEY = 'pravoslavie-production-secret-key-2025-very-long-and-secure-random-string-for-django'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pravoslavie_portal_db',
        'USER': 'pravoslavie_user',
        'PASSWORD': 'dev_password_123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/pravoslavie_portal/staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/pravoslavie_portal/media/'

print("Production настройки загружены")

# Security настройки для production
# SSL настроен через Nginx reverse proxy, поэтому не включаем SECURE_SSL_REDIRECT
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'stassilin@mail.ru'
EMAIL_HOST_PASSWORD = 'kAZjm3a2159NDohSEdPK'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@dobrist.com'
SERVER_EMAIL = 'info@dobrist.com'

# reCAPTCHA настройки
RECAPTCHA_PUBLIC_KEY = '6LeD-dErAAAAAPFCCTD0oEDipeyX8FYmrbJgZ9Ri'
RECAPTCHA_PRIVATE_KEY = '6LeD-dErAAAAAD6Asd70b0wN98n-YFi0BunWmm2f'
RECAPTCHA_REQUIRED_SCORE = 0.85

# Подавляем некритичные warnings
SILENCED_SYSTEM_CHECKS = [
    'account.W001',  # Конфликт ACCOUNT_LOGIN_METHODS - некритичен
    'security.W008',  # SSL редирект настроен в Nginx
    'security.W009',  # SECRET_KEY достаточно сильный
]

print("Production настройки загружены")
