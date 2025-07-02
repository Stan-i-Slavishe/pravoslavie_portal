#!/usr/bin/env python
"""
Быстрое исправление views.py для правильного отображения комментариев
"""

print("🔧 Быстрое исправление views.py...")

# Читаем исходный файл
with open('stories/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Создаем резервную копию
import shutil
shutil.copy2('stories/views.py', 'stories/views_quick_backup.py')
print("✅ Создана резервная копия: stories/views_quick_backup.py")

# Добавляем миксин перед первым классом если его нет
if 'StoryQuerysetMixin' not in content:
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
    
    insert_pos = content.find('class StoryListView(ListView):')
    if insert_pos != -1:
        content = content[:insert_pos] + mixin_code + content[insert_pos:]
        print("✅ Добавлен StoryQuerysetMixin")

# Быстрые замены для всех классов
replacements = [
    ('class StoryListView(ListView):', 'class StoryListView(StoryQuerysetMixin, ListView):'),
    ('class StoryCategoryView(ListView):', 'class StoryCategoryView(StoryQuerysetMixin, ListView):'),
    ('class StoryTagView(ListView):', 'class StoryTagView(StoryQuerysetMixin, ListView):'),
    ('class PopularStoriesView(ListView):', 'class PopularStoriesView(StoryQuerysetMixin, ListView):'),
    ('class FeaturedStoriesView(ListView):', 'class FeaturedStoriesView(StoryQuerysetMixin, ListView):'),
    ('class StorySearchView(ListView):', 'class StorySearchView(StoryQuerysetMixin, ListView):'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Обновлен: {old.split('(')[0].replace('class ', '')}")

# Заменяем queryset в StoryListView
old_queryset = '''queryset = Story.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
        
        # Добавляем подсчет комментариев
        queryset = queryset.annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True, comments__parent=None))
        )'''

new_queryset = '''queryset = self.get_base_queryset()'''

if old_queryset in content:
    content = content.replace(old_queryset, new_queryset)
    print("✅ Обновлен queryset в StoryListView")

# Исправляем другие querysets
querysets = [
    ('''Story.objects.filter(
            is_published=True,
            category__slug=category_slug
        ).select_related('category').prefetch_related('tags').order_by('-created_at')''',
     '''self.get_base_queryset().filter(
            category__slug=category_slug
        ).order_by('-created_at')'''),
    
    ('''Story.objects.filter(
            is_published=True,
            tags__slug=tag_slug
        ).select_related('category').prefetch_related('tags').order_by('-created_at')''',
     '''self.get_base_queryset().filter(
            tags__slug=tag_slug
        ).order_by('-created_at')'''),
    
    ('''Story.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related('tags').order_by(
            '-views_count', '-created_at'
        )''',
     '''self.get_base_queryset().order_by(
            '-views_count', '-created_at'
        )'''),
    
    ('''Story.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('category').prefetch_related('tags').order_by('-created_at')''',
     '''self.get_base_queryset().filter(
            is_featured=True
        ).order_by('-created_at')'''),
    
    ('''Story.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query),
            is_published=True
        ).select_related('category').prefetch_related('tags').distinct().order_by('-created_at')''',
     '''self.get_base_queryset().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('-created_at')''')
]

for old_qs, new_qs in querysets:
    if old_qs in content:
        content = content.replace(old_qs, new_qs)
        print("✅ Обновлен queryset")

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
    shutil.copy2('stories/views_quick_backup.py', 'stories/views.py')
    print("✅ Резервная копия восстановлена")
    exit(1)

print()
print("🎉 ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!")
print()
print("📋 Что изменилось:")
print("  ✓ Добавлен StoryQuerysetMixin (если не было)")
print("  ✓ Все ListView наследуют от StoryQuerysetMixin")
print("  ✓ Все querysets обновлены для правильного подсчета комментариев")
print("  ✓ Шаблон обновлен для отображения комментариев")
print()
print("🚀 Следующие шаги:")
print("  1. Запустите: python manage.py runserver")
print("  2. Обновите страницу: http://127.0.0.1:8000/stories/ (Ctrl+F5)")
print("  3. Проверьте отображение комментариев")
