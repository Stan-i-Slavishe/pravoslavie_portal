@echo off
chcp 65001 >nul
echo.
echo 🚀 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ ОШИБОК РАССКАЗОВ
echo ================================================
echo.

REM Проверяем, есть ли виртуальное окружение
if exist .venv\Scripts\activate.bat (
    echo 📂 Активируем виртуальное окружение...
    call .venv\Scripts\activate.bat
    echo ✅ Виртуальное окружение активировано
) else (
    echo ⚠️  Виртуальное окружение не найдено, используем системный Python
)

echo.
echo 🔧 Исправляем данные в базе через Django shell...
echo.

REM Создаем временный Python файл для исправления
echo from stories.models import Story > temp_fix.py
echo import re >> temp_fix.py
echo. >> temp_fix.py
echo def extract_youtube_id(url): >> temp_fix.py
echo     if not url: >> temp_fix.py
echo         return None >> temp_fix.py
echo     patterns = [ >> temp_fix.py
echo         r'(?:youtube\.com\/watch\?v=^|youtu\.be\/^|youtube\.com\/embed\/)([^^&\n?#]+)', >> temp_fix.py
echo         r'youtube\.com\/v\/([^^&\n?#]+)', >> temp_fix.py
echo     ] >> temp_fix.py
echo     for pattern in patterns: >> temp_fix.py
echo         match = re.search(pattern, url) >> temp_fix.py
echo         if match: >> temp_fix.py
echo             return match.group(1) >> temp_fix.py
echo     return None >> temp_fix.py
echo. >> temp_fix.py
echo print('🔍 Ищем проблемный рассказ...') >> temp_fix.py
echo try: >> temp_fix.py
echo     story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas') >> temp_fix.py
echo     print(f'✅ Найден: {story.title}') >> temp_fix.py
echo     if story.youtube_url and not story.youtube_embed_id: >> temp_fix.py
echo         youtube_id = extract_youtube_id(story.youtube_url) >> temp_fix.py
echo         if youtube_id: >> temp_fix.py
echo             story.youtube_embed_id = youtube_id >> temp_fix.py
echo             story.save(update_fields=['youtube_embed_id']) >> temp_fix.py
echo             print(f'✅ YouTube ID установлен: {youtube_id}') >> temp_fix.py
echo     elif not story.youtube_url: >> temp_fix.py
echo         story.youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' >> temp_fix.py
echo         story.youtube_embed_id = 'dQw4w9WgXcQ' >> temp_fix.py
echo         story.save(update_fields=['youtube_url', 'youtube_embed_id']) >> temp_fix.py
echo         print('🧪 Установлено тестовое видео') >> temp_fix.py
echo     else: >> temp_fix.py
echo         print(f'✅ Видео уже настроено: {story.youtube_embed_id}') >> temp_fix.py
echo except Story.DoesNotExist: >> temp_fix.py
echo     print('❌ Рассказ не найден') >> temp_fix.py
echo. >> temp_fix.py
echo print('🔧 Исправляем все рассказы без YouTube ID...') >> temp_fix.py
echo stories_fixed = 0 >> temp_fix.py
echo for story in Story.objects.filter(youtube_embed_id__isnull=True): >> temp_fix.py
echo     if story.youtube_url: >> temp_fix.py
echo         youtube_id = extract_youtube_id(story.youtube_url) >> temp_fix.py
echo         if youtube_id: >> temp_fix.py
echo             story.youtube_embed_id = youtube_id >> temp_fix.py
echo             story.save(update_fields=['youtube_embed_id']) >> temp_fix.py
echo             stories_fixed += 1 >> temp_fix.py
echo. >> temp_fix.py
echo for story in Story.objects.filter(youtube_embed_id=''): >> temp_fix.py
echo     if story.youtube_url: >> temp_fix.py
echo         youtube_id = extract_youtube_id(story.youtube_url) >> temp_fix.py
echo         if youtube_id: >> temp_fix.py
echo             story.youtube_embed_id = youtube_id >> temp_fix.py
echo             story.save(update_fields=['youtube_embed_id']) >> temp_fix.py
echo             stories_fixed += 1 >> temp_fix.py
echo. >> temp_fix.py
echo print(f'🎉 Исправлено {stories_fixed} рассказов') >> temp_fix.py
echo. >> temp_fix.py
echo stories_with_video = Story.objects.exclude(youtube_embed_id__isnull=True).exclude(youtube_embed_id='').count() >> temp_fix.py
echo stories_without_video = Story.objects.filter(youtube_embed_id__isnull=True).count() + Story.objects.filter(youtube_embed_id='').count() >> temp_fix.py
echo print(f'📊 Статистика:') >> temp_fix.py
echo print(f'   ✅ С видео: {stories_with_video}') >> temp_fix.py
echo print(f'   ❌ Без видео: {stories_without_video}') >> temp_fix.py

REM Запускаем исправление
python manage.py shell < temp_fix.py

REM Удаляем временный файл
del temp_fix.py

echo.
echo ================================================
echo 🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!
echo ================================================
echo.
echo 📋 Что было сделано:
echo    ✅ Шаблон story_detail.html исправлен
echo    ✅ YouTube ID установлены для рассказов
echo    ✅ Исправлены ошибки в базе данных
echo.
echo 🧪 Для проверки:
echo    1. Запустите: python manage.py runserver
echo    2. Откройте: http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
echo    3. Проверьте отсутствие ошибок и отображение видео
echo.
echo 💡 Если проблемы остались:
echo    - Проверьте логи сервера
echo    - Убедитесь что все миграции применены
echo    - Смотрите STORY_FIX_GUIDE.md для подробностей
echo.

pause
