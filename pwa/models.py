# PWA Models for Православный портал

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator

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

# =============================================================================
# 🔔 НОВЫЕ МОДЕЛИ ДЛЯ НАСТРОЕК УВЕДОМЛЕНИЙ
# =============================================================================

class NotificationCategory(models.Model):
    """Категории уведомлений"""
    
    CATEGORY_CHOICES = [
        ('bedtime_stories', '🌙 Сказки на ночь'),
        ('orthodox_calendar', '⛪ Православный календарь'),
        ('new_content', '📚 Новый контент'),
        ('fairy_tales', '🧚 Терапевтические сказки'),
        ('audio_content', '🎵 Аудио-контент'),
        ('book_releases', '📖 Новые книги'),
        ('special_events', '🎉 Особые события'),
        ('daily_wisdom', '💭 Мудрость дня'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name="Категория")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=10, default="🔔", verbose_name="Иконка")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    default_enabled = models.BooleanField(default=False, verbose_name="Включена по умолчанию")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Категория уведомлений"
        verbose_name_plural = "Категории уведомлений"
        
    def __str__(self):
        return f"{self.icon} {self.title}"

class UserNotificationSettings(models.Model):
    """Настройки уведомлений пользователя"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    
    # Общие настройки
    notifications_enabled = models.BooleanField(default=True, verbose_name="Уведомления включены")
    quiet_hours_enabled = models.BooleanField(default=True, verbose_name="Тихие часы")
    quiet_start = models.TimeField(default='22:00', verbose_name="Начало тихих часов")
    quiet_end = models.TimeField(default='08:00', verbose_name="Конец тихих часов")
    
    # Настройки по дням недели
    notify_monday = models.BooleanField(default=True)
    notify_tuesday = models.BooleanField(default=True) 
    notify_wednesday = models.BooleanField(default=True)
    notify_thursday = models.BooleanField(default=True)
    notify_friday = models.BooleanField(default=True)
    notify_saturday = models.BooleanField(default=True)
    notify_sunday = models.BooleanField(default=True)
    
    # Специальные настройки для детей
    child_mode = models.BooleanField(default=False, verbose_name="Детский режим")
    child_bedtime = models.TimeField(default='20:00', verbose_name="Время сказки")
    
    # Технические настройки
    timezone = models.CharField(max_length=50, default='Europe/Moscow', verbose_name="Часовой пояс")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Настройки уведомлений пользователя"
        verbose_name_plural = "Настройки уведомлений пользователей"
        
    def __str__(self):
        return f"Настройки {self.user.username}"
    
    def get_weekday_setting(self, weekday):
        """Получить настройку для дня недели (0=понедельник)"""
        weekday_fields = [
            'notify_monday', 'notify_tuesday', 'notify_wednesday',
            'notify_thursday', 'notify_friday', 'notify_saturday', 'notify_sunday'
        ]
        return getattr(self, weekday_fields[weekday])
    
    def is_quiet_time_now(self):
        """Проверить, сейчас ли тихие часы"""
        if not self.quiet_hours_enabled:
            return False
            
        now = timezone.now().time()
        
        if self.quiet_start <= self.quiet_end:
            # Обычный случай: 22:00 - 08:00
            return self.quiet_start <= now <= self.quiet_end
        else:
            # Через полночь: 22:00 - 08:00
            return now >= self.quiet_start or now <= self.quiet_end

class UserNotificationSubscription(models.Model):
    """Подписки пользователя на категории уведомлений"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_subscriptions')
    category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE)
    
    # Настройки подписки
    enabled = models.BooleanField(default=True, verbose_name="Включена")
    frequency = models.CharField(max_length=20, choices=[
        ('immediately', 'Сразу'),
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('custom', 'Настраиваемая'),
    ], default='daily', verbose_name="Частота")
    
    # Настройки времени
    preferred_time = models.TimeField(null=True, blank=True, verbose_name="Предпочитаемое время")
    max_daily_count = models.PositiveIntegerField(
        default=3, 
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Максимум в день"
    )
    
    # Персонализация
    priority = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Приоритет (1-10)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'category']
        verbose_name = "Подписка на уведомления"
        verbose_name_plural = "Подписки на уведомления"
        
    def __str__(self):
        return f"{self.user.username} → {self.category.title}"
