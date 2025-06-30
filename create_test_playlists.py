#!/usr/bin/env python
"""
Скрипт для создания тестовых плейлистов
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

def create_test_playlists():
    """Создание тестовых плейлистов"""
    
    try:
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
            print(f"ℹ️  Использован существующий пользователь: {user.username}")
        
        # Создаем тестовые плейлисты
        playlists_data = [
            {
                'title': 'Любимые рассказы',
                'description': 'Коллекция самых трогательных историй',
                'playlist_type': 'public'
            },
            {
                'title': 'Детские истории',
                'description': 'Добрые рассказы для маленьких слушателей',
                'playlist_type': 'private'
            },
            {
                'title': 'Праздничные рассказы',
                'description': 'Истории к православным праздникам',
                'playlist_type': 'public'
            },
            {
                'title': 'Семейные ценности',
                'description': 'Рассказы о важности семьи и традиций',
                'playlist_type': 'private'
            }
        ]
        
        created_playlists = []
        
        for playlist_data in playlists_data:
            # Проверяем, не существует ли уже такой плейлист
            existing = Playlist.objects.filter(
                creator=user,
                title=playlist_data['title']
            ).first()
            
            if existing:
                print(f"⚠️  Плейлист '{playlist_data['title']}' уже существует")
                created_playlists.append(existing)
                continue
            
            # Создаем плейлист
            from django.utils.text import slugify
            
            playlist = Playlist.objects.create(
                creator=user,
                title=playlist_data['title'],
                slug=slugify(playlist_data['title'], allow_unicode=True),
                description=playlist_data['description'],
                playlist_type=playlist_data['playlist_type']
            )
            
            created_playlists.append(playlist)
            print(f"✅ Создан плейлист: {playlist.title}")
        
        # Добавляем рассказы в плейлисты (если есть)
        stories = Story.objects.filter(is_published=True)[:10]
        
        if stories.exists():
            print(f"\n📹 Найдено {stories.count()} рассказов для добавления в плейлисты")
            
            for playlist in created_playlists:
                # Добавляем 2-3 случайных рассказа в каждый плейлист
                import random
                selected_stories = random.sample(list(stories), min(3, len(stories)))
                
                for i, story in enumerate(selected_stories, 1):
                    playlist_item, created = PlaylistItem.objects.get_or_create(
                        playlist=playlist,
                        story=story,
                        defaults={'order': i}
                    )
                    
                    if created:
                        print(f"  ➕ Добавлен рассказ '{story.title}' в плейлист '{playlist.title}'")
        else:
            print("⚠️  Рассказы не найдены. Плейлисты созданы пустыми.")
        
        print(f"\n🎉 Успешно создано {len(created_playlists)} плейлистов!")
        print("\n📋 Информация для входа:")
        print(f"   Логин: {user.username}")
        print(f"   Пароль: testpass123")
        print(f"   Ссылка на плейлисты: http://127.0.0.1:8000/stories/playlists/")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании тестовых плейлистов: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Создание тестовых плейлистов...")
    success = create_test_playlists()
    
    if success:
        print("\n✅ Готово! Теперь вы можете:")
        print("   1. Запустить сервер: python manage.py runserver")
        print("   2. Войти под тестовым пользователем")
        print("   3. Перейти в 'Мои плейлисты' в меню пользователя")
        print("   4. Попробовать удалить плейлист")
    else:
        print("\n❌ Произошла ошибка. Проверьте лог выше.")
