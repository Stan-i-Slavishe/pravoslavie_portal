import os
import re

print("🔧 Очистка URL и Views от православного календаря")
print("=" * 50)

# Путь к файлам
urls_path = r'E:\pravoslavie_portal\pwa\urls.py'
views_path = r'E:\pravoslavie_portal\pwa\views.py'

# 1. Очищаем URLs
print("\n📂 Очистка URLs...")
try:
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"   📄 Исходный размер файла: {len(content)} символов")
    
    # Удаляем строки с православным календарем
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        # Пропускаем строки с календарем
        if any(keyword in line.lower() for keyword in [
            'orthodox-calendar', 'daily-calendar', 'orthodox_calendar', 
            'daily_orthodox', 'orthodox_events', 'calendar-month'
        ]):
            print(f"   🗑️ Удаляем: {line.strip()}")
            continue
        clean_lines.append(line)
    
    # Записываем очищенный файл
    clean_content = '\n'.join(clean_lines)
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"   ✅ URLs очищен. Новый размер: {len(clean_content)} символов")
    
except Exception as e:
    print(f"   ❌ Ошибка при очистке URLs: {e}")

# 2. Очищаем Views
print(f"\n🔍 Очистка Views...")
try:
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"   📄 Исходный размер файла: {len(content)} символов")
    
    # Удаляем функции views для календаря
    # Ищем функции по паттерну
    patterns_to_remove = [
        r'@require_http_methods.*?def orthodox_calendar.*?(?=@|\Z)',
        r'@require_http_methods.*?def daily_orthodox.*?(?=@|\Z)',
        r'def orthodox_calendar.*?(?=@|\ndef |\Z)',
        r'def daily_orthodox.*?(?=@|\ndef |\Z)',
        r'def get_day_type_for_calendar.*?(?=@|\ndef |\Z)',
        r'def orthodoxy_calendar.*?(?=@|\ndef |\Z)',
    ]
    
    for pattern in patterns_to_remove:
        matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
        for match in matches:
            if len(match.strip()) > 10:  # Проверяем, что это не пустая строка
                print(f"   🗑️ Удаляем функцию: {match.split('def ')[1].split('(')[0] if 'def ' in match else 'неизвестную'}")
                content = content.replace(match, '')
    
    # Удаляем импорты связанные с календарем
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        # Удаляем импорты календарных моделей из строки импорта
        if 'OrthodoxEvent' in line or 'DailyOrthodoxInfo' in line or 'FastingPeriod' in line:
            # Убираем только упоминания этих моделей, оставляя остальные
            line = re.sub(r',?\s*OrthodoxEvent', '', line)
            line = re.sub(r',?\s*DailyOrthodoxInfo', '', line)  
            line = re.sub(r',?\s*FastingPeriod', '', line)
            line = re.sub(r'OrthodoxEvent,?\s*', '', line)
            line = re.sub(r'DailyOrthodoxInfo,?\s*', '', line)
            line = re.sub(r'FastingPeriod,?\s*', '', line)
            # Очищаем лишние запятые
            line = re.sub(r',\s*,', ',', line)
            line = re.sub(r'\(\s*,', '(', line)
            line = re.sub(r',\s*\)', ')', line)
            
        clean_lines.append(line)
    
    # Записываем очищенный файл
    clean_content = '\n'.join(clean_lines)
    
    # Удаляем лишние пустые строки
    clean_content = re.sub(r'\n\n\n+', '\n\n', clean_content)
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"   ✅ Views очищен. Новый размер: {len(clean_content)} символов")
    
except Exception as e:
    print(f"   ❌ Ошибка при очистке Views: {e}")

print(f"\n🎉 Очистка кода завершена!")
print(f"📋 Что осталось сделать вручную:")
print(f"   1. Удалить шаблоны из templates/pwa/")
print(f"   2. Удалить модели из pwa/models.py")
print(f"   3. Создать и применить миграции")
print(f"   4. Убрать ссылки из навигационного меню")
