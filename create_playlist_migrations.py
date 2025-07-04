#!/usr/bin/env python
"""
Скрипт для создания миграций плейлистов
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("🔧 Создание миграций для моделей плейлистов...")

try:
    # Создаем миграции
    call_command('makemigrations', 'stories', '--name=add_playlist_models')
    print("✅ Миграции созданы успешно!")
    
    # Применяем миграции
    call_command('migrate', 'stories')
    print("✅ Миграции применены успешно!")
    
    print("\n🎉 Модели плейлистов готовы к использованию!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\n🔄 Попробуйте выполнить команды вручную:")
    print("python manage.py makemigrations stories --name=add_playlist_models")
    print("python manage.py migrate stories")
