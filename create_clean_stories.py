#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание только stories данных без пользовательских зависимостей
"""

import json

def create_stories_only():
    """Создаем только stories записи без проблемных зависимостей"""
    
    try:
        # Читаем исходный файл
        with open('backups/stories_20250901_2113.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Фильтруем только модели Story и Category
        stories_data = []
        
        for item in data:
            model_name = item.get('model', '')
            
            # Берем только основные записи рассказов
            if model_name == 'stories.story':
                fields = item.get('fields', {})
                
                # Убираем проблемные поля
                clean_fields = {
                    'title': fields.get('title', ''),
                    'slug': fields.get('slug', ''),
                    'description': fields.get('description', ''),
                    'content': fields.get('content', ''),
                    'youtube_embed': fields.get('youtube_embed', ''),
                    'category': fields.get('category') or 1,  # Дефолтная категория
                    'is_published': fields.get('is_published', True),
                    'featured': fields.get('featured', False),
                    'views_count': 0,
                    'created_at': fields.get('created_at', '2025-09-02T00:00:00Z'),
                    'updated_at': fields.get('updated_at', '2025-09-02T00:00:00Z')
                }
                
                stories_data.append({
                    'model': 'stories.story',
                    'pk': item['pk'],
                    'fields': clean_fields
                })
        
        # Сохраняем только stories
        output_file = 'backups/stories_only_clean.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stories_data, f, indent=2, ensure_ascii=False)
        
        print(f"Создано {len(stories_data)} чистых stories записей")
        print(f"Сохранено в: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def create_test_data():
    """Создаем минимальные тестовые данные для остальных модулей"""
    
    test_data = [
        # Тестовая книга
        {
            "model": "books.book",
            "pk": 1,
            "fields": {
                "title": "Тестовая книга",
                "slug": "test-book",
                "description": "Описание тестовой книги",
                "price": "100.00",
                "is_published": True,
                "created_at": "2025-09-02T00:00:00Z"
            }
        },
        # Тестовый товар в магазине
        {
            "model": "shop.product",
            "pk": 1,
            "fields": {
                "title": "Тестовый товар",
                "description": "Описание тестового товара",
                "price": "50.00",
                "product_type": "book",
                "is_active": True
            }
        },
        # Тестовая сказка
        {
            "model": "fairy_tales.fairytaletemplate",
            "pk": 1,
            "fields": {
                "title": "Тестовая сказка",
                "slug": "test-fairy-tale",
                "short_description": "Короткое описание",
                "content_template": "Жил-был {name}...",
                "target_age_min": 3,
                "target_age_max": 8,
                "is_published": True
            }
        }
    ]
    
    output_file = 'backups/test_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"Создан файл тестовых данных: {output_file}")
    return output_file

if __name__ == "__main__":
    print("СОЗДАНИЕ ЧИСТЫХ STORIES ДАННЫХ")
    print("=" * 40)
    
    stories_file = create_stories_only()
    test_file = create_test_data()
    
    if stories_file:
        print(f"\nКоманды для импорта:")
        print(f"1. python manage.py createsuperuser --settings=config.settings_local_postgresql")
        print(f"2. python manage.py loaddata {stories_file} --settings=config.settings_local_postgresql")
        print(f"3. python manage.py loaddata {test_file} --settings=config.settings_local_postgresql")
        print("\nПосле этого у вас будут все stories + минимальные тестовые данные для остальных модулей")
