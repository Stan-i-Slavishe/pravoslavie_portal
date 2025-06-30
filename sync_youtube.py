#!/usr/bin/env python3
"""
Скрипт для синхронизации YouTube URL и ID
"""

import os
import django
import sys

# Добавляем путь к проекту
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def sync_youtube_ids():
    """Синхронизируем YouTube URL и ID"""
    print("🔧 Синхронизация YouTube URL и ID...")
    
    stories = Story.objects.all()
    
    for story in stories:
        if story.youtube_url:
            # Очищаем старый ID
            story.youtube_embed_id = ''
            # Сохраняем - ID извлечется автоматически
            story.save()
            print(f"✅ Обновлен: {story.title}")
            print(f"   URL: {story.youtube_url}")
            print(f"   ID: {story.youtube_embed_id}")
            print()
        else:
            print(f"⚠️  Нет URL: {story.title}")

def main():
    print("🚀 Исправление YouTube видео...")
    sync_youtube_ids()
    print("\n✅ Готово! Обновите страницу в браузере.")

if __name__ == '__main__':
    main()
