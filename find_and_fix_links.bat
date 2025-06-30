@echo off
echo ===== ПОИСК И УДАЛЕНИЕ ССЫЛОК НА СТАРЫЙ ФАЙЛ =====
echo.

echo 🔍 Ищем где подключается youtube_comments.js...

echo 📁 Проверяем шаблоны комментариев...
findstr /s /i "youtube_comments" "comments\templates\*.html" 2>nul

echo 📁 Проверяем базовые шаблоны...
findstr /s /i "youtube_comments" "templates\*.html" 2>nul

echo 📁 Проверяем другие шаблоны...
findstr /s /i "youtube_comments" "stories\templates\*.html" 2>nul

echo.
echo 🗑️ Удаляем все старые файлы youtube_comments...
del "stories\static\stories\js\youtube_comments*" 2>nul
del "staticfiles\stories\js\youtube_comments*" 2>nul

echo.
echo 🧹 Очищаем кеш статических файлов...
python manage.py collectstatic --noinput --clear >nul 2>&1

echo.
echo ✅ Очистка завершена!
echo 🔄 Перезапуск сервера...

start http://127.0.0.1:8000/stories/pasha-voskresenie-hristovo/
python manage.py runserver
