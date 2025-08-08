@echo off
echo 🔄 Создаем и применяем миграции после изменения моделей...
echo.

cd /d "E:\pravoslavie_portal"

echo 📝 Создаем миграцию для books (удаление дублирующей модели Tag)...
python manage.py makemigrations books

echo.
echo 🚀 Применяем миграции...
python manage.py migrate

echo.
echo ✅ Миграции завершены!
echo.
echo 🌐 Запускаем сервер...
python manage.py runserver

pause
