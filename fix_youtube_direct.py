import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Находим и исправляем рассказ
story = Story.objects.get(slug='pochti-pokojnik')

print(f"Рассказ: {story.title}")
print(f"YouTube URL: {story.youtube_url}")
print(f"YouTube ID ДО: '{story.youtube_embed_id}'")

# В HTML видно YouTube ID: WMZ5b1cXxRc (из schema.org)
# А должен быть: SoKS2Aqh7zw (из админки)

# Исправляем ID прямо сейчас
story.youtube_embed_id = 'SoKS2Aqh7zw'
story.save()

print(f"YouTube ID ПОСЛЕ: '{story.youtube_embed_id}'")
print("✅ ИСПРАВЛЕНО! Теперь видео должно работать!")
