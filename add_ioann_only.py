import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo

print("🎂 Добавление Рождества Иоанна Предтечи (7 июля)")
print("=" * 55)

# Проверяем, есть ли уже событие на 7 июля
existing_events = OrthodoxEvent.objects.filter(month=7, day=7, title__icontains="Иоанн")

if existing_events.exists():
    print("✅ Рождество Иоанна Предтечи уже есть в календаре:")
    for event in existing_events:
        print(f"   📅 {event.title}")
        print(f"   ✨ Тип: {event.get_event_type_display()}")
else:
    print("📅 Добавляем Рождество Иоанна Предтечи...")
    
    # Добавляем событие
    event = OrthodoxEvent.objects.create(
        title="Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна",
        description="Великий праздник в честь рождения св. Иоанна Предтечи, который был предуготован Богом быть Предтечей Мессии и крестить Христа в водах Иордана.",
        event_type="great_feast",
        month=7,
        day=7,
        is_old_style=False,
        is_movable=False
    )
    
    print(f"✅ Добавлено: {event.title}")
    print(f"✨ Тип: {event.get_event_type_display()}")

# Проверяем ежедневную информацию для 7 июля
try:
    daily_info = DailyOrthodoxInfo.objects.get(month=7, day=7)
    print(f"\n📖 Ежедневная информация для 7 июля уже есть:")
    print(f"   🍽️ Пост: {daily_info.get_fasting_type_display()}")
    print(f"   📝 Описание: {daily_info.fasting_description}")
except DailyOrthodoxInfo.DoesNotExist:
    print(f"\n📖 Добавляем ежедневную информацию для 7 июля...")
    
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
    
    print(f"✅ Добавлена ежедневная информация для 7 июля")

print("\n🎉 Готово! 7 июля теперь должно отображаться в календаре")
print("🔄 Перезагрузите страницу календаря, чтобы увидеть Рождество Иоанна Предтечи")
