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

# Находим проблемные плейлисты
problem_playlists = []
for p in all_playlists:
    if 'борода' in p.slug:
        problem_playlists.append(p)

print(f"\nНайдено проблемных плейлистов: {len(problem_playlists)}")

# Исправляем проблемные плейлисты
for i, playlist in enumerate(problem_playlists):
    old_slug = playlist.slug
    new_slug = f"playlist-fixed-{playlist.id}"
    playlist.slug = new_slug
    playlist.save()
    print(f"✅ Исправлен плейлист ID {playlist.id}: '{old_slug}' -> '{new_slug}'")

# Проверяем результат
print("\n=== РЕЗУЛЬТАТ ===")
remaining_problems = 0
final_playlists = Playlist.objects.all()
print("Итоговые плейлисты:")
for p in final_playlists:
    print(f"  - ID: {p.id}, Slug: '{p.slug}'")
    if 'борода' in p.slug:
        remaining_problems += 1

if remaining_problems == 0:
    print("\n🎉 ВСЕ ПРОБЛЕМЫ ИСПРАВЛЕНЫ!")
    print("Теперь перезагрузите страницу в браузере.")
else:
    print(f"\n⚠️ Осталось проблем: {remaining_problems}")

input("\nНажмите Enter для закрытия...")
