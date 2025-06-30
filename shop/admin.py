from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Product, Cart, CartItem, Order, OrderItem, Purchase, Discount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'get_product_type_display', 
        'price', 
        'is_active', 
        'is_digital',
        'content_link',
        'created_at'
    ]
    list_filter = ['product_type', 'is_active', 'is_digital', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'price', 'product_type')
        }),
        ('Связи с контентом', {
            'fields': ('book_id', 'audio_id', 'subscription_id', 'fairy_tale_template_id'),
            'description': 'Укажите ID соответствующего контента'
        }),
        ('Настройки для терапевтических сказок', {
            'fields': (
                'requires_personalization', 
                'has_audio_option', 'audio_option_price',
                'has_illustration_option', 'illustration_option_price',
                'personalization_form_config'
            ),
            'classes': ('collapse',),
            'description': 'Настройки для персонализированных сказок'
        }),
        ('Настройки', {
            'fields': ('is_active', 'is_digital', 'image')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_link(self, obj):
        """Ссылка на связанный контент"""
        content = obj.content_object
        if content:
            if obj.product_type == 'book':
                url = reverse('admin:books_book_change', args=[content.id])
                return format_html('<a href="{}" target="_blank">{}</a>', url, content.title)
            elif obj.product_type == 'fairy_tale':
                url = reverse('admin:fairy_tales_fairytaletemplate_change', args=[content.id])
                return format_html('<a href="{}" target="_blank">🧚‍♀️ {}</a>', url, content.title)
            # Добавить для audio и subscription когда будет готово
        return 'Не связано'
    content_link.short_description = 'Связанный контент'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'total_price_display', 'personalization_summary']
    fields = ['product', 'quantity', 'personalization_summary', 'total_price_display', 'added_at']
    
    def total_price_display(self, obj):
        return f"{obj.total_price}₽"
    total_price_display.short_description = 'Сумма'
    
    def personalization_summary(self, obj):
        if obj.product.product_type == 'fairy_tale' and obj.personalization_data:
            summary = obj.get_personalization_summary()
            options = []
            if obj.include_audio:
                options.append('🎤 Озвучка')
            if obj.include_illustrations:
                options.append('🎨 Иллюстрации')
            result = summary
            if options:
                result += f' + {", ".join(options)}'
            return result
        return '-'
    personalization_summary.short_description = 'Персонализация'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price_display', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_price_display', 'total_items']
    inlines = [CartItemInline]
    
    def total_price_display(self, obj):
        return f"{obj.total_price}₽"
    total_price_display.short_description = 'Общая сумма'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'is_downloaded', 'download_count', 'first_download_at', 'last_download_at', 'personalization_summary', 'fairy_tale_status_display']
    fields = [
        'product', 'product_title', 'product_price', 'quantity', 'total_price',
        'personalization_summary', 'fairy_tale_status_display',
        'is_downloaded', 'download_count', 'first_download_at', 'last_download_at'
    ]
    
    def personalization_summary(self, obj):
        if obj.product.product_type == 'fairy_tale' and obj.personalization_data:
            summary = obj.get_personalization_summary()
            options = []
            if obj.include_audio:
                options.append('🎤 Озвучка')
            if obj.include_illustrations:
                options.append('🎨 Иллюстрации')
            result = summary
            if options:
                result += f' + {", ".join(options)}'
            return result
        return '-'
    personalization_summary.short_description = 'Персонализация'
    
    def fairy_tale_status_display(self, obj):
        if obj.is_fairy_tale:
            status_display = obj.fairy_tale_status_display or 'Не установлен'
            status_icons = {
                'Ожидает': '⏳',
                'В работе': '🛠️',
                'Готова': '✅',
                'Доставлена': '📦'
            }
            icon = status_icons.get(status_display, '❓')
            return f'{icon} {status_display}'
        return '-'
    fairy_tale_status_display.short_description = 'Статус сказки'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'short_id', 
        'user', 
        'full_name', 
        'status', 
        'total_amount',
        'payment_method',
        'created_at',
        'paid_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at', 'paid_at']
    search_fields = [
        'order_id', 
        'user__username', 
        'user__email', 
        'first_name', 
        'last_name', 
        'email',
        'payment_id'
    ]
    readonly_fields = [
        'order_id', 
        'short_id', 
        'created_at', 
        'updated_at',
        'payment_data_display'
    ]
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order_id', 'short_id', 'user', 'status', 'total_amount')
        }),
        ('Контактная информация', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
        ('Информация об оплате', {
            'fields': ('payment_method', 'payment_id', 'payment_data_display')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'paid_at', 'completed_at')
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_completed', 'mark_as_cancelled']
    
    def payment_data_display(self, obj):
        """Отображение данных платежа в удобном виде"""
        if obj.payment_data:
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.payment_data, indent=2, ensure_ascii=False))
        return 'Нет данных'
    payment_data_display.short_description = 'Данные платежа'
    
    def mark_as_paid(self, request, queryset):
        """Отметить заказы как оплаченные"""
        updated = queryset.update(status='paid', paid_at=timezone.now())
        self.message_user(request, f'{updated} заказов отмечены как оплаченные.')
    mark_as_paid.short_description = 'Отметить как оплаченные'
    
    def mark_as_completed(self, request, queryset):
        """Отметить заказы как завершенные"""
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} заказов отмечены как завершенные.')
    mark_as_completed.short_description = 'Отметить как завершенные'
    
    def mark_as_cancelled(self, request, queryset):
        """Отметить заказы как отмененные"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} заказов отменены.')
    mark_as_cancelled.short_description = 'Отменить заказы'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 
        'product_title', 
        'product_type_display',
        'product_price', 
        'quantity', 
        'total_price',
        'fairy_tale_status_icon',
        'is_downloaded',
        'download_count'
    ]
    list_filter = ['is_downloaded', 'order__status', 'order__created_at', 'product__product_type', 'fairy_tale_status']
    search_fields = ['product_title', 'order__order_id', 'order__user__username']
    readonly_fields = ['total_price', 'first_download_at', 'last_download_at', 'personalization_display']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order', 'product', 'product_title', 'product_price', 'quantity', 'total_price')
        }),
        ('Персонализация сказки', {
            'fields': (
                'personalization_display', 'include_audio', 'include_illustrations', 
                'special_requests', 'fairy_tale_status'
            ),
            'classes': ('collapse',)
        }),
        ('Результаты работы', {
            'fields': (
                'generated_content', 'audio_file', 'illustration_file',
                'estimated_completion', 'admin_notes'
            ),
            'classes': ('collapse',)
        }),
        ('Скачивания', {
            'fields': ('is_downloaded', 'download_count', 'first_download_at', 'last_download_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')
    
    def product_type_display(self, obj):
        type_icons = {
            'book': '📚',
            'audio': '🎧',
            'subscription': '📅',
            'fairy_tale': '🧚‍♀️'
        }
        icon = type_icons.get(obj.product.product_type, '📎')
        return f'{icon} {obj.product.get_product_type_display()}'
    product_type_display.short_description = 'Тип товара'
    
    def fairy_tale_status_icon(self, obj):
        if obj.is_fairy_tale:
            status_display = obj.fairy_tale_status_display or 'Не установлен'
            status_icons = {
                'Ожидает': '⏳',
                'В работе': '🛠️',
                'Готова': '✅',
                'Доставлена': '📦'
            }
            icon = status_icons.get(status_display, '❓')
            return f'{icon} {status_display}'
        return '-'
    fairy_tale_status_icon.short_description = 'Статус'
    
    def personalization_display(self, obj):
        if obj.product.product_type == 'fairy_tale' and obj.personalization_data:
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.personalization_data, indent=2, ensure_ascii=False))
        return 'Нет данных'
    personalization_display.short_description = 'Данные персонализации'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'order', 'purchased_at']
    list_filter = ['purchased_at', 'product__product_type']
    search_fields = ['user__username', 'product__title', 'order__order_id']
    readonly_fields = ['purchased_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product', 'order')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'code', 
        'description', 
        'discount_display',
        'uses_display', 
        'valid_period',
        'is_active'
    ]
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    readonly_fields = ['uses_count', 'created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Настройки скидки', {
            'fields': ('discount_type', 'discount_value', 'min_amount')
        }),
        ('Ограничения использования', {
            'fields': ('max_uses', 'uses_count', 'valid_from', 'valid_until')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def discount_display(self, obj):
        """Отображение размера скидки"""
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        return f"{obj.discount_value}₽"
    discount_display.short_description = 'Скидка'
    
    def uses_display(self, obj):
        """Отображение использований"""
        if obj.max_uses:
            return f"{obj.uses_count}/{obj.max_uses}"
        return f"{obj.uses_count}/∞"
    uses_display.short_description = 'Использований'
    
    def valid_period(self, obj):
        """Период действия"""
        return f"{obj.valid_from.strftime('%d.%m.%Y')} - {obj.valid_until.strftime('%d.%m.%Y')}"
    valid_period.short_description = 'Период действия'

# Дополнительные настройки
admin.site.site_header = 'Православный портал - Администрирование'
