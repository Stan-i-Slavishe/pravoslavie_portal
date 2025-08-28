#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo
from datetime import date

def check_august_29():
    print("Проверяем 29 августа 2025...")
    
    target_date = date(2025, 8, 29)
    print(f"Дата: {target_date}")
    print(f"День недели: {target_date.strftime('%A')} (пятница)")
    
    # Проверяем события на эту дату
    events = OrthodoxEvent.get_events_for_date(target_date)
    print(f"\nСобытия на эту дату ({len(events)}):")
    for event in events:
        print(f"  - ID:{event.id} '{event.title}' ({event.event_type})")
        print(f"    Описание: {event.description}")
        print(f"    Переходящий: {event.is_movable}")
    
    # Проверяем информацию о дне
    daily_info = DailyOrthodoxInfo.get_info_for_date(target_date)
    print(f"\nИнформация о дне:")
    print(f"  Тип поста: {daily_info.fasting_type} ({daily_info.get_fasting_type_display()})")
    print(f"  Описание: {daily_info.fasting_description}")
    print(f"  Разрешенная пища: {daily_info.allowed_food}")
    
    # Проверяем активные периоды постов
    active_periods = DailyOrthodoxInfo.get_active_fasting_periods(target_date)
    print(f"\nАктивные периоды постов ({len(active_periods)}):")
    for period in active_periods:
        print(f"  - {period.title} (приоритет: {period.priority})")
        weekday = target_date.weekday()
        fasting_type = period.get_fasting_type_for_weekday(weekday)
        print(f"    Тип поста в пятницу: {fasting_type}")
    
    # Проверяем что происходит в августе
    print(f"\nПроверяем другие дни августа:")
    
    # 28 августа - Успение
    uspenie_date = date(2025, 8, 28)
    uspenie_events = OrthodoxEvent.get_events_for_date(uspenie_date)
    print(f"28 августа: {len(uspenie_events)} событий")
    for event in uspenie_events:
        print(f"  - '{event.title}' ({event.event_type})")
    
    # 27 августа - окончание Успенского поста
    end_fast_date = date(2025, 8, 27)
    end_fast_info = DailyOrthodoxInfo.get_info_for_date(end_fast_date)
    print(f"27 августа: {end_fast_info.get_fasting_type_display()}")
    
    # 30 августа - следующий день
    next_date = date(2025, 8, 30)
    next_info = DailyOrthodoxInfo.get_info_for_date(next_date)
    print(f"30 августа: {next_info.get_fasting_type_display()}")

if __name__ == "__main__":
    check_august_29()
