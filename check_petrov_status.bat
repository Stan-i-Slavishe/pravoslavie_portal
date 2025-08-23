@echo off
chcp 65001 >nul
echo ========================================
echo 🔍 ПРОВЕРКА СТАТУСА ПЕТРОВА ПОСТА
echo ========================================
echo.

cd /d E:\pravoslavie_portal

echo 📊 Проверяем базу данных...
python -c "
import os, sys, django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from pwa.models import FastingPeriod, OrthodoxEvent, DailyOrthodoxInfo
    from datetime import date
    
    # Проверяем FastingPeriod
    print('📦 Таблица FastingPeriod:')
    count = FastingPeriod.objects.count()
    print(f'   Всего записей: {count}')
    
    # Ищем Петров пост
    petrov = FastingPeriod.objects.filter(name='peter_paul_fast').first()
    if petrov:
        print(f'✅ Петров пост найден: {petrov.title}')
        print(f'   Активен: {petrov.is_active}')
        print(f'   Приоритет: {petrov.priority}')
        print(f'   Easter offset: {petrov.easter_start_offset}')
        print(f'   Конец: {petrov.end_month}/{petrov.end_day}')
    else:
        print('❌ Петров пост НЕ найден!')
    
    print()
    print('📋 Все периоды постов:')
    for period in FastingPeriod.objects.all():
        status = '✅' if period.is_active else '❌'
        print(f'   {status} {period.name}: {period.title}')
    
    print()
    print('🧪 Тестирование июня 2026:')
    
    # Пасха и Троица
    easter = OrthodoxEvent.calculate_easter(2026)
    print(f'   🥚 Пасха 2026: {easter.strftime(\"%d.%m.%Y\")}')
    
    trinity = easter + date.resolution * 49
    print(f'   🕊️ Троица 2026: {trinity.strftime(\"%d.%m.%Y\")}')
    
    # Тестируем конкретные дни
    test_dates = [
        (date(2026, 6, 1), '1 июня (должна быть Троицкая седмица)'),
        (date(2026, 6, 8), '8 июня (должен начаться Петров пост)'),
        (date(2026, 6, 15), '15 июня (Петров пост)'),
        (date(2026, 6, 30), '30 июня (Петров пост)'),
        (date(2026, 7, 12), '12 июля (конец Петрова поста)'),
    ]
    
    for test_date, description in test_dates:
        try:
            daily_info = DailyOrthodoxInfo.get_info_for_date(test_date)
            active_periods = DailyOrthodoxInfo.get_active_fasting_periods(test_date)
            
            weekday = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс'][test_date.weekday()]
            print(f'   📅 {description} ({weekday}):')
            print(f'      Пост: {daily_info.get_fasting_type_display()}')
            print(f'      Описание: {daily_info.fasting_description}')
            if active_periods:
                periods_names = [p.title for p in active_periods]
                print(f'      Активные периоды: {periods_names}')
            print()
        except Exception as e:
            print(f'      ❌ Ошибка: {e}')
            
except Exception as e:
    print(f'❌ Критическая ошибка: {e}')
    import traceback
    traceback.print_exc()
"

echo.
echo ========================================
echo 📋 ИНСТРУКЦИИ:
echo ========================================
echo.
echo Если Петров пост НЕ найден:
echo   1. Запустите: fix_petrov_fast.bat
echo.  
echo Если найден, но календарь не обновился:
echo   1. Перезапустите сервер (Ctrl+C, затем python manage.py runserver)
echo   2. Очистите кеш браузера (Ctrl+F5)
echo   3. Проверьте http://127.0.0.1:8000/pwa/daily-calendar/
echo.
pause
