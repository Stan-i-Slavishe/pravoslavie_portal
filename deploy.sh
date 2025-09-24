#!/bin/bash
echo "🚀 Деплой православного портала..."
echo "======================================"

# Получаем изменения
echo "📥 Получение изменений с GitHub..."
git pull origin main

# Активируем виртуальное окружение и выполняем команды
echo ""
echo "🔧 Применение миграций БД..."
source venv/bin/activate
python manage.py migrate

echo ""
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput

echo ""
echo "🔄 Перезапуск сервисов..."
systemctl restart gunicorn
systemctl restart nginx

echo ""
echo "✅ Деплой завершен успешно!"
echo "======================================"
echo ""
echo "🔗 Проверьте сайт: https://dobrist.com"
echo "📊 Мониторинг: https://dobrist.com/admin/"
