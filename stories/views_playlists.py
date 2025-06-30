# ==========================================
# НОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ ПЛЕЙЛИСТОВ
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.utils.crypto import get_random_string
import json

try:
    from .models import Story, Playlist, PlaylistItem, StoryView, StoryRecommendation
except ImportError:
    # Если модели плейлистов еще не созданы
    from .models import Story
    Playlist = None
    PlaylistItem = None
    StoryView = None
    StoryRecommendation = None


def get_story_recommendations(story, user=None, limit=6):
    """Получение рекомендаций для рассказа"""
    recommendations = []
    
    # 1. Рекомендации по тегам
    if story.tags.exists():
        tag_recommendations = Story.objects.filter(
            tags__in=story.tags.all(),
            is_published=True
        ).exclude(id=story.id).annotate(
            view_count=Count('views')
        ).order_by('-view_count', '-created_at')[:limit//2]
        
        recommendations.extend(tag_recommendations)
    
    # 2. Рекомендации по категории
    if story.category:
        category_recommendations = Story.objects.filter(
            category=story.category,
            is_published=True
        ).exclude(id=story.id).exclude(
            id__in=[r.id for r in recommendations]
        ).annotate(
            view_count=Count('views')
        ).order_by('-view_count', '-created_at')[:limit//2]
        
        recommendations.extend(category_recommendations)
    
    # 3. Если недостаточно рекомендаций, добавляем популярные
    if len(recommendations) < limit:
        popular_stories = Story.objects.filter(
            is_published=True
        ).exclude(id=story.id).exclude(
            id__in=[r.id for r in recommendations]
        ).annotate(
            view_count=Count('views')
        ).order_by('-view_count', '-created_at')[:limit - len(recommendations)]
        
        recommendations.extend(popular_stories)
    
    return recommendations[:limit]


@login_required
def playlists_list(request):
    """Список плейлистов пользователя"""
    if not Playlist:
        messages.error(request, 'Функция плейлистов пока недоступна')
        return redirect('stories:list')
        
    try:
        playlists = Playlist.objects.filter(
            creator=request.user
        ).annotate(
            calculated_stories_count=Count('playlist_items')
        ).order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(playlists, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
        }
        
        return render(request, 'stories/playlists_list.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка загрузки плейлистов: {e}')
        return redirect('stories:list')


@login_required
def playlist_detail(request, slug):
    """Детальная страница плейлиста"""
    try:
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        
        # Получаем элементы плейлиста в правильном порядке
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story').order_by('order')
        
        context = {
            'playlist': playlist,
            'playlist_items': playlist_items,
        }
        
        return render(request, 'stories/playlist_detail.html', context)
    except Exception as e:
        messages.error(request, 'Плейлист не найден или недоступен')
        return redirect('stories:playlists_list')


@login_required
def create_playlist(request):
    """Создание нового плейлиста"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_public = request.POST.get('is_public') == 'on'
        
        if not name:
            messages.error(request, 'Название плейлиста обязательно')
            return redirect('stories:playlists_list')
        
        # Создаем слаг
        base_slug = slugify(name)
        if not base_slug:
            base_slug = 'playlist'
        
        slug = base_slug
        counter = 1
        try:
            while Playlist.objects.filter(slug=slug, creator=request.user).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            playlist = Playlist.objects.create(
                creator=request.user,
                title=name,
                slug=slug,
                description=description,
                playlist_type='public' if is_public else 'private'
            )
            
            messages.success(request, f'Плейлист "{name}" создан успешно!')
            return redirect('stories:playlist_detail', slug=playlist.slug)
        except Exception as e:
            messages.error(request, 'Ошибка при создании плейлиста')
            return redirect('stories:playlists_list')
    
    return render(request, 'stories/create_playlist.html')


@login_required
def edit_playlist(request, slug):
    """Редактирование плейлиста"""
    try:
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        
        if request.method == 'POST':
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            is_public = request.POST.get('is_public') == 'on'
            
            if not name:
                messages.error(request, 'Название плейлиста обязательно')
            else:
                playlist.title = name
                playlist.description = description
                # Устанавливаем тип плейлиста в зависимости от is_public
                playlist.playlist_type = 'public' if is_public else 'private'
                playlist.save()
                
                messages.success(request, 'Плейлист обновлен успешно!')
                return redirect('stories:playlist_detail', slug=playlist.slug)
        
        context = {
            'playlist': playlist,
        }
        
        return render(request, 'stories/edit_playlist.html', context)
    except Exception as e:
        messages.error(request, 'Плейлист не найден')
        return redirect('stories:playlists_list')


@login_required
@require_http_methods(["POST"])
def delete_playlist(request, slug):
    """Удаление плейлиста"""
    try:
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        playlist_name = playlist.title
        playlist.delete()
        
        messages.success(request, f'Плейлист "{playlist_name}" удален')
    except Exception as e:
        messages.error(request, 'Ошибка при удалении плейлиста')
    
    return redirect('stories:playlists_list')


@login_required
@require_http_methods(["POST"])
def add_to_playlist(request):
    """AJAX: Добавление рассказа в плейлист"""
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        story = get_object_or_404(Story, id=story_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        
        # Проверяем, нет ли уже этого рассказа в плейлисте
        if PlaylistItem.objects.filter(playlist=playlist, story=story).exists():
            return JsonResponse({
                'success': False,
                'message': 'Рассказ уже есть в этом плейлисте'
            })
        
        # Определяем порядок (последний + 1)
        last_order = PlaylistItem.objects.filter(
            playlist=playlist
        ).count()
        
        PlaylistItem.objects.create(
            playlist=playlist,
            story=story,
            order=last_order + 1
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ добавлен в плейлист "{playlist.title}"'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при добавлении'
        })


@login_required
@require_http_methods(["POST"])
def remove_from_playlist(request):
    """AJAX: Удаление рассказа из плейлиста"""
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        story = get_object_or_404(Story, id=story_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        
        playlist_item = get_object_or_404(
            PlaylistItem,
            playlist=playlist,
            story=story
        )
        
        playlist_item.delete()
        
        # Переупорядочиваем оставшиеся элементы
        remaining_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).order_by('order')
        
        for i, item in enumerate(remaining_items, 1):
            if item.order != i:
                item.order = i
                item.save(update_fields=['order'])
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ удален из плейлиста "{playlist.title}"'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при удалении'
        })


@login_required
@require_http_methods(["POST"])
def reorder_playlist(request, slug):
    """AJAX: Изменение порядка рассказов в плейлисте"""
    try:
        playlist = get_object_or_404(Playlist, slug=slug, creator=request.user)
        data = json.loads(request.body)
        story_orders = data.get('story_orders', [])
        
        # Обновляем порядок для каждого элемента
        for item_data in story_orders:
            story_id = item_data.get('story_id')
            new_order = item_data.get('order')
            
            PlaylistItem.objects.filter(
                playlist=playlist,
                story_id=story_id
            ).update(order=new_order)
        
        return JsonResponse({
            'success': True,
            'message': 'Порядок рассказов обновлен'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при изменении порядка'
        })


def public_playlists(request):
    """Публичные плейлисты всех пользователей"""
    try:
        playlists = Playlist.objects.filter(
            playlist_type='public'
        ).select_related('creator').annotate(
            calculated_stories_count=Count('playlist_items')
        ).order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(playlists, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
        }
        
        return render(request, 'stories/public_playlists.html', context)
    except Exception as e:
        messages.error(request, 'Функция публичных плейлистов пока недоступна')
        return redirect('stories:list')


def public_playlist_detail(request, user_id, slug):
    """Детальная страница публичного плейлиста"""
    try:
        playlist = get_object_or_404(
            Playlist,
            slug=slug,
            creator_id=user_id,
            playlist_type='public'
        )
        
        # Получаем элементы плейлиста в правильном порядке
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story').order_by('order')
        
        context = {
            'playlist': playlist,
            'playlist_items': playlist_items,
            'is_owner': request.user == playlist.creator,
        }
        
        return render(request, 'stories/public_playlist_detail.html', context)
    except Exception as e:
        messages.error(request, 'Плейлист не найден или недоступен')
        return redirect('stories:public_playlists')


# ==========================================
# УЛУЧШЕННЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ РЕКОМЕНДАЦИЙ
# ==========================================

def enhanced_story_detail(request, slug):
    """Улучшенная детальная страница рассказа с рекомендациями и плейлистами"""
    story = get_object_or_404(Story, slug=slug, is_published=True)
    
    # Обработка POST-запросов (добавление комментариев)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Для добавления комментариев необходимо войти в систему')
            return redirect('account_login')
        
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent')
        
        if text:
            try:
                from .models import StoryComment
                parent = None
                if parent_id:
                    try:
                        parent = StoryComment.objects.get(id=parent_id, story=story)
                    except StoryComment.DoesNotExist:
                        pass
                
                comment = StoryComment.objects.create(
                    story=story,
                    user=request.user,
                    text=text,
                    parent=parent
                )
                
                messages.success(request, 'Комментарий успешно добавлен!')
            except Exception as e:
                messages.error(request, 'Ошибка при добавлении комментария')
        else:
            messages.error(request, 'Комментарий не может быть пустым')
        
        return redirect('stories:detail', slug=story.slug)
    
    # Увеличиваем счетчик просмотров
    session_key = f'viewed_story_{story.id}'
    if not request.session.get(session_key, False):
        try:
            if request.user.is_authenticated:
                story_view, created = StoryView.objects.get_or_create(
                    story=story,
                    user=request.user,
                    defaults={'ip_address': request.META.get('REMOTE_ADDR')}
                )
                if not created:
                    story_view.view_count += 1
                    story_view.save()
            else:
                # Для неавторизованных пользователей считаем по IP
                ip_address = request.META.get('REMOTE_ADDR')
                story_view, created = StoryView.objects.get_or_create(
                    story=story,
                    ip_address=ip_address,
                    defaults={'user': None}
                )
                if not created:
                    story_view.view_count += 1
                    story_view.save()
            
            # Обновляем общий счетчик просмотров
            story.views_count = StoryView.objects.filter(story=story).aggregate(
                total=Count('id')
            )['total'] or 0
            story.save(update_fields=['views_count'])
        except Exception as e:
            # Если модели просмотров еще нет, просто увеличиваем старый счетчик
            story.increment_views()
        
        request.session[session_key] = True
    
    # Получаем рекомендации
    recommendations = get_story_recommendations(story, request.user)
    
    # Плейлисты пользователя (если авторизован)
    user_playlists = []
    story_in_playlists = []
    if request.user.is_authenticated and Playlist:
        try:
            # Получаем плейлисты с аннотацией количества рассказов
            user_playlists = Playlist.objects.filter(
                creator=request.user
            ).annotate(
                calculated_stories_count=Count('playlist_items')
            )
            
            print(f"Отладка: Найдено плейлистов: {user_playlists.count()}")
            
            # Проверяем, в каких плейлистах уже есть этот рассказ
            story_in_playlists = PlaylistItem.objects.filter(
                playlist__creator=request.user,
                story=story
            ).values_list('playlist_id', flat=True)
            
            print(f"Отладка: Рассказ в плейлистах: {list(story_in_playlists)}")
        except Exception as e:
            print(f"Ошибка получения плейлистов: {e}")
            pass
    
    # Похожие рассказы (по категории и тегам)
    related_stories = Story.objects.filter(
        is_published=True
    ).exclude(
        id=story.id
    ).select_related('category')
    
    if story.category:
        related_stories = related_stories.filter(category=story.category)
    
    related_stories = related_stories[:3]
    
    # Проверяем лайки
    try:
        if request.user.is_authenticated:
            from .models import StoryLike
            user_liked = StoryLike.objects.filter(
                story=story, 
                user=request.user
            ).exists()
        else:
            user_liked = False
        
        likes_count = story.likes.count()
    except Exception:
        user_liked = False
        likes_count = 0
    
    # Комментарии
    try:
        from .models import StoryComment, CommentReaction
        comments = story.comments.filter(
            is_approved=True,
            parent=None
        ).select_related('user').prefetch_related(
            'replies__user'
        ).order_by('-is_pinned', '-created_at')[:5]  # Первые 5 комментариев
        
        comments_count = story.comments.filter(is_approved=True).count()
        
        # Получаем реакции пользователя на комментарии
        user_reactions = {}
        if request.user.is_authenticated:
            reactions = CommentReaction.objects.filter(
                comment__story=story,
                user=request.user
            ).values('comment_id', 'reaction_type')
            user_reactions = {r['comment_id']: r['reaction_type'] for r in reactions}
            
    except Exception as e:
        comments = []
        comments_count = 0
        user_reactions = {}
    
    # Навигация по рассказам
    all_stories = list(Story.objects.filter(is_published=True).order_by('created_at').values_list('id', flat=True))
    previous_story = None
    next_story = None
    
    try:
        current_index = all_stories.index(story.id)
        if current_index > 0:
            prev_story_id = all_stories[current_index - 1]
            previous_story = Story.objects.get(id=prev_story_id)
        if current_index < len(all_stories) - 1:
            next_story_id = all_stories[current_index + 1]
            next_story = Story.objects.get(id=next_story_id)
    except (ValueError, Story.DoesNotExist):
        pass
    
    context = {
        'story': story,
        'related_stories': related_stories,
        'recommendations': recommendations,
        'user_playlists': user_playlists,
        'story_in_playlists': story_in_playlists,
        'user_liked': user_liked,
        'likes_count': likes_count,
        'comments': comments,
        'comments_count': comments_count,
        'user_reactions': user_reactions,
        'previous_story': previous_story,
        'next_story': next_story,
    }
    
    return render(request, 'stories/detail_v2.html', context)
