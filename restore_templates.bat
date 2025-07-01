@echo off
echo ========================================
echo   ВОССТАНОВЛЕНИЕ И ИСПРАВЛЕНИЕ ШАБЛОНОВ
echo ========================================
echo.

echo 🗂️ Переходим в директорию проекта...
cd /d "E:\pravoslavie_portal"

echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo 🔄 Очищаем кэш Django...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Кэш очищен!')"

echo ✅ Всё восстановлено!
echo.
echo 📋 Что сделано:
echo    ✓ Вернули представления на stories/story_list.html
echo    ✓ Создали файл stories/story_list.html с метаданными комментариев
echo    ✓ В файле есть: [👁️ просмотры] [💬 комментарии]
echo    ✓ Исправили карточки рассказов
echo    ✓ Сохранили оригинальный дизайн
echo.
echo 🎯 Теперь на карточках рассказов должны отображаться:
echo    👁️ Количество просмотров
echo    💬 Количество комментариев
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/
echo.

pause
