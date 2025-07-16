#!/usr/bin/env python
"""
Проверка настроек пагинации на 9 постов
"""
import os
import sys
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_pagination_9():
    """Проверяем настройки пагинации на 9 постов"""
    
    print("🔍 Проверка пагинации на 9 постов...")
    print()
    
    # Импортируем views
    try:
        from stories.views import (
            StoryListView, 
            StoryCategoryView, 
            StoryTagView, 
            PopularStoriesView, 
            FeaturedStoriesView
        )
        
        views_to_check = [
            ('StoryListView', StoryListView),
            ('StoryCategoryView', StoryCategoryView), 
            ('StoryTagView', StoryTagView),
            ('PopularStoriesView', PopularStoriesView),
            ('FeaturedStoriesView', FeaturedStoriesView),
        ]
        
        all_correct = True
        
        for view_name, view_class in views_to_check:
            paginate_by = getattr(view_class, 'paginate_by', None)
            if paginate_by == 9:
                print(f"✅ {view_name}: paginate_by = {paginate_by}")
            else:
                print(f"❌ {view_name}: paginate_by = {paginate_by} (должно быть 9)")
                all_correct = False
        
        print()
        if all_correct:
            print("🎉 Все views настроены на 9 постов!")
        else:
            print("⚠️  Нужно исправить настройки views")
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Проверяем количество историй
    try:
        from stories.models import Story
        story_count = Story.objects.filter(is_published=True).count()
        print(f"📊 Опубликованных историй: {story_count}")
        
        if story_count >= 10:
            expected_pages = (story_count + 8) // 9  # Округление вверх для 9 на странице
            print(f"📄 Ожидается страниц: {expected_pages}")
            print("✅ Достаточно данных для проверки пагинации на 9 постов")
            print(f"🎯 На первой странице: 9 историй")
            if expected_pages > 1:
                remaining = story_count - 9
                print(f"🎯 На остальных страницах: {remaining} историй")
        else:
            print("⚠️  Недостаточно историй для полной проверки пагинации")
            print("   Но пагинация все равно будет работать")
            
    except Exception as e:
        print(f"❌ Ошибка при подсчете историй: {e}")
    
    print()
    print("🚀 Теперь на каждой странице будет показано по 9 историй!")
    print("   Обновите страницу: http://127.0.0.1:8000/stories/")
    
    return all_correct

if __name__ == '__main__':
    print("🎯 Проверка настроек пагинации на 9 постов...\n")
    success = check_pagination_9()
    print()
    if success:
        print("✅ Готово! Пагинация настроена на 9 постов.")
    else:
        print("🛠  Нужно исправить выявленные проблемы.")
