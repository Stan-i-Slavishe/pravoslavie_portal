#!/usr/bin/env python
"""
Ручное исправление views.py для правильного отображения комментариев
"""

# Читаем исходный файл
with open('stories/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("🔧 Применяем точные исправления...")

# 1. Добавляем миксин перед первым классом
mixin_code = '''

# ==========================================
# БАЗОВЫЙ MIXIN ДЛЯ ПОДСЧЕТА КОММЕНТАРИЕВ  
# ==========================================

class StoryQuerysetMixin:
    """Миксин для добавления подсчета комментариев к queryset"""
    
    def get_base_queryset(self):
        """Возвращает базовый queryset с аннотациями"""
        return Story.objects.filter(is_published=True).select_related('category').prefetch_related('tags').annotate(
            # Подсчитываем только основные комментарии (не ответы)
            comments_count=Count('comments', filter=Q(comments__is_approved=True, comments__parent=None)),
            # Подсчитываем лайки
            likes_count=Count('likes', distinct=True)
        )

'''

# Вставляем миксин если его еще нет
if 'StoryQuerysetMixin' not in content:
    insert_pos = content.find('class StoryListView(ListView):')
    if insert_pos != -1:
        content = content[:insert_pos] + mixin_code + content[insert_pos:]
        print("✅ Добавлен StoryQuerysetMixin")

# 2. Обновляем StoryListView
content = content.replace(
    'class StoryListView(ListView):',
    'class StoryListView(StoryQuerysetMixin, ListView):'
)

# 3. Заменяем queryset в StoryListView
old_queryset = '''queryset = Story.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
        
        # Добавляем подсчет комментариев
        queryset = queryset.annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True, comments__parent=None))
        )'''

new_queryset = '''queryset = self.get_base_queryset()'''

content = content.replace(old_queryset, new_queryset)

# 4. Обновляем StoryCategoryView
content = content.replace(
    'class StoryCategoryView(ListView):',
    'class StoryCategoryView(StoryQuerysetMixin, ListView):'
)

old_category_queryset = '''return Story.objects.filter(
            is_published=True,
            category__slug=category_slug
        ).select_related('category').prefetch_related('tags').order_by('-created_at')'''

new_category_queryset = '''return self.get_base_queryset().filter(
            category__slug=category_slug
        ).order_by('-created_at')'''

content = content.replace(old_category_queryset, new_category_queryset)

# 5. Обновляем StoryTagView  
content = content.replace(
    'class StoryTagView(ListView):',
    'class StoryTagView(StoryQuerysetMixin, ListView):'
)

old_tag_queryset = '''return Story.objects.filter(
            is_published=True,
            tags__slug=tag_slug
        ).select_related('category').prefetch_related('tags').order_by('-created_at')'''

new_tag_queryset = '''return self.get_base_queryset().filter(
            tags__slug=tag_slug
        ).order_by('-created_at')'''

content = content.replace(old_tag_queryset, new_tag_queryset)

# 6. Обновляем PopularStoriesView
content = content.replace(
    'class PopularStoriesView(ListView):',
    'class PopularStoriesView(StoryQuerysetMixin, ListView):'
)

old_popular_queryset = '''return Story.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related('tags').order_by(
            '-views_count', '-created_at'
        )'''

new_popular_queryset = '''return self.get_base_queryset().order_by(
            '-views_count', '-created_at'
        )'''

content = content.replace(old_popular_queryset, new_popular_queryset)

# 7. Обновляем FeaturedStoriesView
content = content.replace(
    'class FeaturedStoriesView(ListView):',
    'class FeaturedStoriesView(StoryQuerysetMixin, ListView):'
)

old_featured_queryset = '''return Story.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('category').prefetch_related('tags').order_by('-created_at')'''

new_featured_queryset = '''return self.get_base_queryset().filter(
            is_featured=True
        ).order_by('-created_at')'''

content = content.replace(old_featured_queryset, new_featured_queryset)

# 8. Обновляем StorySearchView
content = content.replace(
    'class StorySearchView(ListView):',
    'class StorySearchView(StoryQuerysetMixin, ListView):'
)

old_search_queryset = '''return Story.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query),
            is_published=True
        ).select_related('category').prefetch_related('tags').distinct().order_by('-created_at')'''

new_search_queryset = '''return self.get_base_queryset().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('-created_at')'''

content = content.replace(old_search_queryset, new_search_queryset)

# Создаем резервную копию
import shutil
shutil.copy2('stories/views.py', 'stories/views_backup_manual.py')
print("✅ Создана резервная копия: stories/views_backup_manual.py")

# Сохраняем исправленный файл
with open('stories/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Файл stories/views.py обновлен")

# Проверяем синтаксис
try:
    import ast
    ast.parse(content)
    print("✅ Синтаксис Python корректен")
except SyntaxError as e:
    print(f"❌ Ошибка синтаксиса: {e}")
    # Восстанавливаем резервную копию
    shutil.copy2('stories/views_backup_manual.py', 'stories/views.py')
    print("✅ Резервная копия восстановлена")
    exit(1)

print()
print("🎉 ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ УСПЕШНО!")
print()
print("📋 Что изменилось:")
print("  ✓ Добавлен StoryQuerysetMixin")
print("  ✓ Все ListView теперь наследуют от StoryQuerysetMixin")
print("  ✓ Все views теперь правильно подсчитывают комментарии")
print("  ✓ Оптимизированы запросы к БД")
print()
print("🚀 Следующие шаги:")
print("  1. Запустите: python manage.py runserver")
print("  2. Откройте: http://127.0.0.1:8000/stories/")
print("  3. Проверьте отображение комментариев")
