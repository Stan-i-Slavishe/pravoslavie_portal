#!/usr/bin/env python
"""
Проверка статуса миграций и модели FastingPeriod
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_fasting_period_table():
    """Проверить существование таблицы FastingPeriod"""
    try:
        from pwa.models import FastingPeriod
        
        # Проверяем, существует ли таблица
        count = FastingPeriod.objects.count()
        print(f"✅ Таблица FastingPeriod существует. Записей: {count}")
        
        # Проверяем Петров пост
        petrov_fast = FastingPeriod.objects.filter(name='peter_paul_fast').first()
        if petrov_fast:
            print(f"✅ Петров пост найден: {petrov_fast.title}")
            print(f"   Приоритет: {petrov_fast.priority}")
            print(f"   Активен: {petrov_fast.is_active}")
            print(f"   Easter offset: {petrov_fast.easter_start_offset}")
            print(f"   End date: {petrov_fast.end_month}/{petrov_fast.end_day}")
        else:
            print("❌ Петров пост НЕ найден в базе данных")
        
        # Показываем все посты
        print(f"\n📋 Все посты в базе:")
        for period in FastingPeriod.objects.all():
            print(f"   - {period.name}: {period.title} (приоритет: {period.priority})")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка доступа к таблице FastingPeriod: {e}")
        return False

def check_migrations():
    """Проверить статус миграций"""
    try:
        from django.core.management import execute_from_command_line
        print("📦 Проверка миграций...")
        execute_from_command_line(['manage.py', 'showmigrations', 'pwa'])
    except Exception as e:
        print(f"❌ Ошибка проверки миграций: {e}")

def test_june_2026():
    """Тестировать июнь 2026"""
    try:
        from pwa.models import DailyOrthodoxInfo, OrthodoxEvent
        from datetime import date
        
        print(f"\n🧪 Тестирование июня 2026:")
        
        test_dates = [
            date(2026, 6, 1),   # Троицкая седмица
            date(2026, 6, 8),   # Должен быть Петров пост
            date(2026, 6, 15),  # Должен быть Петров пост
        ]
        
        for test_date in test_dates:
            daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
            active_periods = DailyOrthodoxInfo.get_active_fasting_periods(test_date)
            
            print(f"   {test_date.strftime('%d.%m')}: {daily_info.get_fasting_type_display()}")
            print(f"      Описание: {daily_info.fasting_description}")
            print(f"      Активные посты: {[p.title for p in active_periods]}")
            
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")

def main():
    print("🔍 ДИАГНОСТИКА ПЕТРОВА ПОСТА")
    print("=" * 50)
    
    # 1. Проверяем миграции
    check_migrations()
    
    # 2. Проверяем таблицу FastingPeriod
    table_exists = check_fasting_period_table()
    
    # 3. Тестируем июнь 2026
    if table_exists:
        test_june_2026()
    
    print("=" * 50)
    print("🎯 РЕЗУЛЬТАТ ДИАГНОСТИКИ:")
    print("Если Петров пост НЕ найден, выполните:")
    print("1. python manage.py makemigrations pwa")
    print("2. python manage.py migrate") 
    print("3. python add_petrov_fast.py")
    print("4. python manage.py runserver")

if __name__ == "__main__":
    main()
