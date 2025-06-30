@echo off
echo 🔄 Быстрое обновление системы комментариев...
cd /d "E:\pravoslavie_portal"

echo.
echo 📝 Создание миграций...
python manage.py makemigrations

echo.
echo 🔨 Применение миграций...
python manage.py migrate

echo.
echo ✅ Обновление завершено!
echo 🌐 Запустите сервер: python manage.py runserver
echo 📍 Перейдите на: http://127.0.0.1:8000/stories/

pause
