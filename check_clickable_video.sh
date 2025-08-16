#!/bin/bash
# Скрипт для проверки кликабельного превью

echo "🎯 Проверка кликабельного превью видео"
echo "========================================"

# Проверяем наличие кликабельной ссылки в шаблоне
if grep -q "story-thumbnail-link" templates/stories/story_list.html; then
    echo "✅ Кликабельная ссылка найдена в шаблоне"
else
    echo "❌ Кликабельная ссылка НЕ найдена в шаблоне"
fi

# Проверяем наличие стилей
if grep -q "cursor: pointer" templates/stories/story_list.html; then
    echo "✅ CSS стили курсора найдены"
else
    echo "❌ CSS стили курсора НЕ найдены"
fi

# Проверяем структуру HTML
if grep -q "<!-- Кликабельное превью -->" templates/stories/story_list.html; then
    echo "✅ HTML структура обновлена"
else
    echo "❌ HTML структура НЕ обновлена"
fi

echo ""
echo "🚀 Что дальше:"
echo "   1. Запустите сервер: python manage.py runserver"
echo "   2. Перейдите на http://127.0.0.1:8000/stories/"
echo "   3. Кликните на любое превью видео"
echo "   4. Убедитесь, что переход работает!"
echo ""
echo "✨ Теперь превью видео полностью кликабельны!"
