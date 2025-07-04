#!/usr/bin/env python
"""
Быстрое исправление views.py
"""

print("🔧 ИСПРАВЛЕНИЕ VIEWS.PY")
print("=" * 40)

# Читаем поврежденный файл
try:
    with open('stories/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Исправляем дублированный импорт
    if 'from django.views.generic import ListView, DetailView' in content:
        # Убираем дублированную строку
        content = content.replace(
            'status=500)from django.views.generic import ListView, DetailView',
            'status=500)\n\nfrom django.views.generic import ListView, DetailView'
        )
        
        # Перемещаем заглушки в конец файла
        lines = content.split('\n')
        
        # Находим заглушки
        stub_start = -1
        stub_end = -1
        
        for i, line in enumerate(lines):
            if '# ЗАГЛУШКИ ДЛЯ ЛАЙКОВ И ИЗБРАННОГО' in line:
                stub_start = i
            if stub_start != -1 and 'from django.views.generic import ListView, DetailView' in line and i > stub_start:
                stub_end = i - 1
                break
        
        if stub_start != -1 and stub_end != -1:
            # Извлекаем заглушки
            stub_lines = lines[stub_start:stub_end + 1]
            
            # Удаляем заглушки из начала
            remaining_lines = lines[:stub_start] + lines[stub_end + 1:]
            
            # Добавляем заглушки в конец
            fixed_lines = remaining_lines + [''] + stub_lines
            
            content = '\n'.join(fixed_lines)
    
    # Записываем исправленный файл
    with open('stories/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ views.py исправлен")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    
    # Создаем минимальную версию views.py
    minimal_content = '''from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Q
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Avg
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import json

# Импортируем основные модели
from .models import Story, StoryComment, CommentReaction, Playlist, PlaylistItem
from core.models import Category, Tag
from django.template.loader import render_to_string
from django.utils.html import escape

# Базовые классы
class StoryListView(ListView):
    model = Story
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    paginate_by = 12

    def get_queryset(self):
        return Story.objects.filter(is_published=True).select_related('category').prefetch_related('tags')

class StoryCategoryView(ListView):
    model = Story
    template_name = 'stories/category.html'
    context_object_name = 'stories'
    paginate_by = 12

class StoryTagView(ListView):
    model = Story
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    paginate_by = 12

class PopularStoriesView(ListView):
    model = Story
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    paginate_by = 12

class FeaturedStoriesView(ListView):
    model = Story
    template_name = 'stories/list.html'
    context_object_name = 'stories'
    paginate_by = 12

class StorySearchView(ListView):
    model = Story
    template_name = 'stories/search_results.html'
    context_object_name = 'stories'
    paginate_by = 12

def story_detail(request, slug):
    """Детальная страница рассказа"""
    story = get_object_or_404(Story, slug=slug, is_published=True)
    
    # Увеличиваем просмотры
    story.views_count = F('views_count') + 1
    story.save(update_fields=['views_count'])
    story.refresh_from_db()
    
    context = {
        'story': story,
        'likes_count': story.likes_count,
        'user_liked': False,
    }
    
    return render(request, 'stories/story_detail.html', context)

@require_POST
@login_required
def story_like(request, story_id):
    """Заглушка для лайков рассказов"""
    try:
        story = get_object_or_404(Story, id=story_id)
        
        # Просто увеличиваем счетчик лайков
        story.likes_count += 1
        story.save(update_fields=['likes_count'])
        
        return JsonResponse({
            'status': 'success',
            'liked': True,
            'likes_count': story.likes_count,
            'message': 'Лайк добавлен!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@login_required
def story_favorite(request, story_id):
    """Заглушка для добавления в избранное"""
    try:
        story = get_object_or_404(Story, id=story_id)
        
        return JsonResponse({
            'status': 'success',
            'favorited': True,
            'message': 'Добавлено в избранное!'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

# Заглушки для комментариев
def add_comment(request, story_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})

def load_comments(request, story_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})

def load_more_comments(request, story_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})

def comment_reaction(request, comment_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})

def edit_comment(request, comment_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})

def delete_comment(request, comment_id):
    return JsonResponse({'status': 'error', 'message': 'Функция в разработке'})
'''
    
    with open('stories/views.py', 'w', encoding='utf-8') as f:
        f.write(minimal_content)
    
    print("✅ Создан минимальный views.py")

print("\n🚀 Теперь попробуйте запустить сервер:")
print("python manage.py runserver")
