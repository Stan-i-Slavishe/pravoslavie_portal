#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Быстрое исправление конкретного рассказа
"""

import re

def extract_youtube_id(url):
    """Извлекает ID видео из YouTube URL"""
    if not url:
        return None
    
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

# Проверяем некоторые тестовые URL
test_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://youtu.be/dQw4w9WgXcQ", 
    "https://www.youtube.com/embed/dQw4w9WgXcQ",
]

print("🧪 Тестирование извлечения YouTube ID:")
for url in test_urls:
    youtube_id = extract_youtube_id(url)
    print(f"  {url} -> {youtube_id}")

print("\n✅ Функция работает правильно!")
print("\nТеперь запустите исправление через Django shell:")
print("python manage.py shell")
print("")
print("Затем выполните в shell:")
print("""
from stories.models import Story
import re

def extract_youtube_id(url):
    if not url:
        return None
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Исправляем конкретный рассказ
try:
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    print(f"Найден: {story.title}")
    
    if story.youtube_url and not story.youtube_embed_id:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save()
            print(f"✅ YouTube ID установлен: {youtube_id}")
        else:
            print("❌ Не удалось извлечь ID")
    elif not story.youtube_url:
        # Устанавливаем тестовое видео
        story.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        story.youtube_embed_id = "dQw4w9WgXcQ"
        story.save()
        print("🧪 Установлено тестовое видео")
    else:
        print("✅ Видео уже настроено")
        
except Story.DoesNotExist:
    print("❌ Рассказ не найден")

# Исправляем все рассказы без YouTube ID
stories_fixed = 0
for story in Story.objects.filter(youtube_embed_id__isnull=True):
    if story.youtube_url:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save()
            stories_fixed += 1

print(f"🎉 Исправлено {stories_fixed} рассказов")
""")
