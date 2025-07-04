import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Playlist, Story
from django.contrib.auth.models import User

print("=== ПРОВЕРКА ПЛЕЙЛИСТОВ ===")

try:
    # Получаем все плейлисты
    playlists = Playlist.objects.all()
    print(f"Всего плейлистов: {playlists.count()}")
    
    for playlist in playlists:
        print(f"ID: {playlist.id}")
        print(f"Slug: {playlist.slug}")
        print(f"Title: {playlist.title}")
        print(f"Creator: {playlist.creator.username}")
        print(f"Type: {playlist.playlist_type}")
        print(f"Stories count: {playlist.playlist_items.count()}")
        print("---")
        
    # Ищем проблемный плейлист
    problematic_playlist = Playlist.objects.filter(slug='борода').first()
    if problematic_playlist:
        print(f"\nНайден проблемный плейлист 'борода':")
        print(f"Creator: {problematic_playlist.creator.username}")
        print(f"Type: {problematic_playlist.playlist_type}")
        print(f"Title: {problematic_playlist.title}")
    else:
        print("\nПлейлист 'борода' не найден")
        
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
