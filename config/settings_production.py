from .settings_base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['46.62.167.17', 'localhost', '127.0.0.1', 'dobrist.com', 'www.dobrist.com']

SECRET_KEY = 'pravoslavie-secret-key-2025'

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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'stassilin@mail.ru'
EMAIL_HOST_PASSWORD = 'kAZjm3a2159NDohSEdPK'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'stassilin@mail.ru'
SERVER_EMAIL = 'info@dobrist.com'
# Email для получения писем с сайта
CONTACT_EMAIL = 'stassilin@mail.ru'
ADMINS = [('Admin', 'stassilin@mail.ru')]
EMAIL_TIMEOUT = 30
