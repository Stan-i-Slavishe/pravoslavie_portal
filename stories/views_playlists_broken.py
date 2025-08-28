# ==========================================
# НОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ ПЛЕЙЛИСТОВ
# ==========================================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
import json

try:
    from .models import Story, Playlist, PlaylistItem, StoryView, StoryRecommendation, UserPlaylistPreference
except ImportError:
    # Если модели плейлистов еще не созданы
    from .models import Story
    Playlist = None
    PlaylistItem = None
    StoryView = None
    StoryRecommendation = None
    UserPlaylistPreference = None


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
def playlist_modal_content(request, playlist_id):
    """AJAX: Загрузка содержимого плейлиста для модального окна"""
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        
        # Получаем элементы плейлиста с информацией о рассказах
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related(
            'story', 'story__category'
        ).prefetch_related(
            'story__tags'
        ).order_by('order')
        
        context = {
            'playlist': playlist,
            'playlist_items': playlist_items,
        }
        
        # Рендерим шаблон содержимого плейлиста
        html = render_to_string('stories/playlist_modal_content.html', context, request)
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(
            f'<div class="alert alert-danger m-3">Ошибка загрузки плейлиста: {e}</div>'
        )


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
    playlist = None
    
    try:
        # Пытаемся найти плейлист пользователя
        try:
            playlist = Playlist.objects.get(slug=slug, creator=request.user)
        except Playlist.DoesNotExist:
            # Пытаемся найти публичные плейлисты
            try:
                playlist = Playlist.objects.get(slug=slug, playlist_type='public')
            except Playlist.DoesNotExist:
                messages.error(request, f'Плейлист с адресом "{slug}" не найден')
                return redirect('stories:playlists_list')


@login_required
@require_http_methods(["POST"])
def add_to_playlist(request):
    """AJAX: Добавление рассказа в плейлист"""
    print(f"🔍 ADD Headers: {dict(request.headers)}")
    print(f"📝 ADD Content-Type: {request.content_type}")
    print(f"📦 ADD Body: {request.body[:200]}")
    
    try:
        # Парсим JSON данные
        data = json.loads(request.body)
        print(f"✅ ADD Parsed data: {data}")
        
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        if not story_id or not playlist_id:
            print("❌ ADD Missing parameters")
            return JsonResponse({
                'success': False,
                'message': 'Не указаны обязательные параметры'
            })
        
        # Получаем рассказ - поддерживаем и ID и slug
        try:
            if str(story_id).isdigit():
                story = get_object_or_404(Story, id=story_id, is_published=True)
            else:
                story = get_object_or_404(Story, slug=story_id, is_published=True)
        except Exception as e:
            print(f"❌ Story not found: {story_id}")
            return JsonResponse({
                'success': False,
                'message': f'Рассказ не найден: {story_id}'
            })
        
        # Обработка системных плейлистов
        if playlist_id == 'watch_later':
            if UserPlaylistPreference:
                prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
                playlist = prefs.get_or_create_watch_later()
            else:
                return JsonResponse({'success': False, 'message': 'Системные плейлисты недоступны'})
        elif playlist_id == 'favorites':
            if UserPlaylistPreference:
                prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
                playlist = prefs.get_or_create_favorites()
            else:
                return JsonResponse({'success': False, 'message': 'Системные плейлисты недоступны'})
        else:
            # Обычный плейлист пользователя
            try:
                if str(playlist_id).isdigit():
                    playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
                else:
                    # Локальные плейлисты из JavaScript
                    return JsonResponse({'success': True, 'message': 'Локальный плейлист обновлен'})
            except Exception as e:
                print(f"❌ Playlist not found: {playlist_id}")
                return JsonResponse({
                    'success': False,
                    'message': f'Плейлист не найден: {playlist_id}'
                })
        
        print(f"📚 ADD Story: {story.title}")
        print(f"📁 ADD Playlist: {playlist.title}")
        
        # Проверяем, что рассказа нет в плейлисте
        if PlaylistItem and PlaylistItem.objects.filter(playlist=playlist, story=story).exists():
            print(f"⚠️ Story already in playlist")
            return JsonResponse({'success': False, 'message': 'Рассказ уже в плейлисте'})
        
        # Добавляем в плейлист
        if PlaylistItem:
            # Определяем порядок (последний + 1)
            last_item = PlaylistItem.objects.filter(playlist=playlist).order_by('-order').first()
            order = (last_item.order + 1) if last_item else 1
            
            PlaylistItem.objects.create(
                playlist=playlist,
                story=story,
                order=order
            )
            print(f"✅ Added story to playlist with order {order}")
        
        print("✅ ADD Success! Returning JSON response")
        return JsonResponse({
            'success': True, 
            'message': f'Рассказ добавлен в плейлист "{playlist.title}"'
        })
        
    except json.JSONDecodeError as e:
        print(f"❌ ADD JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Неверный формат данных'
        })
    except Exception as e:
        print(f"❌ ADD General error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }, status=400)
        
        # Проверяем доступ
        if playlist and playlist.creator != request.user and playlist.playlist_type != 'public':
            messages.error(request, 'У вас нет доступа к этому плейлисту')
            return redirect('stories:playlists_list')
        
        # Получаем элементы плейлиста
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story', 'story__category').order_by('order')
        
        # Увеличиваем счетчик просмотров
        if playlist.creator != request.user and playlist.playlist_type == 'public':
            playlist.increment_views()
        
        context = {
            'playlist': playlist,
            'playlist_items': playlist_items,
            'can_edit': playlist.can_be_edited_by(request.user),
        }
        
        return render(request, 'stories/playlist_detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Ошибка при загрузке плейлиста: {e}')
        return redirect('stories:playlists_list')


@login_required
def create_playlist(request):
    """Создание нового плейлиста"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_public = request.POST.get('is_public') == 'on'
        initial_story_id = request.POST.get('initial_story_id')
        
        if not name:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Название плейлиста обязательно'
                })
            messages.error(request, 'Название плейлиста обязательно')
            return redirect('stories:playlists_list')
        
        # Создаем слаг
        base_slug = slugify(name, allow_unicode=True)
        if not base_slug:
            base_slug = 'playlist'
        
        slug = base_slug
        counter = 1
        try:
            while Playlist.objects.filter(slug=slug, creator=request.user).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Создаем плейлист
            playlist = Playlist.objects.create(
                creator=request.user,
                title=name,
                slug=slug,
                description=description,
                playlist_type='public' if is_public else 'private'
            )
            
            # Добавляем текущий рассказ, если указан
            if initial_story_id:
                try:
                    story = Story.objects.get(id=initial_story_id, is_published=True)
                    PlaylistItem.objects.create(
                        playlist=playlist,
                        story=story,
                        order=1
                    )
                except Story.DoesNotExist:
                    pass
            
            # Возвращаем JSON для AJAX запросов
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Плейлист "{name}" создан успешно!',
                    'playlist': {
                        'id': playlist.id,
                        'title': playlist.title,
                        'slug': playlist.slug,
                        'url': playlist.get_absolute_url()
                    }
                })
            
            messages.success(request, f'Плейлист "{name}" создан успешно!')
            return redirect('stories:playlist_detail', slug=playlist.slug)
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Ошибка при создании плейлиста'
                })
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
    print(f"🔍 Headers: {dict(request.headers)}")
    print(f"📝 Content-Type: {request.content_type}")
    print(f"📦 Body: {request.body[:200]}")
    
    try:
        # Парсим JSON данные
        data = json.loads(request.body)
        print(f"✅ Parsed data: {data}")
        
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        if not story_id or not playlist_id:
            print("❌ Missing parameters")
            return JsonResponse({
                'success': False,
                'message': 'Не указаны обязательные параметры'
            })
        
        # Получаем объекты
        story = get_object_or_404(Story, id=story_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, creator=request.user)
        
        print(f"📚 Story: {story.title}")
        print(f"📁 Playlist: {playlist.title}")
        
        # Находим и удаляем элемент плейлиста
        try:
            playlist_item = PlaylistItem.objects.get(
                playlist=playlist,
                story=story
            )
            playlist_item.delete()
            print(f"✅ Deleted playlist item for story {story_id}")
        except PlaylistItem.DoesNotExist:
            print(f"⚠️  Playlist item not found for story {story_id} in playlist {playlist_id}")
            return JsonResponse({
                'success': False,
                'message': 'Рассказ не найден в этом плейлисте'
            })
        
        # Переупорядочиваем оставшиеся элементы
        remaining_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).order_by('order')
        
        for i, item in enumerate(remaining_items, 1):
            if item.order != i:
                item.order = i
                item.save(update_fields=['order'])
        
        print("✅ Success! Returning JSON response")
        return JsonResponse({
            'success': True,
            'message': f'Рассказ удален из плейлиста "{playlist.title}"'
        })
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Неверный формат данных'
        })
    except Exception as e:
        print(f"❌ General error: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка при удалении: {str(e)}'
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
    story_in_watch_later = []
    story_in_favorites = []
    
    if request.user.is_authenticated and Playlist:
        try:
            # Получаем плейлисты с аннотацией количества рассказов
            user_playlists = Playlist.objects.filter(
                creator=request.user
            ).annotate(
                calculated_stories_count=Count('playlist_items')
            ).order_by('-updated_at')
            
            # Проверяем, в каких плейлистах уже есть этот рассказ
            story_in_playlists = list(PlaylistItem.objects.filter(
                playlist__creator=request.user,
                story=story
            ).values_list('playlist_id', flat=True))
            
            # Проверяем системные плейлисты
            if UserPlaylistPreference:
                try:
                    prefs = UserPlaylistPreference.objects.get(user=request.user)
                    
                    if prefs.watch_later_playlist:
                        if PlaylistItem.objects.filter(
                            playlist=prefs.watch_later_playlist,
                            story=story
                        ).exists():
                            story_in_watch_later = [story.id]
                    
                    if prefs.favorites_playlist:
                        if PlaylistItem.objects.filter(
                            playlist=prefs.favorites_playlist,
                            story=story
                        ).exists():
                            story_in_favorites = [story.id]
                            
                except UserPlaylistPreference.DoesNotExist:
                    pass
                    
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
        
        # ИСПРАВЛЕНИЕ: Считаем только основные комментарии (без ответов)
        comments_count = story.comments.filter(is_approved=True, parent=None).count()
        
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
        'story_in_watch_later': story_in_watch_later,
        'story_in_favorites': story_in_favorites,
        'user_liked': user_liked,
        'likes_count': likes_count,
        'comments': comments,
        'comments_count': comments_count,
        'user_reactions': user_reactions,
        'previous_story': previous_story,
        'next_story': next_story,
    }
    
    return render(request, 'stories/story_detail.html', context)


# ==========================================
# НОВЫЕ ФУНКЦИИ ДЛЯ ИНТЕРАКТИВНОГО САЙДБАРА
# ==========================================

@login_required
@require_http_methods(["POST"])
def toggle_watch_later(request):
    """AJAX: Добавить/убрать рассказ из 'Посмотреть позже'"""
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        
        story = get_object_or_404(Story, id=story_id)
        
        # Получаем или создаем настройки пользователя
        if not UserPlaylistPreference:
            return JsonResponse({
                'success': False,
                'message': 'Функция недоступна - отсутствуют модели'
            })
            
        prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
        watch_later_playlist = prefs.get_or_create_watch_later()
        
        # Проверяем, есть ли уже рассказ в плейлисте
        playlist_item = PlaylistItem.objects.filter(
            playlist=watch_later_playlist,
            story=story
        ).first()
        
        if playlist_item:
            # Удаляем из плейлиста
            playlist_item.delete()
            message = "Убрано из 'Посмотреть позже'"
            action = "removed"
        else:
            # Добавляем в плейлист
            PlaylistItem.objects.create(
                playlist=watch_later_playlist,
                story=story,
                order=watch_later_playlist.playlist_items.count() + 1
            )
            message = "Добавлено в 'Посмотреть позже'"
            action = "added"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'action': action
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка'
        })


@login_required
@require_http_methods(["POST"])
def toggle_favorites(request):
    """AJAX: Добавить/убрать рассказ из 'Избранное'"""
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        
        story = get_object_or_404(Story, id=story_id)
        
        # Получаем или создаем настройки пользователя
        if not UserPlaylistPreference:
            return JsonResponse({
                'success': False,
                'message': 'Функция недоступна - отсутствуют модели'
            })
            
        prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
        favorites_playlist = prefs.get_or_create_favorites()
        
        # Проверяем, есть ли уже рассказ в плейлисте
        playlist_item = PlaylistItem.objects.filter(
            playlist=favorites_playlist,
            story=story
        ).first()
        
        if playlist_item:
            # Удаляем из плейлиста
            playlist_item.delete()
            message = "Убрано из избранного"
            action = "removed"
        else:
            # Добавляем в плейлист
            PlaylistItem.objects.create(
                playlist=favorites_playlist,
                story=story,
                order=favorites_playlist.playlist_items.count() + 1
            )
            message = "Добавлено в избранное"
            action = "added"
        
        return JsonResponse({
            'success': True,
            'message': message,
            'action': action
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка'
        })


@login_required
def sidebar_playlists_partial(request, story_slug):
    """Частичный рендер сайдбара плейлистов для AJAX обновления"""
    try:
        story = get_object_or_404(Story, slug=story_slug, is_published=True)
        
        # Получаем плейлисты пользователя с информацией о наличии рассказа
        user_playlists = []
        story_in_playlists = []
        story_in_watch_later = []
        story_in_favorites = []
        
        if Playlist:
            # Получаем плейлисты с аннотацией количества рассказов
            user_playlists = Playlist.objects.filter(
                creator=request.user
            ).annotate(
                calculated_stories_count=Count('playlist_items')
            ).order_by('-updated_at')
            
            # Проверяем, в каких плейлистах уже есть этот рассказ
            story_in_playlists = list(PlaylistItem.objects.filter(
                playlist__creator=request.user,
                story=story
            ).values_list('playlist_id', flat=True))
            
            # Проверяем системные плейлисты
            if UserPlaylistPreference:
                try:
                    prefs = UserPlaylistPreference.objects.get(user=request.user)
                    
                    if prefs.watch_later_playlist:
                        if PlaylistItem.objects.filter(
                            playlist=prefs.watch_later_playlist,
                            story=story
                        ).exists():
                            story_in_watch_later = [story.id]
                    
                    if prefs.favorites_playlist:
                        if PlaylistItem.objects.filter(
                            playlist=prefs.favorites_playlist,
                            story=story
                        ).exists():
                            story_in_favorites = [story.id]
                            
                except UserPlaylistPreference.DoesNotExist:
                    pass
        
        context = {
            'story': story,
            'user_playlists': user_playlists,
            'story_in_playlists': story_in_playlists,
            'story_in_watch_later': story_in_watch_later,
            'story_in_favorites': story_in_favorites,
        }
        
        # Возвращаем только HTML сайдбара
        html = render_to_string('stories/partials/playlist_sidebar.html', context, request)
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse('<div class="alert alert-danger">Ошибка загрузки плейлистов</div>')


@login_required
def watch_later_playlist(request):
    """Страница плейлиста 'Посмотреть позже'"""
    if not UserPlaylistPreference:
        messages.error(request, 'Функция недоступна')
        return redirect('stories:list')
        
    try:
        prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
        playlist = prefs.get_or_create_watch_later()
        
        # Получаем элементы плейлиста
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story').order_by('-added_at')  # Последние добавленные сверху
        
        # Пагинация
        paginator = Paginator(playlist_items, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'playlist': playlist,
            'page_obj': page_obj,
            'is_system_playlist': True,
            'playlist_type': 'watch_later'
        }
        
        return render(request, 'stories/system_playlist.html', context)
    except Exception as e:
        messages.error(request, 'Ошибка загрузки плейлиста')
        return redirect('stories:playlists_list')


def public_playlist_detail(request, user_id, slug):
    """Публичная страница плейлиста"""
    try:
        playlist = get_object_or_404(
            Playlist, 
            slug=slug, 
            creator_id=user_id,
            playlist_type='public'
        )
        
        # Получаем элементы плейлиста
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story', 'story__category').order_by('order')
        
        # Увеличиваем счетчик просмотров
        playlist.increment_views()
        
        context = {
            'playlist': playlist,
            'playlist_items': playlist_items,
            'can_edit': False,  # Публичный просмотр - редактирование недоступно
            'is_public_view': True,
        }
        
        return render(request, 'stories/playlist_detail.html', context)
    except Exception as e:
        messages.error(request, 'Плейлист не найден')
        return redirect('stories:list')


@login_required
def quick_add_to_playlist_modal(request, story_id):
    """Модальное окно для быстрого добавления в плейлист"""
    story = get_object_or_404(Story, id=story_id)
    
    # Получаем все плейлисты пользователя с информацией о наличии рассказа
    user_playlists = Playlist.objects.filter(
        creator=request.user
    ).annotate(
        has_story=Count('playlist_items', filter=Q(playlist_items__story=story))
    ).order_by('-updated_at')
    
    context = {
        'story': story,
        'user_playlists': user_playlists,
    }
    
    return render(request, 'stories/quick_add_playlist_modal.html', context)


def story_player(request, slug):
    """Проигрыватель рассказа с поддержкой плейлистов"""
    story = get_object_or_404(Story, slug=slug, is_published=True)
    
    # Получаем информацию о плейлисте, если передан
    playlist_slug = request.GET.get('playlist')
    current_playlist = None
    next_story = None
    prev_story = None
    
    if playlist_slug and request.user.is_authenticated:
        try:
            current_playlist = Playlist.objects.get(
                slug=playlist_slug,
                creator=request.user
            )
            
            # Получаем следующий и предыдущий рассказы в плейлисте
            try:
                current_item = PlaylistItem.objects.get(playlist=current_playlist, story=story)
                next_item = PlaylistItem.objects.filter(
                    playlist=current_playlist,
                    order__gt=current_item.order
                ).order_by('order').first()
                
                prev_item = PlaylistItem.objects.filter(
                    playlist=current_playlist,
                    order__lt=current_item.order
                ).order_by('-order').first()
                
                next_story = next_item.story if next_item else None
                prev_story = prev_item.story if prev_item else None
            except PlaylistItem.DoesNotExist:
                pass
            
        except Playlist.DoesNotExist:
            pass
    
    # Проверяем статус системных плейлистов
    in_watch_later = False
    in_favorites = False
    
    if request.user.is_authenticated and UserPlaylistPreference:
        try:
            prefs = UserPlaylistPreference.objects.get(user=request.user)
            
            if prefs.watch_later_playlist:
                in_watch_later = PlaylistItem.objects.filter(
                    playlist=prefs.watch_later_playlist,
                    story=story
                ).exists()
            
            if prefs.favorites_playlist:
                in_favorites = PlaylistItem.objects.filter(
                    playlist=prefs.favorites_playlist,
                    story=story
                ).exists()
                
        except UserPlaylistPreference.DoesNotExist:
            pass
    
    context = {
        'story': story,
        'current_playlist': current_playlist,
        'next_story': next_story,
        'prev_story': prev_story,
        'in_watch_later': in_watch_later,
        'in_favorites': in_favorites,
    }
    
    return render(request, 'stories/player.html', context)


@login_required
def favorites_playlist(request):
    """Страница плейлиста 'Избранное'"""
    if not UserPlaylistPreference:
        messages.error(request, 'Функция недоступна')
        return redirect('stories:list')
        
    try:
        prefs, created = UserPlaylistPreference.objects.get_or_create(user=request.user)
        playlist = prefs.get_or_create_favorites()
        
        # Получаем элементы плейлиста
        playlist_items = PlaylistItem.objects.filter(
            playlist=playlist
        ).select_related('story').order_by('-added_at')  # Последние добавленные сверху
        
        # Пагинация
        paginator = Paginator(playlist_items, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'playlist': playlist,
            'page_obj': page_obj,
            'is_system_playlist': True,
            'playlist_type': 'favorites'
        }
        
        return render(request, 'stories/system_playlist.html', context)
    except Exception as e:
        messages.error(request, 'Ошибка загрузки плейлиста')
        return redirect('stories:playlists_list')
