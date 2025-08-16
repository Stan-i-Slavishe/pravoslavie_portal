@echo off
echo ===== ИСПРАВЛЕНИЕ YOUTUBE_EMBED_ID ОШИБКИ =====
echo.
echo ✅ Исправлено: story.youtube_embed -> story.youtube_embed_id
echo ✅ Файл: core/seo/schema_org.py
echo.
echo Перезапуск сервера...

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запуск Django сервера...
python manage.py runserver

pause
