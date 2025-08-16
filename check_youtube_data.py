#!/usr/bin/env python3
"""
Проверка YouTube данных в рассказах
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

def check_youtube_data():
    """Проверяем YouTube данные в рассказах"""
    
    print("🎬 Проверка YouTube данных в рассказах")
    print("=" * 50)
    
    stories = Story.objects.all()
    
    for story in stories:
        print(f"\n📖 Рассказ: {story.title}")
        print(f"   ID: {story.id}")
        print(f"   Slug: {story.slug}")
        print(f"   YouTube URL: {story.youtube_url}")
        print(f"   YouTube ID: {story.youtube_embed_id}")
        
        # Проверяем методы модели
        try:
            embed_url = story.get_youtube_embed_url()
            print(f"   Embed URL: {embed_url}")
        except Exception as e:
            print(f"   ❌ Ошибка get_youtube_embed_url(): {e}")
        
        try:
            thumbnail_url = story.get_youtube_thumbnail_url()
            print(f"   Thumbnail URL: {thumbnail_url}")
        except Exception as e:
            print(f"   ❌ Ошибка get_youtube_thumbnail_url(): {e}")
        
        print(f"   Опубликован: {story.is_published}")
        print("-" * 40)
    
    # Проверяем конкретный рассказ из ошибки
    print(f"\n🔍 Детальная проверка рассказа 'kak-svyatoj-luka-doch-spas'")
    try:
        story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
        print(f"✅ Рассказ найден: {story.title}")
        print(f"   YouTube URL: '{story.youtube_url}'")
        print(f"   YouTube ID: '{story.youtube_embed_id}'")
        print(f"   Пуст ли ID: {not story.youtube_embed_id}")
        print(f"   Длина ID: {len(story.youtube_embed_id) if story.youtube_embed_id else 0}")
        
        # Тестируем логику шаблона
        if story.youtube_embed_id:
            print(f"   ✅ Условие {% if story.youtube_embed_id %} = True")
            embed_url = f"https://www.youtube.com/embed/{story.youtube_embed_id}"
            print(f"   🎬 Embed URL: {embed_url}")
        else:
            print(f"   ❌ Условие {% if story.youtube_embed_id %} = False")
            print(f"   ⚠️  Видео не будет отображаться!")
            
    except Story.DoesNotExist:
        print(f"❌ Рассказ 'kak-svyatoj-luka-doch-spas' не найден!")
    
    print(f"\n📊 Общая статистика:")
    total_stories = stories.count()
    stories_with_youtube = stories.exclude(youtube_embed_id='').count()
    stories_with_url = stories.exclude(youtube_url='').count()
    
    print(f"   Всего рассказов: {total_stories}")
    print(f"   С YouTube ID: {stories_with_youtube}")
    print(f"   С YouTube URL: {stories_with_url}")

if __name__ == "__main__":
    try:
        check_youtube_data()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
