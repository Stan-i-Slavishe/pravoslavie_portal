#!/usr/bin/env python
"""
Скрипт для создания тестовых плейлистов
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Story, Playlist, PlaylistItem

print("🎵 Создание тестовых плейлистов...")

try:
    # Получаем пользователя admin
    try:
        user = User.objects.get(username='admin')
        print(f"✅ Найден пользователь: {user.username}")
    except User.DoesNotExist:
        # Создаем пользователя admin
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print(f"✅ Создан пользователь: {user.username}")
    
    # Получаем рассказы
    stories = Story.objects.filter(is_published=True)[:5]
    print(f"✅ Найдено рассказов: {stories.count()}")
    
    if stories.count() < 2:
        print("❌ Недостаточно рассказов для создания плейлистов")
        print("Создайте сначала несколько рассказов")
        exit(1)
    
    # Создаем тестовые плейлисты
    playlists_data = [
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
    
    for playlist_data in playlists_data:
        # Проверяем, существует ли плейлист
        existing = Playlist.objects.filter(
            creator=user,
            title=playlist_data['title']
        ).first()
        
        if existing:
            print(f"⚠️  Плейлист '{playlist_data['title']}' уже существует")
            playlist = existing
        else:
            # Создаем плейлист
            playlist = Playlist.objects.create(
                creator=user,
                title=playlist_data['title'],
                description=playlist_data['description'],
                playlist_type=playlist_data['playlist_type']
            )
            print(f"✅ Создан плейлист: {playlist.title}")
        
        # Добавляем рассказы в плейлист
        for i, story in enumerate(stories[:3]):
            playlist_item, created = PlaylistItem.objects.get_or_create(
                playlist=playlist,
                story=story,
                defaults={'order': i + 1}
            )
            if created:
                print(f"  ➕ Добавлен рассказ: {story.title}")
            else:
                print(f"  ⚠️  Рассказ уже в плейлисте: {story.title}")
        
        # Обновляем счетчик
        playlist.stories_count = playlist.playlist_items.count()
        playlist.save()
    
    print(f"\n🎉 Тестовые плейлисты созданы успешно!")
    print(f"📊 Всего плейлистов: {Playlist.objects.count()}")
    print(f"📝 Всего элементов: {PlaylistItem.objects.count()}")
    
except Exception as e:
    import traceback
    print(f"❌ Ошибка: {e}")
    traceback.print_exc()
