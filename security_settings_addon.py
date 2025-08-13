

# 🛡️ НАСТРОЙКИ БЕЗОПАСНОСТИ (ДОБАВЛЕНО)

# Логирование безопасности
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'security',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'security',
        },
    },
    'loggers': {
        'core.middleware.security': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Создаем папку для логов
import os
log_dir = BASE_DIR / 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройки rate limiting (можно настраивать)
SECURITY_RATE_LIMITS = {
    'requests_per_minute': 60,      # Запросов в минуту
    'requests_per_hour': 1000,      # Запросов в час
    'mobile_feedback_per_hour': 10, # Мобильная обратная связь
    'login_attempts_per_hour': 10,  # Попытки входа
}

# Уведомления о мобильной обратной связи
FEEDBACK_EMAIL_NOTIFICATIONS = config('FEEDBACK_EMAIL_NOTIFICATIONS', default=True, cast=bool)

# URL сайта для ссылок в email
SITE_URL = config('SITE_URL', default='http://localhost:8000')

# Дополнительные настройки безопасности для продакшена
if not DEBUG:
    # HTTPS настройки
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookies безопасность
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Дополнительные заголовки
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    
    # Строгие настройки безопасности
    SECURITY_RATE_LIMITS.update({
        'requests_per_minute': 30,      # Строже для продакшена
        'requests_per_hour': 500,
        'mobile_feedback_per_hour': 5,
        'login_attempts_per_hour': 5,
    })

# Настройки для кеширования (Redis рекомендуется для продакшена)
if config('REDIS_URL', default=''):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    # Fallback на локальное кеширование
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
