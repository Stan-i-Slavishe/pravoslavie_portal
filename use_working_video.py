import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

print("=== РАБОЧИЕ YOUTUBE ВИДЕО ===")

# Берем ID из похожих рассказов, которые работают
working_stories = [
    ('kak-svyatoj-luka-doch-spas', '5okS2Aqh7zw'),
    ('dva-syna', 'd0dxRY9kKhQ'), 
    ('vanechka', 'Rd81hFKh2BM')
]

target_story = Story.objects.get(slug='pochti-pokojnik')
print(f"Целевой рассказ: {target_story.title}")
print(f"Текущий YouTube ID: {target_story.youtube_embed_id}")

# Попробуем первый рабочий ID
new_id = '5okS2Aqh7zw'  # из "Как святой Лука дочь спас"
print(f"\nПробуем ID от рассказа 'Как святой Лука дочь спас': {new_id}")

target_story.youtube_embed_id = new_id
target_story.youtube_url = f'https://youtu.be/{new_id}'
target_story.save()

print(f"✅ Установлен новый YouTube ID: {new_id}")
print(f"✅ Новый YouTube URL: {target_story.youtube_url}")
print(f"✅ Embed URL: {target_story.get_youtube_embed_url()}")

print("\n🎬 Теперь обновите страницу - видео должно заработать!")
