#!/usr/bin/env python
"""
Скрипт для принудительного создания базовых данных
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Category, Tag, SiteSettings

def create_test_data():
    print("🔄 Принудительное создание тестовых данных...")
    
    # Создаем несколько тегов для теста
    test_tags = [
        {'name': 'вера', 'color': '#e17055'},
        {'name': 'молитва', 'color': '#0984e3'},
        {'name': 'любовь', 'color': '#fd79a8'},
    ]
    
    created_tags = 0
    for tag_data in test_tags:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            defaults=tag_data
        )
        if created:
            created_tags += 1
            print(f"✅ Создан тег: {tag.name}")
    
    # Создаем несколько категорий для теста
    test_categories = [
        {
            'name': 'Духовные истории',
            'content_type': 'story',
            'description': 'Рассказы о духовных переживаниях',
            'icon': 'bi-heart',
            'color': '#e17055',
            'order': 1
        },
        {
            'name': 'Духовная литература',
            'content_type': 'book',
            'description': 'Книги о православной вере',
            'icon': 'bi-book',
            'color': '#0984e3',
            'order': 10
        },
    ]
    
    created_categories = 0
    for cat_data in test_categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            created_categories += 1
            print(f"✅ Создана категория: {category.name}")
    
    # Создаем настройки сайта
    settings, created = SiteSettings.objects.get_or_create(pk=1)
    if created:
        print("✅ Созданы настройки сайта")
    
    print(f"\n📊 ИТОГО:")
    print(f"Тегов создано: {created_tags}")
    print(f"Категорий создано: {created_categories}")
    print(f"Всего тегов в БД: {Tag.objects.count()}")
    print(f"Всего категорий в БД: {Category.objects.count()}")

if __name__ == '__main__':
    create_test_data()