# PWA Models for Православный портал

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PushSubscription(models.Model):
    """Модель для хранения push-подписок пользователей"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='push_subscriptions',
        null=True, 
        blank=True,
        help_text="Пользователь (может быть null для анонимных подписок)"
    )
    
    endpoint = models.URLField(
        max_length=500,
        help_text="URL endpoint для push-уведомлений"
    )
    
    p256dh_key = models.TextField(
        help_text="Ключ p256dh для шифрования"
    )
    
    auth_key = models.TextField(
        help_text="Ключ auth для аутентификации"
    )
    
    user_agent = models.TextField(
        blank=True,
        help_text="User-Agent браузера"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Активна ли подписка"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Дата создания подписки"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Дата последнего обновления"
    )
    
    class Meta:
        verbose_name = "Push-подписка"
        verbose_name_plural = "Push-подписки"
        unique_together = ['user', 'endpoint']
        
    def __str__(self):
        user_info = f"User {self.user.id}" if self.user else "Anonymous"
        return f"Push subscription for {user_info}"

class PWAInstallEvent(models.Model):
    """Модель для отслеживания установок PWA"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pwa_installs',
        null=True,
        blank=True
    )
    
    user_agent = models.TextField(
        help_text="User-Agent при установке"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP адрес пользователя"
    )
    
    installed_at = models.DateTimeField(
        default=timezone.now,
        help_text="Дата и время установки"
    )
    
    platform = models.CharField(
        max_length=50,
        blank=True,
        help_text="Платформа (Android, iOS, Desktop)"
    )
    
    browser = models.CharField(
        max_length=50,
        blank=True,
        help_text="Браузер пользователя"
    )
    
    class Meta:
        verbose_name = "Установка PWA"
        verbose_name_plural = "Установки PWA"
        
    def __str__(self):
        user_info = f"User {self.user.id}" if self.user else "Anonymous"
        return f"PWA install by {user_info} at {self.installed_at}"

class OfflineAction(models.Model):
    """Модель для хранения действий в офлайн режиме"""
    
    ACTION_TYPES = [
        ('playlist_create', 'Создание плейлиста'),
        ('playlist_add', 'Добавление в плейлист'),
        ('favorite_add', 'Добавление в избранное'),
        ('favorite_remove', 'Удаление из избранного'),
        ('cart_add', 'Добавление в корзину'),
        ('cart_remove', 'Удаление из корзины'),
        ('book_download', 'Скачивание книги'),
        ('story_view', 'Просмотр рассказа'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offline_actions',
        null=True,
        blank=True
    )
    
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text="Ключ сессии для анонимных пользователей"
    )
    
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        help_text="Тип действия"
    )
    
    content_type = models.CharField(
        max_length=20,
        help_text="Тип контента (story, book, fairy_tale)"
    )
    
    object_id = models.PositiveIntegerField(
        help_text="ID объекта"
    )
    
    action_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Дополнительные данные действия"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Дата создания действия"
    )
    
    is_synced = models.BooleanField(
        default=False,
        help_text="Синхронизировано ли действие"
    )
    
    synced_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Дата синхронизации"
    )
    
    class Meta:
        verbose_name = "Офлайн действие"
        verbose_name_plural = "Офлайн действия"
        ordering = ['-created_at']
        
    def __str__(self):
        user_info = f"User {self.user.id}" if self.user else f"Session {self.session_key}"
        return f"{self.get_action_type_display()} by {user_info}"
    
    def mark_synced(self):
        """Помечает действие как синхронизированное"""
        self.is_synced = True
        self.synced_at = timezone.now()
        self.save()

class PWAAnalytics(models.Model):
    """Модель для аналитики PWA"""
    
    EVENT_TYPES = [
        ('install_prompt_shown', 'Показ промпта установки'),
        ('install_prompt_accepted', 'Принятие установки'),
        ('install_prompt_dismissed', 'Отклонение установки'),
        ('offline_usage', 'Использование в офлайн'),
        ('push_permission_granted', 'Разрешение push-уведомлений'),
        ('push_permission_denied', 'Отказ от push-уведомлений'),
        ('background_sync', 'Фоновая синхронизация'),
        ('cache_hit', 'Попадание в кеш'),
        ('cache_miss', 'Промах кеша'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pwa_analytics',
        null=True,
        blank=True
    )
    
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )
    
    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES
    )
    
    event_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Дополнительные данные события"
    )
    
    user_agent = models.TextField(
        blank=True
    )
    
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        verbose_name = "PWA аналитика"
        verbose_name_plural = "PWA аналитика"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_event_type_display()} at {self.created_at}"

class CachedContent(models.Model):
    """Модель для отслеживания кешированного контента"""
    
    CONTENT_TYPES = [
        ('story', 'Рассказ'),
        ('book', 'Книга'),
        ('fairy_tale', 'Сказка'),
        ('playlist', 'Плейлист'),
        ('page', 'Страница'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cached_content',
        null=True,
        blank=True
    )
    
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES
    )
    
    object_id = models.PositiveIntegerField()
    
    cache_key = models.CharField(
        max_length=255,
        help_text="Ключ кеша"
    )
    
    cache_size = models.PositiveIntegerField(
        help_text="Размер кешированных данных в байтах"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    last_accessed = models.DateTimeField(
        default=timezone.now
    )
    
    access_count = models.PositiveIntegerField(
        default=1,
        help_text="Количество обращений к кешу"
    )
    
    class Meta:
        verbose_name = "Кешированный контент"
        verbose_name_plural = "Кешированный контент"
        unique_together = ['user', 'content_type', 'object_id']
        
    def __str__(self):
        user_info = f"User {self.user.id}" if self.user else "Anonymous"
        return f"{self.get_content_type_display()} {self.object_id} cached for {user_info}"
    
    def update_access(self):
        """Обновляет статистику доступа"""
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save()
