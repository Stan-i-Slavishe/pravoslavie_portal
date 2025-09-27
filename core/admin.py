from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Tag, ContactMessage, SiteSettings, MobileFeedback

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'color_preview', 'is_active', 'order', 'created_at']
    list_filter = ['content_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description', 'content_type')
        }),
        ('Внешний вид', {
            'fields': ('icon', 'color', 'order'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    
    def color_preview(self, obj):
        """Превью цвета категории"""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Цвет'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def color_preview(self, obj):
        """Превью цвета тега"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{}</span>',
            obj.color,
            obj.name
        )
    color_preview.short_description = 'Превью'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'is_read', 'created_at']
    list_filter = ['status', 'subject', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']
    list_editable = ['status', 'is_read']
    
    fieldsets = (
        ('Информация о сообщении', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Статус', {
            'fields': ('status', 'is_read', 'admin_notes')
        }),
        ('Техническая информация', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Редактирование существующего объекта
            return self.readonly_fields + ['name', 'email', 'subject', 'message']
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_answered']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} сообщений отмечено как прочитанные.')
    mark_as_read.short_description = 'Отметить как прочитанные'
    
    def mark_as_answered(self, request, queryset):
        updated = queryset.update(status='answered', is_read=True)
        self.message_user(request, f'{updated} сообщений отмечено как отвеченные.')
    mark_as_answered.short_description = 'Отметить как отвеченные'

@admin.register(MobileFeedback)
class MobileFeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_type_display', 'message_preview', 'priority_badge', 'status_badge', 'user_info', 'is_read', 'created_at']
    list_filter = ['feedback_type', 'status', 'priority', 'is_read', 'created_at']
    search_fields = ['message', 'user__username', 'user__email', 'ip_address']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent', 'url', 'screen_resolution']
    list_editable = ['is_read']  # Оставляем только is_read
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация об обращении', {
            'fields': ('feedback_type', 'message', 'user')
        }),
        ('Статус и приоритет', {
            'fields': ('status', 'priority', 'is_read', 'assigned_to')
        }),
        ('Административные заметки', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
        ('Техническая информация', {
            'fields': ('url', 'user_agent', 'ip_address', 'screen_resolution', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def feedback_type_display(self, obj):
        """Красивое отображение типа обращения с иконками"""
        icons = {
            'bug': '🐛',
            'feature': '💡',
            'design': '🎨',
            'content': '📚',
            'performance': '⚡',
            'other': '💬'
        }
        icon = icons.get(obj.feedback_type, '📝')
        return format_html(
            '{} {}',
            icon,
            obj.get_feedback_type_display()
        )
    feedback_type_display.short_description = 'Тип обращения'
    
    def message_preview(self, obj):
        """Превью сообщения"""
        preview = obj.message[:80]
        if len(obj.message) > 80:
            preview += '...'
        return preview
    message_preview.short_description = 'Сообщение'
    
    def priority_badge(self, obj):
        """Бейдж приоритета"""
        color = obj.get_priority_color()
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Приоритет'
    
    def status_badge(self, obj):
        """Бейдж статуса"""
        colors = {
            'new': '#dc3545',
            'in_progress': '#ffc107',
            'resolved': '#28a745',
            'closed': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Статус'
    
    def user_info(self, obj):
        """Информация о пользователе"""
        if obj.user:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:auth_user_change', args=[obj.user.id]),
                obj.user.username
            )
        return 'Анонимный'
    user_info.short_description = 'Пользователь'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Редактирование существующего объекта
            return self.readonly_fields + ['feedback_type', 'message', 'user']
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_in_progress', 'mark_as_resolved', 'set_high_priority']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} обращений отмечено как прочитанные.')
    mark_as_read.short_description = 'Отметить как прочитанные'
    
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress', is_read=True)
        self.message_user(request, f'{updated} обращений взято в работу.')
    mark_as_in_progress.short_description = 'Взять в работу'
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved', is_read=True)
        self.message_user(request, f'{updated} обращений отмечено как решённые.')
    mark_as_resolved.short_description = 'Отметить как решённые'
    
    def set_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} обращений получили высокий приоритет.')
    set_high_priority.short_description = 'Установить высокий приоритет'

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основные настройки', {
            'fields': ('site_name', 'site_description')
        }),
        ('Контактная информация', {
            'fields': ('contact_email', 'contact_phone')
        }),
        # ⭐ НОВЫЕ СЕКЦИИ ДЛЯ РЕЖИМА РАБОТЫ И АДРЕСА
        ('Время работы', {
            'fields': ('work_hours', 'work_hours_note'),
            'description': 'Настройки рабочего времени для отображения на странице контактов'
        }),
        ('Адрес и местоположение', {
            'fields': ('address_city', 'address_country', 'address_full'),
            'description': 'Адресная информация для страницы контактов'
        }),
        # ⭐ НОВАЯ СЕКЦИЯ - УПРАВЛЕНИЕ НАВИГАЦИЕЙ
        ('Управление навигацией', {
            'fields': (
                'show_stories', 'stories_coming_soon',
                'show_books', 'books_coming_soon',
                'show_audio', 'audio_coming_soon',
                'show_fairy_tales', 'fairy_tales_coming_soon',
                'show_shop', 'shop_coming_soon',
            ),
            'description': 'Включение/отключение разделов в навигации и бейджи "Скоро"',
            'classes': ('wide',)
        }),
        ('Социальные сети', {
            'fields': ('social_telegram', 'social_youtube', 'social_vk'),
            'classes': ('collapse',)
        }),
        ('Режим обслуживания', {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'classes': ('collapse',)
        }),
        ('Аналитика', {
            'fields': ('analytics_yandex', 'analytics_google'),
            'classes': ('collapse',)
        }),
    )
    
    # Переопределяем changelist_view чтобы сразу перенаправлять на редактирование
    def changelist_view(self, request, extra_context=None):
        """Перенаправляем с списка на редактирование"""
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        
        # Получаем или создаём настройки
        settings = SiteSettings.get_settings()
        
        # Перенаправляем на страницу редактирования
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[settings.id])
        )
    
    def has_add_permission(self, request):
        # Запрещаем создание новых записей
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление настроек
        return False
    
    def has_change_permission(self, request, obj=None):
        # Всегда разрешаем редактирование
        return True

# Кастомизация заголовка админки
admin.site.site_header = 'Православный портал - Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.index_title = 'Добро пожаловать в панель управления'