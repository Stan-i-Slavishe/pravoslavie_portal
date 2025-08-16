@echo off
echo ✅ Исправление админки применено!
echo 📋 Отключены проблемные middleware:
echo    - stories.middleware.AdminPerformanceMiddleware
echo    - stories.middleware.DatabaseOptimizationMiddleware
echo.
echo 🔄 Перезапускаем сервер...
echo.

cd /d "E:\pravoslavie_portal"

REM Останавливаем текущий сервер если он запущен
taskkill /f /im python.exe 2>nul

REM Ждем 2 секунды
timeout /t 2 /nobreak > nul

REM Запускаем сервер заново
echo 🚀 Запускаем сервер с исправлениями...
python manage.py runserver 127.0.0.1:8000

pause
