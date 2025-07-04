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

print("=== ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ ===")

# Показываем все плейлисты
print("Текущие плейлисты:")
all_playlists = Playlist.objects.all()
for p in all_playlists:
    print(f"  ID: {p.id}, Slug: '{p.slug}', Title: '{p.title}'")

# Ищем конкретно проблемный плейлист с ID 3
problem_playlist = Playlist.objects.filter(id=3).first()

if problem_playlist:
    print(f"\nНайден проблемный плейлист ID 3: '{problem_playlist.slug}'")
    
    # Исправляем его
    old_slug = problem_playlist.slug
    new_slug = f"playlist-fixed-{problem_playlist.id}"
    problem_playlist.slug = new_slug
    problem_playlist.save()
    print(f"✅ Исправлен: '{old_slug}' -> '{new_slug}'")
else:
    print("\nПлейлист с ID 3 не найден")

# Дополнительно ищем все плейлисты с похожими slug
suspicious_playlists = []
for p in all_playlists:
    # Ищем плейлисты содержащие "борода" в любом виде
    if 'борода' in p.slug.lower() or 'бородa' in p.slug.lower():
        suspicious_playlists.append(p)

if suspicious_playlists:
    print(f"\nНайдено подозрительных плейлистов: {len(suspicious_playlists)}")
    for playlist in suspicious_playlists:
        if playlist.id != 3:  # Не исправляем дважды
            old_slug = playlist.slug
            new_slug = f"playlist-safe-{playlist.id}"
            playlist.slug = new_slug
            playlist.save()
            print(f"✅ Исправлен: '{old_slug}' -> '{new_slug}'")

# Проверяем результат
print("\n=== РЕЗУЛЬТАТ ===")
final_playlists = Playlist.objects.all()
print("Итоговые плейлисты:")
for p in final_playlists:
    print(f"  - ID: {p.id}, Slug: '{p.slug}'")

print("\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
print("Теперь перезагрузите страницу в браузере.")

input("\nНажмите Enter для закрытия...")
