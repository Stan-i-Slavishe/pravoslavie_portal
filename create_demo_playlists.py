#!/usr/bin/env python
"""
Скрипт для создания демонстрационных плейлистов для пользователя
"""

import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Playlist, Story, PlaylistItem

def create_demo_playlists():
    """Создает демонстрационные плейлисты"""
    try:
        # Ищем пользователя stassilin
        user = User.objects.get(username='stassilin')
        print(f"✅ Найден пользователь: {user.username}")
        
        # Получаем список рассказов
        stories = Story.objects.filter(is_published=True)
        print(f"✅ Найдено рассказов: {stories.count()}")
        
        if stories.count() < 3:
            print("❌ Недостаточно рассказов для создания плейлистов")
            return
        
        # Удаляем старые плейлисты пользователя для чистого тестирования
        old_playlists = Playlist.objects.filter(creator=user)
        if old_playlists.exists():
            print(f"🗑️ Удаляем {old_playlists.count()} старых плейлистов...")
            old_playlists.delete()
        
        # Создаем демонстрационные плейлисты
        playlists_data = [
            {
                'title': 'Святые истории',
                'description': 'Рассказы о жизни святых и их подвигах',
                'playlist_type': 'public',
                'stories_count': 3
            },
            {
                'title': 'Для детей',
                'description': 'Поучительные истории для самых маленьких',
                'playlist_type': 'public',
                'stories_count': 2
            },
            {
                'title': 'Мои избранные',
                'description': 'Личная подборка любимых рассказов',
                'playlist_type': 'private',
                'stories_count': 4
            },
            {
                'title': 'Праздничные истории',
                'description': 'Рассказы к церковным праздникам',
                'playlist_type': 'public',
                'stories_count': 2
            },
            {
                'title': 'Посмотреть позже',
                'description': 'Сохраненные для просмотра в будущем',
                'playlist_type': 'private',
                'stories_count': 1
            }
        ]
        
        created_playlists = []
        
        for i, playlist_data in enumerate(playlists_data):
            # Создаем плейлист
            playlist = Playlist.objects.create(
                title=playlist_data['title'],
                description=playlist_data['description'],
                creator=user,
                playlist_type=playlist_data['playlist_type']
            )
            
            # Добавляем рассказы в плейлист
            stories_for_playlist = stories[i:i+playlist_data['stories_count']]
            for order, story in enumerate(stories_for_playlist, 1):
                PlaylistItem.objects.create(
                    playlist=playlist,
                    story=story,
                    order=order
                )
            
            created_playlists.append(playlist)
            print(f"✅ Создан плейлист: '{playlist.title}' ({playlist_data['stories_count']} рассказов)")
        
        print(f"\n🎉 Успешно создано {len(created_playlists)} плейлистов для пользователя {user.username}")
        
        # Выводим статистику
        total_playlists = Playlist.objects.filter(creator=user).count()
        print(f"📊 Общее количество плейлистов пользователя: {total_playlists}")
        
        return created_playlists
        
    except User.DoesNotExist:
        print("❌ Пользователь 'stassilin' не найден")
        print("💡 Создайте пользователя или измените username в скрипте")
        return None
    except Exception as e:
        print(f"❌ Ошибка при создании плейлистов: {e}")
        return None

def show_playlists_info():
    """Показывает информацию о существующих плейлистах"""
    try:
        user = User.objects.get(username='stassilin')
        playlists = Playlist.objects.filter(creator=user).annotate(
            calculated_stories_count=Count('playlist_items')
        )
        
        print(f"\n📋 Плейлисты пользователя {user.username}:")
        print("-" * 60)
        
        for playlist in playlists:
            privacy = "🌐 Публичный" if playlist.playlist_type == 'public' else "🔒 Приватный"
            # Используем calculated_stories_count вместо stories_count
            stories_count = getattr(playlist, 'calculated_stories_count', 0)
            print(f"• {playlist.title}")
            print(f"  {privacy} | {stories_count} рассказов | {playlist.created_at.strftime('%d.%m.%Y')}")
            print(f"  {playlist.description}")
            print()
            
    except User.DoesNotExist:
        print("❌ Пользователь не найден")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    from django.db.models import Count
    
    print("🎵 Создание демонстрационных плейлистов")
    print("=" * 50)
    
    # Показываем текущие плейлисты
    show_playlists_info()
    
    # Создаем новые плейлисты
    create_demo_playlists()
    
    # Показываем результат
    show_playlists_info()
