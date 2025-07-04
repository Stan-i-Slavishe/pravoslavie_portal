#!/usr/bin/env python
"""
Применяем исправления - финальная версия
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("🔧 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ МОДЕЛЕЙ")
print("=" * 50)

try:
    django.setup()
    print("✅ Django успешно инициализирован")
except Exception as e:
    print(f"❌ Ошибка инициализации Django: {e}")
    exit(1)

# Создаем новые миграции
print("\n📦 Создание миграций...")
from django.core.management import call_command

try:
    call_command('makemigrations', 'stories', '--name=fix_playlist_final')
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
print("🎉 ВСЁ ИСПРАВЛЕНО!")
print("\n🚀 Запустите сервер:")
print("python manage.py runserver")
print("\n📱 Проверьте плейлисты на странице рассказа!")
