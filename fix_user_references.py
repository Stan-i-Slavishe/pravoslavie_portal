#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправление ссылок на пользователей в stories данных
"""

import json

def fix_user_references():
    """Исправляем все ссылки на пользователей, заменяя строки на ID"""
    
    input_file = 'backups/stories_clean.json'
    output_file = 'backups/stories_final.json'
    
    # Маппинг имен пользователей на ID
    user_mapping = {
        'admin': 1,
        'user': 2,
        'test': 3
    }
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Обрабатываем {len(data)} записей...")
        
        fixed_count = 0
        removed_count = 0
        clean_data = []
        
        for item in data:
            fields = item.get('fields', {})
            model_name = item.get('model', '')
            
            # Список полей, которые могут содержать ссылки на пользователей
            user_fields = ['user', 'author', 'creator']
            
            item_fixed = False
            skip_item = False
            
            for field_name in user_fields:
                if field_name in fields:
                    field_value = fields[field_name]
                    
                    # Если это строка - пытаемся конвертировать в ID
                    if isinstance(field_value, str):
                        if field_value in user_mapping:
                            fields[field_name] = user_mapping[field_value]
                            item_fixed = True
                        elif field_value.isdigit():
                            fields[field_name] = int(field_value)
                            item_fixed = True
                        else:
                            print(f"Неизвестный пользователь '{field_value}' в {model_name}:{item['pk']}, удаляем запись")
                            skip_item = True
                            break
                    
                    # Если это список с одним элементом
                    elif isinstance(field_value, list) and len(field_value) == 1:
                        user_ref = field_value[0]
                        if isinstance(user_ref, str) and user_ref in user_mapping:
                            fields[field_name] = user_mapping[user_ref]
                            item_fixed = True
                        elif isinstance(user_ref, str) and user_ref.isdigit():
                            fields[field_name] = int(user_ref)
                            item_fixed = True
                        else:
                            skip_item = True
                            break
                    
                    # Если это пустое значение - удаляем запись
                    elif field_value is None or field_value == []:
                        skip_item = True
                        break
            
            if skip_item:
                removed_count += 1
                continue
            
            if item_fixed:
                fixed_count += 1
            
            clean_data.append(item)
        
        print(f"Исправлено записей: {fixed_count}")
        print(f"Удалено записей: {removed_count}")
        print(f"Сохраняем {len(clean_data)} записей в {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2, ensure_ascii=False)
        
        return output_file
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def create_test_user_data():
    """Создаем минимальные пользовательские данные для импорта"""
    
    users_file = 'backups/test_users.json'
    
    test_users = [
        {
            "model": "auth.user",
            "pk": 1,
            "fields": {
                "username": "admin",
                "email": "admin@test.com",
                "is_staff": True,
                "is_active": True,
                "is_superuser": True,
                "password": "pbkdf2_sha256$260000$test$test",
                "date_joined": "2025-09-02T00:00:00Z"
            }
        }
    ]
    
    try:
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(test_users, f, indent=2, ensure_ascii=False)
        
        print(f"Создан файл тестовых пользователей: {users_file}")
        return users_file
        
    except Exception as e:
        print(f"Ошибка создания пользователей: {e}")
        return None

if __name__ == "__main__":
    print("ИСПРАВЛЕНИЕ ССЫЛОК НА ПОЛЬЗОВАТЕЛЕЙ")
    print("=" * 40)
    
    # Создаем тестовых пользователей
    users_file = create_test_user_data()
    
    # Исправляем ссылки на пользователей
    fixed_file = fix_user_references()
    
    if users_file and fixed_file:
        print("\nКоманды для импорта:")
        print(f"1. python manage.py loaddata {users_file} --settings=config.settings_local_postgresql")
        print(f"2. python manage.py loaddata {fixed_file} --settings=config.settings_local_postgresql")
    else:
        print("Не удалось создать исправленные файлы")
