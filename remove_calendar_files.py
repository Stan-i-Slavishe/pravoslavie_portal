import os
import shutil
from pathlib import Path

print("🗑️ Удаление файлов православного календаря")
print("=" * 45)

# Путь к проекту
project_root = Path(r'E:\pravoslavie_portal')

# Файлы для удаления
files_to_remove = [
    # Шаблоны
    'templates/pwa/orthodox_calendar.html',
    'templates/pwa/orthodox_calendar_under_construction.html', 
    'templates/pwa/daily_orthodox_calendar.html',
    'templates/pwa/daily_orthodox_calendar_under_construction.html',
    
    # Скрипты календаря
    'fix_july_remove_2nd.py',
    'fix_july_calendar.py',
    'fix_july_calendar_corrected.py',
    'fix_petrov_fast_july7.py',
    'fix_july_debug.py',
    'add_ioann_birthday.py',
    'add_ioann_only.py',
    'check_july_calendar.py',
    'orthodox_calendar.py',
    'orthodox_calendar_data.json',
    'orthodox_calendar_service.py',
    'orthodox_calendar_tasks.py',
    'populate_orthodox_calendar_detailed.py',
    'create_daily_orthodox_calendar.py',
    'create_orthodox_system.py',
    'quick_calendar_setup.py',
    'setup_calendar_data.py',
    
    # Батч файлы
    'fix_july_remove_2nd.bat',
    'fix_july_calendar.bat',
    'fix_july_calendar_corrected.bat', 
    'fix_petrov_fast_july7.bat',
    'fix_july_debug.bat',
    'add_ioann_birthday.bat',
    'check_july_calendar.bat',
    'setup_eternal_calendar.bat',
    'update_calendar_complete.bat',
    
    # Документация
    'ORTHODOX_CALENDAR_GUIDE.md',
    'ORTHODOX_CALENDAR_INTEGRATION_GUIDE.md',
    'ORTHODOX_CALENDAR_STATUS.md',
]

removed_count = 0
not_found_count = 0

for file_path in files_to_remove:
    full_path = project_root / file_path
    
    if full_path.exists():
        try:
            if full_path.is_file():
                full_path.unlink()
                print(f"   ✅ Удален файл: {file_path}")
                removed_count += 1
            elif full_path.is_dir():
                shutil.rmtree(full_path)
                print(f"   ✅ Удалена папка: {file_path}")
                removed_count += 1
        except Exception as e:
            print(f"   ❌ Ошибка удаления {file_path}: {e}")
    else:
        print(f"   ℹ️ Не найден: {file_path}")
        not_found_count += 1

print(f"\n📊 Статистика:")
print(f"   ✅ Удалено файлов: {removed_count}")
print(f"   ℹ️ Не найдено: {not_found_count}")

# Ищем и удаляем другие связанные файлы
print(f"\n🔍 Поиск дополнительных файлов...")

patterns = ['*orthodox*', '*calendar*', '*petrov*', '*july*']
additional_files = []

for pattern in patterns:
    for file in project_root.glob(pattern):
        if file.is_file() and file.name.endswith(('.py', '.bat', '.md', '.json', '.html')):
            # Исключаем системные файлы
            if not any(exclude in str(file) for exclude in [
                'venv', '__pycache__', '.git', 'node_modules',
                'staticfiles', 'media', 'logs'
            ]):
                additional_files.append(file)

if additional_files:
    print(f"   📂 Найдены дополнительные файлы:")
    for file in additional_files[:10]:  # Показываем первые 10
        file_size = file.stat().st_size if file.exists() else 0
        print(f"      - {file.relative_to(project_root)} ({file_size} bytes)")
    
    if len(additional_files) > 10:
        print(f"      ... и еще {len(additional_files) - 10} файлов")
    
    # Не удаляем автоматически, т.к. могут быть важные файлы
    print(f"   ⚠️  Проверьте эти файлы вручную перед удалением")

print(f"\n🎉 Удаление файлов завершено!")
print(f"📋 Остается сделать:")
print(f"   1. Очистить модели в pwa/models.py")
print(f"   2. Создать миграцию: python manage.py makemigrations")
print(f"   3. Применить миграцию: python manage.py migrate")
print(f"   4. Убрать ссылки календаря из меню")
