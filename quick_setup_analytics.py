#!/usr/bin/env python
"""
Простой скрипт для создания миграций аналитики
"""

import os
import sys
import django
from pathlib import Path

# Настройка Django
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✅ Django настроен успешно")
    
    # Импортируем команды Django
    from django.core.management import execute_from_command_line
    
    print("🔄 Создание миграций для analytics...")
    execute_from_command_line(['manage.py', 'makemigrations', 'analytics'])
    
    print("🔄 Применение миграций...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Миграции созданы и применены!")
    
    # Проверяем модели
    from analytics.models import AnalyticsEvent, ConversionFunnel
    print(f"✅ Модели импортируются: {AnalyticsEvent}, {ConversionFunnel}")
    
    print("\n🎉 АНАЛИТИКА ГОТОВА К РАБОТЕ!")
    print("Откройте: http://127.0.0.1:8000/analytics/dashboard/")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
