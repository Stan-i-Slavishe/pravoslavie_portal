#!/bin/bash
# Скрипт проверки применения исправлений мобильной навигации

echo "🔧 Проверка исправлений мобильной навигации..."
echo "==============================================="

# Проверяем наличие нового CSS файла
if [ -f "static/css/mobile-icons-spacing-fix.css" ]; then
    echo "✅ Файл mobile-icons-spacing-fix.css найден"
    echo "   Размер: $(wc -c < static/css/mobile-icons-spacing-fix.css) байт"
else
    echo "❌ Файл mobile-icons-spacing-fix.css НЕ найден"
fi

# Проверяем подключение в base.html
if grep -q "mobile-icons-spacing-fix.css" templates/base.html; then
    echo "✅ CSS файл подключен в base.html"
else
    echo "❌ CSS файл НЕ подключен в base.html"
fi

# Проверяем обновления в mobile-burger-menu.css  
if grep -q "ИСПРАВЛЕНИЕ НАЛОЖЕНИЯ КОРЗИНЫ И БУРГЕРА" static/css/mobile-burger-menu.css; then
    echo "✅ Исправления добавлены в mobile-burger-menu.css"
else
    echo "❌ Исправления НЕ найдены в mobile-burger-menu.css"
fi

echo ""
echo "🚀 Для применения изменений:"
echo "1. python manage.py collectstatic --noinput"
echo "2. Перезапустите сервер"
echo "3. Очистите кеш браузера (Ctrl+F5)"
echo ""
echo "📱 Тестируйте на экранах шире 992px - должен исчезнуть бургер"
echo "📱 Тестируйте на мобильных - корзина слева, бургер справа"
