@echo off
echo 🚀 Исправление ошибок рассказов
echo ================================

REM Активируем виртуальное окружение
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo ✅ Виртуальное окружение активировано
) else (
    echo ⚠️ Виртуальное окружение не найдено, используем системный Python
)

REM Запускаем скрипт исправления
echo 🔧 Запуск исправления...
python fix_story_detail_errors.py

echo.
echo 📋 После исправления выполните:
echo    1. python manage.py collectstatic --noinput
echo    2. python manage.py runserver
echo    3. Откройте http://127.0.0.1:8000/stories/test-story-fix/

pause
