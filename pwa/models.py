# PWA Models for Православный портал

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class PushSubscription(models.Model):
    """Подписки на push-уведомления"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField(verbose_name="Endpoint")
    p256dh_key = models.TextField(verbose_name="P256DH ключ")
    auth_key = models.TextField(verbose_name="Auth ключ")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'endpoint']
        verbose_name = "Push-подписка"
        verbose_name_plural = "Push-подписки"
        
    def __str__(self):
        return f"{self.user.username} - {self.endpoint[:50]}..."

class PWAInstallEvent(models.Model):
    """События установки PWA"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    platform = models.CharField(max_length=50, verbose_name="Платформа")
    browser = models.CharField(max_length=50, verbose_name="Браузер")
    user_agent = models.TextField(verbose_name="User Agent")
    installed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Событие установки PWA"
        verbose_name_plural = "События установки PWA"
        
    def __str__(self):
        return f"{self.user or 'Anonymous'} - {self.platform} - {self.installed_at}"

class OfflineAction(models.Model):
    """Действия выполненные офлайн"""
    ACTION_CHOICES = [
        ('create_playlist', 'Создание плейлиста'),
        ('add_to_playlist', 'Добавление в плейлист'),
        ('toggle_favorite', 'Изменение избранного'),
        ('add_to_cart', 'Добавление в корзину'),
        ('remove_from_cart', 'Удаление из корзины'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    action_data = models.JSONField(default=dict)
    is_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(null=True, blank=True)
    
    def mark_synced(self):
        self.is_synced = True
        self.synced_at = timezone.now()
        self.save()
    
    class Meta:
        verbose_name = "Офлайн действие"
        verbose_name_plural = "Офлайн действия"
        
    def __str__(self):
        return f"{self.user.username} - {self.get_action_type_display()}"

class PWAAnalytics(models.Model):
    """Аналитика PWA"""
    EVENT_CHOICES = [
        ('install', 'Установка'),
        ('uninstall', 'Удаление'),
        ('offline_usage', 'Использование офлайн'),
        ('sync_performed', 'Синхронизация'),
        ('notification_sent', 'Уведомление отправлено'),
        ('notification_clicked', 'Уведомление кликнуто'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    event_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "PWA аналитика"
        verbose_name_plural = "PWA аналитика"
        
    def __str__(self):
        return f"{self.user or 'Anonymous'} - {self.get_event_type_display()}"

class CachedContent(models.Model):
    """Кешированный контент для офлайн доступа"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    cache_key = models.CharField(max_length=255)
    cache_size = models.PositiveIntegerField(default=0)  # в байтах
    access_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'cache_key']
        verbose_name = "Кешированный контент"
        verbose_name_plural = "Кешированный контент"
        
    def __str__(self):
        return f"{self.user.username} - {self.cache_key}"
