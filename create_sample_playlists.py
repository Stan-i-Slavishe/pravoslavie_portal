#!/usr/bin/env python
"""
Создание тестовых плейлистов для демонстрации
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
from django.utils.text import slugify

def create_sample_playlists():
    """Создание примеров плейлистов"""
    
    try:
        # Получаем первого администратора или создаем тестового пользователя
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'is_superuser': True,
                    'is_staff': True
                }
            )
            if created:
                admin_user.set_password('admin123')
                admin_user.save()
                print(f"✅ Создан администратор: {admin_user.username}")
        
        # Получаем существующие рассказы
        stories = Story.objects.filter(is_published=True)[:10]
        print(f"📚 Найдено {stories.count()} опубликованных рассказов")
        
        if stories.count() == 0:
            print("❌ Нет опубликованных рассказов для добавления в плейлисты")
            return
        
        # Создаем плейлисты
        playlists_data = [
            {
                'title': 'Избранные рассказы',
                'description': 'Лучшие духовные истории',
                'playlist_type': 'public',
                'stories_count': 5
            },
            {
                'title': 'Поучительные истории',
                'description': 'Рассказы с глубоким смыслом',
                'playlist_type': 'public',
                'stories_count': 4
            },
            {
                'title': 'Чудеса и исцеления',
                'description': 'Истории о божественных чудесах',
                'playlist_type': 'public',
                'stories_count': 3
            }
        ]
        
        created_playlists = 0
        
        for playlist_data in playlists_data:
            # Проверяем, существует ли уже такой плейлист
            existing_playlist = Playlist.objects.filter(
                title=playlist_data['title'],
                creator=admin_user
            ).first()
            
            if existing_playlist:
                print(f"ℹ️  Плейлист '{playlist_data['title']}' уже существует")
                continue
            
            # Создаем плейлист
            playlist = Playlist.objects.create(
                title=playlist_data['title'],
                slug=slugify(playlist_data['title'], allow_unicode=True),
                description=playlist_data['description'],
                creator=admin_user,
                playlist_type=playlist_data['playlist_type']
            )
            
            # Добавляем рассказы в плейлист
            stories_to_add = stories[:playlist_data['stories_count']]
            for order, story in enumerate(stories_to_add, 1):
                PlaylistItem.objects.create(
                    playlist=playlist,
                    story=story,
                    order=order
                )
            
            created_playlists += 1
            print(f"✅ Создан плейлист: '{playlist.title}' с {stories_to_add.count()} рассказами")
        
        print(f"\n🎉 Успешно создано {created_playlists} плейлистов!")
        
        # Создаем системные плейлисты для админа
        from stories.models import UserPlaylistPreference
        
        user_prefs, created = UserPlaylistPreference.objects.get_or_create(
            user=admin_user
        )
        
        # Создаем плейлист "Посмотреть позже"
        watch_later = user_prefs.get_or_create_watch_later()
        print(f"✅ Создан системный плейлист: {watch_later.title}")
        
        # Создаем плейлист "Избранное"
        favorites = user_prefs.get_or_create_favorites()
        print(f"✅ Создан системный плейлист: {favorites.title}")
        
        # Добавляем несколько рассказов в системные плейлисты
        if stories.count() >= 2:
            PlaylistItem.objects.get_or_create(
                playlist=watch_later,
                story=stories[0],
                defaults={'order': 1}
            )
            PlaylistItem.objects.get_or_create(
                playlist=favorites,
                story=stories[1],
                defaults={'order': 1}
            )
            print("✅ Добавлены тестовые рассказы в системные плейлисты")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_sample_playlists()
