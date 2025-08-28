# Очистка дубликатов православных событий
# Запустите: python manage.py shell

from pwa.models import OrthodoxEvent
from collections import defaultdict

print("🧹 Очистка дубликатов православных событий...")

# Функция для очистки дубликатов
def clean_duplicates():
    events_by_date = defaultdict(list)
    
    # Группируем по дате
    for event in OrthodoxEvent.objects.filter(is_movable=False):
        key = f"{event.month:02d}-{event.day:02d}"
        events_by_date[key].append(event)
    
    cleaned_count = 0
    
    # Обрабатываем каждую дату
    for date_key, events in events_by_date.items():
        if len(events) > 1:
            print(f"\n📅 {date_key} - найдено {len(events)} дубликатов")
            
            # Сортируем: сначала великие праздники, потом по ID (старые первыми)
            events.sort(key=lambda x: (
                0 if x.event_type == 'great_feast' else 1,
                0 if x.event_type == 'major_feast' else 2,
                x.id  # Старые записи имеют меньший ID
            ))
            
            # Оставляем первый (лучший), удаляем остальные
            keep_event = events[0]
            remove_events = events[1:]
            
            print(f"   ✅ Оставляем: '{keep_event.title}' (ID:{keep_event.id}, {keep_event.event_type})")
            
            for event in remove_events:
                print(f"   ❌ Удаляем: '{event.title}' (ID:{event.id}, {event.event_type})")
                event.delete()
                cleaned_count += 1
    
    return cleaned_count

# Выполняем очистку
try:
    removed = clean_duplicates()
    print(f"\n🎉 Очистка завершена! Удалено дубликатов: {removed}")
    print(f"📊 Осталось событий: {OrthodoxEvent.objects.count()}")
    
    # Проверяем результат
    print("\n📋 Основные праздники:")
    for event in OrthodoxEvent.objects.filter(event_type='great_feast', is_movable=False).order_by('month', 'day'):
        print(f"   {event.day:02d}.{event.month:02d} - {event.title}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n🔄 Теперь обновите страницу календаря!")
