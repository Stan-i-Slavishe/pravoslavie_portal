from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    """Модель подписки"""
    SUBSCRIPTION_TYPES = [
        ('basic', 'Базовая'),
        ('premium', 'Премиум'),
        ('vip', 'VIP'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название")
    subscription_type = models.CharField(
        max_length=20, 
        choices=SUBSCRIPTION_TYPES, 
        default='basic',
        verbose_name="Тип подписки"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_months = models.PositiveIntegerField(default=1, verbose_name="Длительность (месяцев)")
    description = models.TextField(blank=True, verbose_name="Описание")
    features = models.JSONField(default=list, verbose_name="Возможности")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} ({self.get_subscription_type_display()})"


class UserSubscription(models.Model):
    """Подписка пользователя"""
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('cancelled', 'Отменена'),
        ('expired', 'Истекла'),
        ('pending', 'Ожидание оплаты'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name="Подписка")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Статус"
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    auto_renew = models.BooleanField(default=True, verbose_name="Автопродление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        verbose_name = "Подписка пользователя"
        verbose_name_plural = "Подписки пользователей"
        ordering = ['-created_at']
        unique_together = ['user', 'subscription', 'start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription.name}"
    
    @property
    def is_active(self):
        """Проверка активности подписки"""
        from django.utils import timezone
        return (
            self.status == 'active' and 
            self.start_date <= timezone.now() <= self.end_date
        )
    
    def get_status_display_class(self):
        """CSS класс для статуса"""
        status_classes = {
            'active': 'success',
            'cancelled': 'warning', 
            'expired': 'danger',
            'pending': 'info',
        }
        return status_classes.get(self.status, 'secondary')
