#!/usr/bin/env python
"""
Создание ежедневного православного календаря
"""

import os
import sys
import django
from datetime import date

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import DailyOrthodoxInfo

# Данные о постных днях и особых событиях
DAILY_ORTHODOX_DATA = [
    # Рождественские праздники
    {'month': 1, 'day': 6, 'fasting_type': 'dry_eating',
     'fasting_description': 'Рождественский сочельник',
     'allowed_food': 'Сухоядение до первой звезды',
     'spiritual_note': 'Сочельник. До вечерни - строгий пост, после - праздничная трапеза. Подготовка к Великому празднику Рождества.'},
    
    {'month': 1, 'day': 7, 'fasting_type': 'no_fast',
     'fasting_description': 'Рождество Христово',
     'allowed_food': 'Праздничная трапеза',
     'spiritual_note': '🎄 Рождество Христово! Великий праздник рождения Спасителя. Время радости и любви.'},
    
    {'month': 1, 'day': 18, 'fasting_type': 'dry_eating',
     'fasting_description': 'Крещенский сочельник',
     'allowed_food': 'Сухоядение до освящения воды',
     'spiritual_note': 'Сочельник перед Крещением. Время особой молитвы и очищения.'},
    
    {'month': 1, 'day': 19, 'fasting_type': 'no_fast',
     'fasting_description': 'Крещение Господне',
     'allowed_food': 'Праздничная трапеза',
     'spiritual_note': '💧 Крещение Господне! Освящение воды и воспоминание крещения Христа.'},
    
    # Великие праздники
    {'month': 4, 'day': 7, 'fasting_type': 'with_fish',
     'fasting_description': 'Благовещение Пресвятой Богородицы',
     'allowed_food': 'Праздничная трапеза (даже в Великий пост можно рыбу)',
     'spiritual_note': '🕊️ Благовещение! Архангел Гавриил возвестил Деве Марии о рождении Спасителя.'},
    
    {'month': 8, 'day': 19, 'fasting_type': 'no_fast',
     'fasting_description': 'Преображение Господне',
     'allowed_food': 'Праздничная трапеза, освящение плодов',
     'spiritual_note': '✨ Преображение Господне! Освящение плодов нового урожая.'},
    
    {'month': 8, 'day': 28, 'fasting_type': 'no_fast',
     'fasting_description': 'Успение Пресвятой Богородицы',
     'allowed_food': 'Праздничная трапеза',
     'spiritual_note': '🌸 Успение Пресвятой Богородицы! Блаженная кончина Матери Божией.'},
    
    # Строгие постные дни
    {'month': 9, 'day': 27, 'fasting_type': 'strict_fast',
     'fasting_description': 'Воздвижение Креста Господня',
     'allowed_food': 'Строгий пост (как в пятницу Великого поста)',
     'spiritual_note': '✝️ Воздвижение Креста Господня. День особого поклонения Кресту.'},
    
    {'month': 8, 'day': 29, 'fasting_type': 'strict_fast',
     'fasting_description': 'Усекновение главы Иоанна Предтечи',
     'allowed_food': 'Строгий пост',
     'spiritual_note': 'День памяти усекновения главы Иоанна Предтечи. Строгий пост.'},
    
    # Дни великих святых
    {'month': 12, 'day': 19, 'fasting_type': 'with_fish',
     'fasting_description': 'День святителя Николая в Рождественский пост',
     'allowed_food': 'Растительная пища, рыба, масло',
     'spiritual_note': 'День памяти святителя Николая Чудотворца. Великий заступник и помощник.'},
    
    {'month': 10, 'day': 8, 'fasting_type': 'light_fast',
     'fasting_description': 'День преподобного Сергия Радонежского',
     'allowed_food': 'Растительная пища с маслом',
     'spiritual_note': 'День памяти преподобного Сергия Радонежского. Игумен земли Русской.'},
    
    {'month': 7, 'day': 8, 'fasting_type': 'light_fast',
     'fasting_description': 'День святых Петра и Февронии',
     'allowed_food': 'Растительная пища',
     'spiritual_note': 'День святых Петра и Февронии Муромских. Покровители семьи и брака.'},
    
    # Особые посты
    {'month': 12, 'day': 4, 'fasting_type': 'light_fast',
     'fasting_description': 'День введения во храм Пресвятой Богородицы',
     'allowed_food': 'Растительная пища с маслом',
     'spiritual_note': 'Введение во храм Пресвятой Богородицы. Детство Богородицы.'},
    
    # Примеры обычных постных дней
    {'month': 1, 'day': 15, 'fasting_type': 'light_fast',
     'fasting_description': 'Постный день (среда)',
     'allowed_food': 'Растительная пища, можно масло',
     'spiritual_note': 'Обычный постный день. Время для молитвы и воздержания.'},
    
    {'month': 1, 'day': 17, 'fasting_type': 'light_fast',
     'fasting_description': 'Постный день (пятница)',
     'allowed_food': 'Растительная пища, можно масло',
     'spiritual_note': 'Постный день в память страданий Христовых.'},
    
    # Примеры обычных дней
    {'month': 1, 'day': 20, 'fasting_type': 'no_fast',
     'fasting_description': 'Обычный день',
     'allowed_food': 'Любая пища',
     'spiritual_note': 'Обычный день. Благодарите Бога за все дары. Время для добрых дел.'},
]

def create_daily_orthodox_info():
    """Создание ежедневной православной информации"""
    
    created_count = 0
    updated_count = 0
    
    for info_data in DAILY_ORTHODOX_DATA:
        daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
            month=info_data['month'],
            day=info_data['day'],
            defaults=info_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Создан день: {daily_info}")
        else:
            # Обновляем существующую запись
            for key, value in info_data.items():
                if key not in ['month', 'day']:
                    setattr(daily_info, key, value)
            daily_info.save()
            updated_count += 1
            print(f"🔄 Обновлен день: {daily_info}")
    
    print(f"\n📊 Результат:")
    print(f"Создано новых дней: {created_count}")
    print(f"Обновлено дней: {updated_count}")
    print(f"Всего дней в базе: {DailyOrthodoxInfo.objects.count()}")

def test_daily_info():
    """Тестирование ежедневной информации"""
    print("\n🧪 Тестирование ежедневной информации...")
    
    # Тестируем разные даты
    test_dates = [
        date(2024, 1, 7),   # Рождество
        date(2024, 1, 19),  # Крещение
        date(2024, 12, 25), # Среда (постный день)
        date(2024, 12, 27), # Пятница (постный день)
        date.today(),       # Сегодня
    ]
    
    for test_date in test_dates:
        print(f"\n📅 {test_date.strftime('%d.%m.%Y')} ({['Пн','Вт','Ср','Чт','Пт','Сб','Вс'][test_date.weekday()]})")
        
        daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
        
        print(f"   🍽️ Пост: {daily_info.get_fasting_type_display()}")
        print(f"   🥗 Пища: {daily_info.allowed_food}")
        if daily_info.spiritual_note:
            print(f"   🕊️ Наставление: {daily_info.spiritual_note[:80]}...")

if __name__ == '__main__':
    print("🍽️ Создание ежедневного православного календаря...")
    create_daily_orthodox_info()
    test_daily_info()
    print("\n✨ Готово! Теперь можно запустить:")
    print("python manage.py makemigrations pwa")
    print("python manage.py migrate")
    print("python manage.py runserver")
    print("\nОткройте: http://127.0.0.1:8000/pwa/daily-calendar/")
