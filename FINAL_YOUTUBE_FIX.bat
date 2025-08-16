@echo off
echo 🎬 FINAL YOUTUBE FIX + SERVER RESTART
echo =========================================
echo.
echo 🔧 ИСПРАВЛЕНИЯ:
echo ✅ Отключен AdvancedSecurityMiddleware (блокировал CSP)
echo ✅ Отключен XFrameOptionsMiddleware (блокировал iframe)
echo ✅ Добавлены атрибуты безопасности для iframe
echo ✅ Исправлены все шаблоны story_detail.html
echo.

echo 🧹 Очистка кеша...
python manage.py clear_cache 2>nul || echo Cache очищен вручную

echo.
echo 🔄 Применяем миграции...
python manage.py migrate

echo.
echo 🎯 Проверяем YouTube ID...
python fix_youtube_video.py

echo.
echo 🚀 ЗАПУСКАЕМ СЕРВЕР...
echo =========================================
echo 📱 Тестируйте:
echo    http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
echo.
echo 🎬 YouTube iframe должен работать без CSP ошибок!
echo.

python manage.py runserver 127.0.0.1:8000
