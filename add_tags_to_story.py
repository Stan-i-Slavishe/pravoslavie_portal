"""
Простой скрипт для добавления тегов к рассказам
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Tag as CoreTag
from stories.models import Story

def main():
    print("\n" + "=" * 70)
    print("ДОБАВЛЕНИЕ ТЕГОВ К РАССКАЗАМ")
    print("=" * 70)
    
    # Показываем доступные рассказы
    stories = Story.objects.all()[:10]
    
    print("\nДоступные рассказы:")
    for i, story in enumerate(stories, 1):
        tags = story.tags.all()
        tag_names = [t.name for t in tags]
        print(f"{i}. {story.title[:50]}... (теги: {', '.join(tag_names) if tag_names else 'нет'})")
    
    # Выбираем рассказ
    try:
        story_num = int(input("\nВыберите номер рассказа (1-10): "))
        selected_story = stories[story_num - 1]
    except (ValueError, IndexError):
        print("Неверный выбор!")
        return
    
    print(f"\nВыбран: {selected_story.title}")
    
    # Показываем доступные теги
    tags = CoreTag.objects.filter(is_active=True).order_by('name')
    
    print("\nДоступные теги:")
    for i, tag in enumerate(tags, 1):
        print(f"{i:2}. {tag.name}")
    
    # Выбираем теги
    tag_nums = input("\nВведите номера тегов через запятую (например: 1,3,5): ")
    
    try:
        tag_indices = [int(x.strip()) - 1 for x in tag_nums.split(',')]
        selected_tags = [tags[i] for i in tag_indices]
    except (ValueError, IndexError):
        print("Неверный выбор тегов!")
        return
    
    # Добавляем теги
    print("\nДобавление тегов...")
    for tag in selected_tags:
        selected_story.tags.add(tag)
        print(f"  ✅ Добавлен тег: {tag.name}")
    
    # Показываем результат
    print(f"\nТеги рассказа '{selected_story.title}':")
    for tag in selected_story.tags.all():
        print(f"  - {tag.name}")
    
    print("\n✅ Готово! Теперь проверьте в админке.")

if __name__ == '__main__':
    main()
