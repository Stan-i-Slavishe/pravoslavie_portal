# БЫСТРОЕ ИСПРАВЛЕНИЕ ОШИБОК ПЛЕЙЛИСТОВ

# 1. Исправляем неправильные URL redirects
# 2. Добавляем проверку существования плейлистов  
# 3. Исправляем функцию add_to_playlist

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

try:
    from .models import Story, Playlist, PlaylistItem
except ImportError:
    from .models import Story
    Playlist = None
    PlaylistItem = None

@login_required
@require_http_methods(["POST"])
def add_to_playlist(request):
    """AJAX: Добавление рассказа в плейлист - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    
    # Проверяем, доступны ли модели плейлистов
    if not Playlist or not PlaylistItem:
        return JsonResponse({
            'success': False,
            'message': 'Функция плейлистов недоступна - модели не найдены'
        }, status=400)
    
    try:
        # Получаем данные из JSON
        if hasattr(request, 'content_type') and request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            # Fallback для form data
            data = request.POST
            
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        print(f"DEBUG: story_id={story_id}, playlist_id={playlist_id}")
        print(f"DEBUG: content_type={getattr(request, 'content_type', 'unknown')}")
        print(f"DEBUG: request.body={request.body}")
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False,
                'message': 'Не указан ID рассказа или плейлиста'
            }, status=400)
        
        # Проверяем существование объектов
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Рассказ с ID {story_id} не найден'
            }, status=404)
        
        try:
            playlist = Playlist.objects.get(id=playlist_id, creator=request.user)
        except Playlist.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Плейлист с ID {playlist_id} не найден или не принадлежит вам'
            }, status=404)
        
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
        
        print(f"DEBUG: Добавлен рассказ {story.title} в плейлист {playlist.title}")
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ добавлен в плейлист "{playlist.title}"'
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка в формате данных'
        }, status=400)
    except Exception as e:
        print(f"Add to playlist error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def remove_from_playlist(request):
    """AJAX: Удаление рассказа из плейлиста - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    
    # Проверяем, доступны ли модели плейлистов
    if not Playlist or not PlaylistItem:
        return JsonResponse({
            'success': False,
            'message': 'Функция плейлистов недоступна - модели не найдены'
        }, status=400)
    
    try:
        # Получаем данные из JSON
        if hasattr(request, 'content_type') and request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        print(f"DEBUG: Removing story_id={story_id} from playlist_id={playlist_id}")
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False,
                'message': 'Не указан ID рассказа или плейлиста'
            }, status=400)
        
        try:
            story = Story.objects.get(id=story_id)
            playlist = Playlist.objects.get(id=playlist_id, creator=request.user)
            playlist_item = PlaylistItem.objects.get(playlist=playlist, story=story)
        except (Story.DoesNotExist, Playlist.DoesNotExist, PlaylistItem.DoesNotExist) as e:
            return JsonResponse({
                'success': False,
                'message': f'Объект не найден: {str(e)}'
            }, status=404)
        
        playlist_item.delete()
        
        print(f"DEBUG: Удален рассказ {story.title} из плейлиста {playlist.title}")
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ удален из плейлиста "{playlist.title}"'
        })
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка в формате данных'
        }, status=400)
    except Exception as e:
        print(f"Remove from playlist error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Произошла ошибка: {str(e)}'
        }, status=500)


@login_required  
def create_playlist(request):
    """Создание нового плейлиста - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
    
    # Проверяем, доступны ли модели плейлистов
    if not Playlist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Функция плейлистов недоступна - модели не найдены'
            }, status=400)
        else:
            messages.error(request, 'Функция плейлистов недоступна')
            return redirect('stories:list')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_public = request.POST.get('is_public') == 'on'
        
        print(f"DEBUG: Creating playlist - name={name}, is_public={is_public}")
        
        if not name:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Название плейлиста обязательно'
                }, status=400)
            else:
                messages.error(request, 'Название плейлиста обязательно')
                return redirect('stories:list')
        
        try:
            from django.utils.text import slugify
            
            # Создаем слаг
            base_slug = slugify(name)
            if not base_slug:
                base_slug = 'playlist'
            
            slug = base_slug
            counter = 1
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
            
            print(f"DEBUG: Created playlist {playlist.title} with slug {playlist.slug}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Плейлист "{name}" создан успешно!',
                    'playlist_id': playlist.id
                })
            else:
                messages.success(request, f'Плейлист "{name}" создан успешно!')
                return redirect('stories:list')
                
        except Exception as e:
            print(f"Create playlist error: {e}")
            import traceback
            traceback.print_exc()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Ошибка при создании плейлиста: {str(e)}'
                }, status=500)
            else:
                messages.error(request, 'Ошибка при создании плейлиста')
                return redirect('stories:list')
    
    return render(request, 'stories/create_playlist.html')
