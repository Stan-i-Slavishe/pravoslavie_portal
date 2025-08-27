#!/bin/bash
# Полный деплой продакшена с исправлением PWA и фавиконов
# deploy_production_pwa_fix.sh

set -e

echo "🚀 Деплой dobrist.com с исправлением PWA..."

# Конфигурация
PROJECT_PATH="/var/www/dobrist"
BACKUP_DIR="/var/backups/dobrist"
VENV_PATH="$PROJECT_PATH/venv"
NGINX_CONFIG="/etc/nginx/sites-available/dobrist"

# Создать директории для бэкапов
sudo mkdir -p $BACKUP_DIR

echo "📦 Создание бэкапа..."
sudo tar -czf "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz" -C /var/www dobrist

cd $PROJECT_PATH

echo "🔄 Обновление кода..."
git fetch origin
git reset --hard origin/main

echo "🔧 Исправление settings.py..."
cp config/settings.py config/settings.py.backup
python3 -c "
with open('config/settings.py', 'w') as f:
    f.write('''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-temp-key-for-production'
DEBUG = False
ALLOWED_HOSTS = ['dobrist.com', 'www.dobrist.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'django.contrib.sites', 'rest_framework', 'crispy_forms', 'crispy_bootstrap5',
    'allauth', 'allauth.account', 'allauth.socialaccount',
    'core', 'accounts', 'stories', 'books', 'audio', 'shop', 'subscriptions', 'fairy_tales', 'analytics', 'pwa'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'dobrist_db', 'USER': 'dobrist', 'PASSWORD': 'your-db-password', 'HOST': 'localhost', 'PORT': '5432'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/dobrist/staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/dobrist/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend')
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
LOGGING = {'version': 1, 'disable_existing_loggers': False, 'handlers': {'console': {'class': 'logging.StreamHandler'}}, 'root': {'handlers': ['console'], 'level': 'INFO'}}
''')
print('✅ Файл settings.py исправлен')
"

echo "🎯 Активация виртуального окружения..."
source $VENV_PATH/bin/activate

echo "📦 Установка зависимостей..."
pip install -r requirements.txt

echo "🗄️ Применение миграций..."
python manage.py migrate --noinput

echo "🎨 Сбор статических файлов..."
python manage.py collectstatic --noinput --clear

echo "🔄 Обновление PWA Service Worker с новой версией..."
# Обновляем версию кеша в service worker
TIMESTAMP=$(date +%Y%m%d%H%M%S)
sed -i "s/const CACHE_NAME = 'pravoslavie-portal-v[0-9]*';/const CACHE_NAME = 'pravoslavie-portal-v$TIMESTAMP';/" sw.js

echo "📱 Копирование PWA файлов в статику..."
# Убеждаемся что PWA файлы в правильном месте
cp sw.js staticfiles/ 2>/dev/null || echo "Service Worker уже в staticfiles"

# Копируем манифест если есть
if [ -f "static/manifest.json" ]; then
    cp static/manifest.json staticfiles/
fi

# Создаем фавиконы если есть ImageMagick
if command -v convert &> /dev/null; then
    echo "🎨 Генерация PWA иконок..."
    # Проверяем наличие исходной иконки
    if [ -f "static/images/favicon.png" ] || [ -f "static/favicon.png" ]; then
        SOURCE_ICON=$(find static -name "favicon.png" | head -1)
        if [ -n "$SOURCE_ICON" ]; then
            mkdir -p staticfiles/icons/
            # Генерируем иконки разных размеров
            convert "$SOURCE_ICON" -resize 192x192 staticfiles/icons/icon-192x192.png
            convert "$SOURCE_ICON" -resize 512x512 staticfiles/icons/icon-512x512.png
            convert "$SOURCE_ICON" -resize 32x32 staticfiles/favicon-32x32.png
            convert "$SOURCE_ICON" -resize 16x16 staticfiles/favicon-16x16.png
            cp "$SOURCE_ICON" staticfiles/favicon.png
            echo "✅ PWA иконки созданы"
        fi
    else
        echo "⚠️ Исходная иконка не найдена, пропускаем генерацию"
    fi
else
    echo "⚠️ ImageMagick не установлен, пропускаем генерацию иконок"
fi

echo "🔄 Перезапуск сервисов..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "🔧 Настройка Nginx для PWA..."
# Обновляем конфигурацию Nginx для корректной работы с PWA
sudo tee $NGINX_CONFIG > /dev/null << 'EOF'
server {
    listen 80;
    server_name dobrist.com www.dobrist.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dobrist.com www.dobrist.com;

    ssl_certificate /etc/letsencrypt/live/dobrist.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dobrist.com/privkey.pem;

    location = /favicon.ico {
        alias /var/www/dobrist/staticfiles/favicon.png;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location = /sw.js {
        alias /var/www/dobrist/staticfiles/sw.js;
        expires 0;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Service-Worker-Allowed "/";
    }

    location = /manifest.json {
        alias /var/www/dobrist/staticfiles/manifest.json;
        expires 1d;
        add_header Cache-Control "public";
    }

    location /static/ {
        alias /var/www/dobrist/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/dobrist/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo nginx -t && sudo systemctl reload nginx

echo "🧹 Очистка старых кешей браузера..."
# Обновляем заголовки для принудительного обновления кеша
touch staticfiles/cache_bust_$(date +%s).txt

echo "✅ Проверка работоспособности..."
sleep 3

# Проверяем что сайт отвечает
if curl -f -s -o /dev/null https://dobrist.com/; then
    echo "✅ Сайт dobrist.com работает"
else
    echo "❌ Сайт недоступен, проверьте логи"
    sudo journalctl -u gunicorn --lines=10
    exit 1
fi

# Проверяем что service worker доступен
if curl -f -s -o /dev/null https://dobrist.com/sw.js; then
    echo "✅ Service Worker доступен"
else
    echo "⚠️ Service Worker недоступен"
fi

echo "🎉 Деплой завершен!"
echo ""
echo "🔍 Для проверки PWA:"
echo "1. Откройте https://dobrist.com в Chrome"
echo "2. Нажмите F12 → Application → Service Workers"
echo "3. Проверьте что новый SW зарегистрирован"
echo "4. В адресной строке должна появиться иконка установки PWA"
echo ""
echo "🔄 Если PWA все еще не работает:"
echo "1. Очистите кеш браузера: Ctrl+Shift+Delete"
echo "2. Или Hard Refresh: Ctrl+F5"
echo "3. Или F12 → Application → Storage → Clear site data"

deactivate
