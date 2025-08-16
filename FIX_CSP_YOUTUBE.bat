@echo off
echo ===== ИСПРАВЛЕНИЕ CSP ДЛЯ YOUTUBE =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Исправляем Content Security Policy для YouTube iframe...
python fix_csp_youtube.py

echo.
echo ===== ПЕРЕЗАПУСК СЕРВЕРА =====
echo.
echo Сейчас нужно перезапустить Django сервер чтобы изменения вступили в силу.
echo.

taskkill /f /im python.exe 2>nul
timeout /t 2

echo Запускаем сервер...
python manage.py runserver

pause
