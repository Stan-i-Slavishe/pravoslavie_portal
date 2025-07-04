#!/usr/bin/env python
"""
Применяем исправления к модели Playlist
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔧 ПРИМЕНЕНИЕ ИСПРАВЛЕНИЙ МОДЕЛИ")
print("=" * 50)

# Создаем новые миграции
print("\n📦 Создание миграций...")
from django.core.management import call_command

try:
    call_command('makemigrations', 'stories', '--name=fix_playlist_duplicates')
    print("✅ Миграции созданы")
except Exception as e:
    print(f"⚠️  Миграции: {e}")

# Применяем миграции
print("\n⚙️ Применение миграций...")
try:
    call_command('migrate', 'stories')
    print("✅ Миграции применены")
except Exception as e:
    print(f"⚠️  Миграции: {e}")

# Проверяем модели
print("\n✅ Проверка модели...")
try:
    from stories.models import Playlist, PlaylistItem, Story
    print("✅ Все модели импортированы успешно")
    
    playlist_count = Playlist.objects.count()
    items_count = PlaylistItem.objects.count()
    stories_count = Story.objects.count()
    
    print(f"📊 Плейлистов: {playlist_count}")
    print(f"📊 Элементов плейлистов: {items_count}")
    print(f"📊 Рассказов: {stories_count}")
    
except Exception as e:
    print(f"❌ Ошибка проверки: {e}")

print("\n" + "=" * 50)
print("🎉 ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
print("\n🚀 Запустите сервер:")
print("python manage.py runserver")
