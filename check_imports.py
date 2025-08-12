#!/usr/bin/env python
"""
IMPORT TESTS CHECKER
"""
import os
import sys

# Настройка пути
sys.path.append(r'E:\pravoslavie_portal')

print('🔍 Тестирование критических импортов...')

critical_imports = [
    ('core.seo', 'Основной SEO модуль'),
    ('core.seo.meta_tags', 'Мета-теги'),
    ('core.seo.schema_org', 'Schema.org'),
    ('core.templatetags.seo_tags', 'SEO templatetags'),
    ('core.views.main_views', 'Основные views'),
    ('core.views.seo_views', 'SEO views'),
]

failed = 0
for module, description in critical_imports:
    try:
        __import__(module)
        print(f'   ✅ {description}: {module}')
    except Exception as e:
        print(f'   ❌ {description}: {module} - {e}')
        failed += 1

if failed == 0:
    print('✨ Все критические модули импортируются успешно!')
else:
    print(f'⚠️  Проблемы с {failed} модулями из {len(critical_imports)}')
