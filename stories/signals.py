from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Story, StoryComment, Playlist, StoryLike


@receiver([post_save, post_delete], sender=Story)
def clear_story_cache(sender, **kwargs):
    """Очищает кеш при изменении рассказов"""
    cache_keys = [
        'admin_stories_count',
        'admin_popular_stories',
        'stories_list',
        'featured_stories'
    ]
    cache.delete_many(cache_keys)
    
    # Очищаем кеш списков админки (паттерн удаления)
    try:
        # Для Redis
        from django.core.cache.backends.redis import RedisCache
        if isinstance(cache, RedisCache):
            cache.delete_pattern('admin_stories_list_*')
    except:
        # Fallback - просто очищаем весь кеш админки
        cache.clear()


@receiver([post_save, post_delete], sender=StoryComment)
def clear_comment_cache(sender, **kwargs):
    """Очищает кеш при изменении комментариев"""
    cache.delete('admin_comments_count')
    
    try:
        from django.core.cache.backends.redis import RedisCache
        if isinstance(cache, RedisCache):
            cache.delete_pattern('admin_comments_list_*')
    except:
        pass


@receiver([post_save, post_delete], sender=Playlist)
def clear_playlist_cache(sender, **kwargs):
    """Очищает кеш при изменении плейлистов"""
    cache.delete('admin_playlists_count')
    
    try:
        from django.core.cache.backends.redis import RedisCache
        if isinstance(cache, RedisCache):
            cache.delete_pattern('admin_playlists_list_*')
    except:
        pass


@receiver([post_save, post_delete], sender=StoryLike)
def clear_like_cache(sender, **kwargs):
    """Очищает кеш при изменении лайков"""
    instance = kwargs.get('instance')
    if instance and instance.story_id:
        cache_keys = [
            f'story_likes_{instance.story_id}',
            f'story_detail_{instance.story.slug}',
            'admin_popular_stories'
        ]
        cache.delete_many(cache_keys)
