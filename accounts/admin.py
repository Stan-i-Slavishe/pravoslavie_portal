from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_display_name', 'city', 'gender', 'created_at', 'last_activity', 'get_avatar_preview']
    list_filter = ['gender', 'email_notifications', 'newsletter_subscription', 'new_content_notifications', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'bio', 'city']
    readonly_fields = ['created_at', 'updated_at', 'last_activity', 'get_avatar_preview']
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user', 'get_avatar_preview', 'avatar')
        }),
        ('Личная информация', {
            'fields': ('bio', 'gender', 'birth_date', 'phone', 'city')
        }),
        ('Православные интересы', {
            'fields': ('favorite_saints', 'confession_frequency', 'favorite_prayers', 'parish')
        }),
        ('Настройки уведомлений', {
            'fields': ('email_notifications', 'newsletter_subscription', 'new_content_notifications', 'order_notifications')
        }),
        ('Настройки чтения', {
            'fields': ('preferred_font_size', 'preferred_theme')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at', 'last_activity'),
            'classes': ('collapse',)
        })
    )
    
    def get_display_name(self, obj):
        """Отображаемое имя пользователя"""
        return obj.get_display_name()
    get_display_name.short_description = 'Имя'
    
    def get_avatar_preview(self, obj):
        """Превью аватара в админке"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #f0f0f0; border-radius: 50%; display: flex; align-items: center; justify-content: center;">'
            '<i class="bi bi-person" style="font-size: 20px; color: #666;"></i>'
            '</div>'
        )
    get_avatar_preview.short_description = 'Аватар'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
