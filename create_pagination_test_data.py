#!/usr/bin/env python
"""
Скрипт для создания тестовых данных для проверки пагинации
"""
import os
import sys
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import models
from stories.models import Story
from core.models import Category

def create_test_stories():
    """Создаем тестовые истории для проверки пагинации"""
    
    # Создаем категории если их нет
    categories_data = [
        {'name': 'Врачебные истории', 'slug': 'vrachskie', 'color': '#e74c3c'},
        {'name': 'Школьные истории', 'slug': 'shkolnye', 'color': '#3498db'},
        {'name': 'Чудеса', 'slug': 'chudesa', 'color': '#f39c12'},
        {'name': 'Семейные истории', 'slug': 'semeinye', 'color': '#27ae60'},
    ]
    
    for cat_data in categories_data:
        try:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],  # Ищем по name вместо slug
                defaults={
                    'slug': cat_data['slug'],
                    'color': cat_data['color']
                }
            )
            if created:
                print(f"✅ Создана категория: {category.name}")
            else:
                print(f"📝 Категория уже существует: {category.name}")
        except Exception as e:
            # Если ошибка, пробуем найти по slug
            try:
                category = Category.objects.get(slug=cat_data['slug'])
                print(f"📝 Найдена категория по slug: {category.name}")
            except Category.DoesNotExist:
                print(f"❌ Не удалось создать/найти категорию: {cat_data['name']} - {e}")
                continue
    
    # Данные для создания тестовых историй
    test_stories = [
        {
            'title': 'Дайте мне самого больного ребёнка',
            'description': 'Людям, которые страдают от депрессии.',
            'category_slug': 'vrachskie',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Богородица спасла от аборта',
            'description': 'Этот рассказ о том, как еще в советское время',
            'category_slug': 'chudesa',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Восстановились милостью Божьей',
            'description': 'В моей жизни были случаи, когда я явственно',
            'category_slug': 'chudesa',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'История о настоящем друге',
            'description': 'Рассказ о дружбе, которая проверяется временем',
            'category_slug': 'shkolnye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Урок милосердия',
            'description': 'История о том, как маленький поступок может изменить жизнь',
            'category_slug': 'shkolnye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Семейные традиции',
            'description': 'О важности передачи традиций от поколения к поколению',
            'category_slug': 'semeinye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Прощение в семье',
            'description': 'История о силе прощения и восстановлении отношений',
            'category_slug': 'semeinye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Молитва за детей',
            'description': 'Рассказ о силе родительской молитвы',
            'category_slug': 'semeinye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Чудо в больнице',
            'description': 'Невероятная история выздоровления через веру',
            'category_slug': 'vrachskie',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Учитель и ученик',
            'description': 'О влиянии хорошего учителя на судьбу ребенка',
            'category_slug': 'shkolnye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Икона, которая спасла',
            'description': 'История о чудотворной силе православных икон',
            'category_slug': 'chudesa',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
        {
            'title': 'Доброта спасает мир',
            'description': 'Простая история о том, как доброта меняет людей',
            'category_slug': 'semeinye',
            'youtube_embed_id': 'dQw4w9WgXcQ'
        },
    ]
    
    created_count = 0
    
    for story_data in test_stories:
        try:
            category = Category.objects.filter(
                models.Q(slug=story_data['category_slug']) |
                models.Q(name__icontains=story_data['category_slug'].replace('_', ' '))
            ).first()
            
            if not category:
                print(f"⚠️  Категория не найдена: {story_data['category_slug']}")
                continue
            
            story, created = Story.objects.get_or_create(
                title=story_data['title'],
                defaults={
                    'description': story_data['description'],
                    'category': category,
                    'youtube_embed_id': story_data['youtube_embed_id'],
                    'is_published': True
                }
            )
            
            if created:
                created_count += 1
                print(f"✅ Создана история: {story.title}")
            else:
                print(f"📝 История уже существует: {story.title}")
                
        except Exception as e:
            print(f"❌ Ошибка при создании истории '{story_data['title']}': {e}")
    
    total_stories = Story.objects.filter(is_published=True).count()
    print(f"\n📊 Итого создано новых историй: {created_count}")
    print(f"📊 Всего опубликованных историй: {total_stories}")
    
    if total_stories >= 6:
        print(f"✅ Пагинация будет работать! (показывает по 6 историй на странице)")
        print(f"📄 Ожидается страниц: {(total_stories + 5) // 6}")
    else:
        print(f"⚠️  Нужно еще {6 - total_stories} историй для проверки пагинации")

if __name__ == '__main__':
    print("🚀 Создание тестовых данных для пагинации...")
    create_test_stories()
    print("✅ Готово!")
