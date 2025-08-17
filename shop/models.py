from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

class Product(models.Model):
    """Базовая модель товара"""
    
    PRODUCT_TYPES = [
        ('book', 'Книга'),
        ('audio', 'Аудио'),
        ('subscription', 'Подписка'),
        ('fairy_tale', 'Персонализированная сказка'),
    ]
    
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    product_type = models.CharField('Тип товара', max_length=20, choices=PRODUCT_TYPES)
    
    # Связи с контентом
    book_id = models.PositiveIntegerField('ID книги', null=True, blank=True)
    audio_id = models.PositiveIntegerField('ID аудио', null=True, blank=True)
    subscription_id = models.PositiveIntegerField('ID подписки', null=True, blank=True)
    fairy_tale_template_id = models.PositiveIntegerField('ID шаблона сказки', null=True, blank=True)
    
    # Настройки товара
    is_active = models.BooleanField('Активный', default=True)
    is_digital = models.BooleanField('Цифровой товар', default=True)
    requires_personalization = models.BooleanField('Требует персонализации', default=False)
    
    # Настройки для терапевтических сказок
    has_audio_option = models.BooleanField('Доступна озвучка', default=False)
    audio_option_price = models.DecimalField('Цена озвучки', max_digits=6, decimal_places=2, default=0.00)
    has_illustration_option = models.BooleanField('Доступны иллюстрации', default=False)
    illustration_option_price = models.DecimalField('Цена иллюстраций', max_digits=6, decimal_places=2, default=0.00)
    personalization_form_config = models.JSONField('Конфигурация формы персонализации', default=dict, blank=True)
    
    # Изображения и файлы
    image = models.ImageField('Изображение', upload_to='shop/products/', blank=True, null=True)
    
    # Метаданные
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_product_type_display()}) - {self.price}₽"
    
    @property
    def content_object(self):
        """Получить связанный объект контента"""
        if self.product_type == 'book' and self.book_id:
            from books.models import Book
            try:
                return Book.objects.get(id=self.book_id)
            except Book.DoesNotExist:
                return None
        elif self.product_type == 'audio' and self.audio_id:
            from audio.models import AudioTrack
            try:
                return AudioTrack.objects.get(id=self.audio_id)
            except AudioTrack.DoesNotExist:
                return None
        elif self.product_type == 'subscription' and self.subscription_id:
            from subscriptions.models import Subscription
            try:
                return Subscription.objects.get(id=self.subscription_id)
            except Subscription.DoesNotExist:
                return None
        elif self.product_type == 'fairy_tale' and self.fairy_tale_template_id:
            from fairy_tales.models import FairyTaleTemplate
            try:
                return FairyTaleTemplate.objects.get(id=self.fairy_tale_template_id)
            except FairyTaleTemplate.DoesNotExist:
                return None
        return None
    
    @property
    def full_price_with_options(self):
        """Полная цена со всеми опциями"""
        total = self.price
        if self.product_type == 'fairy_tale':
            if self.has_audio_option:
                total += self.audio_option_price
            if self.has_illustration_option:
                total += self.illustration_option_price
        return total

class Cart(models.Model):
    """Корзина покупок"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина {self.user.username}"
    
    @property
    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        """Общее количество товаров"""
        return sum(item.quantity for item in self.items.all())
    
    def clear(self):
        """Очистить корзину"""
        self.items.all().delete()

class CartItem(models.Model):
    """Элемент корзины"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1), MaxValueValidator(99)])
    added_at = models.DateTimeField('Добавлено', auto_now_add=True)
    
    # Поля для персонализации сказок
    personalization_data = models.JSONField('Данные персонализации', default=dict, blank=True)
    include_audio = models.BooleanField('Включить озвучку', default=False)
    include_illustrations = models.BooleanField('Включить иллюстрации', default=False)
    special_requests = models.TextField('Особые пожелания', blank=True)
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.title} x{self.quantity}"
    
    @property
    def total_price(self):
        """Стоимость этого элемента с учетом опций"""
        base_price = self.product.price * self.quantity
        
        # Дополнительные опции для сказок
        if self.product.product_type == 'fairy_tale':
            if self.include_audio and self.product.has_audio_option:
                base_price += self.product.audio_option_price * self.quantity
            if self.include_illustrations and self.product.has_illustration_option:
                base_price += self.product.illustration_option_price * self.quantity
                
        return base_price
    
    def get_personalization_summary(self):
        """Краткое описание персонализации"""
        if not self.personalization_data:
            return "Не указано"
        
        summary_parts = []
        data = self.personalization_data
        
        if 'child_name' in data and data['child_name']:
            summary_parts.append(f"Имя: {data['child_name']}")
        if 'child_age' in data and data['child_age']:
            summary_parts.append(f"Возраст: {data['child_age']}")
        if 'main_problem' in data and data['main_problem']:
            summary_parts.append(f"Проблема: {data['main_problem']}")
            
        return "; ".join(summary_parts) if summary_parts else "Не указано"

class Order(models.Model):
    """Заказ"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('processing', 'Обрабатывается'),
        ('paid', 'Оплачен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
        ('refunded', 'Возврат'),
    ]
    
    # Основная информация
    order_id = models.UUIDField('ID заказа', default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='orders')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Финансовая информация
    total_amount = models.DecimalField('Общая сумма', max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField('Размер скидки', max_digits=10, decimal_places=2, default=0.00)
    discount_code = models.CharField('Промокод', max_length=50, blank=True, default='')
    
    # Контактная информация
    email = models.EmailField('Email')
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    
    # Информация об оплате
    payment_method = models.CharField('Способ оплаты', max_length=50, blank=True)
    payment_id = models.CharField('ID платежа', max_length=100, blank=True)
    payment_data = models.JSONField('Данные платежа', default=dict, blank=True)
    
    # Временные метки
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    paid_at = models.DateTimeField('Оплачено', null=True, blank=True)
    completed_at = models.DateTimeField('Завершено', null=True, blank=True)
    
    # Заметки
    notes = models.TextField('Заметки', blank=True)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.order_id.hex[:8]} - {self.user.username} ({self.get_status_display()})"
    
    @property
    def short_id(self):
        """Короткий ID для отображения"""
        return self.order_id.hex[:8].upper()
    
    @property
    def full_name(self):
        """Полное имя покупателя"""
        return f"{self.first_name} {self.last_name}"

class OrderItem(models.Model):
    """Элемент заказа"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    
    # Зафиксированная информация на момент заказа
    product_title = models.CharField('Название товара', max_length=200)
    product_price = models.DecimalField('Цена товара', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    # Доступ к цифровому контенту
    is_downloaded = models.BooleanField('Скачано', default=False)
    download_count = models.PositiveIntegerField('Количество скачиваний', default=0)
    first_download_at = models.DateTimeField('Первое скачивание', null=True, blank=True)
    last_download_at = models.DateTimeField('Последнее скачивание', null=True, blank=True)
    
    # Поля для персонализированных сказок
    personalization_data = models.JSONField('Данные персонализации', default=dict, blank=True)
    include_audio = models.BooleanField('Включить озвучку', default=False)
    include_illustrations = models.BooleanField('Включить иллюстрации', default=False)
    special_requests = models.TextField('Особые пожелания', blank=True)
    
    # Статус выполнения для сказок
    FAIRY_TALE_STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('ready', 'Готова'),
        ('delivered', 'Доставлена'),
    ]
    
    fairy_tale_status = models.CharField('Статус сказки', max_length=20, choices=FAIRY_TALE_STATUS_CHOICES, blank=True)
    
    # Результаты работы
    generated_content = models.TextField('Готовая сказка', blank=True)
    audio_file = models.FileField('Аудио-файл', upload_to='fairy_tales/audio/%Y/%m/', blank=True, null=True)
    illustration_file = models.FileField('Иллюстрации', upload_to='fairy_tales/illustrations/%Y/%m/', blank=True, null=True)
    
    # Административное
    estimated_completion = models.DateTimeField('Планируемое завершение', null=True, blank=True)
    admin_notes = models.TextField('Заметки администратора', blank=True)
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.product_title} x{self.quantity} (Заказ #{self.order.short_id})"
    
    @property
    def total_price(self):
        """Общая стоимость этого элемента с учетом опций"""
        base_price = self.product_price * self.quantity
        
        # Дополнительные опции для сказок
        if self.product.product_type == 'fairy_tale':
            if self.include_audio and self.product.has_audio_option:
                base_price += self.product.audio_option_price * self.quantity
            if self.include_illustrations and self.product.has_illustration_option:
                base_price += self.product.illustration_option_price * self.quantity
                
        return base_price
    
    def get_personalization_summary(self):
        """Краткое описание персонализации"""
        if not self.personalization_data:
            return "Не указано"
        
        summary_parts = []
        data = self.personalization_data
        
        if 'child_name' in data and data['child_name']:
            summary_parts.append(f"Имя: {data['child_name']}")
        if 'child_age' in data and data['child_age']:
            summary_parts.append(f"Возраст: {data['child_age']}")
        if 'main_problem' in data and data['main_problem']:
            summary_parts.append(f"Проблема: {data['main_problem']}")
            
        return "; ".join(summary_parts) if summary_parts else "Не указано"
    
    @property
    def is_fairy_tale(self):
        """Проверить, является ли товар сказкой"""
        return self.product.product_type == 'fairy_tale'
    
    @property
    def fairy_tale_status_display(self):
        """Отображение статуса сказки"""
        if self.is_fairy_tale and self.fairy_tale_status:
            return dict(self.FAIRY_TALE_STATUS_CHOICES).get(self.fairy_tale_status, 'Неизвестно')
        return None
    
    def mark_downloaded(self):
        """Отметить как скачанное"""
        from django.utils import timezone
        
        self.download_count += 1
        self.last_download_at = timezone.now()
        
        if not self.is_downloaded:
            self.is_downloaded = True
            self.first_download_at = timezone.now()
        
        self.save()

class Purchase(models.Model):
    """Покупка пользователя (для быстрого доступа)"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    
    purchased_at = models.DateTimeField('Дата покупки', auto_now_add=True)
    download_count = models.PositiveIntegerField('Количество скачиваний', default=0)
    last_downloaded = models.DateTimeField('Последнее скачивание', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = ['user', 'product']
        ordering = ['-purchased_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class Discount(models.Model):
    """Скидки и промокоды"""
    
    DISCOUNT_TYPES = [
        ('percentage', 'Процент'),
        ('fixed', 'Фиксированная сумма'),
    ]
    
    code = models.CharField('Промокод', max_length=50, unique=True)
    description = models.CharField('Описание', max_length=200)
    
    discount_type = models.CharField('Тип скидки', max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField('Размер скидки', max_digits=10, decimal_places=2)
    
    # Ограничения
    min_amount = models.DecimalField('Минимальная сумма заказа', max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField('Максимальное количество использований', null=True, blank=True)
    uses_count = models.PositiveIntegerField('Количество использований', default=0)
    
    # Сроки действия
    valid_from = models.DateTimeField('Действует с')
    valid_until = models.DateTimeField('Действует до')
    
    # Настройки
    is_active = models.BooleanField('Активный', default=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == 'percentage' else '₽'})"
    
    def is_valid(self):
        """Проверить валидность промокода"""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False, "Промокод неактивен"
        
        if now < self.valid_from:
            return False, "Промокод еще не действует"
        
        if now > self.valid_until:
            return False, "Срок действия промокода истек"
        
        if self.max_uses and self.uses_count >= self.max_uses:
            return False, "Промокод больше не действует"
        
        return True, "Промокод действителен"
    
    def calculate_discount(self, amount):
        """Рассчитать размер скидки"""
        if amount < self.min_amount:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
        else:
            discount = self.discount_value
        
        # Скидка не может быть больше суммы заказа
        return min(discount, amount)
