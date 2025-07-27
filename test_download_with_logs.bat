@echo off
echo ===================================================
echo      ТЕСТ ИСПРАВЛЕНИЯ СКАЧИВАНИЯ С ЛОГАМИ
echo ===================================================
echo.
echo Запускаем сервер Django с логированием...
echo.
cd /d E:\pravoslavie_portal

echo Создаем временный settings файл с включенным логированием...
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем настройки с логированием
settings_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'stories',
    'books',
    'accounts',
    'shop',
    'fairy_tales',
    'audio',
    'subscriptions',
    'analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'download_debug.log',
        },
    },
    'loggers': {
        'books': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
'''

with open('config/settings_debug.py', 'w', encoding='utf-8') as f:
    f.write(settings_content)

print('Настройки с логированием созданы')
"

echo.
echo Запускаем сервер с отладочными настройками...
set DJANGO_SETTINGS_MODULE=config.settings_debug
python manage.py runserver 127.0.0.1:8000

echo.
echo После тестирования проверьте файл download_debug.log
echo.
pause
