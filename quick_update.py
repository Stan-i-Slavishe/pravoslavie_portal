#!/usr/bin/env python
"""Быстрое обновление системы комментариев"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🔄 Быстрое обновление...")
    
    try:
        # Создаем и применяем миграции
        print("📝 Создание миграций...")
        call_command('makemigrations', verbosity=1)
        
        print("🔨 Применение миграций...")
        call_command('migrate', verbosity=1)
        
        print("✅ Обновление завершено!")
        print("🌐 Запустите сервер: python manage.py runserver")
        print("📍 Перейдите на: http://127.0.0.1:8000/stories/")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
