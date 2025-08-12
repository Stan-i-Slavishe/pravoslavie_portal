#!/usr/bin/env python
"""
URL PATTERNS VALIDATION
"""
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print('🔍 Проверка URL паттернов для SEO...')
from django.urls import reverse, NoReverseMatch

seo_urls = [
    ('robots_txt', 'robots.txt'),
    ('django.contrib.sitemaps.views.sitemap', 'sitemap.xml'),
    ('core:home', 'главная страница'),
]

for url_name, description in seo_urls:
    try:
        url = reverse(url_name)
        print(f'   ✅ {description}: {url}')
    except NoReverseMatch:
        print(f'   ❌ {description}: URL {url_name} не найден')
    except Exception as e:
        print(f'   💥 {description}: ошибка - {e}')

print('✨ Проверка URL завершена!')
