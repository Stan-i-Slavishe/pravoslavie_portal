"""
Исправление для HTTPS и кодировки в development режиме
"""
import os
import sys
from config.settings import *

# Принудительно отключаем HTTPS редиректы
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Настройки сессий
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Настройки для корректного логирования на Windows
if os.name == 'nt':  # Windows
    import locale
    try:
        # Пытаемся установить UTF-8 кодировку
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')
        except:
            pass

# Настройки логирования с правильной кодировкой
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,  # Принудительно используем stdout
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',  # Принудительно UTF-8
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Создаем папку для логов если её нет
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

print("🔧 Development настройки загружены:")
print(f"   DEBUG = {DEBUG}")
print(f"   HTTPS редиректы отключены")
print(f"   Кодировка логов исправлена")
print(f"   Используйте только HTTP: http://127.0.0.1:8000")
