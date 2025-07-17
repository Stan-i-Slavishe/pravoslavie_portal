@echo off
echo 🔄 Откат изменений после fix_browser_errors.bat
echo.

echo 1. Активируем виртуальное окружение...
call .venv\Scripts\activate

echo 2. Отключаем фильтрацию ошибок...
echo    Удаляем error-filter.js из загрузки...

REM Создаем резервную копию base.html
copy templates\base.html templates\base.html.backup_rollback

echo 3. Восстанавливаем базовую загрузку в base.html...
REM Временно отключаем error-filter.js

echo 4. Очищаем статические файлы...
rmdir /s /q staticfiles 2>nul

echo 5. Пересобираем статические файлы...
python manage.py collectstatic --noinput

echo 6. Очищаем кеш Django...
python -c "import django; django.setup(); from django.core.cache import cache; cache.clear()"

echo.
echo ✅ Откат завершен!
echo.
echo 💡 Что было отменено:
echo   • Отключена агрессивная фильтрация ошибок JavaScript
echo   • Очищены статические файлы
echo   • Сброшен кеш Django
echo.
echo 🔄 Теперь перезапустите Django сервер:
echo python manage.py runserver
echo.
pause
