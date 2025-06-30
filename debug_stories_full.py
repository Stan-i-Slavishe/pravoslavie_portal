#!/usr/bin/env python3
"""
Диагностика проблем Stories
"""

import os
import django
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story
from django.urls import reverse

def debug_story_urls():
    """Проверяем URL и Story"""
    print("🔍 Диагностика Story и URL...")
    
    try:
        story = Story.objects.get(slug='pasha-voskresenie-hristovo')
        
        print(f"📖 Story найден:")
        print(f"   ID: {story.id}")
        print(f"   Title: {story.title}")
        print(f"   Slug: {story.slug}")
        print(f"   YouTube URL: {story.youtube_url}")
        print(f"   YouTube ID: '{story.youtube_embed_id}'")
        print(f"   Published: {story.is_published}")
        
        # Проверяем URL
        try:
            detail_url = reverse('stories:detail', kwargs={'slug': story.slug})
            print(f"   Detail URL: {detail_url}")
        except Exception as e:
            print(f"   ❌ Detail URL error: {e}")
        
        try:
            view_url = reverse('stories:view_count', kwargs={'story_id': story.id})
            print(f"   View URL: {view_url}")
        except Exception as e:
            print(f"   ❌ View URL error: {e}")
        
        # Проверяем встраивание
        if story.youtube_embed_id:
            embed_url = f"https://www.youtube.com/embed/{story.youtube_embed_id}"
            print(f"   Embed URL: {embed_url}")
            print(f"   ID Length: {len(story.youtube_embed_id)}")
            
            # Проверяем на допустимые символы
            import re
            if re.match(r'^[a-zA-Z0-9_-]+$', story.youtube_embed_id):
                print(f"   ✅ YouTube ID валидный")
            else:
                print(f"   ❌ YouTube ID содержит недопустимые символы")
        else:
            print(f"   ❌ YouTube ID отсутствует")
            
    except Story.DoesNotExist:
        print("❌ Story не найден")

def fix_simple_video():
    """Устанавливаем максимально простое рабочее видео"""
    print("\n🔧 Устанавливаем простое тестовое видео...")
    
    try:
        story = Story.objects.get(slug='pasha-voskresenie-hristovo')
        
        # Максимально простое и надежное видео
        story.youtube_url = 'https://www.youtube.com/watch?v=YE7VzlLtp-4'
        story.youtube_embed_id = 'YE7VzlLtp-4'  # Big Buck Bunny
        story.save()
        
        print(f"✅ Установлено:")
        print(f"   URL: {story.youtube_url}")
        print(f"   ID: {story.youtube_embed_id}")
        print(f"   Embed: https://www.youtube.com/embed/{story.youtube_embed_id}")
        
    except Story.DoesNotExist:
        print("❌ Story не найден")

def check_urls_config():
    """Проверяем конфигурацию URL"""
    print("\n🔗 Проверяем URL конфигурацию...")
    
    try:
        from django.conf import settings
        from django.urls import get_resolver
        
        # Получаем все URL patterns
        resolver = get_resolver()
        
        print("📋 Доступные URL patterns для stories:")
        
        # Ищем patterns stories
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'namespace') and pattern.namespace == 'stories':
                print(f"   Stories namespace найден")
                break
        else:
            print("   ❌ Stories namespace НЕ найден")
            
    except Exception as e:
        print(f"   ❌ Ошибка проверки URL: {e}")

def main():
    print("=" * 60)
    debug_story_urls()
    check_urls_config()
    fix_simple_video()
    print("=" * 60)
    print("\n🚀 После исправления:")
    print("   1. Обновите страницу")
    print("   2. Должен появиться Big Buck Bunny")
    print("   3. Проверьте консоль на ошибки")

if __name__ == '__main__':
    main()
