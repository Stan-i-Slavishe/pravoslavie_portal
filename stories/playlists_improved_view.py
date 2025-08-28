# Улучшенная функция playlists_list с превью
# Добавить в views_playlists.py

@login_required
def playlists_list_improved(request):
    """Список плейлистов пользователя с превью изображений"""
    if not Playlist:
        messages.error(request, 'Функция плейлистов пока недоступна')
        return redirect('stories:list')
        
    try:
        # Получаем плейлисты с предзагруженными рассказами для превью
        playlists = Playlist.objects.filter(
            creator=request.user
        ).annotate(
            calculated_stories_count=Count('playlist_items')
        ).prefetch_related(
            # Загружаем первые 4 рассказа для превью
            'stories__tags',
            'stories__category'
        ).order_by('-updated_at', '-created_at')
        
        # Пагинация
        paginator = Paginator(playlists, 12)  # 12 карточек на страницу (3x4 сетка)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
        }
        
        return render(request, 'stories/playlists_list.html', context)
    except Exception as e:
        messages.error(request, f'Ошибка загрузки плейлистов: {e}')
        return redirect('stories:list')


# Добавим также метод для получения YouTube ID из Story модели
# (если его еще нет)

def get_youtube_id_from_embed(youtube_embed):
    """Извлекает YouTube ID из embed кода или URL"""
    import re
    
    # Различные паттерны для извлечения YouTube ID
    patterns = [
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/v/([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_embed)
        if match:
            return match.group(1)
    
    return None