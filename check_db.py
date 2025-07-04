#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Проверяем плейлисты
    import django
    django.setup()
    
    from stories.models import Playlist
    
    print("=== ПРОВЕРКА ПЛЕЙЛИСТОВ ===")
    
    try:
        playlists = Playlist.objects.all()
        print(f"Всего плейлистов: {playlists.count()}")
        
        for playlist in playlists:
            print(f"ID: {playlist.id}, Slug: '{playlist.slug}', Title: '{playlist.title}', Creator: {playlist.creator.username}")
            
        # Ищем проблемный
        problem_playlist = Playlist.objects.filter(slug='борода').first()
        if problem_playlist:
            print(f"\n🔍 Найден плейлист 'борода': Creator={problem_playlist.creator.username}, Type={problem_playlist.playlist_type}")
        else:
            print("\n✅ Плейлист 'борода' не найден")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
