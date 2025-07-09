#!/usr/bin/env python
"""
Простая проверка созданных плейлистов
"""

import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Playlist, PlaylistItem
from django.db.models import Count

def check_playlists():
    """Проверяет плейлисты пользователя"""
    try:
        user = User.objects.get(username='stassilin')
        print(f"✅ Пользователь: {user.username}")
        
        playlists = Playlist.objects.filter(creator=user).annotate(
            items_count=Count('playlist_items')
        ).order_by('-created_at')
        
        print(f"📊 Всего плейлистов: {playlists.count()}")
        print("=" * 50)
        
        for i, playlist in enumerate(playlists, 1):
            privacy_icon = "🌐" if playlist.playlist_type == 'public' else "🔒"
            print(f"{i}. {privacy_icon} {playlist.title}")
            print(f"   📝 {playlist.description}")
            print(f"   🎬 {playlist.items_count} рассказов")
            print(f"   📅 {playlist.created_at.strftime('%d.%m.%Y %H:%M')}")
            
            # Показываем рассказы в плейлисте
            items = PlaylistItem.objects.filter(playlist=playlist).select_related('story').order_by('order')
            if items.exists():
                print(f"   📋 Рассказы:")
                for item in items:
                    print(f"      {item.order}. {item.story.title}")
            print()
        
        return playlists.count()
        
    except User.DoesNotExist:
        print("❌ Пользователь 'stassilin' не найден")
        return 0
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 0

if __name__ == "__main__":
    print("🎵 Проверка плейлистов пользователя")
    print("=" * 50)
    
    count = check_playlists()
    
    if count > 0:
        print(f"🎉 Найдено {count} плейлистов!")
        print("✅ Теперь обновите страницу рассказа, чтобы увидеть их в сайдбаре")
    else:
        print("❌ Плейлисты не найдены")
        print("💡 Запустите: python create_demo_playlists.py")
