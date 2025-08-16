import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Тестовые YouTube видео, которые точно разрешают встраивание
test_videos = [
    'dQw4w9WgXcQ',  # Rick Roll - классика, всегда работает
    'jNQXAC9IVRw',  # Me at the zoo - первое видео на YouTube
    'ZZ5LpwO-An4',  # HEYYEYAAEYAAAEYAEYAA
    'kffacxfA7G4',  # Baby Shark - популярное
    '9bZkp7q19f0',  # PSY - Gangnam Style
]

print("=== УСТАНОВКА ТЕСТОВЫХ ВИДЕО ===")

# Получаем все рассказы
stories = Story.objects.all()[:len(test_videos)]

for i, story in enumerate(stories):
    if i < len(test_videos):
        old_id = story.youtube_embed_id
        new_id = test_videos[i]
        
        print(f"\n📹 {story.title}")
        print(f"   Старый ID: {old_id}")
        print(f"   Новый ID:  {new_id}")
        
        story.youtube_embed_id = new_id
        story.youtube_url = f'https://youtu.be/{new_id}'
        story.save()
        
        print(f"   ✅ Обновлено!")

print(f"\n🎬 Тестовые видео установлены!")
print(f"📍 Проверьте любой рассказ - видео должно заработать!")
print(f"🔗 Например: http://127.0.0.1:8000/stories/dva-syna/")
