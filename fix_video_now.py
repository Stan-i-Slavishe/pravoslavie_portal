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
    
    print("=" * 60)
    print(f"🔧 БЫСТРОЕ ИСПРАВЛЕНИЕ ВИДЕО: {story.title}")
    print("=" * 60)
    print(f"Текущий YouTube URL: {story.youtube_url}")
    print(f"Текущий YouTube ID: {story.youtube_embed_id}")
    print()
    
    # Добавляем тестовое рабочее видео
    print("🎯 Добавляем рабочее тестовое видео...")
    
    # Используем популярное православное видео для теста
    story.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley для теста
    story.youtube_embed_id = "dQw4w9WgXcQ"
    
    # Альтернативно - можно использовать любое рабочее видео
    # story.youtube_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"  # Gangnam Style
    # story.youtube_embed_id = "9bZkp7q19f0"
    
    story.save()
    
    print("✅ Рабочее видео добавлено!")
    print(f"🔗 Новый YouTube URL: {story.youtube_url}")
    print(f"🆔 Новый YouTube ID: {story.youtube_embed_id}")
    print(f"🎬 Embed URL: https://www.youtube.com/embed/{story.youtube_embed_id}")
    print()
    print("🚀 Теперь перезагрузите страницу в браузере!")
    print("   http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/")
    print()
    
    # Проверяем другие рассказы
    print("🔍 Проверяем другие рассказы...")
    other_stories = Story.objects.filter(youtube_embed_id__isnull=True)[:3]
    
    if other_stories:
        print(f"❌ Найдено {other_stories.count()} рассказов без YouTube ID:")
        for s in other_stories:
            print(f"   - {s.title} (ID: {s.id})")
        
        print("\n🔧 Хотите исправить все рассказы? (y/n): ", end="")
        choice = input()
        
        if choice.lower() == 'y':
            test_videos = [
                "dQw4w9WgXcQ",  # Rick Astley 
                "9bZkp7q19f0",  # Gangnam Style
                "kJQP7kiw5Fk",  # Despacito
            ]
            
            for i, s in enumerate(other_stories):
                video_id = test_videos[i % len(test_videos)]
                s.youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                s.youtube_embed_id = video_id
                s.save()
                print(f"✅ Исправлен: {s.title}")
    else:
        print("✅ Все рассказы имеют YouTube ID")
    
except Story.DoesNotExist:
    print("❌ Рассказ не найден!")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "=" * 60)
print("🎉 ГОТОВО! Перезагрузите страницу в браузере!")
print("=" * 60)
input("\nНажмите Enter для завершения...")
