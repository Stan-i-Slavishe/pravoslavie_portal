#!/usr/bin/env python
"""
Модель православного календаря для уведомлений
"""

import os
import sys
import django
from datetime import datetime, date

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import models
from django.utils import timezone

class OrthodoxEvent(models.Model):
    """Православные праздники и события"""
    
    EVENT_TYPES = [
        ('great_feast', 'Великий праздник'),
        ('major_feast', 'Большой праздник'), 
        ('minor_feast', 'Малый праздник'),
        ('fast', 'Пост'),
        ('fast_day', 'Постный день'),
        ('memorial', 'Поминовение'),
        ('saint', 'День святого'),
        ('icon', 'Икона'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Тип события")
    
    # Дата (может быть переменной)
    month = models.IntegerField(verbose_name="Месяц")
    day = models.IntegerField(verbose_name="День")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год (если конкретный)")
    
    # Старый/новый стиль
    is_old_style = models.BooleanField(default=False, verbose_name="По старому стилю")
    
    # Переходящие праздники (Пасха и т.д.)
    is_movable = models.BooleanField(default=False, verbose_name="Переходящий праздник")
    easter_offset = models.IntegerField(null=True, blank=True, verbose_name="Сдвиг от Пасхи (дни)")
    
    # Метаданные
    icon_url = models.URLField(blank=True, verbose_name="Ссылка на икону")
    reading_url = models.URLField(blank=True, verbose_name="Ссылка на чтения")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Православное событие"
        verbose_name_plural = "Православные события"
        ordering = ['month', 'day']
    
    def __str__(self):
        return f"{self.day}.{self.month} - {self.title}"

# Базовые православные праздники
ORTHODOX_EVENTS = [
    # Великие праздники
    {'title': 'Рождество Христово', 'month': 1, 'day': 7, 'event_type': 'great_feast'},
    {'title': 'Крещение Господне', 'month': 1, 'day': 19, 'event_type': 'great_feast'},
    {'title': 'Сретение Господне', 'month': 2, 'day': 15, 'event_type': 'great_feast'},
    {'title': 'Благовещение', 'month': 4, 'day': 7, 'event_type': 'great_feast'},
    {'title': 'Преображение Господне', 'month': 8, 'day': 19, 'event_type': 'great_feast'},
    {'title': 'Успение Пресвятой Богородицы', 'month': 8, 'day': 28, 'event_type': 'great_feast'},
    {'title': 'Рождество Пресвятой Богородицы', 'month': 9, 'day': 21, 'event_type': 'great_feast'},
    {'title': 'Воздвижение Креста Господня', 'month': 9, 'day': 27, 'event_type': 'great_feast'},
    {'title': 'Введение во храм Пресвятой Богородицы', 'month': 12, 'day': 4, 'event_type': 'great_feast'},
    
    # Переходящие праздники (зависят от Пасхи)
    {'title': 'Пасха', 'is_movable': True, 'easter_offset': 0, 'event_type': 'great_feast'},
    {'title': 'Вход Господень в Иерусалим', 'is_movable': True, 'easter_offset': -7, 'event_type': 'great_feast'},
    {'title': 'Вознесение Господне', 'is_movable': True, 'easter_offset': 39, 'event_type': 'great_feast'},
    {'title': 'День Святой Троицы', 'is_movable': True, 'easter_offset': 49, 'event_type': 'great_feast'},
    
    # Посты
    {'title': 'Начало Великого поста', 'is_movable': True, 'easter_offset': -48, 'event_type': 'fast'},
    {'title': 'Петров пост', 'is_movable': True, 'easter_offset': 57, 'event_type': 'fast'},
    {'title': 'Успенский пост', 'month': 8, 'day': 14, 'event_type': 'fast'},
    {'title': 'Рождественский пост', 'month': 11, 'day': 28, 'event_type': 'fast'},
    
    # Популярные святые
    {'title': 'День святителя Николая Чудотворца', 'month': 12, 'day': 19, 'event_type': 'saint'},
    {'title': 'День святой великомученицы Варвары', 'month': 12, 'day': 17, 'event_type': 'saint'},
    {'title': 'День преподобного Сергия Радонежского', 'month': 10, 'day': 8, 'event_type': 'saint'},
    {'title': 'День святых Петра и Февронии', 'month': 7, 'day': 8, 'event_type': 'saint'},
    
    # Постные дни
    {'title': 'Среда (постный день)', 'event_type': 'fast_day'},
    {'title': 'Пятница (постный день)', 'event_type': 'fast_day'},
]

def calculate_easter(year):
    """Вычисление даты Пасхи по православному календарю"""
    # Алгоритм вычисления православной Пасхи
    a = year % 19
    b = year % 4
    c = year % 7
    d = (19 * a + 15) % 30
    e = (2 * b + 4 * c + 6 * d + 6) % 7
    
    if d + e < 10:
        day = d + e + 22
        month = 3
    else:
        day = d + e - 9
        month = 4
    
    # Коррекция для старого стиля (+13 дней)
    easter_date = date(year, month, day)
    # Добавляем 13 дней для перевода в новый стиль
    from datetime import timedelta
    easter_date += timedelta(days=13)
    
    return easter_date

def get_orthodox_events_for_date(target_date):
    """Получить православные события для конкретной даты"""
    events = []
    
    # Фиксированные праздники
    for event_data in ORTHODOX_EVENTS:
        if not event_data.get('is_movable', False):
            if (event_data.get('month') == target_date.month and 
                event_data.get('day') == target_date.day):
                events.append(event_data)
    
    # Переходящие праздники
    easter_date = calculate_easter(target_date.year)
    for event_data in ORTHODOX_EVENTS:
        if event_data.get('is_movable', False):
            offset = event_data.get('easter_offset', 0)
            event_date = easter_date + timedelta(days=offset)
            if event_date == target_date:
                events.append(event_data)
    
    return events

def create_orthodox_calendar():
    """Создание базового православного календаря"""
    print("📅 Создание православного календаря...")
    
    created_count = 0
    
    for event_data in ORTHODOX_EVENTS:
        # Проверяем, не переходящий ли это праздник
        if event_data.get('is_movable', False):
            event, created = OrthodoxEvent.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'event_type': event_data['event_type'],
                    'is_movable': True,
                    'easter_offset': event_data.get('easter_offset', 0),
                    'month': 1,  # Заглушка
                    'day': 1,    # Заглушка
                }
            )
        else:
            event, created = OrthodoxEvent.objects.get_or_create(
                title=event_data['title'],
                month=event_data.get('month', 1),
                day=event_data.get('day', 1),
                defaults={
                    'event_type': event_data['event_type'],
                    'is_movable': False,
                }
            )
        
        if created:
            created_count += 1
            print(f"✅ Создано: {event.title}")
        else:
            print(f"📅 Уже существует: {event.title}")
    
    print(f"\n📊 Результат: создано {created_count} новых событий")
    print(f"📊 Всего в календаре: {OrthodoxEvent.objects.count()} событий")

if __name__ == '__main__':
    print("🚀 Инициализация православного календаря...")
    
    # Тест расчета Пасхи
    print(f"🥚 Пасха 2024: {calculate_easter(2024)}")
    print(f"🥚 Пасха 2025: {calculate_easter(2025)}")
    
    # Тест событий на сегодня
    today = date.today()
    today_events = get_orthodox_events_for_date(today)
    print(f"\n📅 События на {today}: {len(today_events)}")
    for event in today_events:
        print(f"  - {event['title']} ({event['event_type']})")
    
    print("✨ Готово!")
