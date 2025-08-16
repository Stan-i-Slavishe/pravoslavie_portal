from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.core.cache import cache
from .models import (
    Story, StoryLike, 
    Playlist, PlaylistItem, StoryView, StoryRecommendation,
    SearchQuery, UserRecommendation, UserWatchHistory,
    StoryComment, CommentReaction, CommentReport
)


# ==========================================
# ОПТИМИЗИРОВАННАЯ АДМИНКА ДЛЯ STORIES
# ==========================================

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'category', 
        'views_count', 
        'likes_count_display',
        'comments_count_display',
        'is_featured', 
        'is_published', 
        'created_at'
    ]
    list_filter = [
        'is_published', 
        'is_featured', 
        'category', 
        'created_at'
    ]
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = [
        'views_count', 
        'youtube_embed_id', 
        'created_at', 
        'updated_at',
        'likes_count_display',
        'comments_count_display'
    ]
    
    # КРИТИЧНО: Оптимизируем запросы
    list_select_related = ['category']
    list_prefetch_related = ['tags', 'likes', 'comments']
    
    # Уменьшаем количество элементов на странице
    list_per_page = 25
    list_max_show_all = 100
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description')
        }),
        ('YouTube видео', {
            'fields': ('youtube_url', 'youtube_embed_id'),
            'description': 'Вставьте ссылку на YouTube видео. ID будет извлечен автоматически.'
        }),
        ('Медиа', {
            'fields': ('thumbnail', 'duration'),
            'classes': ('collapse',)
        }),
        ('Категоризация', {
            'fields': ('category', 'tags')
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Статистика', {
            'fields': (
                'views_count', 
                'likes_count_display',
                'comments_count_display',
                'created_at', 
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Оптимизированный QuerySet с минимальными JOIN'ами"""
        return super().get_queryset(request).select_related(
            'category'
        ).prefetch_related(
            models.Prefetch(
                'likes',
                queryset=StoryLike.objects.select_related('user')
            ),
            models.Prefetch(
                'comments',
                queryset=StoryComment.objects.filter(is_approved=True)
            )
        ).annotate(
            # Добавляем аннотации для подсчетов прямо в SQL
            total_likes=models.Count('likes', distinct=True),
            total_comments=models.Count('comments', filter=models.Q(comments__is_approved=True), distinct=True)
        )

    def likes_count_display(self, obj):
        """Оптимизированный подсчет лайков"""
        # Используем аннотацию вместо дополнительных запросов
        return getattr(obj, 'total_likes', obj.likes.count())
    likes_count_display.short_description = "👍 Лайки"
    likes_count_display.admin_order_field = 'total_likes'

    def comments_count_display(self, obj):
        """Оптимизированный подсчет комментариев"""
        # Используем аннотацию вместо дополнительных запросов
        return getattr(obj, 'total_comments', obj.comments.filter(is_approved=True).count())
    comments_count_display.short_description = "💬 Комментарии"
    comments_count_display.admin_order_field = 'total_comments'

    def save_model(self, request, obj, form, change):
        """Оптимизированное сохранение"""
        if obj.youtube_url and not obj.youtube_embed_id:
            obj.youtube_embed_id = obj.extract_youtube_id(obj.youtube_url)
        
        super().save_model(request, obj, form, change)
        
        # Очищаем кеш после изменений
        cache_keys = [
            f'story_detail_{obj.slug}',
            'stories_list',
            'featured_stories'
        ]
        cache.delete_many(cache_keys)

    class Media:
        css = {
            'all': ('admin/css/stories_admin.css',)
        }


# ==========================================
# ОПТИМИЗИРОВАННАЯ АДМИНКА ДЛЯ ПЛЕЙЛИСТОВ
# ==========================================

class PlaylistItemInline(admin.TabularInline):
    """Оптимизированный инлайн для элементов плейлиста"""
    model = PlaylistItem
    extra = 0
    min_num = 0
    max_num = 20  # Ограничиваем количество инлайнов
    fields = ['story', 'order']
    ordering = ['order']
    autocomplete_fields = ['story']
    
    # Оптимизируем запросы для инлайна
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('story')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'creator',
        'story_count_display',
        'playlist_type',
        'is_active',
        'views_count', 
        'created_at'
    ]
    list_filter = [
        'playlist_type',
        'is_active',
        'created_at',
        'creator'
    ]
    search_fields = ['title', 'description', 'creator__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [PlaylistItemInline]
    
    # КРИТИЧНО: Оптимизация
    list_select_related = ['creator']
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'creator')
        }),
        ('Настройки', {
            'fields': ('playlist_type', 'is_active', 'cover_image')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Оптимизированный QuerySet с аннотациями"""
        return super().get_queryset(request).select_related(
            'creator'
        ).annotate(
            items_count=models.Count('playlist_items', distinct=True)
        )
    
    def story_count_display(self, obj):
        """Используем аннотацию для подсчета"""
        return getattr(obj, 'items_count', 0)
    story_count_display.short_description = "Кол-во рассказов"
    story_count_display.admin_order_field = 'items_count'


# ==========================================
# УПРОЩЕННЫЕ АДМИНКИ ДЛЯ ВСПОМОГАТЕЛЬНЫХ МОДЕЛЕЙ
# ==========================================

@admin.register(StoryLike)
class StoryLikeAdmin(admin.ModelAdmin):
    list_display = ['story_title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['story__title', 'user__username']
    readonly_fields = ['created_at']
    list_select_related = ['story', 'user']
    list_per_page = 50
    
    def story_title(self, obj):
        return obj.story.title
    story_title.short_description = "Рассказ"
    story_title.admin_order_field = 'story__title'


@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = [
        'story_title', 
        'user_display', 
        'view_count', 
        'last_viewed'
    ]
    list_filter = [
        'last_viewed', 
        ('story', admin.RelatedOnlyFieldListFilter)
    ]
    search_fields = ['story__title', 'user__username']
    readonly_fields = ['first_viewed', 'last_viewed']
    date_hierarchy = 'last_viewed'
    list_select_related = ['story', 'user']
    list_per_page = 100
    
    def story_title(self, obj):
        return obj.story.title
    story_title.short_description = "Рассказ"
    story_title.admin_order_field = 'story__title'
    
    def user_display(self, obj):
        return obj.user.username if obj.user else f"IP: {obj.ip_address}"
    user_display.short_description = "Пользователь"


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'count', 'last_searched']
    list_filter = ['last_searched']
    search_fields = ['query']
    readonly_fields = ['created_at', 'last_searched']
    ordering = ['-count', '-last_searched']
    list_per_page = 50


# ==========================================
# ОПТИМИЗИРОВАННАЯ АДМИНКА КОММЕНТАРИЕВ
# ==========================================

@admin.register(StoryComment)
class StoryCommentAdmin(admin.ModelAdmin):
    list_display = [
        'comment_preview',
        'user',
        'story_title',
        'reaction_score',
        'replies_count',
        'is_approved',
        'created_at'
    ]
    list_filter = [
        'is_approved',
        'is_pinned',
        'created_at',
        ('story', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter)
    ]
    search_fields = [
        'text',
        'user__username',
        'story__title'
    ]
    readonly_fields = [
        'likes_count',
        'dislikes_count',
        'replies_count',
        'created_at',
        'updated_at'
    ]
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    # КРИТИЧНО: Оптимизация
    list_select_related = ['user', 'story', 'parent']
    list_per_page = 30
    
    def get_queryset(self, request):
        """Оптимизированный QuerySet"""
        return super().get_queryset(request).select_related(
            'user', 'story', 'parent__user'
        ).annotate(
            # Считаем реакции в SQL
            total_likes=models.Count(
                'reactions',
                filter=models.Q(reactions__reaction_type='like'),
                distinct=True
            ),
            total_dislikes=models.Count(
                'reactions',
                filter=models.Q(reactions__reaction_type='dislike'),
                distinct=True
            )
        )
    
    def story_title(self, obj):
        return obj.story.title
    story_title.short_description = "Рассказ"
    story_title.admin_order_field = 'story__title'
    
    def comment_preview(self, obj):
        """Краткое превью комментария"""
        preview = obj.text[:80]
        if len(obj.text) > 80:
            preview += '...'
        
        if obj.parent:
            return format_html(
                '<div style="margin-left: 20px; color: #666;">↳ {}</div>',
                preview
            )
        return format_html('<div>{}</div>', preview)
    comment_preview.short_description = 'Комментарий'
    
    def reaction_score(self, obj):
        """Оптимизированный счет реакций"""
        likes = getattr(obj, 'total_likes', obj.likes_count)
        dislikes = getattr(obj, 'total_dislikes', obj.dislikes_count)
        score = likes - dislikes
        
        if score > 0:
            return format_html('<span style="color: green;">+{}</span>', score)
        elif score < 0:
            return format_html('<span style="color: red;">{}</span>', score)
        return score
    reaction_score.short_description = 'Рейтинг'
    
    # Упрощенные действия
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} комментариев одобрено.')
    approve_comments.short_description = 'Одобрить выбранные'
    
    def disapprove_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} комментариев скрыто.')
    disapprove_comments.short_description = 'Скрыть выбранные'


# ==========================================
# УПРОЩЕННЫЕ АДМИНКИ ДЛЯ ОСТАЛЬНЫХ МОДЕЛЕЙ
# ==========================================

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ['comment_id', 'user', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    list_select_related = ['user', 'comment']
    list_per_page = 100
    
    def comment_id(self, obj):
        return f"Комментарий #{obj.comment.id}"
    comment_id.short_description = 'Комментарий'


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ['playlist_title', 'story_title', 'order']
    list_filter = [
        ('playlist', admin.RelatedOnlyFieldListFilter),
        'added_at'
    ]
    search_fields = ['playlist__title', 'story__title']
    ordering = ['playlist', 'order']
    readonly_fields = ['added_at']
    list_select_related = ['playlist', 'story']
    list_per_page = 50
    
    def playlist_title(self, obj):
        return obj.playlist.title
    playlist_title.short_description = "Плейлист"
    playlist_title.admin_order_field = 'playlist__title'
    
    def story_title(self, obj):
        return obj.story.title
    story_title.short_description = "Рассказ"
    story_title.admin_order_field = 'story__title'


# Упрощенные регистрации для редко используемых моделей
admin.site.register(StoryRecommendation)
admin.site.register(UserRecommendation)
admin.site.register(UserWatchHistory)
admin.site.register(CommentReport)


# ==========================================
# НАСТРОЙКИ АДМИНИСТРИРОВАНИЯ
# ==========================================

# Кастомизация заголовков админки
admin.site.site_header = "Православный портал - Администрирование"
admin.site.site_title = "Админ панель"
admin.site.index_title = "Добро пожаловать в админ панель"
