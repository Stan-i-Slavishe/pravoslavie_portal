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
    # Ищем рассказ
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    
    print("=" * 70)
    print(f"🔍 ДИАГНОСТИКА РАССКАЗА: {story.title}")
    print("=" * 70)
    
    # Проверяем ВСЕ поля
    print(f"ID: {story.id}")
    print(f"Slug: {story.slug}")
    print(f"Опубликован: {story.is_published}")
    print(f"YouTube URL: '{story.youtube_url}'")
    print(f"YouTube Embed ID: '{story.youtube_embed_id}'")
    print()
    
    # Проверяем методы модели
    print("🔧 ПРОВЕРКА МЕТОДОВ МОДЕЛИ:")
    print("-" * 40)
    
    try:
        embed_url = story.get_youtube_embed_url()
        print(f"get_youtube_embed_url(): {embed_url}")
    except Exception as e:
        print(f"get_youtube_embed_url(): ОШИБКА - {e}")
    
    try:
        thumbnail_url = story.get_youtube_thumbnail_url()
        print(f"get_youtube_thumbnail_url(): {thumbnail_url}")
    except Exception as e:
        print(f"get_youtube_thumbnail_url(): ОШИБКА - {e}")
    
    print()
    
    # Проверяем свойства
    print("📋 ПРОВЕРКА СВОЙСТВ:")
    print("-" * 40)
    
    for attr in ['youtube_id', 'video_url']:
        if hasattr(story, attr):
            value = getattr(story, attr)
            print(f"{attr}: '{value}'")
        else:
            print(f"{attr}: НЕ НАЙДЕНО")
    
    print()
    
    # Симулируем то, что происходит в шаблоне
    print("🎭 СИМУЛЯЦИЯ ШАБЛОНА:")
    print("-" * 40)
    
    if story.youtube_embed_id:
        print(f"✅ story.youtube_embed_id ИСТИНА: '{story.youtube_embed_id}'")
        print(f"📺 Embed URL: https://www.youtube.com/embed/{story.youtube_embed_id}")
    else:
        print(f"❌ story.youtube_embed_id ЛОЖЬ: '{story.youtube_embed_id}'")
        print("🔍 Тип данных:", type(story.youtube_embed_id))
        print("🔍 Длина строки:", len(str(story.youtube_embed_id)) if story.youtube_embed_id else 0)
    
    print()
    
    # Проверяем другие возможные поля
    print("🔎 ПОИСК ДРУГИХ YOUTUBE ПОЛЕЙ:")
    print("-" * 40)
    
    for field in story._meta.fields:
        field_name = field.name
        if 'youtube' in field_name.lower() or 'video' in field_name.lower() or 'embed' in field_name.lower():
            value = getattr(story, field_name)
            print(f"📹 {field_name}: '{value}' (тип: {type(value).__name__})")
    
    print()
    print("=" * 70)
    print("🎯 РЕКОМЕНДАЦИИ:")
    print("=" * 70)
    
    if story.youtube_embed_id:
        print("✅ Данные в базе ПРАВИЛЬНЫЕ")
        print("❌ Проблема в ШАБЛОНЕ или VIEW")
        print("🔧 Нужно проверить:")
        print("   1. Правильный ли шаблон используется")
        print("   2. Передается ли story в контекст")
        print("   3. Нет ли ошибок в условиях шаблона")
    else:
        print("❌ Данные в базе НЕПРАВИЛЬНЫЕ")
        print("🔧 Нужно исправить youtube_embed_id")
    
except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

input("\nНажмите Enter для продолжения...")
