@echo off
echo 🔧 ПОЛНОЕ ИСПРАВЛЕНИЕ И ЗАПУСК СЕРВЕРА
echo ========================================
cd /d "E:\pravoslavie_portal"

echo 📋 Активация виртуального окружения...
call .venv\Scripts\activate

echo 🧹 Очистка кеша Python...
python clean_and_check.py

echo 🧪 Проверка импортов...
python test_imports.py

echo.
echo 📊 Проверка Django системы...
python manage.py check --verbosity=2

echo.
echo 🚀 Запуск сервера Django...
echo ========================================
python manage.py runserver

pause
