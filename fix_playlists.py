#!/usr/bin/env python
"""
Скрипт для исправления проблемы с плейлистами
Запуск: python fix_playlists.py
"""
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Playlist, PlaylistItem
from django.contrib.auth.models import User
from django.db import transaction

def main():
    print("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ПЛЕЙЛИСТАМИ")
    print("=" * 50)
    
    try:
        with transaction.atomic():
            # 1. Проверяем все плейлисты
            playlists = Playlist.objects.all()
            print(f"📊 Всего плейлистов в базе: {playlists.count()}")
            
            # 2. Ищем проблемный плейлист 'борода'
            problematic_playlists = Playlist.objects.filter(slug='борода')
            
            if problematic_playlists.exists():
                print(f"🔍 Найдено плейлистов с slug='борода': {problematic_playlists.count()}")
                
                for playlist in problematic_playlists:
                    print(f"   - ID: {playlist.id}")
                    print(f"   - Title: '{playlist.title}'")
                    print(f"   - Creator: {playlist.creator.username}")
                    print(f"   - Type: {playlist.playlist_type}")
                    print(f"   - Stories: {playlist.playlist_items.count()}")
                    
                    # Предлагаем исправления
                    print(f"\n🔧 Исправляем плейлист ID {playlist.id}:")
                    
                    # Вариант 1: Изменить slug
                    new_slug = f"playlist-{playlist.creator.username}-{playlist.id}"
                    playlist.slug = new_slug
                    playlist.save()
                    print(f"   ✅ Изменен slug на: '{new_slug}'")
                    
            else:
                print("✅ Проблемный плейлист 'борода' не найден")
            
            # 3. Проверяем все плейлисты на корректность
            print(f"\n🔍 Проверяем все плейлисты на корректность...")
            
            for playlist in Playlist.objects.all():
                # Проверяем уникальность slug
                duplicates = Playlist.objects.filter(
                    slug=playlist.slug
                ).exclude(id=playlist.id)
                
                if duplicates.exists():
                    print(f"⚠️ Найдены дубликаты slug '{playlist.slug}' для плейлиста ID {playlist.id}")
                    new_slug = f"{playlist.slug}-{playlist.id}"
                    playlist.slug = new_slug
                    playlist.save()
                    print(f"   ✅ Исправлен на: '{new_slug}'")
                
                # Проверяем корректность полей
                if not playlist.title:
                    playlist.title = f"Плейлист {playlist.id}"
                    playlist.save()
                    print(f"   ✅ Добавлено название для плейлиста ID {playlist.id}")
            
            # 4. Финальная проверка
            print(f"\n📊 ФИНАЛЬНАЯ СТАТИСТИКА:")
            playlists = Playlist.objects.all()
            print(f"   Всего плейлистов: {playlists.count()}")
            
            for playlist in playlists:
                print(f"   - '{playlist.slug}' | '{playlist.title}' | {playlist.creator.username}")
                
        print(f"\n✅ ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ УСПЕШНО!")
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
