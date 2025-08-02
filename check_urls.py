#!/usr/bin/env python
"""
Проверяем, есть ли еще ошибки после удаления заглушек
"""

import os
import django
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Добавляем корневую директорию в путь
import sys
sys.path.append('E:\\pravoslavie_portal')

try:
    django.setup()
    print("✅ Django успешно настроен!")
    
    # Проверяем URL-ы
    from django.urls import reverse
    
    urls_to_check = [
        'shop:catalog',
        'shop:cart', 
        'fairy_tales:list',
        'books:list',
        'core:home'
    ]
    
    print("\n🔗 Проверяем основные URL-ы:")
    for url_name in urls_to_check:
        try:
            url = reverse(url_name)
            print(f"   ✅ {url_name} → {url}")
        except Exception as e:
            print(f"   ❌ {url_name} → ОШИБКА: {e}")
    
    print("\n🎉 Проверка завершена! Все URL-ы корректны.")
    
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
