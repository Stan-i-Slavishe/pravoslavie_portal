#!/usr/bin/env python3
import os
import sys
import django

# Настройка Django окружения
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация Django
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

print("🔍 ПРОВЕРКА БАЗЫ ДАННЫХ И МИГРАЦИЙ")
print("=" * 50)

# Проверяем, какие таблицы есть в базе
print("📊 Таблицы в базе данных:")
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   • {table[0]}")

# Проверяем статус миграций
print(f"\n📋 Статус миграций для приложения 'core':")
try:
    # Импортируем нужные классы
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections
    
    connection = connections['default']
    executor = MigrationExecutor(connection)
    
    # Получаем план миграций
    plan = executor.migration_plan([('core', None)])
    
    if plan:
        print("   ❌ Есть неприменённые миграции:")
        for migration, backwards in plan:
            print(f"      • {migration}")
        
        print(f"\n🔧 Применяем миграции...")
        execute_from_command_line(['manage.py', 'migrate', 'core'])
        
    else:
        print("   ✅ Все миграции применены")
        
except Exception as e:
    print(f"   ❌ Ошибка проверки миграций: {e}")
    print(f"\n🔧 Пытаемся применить все миграции...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("   ✅ Миграции применены")
    except Exception as e2:
        print(f"   ❌ Ошибка применения миграций: {e2}")

# Пытаемся создать тег
print(f"\n🏷️ Создание тестового тега...")
try:
    from core.models import Tag
    
    # Проверяем, есть ли уже теги
    existing_tags = Tag.objects.all()
    print(f"   📊 Существующих тегов: {existing_tags.count()}")
    
    # Создаем тег "дочь"
    tag, created = Tag.objects.get_or_create(
        slug='doch',
        defaults={
            'name': 'дочь',
            'description': 'Материалы о воспитании дочерей',
            'color': '#FF6B9D',
            'is_active': True
        }
    )
    
    if created:
        print(f"   ✅ Создан тег: {tag.name} (slug: {tag.slug})")
    else:
        print(f"   ⚠️ Тег уже существует: {tag.name} (slug: {tag.slug})")
    
    # Создаем еще несколько тегов
    other_tags = [
        {'name': 'вера', 'slug': 'vera', 'color': '#9C27B0'},
        {'name': 'семья', 'slug': 'semya', 'color': '#4CAF50'},
        {'name': 'любовь', 'slug': 'lyubov', 'color': '#E91E63'},
    ]
    
    for tag_data in other_tags:
        tag, created = Tag.objects.get_or_create(
            slug=tag_data['slug'],
            defaults={
                'name': tag_data['name'],
                'description': f'Материалы о {tag_data["name"]}',
                'color': tag_data['color'],
                'is_active': True
            }
        )
        if created:
            print(f"   ✅ Создан тег: {tag.name} (slug: {tag.slug})")
    
    # Итоговая статистика
    print(f"\n📋 Все теги в базе:")
    all_tags = Tag.objects.all()
    for tag in all_tags:
        print(f"   • {tag.name} (slug: {tag.slug})")
    
    print(f"\n🎉 Всего тегов: {all_tags.count()}")
    
except Exception as e:
    print(f"   ❌ Ошибка работы с тегами: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "=" * 50)
print("🧪 Теперь проверьте:")
print("   http://127.0.0.1:8000/tag/doch/")
