from django.contrib import admin
from .models import Subscription, UserSubscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'subscription_type', 'price', 'duration_months', 'is_active', 'created_at']
    list_filter = ['subscription_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']
    ordering = ['subscription_type', 'price']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'subscription_type', 'price', 'duration_months')
        }),
        ('Описание и возможности', {
            'fields': ('description', 'features')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'subscription', 'auto_renew', 'created_at']
    search_fields = ['user__username', 'user__email', 'subscription__name']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Подписка', {
            'fields': ('user', 'subscription', 'status')
        }),
        ('Период действия', {
            'fields': ('start_date', 'end_date', 'auto_renew')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # При редактировании
            return self.readonly_fields + ['user', 'subscription']
        return self.readonly_fields
