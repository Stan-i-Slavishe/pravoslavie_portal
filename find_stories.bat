@echo off
echo ===== ПОИСК СУЩЕСТВУЮЩИХ РАССКАЗОВ =====
echo.

echo 📚 Ищем рассказы в базе данных...

python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

stories = Story.objects.all()
print(f'📊 Всего рассказов: {stories.count()}')
print()

if stories.exists():
    print('📋 Список всех рассказов:')
    for i, story in enumerate(stories, 1):
        print(f'{i}. {story.title}')
        print(f'   Slug: {story.slug}')
        print(f'   URL: http://127.0.0.1:8000/stories/{story.slug}/')
        print('   ---')
else:
    print('❌ Рассказы не найдены!')
    print('🔧 Создаем тестовый рассказ...')
    
    # Создаем тестовый рассказ
    from core.models import Category
    
    # Создаем категорию если нет
    category, created = Category.objects.get_or_create(
        name='Тестовая категория',
        defaults={'slug': 'testovaya-kategoriya', 'description': 'Категория для тестов'}
    )
    
    # Создаем рассказ
    story = Story.objects.create(
        title='Тестовый рассказ для комментариев',
        slug='testovyy-rasskaz-dlya-kommentariev',
        description='Этот рассказ создан для тестирования системы комментариев',
        youtube_embed_id='dQw4w9WgXcQ',  # Rick Roll для теста :)
        category=category,
        views_count=0
    )
    
    print(f'✅ Создан тестовый рассказ:')
    print(f'   Название: {story.title}')
    print(f'   Slug: {story.slug}')
    print(f'   URL: http://127.0.0.1:8000/stories/{story.slug}/')
"

echo.
echo 🚀 Теперь попробуйте открыть один из URL'ов выше!
echo.
pause
