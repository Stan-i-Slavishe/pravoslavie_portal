from stories.models import Story

# Найдем наш рассказ
story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')

# Очистим YouTube данные чтобы показывалась наша красивая заглушка
story.youtube_embed_id = ''
story.youtube_url = ''
story.save()

print(f"✅ Установлена красивая заглушка для: {story.title}")
print("🎬 Теперь будет показываться сообщение 'Видео временно недоступно'")
