#!/usr/bin/env python
"""
QUICK META TAGS CHECK
"""
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from core.seo import page_meta
    
    # Тестируем генерацию мета-тегов
    meta = page_meta('home')
    
    if meta and meta.get('title') and meta.get('description'):
        print(f'✅ Мета-теги генерируются: {meta["title"][:30]}...')
    else:
        print('❌ Проблема с генерацией мета-тегов')
        
except Exception as e:
    print(f'❌ Проблема мета-тегов: {e}')
