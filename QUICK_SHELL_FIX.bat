@echo off
echo ===== БЫСТРОЕ ИСПРАВЛЕНИЕ ЧЕРЕЗ SHELL =====
echo.

cd /d E:\pravoslavie_portal
call .venv\Scripts\activate

echo Запуск Django shell...
python manage.py shell -c "
from stories.models import Story
story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
story.youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
story.youtube_embed_id = 'dQw4w9WgXcQ'
story.save()
print('✅ Видео исправлено! Обновите браузер!')
"

echo.
echo 🚀 ГОТОВО! Обновите страницу в браузере!
pause
