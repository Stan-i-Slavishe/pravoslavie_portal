#!/usr/bin/env python3
"""
Простая диагностика проблем
"""

import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, 'E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    print("✅ Django инициализирован")
    
    # Проверяем базу данных
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"📊 Таблиц в БД: {len(tables)}")
    
    # Ищем таблицы плейлистов
    playlist_tables = [t for t in tables if 'playlist' in t.lower()]
    print(f"🎵 Таблиц плейлистов: {playlist_tables}")
    
    # Проверяем модели
    try:
        from stories.models import Story
        story_count = Story.objects.count()
        print(f"📚 Рассказов: {story_count}")
    except Exception as e:
        print(f"❌ Ошибка Story: {e}")
    
    try:
        from stories.models import Playlist
        if Playlist:
            playlist_count = Playlist.objects.count()
            print(f"🎵 Плейлистов: {playlist_count}")
        else:
            print("⚠️ Playlist is None")
    except Exception as e:
        print(f"❌ Ошибка Playlist: {e}")
    
    # Проверяем shop модели
    try:
        from shop.models import Cart
        print("✅ Shop модели доступны")
    except Exception as e:
        print(f"❌ Ошибка Shop: {e}")
    
    print("\n🎯 Диагностика завершена")
    
except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
