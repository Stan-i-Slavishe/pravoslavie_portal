@echo off
echo 🔧 Исправили конфликт в админке - пробуем запустить сервер...
echo.

cd /d "E:\pravoslavie_portal"

echo 🚀 Запускаем Django сервер...
python manage.py runserver

echo.
echo 💡 Если сервер запустился успешно:
echo Проверьте: http://127.0.0.1:8000/tags/doch/
echo.
pause
