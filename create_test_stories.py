#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from core.models import Category
from django.utils.text import slugify

# Создаем тестовые рассказы для демонстрации пагинации
test_stories = [
    {
        'title': 'О терпении и смирении',
        'description': 'Рассказ о том, как важно проявлять терпение в трудные времена и находить силы в вере.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Молитва матери',
        'description': 'История о силе материнской молитвы и о том, как она может изменить судьбу.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Чудо в пустыне',
        'description': 'Рассказ о старце, который своей верой совершал чудеса в безводной пустыне.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Прощение врагов',
        'description': 'История о том, как христианское прощение может изменить сердца людей.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Бедная вдова',
        'description': 'Рассказ о вдове, которая отдала последнее ради помощи ближним.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Детская вера',
        'description': 'История о том, как чистая детская вера может творить настоящие чудеса.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Путь к храму',
        'description': 'Рассказ о человеке, который долго искал свой путь к Богу.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    },
    {
        'title': 'Святая вода',
        'description': 'История о чудесном исцелении через святую воду.',
        'youtube_embed_id': 'dQw4w9WgXcQ'
    }
]

# Получаем категорию для рассказов
try:
    category = Category.objects.first()
    if not category:
        category = Category.objects.create(
            name='Врачебные истории',
            slug='vrachebnyie-istorii',
            description='Духовные рассказы о врачебном деле'
        )
except:
    category = None

created_count = 0
for story_data in test_stories:
    slug = slugify(story_data['title'])
    
    # Проверяем, есть ли уже такой рассказ
    if not Story.objects.filter(slug=slug).exists():
        story = Story.objects.create(
            title=story_data['title'],
            slug=slug,
            description=story_data['description'],
            youtube_embed_id=story_data['youtube_embed_id'],
            category=category,
            is_published=True,
            is_featured=False
        )
        created_count += 1
        print(f"✅ Создан рассказ: {story.title}")
    else:
        print(f"⚠️  Рассказ уже существует: {story_data['title']}")

print(f"\n🎉 Создано новых рассказов: {created_count}")
print(f"📊 Всего рассказов в базе: {Story.objects.count()}")
print(f"📖 Опубликованных рассказов: {Story.objects.filter(is_published=True).count()}")
print("\n✅ Теперь пагинация должна работать!")
