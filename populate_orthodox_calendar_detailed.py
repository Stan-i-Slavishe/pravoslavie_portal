#!/usr/bin/env python
"""
Скрипт для заполнения православного календаря подробной достоверной информацией о постах.
Запуск: python populate_orthodox_calendar_detailed.py
"""

import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from pwa.models import DailyOrthodoxInfo, OrthodoxEvent

def populate_success_fast_info():
    """Заполнение информации об Успенском посте с достоверными данными"""
    print("🍇 Обновляем информацию об Успенском посте...")
    
    # Успенский пост: 14-27 августа 2025
    start_date = date(2025, 8, 14)
    end_date = date(2025, 8, 27)
    
    current = start_date
    while current <= end_date:
        weekday = current.weekday()  # 0=понедельник, 6=воскресенье
        
        try:
            daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                month=current.month,
                day=current.day
            )
            
            # Успенский пост строгий как Великий пост
            if current.day == 19 and current.month == 8:  # Преображение Господне
                # 19 августа - Преображение, можно рыбу
                daily_info.fasting_type = 'with_fish'
                daily_info.fasting_description = 'Успенский пост: Преображение Господне (Яблочный Спас)'
                daily_info.allowed_food = '''🍎 <strong>Преображение Господне - можно рыбу!</strong>

В праздник Преображения разрешается:

✅ <strong>Можно:</strong>
• Рыба и морепродукты 🐟
• Растительная пища с маслом
• Овощи, фрукты (особенно яблоки!)
• Каши с маслом
• Грибы жареные
• Орехи, мед
• Вино (немного)

🍎 <strong>Традиция:</strong> Освящение яблок и других плодов

❌ <strong>Запрещено:</strong>
• Мясо и мясные продукты
• Молочные продукты  
• Яйца'''
                daily_info.spiritual_note = '🍎 Преображение Господне! Яблочный Спас. Благословите новый урожай и вспомните о преображении души.'
                
            elif weekday in [0, 2, 4]:  # Понедельник, среда, пятница - сухоядение
                daily_info.fasting_type = 'dry_eating'
                daily_info.fasting_description = 'Успенский пост: сухоядение'
                daily_info.allowed_food = '''🥗 <strong>Успенский пост - сухоядение (холодная пища):</strong>

Август богат дарами природы!

✅ <strong>Разрешается:</strong>
• Свежие овощи: огурцы, помидоры, капуста, морковь, перец
• Летние фрукты: яблоки, груши, сливы, персики
• Ягоды: виноград, арбуз, дыня, смородина
• Орехи всех видов
• Семечки подсолнечные, тыквенные
• Мед свежий
• Хлеб постный (без молока и яиц)
• Сухофрукты: изюм, курага, инжир
• Вода, квас домашний, морсы (холодные)

❌ <strong>Запрещается:</strong>
• Любая горячая пища
• Растительное масло
• Продукты животного происхождения
• Варенье (можно мед)

💡 <strong>Совет:</strong> Делайте салаты из свежих овощей без масла, но с лимонным соком'''
                daily_info.spiritual_note = 'День сухоядения в Успенский пост. Время строгого воздержания в память о посте Богородицы перед Успением.'
                
            elif weekday in [1, 3]:  # Вторник, четверг - горячее без масла
                daily_info.fasting_type = 'strict_fast'
                daily_info.fasting_description = 'Успенский пост: горячая пища без масла'
                daily_info.allowed_food = '''🍲 <strong>Успенский пост - горячее без масла:</strong>

✅ <strong>Разрешается:</strong>
• Каши на воде: гречневая, овсяная, рисовая, пшенная
• Постные супы: овощные, грибные, щи постные
• Отварные овощи: картофель, морковь, свекла, капуста
• Картофель печеный в мундире
• Тушеные овощи без масла
• Грибы отварные, тушеные (без масла)
• Бобовые: горох, фасоль, чечевица
• Макароны (из твердых сортов пшеницы)
• Компоты из свежих фруктов
• Чай, кофе, травяные отвары

❌ <strong>Запрещается:</strong>
• Растительное масло для готовки
• Жареная пища
• Продукты животного происхождения
• Сливочное масло

💡 <strong>Рецепт:</strong> Овощное рагу без масла - тушите овощи в собственном соку'''
                daily_info.spiritual_note = 'Горячая пища без масла. Время умеренности и духовного сосредоточения.'
                
            else:  # Суббота, воскресенье - горячее с маслом
                daily_info.fasting_type = 'with_oil'
                daily_info.fasting_description = 'Успенский пост: горячая пища с растительным маслом'
                daily_info.allowed_food = '''🫒 <strong>Успенский пост - горячее с маслом:</strong>

✅ <strong>Разрешается:</strong>
• Все каши с растительным маслом
• Жареные и тушеные овощи
• Овощные рагу с маслом
• Салаты из свежих овощей с маслом
• Жареные грибы
• Картофель жареный, драники постные
• Постная выпечка (пирожки с капустой, картошкой)
• Постные блины на воде
• Соленые и маринованные овощи
• Варенье, джемы
• Вино красное (немного, по церковному уставу)

🍇 <strong>Августовские радости:</strong>
• Свежий виноград
• Арбузы и дыни
• Яблоки нового урожая
• Груши летние

❌ <strong>Запрещается:</strong>
• Мясо и мясные продукты
• Молочные продукты (молоко, сыр, творог, сметана)
• Яйца
• Рыба (кроме 19 августа)

💡 <strong>Особенность:</strong> Выходные дни поста более мягкие'''
                daily_info.spiritual_note = 'Выходной день поста. Время молитвы в семейном кругу и духовного общения.'
            
            daily_info.save()
            action = "Создана" if created else "Обновлена"
            print(f"   {action} информация для {current.strftime('%d.%m')}")
            
        except Exception as e:
            print(f"   Ошибка для {current.strftime('%d.%m')}: {e}")
            
        current += timedelta(days=1)

def create_success_orthodox_events():
    """Создание событий Успенского поста"""
    print("📅 Создаем события Успенского поста...")
    
    events = [
        (8, 14, "Медовый Спас (Происхождение Честных Древ)", "Первый Спас. Освящение меда и мака.", 'major_feast'),
        (8, 19, "Преображение Господне (Яблочный Спас)", "Великий праздник Преображения. Освящение яблок и винограда.", 'great_feast'),
        (8, 29, "Ореховый Спас (Нерукотворный Образ)", "Третий Спас. Освящение орехов и хлеба нового урожая.", 'major_feast'),
        (8, 28, "Успение Пресвятой Богородицы", "Великий праздник Успения Божией Матери.", 'great_feast'),
    ]
    
    for month, day, title, description, event_type in events:
        event, created = OrthodoxEvent.objects.get_or_create(
            month=month,
            day=day,
            title=title,
            defaults={
                'description': description,
                'event_type': event_type,
                'is_movable': False
            }
        )
        action = "Создано" if created else "Обновлено"
        print(f"   {action} событие: {title}")

def update_wednesdays_fridays():
    """Обновление информации о средах и пятницах"""
    print("📿 Обновляем информацию о постных средах и пятницах...")
    
    # Проходим по всем дням года
    for month in range(1, 13):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
        if month == 2 and 2025 % 4 == 0:  # Високосный год
            days_in_month = 29
            
        for day in range(1, days_in_month + 1):
            target_date = date(2025, month, day)
            weekday = target_date.weekday()
            
            # Среда и пятница - постные дни (если не в период многодневного поста)
            if weekday == 2:  # Среда
                try:
                    daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                        month=month,
                        day=day
                    )
                    
                    # Проверяем, не в многодневном ли посту
                    if daily_info.fasting_type == 'no_fast':
                        daily_info.fasting_type = 'light_fast'
                        daily_info.fasting_description = 'Постная среда'
                        daily_info.allowed_food = '''🥬 <strong>Постная среда:</strong>

✅ <strong>Разрешается:</strong>
• Растительная пища всех видов
• Каши на воде или с растительным маслом
• Овощи (свежие, тушеные, вареные, жареные)
• Фрукты и ягоды
• Орехи и семечки
• Грибы в любом виде
• Растительное масло
• Хлеб (без молока и яиц)
• Мед, варенье
• Напитки: чай, кофе, соки, компоты

❌ <strong>Не разрешается:</strong>
• Мясо и мясные продукты
• Молоко и молочные продукты (сыр, творог, сметана)
• Яйца
• Рыба и морепродукты
• Продукты, содержащие молоко и яйца'''
                        daily_info.spiritual_note = 'Среда - день воспоминания предательства Иуды. Время для покаяния и дел милосердия.'
                        daily_info.save()
                except Exception as e:
                    print(f"   Ошибка для среды {day}.{month}: {e}")
                    
            elif weekday == 4:  # Пятница
                try:
                    daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                        month=month,
                        day=day
                    )
                    
                    if daily_info.fasting_type == 'no_fast':
                        daily_info.fasting_type = 'light_fast'
                        daily_info.fasting_description = 'Постная пятница'
                        daily_info.allowed_food = '''🥬 <strong>Постная пятница:</strong>

✅ <strong>Разрешается:</strong>
• Растительная пища всех видов
• Каши на воде или с растительным маслом
• Овощи (свежие, тушеные, вареные, жареные)
• Фрукты и ягоды
• Орехи и семечки
• Грибы в любом виде
• Растительное масло
• Хлеб (без молока и яиц)
• Мед, варенье
• Напитки: чай, кофе, соки, компоты

❌ <strong>Не разрешается:</strong>
• Мясо и мясные продукты
• Молоко и молочные продукты (сыр, творог, сметана)
• Яйца
• Рыба и морепродукты
• Продукты, содержащие молоко и яйца'''
                        daily_info.spiritual_note = 'Пятница - день воспоминания крестных страданий Спасителя. День особой молитвы и воздержания.'
                        daily_info.save()
                except Exception as e:
                    print(f"   Ошибка для пятницы {day}.{month}: {e}")

def create_main_orthodox_events():
    """Создание основных православных событий"""
    print("⛪ Создаем основные православные события...")
    
    # Великие праздники
    great_feasts = [
        (1, 7, "Рождество Христово", "Великий праздник Рождества Господа нашего Иисуса Христа"),
        (1, 19, "Крещение Господне (Богоявление)", "Великий праздник Крещения Иисуса Христа в Иордане"),
        (4, 7, "Благовещение Пресвятой Богородицы", "Великий праздник Благовещения"),
        (8, 19, "Преображение Господне", "Великий праздник Преображения Христа на горе Фавор"),
        (8, 28, "Успение Пресвятой Богородицы", "Великий праздник Успения Божией Матери"),
        (9, 21, "Рождество Пресвятой Богородицы", "Великий праздник Рождества Богоматери"),
        (9, 27, "Воздвижение Честного и Животворящего Креста", "Великий праздник Воздвижения Креста"),
        (12, 4, "Введение во храм Пресвятой Богородицы", "Великий праздник Введения во храм"),
    ]
    
    for month, day, title, description in great_feasts:
        event, created = OrthodoxEvent.objects.get_or_create(
            month=month,
            day=day,
            title=title,
            defaults={
                'description': description,
                'event_type': 'great_feast',
                'is_movable': False
            }
        )
        action = "Создано" if created else "Обновлено"
        print(f"   {action} великий праздник: {title}")

def update_feast_days():
    """Обновление дней великих праздников (отменяют пост)"""
    print("🎉 Обновляем дни великих праздников...")
    
    great_feast_days = [
        (1, 7), (1, 19), (4, 7), (8, 19), (8, 28), 
        (9, 21), (9, 27), (12, 4)
    ]
    
    for month, day in great_feast_days:
        try:
            daily_info = DailyOrthodoxInfo.objects.get(month=month, day=day)
            event = OrthodoxEvent.objects.get(month=month, day=day, event_type='great_feast')
            
            daily_info.fasting_type = 'no_fast'
            daily_info.fasting_description = f'Великий праздник: {event.title}'
            daily_info.allowed_food = f'''🎉 <strong>Великий праздник - поста нет!</strong>

В честь праздника {event.title} разрешается любая пища.

🍽️ <strong>Можно употреблять:</strong>
• Все виды мясных блюд
• Молочные продукты (молоко, сыр, творог, сметана)
• Яйца в любом виде
• Рыбу и морепродукты
• Любую другую пищу
• Праздничные сладости
• Вино для праздничного стола

🎊 <strong>Традиция:</strong> Праздничная трапеза в кругу семьи

💒 <strong>Главное:</strong> Празднуйте с радостью, но помните об умеренности'''
            daily_info.spiritual_note = f'🎉 {event.title}! {event.description} Великий день радости для всех православных христиан.'
            daily_info.save()
            print(f"   Обновлен праздник: {event.title}")
            
        except (DailyOrthodoxInfo.DoesNotExist, OrthodoxEvent.DoesNotExist):
            print(f"   Не найден праздник для {day}.{month}")

def add_helpful_notes():
    """Добавление полезных заметок к обычным дням"""
    print("📝 Добавляем полезные духовные заметки...")
    
    # Для воскресных дней
    for month in range(1, 13):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
        if month == 2 and 2025 % 4 == 0:
            days_in_month = 29
            
        for day in range(1, days_in_month + 1):
            target_date = date(2025, month, day)
            weekday = target_date.weekday()
            
            if weekday == 6:  # Воскресенье
                try:
                    daily_info = DailyOrthodoxInfo.objects.get(month=month, day=day)
                    if daily_info.fasting_type == 'no_fast' and not daily_info.spiritual_note:
                        daily_info.spiritual_note = 'Воскресенье - день Воскресения Христова. Время семейной молитвы, посещения храма и духовного общения.'
                        daily_info.allowed_food = '''🍽️ <strong>Воскресенье - обычный день:</strong>

✅ <strong>Разрешается любая пища:</strong>
• Мясные блюда
• Молочные продукты
• Яйца
• Рыба и морепродукты
• Растительная пища
• Все виды хлеба и выпечки
• Сладости (в умеренных количествах)

💡 <strong>Рекомендация:</strong> 
Воскресная трапеза - время семейного общения. Соблюдайте умеренность и благодарите Бога за все дары.

🏠 <strong>Традиция:</strong> Семейный обед после литургии'''
                        daily_info.save()
                except DailyOrthodoxInfo.DoesNotExist:
                    pass

def main():
    """Основная функция запуска"""
    print("🕊️ Запуск обновления православного календаря с достоверной информацией о постах...")
    print("📖 Источники: Типикон, церковный устав, журнал 'Фома', официальные церковные источники")
    print("=" * 70)
    
    try:
        # Создаем основные события
        create_main_orthodox_events()
        
        # Обновляем Успенский пост (сейчас актуален)
        populate_success_fast_info()
        create_success_orthodox_events()
        
        # Обновляем среды и пятницы
        update_wednesdays_fridays()
        
        # Обновляем дни великих праздников
        update_feast_days()
        
        # Добавляем полезные заметки
        add_helpful_notes()
        
        print("\n📊 Статистика после обновления:")
        print(f"   • Всего записей о постах: {DailyOrthodoxInfo.objects.count()}")
        print(f"   • Православных событий: {OrthodoxEvent.objects.count()}")
        print(f"   • Великих праздников: {OrthodoxEvent.objects.filter(event_type='great_feast').count()}")
        print(f"   • Дней без поста: {DailyOrthodoxInfo.objects.filter(fasting_type='no_fast').count()}")
        print(f"   • Постных дней: {DailyOrthodoxInfo.objects.exclude(fasting_type='no_fast').count()}")
        
        # Проверяем Успенский пост
        uspenie_days = DailyOrthodoxInfo.objects.filter(
            month=8, day__gte=14, day__lte=27
        ).exclude(fasting_type='no_fast')
        print(f"   • Дней Успенского поста: {uspenie_days.count()}")
        
        print("\n✅ Православный календарь успешно обновлен!")
        print("🎯 Особое внимание уделено Успенскому посту (14-27 августа)")
        print("📱 Теперь ваши пользователи получат подробную и достоверную информацию о постах")
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении календаря: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
