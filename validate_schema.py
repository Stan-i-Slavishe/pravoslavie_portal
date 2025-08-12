#!/usr/bin/env python
"""
SCHEMA.ORG VALIDATION SCRIPT
"""
import os
import sys
import django
import json

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print('🔍 Проверка Schema.org генерации...')
try:
    from core.seo.schema_org import get_schema_data
    
    # Тест всех типов схем
    schemas = ['organization', 'website']
    for schema_type in schemas:
        result = get_schema_data(schema_type)
        if result:
            data = json.loads(result)
            required_fields = ['@context', '@type', 'name']
            missing = [f for f in required_fields if f not in data]
            if missing:
                print(f'   ⚠️  {schema_type}: отсутствуют поля {missing}')
            else:
                print(f'   ✅ {schema_type}: валидная схема')
        else:
            print(f'   ❌ {schema_type}: пустой результат')
    
    print('✨ Schema.org валидация завершена!')
    
except Exception as e:
    print(f'💥 Ошибка валидации Schema.org: {e}')
