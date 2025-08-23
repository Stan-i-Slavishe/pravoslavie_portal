import os
import sys
import django

print("🔧 Запуск исправления православного календаря...")
print("=" * 50)

try:
    # Настройка Django
    print("⚙️ Настройка Django...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    print("✅ Django настроен")
    
    from pwa.models import OrthodoxEvent, DailyOrthodoxInfo
    print("✅ Модели импортированы")
    
    # Проверяем подключение к БД
    print("\n🔍 Проверка подключения к базе данных...")
    total_events = OrthodoxEvent.objects.count()
    print(f"✅ Подключение успешно. Всего событий в БД: {total_events}")
    
    # Проверяем июльские события
    print(f"\n📅 Текущие события июля:")
    july_events = OrthodoxEvent.objects.filter(month=7).order_by('day')
    if july_events.exists():
        for event in july_events:
            print(f"   {event.day:2d} июля - {event.title[:50]}...")
    else:
        print("   ❌ События июля не найдены")
    
    # Проверяем конкретно 7 июля
    print(f"\n🔍 Проверка 7 июля:")
    july_7 = OrthodoxEvent.objects.filter(month=7, day=7)
    if july_7.exists():
        for event in july_7:
            print(f"   ✅ {event.title}")
            print(f"   📖 Тип: {event.get_event_type_display()}")
    else:
        print("   ❌ События на 7 июля НЕТ - нужно добавить!")
        
        # Добавляем Рождество Иоанна Предтечи
        print("   🎂 Добавляем Рождество Иоанна Предтечи...")
        event = OrthodoxEvent.objects.create(
            title="Рождество честного славного Пророка, Предтечи и Крестителя Господня Иоанна",
            description="Великий праздник в честь рождения св. Иоанна Предтечи",
            event_type="great_feast",
            month=7,
            day=7,
            is_old_style=False,
            is_movable=False
        )
        print(f"   ✅ ДОБАВЛЕНО: {event.title}")
        
        # Добавляем ежедневную информацию
        try:
            DailyOrthodoxInfo.objects.get(month=7, day=7)
            print("   📖 Ежедневная информация уже есть")
        except DailyOrthodoxInfo.DoesNotExist:
            daily_info = DailyOrthodoxInfo.objects.create(
                month=7, day=7,
                fasting_type='no_fast',
                fasting_description='Рождество Иоанна Предтечи (великий праздник)',
                allowed_food='Любая пища (праздничный день)',
                spiritual_note='🎉 Рождество Иоанна Предтечи! Великий праздник.',
                gospel_reading='Лк. 1:1-25, 57-68, 76, 80',
                epistle_reading='Рим. 13:11 - 14:4'
            )
            print("   ✅ Добавлена ежедневная информация")
    
    # Удаляем лишнее 2 июля
    print(f"\n🗑️ Проверка 2 июля:")
    july_2 = OrthodoxEvent.objects.filter(month=7, day=2)
    if july_2.exists():
        print("   🗑️ Найдено событие на 2 июля - удаляем...")
        for event in july_2:
            print(f"      Удаляем: {event.title}")
        deleted_count = july_2.delete()[0]
        print(f"   ✅ Удалено событий: {deleted_count}")
        
        # Удаляем ежедневную информацию
        try:
            daily_2 = DailyOrthodoxInfo.objects.get(month=7, day=2)
            daily_2.delete()
            print("   ✅ Удалена ежедневная информация для 2 июля")
        except DailyOrthodoxInfo.DoesNotExist:
            print("   ℹ️ Ежедневной информации для 2 июля не было")
    else:
        print("   ✅ 2 июля чисто (нет лишних событий)")
    
    print(f"\n🎉 ИТОГ:")
    july_events_final = OrthodoxEvent.objects.filter(month=7).order_by('day')
    print(f"📊 Всего событий в июле: {july_events_final.count()}")
    for event in july_events_final:
        print(f"   {event.day:2d} июля - {event.title[:50]}... ({event.get_event_type_display()})")
    
    print(f"\n✅ Исправление завершено успешно!")
    print(f"🔄 Обновите страницу календаря в браузере")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

print(f"\n📝 Нажмите Enter для завершения...")
input()
