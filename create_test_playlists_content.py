#!/usr/bin/env python3
"""
Скрипт для создания тестовых плейлистов с содержимым
Запускать из корня проекта: python create_test_playlists_content.py
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Story, Playlist, PlaylistItem, UserPlaylistPreference

def create_test_playlists():
    """Создает тестовые плейлисты с содержимым"""
    
    print("🎵 Создание тестовых плейлистов...")
    
    # Получаем или создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Тест',
            'last_name': 'Пользователь'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Создан тестовый пользователь: {user.username}")
    else:
        print(f"👤 Используем существующего пользователя: {user.username}")
    
    # Получаем существующие рассказы
    stories = list(Story.objects.all()[:10])  # Берем первые 10 рассказов
    
    if not stories:
        print("❌ Нет рассказов в базе данных. Сначала создайте рассказы.")
        return
    
    print(f"📚 Найдено {len(stories)} рассказов для добавления в плейлисты")
    
    # Создаем системные плейлисты
    prefs, created = UserPlaylistPreference.objects.get_or_create(user=user)
    
    # Плейлист "Посмотреть позже"
    watch_later = prefs.get_or_create_watch_later()
    
    # Добавляем рассказы в "Посмотреть позже"
    for i, story in enumerate(stories[:5]):
        item, created = PlaylistItem.objects.get_or_create(
            playlist=watch_later,
            story=story,
            defaults={'position': i + 1}
        )
        if created:
            print(f"📼 Добавлен в 'Посмотреть позже': {story.title}")
    
    # Плейлист "Мне нравится"
    favorites = prefs.get_or_create_favorites()
    
    # Добавляем рассказы в "Мне нравится"
    for i, story in enumerate(stories[2:5]):  # Частично пересекающиеся
        item, created = PlaylistItem.objects.get_or_create(
            playlist=favorites,
            story=story,
            defaults={'position': i + 1}
        )
        if created:
            print(f"❤️ Добавлен в 'Мне нравится': {story.title}")
    
    # Создаем пользовательские плейлисты
    test_playlists = [
        {
            'title': 'Отлично',
            'description': 'Самые лучшие рассказы',
            'is_public': False,
            'stories': stories[:2]
        },
        {
            'title': 'Левый',
            'description': 'Экспериментальный плейлист',
            'is_public': False,
            'stories': stories[5:6]
        },
        {
            'title': 'Тестовый плей лист',
            'description': 'Публичный плейлист для всех',
            'is_public': True,
            'stories': stories[3:6]
        }
    ]
    
    for playlist_data in test_playlists:
        playlist, created = Playlist.objects.get_or_create(
            user=user,
            title=playlist_data['title'],
            defaults={
                'description': playlist_data['description'],
                'is_public': playlist_data['is_public']
            }
        )
        
        if created:
            print(f"🎼 Создан плейлист: {playlist.title}")
        
        # Добавляем рассказы в плейлист
        for i, story in enumerate(playlist_data['stories']):
            item, created = PlaylistItem.objects.get_or_create(
                playlist=playlist,
                story=story,
                defaults={'position': i + 1}
            )
            if created:
                print(f"   📹 Добавлен рассказ: {story.title}")
    
    print("\n🎉 Тестовые плейлисты созданы успешно!")
    print("\n📊 Статистика:")
    print(f"   👤 Пользователь: {user.username}")
    print(f"   🎵 Системных плейлистов: 2")
    print(f"   🎼 Пользовательских плейлистов: {len(test_playlists)}")
    print(f"   📹 Всего элементов: {PlaylistItem.objects.filter(playlist__user=user).count()}")

def clean_playlists():
    """Очищает тестовые плейлисты"""
    print("🧹 Очистка тестовых плейлистов...")
    
    try:
        user = User.objects.get(username='testuser')
        
        # Удаляем пользовательские плейлисты
        playlists_count = Playlist.objects.filter(user=user).count()
        Playlist.objects.filter(user=user).delete()
        
        # Удаляем системные плейлисты
        try:
            prefs = UserPlaylistPreference.objects.get(user=user)
            prefs.delete()
        except UserPlaylistPreference.DoesNotExist:
            pass
        
        print(f"✅ Удалено {playlists_count} плейлистов")
        
    except User.DoesNotExist:
        print("👤 Тестовый пользователь не найден")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Управление тестовыми плейлистами')
    parser.add_argument('--clean', action='store_true', help='Очистить тестовые плейлисты')
    
    args = parser.parse_args()
    
    if args.clean:
        clean_playlists()
    else:
        create_test_playlists()
