@echo off
echo 🔄 ПЕРЕЗАПУСК СЕРВЕРА ПОСЛЕ ИСПРАВЛЕНИЙ SCHEMA.ORG
echo ===============================================
cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate

echo 🧪 Запуск тестов исправлений...
python test_schema_fixes.py

echo.
echo 🚀 Запуск Django сервера...
echo ===============================================
python manage.py runserver

pause
