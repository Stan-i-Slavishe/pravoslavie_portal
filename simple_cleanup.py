# Простой скрипт для очистки дубликатов (без эмодзи)
# python manage.py shell

from pwa.models import OrthodoxEvent
from collections import defaultdict

print("Поиск дубликатов православных событий...")

# Находим все события по дате
events_by_date = defaultdict(list)
for event in OrthodoxEvent.objects.filter(is_movable=False):
    key = f"{event.month:02d}-{event.day:02d}"
    events_by_date[key].append(event)

# Показываем дубликаты
duplicates_found = False
for date_key, events in events_by_date.items():
    if len(events) > 1:
        duplicates_found = True
        print(f"\nДата {date_key} - найдено {len(events)} событий:")
        for i, event in enumerate(events, 1):
            print(f"  {i}. ID:{event.id} - '{event.title}' ({event.event_type})")

if duplicates_found:
    print("\nОчищаем дубликаты...")
    
    # Очищаем дубликаты
    cleaned_count = 0
    for date_key, events in events_by_date.items():
        if len(events) > 1:
            # Сортируем: great_feast первыми, потом по ID
            events.sort(key=lambda x: (0 if x.event_type == 'great_feast' else 1, x.id))
            
            # Оставляем первый, удаляем остальные
            keep_event = events[0]
            remove_events = events[1:]
            
            print(f"Дата {date_key}: оставляем '{keep_event.title}' (ID:{keep_event.id})")
            
            for event in remove_events:
                print(f"  Удаляем: '{event.title}' (ID:{event.id})")
                event.delete()
                cleaned_count += 1
    
    print(f"\nОчистка завершена! Удалено: {cleaned_count}")
else:
    print("Дубликатов не найдено!")

print(f"Всего событий в базе: {OrthodoxEvent.objects.count()}")

# Показываем основные праздники
print("\nОсновные праздники:")
for event in OrthodoxEvent.objects.filter(event_type='great_feast', is_movable=False).order_by('month', 'day'):
    print(f"  {event.day:02d}.{event.month:02d} - {event.title}")
