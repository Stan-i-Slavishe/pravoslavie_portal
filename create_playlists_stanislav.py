#!/usr/bin/env python
"""
Быстрое создание тестовых плейлистов для пользователя Станислав
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

def create_playlists_for_stanislav():
    """Создание плейлистов для пользователя Станислав"""
    
    try:
        # Найти пользователя Станислав
        user = User.objects.filter(username='Станислав').first()
        if not user:
            # Попробуем найти по first_name
            user = User.objects.filter(first_name='Станислав').first()
        
        if not user:
            print("❌ Пользователь 'Станислав' не найден!")
            print("📋 Найденные пользователи:")
            for u in User.objects.all():
                print(f"   - {u.username} ({u.first_name} {u.last_name})")
            return False
        
        print(f"✅ Найден пользователь: {user.username} ({user.first_name} {user.last_name})")
        
        # Проверяем, есть ли уже плейлисты
        existing_playlists = Playlist.objects.filter(creator=user).count()
        print(f"ℹ️  У пользователя уже есть {existing_playlists} плейлистов")
        
        # Создаем тестовые плейлисты
        playlists_data = [
            {
                'title': 'Мои любимые рассказы',
                'description': 'Самые трогательные православные истории',
                'playlist_type': 'public'
            },
            {
                'title': 'Детские истории',
                'description': 'Добрые рассказы для детей',
                'playlist_type': 'private'
            },
            {
                'title': 'Праздничные рассказы',
                'description': 'Рассказы к православным праздникам',
                'playlist_type': 'public'
            }
        ]
        
        created_count = 0
        
        from django.utils.text import slugify
        
        for playlist_data in playlists_data:
            # Проверяем, не существует ли уже такой плейлист
            existing = Playlist.objects.filter(
                creator=user,
                title=playlist_data['title']
            ).first()
            
            if existing:
                print(f"⚠️  Плейлист '{playlist_data['title']}' уже существует")
                continue
            
            # Создаем уникальный slug
            base_slug = slugify(playlist_data['title'], allow_unicode=True)
            if not base_slug:
                base_slug = f'playlist-{created_count + 1}'
            
            slug = base_slug
            counter = 1
            while Playlist.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Создаем плейлист
            playlist = Playlist.objects.create(
                creator=user,
                title=playlist_data['title'],
                slug=slug,
                description=playlist_data['description'],
                playlist_type=playlist_data['playlist_type']
            )
            
            created_count += 1
            print(f"✅ Создан плейлист: {playlist.title} (slug: {playlist.slug})")
        
        # Добавляем рассказы в плейлисты (если есть)
        stories = Story.objects.filter(is_published=True)[:5]
        if stories.exists():
            print(f"\n📹 Найдено {stories.count()} рассказов для добавления")
            
            playlists = Playlist.objects.filter(creator=user)
            for playlist in playlists:
                # Добавляем 1-2 рассказа в каждый плейлист
                import random
                selected_stories = random.sample(list(stories), min(2, len(stories)))
                
                for i, story in enumerate(selected_stories, 1):
                    playlist_item, created = PlaylistItem.objects.get_or_create(
                        playlist=playlist,
                        story=story,
                        defaults={'order': i}
                    )
                    
                    if created:
                        print(f"  ➕ Добавлен '{story.title}' в '{playlist.title}'")
        
        print(f"\n🎉 Создано {created_count} новых плейлистов!")
        print(f"📋 Всего у пользователя {user.username}: {Playlist.objects.filter(creator=user).count()} плейлистов")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Создание плейлистов для Станислава...")
    success = create_playlists_for_stanislav()
    
    if success:
        print("\n✅ Готово! Теперь:")
        print("   1. Перезапустите сервер: python manage.py runserver")
        print("   2. Обновите страницу (Ctrl+F5)")
        print("   3. Виджет плейлистов должен появиться в сайдбаре")
    else:
        print("\n❌ Что-то пошло не так...")
