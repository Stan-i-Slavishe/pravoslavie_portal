#!/usr/bin/env python3
"""
Устанавливаем заведомо рабочее видео для теста
"""

import os
import django
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def set_working_video():
    """Устанавливаем заведомо рабочее видео"""
    print("🔧 Устанавливаем тестовое видео...")
    
    try:
        story = Story.objects.get(slug='pasha-voskresenie-hristovo')
        
        # Rick Roll - 100% рабочее видео для встраивания
        story.youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        story.youtube_embed_id = 'dQw4w9WgXcQ'
        story.save()
        
        print(f"✅ Установлено тестовое видео:")
        print(f"   Title: {story.title}")
        print(f"   URL: {story.youtube_url}")
        print(f"   ID: {story.youtube_embed_id}")
        print(f"   Embed: https://www.youtube.com/embed/{story.youtube_embed_id}")
        
        print("\n🌐 Проверьте страницу:")
        print(f"   http://127.0.0.1:8000/stories/{story.slug}/")
        
    except Story.DoesNotExist:
        print("❌ Рассказ не найден")

if __name__ == '__main__':
    set_working_video()
