#!/bin/bash
# Тестовый скрипт для проверки кнопок-закладок

echo "🔖 Проверка файлов кнопок-закладок..."

# Проверяем CSS файл
if [ -f "static/css/bookmark-buttons.css" ]; then
    echo "✅ CSS файл найден: static/css/bookmark-buttons.css"
else
    echo "❌ CSS файл не найден!"
fi

# Проверяем JS файл
if [ -f "static/js/bookmark-buttons.js" ]; then
    echo "✅ JS файл найден: static/js/bookmark-buttons.js"
else
    echo "❌ JS файл не найден!"
fi

# Проверяем обновленный шаблон
if grep -q "btn-bookmark" templates/books/book_list.html; then
    echo "✅ Шаблон book_list.html обновлен"
else
    echo "❌ Шаблон не обновлен!"
fi

# Проверяем base.html
if grep -q "bookmark-buttons.css" templates/base.html; then
    echo "✅ CSS подключен в base.html"
else
    echo "❌ CSS не подключен в base.html!"
fi

if grep -q "bookmark-buttons.js" templates/base.html; then
    echo "✅ JS подключен в base.html"
else
    echo "❌ JS не подключен в base.html!"
fi

echo ""
echo "🎯 Инструкции для тестирования:"
echo "1. Запустите сервер: python manage.py runserver"
echo "2. Откройте /books/ в браузере"  
echo "3. Проверьте кнопки-закладки рядом с книгами"
echo "4. Кнопки должны быть золотистыми когда активны"
echo "5. При нажатии должны появляться красивые уведомления"
echo ""
echo "🔧 Если что-то не работает:"
echo "- Проверьте консоль браузера на ошибки"
echo "- Убедитесь что пользователь авторизован"
echo "- Проверьте что URL /books/favorite/<id>/ работает"
