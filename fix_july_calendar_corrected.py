import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import OrthodoxEvent, DailyOrthodoxInfo
from datetime import date

print("🕊️ Обновление православного календаря для июля 2025")
print("=" * 60)

# =========================================================================
# ДОБАВЛЯЕМ КЛЮЧЕВЫЕ СОБЫТИЯ ИЮЛЯ (БЕЗ 2 ИЮЛЯ - ОБЫЧНЫЙ ПОСТНЫЙ ДЕНЬ)
# =========================================================================

july_events = [
    {
        'day': 7,
        'title': 'Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна',
        'description': 'Великий праздник в честь рождения св. Иоанна Предтечи, который был предуготован Богом быть Предтечей Мессии и крестить Христа в водах Иордана.',
        'event_type': 'great_feast',
        'gospel': 'Лк. 1:1-25, 57-68, 76, 80',
        'epistle': 'Рим. 13:11 - 14:4',
        'fasting_type': 'no_fast',
        'fasting_desc': 'Рождество Иоанна Предтечи (великий праздник)',
        'spiritual_note': '🎉 Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна! Великий праздник в честь рождения святого, который приготовил путь Господу.'
    },
    {
        'day': 12,
        'title': 'Святых первоверховных апостолов Петра и Павла',
        'description': 'Великий праздник в честь святых апостолов Петра и Павла, столпов Церкви Христовой.',
        'event_type': 'great_feast',
        'gospel': 'Мф. 16:13-19',
        'epistle': '2 Кор. 11:21 - 12:9',
        'fasting_type': 'no_fast',
        'fasting_desc': 'Апостолы Петр и Павел (великий праздник)',
        'spiritual_note': '✝️ Святые первоверховные апостолы Петра и Павла! Великий праздник в честь столпов Церкви, которые понесли веру Христову по всему миру.'
    },
    {
        'day': 8,
        'title': 'Великомученика Прокопия',
        'description': 'День памяти святого великомученика Прокопия Кесарийского.',
        'event_type': 'minor_feast',
        'fasting_type': 'light_fast',  # Проверить день недели
        'fasting_desc': 'Обычный день (проверить календарь постов)',
        'spiritual_note': '⚔️ Святой великомученик Прокопий. Память воина Христова, пострадавшего за веру.'
    },
    {
        'day': 17,
        'title': 'Святой царственной страстотерпицы великой княгини Елисаветы и инокини Варвары',
        'description': 'День памяти святых новомучениц российских.',
        'event_type': 'minor_feast',
        'fasting_type': 'light_fast',
        'fasting_desc': 'Обычный день (проверить календарь постов)', 
        'spiritual_note': '👑 Святые царственные страстотерпицы. Память о новомучениках российских, пострадавших за Христа.'
    },
    {
        'day': 21,
        'title': 'Явление иконы Пресвятой Богородицы во граде Казани',
        'description': 'Великий праздник явления чудотворной Казанской иконы Божией Матери.',
        'event_type': 'great_feast', 
        'gospel': 'Лк. 1:39-49, 56',
        'epistle': 'Флп. 2:5-11',
        'fasting_type': 'no_fast',
        'fasting_desc': 'Казанская икона Божией Матери (великий праздник)',
        'spiritual_note': '🖼️ Явление Казанской иконы Пресвятой Богородицы! Великий праздник чудотворной иконы, заступницы земли Русской.'
    },
    {
        'day': 28,
        'title': 'Равноапостольного великого князя Владимира, во Святом Крещении Василия',
        'description': 'День памяти святого равноапостольного князя Владимира, Крестителя Руси.',
        'event_type': 'major_feast',
        'gospel': 'Ин. 10:9-16',
        'epistle': 'Гал. 5:22 - 6:2',
        'fasting_type': 'no_fast',
        'fasting_desc': 'Равноапостольный князь Владимир (большой праздник)',
        'spiritual_note': '👑 Святой равноапостольный князь Владимир! Память Крестителя Руси, просветившего нашу землю светом Христовым.'
    }
]

# Также удаляем событие 2 июля, если оно было добавлено по ошибке
print("🗑️ Удаляем лишнее событие 2 июля (если существует)...")
july_2_events = OrthodoxEvent.objects.filter(month=7, day=2)
if july_2_events.exists():
    deleted_count = july_2_events.delete()[0]
    print(f"   ✅ Удалено событий: {deleted_count}")
else:
    print("   ℹ️ События на 2 июля не найдены")

# Удаляем ежедневную информацию для 2 июля
try:
    daily_info_2 = DailyOrthodoxInfo.objects.get(month=7, day=2)
    daily_info_2.delete()
    print("   ✅ Удалена ежедневная информация для 2 июля")
except DailyOrthodoxInfo.DoesNotExist:
    print("   ℹ️ Ежедневная информация для 2 июля не найдена")

print()

# Проверяем и добавляем события
added_events = 0
updated_daily_info = 0

for event_data in july_events:
    day = event_data['day']
    
    # Проверяем, есть ли событие в базе
    existing_events = OrthodoxEvent.objects.filter(month=7, day=day, title__icontains=event_data['title'][:20])
    
    if not existing_events.exists():
        print(f"📅 Добавляем событие на {day} июля...")
        
        event = OrthodoxEvent.objects.create(
            title=event_data['title'],
            description=event_data['description'],
            event_type=event_data['event_type'],
            month=7,
            day=day,
            is_old_style=False,
            is_movable=False
        )
        
        print(f"   ✅ {event.title}")
        print(f"   ✨ Тип: {event.get_event_type_display()}")
        added_events += 1
    else:
        print(f"📅 Событие на {day} июля уже существует: {existing_events.first().title[:50]}...")
    
    # Добавляем/обновляем ежедневную информацию только для великих праздников
    if event_data['event_type'] in ['great_feast', 'major_feast']:
        try:
            daily_info = DailyOrthodoxInfo.objects.get(month=7, day=day)
            print(f"   📖 Ежедневная информация уже есть")
        except DailyOrthodoxInfo.DoesNotExist:
            print(f"   📖 Добавляем ежедневную информацию для {day} июля...")
            
            daily_info = DailyOrthodoxInfo.objects.create(
                month=7,
                day=day,
                fasting_type=event_data['fasting_type'],
                fasting_description=event_data['fasting_desc'],
                allowed_food='Любая пища (праздничный день)' if event_data['fasting_type'] == 'no_fast' else 'Растительная пища',
                spiritual_note=event_data['spiritual_note'],
                gospel_reading=event_data.get('gospel', ''),
                epistle_reading=event_data.get('epistle', '')
            )
            
            print(f"   ✅ Добавлена ежедневная информация")
            updated_daily_info += 1

print("\n" + "=" * 60)
print(f"🎉 ЗАВЕРШЕНО!")
print(f"📅 Добавлено новых событий: {added_events}")
print(f"📖 Добавлено ежедневной информации: {updated_daily_info}")

# Проверяем все события июля
print(f"\n📊 Все события июля в базе данных:")
july_events_db = OrthodoxEvent.objects.filter(month=7).order_by('day')
for event in july_events_db:
    print(f"   {event.day:2d} июля - {event.title[:60]}... ({event.get_event_type_display()})")

print(f"\n📊 Всего событий в июле: {july_events_db.count()}")
print("\n✅ Обновление православного календаря завершено!")
print("🔄 Перезагрузите страницу календаря, чтобы увидеть изменения.")
print("ℹ️  2 июля остается обычным постным днем (среда) без особых событий.")
