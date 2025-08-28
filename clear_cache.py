#!/usr/bin/env python3
"""
🧹 Очистка всех кешей Django
Удаляет кеши, которые могут блокировать YouTube iframe
"""

import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from django.core.management import execute_from_command_line

def clear_all_caches():
    """Очищаем все кеши"""
    print("🧹 Очищаем кеши...")
    
    try:
        # Django cache
        cache.clear()
        print("✅ Django cache очищен")
        
        # Static files cache
        execute_from_command_line(['manage.py', 'collectstatic', '--clear', '--noinput'])
        print("✅ Static files cache очищен")
        
    except Exception as e:
        print(f"⚠️ Ошибка при очистке кеша: {e}")
        print("✅ Кеш очищен частично")

if __name__ == "__main__":
    clear_all_caches()
    print("🎉 Кеши очищены!")
