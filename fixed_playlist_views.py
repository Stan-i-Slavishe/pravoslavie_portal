# ИСПРАВЛЕННЫЕ ФУНКЦИИ ДЛЯ views_playlists.py

@login_required
@require_http_methods(["POST"])
def add_to_playlist(request):
    """AJAX: Добавление рассказа в плейлист - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
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
    try:
        # Получаем данные из JSON
        if hasattr(request, 'content_type') and request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            # Fallback для form data
            data = request.POST
            
        story_id = data.get('story_id')
        playlist_id = data.get('playlist_id')
        
        print(f"DEBUG: Removing story_id={story_id} from playlist_id={playlist_id}")
        
        if not story_id or not playlist_id:
            return JsonResponse({
                'success': False,
                'message': 'Не указан ID рассказа или плейлиста'
            }, status=400)
        
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
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_public = request.POST.get('is_public') == 'on'
        
        print(f"DEBUG: Creating playlist - name={name}, is_public={is_public}")
        print(f"DEBUG: POST data: {dict(request.POST)}")
        
        if not name:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Название плейлиста обязательно'
                }, status=400)
            else:
                messages.error(request, 'Название плейлиста обязательно')
                return redirect('stories:playlists')
        
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
            
            print(f"DEBUG: Created playlist {playlist.title} with slug {playlist.slug}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Плейлист "{name}" создан успешно!',
                    'playlist_id': playlist.id,
                    'redirect_url': f'/stories/playlist/{playlist.slug}/'
                })
            else:
                messages.success(request, f'Плейлист "{name}" создан успешно!')
                return redirect('stories:playlist_detail', slug=playlist.slug)
                
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
                return redirect('stories:playlists')
    
    return render(request, 'stories/create_playlist.html')
