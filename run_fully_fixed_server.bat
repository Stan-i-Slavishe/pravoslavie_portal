@echo off
echo ===============================================
echo ИСПРАВЛЕНИЕ ОШИБКИ youtube_embed ЗАВЕРШЕНО!
echo ===============================================

cd /d E:\pravoslavie_portal

echo.
echo ✅ Исправлено:
echo    1. Шаблон story_detail.html - убраны стили между блоками
echo    2. Schema.org генератор - добавлена поддержка youtube_embed_id
echo    3. Модель Story - добавлен алиас youtube_embed для совместимости
echo.

echo 🚀 Запускаю сервер...
echo.
echo Теперь откройте в браузере:
echo http://127.0.0.1:8000/stories/pochti-pokojnik/
echo.

call .venv\Scripts\activate.bat
python manage.py runserver
