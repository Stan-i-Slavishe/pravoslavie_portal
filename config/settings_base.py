import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

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
    'django_recaptcha',  # Google reCAPTCHA v3
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
    'books',          # книги и публикации
    'audio',          # аудио-контент
    'shop',           # интернет-магазин
    'subscriptions',  # премиум подписки
    'fairy_tales',    # терапевтические сказки
    'analytics',      # аналитика и метрики
    'pwa',           # Progressive Web App функциональность
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'core.middleware.maintenance.MaintenanceModeMiddleware',  # Режим обслуживания (ПОСЛЕ аутентификации!)
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
                'core.context_processors.site_context',
                'core.context_processors.maintenance_context',
                'core.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

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

# Site ID для django-allauth
SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django Allauth settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Django-allauth настройки (новый синтаксис v65+)
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True

# Поля регистрации - email опционален (без звездочки для VK OAuth)
# * означает обязательное поле, без * - опциональное
ACCOUNT_SIGNUP_FIELDS = ['email', 'password1*', 'password2*']

# Кастомные формы allauth с капчей
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email settings (базовые, переопределяются в окружениях)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
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
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Создать папку для логов, если её нет
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# VK OAuth настройки
SOCIALACCOUNT_PROVIDERS = {
    'vk': {
        'SCOPE': ['email'],
    }
}
