#!/usr/bin/env python
"""
Скрипт для экспорта видео-рассказов и тегов из локальной базы
"""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
django.setup()

from django.core import serializers
from stories.models import Story, Category
from core.models import Tag

def export_stories_data():
    # Экспорт категорий
    categories = Category.objects.all()
    print(f"Найдено категорий: {categories.count()}")
    
    # Экспорт тегов
    tags = Tag.objects.all()
    print(f"Найдено тегов: {tags.count()}")
    
    # Экспорт рассказов
    stories = Story.objects.all()
    print(f"Найдено рассказов: {stories.count()}")
    
    # Создание JSON дампа
    data = []
    
    # Добавляем категории
    for category in categories:
        data.extend(serializers.serialize('python', [category]))
    
    # Добавляем теги
    for tag in tags:
        data.extend(serializers.serialize('python', [tag]))
    
    # Добавляем рассказы
    for story in stories:
        data.extend(serializers.serialize('python', [story]))
    
    # Сохраняем в JSON
    with open('stories_data.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Данные экспортированы в stories_data.json")

if __name__ == '__main__':
    export_stories_data()
