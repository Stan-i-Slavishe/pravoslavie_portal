#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Радикальное исправление данных stories
"""

import json
import sys

def fix_stories_radical():
    """Радикально исправляем все проблемы в stories"""
    
    backup_file = 'backups/stories_20250901_2113.json'
    clean_file = 'backups/stories_clean.json'
    
    try:
        print(f"Обрабатываем файл: {backup_file}")
        with open(backup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Исходных записей: {len(data)}")
        
        clean_data = []
        removed_playlists = 0
        fixed_records = 0
        
        for item in data:
            model_name = item.get('model', '')
            fields = item.get('fields', {})
            
            # Убираем все проблематичные плейлисты
            if model_name == 'stories.playlist':
                creator = fields.get('creator')
                if creator is None or creator == 'null' or not creator:
                    print(f"Удаляем плейлист {item['pk']} без создателя")
                    removed_playlists += 1
                    continue
                    
            # Убираем записи с проблемными пользователями
            elif model_name in ['stories.storycomment', 'stories.storylike']:
                user_field = fields.get('author') or fields.get('user')
                if user_field is None or user_field == 'null' or not user_field:
                    print(f"Удаляем {model_name} {item['pk']} без пользователя")
                    continue
                    
            # Исправляем ссылки на пользователей в формате массива
            if 'user' in fields and isinstance(fields['user'], list):
                if fields['user'] and fields['user'][0]:
                    # Конвертируем массив в строку пользователя
                    fields['user'] = fields['user'][0]
                    fixed_records += 1
                else:
                    # Убираем записи с пустыми пользователями
                    continue
                    
            if 'author' in fields and isinstance(fields['author'], list):
                if fields['author'] and fields['author'][0]:
                    fields['author'] = fields['author'][0]
                    fixed_records += 1
                else:
                    continue
            
            clean_data.append(item)
        
        print(f"Очищенных записей: {len(clean_data)}")
        print(f"Удалено плейлистов: {removed_playlists}")
        print(f"Исправлено записей: {fixed_records}")
        
        # Сохраняем очищенные данные
        with open(clean_file, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
        print(f"Сохранено в: {clean_file}")
        return clean_file
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def create_minimal_stories():
    """Создаем минимальный набор stories данных"""
    
    minimal_file = 'backups/stories_minimal.json'
    
    # Только самые важные записи без зависимостей от пользователей
    minimal_data = [
        {
            "model": "stories.story",
            "pk": 1,
            "fields": {
                "title": "Тестовый рассказ",
                "slug": "test-story",
                "description": "Это тестовый рассказ для проверки работы системы",
                "content": "Содержимое тестового рассказа.",
                "youtube_embed": "dQw4w9WgXcQ",
                "category": 1,
                "is_published": True,
                "featured": False,
                "views_count": 0,
                "created_at": "2025-09-02T00:00:00Z",
                "updated_at": "2025-09-02T00:00:00Z"
            }
        }
    ]
    
    try:
        with open(minimal_file, 'w', encoding='utf-8') as f:
            json.dump(minimal_data, f, indent=2, ensure_ascii=False)
        
        print(f"Создан минимальный файл: {minimal_file}")
        return minimal_file
        
    except Exception as e:
        print(f"Ошибка создания минимального файла: {e}")
        return None

if __name__ == "__main__":
    print("РАДИКАЛЬНАЯ ОЧИСТКА STORIES ДАННЫХ")
    print("=" * 50)
    
    # Пытаемся очистить исходные данные
    clean_file = fix_stories_radical()
    
    if not clean_file:
        print("Основная очистка не удалась, создаем минимальный набор...")
        clean_file = create_minimal_stories()
    
    if clean_file:
        print(f"\nИспользуйте команду:")
        print(f"python manage.py loaddata {clean_file} --settings=config.settings_local_postgresql")
    else:
        print("Не удалось создать чистые данные")
