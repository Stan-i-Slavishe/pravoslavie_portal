# Настройки для гибридного режима: Django локально + базы в Docker
from .settings import *

# Подключение к PostgreSQL в Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pravoslavie_local_db',
        'USER': 'pravoslavie_user',
        'PASSWORD': 'dev_password_123',
        'HOST': '192.168.99.100',  # IP Docker Machine
        'PORT': '5432',
    }
}

# Подключение к Redis в Docker
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://192.168.99.100:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Отладка включена
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.99.100']

# Email в консоль для разработки
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
