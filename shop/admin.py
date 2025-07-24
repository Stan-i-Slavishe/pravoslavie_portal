from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Cart, CartItem, Order, OrderItem, Purchase, Discount

# Улучшенная форма для Product с выбором контента из списков
class ProductAdminForm(forms.ModelForm):
    """Улучшенная форма с выбором контента из выпадающих списков"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Динамически загружаем доступный контент для выбора
        try:
            from books.models import Book
            book_choices = [('', '-- Выберите книгу --')] + [
                (book.id, f"{book.title} (ID: {book.id})") 
                for book in Book.objects.all()
            ]
            self.fields['book_id'] = forms.ChoiceField(
                choices=book_choices,
                required=False,
                label='Книга',
                help_text='Выберите книгу из списка',
                widget=forms.Select(attrs={'onchange': 'updateContentPreview()'})
            )
        except Exception as e:
            # Если модель Book не найдена, оставляем обычное поле
            print(f"Ошибка загрузки книг: {e}")
            
        try:
            from audio.models import AudioTrack
            audio_choices = [('', '-- Выберите аудио --')] + [
                (audio.id, f"{audio.title} (ID: {audio.id})") 
                for audio in AudioTrack.objects.all()
            ]
            self.fields['audio_id'] = forms.ChoiceField(
                choices=audio_choices,
                required=False,
                label='Аудио трек',
                help_text='Выберите аудио из списка',
                widget=forms.Select(attrs={'onchange': 'updateContentPreview()'})
            )
        except Exception as e:
            print(f"Ошибка загрузки аудио: {e}")
            
        try:
            from subscriptions.models import Subscription
            subscription_choices = [('', '-- Выберите подписку --')] + [
                (sub.id, f"{sub.name} (ID: {sub.id})") 
                for sub in Subscription.objects.all()
            ]
            self.fields['subscription_id'] = forms.ChoiceField(
                choices=subscription_choices,
                required=False,
                label='Тип подписки',
                help_text='Выберите подписку из списка',
                widget=forms.Select(attrs={'onchange': 'updateContentPreview()'})
            )
        except Exception as e:
            print(f"Ошибка загрузки подписок: {e}")
            
        try:
            from fairy_tales.models import FairyTale
            fairy_tale_choices = [('', '-- Выберите шаблон сказки --')] + [
                (ft.id, f"{ft.title} ({ft.age_group}) (ID: {ft.id})") 
                for ft in FairyTale.objects.all()
            ]
            self.fields['fairy_tale_template_id'] = forms.ChoiceField(
                choices=fairy_tale_choices,
                required=False,
                label='Шаблон сказки',
                help_text='Выберите шаблон сказки из списка',
                widget=forms.Select(attrs={'onchange': 'updateContentPreview()'})
            )
        except Exception as e:
            print(f"Ошибка загрузки сказок: {e}")
    
    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        product_type = cleaned_data.get('product_type')
        
        # Проверяем, что для выбранного типа товара указан соответствующий ID
        if product_type == 'book':
            if not cleaned_data.get('book_id'):
                raise ValidationError('Для типа "Книга" необходимо выбрать книгу')
            # Очищаем остальные поля
            cleaned_data['audio_id'] = None
            cleaned_data['subscription_id'] = None
            cleaned_data['fairy_tale_template_id'] = None
            
        elif product_type == 'audio':
            if not cleaned_data.get('audio_id'):
                raise ValidationError('Для типа "Аудио" необходимо выбрать аудио трек')
            # Очищаем остальные поля
            cleaned_data['book_id'] = None
            cleaned_data['subscription_id'] = None
            cleaned_data['fairy_tale_template_id'] = None
            
        elif product_type == 'subscription':
            if not cleaned_data.get('subscription_id'):
                raise ValidationError('Для типа "Подписка" необходимо выбрать тип подписки')
            # Очищаем остальные поля
            cleaned_data['book_id'] = None
            cleaned_data['audio_id'] = None
            cleaned_data['fairy_tale_template_id'] = None
            
        elif product_type == 'fairy_tale':
            if not cleaned_data.get('fairy_tale_template_id'):
                raise ValidationError('Для типа "Сказка" необходимо выбрать шаблон сказки')
            # Очищаем остальные поля
            cleaned_data['book_id'] = None
            cleaned_data['audio_id'] = None
            cleaned_data['subscription_id'] = None
        
        return cleaned_data
    
    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    
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
    readonly_fields = ['created_at', 'updated_at', 'content_preview']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'price', 'product_type')
        }),
        ('Связь с контентом', {
            'fields': ('book_id', 'audio_id', 'subscription_id', 'fairy_tale_template_id', 'content_preview'),
            'description': 'Выберите соответствующий контент в зависимости от типа товара'
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
            try:
                if obj.product_type == 'book':
                    url = reverse('admin:books_book_change', args=[content.id])
                    return format_html('<a href="{}" target="_blank">📚 {}</a>', url, content.title)
                elif obj.product_type == 'fairy_tale':
                    url = reverse('admin:fairy_tales_fairytale_change', args=[content.id])
                    return format_html('<a href="{}" target="_blank">🧚‍♀️ {}</a>', url, content.title)
                elif obj.product_type == 'audio':
                    url = reverse('admin:audio_audiotrack_change', args=[content.id])
                    return format_html('<a href="{}" target="_blank">🎧 {}</a>', url, content.title)
                elif obj.product_type == 'subscription':
                    url = reverse('admin:subscriptions_subscription_change', args=[content.id])
                    return format_html('<a href="{}" target="_blank">📅 {}</a>', url, content.name)
            except:
                pass
        return format_html('<span style="color: red;">❌ Не связано</span>')
    content_link.short_description = 'Связанный контент'
    
    def content_preview(self, obj):
        """Предпросмотр связанного контента"""
        if not obj.pk:
            return format_html(
                '<div style="padding: 10px; background: #f0f8ff; border-radius: 5px;">'
                '💡 Сохраните товар, чтобы увидеть предпросмотр'
                '</div>'
            )
            
        content = obj.content_object
        if content:
            try:
                if obj.product_type == 'book':
                    description = getattr(content, 'description', 'Описание отсутствует')
                    if len(description) > 100:
                        description = description[:100] + '...'
                    
                    file_info = 'Не загружен'
                    if hasattr(content, 'pdf_file') and content.pdf_file:
                        file_info = content.pdf_file.name
                    
                    return format_html(
                        '<div style="padding: 10px; background: #f8f9fa; border-radius: 5px; border: 1px solid #ddd;">'
                        '<strong>📚 Книга:</strong> {}<br>'
                        '<strong>Описание:</strong> {}<br>'
                        '<strong>Файл:</strong> {}'
                        '</div>',
                        content.title,
                        description,
                        file_info
                    )
                elif obj.product_type == 'fairy_tale':
                    age_group = getattr(content, 'age_group', 'Не указан')
                    therapeutic_goal = getattr(content, 'therapeutic_goal', 'Не указана')
                    if len(therapeutic_goal) > 100:
                        therapeutic_goal = therapeutic_goal[:100] + '...'
                    
                    category_name = 'Не указана'
                    if hasattr(content, 'category') and content.category:
                        category_name = content.category.name
                    
                    return format_html(
                        '<div style="padding: 10px; background: #f0f8ff; border-radius: 5px; border: 1px solid #ddd;">'
                        '<strong>🧚‍♀️ Сказка:</strong> {}<br>'
                        '<strong>Возраст:</strong> {}<br>'
                        '<strong>Категория:</strong> {}<br>'
                        '<strong>Цель:</strong> {}'
                        '</div>',
                        content.title,
                        age_group,
                        category_name,
                        therapeutic_goal
                    )
                elif obj.product_type == 'audio':
                    description = getattr(content, 'description', 'Описание отсутствует')
                    if len(description) > 100:
                        description = description[:100] + '...'
                    
                    file_info = 'Не загружен'
                    if hasattr(content, 'audio_file') and content.audio_file:
                        file_info = content.audio_file.name
                    
                    return format_html(
                        '<div style="padding: 10px; background: #fff8dc; border-radius: 5px; border: 1px solid #ddd;">'
                        '<strong>🎧 Аудио:</strong> {}<br>'
                        '<strong>Описание:</strong> {}<br>'
                        '<strong>Файл:</strong> {}'
                        '</div>',
                        content.title,
                        description,
                        file_info
                    )
                elif obj.product_type == 'subscription':
                    price = getattr(content, 'price', 'Не указана')
                    duration = getattr(content, 'duration', 'Не указана')
                    
                    return format_html(
                        '<div style="padding: 10px; background: #f0fff0; border-radius: 5px; border: 1px solid #ddd;">'
                        '<strong>📅 Подписка:</strong> {}<br>'
                        '<strong>Цена:</strong> {}₽<br>'
                        '<strong>Продолжительность:</strong> {} дней'
                        '</div>',
                        content.name,
                        price,
                        duration
                    )
            except Exception as e:
                return format_html(
                    '<div style="padding: 10px; background: #ffe4e1; border-radius: 5px; color: #8b0000;">'
                    '❌ Ошибка загрузки контента: {}'
                    '</div>',
                    str(e)
                )
        else:
            return format_html(
                '<div style="padding: 10px; background: #ffe4e1; border-radius: 5px; color: #8b0000;">'
                '❌ Контент не найден. Возможно, указан неверный ID или контент был удален.'
                '</div>'
            )
    content_preview.short_description = 'Предпросмотр контента'
    
    class Media:
        js = ('admin/js/product_admin.js',)

# Остальные админки остаются те же...
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
