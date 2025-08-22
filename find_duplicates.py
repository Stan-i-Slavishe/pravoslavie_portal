# Поиск и очистка дубликатов православных событий
# Запустите: python manage.py shell

from pwa.models import OrthodoxEvent
from collections import defaultdict

print("🔍 Поиск дубликатов в православных событиях...")

# Группируем события по дате
events_by_date = defaultdict(list)
for event in OrthodoxEvent.objects.all():
    if not event.is_movable:  # Только фиксированные даты
        key = f"{event.month:02d}-{event.day:02d}"
        events_by_date[key].append(event)

# Ищем дубликаты
duplicates_found = False
for date_key, events in events_by_date.items():
    if len(events) > 1:
        duplicates_found = True
        print(f"\n📅 {date_key} - найдено {len(events)} событий:")
        for i, event in enumerate(events, 1):
            print(f"   {i}. ID:{event.id} - '{event.title}' ({event.event_type})")
            print(f"      Описание: {event.description}")

if not duplicates_found:
    print("✅ Дубликатов не найдено!")
else:
    print("\n🧹 Для очистки дубликатов выполните:")
    print("   1. Выберите, какие события оставить")
    print("   2. Удалите лишние через Django Admin или код")

print("\n📊 Всего событий в базе:", OrthodoxEvent.objects.count())
print("📊 Фиксированных событий:", OrthodoxEvent.objects.filter(is_movable=False).count())
print("📊 Переходящих событий:", OrthodoxEvent.objects.filter(is_movable=True).count())
