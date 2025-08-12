@echo off
echo 🔧 Исправление ошибок и запуск сервера...
cd /d "E:\pravoslavie_portal"

echo 📋 Активация виртуального окружения...
call .venv\Scripts\activate

echo 🧪 Проверка импортов...
python test_imports.py

echo 📊 Проверка миграций...
python manage.py makemigrations --dry-run

echo 🚀 Запуск сервера...
python manage.py runserver

pause
