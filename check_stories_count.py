#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from stories.models import Story

# Проверяем количество рассказов
total_stories = Story.objects.filter(is_published=True).count()
all_stories = Story.objects.all().count()

print(f"Всего рассказов в базе: {all_stories}")
print(f"Опубликованных рассказов: {total_stories}")

if total_stories <= 6:
    print("\n⚠️  ПРОБЛЕМА: Рассказов меньше чем paginate_by=6")
    print("Пагинатор появляется только когда постов больше, чем на одной странице")
    print("\nРешения:")
    print("1. Добавить больше рассказов в базу")
    print("2. Временно уменьшить paginate_by до 2-3 для тестирования")
    
    # Покажем существующие рассказы
    stories = Story.objects.filter(is_published=True)
    print(f"\nСуществующие опубликованные рассказы:")
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story.title} (опубликован: {story.is_published})")
else:
    print(f"\n✅ Рассказов достаточно для пагинации: {total_stories}")
