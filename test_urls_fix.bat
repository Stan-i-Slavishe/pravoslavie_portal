@echo off
echo 🔍 Проверяем URL-ы тегов после исправлений...
echo.

cd /d "E:\pravoslavie_portal"
python check_urls.py

echo.
echo 🚀 Перезапустите Django сервер командой:
echo python manage.py runserver
echo.
echo 📋 Затем проверьте:
echo - http://127.0.0.1:8000/tags/ (список тегов)
echo - http://127.0.0.1:8000/tags/doch/ (детали тега)
echo.
pause
