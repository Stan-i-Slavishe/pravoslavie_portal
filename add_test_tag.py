import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

from core.models import Tag
from stories.models import Story

try:
    # Проверяем, есть ли тег "дочь"
    tag, created = Tag.objects.get_or_create(
        slug='doch',
        defaults={
            'name': 'дочь',
            'color': '#ff6b9d',
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Создан новый тег: {tag.name}")
    else:
        print(f"✅ Найден существующий тег: {tag.name}")
    
    # Получаем первую историю и добавляем к ней тег
    story = Story.objects.filter(is_published=True).first()
    
    if story:
        # Добавляем тег к истории
        story.tags.add(tag)
        print(f"✅ Тег '{tag.name}' добавлен к истории: {story.title}")
        
        # Проверяем, что тег добавился
        story_tags = [t.name for t in story.tags.all()]
        print(f"Теги истории '{story.title}': {story_tags}")
    else:
        print("❌ Не найдено ни одной опубликованной истории")
    
    # Проверяем количество контента с этим тегом
    stories_with_tag = Story.objects.filter(tags=tag, is_published=True).count()
    print(f"📊 Количество историй с тегом '{tag.name}': {stories_with_tag}")
    
    # Выводим все истории с их тегами
    print("\n📋 Все истории и их теги:")
    all_stories = Story.objects.filter(is_published=True).prefetch_related('tags')
    for story in all_stories[:5]:  # Показываем первые 5
        tag_names = [t.name for t in story.tags.all()]
        print(f"  • {story.title}: {tag_names}")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
