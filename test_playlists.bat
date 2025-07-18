@echo off
echo 🔧 Тестирование улучшенной страницы плейлистов...
echo.

REM Активация виртуального окружения
echo 📦 Активация виртуального окружения...
call .venv\Scripts\activate.bat

REM Проверка миграций
echo 🗄️ Проверка миграций...
python manage.py check --deploy

echo.
echo 🚀 Запуск сервера для тестирования...
echo 📍 Откройте: http://127.0.0.1:8000/stories/playlists/
echo.
python manage.py runserver
