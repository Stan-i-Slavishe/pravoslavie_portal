from stories.models import Story

# Находим рассказ
story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')

# Добавляем тестовое видео
story.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
story.youtube_embed_id = "dQw4w9WgXcQ"
story.save()

print("Видео исправлено!")
