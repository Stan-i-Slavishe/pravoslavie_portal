#!/usr/bin/env python
"""Добавление поля duration"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🔄 Добавление поля duration...")
    
    try:
        print("📝 Создание миграции...")
        call_command('makemigrations', 'stories', verbosity=1)
        
        print("🔨 Применение миграции...")
        call_command('migrate', verbosity=1)
        
        print("✅ Поле duration добавлено!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
