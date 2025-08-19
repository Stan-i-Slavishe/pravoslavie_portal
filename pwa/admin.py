# PWA Admin for Православный портал

from django.contrib import admin
from .models import PushSubscription, PWAInstallEvent, OfflineAction, PWAAnalytics, CachedContent

@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'endpoint_short', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'endpoint']
    readonly_fields = ['created_at', 'updated_at']
    
    def endpoint_short(self, obj):
        return obj.endpoint[:50] + '...' if len(obj.endpoint) > 50 else obj.endpoint
    endpoint_short.short_description = 'Endpoint'

@admin.register(PWAInstallEvent)
class PWAInstallEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'browser', 'installed_at']
    list_filter = ['platform', 'browser', 'installed_at']
    search_fields = ['user__username', 'user__email', 'user_agent']
    readonly_fields = ['installed_at']

@admin.register(OfflineAction)
class OfflineActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'content_type', 'object_id', 'is_synced', 'created_at']
    list_filter = ['action_type', 'content_type', 'is_synced', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'synced_at']
    actions = ['mark_as_synced']
    
    def mark_as_synced(self, request, queryset):
        count = 0
        for action in queryset:
            if not action.is_synced:
                action.mark_synced()
                count += 1
        self.message_user(request, f'{count} действий помечено как синхронизированных.')
    mark_as_synced.short_description = 'Пометить как синхронизированные'

@admin.register(PWAAnalytics)
class PWAAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']

@admin.register(CachedContent)
class CachedContentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'cache_size_mb', 'access_count', 'last_accessed']
    list_filter = ['content_type', 'created_at', 'last_accessed']
    search_fields = ['user__username', 'user__email', 'cache_key']
    readonly_fields = ['created_at', 'last_accessed']
    
    def cache_size_mb(self, obj):
        return f"{obj.cache_size / 1024 / 1024:.2f} MB"
    cache_size_mb.short_description = 'Размер кеша'
