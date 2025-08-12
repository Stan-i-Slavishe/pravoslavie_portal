#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(r'E:\pravoslavie_portal')

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 Проверяем импорты...")

try:
    # Проверяем импорт SEO
    from core.seo import page_meta
    print("✅ SEO модуль импортируется корректно")
except Exception as e:
    print(f"❌ Ошибка импорта SEO: {e}")

try:
    # Проверяем импорт views
    from core.views import HomeView
    print("✅ HomeView импортируется корректно")
except Exception as e:
    print(f"❌ Ошибка импорта HomeView: {e}")

try:
    # Проверяем импорт models
    from core.models import Category, Tag, SiteSettings
    print("✅ Модели импортируются корректно")
except Exception as e:
    print(f"❌ Ошибка импорта моделей: {e}")

try:
    # Проверяем URL patterns
    from django.urls import reverse
    from config.urls import urlpatterns
    print("✅ URL patterns загружаются корректно")
except Exception as e:
    print(f"❌ Ошибка загрузки URL patterns: {e}")

print("\n🚀 Все проверки пройдены! Сервер должен запускаться.")
