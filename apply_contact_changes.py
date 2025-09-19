#!/usr/bin/env python
"""
Скрипт для применения миграции и заполнения начальных данных
для полей адреса и режима работы в SiteSettings
"""

import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import execute_from_command_line
from core.models import SiteSettings

def main():
    print("🔧 Применяем миграцию для новых полей адреса и режима работы...")
    
    try:
        # Применяем миграцию
        print("📦 Применение миграции...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Заполняем начальные данные
        print("📝 Заполнение начальных значений...")
        settings = SiteSettings.get_settings()
        
        # Проверяем, нужно ли заполнять данные
        if not hasattr(settings, 'work_hours') or not settings.work_hours:
            settings.work_hours = 'Пн-Пт: 9:00 - 18:00'
            settings.work_hours_note = 'По московскому времени'
            settings.address_city = 'г. Москва'
            settings.address_country = 'Россия'
            settings.save()
            print("✅ Начальные значения установлены")
        else:
            print("✅ Значения уже существуют")
        
        print("\n🎉 Все изменения успешно применены!")
        print("\n📋 Что изменилось:")
        print("   ✅ Добавлены поля в модель SiteSettings:")
        print("      - work_hours (время работы)")
        print("      - work_hours_note (примечание к времени)")
        print("      - address_city (город)")
        print("      - address_country (страна)")
        print("      - address_full (полный адрес)")
        print("\n   ✅ Обновлена админка с новыми секциями:")
        print("      - 'Время работы'")
        print("      - 'Адрес и местоположение'")
        print("\n   ✅ Шаблон контактов теперь использует данные из БД")
        print("\n🚀 Теперь вы можете:")
        print("   1. Запустить сервер: python manage.py runserver")
        print("   2. Зайти в админку: http://127.0.0.1:8000/admin/")
        print("   3. Перейти в 'Настройки сайта'")
        print("   4. Изменить время работы и адрес")
        print("   5. Проверить изменения на странице контактов")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
