#!/usr/bin/env python
"""
Заполнение православного календаря и категорий уведомлений
"""

import os
import sys
import django
from datetime import date

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import NotificationCategory, OrthodoxEvent

def create_notification_categories():
    """Создание категорий уведомлений"""
    
    categories_data = [
        {
            'name': 'bedtime_stories',
            'title': 'Сказки на ночь',
            'description': 'Напоминания о чтении сказок перед сном для детей',
            'icon': '🌙',
            'default_enabled': True
        },
        {
            'name': 'orthodox_calendar',
            'title': 'Православный календарь',
            'description': 'Уведомления о православных праздниках, постах и важных датах',
            'icon': '⛪',
            'default_enabled': True
        },
        {
            'name': 'new_content',
            'title': 'Видео-рассказы',
            'description': 'Уведомления о новых духовных рассказах и видео на портале',
            'icon': '🎬',
            'default_enabled': True
        },
        {
            'name': 'fairy_tales',
            'title': 'Терапевтические сказки',
            'description': 'Рекомендации терапевтических сказок для решения детских проблем',
            'icon': '🧚',
            'default_enabled': True
        },
        {
            'name': 'audio_content',
            'title': 'Аудио-контент',
            'description': 'Новые аудио-рассказы, подкасты и аудиокниги',
            'icon': '🎵',
            'default_enabled': False
        },
        {
            'name': 'book_releases',
            'title': 'Новые книги',
            'description': 'Уведомления о поступлении новых книг в магазин',
            'icon': '📖',
            'default_enabled': True
        },
        {
            'name': 'special_events',
            'title': 'Особые события',
            'description': 'Важные события и мероприятия портала',
            'icon': '🎉',
            'default_enabled': False
        },
        {
            'name': 'daily_wisdom',
            'title': 'Мудрость дня',
            'description': 'Ежедневные духовные размышления и цитаты',
            'icon': '💭',
            'default_enabled': False
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for category_data in categories_data:
        category, created = NotificationCategory.objects.get_or_create(
            name=category_data['name'],
            defaults=category_data
        )
        
        if created:
            created_count += 1
            print(f"✅ Создана категория: {category.icon} {category.title}")
        else:
            # Обновляем существующую категорию
            for key, value in category_data.items():
                if key != 'name':
                    setattr(category, key, value)
            category.save()
            updated_count += 1
            print(f"🔄 Обновлена категория: {category.icon} {category.title}")
    
    print(f"\n📊 Результат категорий:")
    print(f"Создано новых: {created_count}")
    print(f"Обновлено: {updated_count}")
    print(f"Всего категорий: {NotificationCategory.objects.count()}")

def create_orthodox_calendar():
    """Создание православного календаря"""
    
    orthodox_events = [
        # Великие праздники (фиксированные)
        {'title': 'Рождество Христово', 'month': 1, 'day': 7, 'event_type': 'great_feast', 
         'description': 'Рождение Иисуса Христа'},
        {'title': 'Крещение Господне (Богоявление)', 'month': 1, 'day': 19, 'event_type': 'great_feast',
         'description': 'Крещение Иисуса Христа в реке Иордан'},
        {'title': 'Сретение Господне', 'month': 2, 'day': 15, 'event_type': 'great_feast',
         'description': 'Принесение Младенца Иисуса в храм'},
        {'title': 'Благовещение Пресвятой Богородицы', 'month': 4, 'day': 7, 'event_type': 'great_feast',
         'description': 'Благовестие Архангела Гавриила Деве Марии'},
        {'title': 'Преображение Господне', 'month': 8, 'day': 19, 'event_type': 'great_feast',
         'description': 'Преображение Иисуса Христа на горе Фавор'},
        {'title': 'Успение Пресвятой Богородицы', 'month': 8, 'day': 28, 'event_type': 'great_feast',
         'description': 'Блаженная кончина Богородицы'},
        {'title': 'Рождество Пресвятой Богородицы', 'month': 9, 'day': 21, 'event_type': 'great_feast',
         'description': 'Рождение Девы Марии'},
        {'title': 'Воздвижение Честного и Животворящего Креста Господня', 'month': 9, 'day': 27, 'event_type': 'great_feast',
         'description': 'Обретение Креста Господня'},
        {'title': 'Введение во храм Пресвятой Богородицы', 'month': 12, 'day': 4, 'event_type': 'great_feast',
         'description': 'Посвящение трехлетней Марии Богу'},
        
        # Переходящие великие праздники
        {'title': 'Пасха - Воскресение Христово', 'is_movable': True, 'easter_offset': 0, 'event_type': 'great_feast',
         'description': 'Воскресение Иисуса Христа', 'month': 4, 'day': 1},
        {'title': 'Вход Господень в Иерусалим (Вербное воскресенье)', 'is_movable': True, 'easter_offset': -7, 'event_type': 'great_feast',
         'description': 'Торжественный вход Христа в Иерусалим', 'month': 4, 'day': 1},
        {'title': 'Вознесение Господне', 'is_movable': True, 'easter_offset': 39, 'event_type': 'great_feast',
         'description': 'Вознесение Христа на небо', 'month': 5, 'day': 1},
        {'title': 'День Святой Троицы (Пятидесятница)', 'is_movable': True, 'easter_offset': 49, 'event_type': 'great_feast',
         'description': 'Сошествие Святого Духа на апостолов', 'month': 6, 'day': 1},
        
        # Посты
        {'title': 'Начало Великого поста', 'is_movable': True, 'easter_offset': -48, 'event_type': 'fast',
         'description': 'Семинедельный пост перед Пасхой', 'month': 3, 'day': 1},
        {'title': 'Петров пост (начало)', 'is_movable': True, 'easter_offset': 57, 'event_type': 'fast',
         'description': 'Пост перед днем святых Петра и Павла', 'month': 6, 'day': 1},
        {'title': 'Успенский пост', 'month': 8, 'day': 14, 'event_type': 'fast',
         'description': 'Двухнедельный пост перед Успением'},
        {'title': 'Рождественский пост (Филиппов пост)', 'month': 11, 'day': 28, 'event_type': 'fast',
         'description': 'Сорокадневный пост перед Рождеством'},
        
        # Популярные святые
        {'title': 'День святителя Николая Чудотворца', 'month': 12, 'day': 19, 'event_type': 'saint',
         'description': 'Один из самых почитаемых святых'},
        {'title': 'День святой великомученицы Варвары', 'month': 12, 'day': 17, 'event_type': 'saint',
         'description': 'Покровительница от внезапной смерти'},
        {'title': 'День преподобного Сергия Радонежского', 'month': 10, 'day': 8, 'event_type': 'saint',
         'description': 'Игумен земли Русской'},
        {'title': 'День святых Петра и Февронии Муромских', 'month': 7, 'day': 8, 'event_type': 'saint',
         'description': 'Покровители семьи и брака'},
        {'title': 'День святых первоверховных апостолов Петра и Павла', 'month': 7, 'day': 12, 'event_type': 'saint',
         'description': 'Главные апостолы Христа'},
        {'title': 'День святой великомученицы Екатерины', 'month': 12, 'day': 7, 'event_type': 'saint',
         'description': 'Покровительница учащихся'},
        {'title': 'День святого великомученика Георгия Победоносца', 'month': 5, 'day': 6, 'event_type': 'saint',
         'description': 'Покровитель воинов'},
        
        # Важные иконы
        {'title': 'День Казанской иконы Божией Матери', 'month': 11, 'day': 4, 'event_type': 'icon',
         'description': 'Одна из самых почитаемых икон'},
        {'title': 'День Владимирской иконы Божией Матери', 'month': 9, 'day': 8, 'event_type': 'icon',
         'description': 'Древняя чудотворная икона'},
        
        # Особые дни
        {'title': 'Крещенский сочельник', 'month': 1, 'day': 18, 'event_type': 'minor_feast',
         'description': 'Канун Крещения'},
        {'title': 'Рождественский сочельник', 'month': 1, 'day': 6, 'event_type': 'minor_feast',
         'description': 'Канун Рождества'},
    ]
    
    created_count = 0
    updated_count = 0
    
    for event_data in orthodox_events:
        # Создаем или обновляем событие
        if event_data.get('is_movable', False):
            event, created = OrthodoxEvent.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
        else:
            event, created = OrthodoxEvent.objects.get_or_create(
                title=event_data['title'],
                month=event_data['month'],
                day=event_data['day'],
                defaults=event_data
            )
        
        if created:
            created_count += 1
            print(f"✅ Создано событие: {event.title}")
        else:
            # Обновляем существующее событие
            for key, value in event_data.items():
                if key not in ['title', 'month', 'day'] or event_data.get('is_movable', False):
                    setattr(event, key, value)
            event.save()
            updated_count += 1
            print(f"🔄 Обновлено событие: {event.title}")
    
    print(f"\n📊 Результат календаря:")
    print(f"Создано новых событий: {created_count}")
    print(f"Обновлено событий: {updated_count}")
    print(f"Всего событий: {OrthodoxEvent.objects.count()}")

def test_calendar():
    """Тестирование календаря"""
    print("\n🧪 Тестирование календаря...")
    
    # Тест расчета Пасхи
    for year in [2024, 2025, 2026]:
        easter = OrthodoxEvent.calculate_easter(year)
        print(f"🥚 Пасха {year}: {easter.strftime('%d.%m.%Y')}")
    
    # События на сегодня
    today = date.today()
    today_events = OrthodoxEvent.get_events_for_date(today)
    print(f"\n📅 События на {today.strftime('%d.%m.%Y')}:")
    if today_events:
        for event in today_events:
            print(f"  🕊️ {event.title} ({event.get_event_type_display()})")
    else:
        print("  📖 Обычный день")
    
    # Тест переходящих праздников на текущий год
    print(f"\n🔄 Переходящие праздники {today.year}:")
    movable_events = OrthodoxEvent.objects.filter(is_movable=True)[:5]
    for event in movable_events:
        event_date = event.get_date_for_year(today.year)
        print(f"  📅 {event.title}: {event_date.strftime('%d.%m.%Y')}")

if __name__ == '__main__':
    print("🚀 Создание системы православного календаря и уведомлений...")
    print("="*60)
    
    # 1. Создаем категории уведомлений
    print("\n🔔 1. Создание категорий уведомлений...")
    create_notification_categories()
    
    # 2. Создаем православный календарь
    print("\n📅 2. Создание православного календаря...")
    create_orthodox_calendar()
    
    # 3. Тестируем
    test_calendar()
    
    print("\n" + "="*60)
    print("✨ Система успешно создана!")
    print("\n📋 Что создано:")
    print(f"🔔 Категории уведомлений: {NotificationCategory.objects.count()}")
    print(f"📅 События календаря: {OrthodoxEvent.objects.count()}")
    print("\n🎯 Следующие шаги:")
    print("1. python manage.py makemigrations pwa")
    print("2. python manage.py migrate") 
    print("3. python manage.py runserver")
    print("4. Проверить админку: /admin/pwa/")
    print("5. Настроить уведомления: /pwa/notifications/settings/")
