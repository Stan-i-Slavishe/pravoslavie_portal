#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent

def fix_blagoveshenie():
    print("Исправление Благовещения...")
    
    # Находим все Благовещения
    blagoveshenie_events = OrthodoxEvent.objects.filter(
        title__icontains='Благовещение'
    )
    
    print(f"Найдено событий с 'Благовещение': {blagoveshenie_events.count()}")
    
    for event in blagoveshenie_events:
        print(f"  ID:{event.id} - {event.day:02d}.{event.month:02d} - '{event.title}' ({event.event_type})")
    
    # Удаляем неправильное Благовещение (7 апреля)
    wrong_blagoveshenie = OrthodoxEvent.objects.filter(
        month=4,  # апрель
        day=7,
        title__icontains='Благовещение'
    )
    
    if wrong_blagoveshenie.exists():
        print(f"\nУдаляем неправильное Благовещение 7 апреля...")
        for event in wrong_blagoveshenie:
            print(f"  Удаляем: ID:{event.id} - {event.day:02d}.{event.month:02d} - '{event.title}'")
            event.delete()
    
    # Проверяем правильное Благовещение (25 марта)
    correct_blagoveshenie = OrthodoxEvent.objects.filter(
        month=3,  # март
        day=25,
        title__icontains='Благовещение'
    )
    
    if correct_blagoveshenie.exists():
        print(f"\n✅ Правильное Благовещение 25 марта существует:")
        for event in correct_blagoveshenie:
            print(f"  ID:{event.id} - {event.day:02d}.{event.month:02d} - '{event.title}' ({event.event_type})")
    else:
        print(f"\n❌ Правильного Благовещения 25 марта НЕТ! Создаем...")
        OrthodoxEvent.objects.create(
            month=3,
            day=25,
            title='Благовещение Пресвятой Богородицы',
            description='Благая весть архангела Гавриила Деве Марии',
            event_type='great_feast',
            is_movable=False
        )
        print("  ✅ Создано правильное Благовещение 25 марта")
    
    print(f"\n📊 Итого событий в базе: {OrthodoxEvent.objects.count()}")
    
    # Показываем все великие праздники
    print("\n🎉 Великие праздники:")
    for event in OrthodoxEvent.objects.filter(event_type='great_feast', is_movable=False).order_by('month', 'day'):
        print(f"  {event.day:02d}.{event.month:02d} - {event.title}")

if __name__ == "__main__":
    fix_blagoveshenie()
