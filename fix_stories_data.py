#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление данных stories перед импортом
"""

import json
import sys

def fix_stories_backup():
    """Исправляем проблемы в бэкапе stories"""
    
    backup_file = 'backups/stories_20250901_2113.json'
    fixed_file = 'backups/stories_20250901_2113_fixed.json'
    
    try:
        print(f"Читаем файл: {backup_file}")
        with open(backup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Найдено записей: {len(data)}")
        
        fixed_count = 0
        removed_count = 0
        
        fixed_data = []
        
        for item in data:
            # Исправляем проблемы с плейлистами
            if item.get('model') == 'stories.playlist':
                fields = item.get('fields', {})
                
                # Если creator_id пустой, устанавливаем default пользователя (id=1)
                if not fields.get('creator') or fields.get('creator') is None:
                    print(f"Исправляем плейлист {item['pk']}: устанавливаем creator_id=1")
                    fields['creator'] = 1
                    fixed_count += 1
                
                fixed_data.append(item)
                
            # Исправляем проблемы с комментариями
            elif item.get('model') == 'stories.storycomment':
                fields = item.get('fields', {})
                
                # Если author пустой, пропускаем комментарий
                if not fields.get('author') or fields.get('author') is None:
                    print(f"Удаляем комментарий {item['pk']} без автора")
                    removed_count += 1
                    continue
                
                fixed_data.append(item)
                
            else:
                fixed_data.append(item)
        
        # Сохраняем исправленные данные
        print(f"Сохраняем исправленные данные: {fixed_file}")
        with open(fixed_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)
        
        print(f"Исправлено записей: {fixed_count}")
        print(f"Удалено записей: {removed_count}")
        print(f"Итого записей в исправленном файле: {len(fixed_data)}")
        
        return fixed_file
        
    except Exception as e:
        print(f"Ошибка исправления данных: {e}")
        return None

if __name__ == "__main__":
    fixed_file = fix_stories_backup()
    
    if fixed_file:
        print(f"\nИспользуйте команду:")
        print(f"python manage.py loaddata {fixed_file} --settings=config.settings_local_postgresql")
    else:
        print("Не удалось исправить файл данных")
