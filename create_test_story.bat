@echo off
echo ===== СОЗДАНИЕ ТЕСТОВОГО РАССКАЗА =====
echo.

echo 🔧 Создаем тестовый рассказ для комментариев...

python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from core.models import Category

# Создаем категорию
category, created = Category.objects.get_or_create(
    name='Тестовая категория',
    defaults={'slug': 'testovaya-kategoriya', 'description': 'Для тестирования'}
)

# Создаем рассказ
story, created = Story.objects.get_or_create(
    slug='testovyy-rasskaz-dlya-kommentariev',
    defaults={
        'title': 'Тестовый рассказ для комментариев',
        'description': 'Этот рассказ создан специально для тестирования системы комментариев.',
        'youtube_embed_id': 'dQw4w9WgXcQ',
        'category': category,
        'views_count': 0
    }
)

if created:
    print('✅ Создан новый тестовый рассказ!')
else:
    print('✅ Тестовый рассказ уже существует!')

print(f'📖 Название: {story.title}')
print(f'🔗 Slug: {story.slug}')
print(f'🌐 URL: http://127.0.0.1:8000/stories/{story.slug}/')
"

echo.
echo 🎉 ГОТОВО!
echo 🌐 Теперь откройте: http://127.0.0.1:8000/stories/testovyy-rasskaz-dlya-kommentariev/
echo 💬 Комментарии должны работать!
echo.

start http://127.0.0.1:8000/stories/testovyy-rasskaz-dlya-kommentariev/
pause
