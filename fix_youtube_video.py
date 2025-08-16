#!/usr/bin/env python3
"""
🎬 СКРИПТ ИСПРАВЛЕНИЯ YOUTUBE ВИДЕО
Проверяет и исправляет проблемы с отображением YouTube видео
"""

import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def check_youtube_ids():
    """Проверяем YouTube ID у всех рассказов"""
    print("🔍 Проверяем YouTube ID у рассказов...")
    
    stories = Story.objects.all()
    
    for story in stories:
        print(f"\n📖 Рассказ: {story.title}")
        print(f"   YouTube URL: {story.youtube_url}")
        print(f"   YouTube ID: {story.youtube_embed_id}")
        
        if story.youtube_url and not story.youtube_embed_id:
            print("   ⚠️ URL есть, но ID отсутствует!")
            # Извлекаем ID
            new_id = story.extract_youtube_id(story.youtube_url)
            if new_id:
                story.youtube_embed_id = new_id
                story.save()
                print(f"   ✅ ID извлечен и сохранен: {new_id}")
            else:
                print("   ❌ Не удалось извлечь ID")
        elif story.youtube_embed_id:
            print(f"   ✅ ID корректный: {story.youtube_embed_id}")
        else:
            print("   ⚠️ Нет YouTube URL")

def test_specific_story(slug="kak-svyatoj-luka-doch-spas"):
    """Тестируем конкретный рассказ"""
    print(f"\n🎯 Тестируем рассказ: {slug}")
    
    try:
        story = Story.objects.get(slug=slug)
        print(f"✅ Рассказ найден: {story.title}")
        print(f"   YouTube URL: {story.youtube_url}")
        print(f"   YouTube ID: {story.youtube_embed_id}")
        
        if story.youtube_embed_id:
            embed_url = f"https://www.youtube.com/embed/{story.youtube_embed_id}"
            print(f"   🎬 Embed URL: {embed_url}")
            
            # Проверяем embed URL
            import requests
            try:
                response = requests.head(embed_url, timeout=5)
                if response.status_code == 200:
                    print("   ✅ YouTube видео доступно")
                else:
                    print(f"   ⚠️ YouTube ответил: {response.status_code}")
            except:
                print("   ⚠️ Не удалось проверить доступность YouTube")
        else:
            print("   ❌ YouTube ID отсутствует")
            
    except Story.DoesNotExist:
        print(f"❌ Рассказ с slug '{slug}' не найден")

def fix_all_stories():
    """Исправляем все рассказы"""
    print("\n🔧 Исправляем все рассказы...")
    
    stories = Story.objects.filter(youtube_url__isnull=False).exclude(youtube_url='')
    fixed_count = 0
    
    for story in stories:
        if not story.youtube_embed_id and story.youtube_url:
            new_id = story.extract_youtube_id(story.youtube_url)
            if new_id:
                story.youtube_embed_id = new_id
                story.save()
                fixed_count += 1
                print(f"✅ Исправлен: {story.title} -> {new_id}")
    
    print(f"\n🎉 Исправлено рассказов: {fixed_count}")

if __name__ == "__main__":
    print("🎬 YouTube Video Fix Script")
    print("=" * 50)
    
    # Проверяем все рассказы
    check_youtube_ids()
    
    # Тестируем конкретный рассказ
    test_specific_story()
    
    # Исправляем проблемы
    fix_all_stories()
    
    print("\n" + "=" * 50)
    print("✅ Скрипт завершен!")
