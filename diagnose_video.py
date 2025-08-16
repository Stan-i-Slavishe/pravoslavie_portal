import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Проверяем текущее состояние
story = Story.objects.get(slug='pochti-pokojnik')

print("=== ДИАГНОСТИКА ПРОБЛЕМЫ ===")
print(f"Title: {story.title}")
print(f"YouTube URL: '{story.youtube_url}'")
print(f"YouTube ID: '{story.youtube_embed_id}'")
print(f"YouTube ID длина: {len(story.youtube_embed_id) if story.youtube_embed_id else 'None'}")
print(f"YouTube ID bool: {bool(story.youtube_embed_id)}")

# Принудительно устанавливаем правильный ID
correct_id = 'SoKS2Aqh7zw'
print(f"\nУстанавливаем ID: '{correct_id}'")

story.youtube_embed_id = correct_id
story.save()

# Проверяем после сохранения
story.refresh_from_db()
print(f"\nПосле сохранения:")
print(f"YouTube ID: '{story.youtube_embed_id}'")
print(f"YouTube ID bool: {bool(story.youtube_embed_id)}")

# Проверяем метод из модели
print(f"\nМетоды модели:")
print(f"get_youtube_embed_url(): {story.get_youtube_embed_url()}")
print(f"get_youtube_thumbnail_url(): {story.get_youtube_thumbnail_url()}")

print("\n✅ Данные исправлены! Обновите страницу в браузере.")
