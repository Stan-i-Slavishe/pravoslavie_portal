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

class FastingPeriod(models.Model):
    """Периоды постов с их правилами для вечного календаря"""
    
    PERIOD_TYPES = [
        ('great_lent', 'Великий пост'),
        ('christmas_fast', 'Рождественский пост'),
        ('assumption_fast', 'Успенский пост'),
        ('peter_paul_fast', 'Петров пост'),
        ('apostles_fast', 'Апостольский пост'),
        ('weekly_fast', 'Еженедельный пост (ср/пт)'),
        ('one_day_fast', 'Однодневный пост'),
    ]
    
    name = models.CharField(max_length=50, choices=PERIOD_TYPES, verbose_name="Название")
    title = models.CharField(max_length=100, verbose_name="Отображаемое название")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Для фиксированных постов
    start_month = models.IntegerField(null=True, blank=True, verbose_name="Месяц начала")
    start_day = models.IntegerField(null=True, blank=True, verbose_name="День начала")
    end_month = models.IntegerField(null=True, blank=True, verbose_name="Месяц окончания")
    end_day = models.IntegerField(null=True, blank=True, verbose_name="День окончания")
    
    # Для переходящих постов (относительно Пасхи)
    easter_start_offset = models.IntegerField(
        null=True, blank=True, 
        verbose_name="Начало от Пасхи (дни)",
        help_text="Отрицательные значения - до Пасхи, положительные - после"
    )
    easter_end_offset = models.IntegerField(
        null=True, blank=True,
        verbose_name="Конец от Пасхи (дни)"
    )
    
    # Правила поста по дням недели (JSON)
    # Формат: {"monday": "strict_fast", "tuesday": "light_fast", ...}
    fasting_rules = models.JSONField(
        default=dict, 
        verbose_name="Правила поста",
        help_text="Правила по дням недели в формате JSON"
    )
    
    # Приоритет (чем выше число, тем выше приоритет)
    priority = models.IntegerField(
        default=1, 
        verbose_name="Приоритет",
        help_text="Для разрешения конфликтов между постами"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Период поста"
        verbose_name_plural = "Периоды постов"
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.title
    
    def is_active_for_date(self, target_date):
        """Проверить, активен ли пост для указанной даты"""
        if not self.is_active:
            return False
        
        year = target_date.year
        
        if self.easter_start_offset is not None:
            # Переходящий пост (относительно Пасхи)
            easter_date = OrthodoxEvent.calculate_easter(year)
            start_date = easter_date + timezone.timedelta(days=self.easter_start_offset)
            end_date = easter_date + timezone.timedelta(days=self.easter_end_offset)
        else:
            # Фиксированный пост
            try:
                start_date = timezone.date(year, self.start_month, self.start_day)
                end_date = timezone.date(year, self.end_month, self.end_day)
                
                # Обработка постов через новый год (например, Рождественский)
                if end_date < start_date:
                    if target_date >= start_date:
                        end_date = timezone.date(year + 1, self.end_month, self.end_day)
                    else:
                        start_date = timezone.date(year - 1, self.start_month, self.start_day)
            except ValueError:
                # Невалидная дата (например, 29 февраля в не високосном году)
                return False
        
        return start_date <= target_date <= end_date
    
    def get_fasting_type_for_weekday(self, weekday):
        """Получить тип поста для дня недели (0=понедельник)"""
        weekday_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_name = weekday_names[weekday]
        return self.fasting_rules.get(weekday_name, 'no_fast')

class OrthodoxEvent(models.Model):
    """Православные праздники и события"""
    
    EVENT_TYPES = [
        ('great_feast', 'Великий праздник'),
        ('major_feast', 'Большой праздник'), 
        ('minor_feast', 'Малый праздник'),
        ('fast_start', 'Начало поста'),
        ('fast_end', 'Окончание поста'),
        ('special_day', 'Особый день'),
        ('memorial', 'Поминовение'),
        ('saint', 'День святого'),
        ('icon', 'Икона'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, verbose_name="Тип события")
    
    # Дата (может быть переменной)
    month = models.IntegerField(verbose_name="Месяц")
    day = models.IntegerField(verbose_name="День")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год (если конкретный)")
    
    # Старый/новый стиль
    is_old_style = models.BooleanField(default=False, verbose_name="По старому стилю")
    
    # Переходящие праздники (Пасха и т.д.)
    is_movable = models.BooleanField(default=False, verbose_name="Переходящий праздник")
    easter_offset = models.IntegerField(null=True, blank=True, verbose_name="Сдвиг от Пасхи (дни)")
    
    # Метаданные
    icon_url = models.URLField(blank=True, verbose_name="Ссылка на икону")
    reading_url = models.URLField(blank=True, verbose_name="Ссылка на чтения")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Православное событие"
        verbose_name_plural = "Православные события"
        ordering = ['month', 'day']
    
    def __str__(self):
        return f"{self.day}.{self.month} - {self.title}"
    
    def get_date_for_year(self, year):
        """Получить дату события для конкретного года"""
        if self.is_movable:
            easter_date = self.calculate_easter(year)
            from datetime import timedelta
            return easter_date + timedelta(days=self.easter_offset or 0)
        else:
            from datetime import date
            return date(year, self.month, self.day)
    
    @staticmethod
    def calculate_easter(year):
        """Вычисление даты Пасхи по православному календарю"""
        from datetime import date, timedelta
        
        # Алгоритм вычисления православной Пасхи
        a = year % 19
        b = year % 4
        c = year % 7
        d = (19 * a + 15) % 30
        e = (2 * b + 4 * c + 6 * d + 6) % 7
        
        if d + e < 10:
            day = d + e + 22
            month = 3
        else:
            day = d + e - 9
            month = 4
        
        # Коррекция для старого стиля (+13 дней)
        easter_date = date(year, month, day)
        easter_date += timedelta(days=13)
        
        return easter_date
    
    @classmethod
    def get_events_for_date(cls, target_date):
        """Получить все события для конкретной даты"""
        events = []
        
        # Фиксированные события
        fixed_events = cls.objects.filter(
            is_movable=False,
            month=target_date.month,
            day=target_date.day
        )
        events.extend(fixed_events)
        
        # Переходящие события
        easter_date = cls.calculate_easter(target_date.year)
        movable_events = cls.objects.filter(is_movable=True)
        
        for event in movable_events:
            if event.easter_offset is not None:
                from datetime import timedelta
                event_date = easter_date + timedelta(days=event.easter_offset)
                if event_date == target_date:
                    events.append(event)
        
        return events

class DailyOrthodoxInfo(models.Model):
    """Ежедневная православная информация"""
    
    FASTING_TYPES = [
        ('no_fast', 'Поста нет'),
        ('light_fast', 'Обычный пост'),
        ('strict_fast', 'Строгий пост'),
        ('dry_eating', 'Сухоядение'),
        ('with_oil', 'Пост с маслом'),
        ('with_fish', 'Можно рыбу'),
        ('wine_oil', 'Вино и масло'),
        ('complete_fast', 'Полное воздержание'),
    ]
    
    # Дата
    month = models.IntegerField(verbose_name="Месяц")
    day = models.IntegerField(verbose_name="День")
    
    # Пост
    fasting_type = models.CharField(
        max_length=20, 
        choices=FASTING_TYPES,
        default='no_fast',
        verbose_name="Тип поста"
    )
    fasting_description = models.TextField(
        blank=True,
        verbose_name="Описание поста"
    )
    
    # Что можно есть
    allowed_food = models.TextField(
        blank=True,
        verbose_name="Что можно есть"
    )
    
    # Духовное наставление
    spiritual_note = models.TextField(
        blank=True,
        verbose_name="Духовное наставление"
    )
    
    # Чтения дня
    gospel_reading = models.TextField(
        blank=True,
        verbose_name="Евангельское чтение"
    )
    epistle_reading = models.TextField(
        blank=True,
        verbose_name="Апостольское чтение"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ежедневная православная информация"
        verbose_name_plural = "Ежедневная православная информация"
        unique_together = ['month', 'day']
        ordering = ['month', 'day']
    
    def __str__(self):
        return f"{self.day:02d}.{self.month:02d} - {self.get_fasting_type_display()}"
    
    @classmethod
    def get_info_for_date(cls, target_date):
        """Получить информацию для конкретной даты с вечным алгоритмом"""
        # Получаем базовую информацию
        try:
            daily_info = cls.objects.get(
                month=target_date.month,
                day=target_date.day
            )
            # Делаем копию для изменения
            from copy import deepcopy
            daily_info = deepcopy(daily_info)
        except cls.DoesNotExist:
            # Создаем базовую информацию
            daily_info = cls.get_default_info_for_date(target_date)
        
        # Применяем вечный алгоритм
        daily_info = cls.apply_eternal_algorithm(daily_info, target_date)
        
        return daily_info
    
    @classmethod
    def apply_eternal_algorithm(cls, daily_info, target_date):
        """Вечный алгоритм определения типа дня"""
        
        # 1. ПРИОРИТЕТ: Проверяем строгие постные дни (они НЕ отменяются праздниками)
        # 29 августа - Усекновение главы Иоанна Предтечи (строгий пост)
        if target_date.month == 8 and target_date.day == 29:
            daily_info.fasting_type = 'strict_fast'
            daily_info.fasting_description = 'Усекновение главы Иоанна Предтечи (строгий пост)'
            daily_info.allowed_food = 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)'
            daily_info.spiritual_note = '⚔️ Усекновение главы Иоанна Предтечи. Строгий постный день в память о мученической кончине святого Предтечи. Ореховый Спас отмечается, но пост сохраняется.'
            return daily_info
            
        # 11 сентября - Усекновение главы Иоанна Предтечи (по новому стилю)
        if target_date.month == 9 and target_date.day == 11:
            daily_info.fasting_type = 'strict_fast'
            daily_info.fasting_description = 'Усекновение главы Иоанна Предтечи (строгий пост)'
            daily_info.allowed_food = 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)'
            daily_info.spiritual_note = '⚔️ Усекновение главы Иоанна Предтечи. Строгий постный день в память о мученической кончине святого Предтечи.'
            return daily_info
            
        # Крестовоздвижение (27 сентября) - строгий пост
        if target_date.month == 9 and target_date.day == 27:
            daily_info.fasting_type = 'strict_fast'
            daily_info.fasting_description = 'Воздвижение Креста Господня (строгий пост)'
            daily_info.allowed_food = 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)'
            daily_info.spiritual_note = '✝️ Воздвижение Креста Господня. Строгий постный день в честь обретения и воздвижения Животворящего Креста.'
            return daily_info
        
        # 2. Проверяем великие праздники (отменяют обычный пост, но НЕ строгие постные дни)
        events = OrthodoxEvent.get_events_for_date(target_date)
        
        for event in events:
            if event.event_type in ['great_feast', 'major_feast']:
                # В великие праздники пост отменяется (кроме строгих постных дней выше)
                daily_info.fasting_type = 'no_fast'
                daily_info.fasting_description = f'Великий праздник: {event.title}'
                daily_info.allowed_food = 'Любая пища (праздник)'
                daily_info.spiritual_note = f'🎉 {event.title}! ' + (event.description or 'Великий православный праздник.')
                return daily_info
        
        # 2. Проверяем активные периоды постов
        active_fasting_periods = cls.get_active_fasting_periods(target_date)
        
        if active_fasting_periods:
            # Выбираем пост с наивысшим приоритетом
            main_fasting_period = max(active_fasting_periods, key=lambda p: p.priority)
            
            # Определяем тип поста по дню недели
            weekday = target_date.weekday()
            fasting_type = main_fasting_period.get_fasting_type_for_weekday(weekday)
            
            if fasting_type != 'no_fast':
                daily_info.fasting_type = fasting_type
                daily_info.fasting_description = main_fasting_period.title
                daily_info.allowed_food = cls.get_allowed_food_for_fasting_type(fasting_type)
                daily_info.spiritual_note = main_fasting_period.description or f'Период {main_fasting_period.title.lower()}. Время духовного очищения.'
                return daily_info
        
        # 3. Проверяем еженедельные постные дни
        weekday = target_date.weekday()
        if weekday in [2, 4]:  # Среда, пятница
            # Проверяем, не отменяется ли пост малым праздником
            minor_feast = any(event.event_type == 'minor_feast' for event in events)
            if not minor_feast:
                daily_info.fasting_type = 'light_fast'
                daily_info.fasting_description = 'Постный день (среда/пятница)'
                daily_info.allowed_food = 'Растительная пища, можно масло'
                daily_info.spiritual_note = 'Постный день. Время для молитвы и воздержания.'
                return daily_info
        
        # 4. Обычный день - оставляем как есть или базовое значение
        if daily_info.fasting_type is None:
            daily_info.fasting_type = 'no_fast'
            daily_info.fasting_description = 'Обычный день'
            daily_info.allowed_food = 'Любая пища'
            daily_info.spiritual_note = 'Обычный день. Благодарите Бога за все дары.'
        
        return daily_info
    
    @classmethod
    def get_active_fasting_periods(cls, target_date):
        """Получить все активные периоды постов для даты"""
        active_periods = []
        
        # Проверяем все периоды постов
        try:
            for period in FastingPeriod.objects.filter(is_active=True):
                if period.is_active_for_date(target_date):
                    active_periods.append(period)
        except Exception as e:
            # Если таблица еще не создана, пропускаем
            pass
        
        return active_periods
    
    @classmethod
    def get_allowed_food_for_fasting_type(cls, fasting_type):
        """Получить описание разрешенной пищи для типа поста"""
        food_descriptions = {
            'no_fast': 'Любая пища',
            'light_fast': 'Растительная пища, можно масло',
            'strict_fast': 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)',
            'dry_eating': 'Сухоядение: хлеб, сырые овощи и фрукты, орехи, вода',
            'with_oil': 'Растительная пища с маслом',
            'with_fish': 'Растительная пища, можно рыбу и морепродукты',
            'wine_oil': 'Растительная пища, можно вино и масло',
            'complete_fast': 'Полное воздержание от пищи и питья',
        }
        return food_descriptions.get(fasting_type, 'Информация не указана')
    
    @classmethod
    def get_default_info_for_date(cls, target_date):
        """Базовая информация для дня"""
        
        weekday = target_date.weekday()
        
        # Среда и пятница - постные дни
        if weekday in [2, 4]:  # Среда, пятница
            return cls(
                month=target_date.month,
                day=target_date.day,
                fasting_type='light_fast',
                fasting_description='Постный день (среда/пятница)',
                allowed_food='Растительная пища, можно масло',
                spiritual_note='Постный день. Время для молитвы и воздержания.'
            )
        else:
            return cls(
                month=target_date.month,
                day=target_date.day,
                fasting_type='no_fast',
                fasting_description='Обычный день',
                allowed_food='Любая пища',
                spiritual_note='Обычный день. Благодарите Бога за все дары.'
            )
    
    @classmethod
    def apply_special_periods(cls, daily_info, target_date):
        """Применить особые периоды (посты, праздники)"""
        
        # Проверяем великие праздники
        events = OrthodoxEvent.get_events_for_date(target_date)
        
        for event in events:
            if event.event_type == 'great_feast':
                # В великие праздники пост отменяется
                daily_info.fasting_type = 'no_fast'
                daily_info.fasting_description = f'Великий праздник: {event.title}'
                daily_info.allowed_food = 'Любая пища (праздник)'
                daily_info.spiritual_note = f'🎉 {event.title}! ' + (event.description or 'Великий православный праздник.')
                break
        
        return daily_info
