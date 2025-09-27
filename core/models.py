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

class MobileFeedback(TimeStampedModel):
    """Обратная связь через мобильное долгое нажатие"""
    
    FEEDBACK_TYPES = [
        ('bug', 'Нашёл ошибку'),
        ('feature', 'Предложить улучшение'),
        ('design', 'Дизайн и интерфейс'),
        ('content', 'Контент и материалы'),
        ('performance', 'Скорость работы'),
        ('other', 'Другое'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPES,
        verbose_name='Тип обращения'
    )
    message = models.TextField(
        verbose_name='Сообщение',
        validators=[MinLengthValidator(5)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='Приоритет'
    )
    
    # Техническая информация
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    url = models.URLField(
        blank=True,
        verbose_name='URL страницы'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адрес'
    )
    screen_resolution = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Разрешение экрана'
    )
    
    # Связь с пользователем (если авторизован)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    
    # Административные поля
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name='Заметки администратора'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_feedback',
        verbose_name='Назначено'
    )
    
    class Meta:
        verbose_name = 'Мобильная обратная связь'
        verbose_name_plural = 'Мобильная обратная связь'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.message[:50]}..."
    
    def mark_as_read(self):
        """Отметить как прочитанное"""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    @property
    def is_bug_report(self):
        """Является ли это сообщением об ошибке"""
        return self.feedback_type == 'bug'
    
    @property
    def is_high_priority(self):
        """Высокий приоритет"""
        return self.priority in ['high', 'urgent']
    
    def get_priority_color(self):
        """Цвет приоритета для админки"""
        colors = {
            'low': '#28a745',
            'medium': '#ffc107', 
            'high': '#fd7e14',
            'urgent': '#dc3545'
        }
        return colors.get(self.priority, '#6c757d')

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
    
    # ⭐ НОВЫЕ ПОЛЯ ДЛЯ АДРЕСА И РЕЖИМА РАБОТЫ
    work_hours = models.CharField(
        max_length=100,
        default='Пн-Пт: 9:00 - 18:00',
        verbose_name='Время работы',
        help_text='Например: Пн-Пт: 9:00 - 18:00'
    )
    work_hours_note = models.CharField(
        max_length=50,
        default='По московскому времени',
        verbose_name='Примечание к времени работы',
        blank=True
    )
    address_city = models.CharField(
        max_length=100,
        default='г. Москва',
        verbose_name='Город'
    )
    address_country = models.CharField(
        max_length=50,
        default='Россия',
        verbose_name='Страна'
    )
    address_full = models.TextField(
        blank=True,
        verbose_name='Полный адрес',
        help_text='Полный почтовый адрес (необязательно)'
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
    
    # Управление навигацией
    show_stories = models.BooleanField(
        default=True,
        verbose_name='Показывать "Видео-рассказы"'
    )
    show_books = models.BooleanField(
        default=True,
        verbose_name='Показывать "Библиотеку"'
    )
    show_audio = models.BooleanField(
        default=False,
        verbose_name='Показывать "Аудио"'
    )
    show_fairy_tales = models.BooleanField(
        default=False,
        verbose_name='Показывать "Сказки"'
    )
    show_shop = models.BooleanField(
        default=True,
        verbose_name='Показывать "Магазин"'
    )
    
    # Бейджи "В разработке" / "Скоро"
    stories_coming_soon = models.BooleanField(
        default=False,
        verbose_name='Рассказы: показать "Скоро"'
    )
    books_coming_soon = models.BooleanField(
        default=False,
        verbose_name='Библиотека: показать "Скоро"'
    )
    audio_coming_soon = models.BooleanField(
        default=True,
        verbose_name='Аудио: показать "Скоро"'
    )
    fairy_tales_coming_soon = models.BooleanField(
        default=True,
        verbose_name='Сказки: показать "Скоро"'
    )
    shop_coming_soon = models.BooleanField(
        default=False,
        verbose_name='Магазин: показать "Скоро"'
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