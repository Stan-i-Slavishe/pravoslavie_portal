from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os

class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('', 'Не указан'),
    ]
    
    NOTIFICATION_PREFERENCES = [
        ('all', 'Все уведомления'),
        ('important', 'Только важные'),
        ('none', 'Отключить'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='profile')
    
    # Личная информация
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True, 
                              help_text='Рекомендуемый размер: 200x200 пикселей')
    bio = models.TextField('О себе', max_length=500, blank=True, 
                          help_text='Расскажите немного о себе')
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    
    # Православные интересы
    favorite_saints = models.CharField('Любимые святые', max_length=200, blank=True,
                                     help_text='Например: св. Николай Чудотворец, св. Сергий Радонежский')
    confession_frequency = models.CharField('Частота исповеди', max_length=50, blank=True,
                                          help_text='Например: раз в месяц, по большим праздникам')
    favorite_prayers = models.TextField('Любимые молитвы', blank=True, max_length=300)
    parish = models.CharField('Приход', max_length=150, blank=True,
                            help_text='Храм, который вы посещаете')
    
    # Настройки уведомлений
    email_notifications = models.CharField('Email уведомления', max_length=20, 
                                         choices=NOTIFICATION_PREFERENCES, default='important')
    newsletter_subscription = models.BooleanField('Подписка на рассылку', default=True)
    new_content_notifications = models.BooleanField('Уведомления о новом контенте', default=True)
    order_notifications = models.BooleanField('Уведомления о заказах', default=True)
    
    # Настройки чтения
    preferred_font_size = models.FloatField('Размер шрифта', default=1.0,
                                          help_text='От 0.8 до 2.0')
    preferred_theme = models.CharField('Тема оформления', max_length=20, default='light',
                                     choices=[
                                         ('light', 'Светлая'),
                                         ('dark', 'Темная'),
                                         ('sepia', 'Сепия')
                                     ])
    
    # Метаданные
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    last_activity = models.DateTimeField('Последняя активность', auto_now=True)
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Оптимизируем аватар после сохранения
        if self.avatar:
            self.resize_avatar()
    
    def resize_avatar(self):
        """Изменяет размер аватара до 200x200"""
        try:
            img = Image.open(self.avatar.path)
            if img.height > 200 or img.width > 200:
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                img.save(self.avatar.path)
        except Exception:
            pass  # Если не удалось обработать изображение, продолжаем
    
    def get_avatar_url(self):
        """Возвращает URL аватара или URL аватара по умолчанию"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.svg'
    
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username
    
    def get_display_name(self):
        """Возвращает имя для отображения"""
        full_name = self.get_full_name()
        if full_name != self.user.username and len(full_name) > 0:
            return full_name
        return self.user.username
    
    @property
    def age(self):
        """Возраст пользователя"""
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    def get_reading_stats(self):
        """Статистика чтения пользователя"""
        from books.models import ReadingSession, BookDownload
        from shop.models import Purchase
        
        stats = {
            'books_reading': ReadingSession.objects.filter(user=self.user).count(),
            'books_completed': ReadingSession.objects.filter(
                user=self.user, 
                current_page__gte=models.F('total_pages')
            ).count(),
            'books_downloaded': BookDownload.objects.filter(user=self.user).count(),
            'books_purchased': Purchase.objects.filter(user=self.user, product__product_type='book').count(),
        }
        return stats
    
    def get_activity_stats(self):
        """Статистика активности пользователя"""
        from shop.models import Order, Purchase
        from books.models import UserFavoriteBook
        
        stats = {
            'total_orders': Order.objects.filter(user=self.user).count(),
            'total_purchases': Purchase.objects.filter(user=self.user).count(),
            'favorite_books': UserFavoriteBook.objects.filter(user=self.user).count(),
            'total_spent': Order.objects.filter(
                user=self.user, 
                status='completed'
            ).aggregate(
                total=models.Sum('total_amount')
            )['total'] or 0,
        }
        return stats


# Сигнал для автоматического создания профиля
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаем профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняем профиль при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
