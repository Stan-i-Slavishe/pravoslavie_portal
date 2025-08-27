#!/bin/bash
# Полный деплой продакшена с исправлениями
# deploy_production_fixed.sh

set -e

echo "Деплой dobrist.com с исправлениями..."

# Конфигурация (настроить под ваш сервер)
PROJECT_PATH="/var/www/dobrist.com"
VENV_PATH="$PROJECT_PATH/venv"
SERVICE_NAME="dobrist"
NGINX_SERVICE="nginx"

# Проверка прав
if [ "$EUID" -ne 0 ]; then 
    echo "Запустите с правами root: sudo $0"
    exit 1
fi

echo "Создание бэкапа..."
BACKUP_DIR="/var/backups/dobrist_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r "$PROJECT_PATH" "$BACKUP_DIR/"
echo "Бэкап создан: $BACKUP_DIR"

cd "$PROJECT_PATH"

echo "Сохранение локальных изменений..."
git stash push -m "Production backup $(date)"

echo "Обновление кода..."
git fetch origin
git pull origin main

echo "Настройка продакшен окружения..."
# Убеждаемся что используем продакшен настройки
export DJANGO_SETTINGS_MODULE=config.settings_production

echo "Активация виртуального окружения..."
source "$VENV_PATH/bin/activate"

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Копирование продакшен настроек..."
cp .env.production .env

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Создание недостающих папок..."
mkdir -p logs
mkdir -p /var/log/dobrist
chown -R www-data:www-data /var/log/dobrist

echo "Сбор статических файлов..."
python manage.py collectstatic --clear --noinput

echo "Обновление Service Worker версии..."
if [ -f "static/sw.js" ]; then
    NEW_VERSION="pravoslavie-portal-v$(date +%s)"
    sed -i "s/const CACHE_NAME = 'pravoslavie-portal-v[^']*'/const CACHE_NAME = '$NEW_VERSION'/" static/sw.js
    echo "Service Worker обновлен: $NEW_VERSION"
fi

echo "Проверка и создание PWA иконок..."
ICONS_DIR="static/icons"
mkdir -p "$ICONS_DIR"

# Создание иконок если отсутствуют
if [ ! -f "$ICONS_DIR/icon-192x192.png" ] && command -v convert &> /dev/null; then
    echo "Создание PWA иконок..."
    
    # Создаем SVG иконку
    cat > temp_icon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
  <rect width="192" height="192" fill="#2B5AA0"/>
  <text x="96" y="120" font-family="Arial" font-size="80" fill="#D4AF37" text-anchor="middle" font-weight="bold">✝</text>
</svg>
EOF
    
    convert temp_icon.svg -resize 72x72 "$ICONS_DIR/icon-72x72.png"
    convert temp_icon.svg -resize 192x192 "$ICONS_DIR/icon-192x192.png"
    convert temp_icon.svg -resize 512x512 "$ICONS_DIR/icon-512x512.png"
    cp temp_icon.svg "$ICONS_DIR/favicon.svg"
    rm temp_icon.svg
    echo "PWA иконки созданы"
fi

echo "Финальный сбор статики с PWA файлами..."
python manage.py collectstatic --noinput

echo "Установка правильных прав доступа..."
chown -R www-data:www-data "$PROJECT_PATH/media/"
chown -R www-data:www-data "$PROJECT_PATH/staticfiles/"
chmod -R 755 "$PROJECT_PATH/media/"
chmod -R 755 "$PROJECT_PATH/staticfiles/"

echo "Проверка Nginx конфигурации..."
nginx -t
if [ $? -ne 0 ]; then
    echo "Ошибка в конфигурации Nginx"
    exit 1
fi

echo "Перезапуск сервисов..."
systemctl restart "$SERVICE_NAME"
systemctl reload "$NGINX_SERVICE"

echo "Проверка статуса сервисов..."
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Django сервис запущен"
else
    echo "Проблема с Django сервисом"
    systemctl status "$SERVICE_NAME"
    exit 1
fi

if systemctl is-active --quiet "$NGINX_SERVICE"; then
    echo "Nginx запущен"
else
    echo "Проблема с Nginx"
    systemctl status "$NGINX_SERVICE"
    exit 1
fi

echo "Очистка кэша..."
python manage.py shell -c "
from django.core.cache import cache
try:
    cache.clear()
    print('Кэш очищен')
except Exception as e:
    print(f'Кэш не очищен: {e}')
" 2>/dev/null || echo "Кэш не настроен"

echo "Проверка доступности сайта..."
sleep 2
if curl -s -o /dev/null -w "%{http_code}" https://dobrist.com/ | grep -q "200"; then
    echo "Сайт доступен"
else
    echo "Проблемы с доступностью сайта"
fi

echo "Проверка PWA файлов..."
PWA_FILES=(
    "staticfiles/manifest.json"
    "staticfiles/sw.js"
    "staticfiles/icons/icon-192x192.png"
    "staticfiles/icons/favicon.svg"
)

for file in "${PWA_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Найден: $file"
    else
        echo "Отсутствует: $file"
    fi
done

echo ""
echo "Деплой завершен!"
echo ""
echo "Проверьте:"
echo "1. https://dobrist.com - основной сайт"
echo "2. F12 → Application → Service Workers"
echo "3. Иконка PWA в адресной строке"
echo "4. Фавикон в табе браузера"
echo ""
echo "Для отладки:"
echo "- Логи Django: journalctl -u $SERVICE_NAME -f"
echo "- Логи Nginx: tail -f /var/log/nginx/error.log"
echo ""
echo "dobrist.com обновлен!"
