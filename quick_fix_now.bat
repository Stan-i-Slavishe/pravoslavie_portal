@echo off
echo ===== УДАЛЕНИЕ ПРОБЛЕМНОГО JAVASCRIPT =====
echo.

echo 🗑️ Удаляем старый поврежденный файл...
del "stories\static\stories\js\youtube_comments.js" 2>nul

echo 🧹 Очищаем кеш статических файлов...
python manage.py collectstatic --noinput --clear >nul 2>&1

echo 🚀 Перезапускаем сервер...
start http://127.0.0.1:8000/stories/pasha-voskresenie-hristovo/
python manage.py runserver
