#!/usr/bin/env python
"""
Исправление всех ссылок на StoryLike в views.py
"""

print("🔧 ИСПРАВЛЕНИЕ ССЫЛОК НА StoryLike")
print("=" * 40)

try:
    # Читаем файл
    with open('stories/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Список замен
    replacements = [
        # Основные замены
        ('StoryLike.objects.filter(', '# StoryLike.objects.filter('),
        ('story.likes.count()', 'story.likes_count'),
        
        # Исправляем функцию story_detail
        ('user_liked = StoryLike.objects.filter(\n            story=story, \n            user=request.user\n        ).exists()', 'user_liked = False  # StoryLike модель удалена'),
        
        # Исправляем другие обращения
        ('StoryLike.objects.get_or_create(', '# StoryLike.objects.get_or_create('),
        
        # Исправляем импорт если есть
        (', StoryLike', ''),
        ('from .models import Story, StoryLike,', 'from .models import Story,'),
    ]
    
    # Применяем замены
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Заменено: {old[:30]}...")
    
    # Записываем исправленный файл
    with open('stories/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ views.py исправлен")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n🚀 Попробуйте запустить сервер:")
print("python manage.py runserver")
