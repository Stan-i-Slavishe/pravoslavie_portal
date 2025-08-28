# БЫСТРОЕ ИСПРАВЛЕНИЕ - Добавить недостающую функцию add_to_playlist
# Добавить в stories/views.py или создать отдельный файл

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

try:
    from .models import Story, Playlist, PlaylistItem, UserPlaylistPreference
except ImportError:
    # Если модели плейлистов еще не созданы
    from .models import Story
    Playlist = None
    PlaylistItem = None
    UserPlaylistPreference = None


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