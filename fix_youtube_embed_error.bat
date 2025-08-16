@echo off
echo ====================================
echo 🔧 ИСПРАВЛЕНИЕ ОШИБКИ YOUTUBE_EMBED
echo ====================================
echo.

echo ✅ Ошибка в schema_org.py исправлена!
echo.
echo 📋 Что было исправлено:
echo - Заменено story.youtube_embed на story.youtube_embed_id
echo - Убрана необходимость в регулярных выражениях
echo - Прямое использование ID видео из модели
echo.

echo 🔍 Проверяем синтаксис шаблонов...
python check_template_syntax.py

echo.
echo 🚀 Перезапускаем сервер...
echo Нажмите Ctrl+C чтобы остановить сервер
echo.

python manage.py runserver
