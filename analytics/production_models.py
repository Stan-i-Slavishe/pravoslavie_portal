# analytics/production_models.py - НОВЫЕ МОДЕЛИ ДЛЯ ПРОДАКШЕНА

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AnalyticsEvent(models.Model):
    """Универсальная модель для отслеживания событий"""
    
    EVENT_TYPES = [
        ('page_view', 'Просмотр страницы'),
        ('purchase', 'Покупка'),
        ('purchase_complete', 'Завершенная покупка'),
        ('add_to_cart', 'Добавление в корзину'),
        ('download', 'Скачивание'),
        ('interaction', 'Взаимодействие'),
        ('search', 'Поиск'),
        ('session_end', 'Конец сессии'),
        ('time_on_page', 'Время на странице'),
        ('form_submission', 'Отправка формы'),
        ('error', 'Ошибка'),
    ]
    
    # Основные поля
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    session_id = models.CharField(max_length=50, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Данные события
    data = models.JSONField(default=dict)
    
    # Метаданные
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    page_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'analytics_event'
        verbose_name = 'Событие аналитики'
        verbose_name_plural = 'События аналитики'
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class ConversionFunnel(models.Model):
    """Воронка конверсии"""
    
    FUNNEL_STEPS = [
        ('visit', 'Посещение'),
        ('view_product', 'Просмотр товара'),
        ('add_to_cart', 'Добавление в корзину'),
        ('checkout_start', 'Начало оформления'),
        ('purchase', 'Покупка'),
    ]
    
    date = models.DateField(auto_now_add=True, db_index=True)
    step = models.CharField(max_length=20, choices=FUNNEL_STEPS)
    count = models.PositiveIntegerField(default=0)
    
    # Детализация
    product_type = models.CharField(max_length=20, blank=True)
    traffic_source = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ['date', 'step', 'product_type']
        verbose_name = 'Воронка конверсии'
        verbose_name_plural = 'Воронка конверсии'

class RevenueMetrics(models.Model):
    """Метрики доходов"""
    
    date = models.DateField(db_index=True)
    
    # Финансовые метрики
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    orders_count = models.PositiveIntegerField(default=0)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # По типам продуктов
    books_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fairy_tales_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subscriptions_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Метрики пользователей
    new_customers = models.PositiveIntegerField(default=0)
    returning_customers = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['date']
        verbose_name = 'Метрики доходов'
        verbose_name_plural = 'Метрики доходов'
        ordering = ['-date']

class UserSession(models.Model):
    """Детальная информация о сессиях пользователей"""
    
    session_id = models.CharField(max_length=50, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Время сессии
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Активность
    pages_viewed = models.PositiveIntegerField(default=0)
    events_count = models.PositiveIntegerField(default=0)
    
    # Конверсия
    made_purchase = models.BooleanField(default=False)
    added_to_cart = models.BooleanField(default=False)
    downloaded_content = models.BooleanField(default=False)
    
    # Технические данные
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    
    class Meta:
        db_table = 'analytics_user_session'
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['made_purchase']),
        ]

class PopularContentAnalytics(models.Model):
    """Аналитика популярности контента"""
    
    CONTENT_TYPES = [
        ('book', 'Книга'),
        ('fairy_tale', 'Сказка'),
        ('story', 'Рассказ'),
        ('audio', 'Аудио'),
        ('product', 'Товар'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    
    # Статистика за период
    date = models.DateField(db_index=True)
    views_count = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    
    # Взаимодействия
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    
    # Конверсия
    add_to_cart_count = models.PositiveIntegerField(default=0)
    purchases_count = models.PositiveIntegerField(default=0)
    conversion_rate = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['content_type', 'object_id', 'date']
        verbose_name = 'Аналитика контента'
        verbose_name_plural = 'Аналитика контента'
        indexes = [
            models.Index(fields=['date', 'views_count']),
            models.Index(fields=['content_type', 'conversion_rate']),
        ]

class SearchAnalytics(models.Model):
    """Аналитика поиска"""
    
    date = models.DateField(db_index=True)
    query = models.CharField(max_length=255, db_index=True)
    
    # Статистика
    search_count = models.PositiveIntegerField(default=1)
    results_count = models.PositiveIntegerField(default=0)
    click_through_rate = models.FloatField(default=0.0)
    
    # Пользователи
    unique_users = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['date', 'query']
        verbose_name = 'Аналитика поиска'
        verbose_name_plural = 'Аналитика поиска'
        ordering = ['-search_count']

class ErrorLog(models.Model):
    """Лог ошибок от пользователей"""
    
    ERROR_TYPES = [
        ('javascript', 'JavaScript ошибка'),
        ('404', 'Страница не найдена'),
        ('500', 'Серверная ошибка'),
        ('payment', 'Ошибка оплаты'),
        ('form', 'Ошибка формы'),
    ]
    
    error_type = models.CharField(max_length=20, choices=ERROR_TYPES)
    error_message = models.TextField()
    error_page = models.URLField()
    
    # Метаданные
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Статус
    resolved = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'analytics_error_log'
        verbose_name = 'Лог ошибок'
        verbose_name_plural = 'Логи ошибок'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['error_type', 'timestamp']),
            models.Index(fields=['resolved']),
        ]
