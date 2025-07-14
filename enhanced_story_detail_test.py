# Добавим функцию enhanced_story_detail в конец файла views_playlists.py

# Код для добавления в конец файла:

@login_required
@require_http_methods(["POST"]) 
def add_to_playlist(request):
    """
    Добавление рассказа в плейлист
    """
    if not Playlist or not PlaylistItem:
        return JsonResponse({'success': False, 'message': 'Функция недоступна'}, status=503)
    
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False, 
                'message': 'Не указаны необходимые параметры'
            })
        
        try:
            story = Story.objects.get(id=story_id, is_published=True)
        except Story.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Рассказ не найден'
            })
        
        try:
            playlist = Playlist.objects.get(
                id=playlist_id, 
                creator=request.user,
                is_active=True
            )
        except Playlist.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Плейлист не найден'
            })
        
        # Проверяем, нет ли рассказа в плейлисте
        if PlaylistItem.objects.filter(playlist=playlist, story=story).exists():
            return JsonResponse({
                'success': False, 
                'message': 'Рассказ уже в плейлисте'
            })
        
        # Добавляем рассказ в плейлист
        playlist_item = PlaylistItem.objects.create(
            playlist=playlist,
            story=story,
            order=playlist.playlist_items.count() + 1
        )
        
        # Обновляем счетчик в плейлисте
        updated_count = playlist.playlist_items.count()
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ добавлен в плейлист "{playlist.title}"',
            'stories_count': updated_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'message': 'Неверный формат данных'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Произошла ошибка при добавлении рассказа'
        })


@login_required
@require_http_methods(["POST"])
def remove_from_playlist(request):
    """
    Удаление рассказа из плейлиста
    """
    if not Playlist or not PlaylistItem:
        return JsonResponse({'success': False, 'message': 'Функция недоступна'}, status=503)
    
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False, 
                'message': 'Не указаны необходимые параметры'
            })
        
        try:
            story = Story.objects.get(id=story_id, is_published=True)
        except Story.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Рассказ не найден'
            })
        
        try:
            playlist = Playlist.objects.get(
                id=playlist_id, 
                creator=request.user,
                is_active=True
            )
        except Playlist.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Плейлист не найден'
            })
        
        # Ищем элемент плейлиста
        try:
            playlist_item = PlaylistItem.objects.get(
                playlist=playlist,
                story=story
            )
        except PlaylistItem.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Рассказ не найден в плейлисте'
            })
        
        # Удаляем элемент
        playlist_item.delete()
        
        # Обновляем счетчик
        updated_count = playlist.playlist_items.count()
        
        return JsonResponse({
            'success': True,
            'message': f'Рассказ удален из плейлиста "{playlist.title}"',
            'stories_count': updated_count
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'message': 'Неверный формат данных'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Произошла ошибка при удалении рассказа'
        })


# Теперь нужно обновить playlist_sidebar.html файл с кнопкой свора��ивания
