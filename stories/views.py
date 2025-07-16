from django.views.generic import ListView, DetailView
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
from .models import Story, StoryLike, StoryComment, CommentReaction
from core.models import Category, Tag
from django.template.loader import render_to_string
from django.utils.html import escape



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

class StoryListView(StoryQuerysetMixin, ListView):
    """Список всех видео-рассказов"""
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = self.get_base_queryset()
        
        # Добавляем подсчет комментариев
        queryset = queryset.annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True, comments__parent=None))
        )
        
        # Поиск
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Фильтр по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Фильтр по тегу
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Сортировка
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by == 'popular':
            queryset = queryset.order_by('-views_count', '-created_at')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Видео-рассказы'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['featured_stories'] = Story.objects.filter(
            is_published=True, 
            is_featured=True
        )[:3]
        
        # Передаем параметры поиска и фильтрации в контекст
        context['search_query'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        return context


class StoryDetailView(DetailView):
    """Детальная страница видео-рассказа"""
    model = Story
    template_name = 'stories/story_detail.html'
    context_object_name = 'story'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Story.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
    
    def get_object(self, queryset=None):
        # Получаем объект без увеличения счетчика
        obj = super().get_object(queryset)
        
        # Увеличиваем счетчик только один раз за сессию
        session_key = f'viewed_story_{obj.id}'
        if not self.request.session.get(session_key, False):
            obj.increment_views()
            self.request.session[session_key] = True
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        story = self.get_object()
        
        # Похожие рассказы (по категории и тегам)
        related_stories = Story.objects.filter(
            is_published=True
        ).exclude(
            id=story.id
        ).select_related('category')
        
        if story.category:
            related_stories = related_stories.filter(category=story.category)
        
        context['related_stories'] = related_stories[:3]
        
        # Проверяем, лайкнул ли пользователь этот рассказ
        try:
            if self.request.user.is_authenticated:
                context['user_liked'] = StoryLike.objects.filter(
                    story=story, 
                    user=self.request.user
                ).exists()
            else:
                context['user_liked'] = False
            
            # Общее количество лайков
            context['likes_count'] = story.likes.count()
        except Exception:
            # Если модель лайков еще не создана
            context['user_liked'] = False
            context['likes_count'] = 0
        
        # Добавляем комментарии
        try:
            # Получаем основные комментарии (не ответы) 
            comments = StoryComment.objects.filter(
                story=story,
                parent=None,
                is_approved=True
            ).select_related('user').prefetch_related('replies').order_by('-is_pinned', '-created_at')[:5]
            
            context['comments'] = comments
            # ИСПРАВЛЕНИЕ: Правильный подсчет только основных комментариев (не ответы)
            context['comments_count'] = StoryComment.objects.filter(
                story=story, 
                parent=None,  # Только основные комментарии
                is_approved=True
            ).count()
            
            # Получаем реакции пользователя на комментарии
            if self.request.user.is_authenticated:
                user_reactions = CommentReaction.objects.filter(
                    comment__story=story,
                    user=self.request.user
                ).values('comment_id', 'reaction_type')
                context['user_reactions'] = {r['comment_id']: r['reaction_type'] for r in user_reactions}
            else:
                context['user_reactions'] = {}
                
        except Exception as e:
            # Если модели комментариев еще не созданы
            context['comments'] = []
            context['comments_count'] = 0
            context['user_reactions'] = {}
        
        # Добавляем плейлисты пользователя для сайдбара
        if self.request.user.is_authenticated:
            try:
                # Импортируем модель Playlist
                from .models import Playlist
                
                # Получаем плейлисты пользователя (ограничиваем до 5 для сайдбара)
                user_playlists = Playlist.objects.filter(
                    creator=self.request.user
                ).annotate(
                    calculated_stories_count=Count('playlist_items')
                ).order_by('-created_at')[:5]
                
                context['user_playlists'] = user_playlists
                
            except Exception as e:
                # Если модели плейлистов еще не созданы или есть ошибка
                context['user_playlists'] = []
        else:
            context['user_playlists'] = []
        
        return context


@require_POST
@login_required
def story_like(request, story_id):
    """Лайк/дизлайк рассказа"""
    try:
        story = get_object_or_404(Story, id=story_id, is_published=True)
        like, created = StoryLike.objects.get_or_create(
            story=story,
            user=request.user
        )
        
        if not created:
            # Если лайк уже есть, удаляем его (дизлайк)
            like.delete()
            liked = False
        else:
            liked = True
        
        likes_count = story.likes.count()
        
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes_count': likes_count
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_POST
@csrf_exempt
def story_view_count(request, story_id):
    """Увеличение счетчика просмотров"""
    try:
        story = get_object_or_404(Story, id=story_id, is_published=True)
        story.increment_views()
        return JsonResponse({
            'status': 'success', 
            'views': story.views_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=400)


class StoryCategoryView(StoryQuerysetMixin, ListView):
    """Рассказы по категории"""
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    paginate_by = 9
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return self.get_base_queryset().filter(
            category__slug=category_slug
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        try:
            category = Category.objects.get(slug=category_slug)
            context['title'] = f'Рассказы: {category.name}'
            context['current_category'] = category
        except Category.DoesNotExist:
            context['title'] = 'Категория не найдена'
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class StoryTagView(StoryQuerysetMixin, ListView):
    """Рассказы по тегу"""
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    paginate_by = 9
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return self.get_base_queryset().filter(
            tags__slug=tag_slug
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        try:
            tag = Tag.objects.get(slug=tag_slug)
            context['title'] = f'Рассказы по тегу: {tag.name}'
            context['current_tag'] = tag
        except Tag.DoesNotExist:
            context['title'] = 'Тег не найден'
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class PopularStoriesView(StoryQuerysetMixin, ListView):
    """Популярные рассказы"""
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    paginate_by = 9
    
    def get_queryset(self):
        return self.get_base_queryset().order_by(
            '-views_count', '-created_at'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Популярные рассказы'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class FeaturedStoriesView(StoryQuerysetMixin, ListView):
    """Рекомендуемые рассказы"""
    model = Story
    template_name = 'stories/story_list.html'
    context_object_name = 'stories'
    paginate_by = 9
    
    def get_queryset(self):
        return self.get_base_queryset().filter(
            is_featured=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рекомендуемые рассказы'
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class StorySearchView(StoryQuerysetMixin, ListView):
    """Поиск по рассказам с расширенными возможностями"""
    model = Story
    template_name = 'stories/search_results.html'
    context_object_name = 'stories'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Story.objects.none()
        
        return self.get_base_queryset().filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['title'] = f"Результаты поиска: {context['search_query']}"
        return context


def story_favorite(request, story_id):
    """Заглушка для избранного"""
    return JsonResponse({
        'status': 'info',
        'message': 'Функция "Избранное" будет добавлена в будущих обновлениях'
    })


# ==========================================
# СИСТЕМА КОММЕНТАРИЕВ YouTube-style
# ==========================================

@require_POST
@login_required
def add_comment(request, story_id):
    """Добавление нового комментария"""
    try:
        story = get_object_or_404(Story, id=story_id, is_published=True)
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if not text:
            return JsonResponse({
                'status': 'error',
                'message': 'Комментарий не может быть пустым'
            }, status=400)
        
        if len(text) > 1000:
            return JsonResponse({
                'status': 'error',
                'message': 'Комментарий слишком длинный (максимум 1000 символов)'
            }, status=400)
        
        # Создаем комментарий
        comment = StoryComment.objects.create(
            story=story,
            user=request.user,
            text=text,
            parent_id=parent_id if parent_id else None
        )
        
        # Формируем ответ
        comment_html = render_to_string('stories/comment_item.html', {
            'comment': comment,
            'user': request.user
        })
        
        return JsonResponse({
            'status': 'success',
            'message': 'Комментарий добавлен',
            'comment_html': comment_html,
            'comment_id': comment.id,
            'parent_id': comment.parent_id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при добавлении комментария: {str(e)}'
        }, status=500)


@require_POST
@login_required  
def comment_reaction(request, comment_id):
    """Лайк/дизлайк комментария"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id)
        reaction_type = request.POST.get('type')  # 'like' или 'dislike'
        
        if reaction_type not in ['like', 'dislike']:
            return JsonResponse({
                'status': 'error',
                'message': 'Неверный тип реакции'
            }, status=400)
        
        # Проверяем, есть ли уже реакция от этого пользователя
        existing_reaction = CommentReaction.objects.filter(
            comment=comment,
            user=request.user
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Убираем реакцию (повторный клик)
                existing_reaction.delete()
                user_reaction = None
            else:
                # Меняем тип реакции
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                user_reaction = reaction_type
        else:
            # Создаем новую реакцию
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction_type=reaction_type
            )
            user_reaction = reaction_type
        
        # Обновляем данные комментария
        comment.refresh_from_db()
        
        return JsonResponse({
            'status': 'success',
            'likes_count': comment.likes_count,
            'dislikes_count': comment.dislikes_count,
            'user_reaction': user_reaction
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_POST
@login_required
def edit_comment(request, comment_id):
    """Редактирование комментария"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id, user=request.user)
        new_text = request.POST.get('text', '').strip()
        
        if not new_text:
            return JsonResponse({
                'status': 'error',
                'message': 'Комментарий не может быть пустым'
            }, status=400)
        
        if len(new_text) > 1000:
            return JsonResponse({
                'status': 'error',
                'message': 'Комментарий слишком длинный (максимум 1000 символов)'
            }, status=400)
        
        comment.text = new_text
        comment.is_edited = True
        comment.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Комментарий обновлен',
            'new_text': comment.text
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_POST
@login_required
def delete_comment(request, comment_id):
    """Удаление комментария"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id)
        
        # Проверяем права на удаление
        if comment.user != request.user and not request.user.is_staff:
            return JsonResponse({
                'status': 'error',
                'message': 'Нет прав для удаления этого комментария'
            }, status=403)
        
        comment.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Комментарий удален'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def load_comments(request, story_id):
    """Загрузка комментариев для рассказа"""
    try:
        story = get_object_or_404(Story, id=story_id, is_published=True)
        page = int(request.GET.get('page', 1))
        per_page = 10
        
        # Получаем основные комментарии (не ответы)
        comments = StoryComment.objects.filter(
            story=story,
            parent=None,
            is_approved=True
        ).select_related('user').prefetch_related('replies').order_by('-is_pinned', '-created_at')
        
        paginator = Paginator(comments, per_page)
        page_obj = paginator.get_page(page)
        
        # Получаем реакции пользователя если он авторизован
        user_reactions = {}
        if request.user.is_authenticated:
            reactions = CommentReaction.objects.filter(
                comment__in=[c.id for c in page_obj.object_list],
                user=request.user
            ).values('comment_id', 'reaction_type')
            user_reactions = {r['comment_id']: r['reaction_type'] for r in reactions}
        
        comments_html = render_to_string('stories/comments_list.html', {
            'comments': page_obj.object_list,
            'user': request.user,
            'user_reactions': user_reactions
        })
        
        return JsonResponse({
            'status': 'success',
            'comments_html': comments_html,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page,
            'total_pages': paginator.num_pages,
            'total_comments': paginator.count
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def load_more_comments(request, story_id):
    """Загрузка дополнительных комментариев (для кнопки 'Показать еще')"""
    try:
        story = get_object_or_404(Story, id=story_id, is_published=True)
        offset = int(request.GET.get('offset', 0))
        limit = 5  # Загружаем по 5 комментариев за раз
        
        # Получаем основные комментарии (не ответы) с offset
        comments = StoryComment.objects.filter(
            story=story,
            parent=None,
            is_approved=True
        ).select_related('user').prefetch_related('replies').order_by('-is_pinned', '-created_at')[offset:offset + limit]
        
        # Проверяем, есть ли еще комментарии
        total_comments = StoryComment.objects.filter(
            story=story,
            parent=None,
            is_approved=True
        ).count()
        
        has_more = (offset + limit) < total_comments
        
        # Получаем реакции пользователя если он авторизован
        user_reactions = {}
        if request.user.is_authenticated:
            reactions = CommentReaction.objects.filter(
                comment__in=[c.id for c in comments],
                user=request.user
            ).values('comment_id', 'reaction_type')
            user_reactions = {r['comment_id']: r['reaction_type'] for r in reactions}
        
        # Рендерим HTML для новых комментариев
        comments_html = ''
        for comment in comments:
            comment_html = render_to_string('stories/comment_item.html', {
                'comment': comment,
                'user': request.user,
                'user_reactions': user_reactions
            })
            comments_html += comment_html
        
        return JsonResponse({
            'status': 'success',
            'comments_html': comments_html,
            'has_more': has_more,
            'loaded_count': len(comments),
            'total_comments': total_comments
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
