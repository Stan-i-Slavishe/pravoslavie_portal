import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo
from datetime import date

print("🔍 Проверка православного календаря")
print("=" * 50)

# Проверяем 7 июля
print("📅 Проверяем 7 июля (Рождество Иоанна Предтечи):")
july_7_events = OrthodoxEvent.objects.filter(month=7, day=7)

if july_7_events.exists():
    for event in july_7_events:
        print(f"   ✅ {event.title}")
        print(f"   📖 Тип: {event.get_event_type_display()}")
        print(f"   📝 Описание: {event.description[:100]}...")
else:
    print("   ❌ События на 7 июля не найдены!")
    print("   💡 Запустите fix_july_calendar.bat для исправления")

print()

# Проверяем ежедневную информацию для 7 июля
print("📖 Проверяем ежедневную информацию для 7 июля:")
try:
    daily_info = DailyOrthodoxInfo.objects.get(month=7, day=7)
    print(f"   ✅ Тип поста: {daily_info.get_fasting_type_display()}")
    print(f"   ✅ Описание: {daily_info.fasting_description}")
    print(f"   ✅ Духовная заметка: {daily_info.spiritual_note[:100]}...")
except DailyOrthodoxInfo.DoesNotExist:
    print("   ❌ Ежедневная информация для 7 июля не найдена!")

print()

# Показываем все события июля
print("📊 Все события июля:")
july_events = OrthodoxEvent.objects.filter(month=7).order_by('day')
if july_events.exists():
    for event in july_events:
        print(f"   {event.day:2d} июля - {event.title[:50]}... ({event.get_event_type_display()})")
    print(f"\n📈 Всего событий в июле: {july_events.count()}")
else:
    print("   ❌ События июля не найдены!")

print("\n🔍 Проверка завершена!")
