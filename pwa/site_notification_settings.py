# Добавим модель для настроек уведомлений сайта

from django.db import models

class SiteNotificationSettings(models.Model):
    """Глобальные настройки уведомлений сайта"""
    
    # Частота показа уведомлений
    FREQUENCY_CHOICES = [
        ('session', 'Один раз за сессию'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
        ('first_visit', 'Только при первом посещении'),
        ('disabled', 'Отключить'),
    ]
    
    welcome_notification_frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='weekly',
        verbose_name="Частота приветственных уведомлений"
    )
    
    welcome_notification_text = models.TextField(
        default="Добро пожаловать! Теперь вы будете получать уведомления о новом контенте",
        verbose_name="Текст приветственного уведомления"
    )
    
    welcome_notification_enabled = models.BooleanField(
        default=True,
        verbose_name="Показывать приветственные уведомления"
    )
    
    # Настройки для мобильных устройств
    mobile_notification_enabled = models.BooleanField(
        default=True,
        verbose_name="Показывать уведомления на мобильных"
    )
    
    # Время автоскрытия (в секундах)
    auto_hide_delay = models.IntegerField(
        default=8,
        verbose_name="Автоскрытие через (секунд)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Настройки уведомлений сайта"
        verbose_name_plural = "Настройки уведомлений сайта"
    
    def __str__(self):
        return f"Настройки уведомлений ({self.get_welcome_notification_frequency_display()})"
    
    @classmethod
    def get_settings(cls):
        """Получить настройки (создать если не существуют)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
