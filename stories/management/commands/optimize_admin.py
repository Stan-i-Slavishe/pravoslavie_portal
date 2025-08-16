from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db import connection
from stories.models import Story, Playlist, StoryComment


class Command(BaseCommand):
    help = 'Оптимизирует админку для лучшей производительности'

    def handle(self, *args, **options):
        self.stdout.write("Начинаем оптимизацию админки...")
        
        # 1. Создаем индексы для ускорения запросов
        self.create_database_indexes()
        
        # 2. Очищаем старый кеш
        self.clear_admin_cache()
        
        # 3. Предварительно прогреваем кеш
        self.warm_up_cache()
        
        self.stdout.write(
            self.style.SUCCESS('Оптимизация админки завершена успешно!')
        )

    def create_database_indexes(self):
        """Создает дополнительные индексы для ускорения админки"""
        with connection.cursor() as cursor:
            # Индексы для модели Story
            try:
                cursor.execute("""
                    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_story_admin_list 
                    ON stories_story(is_published, is_featured, created_at DESC);
                """)
                
                cursor.execute("""
                    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_story_views_count 
                    ON stories_story(views_count DESC);
                """)
                
                # Индексы для комментариев
                cursor.execute("""
                    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_comment_admin_list 
                    ON stories_storycomment(is_approved, created_at DESC);
                """)
                
                # Индексы для плейлистов
                cursor.execute("""
                    CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_playlist_admin_list 
                    ON stories_playlist(is_active, created_at DESC);
                """)
                
                self.stdout.write("✅ Индексы созданы")
                
            except Exception as e:
                self.stdout.write(f"⚠️ Ошибка создания индексов: {e}")

    def clear_admin_cache(self):
        """Очищает кеш админки"""
        cache_keys = [
            'admin_stories_count',
            'admin_comments_count',
            'admin_playlists_count',
            'admin_popular_stories',
        ]
        cache.delete_many(cache_keys)
        self.stdout.write("✅ Кеш очищен")

    def warm_up_cache(self):
        """Предварительно заполняет кеш часто используемыми данными"""
        # Кешируем количество записей для админки
        cache.set('admin_stories_count', Story.objects.count(), 3600)
        cache.set('admin_comments_count', StoryComment.objects.count(), 3600)
        cache.set('admin_playlists_count', Playlist.objects.count(), 3600)
        
        # Кешируем популярные рассказы
        popular_stories = list(
            Story.objects.select_related('category')
            .order_by('-views_count')[:10]
            .values('id', 'title', 'views_count')
        )
        cache.set('admin_popular_stories', popular_stories, 1800)
        
        self.stdout.write("✅ Кеш прогрет")
