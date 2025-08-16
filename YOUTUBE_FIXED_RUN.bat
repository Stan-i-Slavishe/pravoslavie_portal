@echo off
echo 🎬 YOUTUBE VIDEO FIX + RESTART SERVER
echo =======================================
echo.
echo 📝 Исправления:
echo ✅ Отключен CSP для YouTube iframe
echo ✅ Исправлен X-Frame-Options  
echo ✅ Добавлены атрибуты iframe для безопасности
echo ✅ Исправлен основной шаблон story_detail.html
echo ✅ Исправлен stories/templates шаблон
echo.

echo 🔧 Запускаем скрипт исправления YouTube ID...
python fix_youtube_video.py

echo.
echo 🔥 Применяем миграции...
python manage.py migrate

echo.
echo 🧹 Собираем статику...
python manage.py collectstatic --noinput

echo.
echo 🚀 ЗАПУСКАЕМ СЕРВЕР...
echo =======================================
echo 📱 Откройте браузер:
echo    http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
echo.
echo 🎬 YouTube видео должно работать!
echo.

python manage.py runserver
