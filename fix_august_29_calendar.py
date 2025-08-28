#!/usr/bin/env python
"""
Скрипт для исправления отображения 29 августа в православном календаре
Добавляет событие "Усекновение главы Иоанна Предтечи" если его нет
"""

import os
import sys
import django
from datetime import date

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo

def fix_august_29_calendar():
    """Исправить отображение 29 августа в календаре"""
    
    print("🔧 Исправление календаря для 29 августа...")
    
    # 1. Проверяем есть ли событие "Усекновение главы Иоанна Предтечи"
    john_beheading_old_style = OrthodoxEvent.objects.filter(
        month=8, 
        day=29,
        title__icontains="Усекновение"
    ).first()
    
    if not john_beheading_old_style:
        print("➕ Добавляем событие 'Усекновение главы Иоанна Предтечи' на 29 августа")
        john_beheading_old_style = OrthodoxEvent.objects.create(
            title="Усекновение главы Иоанна Предтечи",
            description="Строгий постный день в память о мученической кончине святого Иоанна Крестителя",
            event_type="special_day",  # Особый день, а не праздник
            month=8,
            day=29,
            is_old_style=True
        )
        print(f"✅ Создано событие: {john_beheading_old_style}")
    else:
        # Обновляем тип события, если это был праздник
        if john_beheading_old_style.event_type in ['great_feast', 'major_feast']:
            print(f"🔄 Обновляем тип события с '{john_beheading_old_style.event_type}' на 'special_day'")
            john_beheading_old_style.event_type = 'special_day'
            john_beheading_old_style.description = "Строгий постный день в память о мученической кончине святого Иоанна Крестителя"
            john_beheading_old_style.save()
            print("✅ Событие обновлено")
        else:
            print(f"✅ Событие уже существует: {john_beheading_old_style}")
    
    # 2. Проверяем/создаем ежедневную информацию для 29 августа
    daily_info_29_aug = DailyOrthodoxInfo.objects.filter(month=8, day=29).first()
    
    if not daily_info_29_aug:
        print("➕ Создаем ежедневную информацию для 29 августа")
        daily_info_29_aug = DailyOrthodoxInfo.objects.create(
            month=8,
            day=29,
            fasting_type='strict_fast',
            fasting_description='Усекновение главы Иоанна Предтечи (строгий пост)',
            allowed_food='Сухоядение: хлеб, овощи, фрукты, орехи (без масла)',
            spiritual_note='⚔️ Усекновение главы Иоанна Предтечи. Строгий постный день в память о мученической кончине святого Предтечи. Ореховый Спас отмечается, но пост сохраняется.'
        )
        print(f"✅ Создана ежедневная информация: {daily_info_29_aug}")
    else:
        # Обновляем информацию
        updated = False
        if daily_info_29_aug.fasting_type != 'strict_fast':
            daily_info_29_aug.fasting_type = 'strict_fast'
            updated = True
        if 'Усекновение' not in daily_info_29_aug.fasting_description:
            daily_info_29_aug.fasting_description = 'Усекновение главы Иоанна Предтечи (строгий пост)'
            updated = True
        if 'Сухоядение' not in daily_info_29_aug.allowed_food:
            daily_info_29_aug.allowed_food = 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)'
            updated = True
        if updated:
            daily_info_29_aug.spiritual_note = '⚔️ Усекновение главы Иоанна Предтечи. Строгий постный день в память о мученической кончине святого Предтечи. Ореховый Спас отмечается, но пост сохраняется.'
            daily_info_29_aug.save()
            print(f"🔄 Ежедневная информация обновлена: {daily_info_29_aug}")
        else:
            print(f"✅ Ежедневная информация уже корректна: {daily_info_29_aug}")
    
    # 3. Тестируем алгоритм для 29 августа 2025
    print("\n🧪 Тестируем алгоритм для 29 августа 2025...")
    test_date = date(2025, 8, 29)
    
    # Получаем информацию через вечный алгоритм
    test_daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
    test_events = OrthodoxEvent.get_events_for_date(test_date)
    
    print(f"📅 Дата: {test_date}")
    print(f"🍽️ Тип поста: {test_daily_info.fasting_type}")
    print(f"📝 Описание поста: {test_daily_info.fasting_description}")
    print(f"🥗 Разрешенная пища: {test_daily_info.allowed_food}")
    print(f"🙏 Духовная заметка: {test_daily_info.spiritual_note}")
    print(f"📅 События дня: {[event.title for event in test_events]}")
    
    # Тестируем функцию определения типа дня для календаря
    from pwa.views import get_day_type_for_calendar
    day_type = get_day_type_for_calendar(test_date, test_daily_info, test_events)
    print(f"🎨 Тип дня для календаря: {day_type}")
    
    if day_type == 'fast-day':
        print("✅ УСПЕХ! 29 августа теперь правильно отображается как постный день (фиолетовый)")
    else:
        print(f"❌ ОШИБКА! 29 августа отображается как '{day_type}', а должно быть 'fast-day'")
    
    print("\n🎯 Исправление завершено!")
    
    return test_daily_info, test_events, day_type

if __name__ == "__main__":
    try:
        daily_info, events, day_type = fix_august_29_calendar()
        
        print(f"\n📊 ИТОГОВАЯ ИНФОРМАЦИЯ:")
        print(f"Тип поста: {daily_info.fasting_type}")
        print(f"Тип дня для календаря: {day_type}")
        print(f"Количество событий: {len(events)}")
        
        if day_type == 'fast-day':
            print("🎉 29 августа будет отображаться ФИОЛЕТОВЫМ цветом (пост)")
        else:
            print("⚠️ Возможно, нужны дополнительные исправления")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
