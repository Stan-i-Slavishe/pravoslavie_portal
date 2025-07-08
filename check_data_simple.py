import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from stories.models import Story

# Проверяем, есть ли рассказы
stories_count = Story.objects.count()
print(f"В базе данных найдено {stories_count} рассказов")

if stories_count > 0:
    # Показываем первые 5
    stories = Story.objects.all()[:5]
    for story in stories:
        print(f"- {story.title}")

# Проверяем пользователей
users_count = User.objects.count()
print(f"\nВ базе данных {users_count} пользователей")
