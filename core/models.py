from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import uuid

class TimeStampedModel(models.Model):
    """Абстрактная модель с временными метками"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        abstract = True

class Category(TimeStampedModel):
    """Категории контента для всего сайта"""
    
    CONTENT_TYPES = [
        ('story', 'Видео-рассказы'),
        ('book', 'Книги'),
        ('article', 'Статьи'),
        ('audio', 'Аудио'),
        ('product', 'Товары'),
        ('general', 'Общее'),
    ]
    
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name='Название категории',
        validators=[MinLengthValidator(2)]
    )
    slug = models.SlugField(
        max_length=120, 
        unique=True, 
        blank=True,
        verbose_name='URL-адрес'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Краткое описание категории'
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        default='general',
        verbose_name='Тип контента'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Иконка',
        help_text='Bootstrap иконка, например: bi-book'
    )
    color = models.CharField(
        max_length=7,
        default='#6c5ce7',
        verbose_name='Цвет',
        help_text='HEX код цвета для категории'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:category', kwargs={'slug': self.slug})
    
    @property
    def content_count(self):
        """Количество контента в категории"""
        # Будем реализовывать по мере добавления моделей контента
        return 0

class Tag(TimeStampedModel):
    """Теги для контента"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег',
        validators=[MinLengthValidator(2)]
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        verbose_name='URL-адрес'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Описание'
    )
    color = models.CharField(
        max_length=7,
        default='#74b9ff',
        verbose_name='Цвет тега'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:tag', kwargs={'slug': self.slug})

class ContactMessage(TimeStampedModel):
    """Сообщения из формы обратной связи"""
    
    SUBJECT_CHOICES = [
        ('general', 'Общие вопросы'),
        ('technical', 'Технические проблемы'),
        ('content', 'Предложения по контенту'),
        ('subscription', 'Вопросы по подписке'),
        ('cooperation', 'Сотрудничество'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('answered', 'Отвечено'),
        ('closed', 'Закрыто'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        verbose_name='Тема'
    )
    message = models.TextField(
        verbose_name='Сообщение',
        validators=[MinLengthValidator(10)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адрес'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name='Заметки администратора'
    )
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"
    
    def mark_as_read(self):
        """Отметить как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])

class SiteSettings(models.Model):
    """Настройки сайта"""
    
    site_name = models.CharField(
        max_length=100,
        default='Православный портал',
        verbose_name='Название сайта'
    )
    site_description = models.TextField(
        default='Духовные рассказы, книги и аудио для современного человека',
        verbose_name='Описание сайта'
    )
    contact_email = models.EmailField(
        default='info@pravoslavie-portal.ru',
        verbose_name='Контактный email'
    )
    contact_phone = models.CharField(
        max_length=20,
        default='+7 (800) 123-45-67',
        verbose_name='Контактный телефон'
    )
    social_telegram = models.URLField(
        blank=True,
        verbose_name='Telegram канал'
    )
    social_youtube = models.URLField(
        blank=True,
        verbose_name='YouTube канал'
    )
    social_vk = models.URLField(
        blank=True,
        verbose_name='ВКонтакте'
    )
    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name='Режим обслуживания'
    )
    maintenance_message = models.TextField(
        blank=True,
        verbose_name='Сообщение в режиме обслуживания'
    )
    analytics_yandex = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Yandex.Metrika ID'
    )
    analytics_google = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Google Analytics ID'
    )
    
    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
        
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Обеспечиваем единственность записи
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Получить настройки сайта"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings