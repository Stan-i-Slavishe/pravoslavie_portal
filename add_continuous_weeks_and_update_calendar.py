#!/usr/bin/env python
"""
Добавление сплошных седмиц и обновление календаря с комбинированным отображением 80/20
"""

import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo

def add_continuous_weeks_2025():
    """Добавить сплошные седмицы (недели без поста в среду/пятницу) на 2025 год"""
    
    print("🗓️ Добавляем сплошные седмицы на 2025 год...")
    
    continuous_weeks_2025 = [
        {
            'name': 'Святки (Рождественские)',
            'start_date': date(2025, 1, 8),
            'end_date': date(2025, 1, 17),
            'description': 'Рождественские Святки - время радости и духовного обновления. Отменяется пост в среду и пятницу.'
        },
        {
            'name': 'Неделя мытаря и фарисея',
            'start_date': date(2025, 2, 10),
            'end_date': date(2025, 2, 16),
            'description': 'Подготовительная неделя к Великому посту. Отменяется пост в среду и пятницу.'
        },
        {
            'name': 'Масленица (Сырная седмица)',
            'start_date': date(2025, 2, 24),
            'end_date': date(2025, 3, 2),
            'description': 'Последняя неделя перед Великим постом, разрешены молочные продукты. Отменяется пост в среду и пятницу.'
        },
        {
            'name': 'Светлая Пасхальная седмица',
            'start_date': date(2025, 4, 21),
            'end_date': date(2025, 4, 27),
            'description': 'Пасхальная неделя - время величайшей радости Воскресения Христова. Отменяется пост в среду и пятницу.'
        },
        {
            'name': 'Троицкая седмица',
            'start_date': date(2025, 6, 9),
            'end_date': date(2025, 6, 15),
            'description': 'Неделя после Троицы перед началом Петрова поста. Отменяется пост в среду и пятницу.'
        }
    ]
    
    created_count = 0
    
    for week_info in continuous_weeks_2025:
        print(f"\\n📅 Обрабатываем: {week_info['name']}")
        
        current_date = week_info['start_date']
        day_count = 0
        
        while current_date <= week_info['end_date']:
            existing_event = OrthodoxEvent.objects.filter(
                month=current_date.month,
                day=current_date.day,
                title__icontains='сплошная'
            ).first()
            
            if not existing_event:
                event = OrthodoxEvent.objects.create(
                    title=f"Сплошная седмица: {week_info['name']}",
                    description=week_info['description'],
                    event_type='special_day',
                    month=current_date.month,
                    day=current_date.day,
                    year=None
                )
                created_count += 1
                day_count += 1
                print(f"   ✅ {current_date.strftime('%d.%m')} - создано событие")
            else:
                print(f"   ⏭️ {current_date.strftime('%d.%m')} - событие уже существует")
            
            current_date += timedelta(days=1)
        
        print(f"   📊 Дней в седмице: {day_count}")
    
    print(f"\\n🎉 Добавлено {created_count} событий сплошных седмиц!")
    return created_count

def create_test_events():
    """Создать тестовые события"""
    
    print("🎭 Создаем тестовые события...")
    
    test_events = [
        {
            'date': (1, 7),
            'title': 'Рождество Христово',
            'description': 'Великий праздник Рождества Господа нашего Иисуса Христа',
            'event_type': 'great_feast'
        },
        {
            'date': (8, 19),
            'title': 'Преображение Господне',
            'description': 'Великий праздник Преображения Господа',
            'event_type': 'great_feast'
        },
        {
            'date': (8, 29),
            'title': 'Ореховый Спас (Нерукотворный Образ)',
            'description': 'Третий Спас. Освящение орехов и хлеба нового урожая.',
            'event_type': 'major_feast'
        }
    ]
    
    created_count = 0
    
    for event_info in test_events:
        month, day = event_info['date']
        
        existing = OrthodoxEvent.objects.filter(
            month=month,
            day=day,
            title=event_info['title']
        ).first()
        
        if not existing:
            event = OrthodoxEvent.objects.create(
                title=event_info['title'],
                description=event_info['description'],
                event_type=event_info['event_type'],
                month=month,
                day=day
            )
            created_count += 1
            print(f"✅ Создано: {day:02d}.{month:02d} - {event_info['title']}")
        else:
            print(f"⏭️ Уже существует: {day:02d}.{month:02d} - {event_info['title']}")
    
    print(f"🎉 Создано {created_count} тестовых событий!")
    return created_count

def test_combined_display():
    """Тестируем комбинированное отображение"""
    
    print("\\n🧪 Тестируем комбинированное отображение...")
    
    from pwa.views import get_day_type_for_calendar
    
    test_dates = [
        (date(2025, 8, 29), "Ореховый Спас + Усекновение главы Иоанна Предтечи"),
        (date(2025, 1, 7), "Рождество + Святки"),
        (date(2025, 6, 15), "Троицкая седмица"),
        (date(2025, 8, 19), "Преображение Господне"),
        (date(2025, 3, 3), "Великий пост"),
        (date(2025, 5, 15), "Обычный день"),
    ]
    
    for test_date, description in test_dates:
        try:
            daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
            events = OrthodoxEvent.get_events_for_date(test_date)
            day_type = get_day_type_for_calendar(test_date, daily_info, events)
            
            color_description = {
                'holiday': '🔴 Красный (праздник)',
                'fast-day': '🟣 Фиолетовый (пост)',
                'continuous-week': '🟢 Зеленый (сплошная неделя)',
                'holiday-fast': '🔴🟣 Красный + фиолетовый (80/20)',
                'holiday-continuous': '🔴🟢 Красный + зеленый (80/20)',
                'fast-continuous': '🟣🟢 Фиолетовый + зеленый (80/20)',
                'feast': '⚪ Обычный (без выделения)'
            }.get(day_type, '❓ Неизвестный тип')
            
            print(f"📅 {test_date.strftime('%d.%m.%Y')} - {description}")
            print(f"   Тип дня: {day_type}")
            print(f"   Отображение: {color_description}")
            print(f"   События: {[event.title for event in events]}")
            print()
            
        except Exception as e:
            print(f"❌ Ошибка для {test_date}: {e}")
    
    return True

def main():
    """Главная функция"""
    
    print("🚀 Обновление православного календаря с комбинированным отображением")
    print("=" * 70)
    
    try:
        # 1. Добавляем сплошные седмицы
        continuous_count = add_continuous_weeks_2025()
        
        # 2. Создаем тестовые события
        events_count = create_test_events()
        
        # 3. Тестируем комбинированное отображение
        test_combined_display()
        
        print("=" * 70)
        print("🎉 ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        print(f"✅ Добавлено сплошных седмиц: {continuous_count}")
        print(f"✅ Создано тестовых событий: {events_count}")
        print()
        print("🎨 Теперь в календаре доступно:")
        print("   🔴 Красный - праздники")
        print("   🟣 Фиолетовый - посты")
        print("   🟢 Зеленый - сплошные недели")
        print("   🎭 Комбинированные (80/20) - несколько событий в один день")
        print()
        print("🔧 Для применения изменений перезапустите Django сервер!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
