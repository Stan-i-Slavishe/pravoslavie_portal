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
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    
    print("=" * 70)
    print("🔧 БЫСТРОЕ ИСПРАВЛЕНИЕ - ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА")
    print("=" * 70)
    
    print(f"✅ ID рассказа: {story.id}")
    print(f"✅ Slug: {story.slug}")
    print(f"✅ YouTube ID: '{story.youtube_embed_id}'")
    print(f"✅ YouTube URL: '{story.youtube_url}'")
    print()
    
    # Проверяем что поле точно не пустое
    if story.youtube_embed_id and story.youtube_embed_id.strip():
        print("✅ youtube_embed_id НЕ ПУСТОЕ")
        print(f"   Длина: {len(story.youtube_embed_id)}")
        print(f"   Содержимое: '{story.youtube_embed_id}'")
        print(f"   Тип: {type(story.youtube_embed_id)}")
    else:
        print("❌ youtube_embed_id ПУСТОЕ или None")
    
    # Дополнительная проверка
    print("\n🔍 ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ:")
    print(f"bool(story.youtube_embed_id): {bool(story.youtube_embed_id)}")
    print(f"story.youtube_embed_id == 'dQw4w9WgXcQ': {story.youtube_embed_id == 'dQw4w9WgXcQ'}")
    print(f"len(story.youtube_embed_id): {len(story.youtube_embed_id) if story.youtube_embed_id else 0}")
    
    # Проверяем другие рассказы
    print("\n📋 ПРОВЕРКА ДРУГИХ РАССКАЗОВ:")
    print("-" * 50)
    
    other_stories = Story.objects.filter(is_published=True)[:5]
    for s in other_stories:
        has_video = "✅" if s.youtube_embed_id else "❌"
        print(f"{has_video} {s.title[:40]:40} | ID: {s.youtube_embed_id or 'ПУСТО'}")
    
    print("\n" + "=" * 70)
    print("🎯 РЕКОМЕНДАЦИЯ:")
    print("=" * 70)
    print("1. Откройте страницу рассказа в браузере:")
    print("   http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/")
    print()
    print("2. Откройте DevTools (F12) -> Console")
    print("3. Проверьте есть ли JavaScript ошибки")
    print("4. Во вкладке Elements найдите div.video-container")
    print("5. Проверьте что внутри - iframe или video-placeholder")
    print()
    print("Если проблема не в JavaScript, то это может быть:")
    print("- Кеширование браузера (Ctrl+F5)")
    print("- CSS скрывает видео")
    print("- Проблема с CORS или блокировкой YouTube")

except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

input("\nНажмите Enter для выхода...")
