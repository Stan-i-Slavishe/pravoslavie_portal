#!/bin/bash
echo "🔍 ПРОВЕРКА ИНТЕГРАЦИИ МОБИЛЬНОЙ НАВИГАЦИИ"
echo "============================================="
echo ""

# Проверяем наличие файлов
echo "📁 Проверка файлов:"
if [ -f "static/css/mobile-navigation.css" ]; then
    echo "✅ static/css/mobile-navigation.css - НАЙДЕН"
else
    echo "❌ static/css/mobile-navigation.css - НЕ НАЙДЕН"
fi

if [ -f "static/js/mobile-navigation.js" ]; then
    echo "✅ static/js/mobile-navigation.js - НАЙДЕН"
else
    echo "❌ static/js/mobile-navigation.js - НЕ НАЙДЕН"
fi

if [ -f "templates/base.html" ]; then
    echo "✅ templates/base.html - ОБНОВЛЕН"
else
    echo "❌ templates/base.html - НЕ НАЙДЕН"
fi

if [ -f "templates/base.html.backup" ]; then
    echo "✅ templates/base.html.backup - СОЗДАН"
else
    echo "❌ templates/base.html.backup - НЕ НАЙДЕН"
fi

echo ""
echo "🎨 Проверка CSS переменных:"
if grep -q "fairy-tales-color" "static/css/azbyka-style.css"; then
    echo "✅ Цветовые переменные добавлены"
else
    echo "❌ Цветовые переменные не найдены"
fi

echo ""
echo "📱 Проверка HTML шаблона:"
if grep -q "mobile-bottom-nav" "templates/base.html"; then
    echo "✅ Мобильная навигация добавлена"
else
    echo "❌ Мобильная навигация не найдена"
fi

if grep -q "has-mobile-nav" "templates/base.html"; then
    echo "✅ CSS класс body добавлен"
else
    echo "❌ CSS класс body не найден"
fi

if grep -q "mobile-navigation.css" "templates/base.html"; then
    echo "✅ CSS файл подключен"
else
    echo "❌ CSS файл не подключен"
fi

if grep -q "mobile-navigation.js" "templates/base.html"; then
    echo "✅ JS файл подключен"
else
    echo "❌ JS файл не подключен"
fi

echo ""
echo "🚀 ГОТОВО К ЗАПУСКУ!"
echo "Запустите: python manage.py runserver 8000"
echo "Откройте в мобильном режиме: http://127.0.0.1:8000"
