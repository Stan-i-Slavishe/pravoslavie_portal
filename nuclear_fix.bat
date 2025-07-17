@echo off
chcp 65001 >nul
echo 🚨 КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ - HTTPS проблема
echo.

REM Полностью убиваем все процессы
echo 💀 Убиваем ВСЕ процессы Python...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1
wmic process where "name like '%%python%%'" delete >nul 2>&1

echo ⏳ Ждем 5 секунд...
timeout /t 5 /nobreak >nul

echo 🌐 Очищаем кеш браузера и DNS...
ipconfig /flushdns >nul
netsh winsock reset >nul

echo 📂 Переходим в проект...
cd /d "E:\pravoslavie_portal"

echo 🐍 Активируем окружение...
call .venv\Scripts\activate

echo 🔧 Создаем супер-чистые настройки...
echo DEBUG=True > .env
echo SECRET_KEY=django-insecure-clean-start >> .env
echo ALLOWED_HOSTS=127.0.0.1,localhost >> .env
echo USE_TZ=False >> .env
echo LANGUAGE_CODE=en-us >> .env

echo 🗑️ Удаляем ВСЕ проблемные файлы...
if exist staticfiles rmdir /s /q staticfiles
if exist logs rmdir /s /q logs
if exist __pycache__ rmdir /s /q __pycache__
if exist "static\js\error-filter.js" del "static\js\error-filter.js"

echo 📦 Пересобираем статику БЕЗ кеша...
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=1
python manage.py collectstatic --noinput --clear

echo.
echo ✅ Готово! Теперь запускаем на другом порту...
echo.
echo 🌐 ВАЖНО: Сервер будет на порту 8080!
echo 🌐 Откройте браузер и идите на: http://127.0.0.1:8080
echo 🌐 НЕ ИСПОЛЬЗУЙТЕ порт 8000!
echo.

set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=1
set DJANGO_SETTINGS_MODULE=config.settings
python manage.py runserver 127.0.0.1:8080

pause
