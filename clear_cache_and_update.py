#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('E:\\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализируем Django
django.setup()

try:
    # Очищаем кеш
    from django.core.cache import cache
    cache.clear()
    print("✅ Кеш очищен успешно!")
    
    # Запускаем collectstatic
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
    print("✅ Статические файлы обновлены!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
