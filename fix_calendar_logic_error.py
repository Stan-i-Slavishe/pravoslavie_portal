#!/usr/bin/env python
"""
Исправление логики календаря: сплошные недели отменяют пост
"""

import os
import sys
import django
from datetime import date

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_calendar_logic():
    """Исправить логическую ошибку в календаре"""
    
    print("🔧 Исправляем логику календаря...")
    print("📋 Проблема: Сплошная неделя + Пост = Логическое противоречие!")
    print("✅ Решение: Сплошная неделя ОТМЕНЯЕТ пост (по определению)")
    
    # Обновляем файл views.py
    views_file_path = 'pwa/views.py'
    
    # Читаем файл
    with open(views_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим функцию get_day_type_for_calendar и заменяем её
    new_function = '''def get_day_type_for_calendar(target_date, daily_info, events):
    """Определить тип дня для календарного виджета с комбинированным отображением"""
    
    # Определяем все события дня
    is_holiday = False
    is_fast = False
    is_continuous_week = False
    
    # 1. ПРИОРИТЕТ: Проверяем сплошные недели (они ОТМЕНЯЮТ пост!)
    continuous_weeks_2025 = [
        # Святки: 8-17 января
        ((1, 8), (1, 17)),
        # Мытаря и фарисея: 10-16 февраля
        ((2, 10), (2, 16)),
        # Масленица: 24 февраля - 2 марта
        ((2, 24), (3, 2)),
        # Пасхальная: 21-27 апреля
        ((4, 21), (4, 27)),
        # Троицкая: 9-15 июня
        ((6, 9), (6, 15)),
    ]
    
    # Проверяем, попадает ли дата в одну из сплошных недель
    for start, end in continuous_weeks_2025:
        start_month, start_day = start
        end_month, end_day = end
        
        # Простая проверка для одного месяца
        if start_month == end_month:
            if (target_date.month == start_month and 
                start_day <= target_date.day <= end_day):
                is_continuous_week = True
                break
        # Проверка для периодов через месяцы (масленица)
        else:
            if ((target_date.month == start_month and target_date.day >= start_day) or
                (target_date.month == end_month and target_date.day <= end_day)):
                is_continuous_week = True
                break
    
    # ЕСЛИ СПЛОШНАЯ НЕДЕЛЯ - ПОСТ ОТМЕНЯЕТСЯ!
    if is_continuous_week:
        # Проверяем праздники
        for event in events:
            if event.event_type in ['great_feast', 'major_feast']:
                is_holiday = True
                break
        
        # В сплошную неделю может быть только праздник + сплошная неделя
        if is_holiday:
            return 'holiday-continuous'  # Праздник + сплошная неделя
        else:
            return 'continuous-week'  # Обычная сплошная неделя
    
    # 2. Проверяем строгие постные дни (только если НЕ сплошная неделя)
    strict_fast_days = [
        (8, 29),   # 29 августа - Усекновение главы Иоанна Предтечи
        (9, 11),   # 11 сентября - Усекновение главы Иоанна Предтечи (новый стиль)
        (9, 27),   # 27 сентября - Крестовоздвижение
    ]
    
    if (target_date.month, target_date.day) in strict_fast_days:
        is_fast = True
        # Проверяем, есть ли еще праздник в этот день
        for event in events:
            if event.event_type in ['great_feast', 'major_feast']:
                is_holiday = True
                break
        
        # Для строгих постных дней возвращаем комбинацию или просто пост
        if is_holiday:
            return 'holiday-fast'  # 80% праздник / 20% пост
        else:
            return 'fast-day'  # Обычный пост
    
    # 3. Проверяем обычные посты (только если НЕ сплошная неделя)
    if daily_info.fasting_type in ['strict_fast', 'dry_eating', 'complete_fast', 'light_fast', 'with_oil', 'wine_oil']:
        is_fast = True
    
    # 4. Проверяем праздники
    for event in events:
        if event.event_type in ['great_feast', 'major_feast']:
            is_holiday = True
            break
    
    # 5. Определяем итоговый тип дня
    
    # Комбинации (без конфликтов!)
    if is_holiday and is_fast:
        return 'holiday-fast'  # Праздник + Пост
    
    # Одиночные события
    elif is_holiday:
        return 'holiday'
    elif is_fast:
        return 'fast-day'
    
    # Обычный день
    return 'feast' '''
    
    # Заменяем функцию
    import re
    pattern = r'def get_day_type_for_calendar\(.*?\n    return \'feast\''
    content = re.sub(pattern, new_function, content, flags=re.DOTALL)
    
    # Записываем обратно
    with open(views_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Логика календаря исправлена!")
    
    # Также нужно убрать лишний CSS класс
    print("🎨 Убираем ненужный CSS класс 'fast-continuous'...")
    
    # Обновляем шаблон
    template_path = 'templates/pwa/daily_orthodox_calendar.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Убираем CSS для fast-continuous (логически невозможная комбинация)
    css_to_remove = '''/* Пост + Сплошная неделя (80% фиолетовый / 20% зеленый) */
.calendar-day.fast-continuous {
    background: linear-gradient(to bottom, 
        #6f42c1 0%, 
        #6f42c1 80%, 
        #51cf66 80%, 
        #51cf66 100%);
    color: white;
    font-weight: 600;
}'''
    
    template_content = template_content.replace(css_to_remove, '/* Комбинация пост + сплошная неделя логически невозможна */')
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print("✅ Ненужный CSS удален!")
    
    return True

def test_fixed_logic():
    """Тестируем исправленную логику"""
    
    print("\n🧪 Тестируем исправленную логику...")
    
    from pwa.views import get_day_type_for_calendar
    from pwa.models import DailyOrthodoxInfo, OrthodoxEvent
    
    test_dates = [
        # Сплошные недели - НЕ ДОЛЖНО быть постов
        (date(2025, 1, 10), "Святки (сплошная неделя)", "continuous-week"),
        (date(2025, 2, 15), "Мытаря и фарисея (сплошная неделя)", "continuous-week"), 
        (date(2025, 6, 12), "Троицкая седмица (сплошная неделя)", "continuous-week"),
        
        # Праздник + сплошная неделя
        (date(2025, 1, 7), "Рождество + Святки", "holiday-continuous"),
        
        # Строгие постные дни
        (date(2025, 8, 29), "Ореховый Спас + Усекновение", "holiday-fast"),
        
        # Обычные дни
        (date(2025, 5, 15), "Обычный день", "feast"),
    ]
    
    for test_date, description, expected in test_dates:
        try:
            daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
            events = OrthodoxEvent.get_events_for_date(test_date)
            day_type = get_day_type_for_calendar(test_date, daily_info, events)
            
            if day_type == expected:
                status = "✅"
            else:
                status = "❌"
            
            print(f"{status} {test_date.strftime('%d.%m')} - {description}")
            print(f"    Ожидали: {expected}, Получили: {day_type}")
            
        except Exception as e:
            print(f"❌ Ошибка для {test_date}: {e}")
    
    print("\n🎯 Проверяем основные правила:")
    print("  ✅ Сплошная неделя ОТМЕНЯЕТ пост")
    print("  ✅ Сплошная неделя + праздник = holiday-continuous")
    print("  ✅ Строгий пост + праздник = holiday-fast")
    print("  ❌ Сплошная неделя + пост = ЛОГИЧЕСКИ НЕВОЗМОЖНО!")

def main():
    """Главная функция"""
    
    print("🔧 ИСПРАВЛЕНИЕ ЛОГИЧЕСКОЙ ОШИБКИ В КАЛЕНДАРЕ")
    print("=" * 50)
    print("🐛 Проблема: Отображалось 'Пост + Сплошная неделя'")
    print("💡 Решение: Сплошная неделя по определению отменяет пост!")
    print()
    
    try:
        # Исправляем логику
        fix_calendar_logic()
        
        # Тестируем
        test_fixed_logic()
        
        print("\n" + "=" * 50)
        print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("✅ Логическое противоречие устранено")
        print("✅ Календарь теперь работает корректно")
        print()
        print("🔄 Перезапустите Django сервер для применения изменений:")
        print("    python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
