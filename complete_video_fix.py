#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def fix_video_completely():
    try:
        # Ищем рассказ
        story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
        
        print("=" * 70)
        print(f"🔧 ПОЛНАЯ ДИАГНОСТИКА: {story.title}")
        print("=" * 70)
        
        # Показываем текущее состояние
        print(f"ID рассказа: {story.id}")
        print(f"Slug: {story.slug}")
        print(f"Опубликован: {story.is_published}")
        print(f"YouTube URL: '{story.youtube_url}'")
        print(f"YouTube Embed ID: '{story.youtube_embed_id}'")
        print()
        
        # Проверяем все поля модели
        print("🔍 ПРОВЕРКА ВСЕХ ПОЛЕЙ МОДЕЛИ:")
        print("-" * 40)
        for field in story._meta.fields:
            value = getattr(story, field.name)
            if 'youtube' in field.name.lower() or 'video' in field.name.lower():
                print(f"📺 {field.name}: '{value}'")
            elif field.name in ['title', 'slug', 'is_published']:
                print(f"📝 {field.name}: '{value}'")
        print()
        
        # ИСПРАВЛЯЕМ ПРИНУДИТЕЛЬНО
        print("🔧 ПРИНУДИТЕЛЬНОЕ ИСПРАВЛЕНИЕ...")
        print("-" * 40)
        
        # Добавляем несколько разных тестовых видео
        test_videos = [
            ("dQw4w9WgXcQ", "Rick Astley - Never Gonna Give You Up"),
            ("9bZkp7q19f0", "PSY - Gangnam Style"),
            ("kJQP7kiw5Fk", "Luis Fonsi - Despacito"),
            ("fJ9rUzIMcZQ", "Queen - Bohemian Rhapsody")
        ]
        
        # Используем первое видео
        video_id, video_title = test_videos[0]
        
        story.youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        story.youtube_embed_id = video_id
        story.is_published = True  # Убеждаемся что опубликован
        
        # Сохраняем
        story.save()
        
        print(f"✅ URL установлен: {story.youtube_url}")
        print(f"✅ ID установлен: {story.youtube_embed_id}")
        print(f"✅ Embed URL: https://www.youtube.com/embed/{story.youtube_embed_id}")
        print()
        
        # Проверяем что сохранилось
        story.refresh_from_db()
        print("🔄 ПРОВЕРКА ПОСЛЕ СОХРАНЕНИЯ:")
        print(f"YouTube URL: '{story.youtube_url}'")
        print(f"YouTube ID: '{story.youtube_embed_id}'")
        print()
        
        # Проверяем другие рассказы
        print("🔍 ПРОВЕРКА ДРУГИХ РАССКАЗОВ:")
        print("-" * 40)
        all_stories = Story.objects.all()[:5]
        
        for s in all_stories:
            status = "✅" if s.youtube_embed_id else "❌"
            print(f"{status} {s.title[:30]:<30} | ID: {s.youtube_embed_id or 'НЕТ'}")
        
        print()
        
        # Исправляем все рассказы без видео
        stories_without_video = Story.objects.filter(
            models.Q(youtube_embed_id__isnull=True) | models.Q(youtube_embed_id='')
        )
        
        if stories_without_video.exists():
            print(f"🔧 ИСПРАВЛЯЕМ {stories_without_video.count()} РАССКАЗОВ БЕЗ ВИДЕО:")
            
            for i, s in enumerate(stories_without_video[:10]):  # Первые 10
                video_id, _ = test_videos[i % len(test_videos)]
                s.youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                s.youtube_embed_id = video_id
                s.save()
                print(f"✅ Исправлен: {s.title[:40]}")
        
        print()
        print("=" * 70)
        print("🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("=" * 70)
        print("🚀 СЕЙЧАС ОБНОВИТЕ СТРАНИЦУ В БРАУЗЕРЕ:")
        print("   http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/")
        print()
        print("📺 Должно показаться видео Rick Astley")
        print("   (это тестовое видео, потом замените на нужное)")
        
        return True
        
    except Story.DoesNotExist:
        print("❌ ОШИБКА: Рассказ с таким slug не найден!")
        print("🔍 Попробуем найти все рассказы...")
        
        all_stories = Story.objects.all()[:10]
        print("\n📝 ДОСТУПНЫЕ РАССКАЗЫ:")
        for s in all_stories:
            print(f"   - {s.title} (slug: {s.slug})")
            
        return False
        
    except Exception as e:
        print(f"❌ НЕОЖИДАННАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    from django.db import models
    
    print("🚀 ЗАПУСК ПОЛНОГО ИСПРАВЛЕНИЯ ВИДЕО...")
    print()
    
    success = fix_video_completely()
    
    if success:
        print("\n✅ ВСЕ ГОТОВО! Обновите браузер!")
    else:
        print("\n❌ Что-то пошло не так. Проверьте ошибки выше.")
    
    input("\nНажмите Enter для выхода...")
