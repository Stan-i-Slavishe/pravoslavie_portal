#!/usr/bin/env python
"""
Быстрая проверка настроек пагинации
"""
import os
import sys
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_pagination_settings():
    """Проверяем настройки пагинации в views"""
    
    print("🔍 Проверка настроек пагинации...")
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
            if paginate_by == 6:
                print(f"✅ {view_name}: paginate_by = {paginate_by}")
            else:
                print(f"❌ {view_name}: paginate_by = {paginate_by} (должно быть 6)")
                all_correct = False
        
        print()
        if all_correct:
            print("🎉 Все views настроены правильно!")
        else:
            print("⚠️  Нужно исправить настройки views")
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    # Проверяем наличие шаблона пагинации
    pagination_template = 'templates/includes/pagination.html'
    if os.path.exists(pagination_template):
        print(f"✅ Шаблон пагинации существует: {pagination_template}")
    else:
        print(f"❌ Шаблон пагинации НЕ найден: {pagination_template}")
        all_correct = False
    
    # Проверяем количество историй
    try:
        from stories.models import Story
        story_count = Story.objects.filter(is_published=True).count()
        print(f"📊 Опубликованных историй: {story_count}")
        
        if story_count >= 7:
            expected_pages = (story_count + 5) // 6  # Округление вверх
            print(f"📄 Ожидается страниц: {expected_pages}")
            print("✅ Достаточно данных для проверки пагинации")
        else:
            print("⚠️  Недостаточно историй для проверки пагинации")
            print("   Запустите: python create_pagination_test_data.py")
            
    except Exception as e:
        print(f"❌ Ошибка при подсчете историй: {e}")
    
    return all_correct

if __name__ == '__main__':
    print("🚀 Проверка настроек пагинации...\n")
    success = check_pagination_settings()
    print()
    if success:
        print("🎯 Все готово! Можете тестировать пагинацию.")
        print("   Запустите: python manage.py runserver")
        print("   Перейдите: http://127.0.0.1:8000/stories/")
    else:
        print("🛠  Нужно исправить выявленные проблемы.")
