#!/usr/bin/env python
"""
Быстрая проверка Django проекта
"""
import os
import sys

def check_django_project():
    """Проверка Django проекта"""
    
    print("🔍 Быстрая диагностика Django проекта")
    print("=" * 50)
    
    # Проверяем основные файлы
    files_to_check = [
        'stories/models.py',
        'stories/views.py', 
        'stories/views_comments.py',
        'stories/urls.py',
        'stories/admin.py'
    ]
    
    print("\n📁 Проверка файлов:")
    for file_path in files_to_check:
        full_path = f'E:\\pravoslavie_portal\\{file_path}'
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
            
            # Простая проверка синтаксиса
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        print(f"   📝 Содержимое найдено ({len(content)} символов)")
                    else:
                        print(f"   ⚠️  Файл пустой")
            except Exception as e:
                print(f"   ❌ Ошибка чтения: {e}")
        else:
            print(f"❌ {file_path}")
    
    print("\n🎯 Команды для исправления:")
    print("1. cd E:\\pravoslavie_portal")
    print("2. python manage.py makemigrations stories")
    print("3. python manage.py migrate")
    print("4. python manage.py runserver")
    
    print("\n📋 Если ошибки продолжаются:")
    print("- Проверьте синтаксис Python в файлах")
    print("- Убедитесь что все import корректны")
    print("- Проверьте отступы (табы/пробелы)")
    
    print("\n🔧 Создание миграции вручную:")
    print("python manage.py makemigrations stories --name add_youtube_comments")

if __name__ == "__main__":
    check_django_project()
