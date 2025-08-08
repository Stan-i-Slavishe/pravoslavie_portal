#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация Django
django.setup()

from core.models import Tag

# Создаем тег "дочь"
try:
    tag, created = Tag.objects.get_or_create(
        slug='doch',
        defaults={
            'name': 'дочь',
            'description': 'Материалы о воспитании дочерей',
            'color': '#FF6B9D',
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")
    else:
        print(f"⚠️ Тег уже существует: {tag.name} (slug: {tag.slug})")
    
    # Создаем еще несколько базовых тегов
    basic_tags = [
        {'name': 'вера', 'slug': 'vera', 'color': '#9C27B0'},
        {'name': 'семья', 'slug': 'semya', 'color': '#4CAF50'},
        {'name': 'любовь', 'slug': 'lyubov', 'color': '#E91E63'},
        {'name': 'сын', 'slug': 'syn', 'color': '#2196F3'},
    ]
    
    for tag_data in basic_tags:
        tag, created = Tag.objects.get_or_create(
            slug=tag_data['slug'],
            defaults={
                'name': tag_data['name'],
                'description': f'Материалы о {tag_data["name"]}',
                'color': tag_data['color'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Создан тег: {tag.name} (slug: {tag.slug})")
    
    # Выводим все теги
    print("\n📋 Все теги в базе данных:")
    all_tags = Tag.objects.all()
    for tag in all_tags:
        print(f"   • {tag.name} (slug: {tag.slug}) - {tag.color}")
    
    print(f"\n🎉 Всего тегов: {all_tags.count()}")
    print("\n🧪 Теперь можете проверить:")
    print("   http://127.0.0.1:8000/tag/doch/")
    print("   http://127.0.0.1:8000/tag/vera/")
    print("   http://127.0.0.1:8000/tag/semya/")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
