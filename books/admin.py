from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Tag, Book, BookReview, BookDownload, UserFavoriteBook

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'books_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def books_count(self, obj):
        return obj.book_set.count()
    books_count.short_description = 'Количество книг'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'books_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def books_count(self, obj):
        return obj.book_set.count()
    books_count.short_description = 'Количество книг'

class BookReviewInline(admin.TabularInline):
    model = BookReview
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']
    can_delete = True

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'author', 
        'category', 
        'format', 
        'price_display',
        'is_free', 
        'downloads_count', 
        'rating', 
        'is_published',
        'is_featured',
        'created_at'
    ]
    list_filter = [
        'is_published', 
        'is_featured', 
        'is_free', 
        'format', 
        'category', 
        'created_at',
        'published_at'
    ]
    search_fields = ['title', 'author', 'description', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['downloads_count', 'views_count', 'created_at', 'updated_at', 'cover_preview']
    inlines = [BookReviewInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'description', 'content')
        }),
        ('Медиа', {
            'fields': ('cover', 'cover_preview', 'file')
        }),
        ('Категоризация', {
            'fields': ('category', 'tags', 'format')
        }),
        ('Ценообразование', {
            'fields': ('price', 'is_free')
        }),
        ('Метаданные', {
            'fields': ('isbn', 'pages', 'language', 'publisher', 'publication_year')
        }),
        ('Статус и публикация', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('Статистика', {
            'fields': ('downloads_count', 'views_count', 'rating'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        if obj.is_free:
            return format_html('<span style="color: green; font-weight: bold;">Бесплатно</span>')
        return f'{obj.price} ₽'
    price_display.short_description = 'Цена'
    
    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 300px; object-fit: cover;">',
                obj.cover.url
            )
        return 'Нет обложки'
    cover_preview.short_description = 'Предварительный просмотр обложки'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('tags')
    
    actions = ['make_published', 'make_unpublished', 'make_featured', 'make_free']
    
    def make_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} книг(и) опубликованы.')
    make_published.short_description = 'Опубликовать выбранные книги'
    
    def make_unpublished(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} книг(и) сняты с публикации.')
    make_unpublished.short_description = 'Снять с публикации выбранные книги'
    
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} книг(и) добавлены в рекомендуемые.')
    make_featured.short_description = 'Добавить в рекомендуемые'
    
    def make_free(self, request, queryset):
        count = queryset.update(is_free=True, price=0)
        self.message_user(request, f'{count} книг(и) стали бесплатными.')
    make_free.short_description = 'Сделать бесплатными'

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at', 'review_preview']
    list_filter = ['rating', 'created_at', 'book__category']
    search_fields = ['book__title', 'user__username', 'comment']
    readonly_fields = ['created_at']
    
    def review_preview(self, obj):
        if obj.comment:
            return obj.comment[:100] + '...' if len(obj.comment) > 100 else obj.comment
        return 'Без отзыва'
    review_preview.short_description = 'Отзыв'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'user')

@admin.register(BookDownload)
class BookDownloadAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'ip_address', 'downloaded_at']
    list_filter = ['downloaded_at', 'book__category']
    search_fields = ['book__title', 'user__username', 'ip_address']
    readonly_fields = ['downloaded_at']
    date_hierarchy = 'downloaded_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'user')

@admin.register(UserFavoriteBook)
class UserFavoriteBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_at']
    list_filter = ['added_at', 'book__category']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['added_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'user')

# Дополнительные настройки админки
admin.site.site_header = 'Православный портал - Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.index_title = 'Добро пожаловать в панель управления'
