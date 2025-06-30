#!/usr/bin/env python
"""Создание миграций для новых моделей"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🔄 Создание миграций для новых моделей...")
    
    try:
        # Создаем пустую миграцию для stories
        print("📝 Создание пустой миграции...")
        call_command('makemigrations', 'stories', '--empty', verbosity=1)
        
        print("✅ Миграция создана!")
        print("📍 Теперь запустите: python manage.py migrate")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
