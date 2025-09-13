@echo off
echo 🚀 Запуск православного портала локально...

:: Активация виртуального окружения
call .venv\Scripts\activate.bat

:: Применение миграций
echo 📊 Применение миграций...
python manage.py migrate

:: Сбор статики
echo 📁 Сбор статических файлов...
python manage.py collectstatic --noinput

:: Запуск сервера
echo 🌐 Запуск Django сервера на http://127.0.0.1:8000
python manage.py runserver

pause
