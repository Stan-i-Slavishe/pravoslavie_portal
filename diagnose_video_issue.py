#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

try:
    # Ищем рассказ по slug
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    
    print("=" * 50)
    print(f"📺 ДИАГНОСТИКА РАССКАЗА: {story.title}")
    print("=" * 50)
    print(f"ID: {story.id}")
    print(f"Slug: {story.slug}")
    print(f"YouTube URL: {story.youtube_url}")
    print(f"YouTube Embed ID: {story.youtube_embed_id}")
    print(f"Опубликован: {story.is_published}")
    print(f"Дата создания: {story.created_at}")
    print()
    
    # Проверяем YouTube данные
    if story.youtube_url:
        print("✅ YouTube URL есть")
        if story.youtube_embed_id:
            print(f"✅ YouTube ID: {story.youtube_embed_id}")
            print(f"🔗 Embed URL: https://www.youtube.com/embed/{story.youtube_embed_id}")
            print(f"🖼️ Thumbnail: https://img.youtube.com/vi/{story.youtube_embed_id}/maxresdefault.jpg")
        else:
            print("❌ YouTube ID отсутствует!")
            print("🔧 Попытаемся извлечь ID из URL...")
            
            # Пытаемся извлечь ID
            import re
            patterns = [
                r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\n?#]+)',
                r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&\n?#]+)',
                r'(?:https?://)?(?:www\.)?youtu\.be/([^&\n?#]+)',
            ]
            
            youtube_id = None
            for pattern in patterns:
                match = re.search(pattern, story.youtube_url)
                if match:
                    youtube_id = match.group(1)
                    break
            
            if youtube_id:
                print(f"🔍 Найден ID: {youtube_id}")
                
                # Автоматически исправляем
                story.youtube_embed_id = youtube_id
                story.save()
                print("✅ ID сохранен в базу данных!")
            else:
                print("❌ Не удалось извлечь ID из URL")
    else:
        print("❌ YouTube URL отсутствует!")
    
    print()
    print("=" * 50)
    print("🎬 РЕКОМЕНДАЦИИ:")
    print("=" * 50)
    
    if not story.youtube_url:
        print("1. Добавьте YouTube URL в админке")
    elif not story.youtube_embed_id:
        print("1. Проверьте формат YouTube URL")
        print("2. Убедитесь что URL содержит корректный ID видео")
    else:
        print("1. Попробуйте открыть embed URL в браузере:")
        print(f"   https://www.youtube.com/embed/{story.youtube_embed_id}")
        print("2. Проверьте, не заблокировано ли видео")
        print("3. Убедитесь что видео существует на YouTube")
    
except Story.DoesNotExist:
    print("❌ Рассказ не найден!")
except Exception as e:
    print(f"❌ Ошибка: {e}")

input("\nНажмите Enter для завершения...")
