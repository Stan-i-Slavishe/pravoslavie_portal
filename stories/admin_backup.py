from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Story, 
    Playlist, PlaylistItem, StoryView, StoryRecommendation,
    StoryComment, CommentReaction, CommentReport
)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'category', 
        'views_count', 
        'is_featured', 
        'is_published', 
        'created_at',
        'youtube_preview'
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
    readonly_fields = ['views_count', 'youtube_embed_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description')
        }),
        ('YouTube видео', {
            'fields': ('youtube_url', 'youtube_embed_id'),
            'description': 'Вставьте ссылку на YouTube видео. ID будет извлечен автоматически.'
        }),
        ('Категоризация', {
            'fields': ('category', 'tags')
        }),
        ('Настройки публикации', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def youtube_preview(self, obj):
        """Показывает превью YouTube видео в админке"""
        if obj.youtube_embed_id:
            embed_url = obj.get_youtube_embed_url()
            return format_html(
                '<iframe width="200" height="113" src="{}" frameborder="0" allowfullscreen></iframe>',
                embed_url
            )
        return "Видео не загружено"
    youtube_preview.short_description = "Превью видео"

    def save_model(self, request, obj, form, change):
        """Автоматически извлекает YouTube ID при сохранении"""
        if obj.youtube_url and not obj.youtube_embed_id:
            obj.youtube_embed_id = obj.extract_youtube_id(obj.youtube_url)
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/stories_admin.css',)
        }


@admin.register(StoryLike)
class StoryLikeAdmin(admin.ModelAdmin):
    list_display = ['story', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['story__title', 'user__username']
    readonly_fields = ['created_at']


# ==========================================
# АДМИНКА ДЛЯ НОВЫХ МОДЕЛЕЙ ПЛЕЙЛИСТОВ
# ==========================================

class PlaylistItemInline(admin.TabularInline):
    """Инлайн для элементов плейлиста"""
    model = PlaylistItem
    extra = 0
    min_num = 0
    fields = ['story', 'order']
    ordering = ['order']
    autocomplete_fields = ['story']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = [
        'title',  # Используем существующее поле
        'creator',  # Используем существующее поле
        'story_count_display',
        'playlist_type',  # Используем существующее поле
        'is_active',  # Используем существующее поле
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
    prepopulated_fields = {'slug': ('title',)}  # Правильное поле
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [PlaylistItemInline]
    
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
    
    def story_count_display(self, obj):
        """Показывает количество рассказов в плейлисте"""
        return obj.stories_count
    story_count_display.short_description = "Кол-во рассказов"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creator')


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'story', 'order', 'added_at']
    list_filter = ['playlist', 'added_at']
    search_fields = ['playlist__title', 'story__title']
    ordering = ['playlist', 'order']
    autocomplete_fields = ['playlist', 'story']
    readonly_fields = ['added_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('playlist', 'story')


@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = [
        'story', 
        'user_display', 
        'ip_address', 
        'view_count', 
        'first_viewed',
        'last_viewed'
    ]
    list_filter = [
        'first_viewed',
        'last_viewed', 
        'story'
    ]
    search_fields = ['story__title', 'user__username', 'ip_address']
    readonly_fields = ['first_viewed', 'last_viewed']
    date_hierarchy = 'first_viewed'
    
    def user_display(self, obj):
        """Показывает пользователя или IP"""
        return obj.user.username if obj.user else f"IP: {obj.ip_address}"
    user_display.short_description = "Пользователь"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('story', 'user')


@admin.register(StoryRecommendation)
class StoryRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        'source_story', 
        'recommended_story', 
        'similarity_score',
        'recommendation_type',
        'created_at'
    ]
    list_filter = [
        'recommendation_type',
        'created_at',
        'similarity_score'
    ]
    search_fields = [
        'source_story__title', 
        'recommended_story__title'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['source_story', 'recommended_story']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'source_story', 
            'recommended_story'
        )


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'count', 'last_searched', 'created_at']
    list_filter = ['last_searched', 'created_at']
    search_fields = ['query']
    readonly_fields = ['created_at', 'last_searched']
    ordering = ['-count', '-last_searched']


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'story', 
        'score', 
        'reason', 
        'is_viewed',
        'created_at'
    ]
    list_filter = [
        'reason',
        'is_viewed', 
        'created_at'
    ]
    search_fields = ['user__username', 'story__title']
    readonly_fields = ['created_at']
    list_editable = ['is_viewed']
    autocomplete_fields = ['user', 'story']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'story')


# ==========================================
# YOUTUBE-STYLE КОММЕНТАРИИ АДМИНКА
# ==========================================

class CommentReactionInline(admin.TabularInline):
    """Инлайн для реакций на комментарий"""
    model = CommentReaction
    extra = 0
    readonly_fields = ['created_at']
    fields = ['user', 'reaction_type', 'created_at']


@admin.register(StoryComment)
class StoryCommentAdmin(admin.ModelAdmin):
    list_display = [
        'comment_preview',
        'user',
        'story',
        'parent_info',
        'reaction_score',
        'replies_count',
        'is_approved',
        'is_pinned',
        'created_at'
    ]
    list_filter = [
        'is_approved',
        'is_pinned',
        'is_edited',
        'created_at',
        'story__category'
    ]
    search_fields = [
        'text',
        'user__username',
        'user__email',
        'story__title'
    ]
    readonly_fields = [
        'likes_count',
        'dislikes_count',
        'replies_count',
        'created_at',
        'updated_at',
        'reaction_score_display'
    ]
    list_editable = ['is_approved', 'is_pinned']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [CommentReactionInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('story', 'user', 'parent', 'text')
        }),
        ('Модерация', {
            'fields': ('is_approved', 'is_pinned', 'is_edited')
        }),
        ('Статистика', {
            'fields': (
                'likes_count', 'dislikes_count', 'replies_count',
                'reaction_score_display', 'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def comment_preview(self, obj):
        """Превью комментария"""
        preview = obj.text[:100]
        if len(obj.text) > 100:
            preview += '...'
        
        if obj.is_reply:
            return format_html(
                '<div style="margin-left: 20px; color: #666;">↳ {}</div>',
                preview
            )
        return format_html('<strong>{}</strong>', preview)
    comment_preview.short_description = 'Комментарий'
    
    def parent_info(self, obj):
        """Информация о родительском комментарии"""
        if obj.parent:
            return format_html(
                'Ответ на: <a href="{}">#{}</a>',
                f'/admin/stories/storycomment/{obj.parent.id}/change/',
                obj.parent.id
            )
        return 'Основной комментарий'
    parent_info.short_description = 'Тип'
    
    def reaction_score(self, obj):
        """Общий счет реакций"""
        score = obj.get_reaction_score()
        if score > 0:
            return format_html('<span style="color: green;">+{}</span>', score)
        elif score < 0:
            return format_html('<span style="color: red;">{}</span>', score)
        return score
    reaction_score.short_description = 'Рейтинг'
    
    def reaction_score_display(self, obj):
        """Подробный счет реакций"""
        return f'Лайки: {obj.likes_count} | Дизлайки: {obj.dislikes_count} | Общий: {obj.get_reaction_score()}'
    reaction_score_display.short_description = 'Подробная статистика'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'story', 'parent__user'
        ).prefetch_related('reactions')
    
    actions = ['approve_comments', 'disapprove_comments', 'pin_comments', 'unpin_comments']
    
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} комментариев одобрено.')
    approve_comments.short_description = 'Одобрить выбранные комментарии'
    
    def disapprove_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} комментариев скрыто.')
    disapprove_comments.short_description = 'Скрыть выбранные комментарии'
    
    def pin_comments(self, request, queryset):
        count = queryset.update(is_pinned=True)
        self.message_user(request, f'{count} комментариев закреплено.')
    pin_comments.short_description = 'Закрепить выбранные комментарии'
    
    def unpin_comments(self, request, queryset):
        count = queryset.update(is_pinned=False)
        self.message_user(request, f'{count} комментариев откреплено.')
    unpin_comments.short_description = 'Открепить выбранные комментарии'


@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ['comment_preview', 'user', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['comment__text', 'user__username', 'comment__story__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def comment_preview(self, obj):
        """Превью комментария для реакции"""
        return format_html(
            '<a href="{}">{}</a>',
            f'/admin/stories/storycomment/{obj.comment.id}/change/',
            obj.comment.text[:50] + '...'
        )
    comment_preview.short_description = 'Комментарий'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'comment__user', 'comment__story', 'user'
        )


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = [
        'comment_preview',
        'reporter',
        'reason',
        'is_resolved',
        'created_at'
    ]
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = [
        'comment__text',
        'reporter__username',
        'description',
        'comment__story__title'
    ]
    readonly_fields = ['created_at']
    list_editable = ['is_resolved']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация о жалобе', {
            'fields': ('comment', 'reporter', 'reason', 'description')
        }),
        ('Статус', {
            'fields': ('is_resolved', 'created_at')
        }),
    )
    
    def comment_preview(self, obj):
        """Превью комментария для жалобы"""
        return format_html(
            '<a href="{}" style="color: {}">{}</a>',
            f'/admin/stories/storycomment/{obj.comment.id}/change/',
            'red' if not obj.comment.is_approved else 'black',
            obj.comment.text[:50] + '...'
        )
    comment_preview.short_description = 'Комментарий'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'comment__user', 'comment__story', 'reporter'
        )
    
    actions = ['resolve_reports', 'unresolve_reports']
    
    def resolve_reports(self, request, queryset):
        count = queryset.update(is_resolved=True)
        self.message_user(request, f'{count} жалоб отмечено как рассмотренные.')
    resolve_reports.short_description = 'Отметить как рассмотренные'
    
    def unresolve_reports(self, request, queryset):
        count = queryset.update(is_resolved=False)
        self.message_user(request, f'{count} жалоб отмечено как нерассмотренные.')
    unresolve_reports.short_description = 'Отметить как нерассмотренные'


@admin.register(UserWatchHistory)
class UserWatchHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'story', 
        'watched_at',
        'watch_duration_display',
        'completed'
    ]
    list_filter = [
        'completed',
        'watched_at'
    ]
    search_fields = ['user__username', 'story__title']
    readonly_fields = ['watched_at']
    date_hierarchy = 'watched_at'
    autocomplete_fields = ['user', 'story']
    
    def watch_duration_display(self, obj):
        """Показывает длительность в читаемом формате"""
        minutes = obj.watch_duration // 60
        seconds = obj.watch_duration % 60
        return f"{minutes}:{seconds:02d}"
    watch_duration_display.short_description = "Длительность"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'story')
