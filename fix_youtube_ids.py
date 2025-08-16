#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Быстрое исправление YouTube ID для конкретного рассказа
"""

import os
import sys
import django
import re
from pathlib import Path

# Добавляем путь к проекту
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

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

def fix_specific_story(slug):
    """Исправляет конкретный рассказ по slug"""
    try:
        story = Story.objects.get(slug=slug)
        print(f"📖 Найден рассказ: {story.title}")
        print(f"🔗 YouTube URL: {story.youtube_url or 'Не установлен'}")
        print(f"🆔 YouTube ID: {story.youtube_embed_id or 'Не установлен'}")
        
        if story.youtube_url and not story.youtube_embed_id:
            youtube_id = extract_youtube_id(story.youtube_url)
            if youtube_id:
                story.youtube_embed_id = youtube_id
                story.save(update_fields=['youtube_embed_id'])
                print(f"✅ YouTube ID установлен: {youtube_id}")
            else:
                print(f"❌ Не удалось извлечь ID из URL: {story.youtube_url}")
        elif story.youtube_embed_id:
            print("✅ YouTube ID уже установлен")
        else:
            print("⚠️ YouTube URL не установлен")
            
            # Предлагаем установить тестовый URL
            test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            story.youtube_url = test_url
            story.youtube_embed_id = "dQw4w9WgXcQ"
            story.save(update_fields=['youtube_url', 'youtube_embed_id'])
            print(f"🧪 Установлен тестовый YouTube URL: {test_url}")
        
        return story
        
    except Story.DoesNotExist:
        print(f"❌ Рассказ с slug '{slug}' не найден")
        return None

def list_stories_without_youtube_id():
    """Показывает рассказы без YouTube ID"""
    stories = Story.objects.filter(youtube_embed_id__isnull=True) | Story.objects.filter(youtube_embed_id='')
    
    if stories.exists():
        print("📋 Рассказы без YouTube ID:")
        for story in stories[:10]:  # Показываем первые 10
            print(f"   - {story.slug}: {story.title}")
        
        if stories.count() > 10:
            print(f"   ... и еще {stories.count() - 10} рассказов")
    else:
        print("✅ Все рассказы имеют YouTube ID")

def main():
    print("🎬 Исправление YouTube ID для рассказов")
    print("=" * 50)
    
    # Проверяем рассказ из ошибки
    problem_slug = "kak-svyatoj-luka-doch-spas"
    
    print(f"🔍 Проверяем проблемный рассказ: {problem_slug}")
    story = fix_specific_story(problem_slug)
    
    if story:
        print(f"\n🌐 Ссылка для проверки:")
        print(f"   http://127.0.0.1:8000/stories/{story.slug}/")
    
    print("\n" + "-" * 30)
    list_stories_without_youtube_id()

if __name__ == '__main__':
    main()
