import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Ищем все рассказы с проблемным ID
stories = Story.objects.all()

print("=== ПОИСК ВСЕХ YOUTUBE ID ===")
for story in stories:
    if story.youtube_embed_id:
        print(f"Story: {story.title}")
        print(f"  Slug: {story.slug}")  
        print(f"  YouTube URL: {story.youtube_url}")
        print(f"  YouTube ID: {story.youtube_embed_id}")
        print("---")

# Специально проверяем наш рассказ
target_story = Story.objects.get(slug='pochti-pokojnik')
print(f"\n=== ЦЕЛЕВОЙ РАССКАЗ ===")
print(f"Title: {target_story.title}")
print(f"URL: {target_story.youtube_url}")
print(f"ID: '{target_story.youtube_embed_id}'")

# Принудительно меняем на правильный
if target_story.youtube_embed_id != 'SoKS2Aqh7zw':
    print(f"\n🔧 ИСПРАВЛЯЕМ ID с '{target_story.youtube_embed_id}' на 'SoKS2Aqh7zw'")
    target_story.youtube_embed_id = 'SoKS2Aqh7zw'
    target_story.save()
    print("✅ СОХРАНЕНО!")
else:
    print("✅ ID уже правильный!")

# Перепроверяем
target_story.refresh_from_db()
print(f"\nФИНАЛЬНАЯ ПРОВЕРКА:")
print(f"YouTube ID: '{target_story.youtube_embed_id}'")
print(f"Embed URL: {target_story.get_youtube_embed_url()}")
