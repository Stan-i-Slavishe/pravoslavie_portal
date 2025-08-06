@echo off
echo ========================================
echo   ПРИМЕНЕНИЕ ИСПРАВЛЕНИЯ НАВИГАЦИИ
echo ========================================

echo 1. Останавливаем сервер разработки...
taskkill /f /im python.exe 2>nul

echo 2. Собираем статические файлы...
python manage.py collectstatic --noinput

echo 3. Очищаем кеш браузера...
echo Откройте DevTools (F12) и нажмите Ctrl+Shift+R для принудительного обновления

echo 4. Запускаем сервер...
start cmd /k "python manage.py runserver 127.0.0.1:8000"

echo ========================================
echo   ИСПРАВЛЕНИЕ ПРИМЕНЕНО!
echo ========================================
echo Перейдите на http://127.0.0.1:8000/shop/?type=subscription
echo И проверьте мобильную версию (F12 -> Toggle Device Toolbar)
echo.

pause
