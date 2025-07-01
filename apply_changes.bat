@echo off
echo ========================================
echo    ПРИМЕНЕНИЕ ИЗМЕНЕНИЙ ШАБЛОНОВ
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

echo ✅ Изменения применены!
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/malyshka/
echo.
echo 📋 Что было исправлено:
echo    ✓ Создан правильный шаблон story_detail.html
echo    ✓ Добавлены CSS стили для горизонтальных кнопок
echo    ✓ Кнопки теперь должны быть в одной строке
echo.

pause
