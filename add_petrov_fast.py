#!/usr/bin/env python
"""
Добавление Петрова поста в православный календарь
"""

import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import FastingPeriod, OrthodoxEvent, DailyOrthodoxInfo

def add_petrov_fast():
    """Добавить Петров пост в базу данных"""
    
    print("⛪ Добавляем Петров пост в календарь...")
    
    # Создаем или обновляем Петров пост
    petrov_fast, created = FastingPeriod.objects.get_or_create(
        name='peter_paul_fast',
        defaults={
            'title': 'Петров пост (Апостольский пост)',
            'description': 'Пост в честь святых апостолов Петра и Павла. Начинается через неделю после Троицы и длится до 12 июля.',
            
            # Фиксированный конец - 12 июля (День Петра и Павла)
            'end_month': 7,
            'end_day': 12,
            
            # Переходящее начало - понедельник после Троицкой седмицы
            'easter_start_offset': 57,  # Троица +49, плюс неделя Троицкой седмицы +7 = 56, понедельник +1 = 57
            'easter_end_offset': None,  # Конец фиксированный
            
            # Правила поста по дням недели
            'fasting_rules': {
                'monday': 'strict_fast',      # Понедельник - строгий пост
                'tuesday': 'with_fish',       # Вторник - можно рыбу  
                'wednesday': 'strict_fast',   # Среда - строгий пост
                'thursday': 'with_fish',      # Четверг - можно рыбу
                'friday': 'strict_fast',      # Пятница - строгий пост
                'saturday': 'with_fish',      # Суббота - можно рыбу
                'sunday': 'with_fish'         # Воскресенье - можно рыбу
            },
            
            'priority': 8,  # Высокий приоритет (выше обычных постных дней)
            'is_active': True
        }
    )
    
    if created:
        print("✅ Петров пост успешно добавлен в базу данных!")
    else:
        print("📅 Петров пост уже существует, обновляем...")
        
        # Обновляем существующий пост
        petrov_fast.title = 'Петров пост (Апостольский пост)'
        petrov_fast.description = 'Пост в честь святых апостолов Петра и Павла. Начинается через неделю после Троицы и длится до 12 июля.'
        petrov_fast.end_month = 7
        petrov_fast.end_day = 12
        petrov_fast.easter_start_offset = 57
        petrov_fast.easter_end_offset = None
        petrov_fast.fasting_rules = {
            'monday': 'strict_fast',
            'tuesday': 'with_fish',
            'wednesday': 'strict_fast', 
            'thursday': 'with_fish',
            'friday': 'strict_fast',
            'saturday': 'with_fish',
            'sunday': 'with_fish'
        }
        petrov_fast.priority = 8
        petrov_fast.is_active = True
        petrov_fast.save()
        
        print("✅ Петров пост обновлен!")
    
    return petrov_fast

def test_petrov_fast_2026():
    """Тестируем Петров пост для 2026 года"""
    
    print("\n🧪 Тестируем Петров пост 2026...")
    
    # Вычисляем даты
    easter_date = OrthodoxEvent.calculate_easter(2026)
    start_date = easter_date + timedelta(days=57)
    end_date = date(2026, 7, 12)
    
    print(f"📅 Петров пост 2026:")
    print(f"   Пасха: {easter_date.strftime('%d.%m.%Y')}")
    print(f"   Троица: {(easter_date + timedelta(days=49)).strftime('%d.%m.%Y')}")
    print(f"   Начало поста: {start_date.strftime('%d.%m.%Y')}")
    print(f"   Конец поста: {end_date.strftime('%d.%m.%Y')}")
    print(f"   Продолжительность: {(end_date - start_date).days + 1} дней")
    
    # Проверяем несколько дней июня
    test_dates = [
        date(2026, 6, 1),   # 1 июня - Троицкая седмица (сплошная)
        date(2026, 6, 8),   # 8 июня - Петров пост (понедельник - строгий)
        date(2026, 6, 9),   # 9 июня - Петров пост (вторник - с рыбой)
        date(2026, 6, 10),  # 10 июня - Петров пост (среда - строгий)
        date(2026, 6, 15),  # 15 июня - Петров пост (воскресенье - с рыбой)
        date(2026, 6, 30),  # 30 июня - Петров пост
        date(2026, 7, 12),  # 12 июля - День Петра и Павла (конец поста)
        date(2026, 7, 13),  # 13 июля - после поста
    ]
    
    print(f"\n📋 Проверка дней:")
    for test_date in test_dates:
        try:
            daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
            events = OrthodoxEvent.get_events_for_date(test_date)
            
            weekday_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'][test_date.weekday()]
            
            print(f"   {test_date.strftime('%d.%m')} ({weekday_ru}): {daily_info.get_fasting_type_display()} - {daily_info.fasting_description}")
            
        except Exception as e:
            print(f"   ❌ Ошибка для {test_date}: {e}")

def main():
    """Главная функция"""
    
    print("🚀 Добавление Петрова поста в православный календарь")
    print("=" * 60)
    
    try:
        # 1. Добавляем Петров пост
        petrov_fast = add_petrov_fast()
        
        # 2. Тестируем на реальных датах
        test_petrov_fast_2026()
        
        print("=" * 60)
        print("🎉 ПЕТРОВ ПОСТ УСПЕШНО ДОБАВЛЕН!")
        print()
        print("📋 Что добавлено:")
        print("   ⛪ Петров пост с правильными датами")
        print("   📅 Динамический расчет начала (после Троицы)")
        print("   🐟 Правила поста по дням недели")
        print("   🔄 Интеграция с календарным виджетом")
        print()
        print("🔄 Перезапустите Django сервер для применения изменений!")
        print("   python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
