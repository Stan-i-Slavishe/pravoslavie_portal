#!/bin/bash

echo "🔄 Создание вечного православного календаря..."

echo "📝 Создание миграций..."
cd /d E:\pravoslavie_portal
python manage.py makemigrations pwa

echo "🗄️ Применение миграций..."
python manage.py migrate

echo "📅 Создание базовых данных календаря..."
python manage.py create_eternal_calendar --clear

echo "✅ Вечный православный календарь готов!"
echo ""
echo "🧪 Для тестирования откройте:"
echo "   http://127.0.0.1:8000/pwa/daily-calendar/"
echo ""
echo "📊 Календарь теперь автоматически определяет:"
echo "   🔴 Великие праздники"
echo "   🟣 Все типы постов" 
echo "   ⚪ Обычные дни"
echo ""
echo "🚀 Календарь работает для ЛЮБОГО года!"
