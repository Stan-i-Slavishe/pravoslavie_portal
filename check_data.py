#!/usr/bin/env python
"""Проверка данных в базе"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story, StoryLike, StoryComment

def main():
    print("🔍 Проверка данных в базе...")
    
    try:
        # Проверяем рассказы
        stories = Story.objects.all()
        print(f"📚 Всего рассказов: {stories.count()}")
        
        if stories.exists():
            story = stories.first()
            print(f"📖 Первый рассказ: {story.title}")
            print(f"🔗 Slug: {story.slug}")
            print(f"🎬 YouTube ID: {story.youtube_embed_id}")
            print(f"👀 Просмотров: {story.views_count}")
        
        # Проверяем лайки
        likes = StoryLike.objects.all()
        print(f"❤️ Всего лайков: {likes.count()}")
        
        # Проверяем комментарии
        comments = StoryComment.objects.all()
        print(f"💬 Всего комментариев: {comments.count()}")
        
        print("\n✅ Проверка завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
