#!/usr/bin/env python
"""Проверка статуса миграций"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🔍 Проверка статуса миграций...")
    
    try:
        print("\n📋 Статус миграций для stories:")
        call_command('showmigrations', 'stories', verbosity=1)
        
        print("\n🔨 Применение всех миграций...")
        call_command('migrate', verbosity=1)
        
        print("✅ Готово!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
