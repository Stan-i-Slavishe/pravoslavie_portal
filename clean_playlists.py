#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Playlist

print("=== ФИНАЛЬНАЯ ОЧИСТКА ПЛЕЙЛИСТОВ ===")

# Удаляем все старые проблемные плейлисты
problematic_ids = [2, 3]  # ID проблемных плейлистов

for playlist_id in problematic_ids:
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        print(f"Найден проблемный плейлист ID {playlist_id}: '{playlist.slug}'")
        playlist.delete()
        print(f"✅ Удален плейлист ID {playlist_id}")
    except Playlist.DoesNotExist:
        print(f"Плейлист ID {playlist_id} уже не существует")

# Показываем оставшиеся плейлисты
print("\n=== ОСТАВШИЕСЯ ПЛЕЙЛИСТЫ ===")
remaining_playlists = Playlist.objects.all()
for p in remaining_playlists:
    print(f"  - ID: {p.id}, Slug: '{p.slug}', Title: '{p.title}'")

print(f"\nВсего плейлистов: {remaining_playlists.count()}")
print("\n🎉 ОЧИСТКА ЗАВЕРШЕНА!")
print("Теперь создайте новый плейлист - он должен работать корректно!")

input("\nНажмите Enter для закрытия...")
