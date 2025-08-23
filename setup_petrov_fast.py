#!/usr/bin/env python
"""
Быстрое создание миграций и добавление Петрова поста
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line

def main():
    """Главная функция"""
    
    print("🚀 Подготовка базы данных для Петрова поста")
    print("=" * 50)
    
    try:
        # 1. Создаем миграции
        print("📦 Создание миграций...")
        execute_from_command_line(['manage.py', 'makemigrations', 'pwa'])
        
        # 2. Применяем миграции
        print("🔧 Применение миграций...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 3. Добавляем Петров пост
        print("⛪ Добавление Петрова поста...")
        from add_petrov_fast import main as add_petrov_main
        add_petrov_main()
        
        print("=" * 50)
        print("🎉 ВСЕ ГОТОВО!")
        print("🔄 Теперь перезапустите сервер: python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
