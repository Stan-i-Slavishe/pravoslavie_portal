@echo off
chcp 65001 >nul
echo ===== ТЕСТИРОВАНИЕ ЗАГРУЗКИ КОММЕНТАРИЕВ =====
echo.

echo Создаем тестовые комментарии для проверки...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story, StoryComment
from django.contrib.auth import get_user_model

User = get_user_model()

# Получаем первый рассказ
story = Story.objects.first()
if not story:
    print('❌ Нет рассказов в базе данных')
    exit()

# Получаем или создаем пользователя
user, created = User.objects.get_or_create(username='testuser')
if created:
    user.set_password('password123')
    user.save()

print(f'📝 Рассказ: {story.title}')
print(f'👤 Пользователь: {user.username}')

# Создаем тестовые комментарии
for i in range(10):
    comment_text = f'Тестовый комментарий номер {i+1}. Это очень интересный рассказ!'
    StoryComment.objects.get_or_create(
        story=story,
        user=user,
        text=comment_text,
        defaults={'is_approved': True}
    )

total_comments = StoryComment.objects.filter(story=story).count()
print(f'✅ Всего комментариев: {total_comments}')
print(f'🔗 URL для тестирования: http://127.0.0.1:8000/stories/{story.slug}/')
"

echo.
echo Запустить Django сервер для тестирования? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo Запускаем сервер...
    python manage.py runserver
)

pause
