import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Находим рассказ "Почти покойник"
story = Story.objects.get(slug='pochti-pokojnik')

print(f"Рассказ: {story.title}")
print(f"YouTube URL: {story.youtube_url}")
print(f"YouTube ID: {story.youtube_embed_id}")

# Если YouTube ID пустое, но URL есть - извлекаем ID
if story.youtube_url and not story.youtube_embed_id:
    print("\nИзвлекаем YouTube ID из URL...")
    # Вызываем метод из модели для извлечения ID
    youtube_id = story.extract_youtube_id(story.youtube_url)
    print(f"Извлеченный ID: {youtube_id}")
    
    if youtube_id:
        story.youtube_embed_id = youtube_id
        story.save()
        print("✅ YouTube ID сохранен!")
    else:
        print("❌ Не удалось извлечь YouTube ID")

print(f"\nИтоговый YouTube ID: {story.youtube_embed_id}")
