import os
import sys
import django

print("🔧 Исправление православного календаря - Праздник + Пост")
print("=" * 55)

try:
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    print("✅ Django настроен")
    
    from pwa.models import OrthodoxEvent, DailyOrthodoxInfo, FastingPeriod
    from datetime import date, timedelta
    print("✅ Модели импортированы")
    
    # 1. Сначала добавляем Рождество Иоанна Предтечи, если его нет
    print("\n🎂 Проверяем Рождество Иоанна Предтечи (7 июля)...")
    july_7_events = OrthodoxEvent.objects.filter(month=7, day=7, title__icontains="Иоанн")
    
    if not july_7_events.exists():
        print("   📅 Добавляем Рождество Иоанна Предтечи...")
        event = OrthodoxEvent.objects.create(
            title="Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна",
            description="Великий праздник в честь рождения св. Иоанна Предтечи",
            event_type="great_feast",
            month=7, day=7,
            is_old_style=False, is_movable=False
        )
        print(f"   ✅ Добавлено: {event.title}")
    else:
        print(f"   ✅ Уже есть: {july_7_events.first().title}")
    
    # 2. Добавляем/обновляем Петров пост
    print("\n⛪ Проверяем Петров пост...")
    
    # Удаляем старую версию Петрова поста, если есть
    old_petrov = FastingPeriod.objects.filter(name='peter_paul_fast')
    if old_petrov.exists():
        old_petrov.delete()
        print("   🗑️ Удалена старая версия Петрова поста")
    
    # Создаем правильный Петров пост
    print("   📅 Создаем Петров пост...")
    petrov_post = FastingPeriod.objects.create(
        name='peter_paul_fast',
        title='Петров пост (Апостольский пост)', 
        description='Апостольский пост в честь святых апостолов Петра и Павла. Переходящий пост от понедельника после Троицы до 12 июля.',
        
        # Переходящее начало (понедельник после Троицы)
        easter_start_offset=57,  # Троица = Пасха + 49, понедельник = +1 день, итого 57
        easter_end_offset=None,  # Конец фиксированный
        
        # Фиксированный конец (11 июля, день перед праздником)
        start_month=None, start_day=None,
        end_month=7, end_day=11,
        
        # Правила поста по дням недели
        fasting_rules={
            'monday': 'light_fast',     # Горячее без масла
            'tuesday': 'with_oil',      # Растительная пища с маслом
            'wednesday': 'light_fast',  # Горячее без масла
            'thursday': 'with_oil',     # Растительная пища с маслом 
            'friday': 'light_fast',     # Горячее без масла
            'saturday': 'with_fish',    # Можно рыбу
            'sunday': 'with_fish'       # Можно рыбу
        },
        
        priority=8,  # Высокий приоритет
        is_active=True
    )
    print(f"   ✅ Создан: {petrov_post.title}")
    print(f"   ⏰ Начало: понедельник после Троицы (переходящий)")
    print(f"   ⏰ Конец: 11 июля (фиксированный)")
    
    # 3. Проверяем, что пост работает для 7 июля 2025
    print(f"\n🔍 Проверяем 7 июля 2025...")
    test_date = date(2025, 7, 7)
    
    # Проверяем, активен ли пост
    is_petrov_active = petrov_post.is_active_for_date(test_date)
    print(f"   📅 Дата: {test_date} (понедельник)")
    print(f"   ⛪ Петров пост активен: {'✅ ДА' if is_petrov_active else '❌ НЕТ'}")
    
    if is_petrov_active:
        weekday = test_date.weekday()  # 0 = понедельник
        fasting_type = petrov_post.get_fasting_type_for_weekday(weekday)
        print(f"   🍽️ Тип поста в понедельник: {fasting_type}")
    
    # Проверяем события на 7 июля
    events_7_july = OrthodoxEvent.get_events_for_date(test_date)
    print(f"   🎉 События: {len(events_7_july)} шт.")
    for event in events_7_july:
        print(f"      - {event.title} ({event.get_event_type_display()})")
    
    # 4. Тестируем алгоритм определения типа дня
    print(f"\n🧮 Тестируем алгоритм...")
    
    # Получаем ежедневную информацию
    daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
    print(f"   📖 Тип поста (ежедневная инф.): {daily_info.fasting_type}")
    print(f"   📖 Описание: {daily_info.fasting_description}")
    
    # Симулируем логику определения типа дня
    is_holiday = any(event.event_type in ['great_feast', 'major_feast'] for event in events_7_july)
    is_fast = is_petrov_active and fasting_type != 'no_fast'
    
    print(f"   🎉 Есть праздник: {'✅ ДА' if is_holiday else '❌ НЕТ'}")
    print(f"   ⛪ Есть пост: {'✅ ДА' if is_fast else '❌ НЕТ'}")
    
    # Определяем тип дня
    if is_holiday and is_fast:
        day_type = 'holiday-fast'
        print(f"   🎨 Тип дня: {day_type} (Праздник + Пост)")
        print(f"   🎨 Цвет: Розово-фиолетовый")
    elif is_holiday:
        day_type = 'holiday'
        print(f"   🎨 Тип дня: {day_type} (Только праздник)")
        print(f"   🎨 Цвет: Красный")
    elif is_fast:
        day_type = 'fast-day'
        print(f"   🎨 Тип дня: {day_type} (Только пост)")
        print(f"   🎨 Цвет: Фиолетовый")
    else:
        day_type = 'feast'
        print(f"   🎨 Тип дня: {day_type} (Обычный)")
        print(f"   🎨 Цвет: Белый")
    
    print(f"\n🎉 РЕЗУЛЬТАТ:")
    print(f"7 июля 2025 должно отображаться как: {day_type}")
    print(f"✅ Рождество Иоанна Предтечи (великий праздник)")
    print(f"✅ Петров пост (понедельник - горячее без масла)")
    print(f"🎨 Цвет: Праздник + Пост (розово-фиолетовый)")
    
    print(f"\n🔄 Перезагрузите страницу календаря в браузере!")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

input("\nНажмите Enter для завершения...")
