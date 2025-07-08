# Дополнительная функция для получения содержимого плейлистов
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def get_playlist_content(request, playlist_slug):
    """
    API endpoint для получения содержимого плейлиста
    Для модального окна просмотра плейлиста
    """
    try:
        stories = []
        
        # Определяем тип плейлиста по slug
        if playlist_slug == 'watch-later':
            # Системный плейлист "Посмотреть позже"
            stories = get_mock_playlist_data('watch-later')
                    
        elif playlist_slug == 'favorites':
            # Системный плейлист "Мне нравится"
            stories = get_mock_playlist_data('favorites')
                    
        elif playlist_slug in ['playlist-1', 'playlist-2', 'playlist-3']:
            # Пользовательские плейлисты (временные моковые данные)
            stories = get_mock_playlist_data(playlist_slug)
                
        else:
            # Пытаемся найти реальный плейлист
            try:
                from .models import Playlist, PlaylistItem
                playlist = Playlist.objects.get(slug=playlist_slug)
                
                # Проверяем доступ
                if not playlist.is_public:
                    if not request.user.is_authenticated or playlist.user != request.user:
                        return JsonResponse({
                            'success': False,
                            'message': 'Нет доступа к этому плейлисту'
                        }, status=403)
                
                playlist_items = PlaylistItem.objects.filter(
                    playlist=playlist
                ).select_related('story').order_by('position', '-added_at')[:50]
                
                stories = [format_story_data(item.story) for item in playlist_items]
                
            except Exception as e:
                # Если плейлист не найден, возвращаем моковые данные
                stories = get_mock_playlist_data('empty')
        
        return JsonResponse({
            'success': True,
            'stories': stories,
            'count': len(stories)
        })
        
    except Exception as e:
        logger.error(f'Ошибка получения содержимого плейлиста: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Ошибка сервера'
        }, status=500)


def get_mock_playlist_data(playlist_type):
    """
    Возвращает моковые данные для демонстрации плейлистов
    """
    base_stories = [
        {
            'id': 1,
            'title': 'Как св. Пантелеймон здоровье восстановил',
            'slug': 'kak-sv-pantelejmon-zdorove-vosstanovil',
            'description': 'Правдивый рассказ о чудесном исцелении крестьянина Игнатия Мокеева, произошедшем в 1891 году в деревне Скачкова.',
            'views_count': 127,
            'created_at': '2025-07-06T10:30:00Z',
            'youtube_thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'duration': '12:34'
        },
        {
            'id': 2,
            'title': 'Святитель Николай и морские чудеса',
            'slug': 'svyatitel-nikolaj-i-morskie-chudesa',
            'description': 'Удивительные истории о помощи святителя Николая морякам и путешественникам.',
            'views_count': 89,
            'created_at': '2025-07-05T14:15:00Z',
            'youtube_thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'duration': '8:45'
        },
        {
            'id': 3,
            'title': 'Преподобный Сергий и медведь',
            'slug': 'prepodobnyj-sergij-i-medved',
            'description': 'Трогательная история о дружбе святого с лесным зверем.',
            'views_count': 203,
            'created_at': '2025-07-04T09:20:00Z',
            'youtube_thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'duration': '6:12'
        },
        {
            'id': 4,
            'title': 'Чудо Георгия Победоносца',
            'slug': 'chudo-georgiya-pobedonosca',
            'description': 'Легенда о святом воине и его победе над злом.',
            'views_count': 156,
            'created_at': '2025-07-03T16:45:00Z',
            'youtube_thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'duration': '10:28'
        },
        {
            'id': 5,
            'title': 'Матрона Московская и её предсказания',
            'slug': 'matrona-moskovskaya-i-ee-predskazaniya',
            'description': 'Рассказы о прозорливости блаженной старицы.',
            'views_count': 342,
            'created_at': '2025-07-02T11:30:00Z',
            'youtube_thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'duration': '15:17'
        }
    ]
    
    if playlist_type == 'watch-later':
        return base_stories[:5]  # Все 5 видео
    elif playlist_type == 'favorites':
        return base_stories[1:4]  # 3 видео (с индексами 1, 2, 3)
    elif playlist_type == 'playlist-1':  # "Отлично"
        return base_stories[:2]  # 2 видео
    elif playlist_type == 'playlist-2':  # "Левый"
        return base_stories[4:5]  # 1 видео
    elif playlist_type == 'playlist-3':  # "Тестовый плей лист"
        return base_stories[2:5]  # 3 видео
    else:
        return []  # Пустой плейлист


def format_story_data(story):
    """
    Форматирует данные рассказа для JSON ответа
    """
    return {
        'id': story.id,
        'title': story.title,
        'slug': story.slug,
        'description': story.description or '',
        'views_count': story.views_count or 0,
        'created_at': story.created_at.isoformat() if story.created_at else None,
        'youtube_thumbnail': get_youtube_thumbnail(story.youtube_embed_id) if hasattr(story, 'youtube_embed_id') and story.youtube_embed_id else None,
        'duration': None  # Можно добавить поле duration в модель Story
    }


def get_youtube_thumbnail(youtube_id):
    """
    Генерирует URL миниатюры YouTube видео
    """
    if not youtube_id:
        return None
    return f"https://img.youtube.com/vi/{youtube_id}/mqdefault.jpg"
