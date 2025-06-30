#!/usr/bin/env python
"""
Создание миграции для добавления поля cover_image
"""

import os
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    print("🖼️  Создаем миграцию для добавления изображений...")
    execute_from_command_line(['manage.py', 'makemigrations', 'fairy_tales', '--name', 'add_cover_image'])
    
    print("🔧 Применяем миграцию...")
    execute_from_command_line(['manage.py', 'migrate', 'fairy_tales'])
    
    print("✅ Поле для изображений добавлено!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n📸 Теперь можно:")
print("1. Загружать изображения в админке")
print("2. Изображения будут автоматически отображаться в каталоге")
print("3. Если изображения нет - показывается иконка")
