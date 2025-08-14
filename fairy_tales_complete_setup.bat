@echo off
echo 🔧 Настройка терапевтических сказок...
echo.

echo 📊 Применение миграций...
python manage.py makemigrations fairy_tales
python manage.py migrate

echo.
echo 🎭 Добавление тестовых данных...
python add_test_fairy_tales.py

echo.
echo 🚀 Запуск сервера...
python manage.py runserver

pause
