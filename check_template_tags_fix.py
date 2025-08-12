#!/usr/bin/env python
"""
QUICK TEMPLATE TAGS CHECK
"""
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from django.template import Template, Context
    from django.test import RequestFactory
    
    # Создаем правильный request
    factory = RequestFactory()
    request = factory.get('/', HTTP_HOST='testserver')
    
    # Тестируем schema_ld template tag
    template = Template('{% load seo_tags %}{% schema_ld "organization" %}')
    context = Context({'request': request})
    rendered = template.render(context)
    
    if '<script type="application/ld+json">' in rendered:
        print('✅ Template Tags исправлены!')
    else:
        print('❌ Template Tags не генерируют правильный JSON-LD')
        
except Exception as e:
    print(f'❌ Проблема: {e}')
