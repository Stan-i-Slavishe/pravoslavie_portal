@echo off
chcp 65001 >nul
echo ===== ДИАГНОСТИКА СИСТЕМЫ КОММЕНТАРИЕВ =====
echo.

echo 🔍 Проверяем состояние комментариев в базе данных...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story, StoryComment
from django.contrib.auth import get_user_model

print('📊 СТАТИСТИКА КОММЕНТАРИЕВ')
print('=' * 50)

stories = Story.objects.all()
print(f'📚 Всего рассказов: {stories.count()}')

if stories.exists():
    for story in stories[:3]:  # Показываем первые 3 рассказа
        total_comments = StoryComment.objects.filter(story=story).count()
        main_comments = StoryComment.objects.filter(story=story, parent=None).count()
        replies = StoryComment.objects.filter(story=story, parent__isnull=False).count()
        approved = StoryComment.objects.filter(story=story, is_approved=True).count()
        
        print(f'\\n📖 {story.title[:50]}...')
        print(f'   • Всего комментариев: {total_comments}')
        print(f'   • Основных комментариев: {main_comments}')
        print(f'   • Ответов: {replies}')
        print(f'   • Одобренных: {approved}')
        print(f'   • URL: /stories/{story.slug}/')

print('\\n' + '=' * 50)
print('✅ Диагностика завершена!')
"

echo.
echo 🌐 Хотите открыть рассказ для проверки счетчика? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo Запускаем сервер и открываем браузер...
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    timeout /t 5
    start http://127.0.0.1:8000/stories/
)

echo.
echo 📋 ИНСТРУКЦИЯ ПО ПРОВЕРКЕ:
echo.
echo 1. В браузере нажмите F12 → Console
echo 2. Перезагрузите страницу с комментариями
echo 3. Ищите логи:
echo    🚀 Инициализация комментариев. Начальное количество: X
echo    📝 Текст badge: Комментарии X
echo.
echo 4. При добавлении комментария должен появиться лог:
echo    📊 Обновление счетчика: X + 1 = Y
echo.
echo 5. Если видите NaN - это означает, что JavaScript
echo    не может извлечь число из текста badge
echo.

pause
