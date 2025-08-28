# PWA Admin for Православный портал

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PushSubscription, PWAInstallEvent, OfflineAction, PWAAnalytics, CachedContent,
    NotificationCategory, UserNotificationSettings, UserNotificationSubscription,
    OrthodoxEvent, DailyOrthodoxInfo, FastingPeriod
)

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

# =============================================================================
# 🔔 АДМИНКА ДЛЯ СИСТЕМЫ УВЕДОМЛЕНИЙ
# =============================================================================

@admin.register(NotificationCategory)
class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'name', 'is_active', 'default_enabled', 'created_at']
    list_filter = ['is_active', 'default_enabled', 'created_at']
    search_fields = ['title', 'name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'title', 'description', 'icon')
        }),
        ('Настройки', {
            'fields': ('is_active', 'default_enabled')
        })
    )

@admin.register(UserNotificationSettings)
class UserNotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'notifications_enabled', 'quiet_hours_enabled', 'child_mode', 'created_at']
    list_filter = ['notifications_enabled', 'quiet_hours_enabled', 'child_mode', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Общие настройки', {
            'fields': ('user', 'notifications_enabled', 'timezone')
        }),
        ('Тихие часы', {
            'fields': ('quiet_hours_enabled', 'quiet_start', 'quiet_end')
        }),
        ('Дни недели', {
            'fields': ('notify_monday', 'notify_tuesday', 'notify_wednesday', 
                      'notify_thursday', 'notify_friday', 'notify_saturday', 'notify_sunday'),
            'classes': ('collapse',)
        }),
        ('Детский режим', {
            'fields': ('child_mode', 'child_bedtime')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserNotificationSubscription)
class UserNotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'enabled', 'frequency', 'priority', 'created_at']
    list_filter = ['enabled', 'frequency', 'priority', 'category', 'created_at']
    search_fields = ['user__username', 'user__email', 'category__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'category', 'enabled')
        }),
        ('Настройки уведомлений', {
            'fields': ('frequency', 'preferred_time', 'max_daily_count', 'priority')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# =============================================================================
# 🗓️ АДМИНКА ПРАВОСЛАВНОГО КАЛЕНДАРЯ
# =============================================================================

@admin.register(OrthodoxEvent)
class OrthodoxEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type_colored', 'date_display', 'is_movable', 'easter_offset']
    list_filter = ['event_type', 'is_movable', 'month']
    search_fields = ['title', 'description']
    ordering = ['month', 'day']
    list_per_page = 50
    
    # Цветное отображение типов событий
    def event_type_colored(self, obj):
        colors = {
            'great_feast': '#dc3545',  # красный
            'major_feast': '#fd7e14',  # оранжевый
            'minor_feast': '#ffc107',  # желтый
            'fast': '#6f42c1',         # фиолетовый
            'fast_day': '#6610f2',     # индиго
            'saint': '#198754',        # зеленый
            'icon': '#0dcaf0',         # голубой
            'memorial': '#6c757d',     # серый
        }
        color = colors.get(obj.event_type, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_event_type_display()
        )
    event_type_colored.short_description = 'Тип события'
    
    # Красивое отображение даты
    def date_display(self, obj):
        if obj.is_movable:
            from datetime import date
            current_year = date.today().year
            event_date = obj.get_date_for_year(current_year)
            return format_html(
                '<strong>{}</strong><br><small style="color: #666;">(переходящий)</small>',
                event_date.strftime('%d.%m')
            )
        else:
            return f"{obj.day:02d}.{obj.month:02d}"
    date_display.short_description = 'Дата'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Дата', {
            'fields': ('month', 'day', 'year', 'is_old_style')
        }),
        ('Переходящие праздники', {
            'fields': ('is_movable', 'easter_offset'),
            'classes': ('collapse',),
            'description': 'Для праздников, зависящих от даты Пасхи'
        }),
        ('Дополнительно', {
            'fields': ('icon_url', 'reading_url'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['calculate_dates_for_year', 'export_calendar']
    
    def calculate_dates_for_year(self, request, queryset):
        """Рассчитать даты событий для текущего года"""
        from datetime import date
        current_year = date.today().year
        
        results = []
        for event in queryset.order_by('month', 'day'):
            event_date = event.get_date_for_year(current_year)
            results.append(f"{event.title}: {event_date.strftime('%d.%m.%Y')}")
        
        message = f"Даты на {current_year} год:\n" + "\n".join(results)
        self.message_user(request, message)
    
    calculate_dates_for_year.short_description = 'Рассчитать даты на текущий год'
    
    def export_calendar(self, request, queryset):
        """Экспорт календаря в JSON"""
        import json
        from datetime import date
        from django.http import HttpResponse
        
        current_year = date.today().year
        calendar_data = []
        
        for event in queryset:
            event_date = event.get_date_for_year(current_year)
            calendar_data.append({
                'title': event.title,
                'description': event.description,
                'date': event_date.strftime('%Y-%m-%d'),
                'type': event.event_type,
                'is_movable': event.is_movable
            })
        
        response = HttpResponse(
            json.dumps(calendar_data, ensure_ascii=False, indent=2),
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="orthodox_calendar_{current_year}.json"'
        return response
    
    export_calendar.short_description = 'Экспорт в JSON'

# =============================================================================
# 🍽️ АДМИНКА ДЛЯ ЕЖЕДНЕВНОЙ ПРАВОСЛАВНОЙ ИНФОРМАЦИИ
# =============================================================================

@admin.register(FastingPeriod)
class FastingPeriodAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'get_period_display', 'priority', 'is_active']
    list_filter = ['name', 'is_active', 'priority']
    search_fields = ['title', 'description']
    ordering = ['-priority', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'title', 'description', 'priority', 'is_active')
        }),
        ('Фиксированные даты', {
            'fields': ('start_month', 'start_day', 'end_month', 'end_day'),
            'description': 'Для постов с фиксированными датами'
        }),
        ('Переходящие даты (относительно Пасхи)', {
            'fields': ('easter_start_offset', 'easter_end_offset'),
            'description': 'Отрицательные значения - до Пасхи, положительные - после'
        }),
        ('Правила поста', {
            'fields': ('fasting_rules',),
            'description': 'Правила по дням недели в JSON формате'
        }),
    )
    
    def get_period_display(self, obj):
        if obj.easter_start_offset is not None:
            return f'Переходящий ({obj.easter_start_offset} до {obj.easter_end_offset} дней от Пасхи)'
        else:
            return f'Фиксированный ({obj.start_day}.{obj.start_month} - {obj.end_day}.{obj.end_month})'
    get_period_display.short_description = 'Период'

@admin.register(DailyOrthodoxInfo)
class DailyOrthodoxInfoAdmin(admin.ModelAdmin):
    list_display = ['date_display', 'fasting_type_colored', 'allowed_food_short', 'spiritual_note_short']
    list_filter = ['fasting_type', 'month']
    search_fields = ['fasting_description', 'allowed_food', 'spiritual_note']
    ordering = ['month', 'day']
    list_per_page = 50
    
    # Красивое отображение даты
    def date_display(self, obj):
        return f"{obj.day:02d}.{obj.month:02d}"
    date_display.short_description = 'Дата'
    
    # Цветное отображение типов поста
    def fasting_type_colored(self, obj):
        colors = {
            'no_fast': '#28a745',        # зеленый
            'light_fast': '#ffc107',     # желтый
            'strict_fast': '#dc3545',    # красный
            'dry_eating': '#6f42c1',     # фиолетовый
            'with_oil': '#fd7e14',       # оранжевый
            'with_fish': '#20c997',      # голубовато-зеленый
            'wine_oil': '#e83e8c',       # розовый
            'complete_fast': '#495057',  # темно-серый
        }
        color = colors.get(obj.fasting_type, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_fasting_type_display()
        )
    fasting_type_colored.short_description = 'Тип поста'
    
    # Короткое отображение разрешенной пищи
    def allowed_food_short(self, obj):
        if obj.allowed_food:
            return obj.allowed_food[:50] + ('...' if len(obj.allowed_food) > 50 else '')
        return '-'
    allowed_food_short.short_description = 'Разрешенная пища'
    
    # Короткое отображение наставления
    def spiritual_note_short(self, obj):
        if obj.spiritual_note:
            return obj.spiritual_note[:50] + ('...' if len(obj.spiritual_note) > 50 else '')
        return '-'
    spiritual_note_short.short_description = 'Наставление'
    
    fieldsets = (
        ('Дата', {
            'fields': ('month', 'day')
        }),
        ('Пост', {
            'fields': ('fasting_type', 'fasting_description', 'allowed_food')
        }),
        ('Духовное наставление', {
            'fields': ('spiritual_note',)
        }),
        ('Чтения', {
            'fields': ('gospel_reading', 'epistle_reading'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['test_fasting_info', 'export_fasting_calendar']
    
    def test_fasting_info(self, request, queryset):
        """Протестировать информацию о посте на сегодня"""
        from datetime import date
        
        today = date.today()
        today_info = DailyOrthodoxInfo.get_info_for_date(today)
        
        message = f"""
Информация на сегодня ({today.strftime('%d.%m.%Y')}):

🍽️ Пост: {today_info.get_fasting_type_display()}
🍅 Пища: {today_info.allowed_food}
🙏 Наставление: {today_info.spiritual_note}
        """
        
        self.message_user(request, message)
    
    test_fasting_info.short_description = 'Показать информацию на сегодня'
    
    def export_fasting_calendar(self, request, queryset):
        """Экспорт календаря постов в JSON"""
        import json
        from django.http import HttpResponse
        
        fasting_data = []
        
        for info in queryset:
            fasting_data.append({
                'date': f'{info.month:02d}-{info.day:02d}',
                'fasting_type': info.fasting_type,
                'fasting_type_display': info.get_fasting_type_display(),
                'description': info.fasting_description,
                'allowed_food': info.allowed_food,
                'spiritual_note': info.spiritual_note
            })
        
        response = HttpResponse(
            json.dumps(fasting_data, ensure_ascii=False, indent=2),
            content_type='application/json; charset=utf-8'
        )
        response['Content-Disposition'] = 'attachment; filename="fasting_calendar.json"'
        return response
    
    export_fasting_calendar.short_description = 'Экспорт календаря постов'
