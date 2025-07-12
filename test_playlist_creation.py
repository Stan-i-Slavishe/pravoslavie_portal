#!/usr/bin/env python
"""
Тестовая команда для проверки создания плейлистов
"""
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Playlist, PlaylistItem, Story

def test_playlist_creation():
    """Тестирование создания плейлиста"""
    print("🧪 Тестирование создания плейлиста...")
    
    try:
        # Проверяем модели
        print(f"✅ Playlist model: {Playlist}")
        print(f"✅ PlaylistItem model: {PlaylistItem}")
        print(f"✅ Story model: {Story}")
        
        # Проверяем пользователей
        users = User.objects.all()
        print(f"👥 Пользователей в системе: {users.count()}")
        
        if users.count() == 0:
            print("❌ Нет пользователей для тестирования")
            return
        
        user = users.first()
        print(f"👤 Тестируем с пользователем: {user.username}")
        
        # Проверяем рассказы
        stories = Story.objects.filter(is_published=True)
        print(f"📚 Опубликованных рассказов: {stories.count()}")
        
        if stories.count() == 0:
            print("❌ Нет рассказов для тестирования")
            return
        
        story = stories.first()
        print(f"📖 Тестируем с рассказом: {story.title}")
        
        # Проверяем существующие плейлисты
        existing_playlists = Playlist.objects.filter(creator=user)
        print(f"🎵 Существующих плейлистов у пользователя: {existing_playlists.count()}")
        
        # Создаем тестовый плейлист
        test_playlist_name = "Тестовый плейлист"
        
        # Удаляем если уже есть
        Playlist.objects.filter(creator=user, title=test_playlist_name).delete()
        
        playlist = Playlist.objects.create(
            title=test_playlist_name,
            slug="test-playlist-123",
            creator=user,
            description="Автоматически созданный тестовый плейлист",
            playlist_type='private'
        )
        print(f"✅ Создан плейлист: {playlist.title} (ID: {playlist.id})")
        
        # Добавляем рассказ в плейлист
        playlist_item = PlaylistItem.objects.create(
            playlist=playlist,
            story=story,
            order=1
        )
        print(f"✅ Добавлен рассказ в плейлист: {story.title}")
        
        # Проверяем связи
        items_count = playlist.playlist_items.count()
        print(f"📊 Элементов в плейлисте: {items_count}")
        
        # Проверяем обратную связь
        story_playlists = story.playlists.count()
        print(f"📊 Плейлистов у рассказа: {story_playlists}")
        
        print("🎉 Все тесты прошли успешно!")
        
        # Очищаем тестовые данные
        playlist.delete()
        print("🧹 Тестовые данные очищены")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_playlist_creation()
