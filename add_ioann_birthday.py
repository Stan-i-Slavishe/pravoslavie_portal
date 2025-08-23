import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent
from datetime import date

# Проверим, что есть в базе на 7 июля
july_events = OrthodoxEvent.objects.filter(month=7, day=7)
print("События на 7 июля:")
for event in july_events:
    print(f"- {event.title} ({event.get_event_type_display()})")

print(f"\nВсего событий на 7 июля: {july_events.count()}")

# Добавим Рождество Иоанна Предтечи, если его нет
if not july_events.filter(title__icontains="Иоанн").exists():
    print("\nДобавляем Рождество Иоанна Предтечи...")
    
    event = OrthodoxEvent.objects.create(
        title="Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна",
        description="Великий праздник в честь рождения св. Иоанна Предтечи, который был предуготован Богом быть Предтечей Мессии и крестить Христа в водах Иордана.",
        event_type="great_feast",  # Это великий праздник!
        month=7,
        day=7,
        is_old_style=False,
        is_movable=False
    )
    
    print(f"✅ Добавлено: {event.title}")
    print(f"✅ Тип: {event.get_event_type_display()}")
    
    # Проверим еще раз
    july_events = OrthodoxEvent.objects.filter(month=7, day=7)
    print(f"\nТеперь событий на 7 июля: {july_events.count()}")
    for event in july_events:
        print(f"- {event.title} ({event.get_event_type_display()})")

else:
    print("\nРождество Иоанна Предтечи уже существует в базе")

# Также добавим информацию для 7 июля в DailyOrthodoxInfo, если её нет
from pwa.models import DailyOrthodoxInfo

try:
    daily_info = DailyOrthodoxInfo.objects.get(month=7, day=7)
    print(f"\nИнформация для 7 июля уже есть: {daily_info.fasting_description}")
except DailyOrthodoxInfo.DoesNotExist:
    print("\nДобавляем информацию для 7 июля...")
    
    daily_info = DailyOrthodoxInfo.objects.create(
        month=7,
        day=7,
        fasting_type='no_fast',
        fasting_description='Рождество Иоанна Предтечи (великий праздник)',
        allowed_food='Любая пища (праздничный день)',
        spiritual_note='🎉 Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна! Великий праздник в честь рождения святого, который приготовил путь Господу.',
        gospel_reading='Лк. 1:1-25, 57-68, 76, 80',
        epistle_reading='Рим. 13:11 - 14:4'
    )
    
    print(f"✅ Добавлена информация для 7 июля")

print("\n✅ Скрипт выполнен!")
