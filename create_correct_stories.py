#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание правильных stories данных по реальной структуре модели
"""

import json

def create_correct_stories():
    """Создаем stories данные с правильными полями"""
    
    try:
        # Читаем исходный файл
        with open('backups/stories_20250901_2113.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stories_data = []
        
        for item in data:
            model_name = item.get('model', '')
            
            # Берем только Story модели
            if model_name == 'stories.story':
                fields = item.get('fields', {})
                
                # Создаем поля согласно реальной модели Story
                clean_fields = {
                    # Основные поля
                    'title': fields.get('title', 'Без названия'),
                    'slug': fields.get('slug', f'story-{item["pk"]}'),
                    'description': fields.get('description', ''),
                    
                    # YouTube поля (новая структура)
                    'youtube_url': fields.get('youtube_url') or f"https://youtube.com/watch?v={fields.get('youtube_embed', '')}",
                    'youtube_embed_id': fields.get('youtube_embed') or fields.get('youtube_embed_id', ''),
                    
                    # Опциональные поля  
                    'thumbnail': fields.get('thumbnail', ''),
                    'duration': fields.get('duration', ''),
                    'category': fields.get('category') or 1,
                    
                    # Булевы поля
                    'is_featured': fields.get('featured', False),
                    'is_published': fields.get('is_published', True),
                    
                    # Счетчики
                    'views_count': fields.get('views_count', 0),
                    
                    # Временные метки
                    'created_at': fields.get('created_at', '2025-09-02T00:00:00Z'),
                    'updated_at': fields.get('updated_at', '2025-09-02T00:00:00Z'),
                }
                
                # Убираем пустые поля
                clean_fields = {k: v for k, v in clean_fields.items() if v is not None}
                
                stories_data.append({
                    'model': 'stories.story',
                    'pk': item['pk'],
                    'fields': clean_fields
                })
        
        # Сохраняем
        output_file = 'backups/stories_correct.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stories_data, f, indent=2, ensure_ascii=False)
        
        print(f"Создано {len(stories_data)} корректных stories записей")
        print(f"Сохранено в: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

if __name__ == "__main__":
    print("СОЗДАНИЕ КОРРЕКТНЫХ STORIES ДАННЫХ")
    print("=" * 45)
    
    stories_file = create_correct_stories()
    
    if stories_file:
        print(f"\nКоманда для импорта:")
        print(f"python manage.py loaddata {stories_file}")
        print("\nЭто должно загрузить все ваши stories с правильной структурой полей!")
