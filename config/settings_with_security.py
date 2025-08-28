import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,testserver', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',  # Для SEO sitemap
]

THIRD_PARTY_APPS = [
    "django_extensions",  # Для HTTPS в разработке
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Провайдеры социальных сетей
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.telegram',
    'allauth.socialaccount.providers.mailru',
    'allauth.socialaccount.providers.yandex',
]

LOCAL_APPS = [
    'core',           # основная навигация, главная страница
    'accounts',       # расширенные профили пользователей
    'stories',        # видео-рассказы
    'subscriptions',  # система подписок
    'books',          # книги и публикации
    'shop',           # цифровой магазин
    'audio',          # аудио-контент
    'fairy_tales',    # терапевтические сказки
    'analytics',      # аналитика покупательских намерений

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    # Система безопасности (добавляем в начало)
    'core.middleware.security.BlacklistMiddleware',  # Проверка черного списка
    'core.middleware.security.SecurityMiddleware',   # Основная защита
    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Добавляем обязательный middleware для allauth
    'allauth.account.middleware.AccountMiddleware',
    
    # Мониторинг (добавляем в конец)
    'core.middleware.security.MonitoringMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='core.db.sqlite'),  # Используем кастомный SQLite backend
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
        'OPTIONS': {
            'timeout': 30,  # Увеличиваем timeout до 30 секунд
        } if 'sqlite' in config('DB_ENGINE', default='core.db.sqlite') else {}
    }
}

# Для продакшена можно добавить пул соединений
if not config('DEBUG', default=True, cast=bool):
    DATABASES['default']['CONN_MAX_AGE'] = 60
    DATABASES['default']['OPTIONS'].update({
        'MAX_CONNS': 20,
        'MIN_CONNS': 5,
    })

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Создаем STATICFILES_DIRS только если директория существует
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Наши статические файлы
]

# Настройки для сбора статических файлов
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Настройки для продакшена
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Максимальный размер загружаемых файлов (100MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Sites framework
SITE_ID = 1

# Allauth settings (обновленные настройки)
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',  # Наш кастомный backend
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Новые настройки вместо устаревших (упрощенные)
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Отключаем подтверждение email
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False  # Не входим автоматически

# Ограничения на попытки входа (исправленный формат)
# ACCOUNT_RATE_LIMITS = {
#     'login_failed': '5/5m',  # Временно отключаем
# }

# Настройки социальных провайдеров
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    'vk': {
        'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email', 
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False
    },
    'telegram': {
        'TOKEN': config('TELEGRAM_BOT_TOKEN', default=''),
    },
    'mailru': {
        'SCOPE': ['userinfo'],
    },
    'yandex': {
        'SCOPE': ['login:email', 'login:info'],
    }
}

# Настройки аккаунтов (упрощенные)
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Отключаем обязательность username
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Поддерживаем оба способа
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_DISPLAY = lambda user: user.username or user.email

# После входа через соцсети
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_SIGNUP_FORM_CLASS = None  # Убираем кастомную форму
ACCOUNT_SESSION_REMEMBER = True

# Дополнительные настройки для исправления проблем
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

# Автоматический вход после регистрации (упрощенно)
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_GET = False

# Redis настройки
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

# Кеширование с Redis (только если Redis доступен)
try:
    import redis
    # Проверяем подключение к Redis
    r = redis.Redis.from_url(REDIS_URL)
    r.ping()
    
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'pravoslavie_portal',
            'TIMEOUT': 300,  # 5 минут по умолчанию
        }
    }
    
    # Сессии в Redis
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
    
except (ImportError, redis.ConnectionError, redis.ResponseError):
    # Fallback к локальному кешу если Redis недоступен
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
            }
        }
    }
    
    # Сессии в базе данных
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    
    print("⚠️  Redis недоступен, используется локальное кеширование")
SESSION_COOKIE_AGE = 86400  # 24 часа

# Celery настройки
try:
    import redis
    r = redis.Redis.from_url(config('CELERY_BROKER_URL', default='redis://localhost:6379/1'))
    r.ping()
    
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')
    CELERY_TASK_ALWAYS_EAGER = config('CELERY_TASK_ALWAYS_EAGER', default=False, cast=bool)
    
except (ImportError, redis.ConnectionError, redis.ResponseError):
    # Fallback - выполняем задачи синхронно
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'cache+memory://'
    
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True

# Логирование
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
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'pravoslavie_portal': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Создаем папку для логов
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Email настройки
EMAIL_BACKEND = config(
    'EMAIL_BACKEND', 
    default='django.core.mail.backends.console.EmailBackend'  # Для разработки
)

if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Настройки отправителя
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@pravoslavie-portal.ru')
SERVER_EMAIL = config('SERVER_EMAIL', default='server@pravoslavie-portal.ru')

# Список администраторов для уведомлений
ADMIN_EMAIL_LIST = config('ADMIN_EMAIL_LIST', default='admin@pravoslavie-portal.ru', cast=lambda v: [s.strip() for s in v.split(',')])

# 🔐 БЕЗОПАСНОСТЬ (базовая) - дополнительные настройки
# HTTPS настройки для продакшена
if not DEBUG:
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Дополнительные настройки безопасности
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Защита от брутфорса
AXES_ENABLED = config('AXES_ENABLED', default=False, cast=bool)
if AXES_ENABLED:
    AXES_FAILURE_LIMIT = 5
    AXES_COOLOFF_TIME = 1  # 1 час
    AXES_RESET_ON_SUCCESS = True

# =====================================
# HTTPS НАСТРОЙКИ ДЛЯ РАЗРАБОТКИ
# =====================================

# Разрешаем как HTTP так и HTTPS в разработке
SECURE_SSL_REDIRECT = False  # Не принуждаем к HTTPS

# Настройки для работы с HTTPS в разработке
if DEBUG:
    # В разработке поддерживаем и HTTP и HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Для HTTPS запросов используем secure cookies
    SESSION_COOKIE_SECURE = False  # Работает и с HTTP и с HTTPS
    CSRF_COOKIE_SECURE = False     # Работает и с HTTP и с HTTPS
    
    # Отключаем HSTS для разработки
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    
    # Доверенные источники для CSRF (для HTTPS)
    CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'https://127.0.0.1:8000',
        'https://localhost:8000',
    ]
else:
    # Продакшен - строгие настройки
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# =====================================
# НАСТРОЙКИ ПРЯМОГО ПЕРЕНАПРАВЛЕНИЯ GOOGLE OAUTH
# =====================================

# Убираем промежуточную страницу при входе через Google
SOCIALACCOUNT_LOGIN_ON_GET = True  # Автоматический вход при GET запросе
SOCIALACCOUNT_EMAIL_AUTHENTICATION = False  # Не запрашивать email дополнительно  
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True  # Автоматическое подключение email

# =====================================
# ОТКЛЮЧЕНИЕ ДУБЛИРОВАННЫХ СООБЩЕНИЙ ALLAUTH
# =====================================

# Настройки сообщений
MESSAGE_TAGS = {
    10: 'debug',
    20: 'info', 
    25: 'success',
    30: 'warning',
    40: 'error',
}

# Отключаем дополнительные сообщения от allauth
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

# Отключаем дублированные сообщения при социальном входе
SOCIALACCOUNT_STORE_TOKENS = False  # Не сохраняем токены (уменьшает сообщения)

# =====================================
# SEO НАСТРОЙКИ
# =====================================

# Домен сайта для генерации абсолютных URL
SITE_DOMAIN = config('SITE_DOMAIN', default='pravoslavie-portal.ru')
SITE_NAME = 'Добрые истории'
SITE_DESCRIPTION = 'Православный портал с духовными рассказами, книгами, аудио и детскими сказками'

# Настройки для robots.txt
ROBOTS_USE_HOST = True
ROBOTS_USE_SITEMAP = True


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
