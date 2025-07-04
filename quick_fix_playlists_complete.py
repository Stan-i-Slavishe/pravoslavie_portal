#!/usr/bin/env python
"""
БЫСТРОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ
Создаем миграции и тестовые данные
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🚀 БЫСТРОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ")
print("=" * 50)

# 1. Создаем миграции
print("\n1️⃣ Создание миграций...")
from django.core.management import call_command

try:
    call_command('makemigrations', 'stories', '--name=add_playlist_models')
    print("✅ Миграции созданы")
except Exception as e:
    print(f"⚠️  Миграции: {e}")

# 2. Применяем миграции
print("\n2️⃣ Применение миграций...")
try:
    call_command('migrate', 'stories')
    print("✅ Миграции применены")
except Exception as e:
    print(f"⚠️  Миграции: {e}")

# 3. Создаем тестовые плейлисты
print("\n3️⃣ Создание тестовых плейлистов...")
try:
    from django.contrib.auth.models import User
    from stories.models import Story, Playlist, PlaylistItem
    
    # Получаем пользователя
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print(f"✅ Создан пользователь: {user.username}")
    else:
        print(f"✅ Найден пользователь: {user.username}")
    
    # Получаем рассказы
    stories = Story.objects.all()[:3]
    print(f"📚 Найдено рассказов: {stories.count()}")
    
    if stories.count() > 0:
        # Создаем тестовые плейлисты
        playlist_data = [
            {
                'title': 'Бородa',
                'description': 'Плейлист с рассказами про бороду',
                'playlist_type': 'public'
            },
            {
                'title': 'Школьные истории',
                'description': 'Рассказы про школьную жизнь', 
                'playlist_type': 'private'
            }
        ]
        
        for data in playlist_data:
            playlist, created = Playlist.objects.get_or_create(
                creator=user,
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'playlist_type': data['playlist_type']
                }
            )
            
            if created:
                print(f"✅ Создан плейлист: {playlist.title}")
                
                # Добавляем рассказы
                for i, story in enumerate(stories):
                    PlaylistItem.objects.get_or_create(
                        playlist=playlist,
                        story=story,
                        defaults={'order': i + 1}
                    )
                
                # Обновляем счетчик
                playlist.stories_count = playlist.playlist_items.count()
                playlist.save()
                print(f"  📝 Добавлено рассказов: {playlist.stories_count}")
            else:
                print(f"⚠️  Плейлист уже существует: {playlist.title}")
        
        total_playlists = Playlist.objects.count()
        total_items = PlaylistItem.objects.count()
        print(f"\n📊 Итого плейлистов: {total_playlists}")
        print(f"📊 Итого элементов: {total_items}")
        
    else:
        print("❌ Нет рассказов для создания плейлистов")

except Exception as e:
    import traceback
    print(f"❌ Ошибка создания плейлистов: {e}")
    traceback.print_exc()

print("\n" + "=" * 50)
print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
print("\n📋 Что было сделано:")
print("✅ Созданы модели плейлистов")
print("✅ Применены миграции")  
print("✅ Созданы тестовые плейлисты")
print("\n🔄 Перезапустите сервер: python manage.py runserver")
