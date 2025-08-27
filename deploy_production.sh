#!/bin/bash
# 🚀 Скрипт деплоя на продакшен сервер
# Файл: deploy_production.sh

set -e  # Остановиться при ошибке

echo "🚀 Деплой проекта dobrist.com на продакшен..."

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Конфигурация (настроить под ваш сервер)
PROJECT_PATH="/var/www/dobrist.com"
VENV_PATH="$PROJECT_PATH/venv"
SERVICE_NAME="dobrist"
NGINX_SERVICE="nginx"

# Проверка прав
if [ "$EUID" -ne 0 ]; then 
    error "Запустите с правами root: sudo $0"
    exit 1
fi

log "📦 Создание бэкапа..."
BACKUP_DIR="/var/backups/dobrist_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r "$PROJECT_PATH" "$BACKUP_DIR/"
log "✅ Бэкап: $BACKUP_DIR"

cd "$PROJECT_PATH"

log "💾 Сохранение локальных изменений..."
git stash push -m "Production backup $(date)"

log "⬇️ Обновление кода..."
git fetch origin
git pull origin main

log "📋 Установка продакшен настроек..."
# Копируем продакшен настройки в основной .env
cp .env.production .env

log "🔧 Обновление зависимостей..."
source "$VENV_PATH/bin/activate"
pip install -r requirements.txt

log "🗄️ Миграции базы данных..."
python manage.py migrate --noinput

log "📁 Сбор статических файлов..."
python manage.py collectstatic --clear --noinput

log "🔄 Обновление Service Worker..."
if [ -f "static/sw.js" ]; then
    NEW_VERSION="pravoslavie-portal-v$(date +%s)"
    sed -i "s/const CACHE_NAME = 'pravoslavie-portal-v[^']*'/const CACHE_NAME = '$NEW_VERSION'/" static/sw.js
    log "✅ SW версия: $NEW_VERSION"
fi

log "🖼️ Проверка PWA иконок..."
ICONS_DIR="static/icons"
REQUIRED_ICONS=("icon-72x72.png" "icon-192x192.png" "icon-512x512.png" "favicon.svg")

for icon in "${REQUIRED_ICONS[@]}"; do
    if [ ! -f "$ICONS_DIR/$icon" ]; then
        warning "Отсутствует: $ICONS_DIR/$icon"
        # Создаем простую иконку если её нет
        if command -v convert &> /dev/null; then
            # Создаем временную SVG иконку
            cat > temp_icon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192">
  <rect width="192" height="192" fill="#2B5AA0"/>
  <text x="96" y="120" font-family="Arial" font-size="100" fill="#D4AF37" text-anchor="middle">✝</text>
</svg>
EOF
            if [[ $icon == *.png ]]; then
                size=${icon%%.png}
                size=${size##*-}
                convert temp_icon.svg -resize ${size} "$ICONS_DIR/$icon"
                log "✅ Создана иконка: $icon"
            elif [[ $icon == *.svg ]]; then
                cp temp_icon.svg "$ICONS_DIR/$icon"
                log "✅ Создана иконка: $icon"
            fi
            rm -f temp_icon.svg
        fi
    else
        log "✅ Иконка найдена: $icon"
    fi
done

log "🔄 Финальный сбор статики..."
python manage.py collectstatic --noinput

log "🌐 Проверка Nginx конфигурации..."
nginx -t
if [ $? -eq 0 ]; then
    log "✅ Nginx конфигурация OK"
else
    error "❌ Ошибка Nginx конфигурации"
    exit 1
fi

log "🔄 Перезапуск сервисов..."
systemctl restart "$SERVICE_NAME"
systemctl reload "$NGINX_SERVICE"

log "📊 Проверка статуса..."
sleep 3

if systemctl is-active --quiet "$SERVICE_NAME"; then
    log "✅ Django сервис запущен"
else
    error "❌ Проблема с Django сервисом"
    systemctl status "$SERVICE_NAME"
    exit 1
fi

if systemctl is-active --quiet "$NGINX_SERVICE"; then
    log "✅ Nginx запущен"
else
    error "❌ Проблема с Nginx"
    systemctl status "$NGINX_SERVICE"
    exit 1
fi

log "🧹 Очистка кэша..."
python manage.py shell -c "
from django.core.cache import cache
try:
    cache.clear()
    print('✅ Кэш очищен')
except Exception as e:
    print(f'⚠️ Кэш не очищен: {e}')
" || warning "Не удалось очистить кэш"

log "🌍 Проверка доступности сайта..."
sleep 2
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://dobrist.com/ || echo "000")
if [ "$HTTP_CODE" -eq 200 ]; then
    log "✅ Сайт доступен (HTTP $HTTP_CODE)"
else
    warning "⚠️ Сайт возвращает код $HTTP_CODE"
fi

log "🔍 Проверка критических файлов..."
CRITICAL_FILES=(
    "staticfiles/manifest.json"
    "staticfiles/sw.js"
    "staticfiles/icons/icon-192x192.png"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        log "✅ $file"
    else
        warning "⚠️ Отсутствует: $file"
    fi
done

# Установка правильных прав доступа
log "🔒 Установка прав доступа..."
chown -R www-data:www-data "$PROJECT_PATH/media/"
chown -R www-data:www-data "$PROJECT_PATH/staticfiles/"
chmod -R 755 "$PROJECT_PATH/media/"
chmod -R 755 "$PROJECT_PATH/staticfiles/"

echo ""
log "🎉 Деплой завершен успешно!"
echo ""
echo -e "${GREEN}📋 Что проверить:${NC}"
echo "1. 🌐 https://dobrist.com - основной сайт"
echo "2. 📱 PWA установка (иконка в адресной строке)"
echo "3. 🔧 F12 → Application → Service Workers"
echo "4. 📖 Все разделы: сказки, книги, магазин"
echo ""
echo -e "${YELLOW}🛠️ Для отладки:${NC}"
echo "- Логи Django: journalctl -u $SERVICE_NAME -f"
echo "- Логи Nginx: tail -f /var/log/nginx/error.log"
echo "- Статус: systemctl status $SERVICE_NAME"
echo ""
echo -e "${GREEN}🎊 dobrist.com обновлен до последней версии!${NC}"
