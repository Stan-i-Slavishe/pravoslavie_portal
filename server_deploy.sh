#!/bin/bash

echo "=========================================="
echo "🚀 Синхронизация изменений на продакшен"
echo "=========================================="

echo "📂 Переходим в директорию проекта..."
cd /var/www/pravoslavie_portal

echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate

echo "📥 Получаем последние изменения из GitHub..."
git pull origin main

echo "🔄 Перезапускаем сервисы..."
sudo systemctl reload nginx
sudo systemctl restart pravoslavie_portal

echo "🔍 Проверяем статус сервисов..."
sudo systemctl status nginx --no-pager -l
sudo systemctl status pravoslavie_portal --no-pager -l

echo "✅ Деплой завершен!"
echo "🌐 Проверьте результат на сайте"
