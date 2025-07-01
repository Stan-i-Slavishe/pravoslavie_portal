@echo off
echo ========================================
echo   УМЕНЬШЕНИЕ ОТСТУПА МЕЖДУ КНОПКАМИ
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

echo ✅ Отступ уменьшен на 50%!
echo.
echo 📋 Что было изменено:
echo    ✓ Изменен класс с "mb-4" на "mb-2"
echo    ✓ Расстояние между кнопками и комментариями уменьшено вдвое
echo    ✓ Теперь отступ составляет 0.5rem вместо 1.5rem
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/malyshka/
echo.

pause
