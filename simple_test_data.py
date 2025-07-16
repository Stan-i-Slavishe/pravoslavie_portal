#!/usr/bin/env python
"""
Упрощенный скрипт для создания тестовых данных пагинации
"""
import os
import sys
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from core.models import Category

def create_simple_test_stories():
    """Создаем простые тестовые истории"""
    
    print("🚀 Создание тестовых историй для пагинации...")
    print()
    
    # Получаем существующие категории
    categories = Category.objects.all()
    print(f"📊 Найдено категорий: {categories.count()}")
    
    for cat in categories:
        print(f"   - {cat.name} (slug: {cat.slug})")
    
    # Если нет категорий, создаем одну базовую
    if not categories.exists():
        try:
            default_category = Category.objects.create(
                name="Общие истории",
                slug="obshchie",
                color="#e74c3c"
            )
            print(f"✅ Создана базовая категория: {default_category.name}")
            categories = [default_category]
        except Exception as e:
            print(f"❌ Не удалось создать категорию: {e}")
            return
    else:
        categories = list(categories)
    
    # Простые тестовые истории
    simple_stories = [
        "История о доброте и милосердии",
        "Чудесное исцеление через молитву", 
        "Как вера помогла в трудную минуту",
        "Рассказ о настоящей дружбе",
        "Урок смирения и терпения",
        "Семейные традиции и ценности",
        "О важности прощения",
        "Помощь ближнему в беде",
        "Благодарность за все в жизни",
        "Сила родительской любви",
        "Детская вера и чистота",
        "О честности и правде",
        "Преодоление жизненных трудностей",
        "Радость в простых вещах",
        "О служении людям"
    ]
    
    created_count = 0
    category_index = 0
    
    for i, title in enumerate(simple_stories, 1):
        try:
            # Используем категории по кругу
            category = categories[category_index % len(categories)]
            category_index += 1
            
            story, created = Story.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'Духовная история номер {i}. {title[:50]}...',
                    'category': category,
                    'youtube_embed_id': 'dQw4w9WgXcQ',  # Тестовое видео
                    'is_published': True,
                    'views_count': i * 10  # Для разнообразия
                }
            )
            
            if created:
                created_count += 1
                print(f"✅ Создана история {i}: {story.title}")
            else:
                print(f"📝 История уже существует: {story.title}")
                
        except Exception as e:
            print(f"❌ Ошибка при создании истории '{title}': {e}")
    
    # Итоговая статистика
    total_stories = Story.objects.filter(is_published=True).count()
    print()
    print(f"📊 Создано новых историй: {created_count}")
    print(f"📊 Всего опубликованных историй: {total_stories}")
    print()
    
    if total_stories >= 7:
        pages = (total_stories + 5) // 6  # Округление вверх для 6 на странице
        print(f"✅ Отлично! Пагинация будет работать!")
        print(f"📄 Ожидается страниц: {pages}")
        print(f"🎯 На первой странице: 6 историй")
        if pages > 1:
            remaining = total_stories - 6
            print(f"🎯 На остальных страницах: {remaining} историй")
    else:
        needed = 7 - total_stories
        print(f"⚠️  Нужно еще {needed} историй для проверки пагинации")
        print("   Попробуйте запустить скрипт еще раз")
    
    print()
    print("🎉 Готово! Теперь можете проверить пагинацию:")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/stories/")

if __name__ == '__main__':
    create_simple_test_stories()
