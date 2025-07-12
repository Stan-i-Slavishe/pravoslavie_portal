# simple_playlist_api.py - Простой API для плейлистов без моделей

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
def api_playlists(request):
    """API для получения плейлистов пользователя (упрощенная версия)"""
    
    # Заглушка - возвращаем базовые плейлисты
    playlists_data = [
        {
            'id': 'watch_later',
            'title': 'Посмотреть позже',
            'has_story': False,
            'stories_count': 0,
            'is_public': False
        },
        {
            'id': 'favorites',
            'title': 'Избранное', 
            'has_story': False,
            'stories_count': 0,
            'is_public': False
        }
    ]
    
    return JsonResponse({
        'success': True,
        'playlists': playlists_data
    })

@login_required
@require_POST  
def api_toggle_playlist(request):
    """API для добавления/удаления рассказа из плейлиста (упрощенная версия)"""
    
    story_slug = request.POST.get('story_slug')
    playlist_id = request.POST.get('playlist_id')
    action = request.POST.get('action')
    
    if not all([story_slug, playlist_id, action]):
        return JsonResponse({
            'success': False,
            'message': 'Недостаточно данных'
        })
    
    # Заглушка - просто возвращаем успех
    playlist_names = {
        'watch_later': 'Посмотреть позже',
        'favorites': 'Избранное'
    }
    
    playlist_name = playlist_names.get(playlist_id, f'Плейлист {playlist_id}')
    
    if action == 'add':
        message = f'Добавлено в "{playlist_name}"'
    elif action == 'remove':
        message = f'Удалено из "{playlist_name}"'
    else:
        return JsonResponse({
            'success': False,
            'message': 'Неизвестное действие'
        })
    
    return JsonResponse({
        'success': True,
        'message': message
    })

@login_required
@require_POST
def api_create_playlist(request):
    """API для создания нового плейлиста (упрощенная версия)"""
    
    name = request.POST.get('name', '').strip()
    
    if not name:
        return JsonResponse({
            'success': False,
            'message': 'Введите название плейлиста'
        })
    
    # Заглушка - просто возвращаем успех
    return JsonResponse({
        'success': True,
        'message': f'Плейлист "{name}" создан!',
        'playlist_id': f'user_{name.lower().replace(" ", "_")}'
    })
