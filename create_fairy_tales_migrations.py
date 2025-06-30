#!/usr/bin/env python
"""
Создание миграций для fairy_tales
"""

import os
import django
from django.core.management import execute_from_command_line

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    print("🔧 Создаем миграции для fairy_tales...")
    execute_from_command_line(['manage.py', 'makemigrations', 'fairy_tales'])
    
    print("🔧 Применяем миграции...")
    execute_from_command_line(['manage.py', 'migrate', 'fairy_tales'])
    
    print("✅ Миграции созданы и применены!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n💡 Теперь попробуйте снова создать шаблон в админке")
print("📝 Используйте:")
print('   Терапевтические цели: ["fears"]')
print('   Поля персонализации: {}')
